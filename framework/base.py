"""
Base classes for Storybook testing framework
"""
from playwright.sync_api import Page, expect, FrameLocator, Locator
from typing import Optional, Dict, Any, Callable, TypeVar
import time

T = TypeVar("T")
import re
from pathlib import Path
from urllib.parse import quote
import sys
import json

# Load configuration
from framework.config_loader import get_config
from utils.logger import logger

config = get_config()


class StorybookBase:
    """Base class for Storybook test interactions. Story content lives in an iframe."""
    
    IFRAME_SELECTOR = "iframe"
    
    def __init__(self, page: Page, storybook_url: str = None):
        self.page = page
        self.storybook_url = storybook_url or config.STORYBOOK_URL
        self.timeout = config.STORYBOOK_TIMEOUT
    
    def get_story_frame_locator(self) -> FrameLocator:
        """Frame locator for the story iframe (all components render here)."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)
    
    def get_story_locator(self, selector: str) -> Locator:
        """Locator for an element inside the story iframe."""
        return self.get_story_frame_locator().locator(selector).first

    def _evaluate_in_story(self, selector: str, body: str, *extra_args) -> Any:
        """Run JS in story iframe. In body, 'el' is the element (or null), 'args' is [selector, ...extra_args]. Return value is passed through."""
        all_args = [selector] + list(extra_args)
        js = """(args) => {
            const doc = document.querySelector('iframe').contentDocument;
            if (!doc) return null;
            const el = doc.querySelector(args[0]);
            """ + body + """
        }"""
        return self.page.evaluate(js, all_args)

    @staticmethod
    def build_storybook_args_query(args: Dict[str, Any]) -> str:
        """
        Build the args query string for Storybook URL.
        Example: children:Primary+Button+label;variant:secondary;loading:!true;disabled:!true
        Format: key:value pairs separated by ; . Booleans as !true/!false, string spaces as +.
        """
        if not args:
            return ""
        parts = []
        for key, value in args.items():
            if value is True:
                vstr = "!true"
            elif value is False:
                vstr = "!false"
            elif isinstance(value, str):
                vstr = value.replace(" ", "+")
            elif isinstance(value, (int, float)):
                vstr = str(value)
            else:
                vstr = quote(json.dumps(value), safe="")
            parts.append(f"{key}:{vstr}")
        return ";".join(parts)

    @staticmethod
    def build_storybook_globals_query(globals_dict: Dict[str, str]) -> str:
        """Build globals query for Storybook URL, e.g. themeMode:light."""
        if not globals_dict:
            return ""
        return ";".join(f"{k}:{v}" for k, v in globals_dict.items())

    def navigate_to_story(
        self,
        story_path: str,
        theme_mode: Optional[str] = None,
        args: Optional[Dict[str, Any]] = None,
        globals_: Optional[Dict[str, str]] = None,
        wait_for_selector: Optional[str] = None,
    ):
        """
        Navigate to a story in Storybook (full UI; story content loads in iframe).
        All components are inside the story iframe.
        Controls can be set via URL args (e.g. args=children:Label;variant:primary;disabled:!true).

        Args:
            story_path: Story id (e.g. "main-button--primary").
            theme_mode: Optional theme (light, dark, etc.) – added as globals.
            args: Optional dict of story args/controls to set in URL (e.g. {"variant": "primary", "disabled": True}).
            globals_: Optional dict of Storybook globals (e.g. {"themeMode": "light"}). Overrides theme_mode if both set.
            wait_for_selector: Optional selector to wait for inside the story iframe.
        """
        url = f"{self.storybook_url}/?path=/story/{story_path}"
        if args:
            args_str = self.build_storybook_args_query(args)
            if args_str:
                # Preserve ; : + for Storybook args format (e.g. variant:primary;loading:!true)
                url = f"{url}&args={quote(args_str, safe=';:+')}"
        if globals_:
            globals_str = self.build_storybook_globals_query(globals_)
            if globals_str:
                url = f"{url}&globals={quote(globals_str)}"
        elif theme_mode:
            url = f"{url}&globals={quote(f'themeMode:{theme_mode}')}"
        logger.info(f"\n{'='*60}")
        logger.info(f"Navigating to: {url}")
        logger.info(f"{'='*60}\n")
        try:
            response = self.page.goto(url, wait_until="domcontentloaded", timeout=min(self.timeout, 10000))
            logger.info(f"✅ Initial page load complete (status: {response.status if response else 'N/A'})")
            try:
                self.page.wait_for_load_state("networkidle", timeout=min(self.timeout - 5000, 20000))
                logger.info(f"✅ Network idle")
            except Exception as e:
                logger.warning(f"⚠️ Network not idle (continuing anyway): {e}")
        except Exception as e:
            logger.error(f"\n❌ Error navigating to {url}")
            logger.error(f"Error type: {type(e).__name__}: {e}")
            logger.error(f"Current URL: {self.page.url}")
            raise
        logger.info("Waiting for Storybook UI to load...")
        self.page.wait_for_selector("body", timeout=10000)
        self.page.wait_for_selector("iframe", timeout=10000)
        logger.info("✅ Storybook page and story iframe ready")
        if wait_for_selector:
            wait_ms = min(self.timeout, 8000)
            self.page.frame_locator("iframe").locator(wait_for_selector).first.wait_for(
                state="visible", timeout=wait_ms
            )
            logger.info("✅ Story iframe selector ready: %s", wait_for_selector)
        
    def get_story_element(self, selector: str = ".sb-story"):
        """Get the main story element"""
        return self.page.locator(selector)
    
    def wait_for_animation(self, duration: float = 0.5):
        """Wait for animations to complete"""
        time.sleep(duration)
        
    def get_component_state(self) -> Dict[str, Any]:
        """Get the current state of the component.

        Returns:
            Dict with keys: url (str), title (str), viewport (dict with width, height in pixels).

        Example:
            {
                "url": "https://localhost:6006/?path=/story/button--primary",
                "title": "Storybook",
                "viewport": {"width": 1280, "height": 720}
            }
        """
        return self.page.evaluate("""() => {
            return {
                url: window.location.href,
                title: document.title,
                viewport: {
                    width: window.innerWidth,
                    height: window.innerHeight
                }
            };
        }""")
    
    def set_viewport(self, width: int, height: int):
        """Set viewport size"""
        self.page.set_viewport_size({"width": width, "height": height})
        time.sleep(0.3)  # Wait for viewport change


class VisualRegressionBase(StorybookBase):
    """Base class for visual regression testing"""
    
    def __init__(self, page: Page, storybook_url: str = None):
        super().__init__(page, storybook_url)
        self.screenshots_dir = config.SCREENSHOTS_DIR
        
    def take_screenshot(
        self, 
        story_path: str, 
        name: str = "screenshot",
        full_page: bool = True,
        selector: Optional[str] = None
    ) -> Path:
        """
        Take a screenshot for visual regression testing
        
        Args:
            story_path: Path to the story
            name: Name for the screenshot file
            full_page: Whether to capture full page or viewport
            selector: Optional selector to capture specific element
            
        Returns:
            Path to the screenshot file
        """
        # Create directory structure: screenshots/{story_path}/
        story_dir = self.screenshots_dir / story_path.replace("--", "/")
        story_dir.mkdir(parents=True, exist_ok=True)
        
        screenshot_path = story_dir / f"{name}.png"
        
        if selector:
            element = self.get_story_locator(selector)
            element.screenshot(path=str(screenshot_path), timeout=self.timeout)
        elif full_page:
            self.page.screenshot(path=str(screenshot_path), full_page=True)
        else:
            self.page.screenshot(path=str(screenshot_path), full_page=False)
            
        return screenshot_path
    
    def compare_screenshot(
        self,
        story_path: str,
        name: str,
        threshold: float = None,
        full_page: bool = True,
        selector: Optional[str] = None
    ):
        """
        Compare screenshot with baseline using Playwright's built-in visual comparison
        
        Args:
            story_path: Path to the story
            name: Name for the screenshot
            threshold: Pixel difference threshold (0-1)
            full_page: Whether to capture full page
            selector: Optional selector to capture specific element
        """
        threshold = threshold or config.VISUAL_THRESHOLD
        
        if selector:
            expect(self.get_story_locator(selector)).to_have_screenshot(
                f"{story_path}/{name}.png",
                threshold=threshold,
                timeout=self.timeout
            )
        elif full_page:
            expect(self.page).to_have_screenshot(
                f"{story_path}/{name}.png",
                threshold=threshold,
                timeout=self.timeout
            )
        else:
            expect(self.page).to_have_screenshot(
                f"{story_path}/{name}.png",
                threshold=threshold,
                timeout=self.timeout
            )


class InteractionBase(StorybookBase):
    """Base class for interaction testing. All selectors target the story iframe."""
    
    def click(self, selector: str, wait_for_selector: Optional[str] = None):
        """Click an element and optionally wait for a selector"""
        self.get_story_locator(selector).click(timeout=self.timeout)
        if wait_for_selector:
            self.get_story_frame_locator().locator(wait_for_selector).first.wait_for(state="visible", timeout=self.timeout)
        self.wait_for_animation()
    
    def fill(self, selector: str, value: str):
        """Fill an input field"""
        self.get_story_locator(selector).fill(value, timeout=self.timeout)
        self.wait_for_animation()
    
    def select_option(self, selector: str, value: str):
        """Select an option from a dropdown"""
        self.get_story_locator(selector).select_option(value, timeout=self.timeout)
        self.wait_for_animation()
    
    def hover(self, selector: str):
        """Hover over an element"""
        self.get_story_locator(selector).hover(timeout=self.timeout)
        self.wait_for_animation()
    
    def keyboard_press(self, selector: str, key: str):
        """Press a key on an element"""
        self.get_story_locator(selector).press(key, timeout=self.timeout)
        self.wait_for_animation()
    
    def wait_for_text(self, selector: str, text: str):
        """Wait for text to appear in an element"""
        expect(self.get_story_locator(selector)).to_contain_text(text, timeout=self.timeout)
    
    def wait_for_visible(self, selector: str):
        """Wait for element to be visible"""
        expect(self.get_story_locator(selector)).to_be_visible(timeout=self.timeout)
    
    def wait_for_hidden(self, selector: str):
        """Wait for element to be hidden"""
        expect(self.get_story_locator(selector)).to_be_hidden(timeout=self.timeout)
    
    def get_text(self, selector: str) -> str:
        """Get text content of an element"""
        return self.get_story_locator(selector).text_content(timeout=self.timeout) or ""
    
    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """Get attribute value of an element"""
        return self.get_story_locator(selector).get_attribute(attribute, timeout=self.timeout)
    
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        return self.get_story_locator(selector).is_visible(timeout=5000)


class StateBase(StorybookBase):
    """Base class for state testing. All selectors target the story iframe."""
    
    def get_component_props(self) -> Dict[str, Any]:
        """Get component props from React/Vue component (if accessible)"""
        return self.page.evaluate("""() => {
            // Try to get component state from common frameworks
            if (window.__STORYBOOK_STORY_STORE__) {
                return window.__STORYBOOK_STORY_STORE__.getState();
            }
            return {};
        }""")
    
    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """Get attribute value of an element in the story iframe."""
        return self.get_story_locator(selector).get_attribute(attribute, timeout=self.timeout)
    
    def get_text(self, selector: str) -> str:
        """Get text content of an element in the story iframe."""
        return self.get_story_locator(selector).text_content(timeout=self.timeout) or ""
    
    def verify_state(self, expected_state: Dict[str, Any], selector: str = ".sb-story"):
        """Verify component state matches expected state"""
        actual_state = self.get_component_state()
        for key, value in expected_state.items():
            assert actual_state.get(key) == value, \
                f"State mismatch for {key}: expected {value}, got {actual_state.get(key)}"
    
    def verify_class(self, selector: str, expected_class: str):
        """Verify element has expected class"""
        classes = self.get_attribute(selector, "class") or ""
        assert expected_class in classes, \
            f"Expected class '{expected_class}' not found in '{classes}'"
    
    def verify_attribute(self, selector: str, attribute: str, expected_value: str):
        """Verify element attribute matches expected value"""
        actual_value = self.get_attribute(selector, attribute)
        assert actual_value == expected_value, \
            f"Attribute '{attribute}' mismatch: expected '{expected_value}', got '{actual_value}'"
    
    def verify_text_content(self, selector: str, expected_text: str):
        """Verify element text content matches expected text"""
        actual_text = self.get_text(selector)
        assert expected_text in actual_text, \
            f"Text mismatch: expected '{expected_text}' in '{actual_text}'"
    
    def verify_count(self, selector: str, expected_count: int):
        """Verify number of elements matching selector in story iframe"""
        count = self.get_story_frame_locator().locator(selector).count()
        assert count == expected_count, \
            f"Element count mismatch: expected {expected_count}, got {count}"


class PropertyChecker(StorybookBase):
    """Base class for checking component properties, colors, dimensions, and text. All selectors target the story iframe."""

    def wait_for_visible(self, selector: str):
        """Wait for element to be visible"""
        expect(self.get_story_locator(selector)).to_be_visible(timeout=self.timeout)

    def hold_click_state(
        self,
        selector: str,
        duration_sec: float = 0.3,
        callback: Optional[Callable[[], T]] = None,
    ) -> Optional[T]:
        """
        Keep element in :active (pressed) state by pressing mouse down, then run callback or wait.
        Use this to capture declared/computed styles for click state (which is too fast to capture after a normal click).

        Args:
            selector: CSS selector for the element (in story iframe).
            duration_sec: How long to hold if no callback (default 0.3s).
            callback: If provided, run this while the mouse is down; mouse is released after it returns.

        Returns:
            Return value of callback if provided, else None.

        Example:
            def capture():
                return button.get_declared_style(button.locators.BUTTON, "background-color")
            value = button.hold_click_state(button.locators.BUTTON, callback=capture)
        """
        locator = self.get_story_locator(selector)
        expect(locator).to_be_visible(timeout=self.timeout)
        box = locator.bounding_box()
        if not box:
            raise ValueError(f"Element not visible or has no bounding box: {selector}")
        x = box["x"] + box["width"] / 2
        y = box["y"] + box["height"] / 2
        self.page.mouse.move(x, y)
        self.page.mouse.down()
        try:
            time.sleep(0.05)  # let :active apply
            if callback is not None:
                return callback()
            time.sleep(duration_sec)
            return None
        finally:
            self.page.mouse.up()

    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """Get attribute value of an element"""
        return self.get_story_locator(selector).get_attribute(attribute, timeout=self.timeout)
    
    def get_computed_style(self, selector: str, property_name: str) -> str:
        """
        Get computed CSS property value for an element (in story iframe).
        
        Args:
            selector: CSS selector for the element
            property_name: CSS property name (e.g., 'backgroundColor', 'color', 'width')
            
        Returns:
            Computed CSS property value as string
        """
        return self._evaluate_in_story(
            selector,
            "if (!el) return null; const s = window.getComputedStyle(el); return s.getPropertyValue(args[1]) || s[args[1]] || '';",
            property_name,
        ) or ""

    def get_declared_style(self, selector: str, property_name: str) -> str:
        """
        Get the declared CSS property value for an element (as in the Styles tab), e.g. var(--color-green-100).
        Resolves cascade by document order; does not compute specificity.

        Args:
            selector: CSS selector for the element
            property_name: CSS property name in kebab-case (e.g. 'background-color', 'color')

        Returns:
            Declared value string (e.g. 'var(--color-green-100)', '16px') or '' if not set.

        Example:
            get_declared_style(button_selector, 'background-color')  -> 'var(--color-green-100)'
        """
        return self._evaluate_in_story(
            selector,
            """
            if (!el) return '';
            const prop = args[1];
            let value = '';
            function collectRules(sheet) {
              try {
                if (!sheet || !sheet.cssRules) return;
                for (let i = 0; i < sheet.cssRules.length; i++) {
                  const r = sheet.cssRules[i];
                  if (r.selectorText) {
                    try {
                      if (el.matches(r.selectorText)) {
                        const v = r.style.getPropertyValue(prop);
                        if (v) value = v;
                      }
                    } catch (_) {}
                  } else if (r.cssRules) collectRules(r);
                }
              } catch (_) {}
            }
            for (let i = 0; i < doc.styleSheets.length; i++) collectRules(doc.styleSheets[i]);
            const inline = el.style.getPropertyValue(prop);
            if (inline) value = inline;
            return value;
            """,
            property_name,
        ) or ""

    def get_all_computed_styles(self, selector: str) -> Dict[str, str]:
        """
        Get all computed CSS properties for an element (in story iframe).
        
        Args:
            selector: CSS selector for the element
            
        Returns:
            Dictionary of all computed CSS properties
        """
        return self._evaluate_in_story(
            selector,
            """if (!el) return {}; const s = window.getComputedStyle(el); const r = {};
            for (let i = 0; i < s.length; i++) { const p = s[i]; r[p] = s.getPropertyValue(p); }
            return r;""",
        ) or {}
    
    def verify_property(self, selector: str, property_name: str, expected_value: str, tolerance: float = None):
        """
        Verify CSS property value matches expected value
        
        Args:
            selector: CSS selector for the element
            property_name: CSS property name (e.g., 'display', 'position', 'font-size')
            expected_value: Expected property value
            tolerance: Optional tolerance for numeric values (e.g., for width/height)
        """
        actual_value = self.get_computed_style(selector, property_name)
        
        # Normalize values (remove extra spaces, convert to lowercase for comparison)
        actual_normalized = actual_value.strip().lower() if actual_value else ""
        expected_normalized = expected_value.strip().lower()
        
        # Handle numeric values with tolerance
        if tolerance is not None:
            try:
                actual_num = float(actual_normalized.replace('px', '').replace('%', ''))
                expected_num = float(expected_normalized.replace('px', '').replace('%', ''))
                assert abs(actual_num - expected_num) <= tolerance, \
                    f"Property '{property_name}' mismatch: expected {expected_value}, got {actual_value}"
                return
            except (ValueError, AttributeError):
                pass  # Fall through to string comparison
        
        assert actual_normalized == expected_normalized, \
            f"Property '{property_name}' mismatch: expected '{expected_value}', got '{actual_value}'"
    
    def get_color(self, selector: str, color_type: str = "color") -> str:
        """
        Get color value (text color, background color, or border color)
        
        Args:
            selector: CSS selector for the element
            color_type: Type of color to get - 'color', 'backgroundColor', 'borderColor'
            
        Returns:
            Color value in RGB/RGBA format
        """
        color_property = {
            "color": "color",
            "text": "color",
            "background": "backgroundColor",
            "bg": "backgroundColor",
            "border": "borderColor"
        }.get(color_type.lower(), color_type)
        
        return self.get_computed_style(selector, color_property)
    
    def verify_color(self, selector: str, expected_color: str, color_type: str = "color"):
        """
        Verify color matches expected value
        
        Args:
            selector: CSS selector for the element
            expected_color: Expected color value (can be hex, rgb, rgba, or named color)
            color_type: Type of color to check - 'color', 'background', 'border'
        """
        actual_color = self.get_color(selector, color_type)
        
        # Normalize colors for comparison
        actual_normalized = self._normalize_color(actual_color)
        expected_normalized = self._normalize_color(expected_color)
        
        assert actual_normalized == expected_normalized, \
            f"Color mismatch ({color_type}): expected '{expected_color}' ({expected_normalized}), got '{actual_color}' ({actual_normalized})"
    
    def _normalize_color(self, color: str) -> str:
        """
        Normalize color value to RGB format for comparison
        
        Args:
            color: Color value in any format
            
        Returns:
            Normalized RGB/RGBA string
        """
        if not color:
            return ""
        
        # Convert to RGB using browser's computed style
        rgb_value = self.page.evaluate(f"""() => {{
            const div = document.createElement('div');
            div.style.color = '{color}';
            document.body.appendChild(div);
            const computed = window.getComputedStyle(div).color;
            document.body.removeChild(div);
            return computed;
        }}""")
        
        return rgb_value.lower().strip()
    
    def get_dimensions(self, selector: str) -> Dict[str, float]:
        """
        Get element dimensions (width, height, and bounding box) in story iframe.
        
        Args:
            selector: CSS selector for the element
            
        Returns:
            Dictionary with width, height, top, left, right, bottom
        """
        return self._evaluate_in_story(
            selector,
            """if (!el) return {}; const r = el.getBoundingClientRect();
            return { width: r.width, height: r.height, top: r.top, left: r.left, right: r.right, bottom: r.bottom,
                clientWidth: el.clientWidth, clientHeight: el.clientHeight, offsetWidth: el.offsetWidth,
                offsetHeight: el.offsetHeight, scrollWidth: el.scrollWidth, scrollHeight: el.scrollHeight };""",
        ) or {}
    
    def verify_width(self, selector: str, expected_width: float, tolerance: float = 1.0):
        """
        Verify element width matches expected value
        
        Args:
            selector: CSS selector for the element
            expected_width: Expected width in pixels
            tolerance: Allowed difference in pixels (default: 1.0)
        """
        dimensions = self.get_dimensions(selector)
        actual_width = dimensions.get("width", 0)
        
        assert abs(actual_width - expected_width) <= tolerance, \
            f"Width mismatch: expected {expected_width}px, got {actual_width}px"
    
    def verify_height(self, selector: str, expected_height: float, tolerance: float = 1.0):
        """
        Verify element height matches expected value
        
        Args:
            selector: CSS selector for the element
            expected_height: Expected height in pixels
            tolerance: Allowed difference in pixels (default: 1.0)
        """
        dimensions = self.get_dimensions(selector)
        actual_height = dimensions.get("height", 0)
        
        assert abs(actual_height - expected_height) <= tolerance, \
            f"Height mismatch: expected {expected_height}px, got {actual_height}px"
    
    def verify_dimensions(self, selector: str, expected_width: float = None, expected_height: float = None, tolerance: float = 1.0):
        """
        Verify element dimensions match expected values
        
        Args:
            selector: CSS selector for the element
            expected_width: Expected width in pixels (optional)
            expected_height: Expected height in pixels (optional)
            tolerance: Allowed difference in pixels (default: 1.0)
        """
        dimensions = self.get_dimensions(selector)
        
        if expected_width is not None:
            actual_width = dimensions.get("width", 0)
            assert abs(actual_width - expected_width) <= tolerance, \
                f"Width mismatch: expected {expected_width}px, got {actual_width}px"
        
        if expected_height is not None:
            actual_height = dimensions.get("height", 0)
            assert abs(actual_height - expected_height) <= tolerance, \
                f"Height mismatch: expected {expected_height}px, got {actual_height}px"
    
    def update_label(self, selector: str, new_text: str):
        """
        Update label/text content of an element (in story iframe).
        
        Args:
            selector: CSS selector for the element
            new_text: New text content to set
        """
        self._evaluate_in_story(
            selector,
            "if (el) { el.textContent = args[1] ?? ''; }",
            new_text,
        )
        self.wait_for_animation()

    def update_label_by_inner_html(self, selector: str, new_html: str):
        """
        Update label/text content using innerHTML (in story iframe).
        
        Args:
            selector: CSS selector for the element
            new_html: New HTML content to set
        """
        self._evaluate_in_story(
            selector,
            "if (el) { el.innerHTML = args[1] ?? ''; }",
            new_html,
        )
        self.wait_for_animation()

    def update_input_value(self, selector: str, new_value: str):
        """
        Update input field value (in story iframe).
        
        Args:
            selector: CSS selector for the input element
            new_value: New value to set
        """
        self.get_story_locator(selector).fill(new_value, timeout=self.timeout)
        self.wait_for_animation()

    def get_component_text(self, selector: str) -> str:
        """
        Get text content of a component (in story iframe).
        
        Args:
            selector: CSS selector for the element
            
        Returns:
            Text content of the element
        """
        return self.get_story_locator(selector).text_content(timeout=self.timeout) or ""

    def get_component_inner_text(self, selector: str) -> str:
        """
        Get inner text content of a component (in story iframe).
        
        Args:
            selector: CSS selector for the element
            
        Returns:
            Inner text content of the element
        """
        return self.get_story_locator(selector).inner_text(timeout=self.timeout) or ""
    
    def verify_component_text(self, selector: str, expected_text: str, exact_match: bool = False):
        """
        Verify component text matches expected text
        
        Args:
            selector: CSS selector for the element
            expected_text: Expected text content
            exact_match: If True, text must match exactly; if False, expected_text can be substring
        """
        actual_text = self.get_component_text(selector)
        
        if exact_match:
            assert actual_text.strip() == expected_text.strip(), \
                f"Text mismatch (exact): expected '{expected_text}', got '{actual_text}'"
        else:
            assert expected_text in actual_text, \
                f"Text mismatch: expected '{expected_text}' to be in '{actual_text}'"
    
    def verify_component_inner_text(self, selector: str, expected_text: str, exact_match: bool = False):
        """
        Verify component inner text matches expected text
        
        Args:
            selector: CSS selector for the element
            expected_text: Expected inner text content
            exact_match: If True, text must match exactly; if False, expected_text can be substring
        """
        actual_text = self.get_component_inner_text(selector)
        
        if exact_match:
            assert actual_text.strip() == expected_text.strip(), \
                f"Inner text mismatch (exact): expected '{expected_text}', got '{actual_text}'"
        else:
            assert expected_text in actual_text, \
                f"Inner text mismatch: expected '{expected_text}' to be in '{actual_text}'"
    
    def verify_multiple_properties(self, selector: str, properties: Dict[str, Any]):
        """
        Verify multiple CSS properties at once
        
        Args:
            selector: CSS selector for the element
            properties: Dictionary of property names and expected values
                        Values can be strings or tuples (value, tolerance) for numeric properties
        """
        for property_name, expected in properties.items():
            if isinstance(expected, tuple):
                expected_value, tolerance = expected
                self.verify_property(selector, property_name, expected_value, tolerance)
            else:
                self.verify_property(selector, property_name, expected)

    def get_component_locator(self, selector: str) -> Locator:
        """Alias for get_story_locator (component in story iframe)."""
        return self.get_story_locator(selector)

    def wait_for_component_ready(self, selector: str, timeout: int = 5000):
        """Wait for element to be visible in the story iframe."""
        self.get_story_locator(selector).wait_for(state="visible", timeout=timeout)

    def _components_dir(self) -> Path:
        """Project components directory (components/)."""
        return Path(__file__).resolve().parent.parent / "components"

    def load_component_properties(self, component_name: str) -> Dict[str, str]:
        """
        Load component properties from a .properties file in components/<component_name>/.
        If component_name is None, infers from class name (e.g. ButtonComponent -> 'button').
        """
        
        components_dir = self._components_dir()
        component_dir = components_dir / component_name
        properties_file = component_dir / f"{component_name}.properties"
        properties = {}
        if not properties_file.exists():
            logger.warning("⚠️ Properties file not found: %s", properties_file)
            return properties
        try:
            with open(properties_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, value = line.split("=", 1)
                        key, value = key.strip(), value.strip()
                        if not key.startswith("css-var."):
                            properties[key] = value
        except Exception as e:
            logger.error("❌ Error loading properties from %s: %s", properties_file, e)
        return properties

    def load_component_properties_for_variant(
        self,
        variant: str,
        state: str,
        size: str,
        component_name: str,
        properties_filename: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Load component properties for a specific variant/state/size from a variant .properties file.
        File format: <variant>.<state>.<size>.<css-property>=value (e.g. primary.active.large.background-color=#fff).
        Returns a dict of CSS property name -> value for use with verify_component_properties.

        Args:
            variant: e.g. primary, secondary, ghost, link, warning
            state: e.g. active, hover, disabled, click, loading
            size: e.g. large, medium, small
            component_name: e.g. 'button'; inferred from class name if None
            properties_filename: e.g. 'button.properties'; default is '{component_name}.properties'
        """

        if properties_filename is None:
            properties_filename = f"{component_name}.properties"

        components_dir = self._components_dir()
        component_dir = components_dir / component_name
        properties_file = component_dir / properties_filename
        prefix = f"{variant.lower()}.{state.lower()}.{size.lower()}."
        result = {}
        if not properties_file.exists():
            logger.warning("⚠️ Variant properties file not found: %s", properties_file)
            return result
        try:
            with open(properties_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    key, value = key.strip(), value.strip()
                    if key.startswith(prefix):
                        prop_name = key[len(prefix) :]
                        result[prop_name] = value
        except Exception as e:
            logger.error("❌ Error loading variant properties from %s: %s", properties_file, e)
        return result

    def load_component_properties_by_prefix(
        self,
        component_name: str,
        prefix: str,
        properties_filename: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Load component properties where key starts with the given prefix.
        Returns a dict of (key without prefix) -> value for use with verify_component_properties.

        Args:
            component_name: e.g. 'checkbox'
            prefix: e.g. 'icon.unchecked.active.'
            properties_filename: optional; default is '{component_name}.properties'
        """
        if properties_filename is None:
            properties_filename = f"{component_name}.properties"
        components_dir = self._components_dir()
        component_dir = components_dir / component_name
        properties_file = component_dir / properties_filename
        result = {}
        if not properties_file.exists():
            logger.warning("⚠️ Properties file not found: %s", properties_file)
            return result
        try:
            with open(properties_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    key, value = key.strip(), value.strip()
                    if key.startswith(prefix):
                        prop_name = key[len(prefix) :]
                        result[prop_name] = value
        except Exception as e:
            logger.error("❌ Error loading properties from %s: %s", properties_file, e)
        return result

    def load_css_variables_from_file(self, file_path: Path) -> Dict[str, str]:
        """Load CSS variables from a .properties file (--var: value; or --var=value;)."""
        css_variables = {}
        if not file_path.exists():
            logger.warning("Properties file not found: %s", file_path)
            return css_variables
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if ":" in line:
                        parts = line.split(":", 1)
                        if len(parts) == 2:
                            var_name = parts[0].strip()
                            value = parts[1].strip().rstrip(";").strip()
                            if var_name.startswith("--"):
                                css_variables[var_name] = value
                    elif "=" in line:
                        key, value = line.split("=", 1)
                        key, value = key.strip(), value.strip()
                        if key.startswith("--"):
                            css_variables[key] = value
            if not css_variables:
                logger.warning("No CSS variables found in %s", file_path.name)
        except Exception as e:
            logger.error("Error loading %s: %s", file_path.name, e)
        return css_variables

    def load_css_variables(self, component_name: Optional[str] = None) -> Dict[str, str]:
        """Load CSS variable definitions from components/css-variables.properties."""
        return self.load_css_variables_from_file(self._components_dir() / "css-variables.properties")

    def _css_values_match(self, expected: Any, actual: str) -> bool:
        """Compare expected vs actual CSS value; treat 0 and 0px (and similar length equivalents) as equal."""
        e_str = str(expected).strip().lower()
        a_str = str(actual).strip().lower() if actual is not None else ""
        if e_str == a_str:
            return True
        # Normalize length values: "0" and "0px" both mean zero
        try:
            e_clean = e_str.replace("px", "").replace("%", "").strip()
            a_clean = a_str.replace("px", "").replace("%", "").strip()
            if e_clean == "":
                e_clean = "0"
            if a_clean == "":
                a_clean = "0"
            if float(e_clean) == float(a_clean):
                return True
        except (ValueError, TypeError):
            pass
        return False

    def verify_component_properties(self, properties: Dict[str, Any] = None, selector: str = None):
        """
        Verify multiple component properties (from .properties or dict). Excludes var(--...) values.
        selector: required CSS selector for the component element.
        """
        if selector is None:
            raise ValueError("selector parameter is required for verify_component_properties")
        if properties is None:
            properties = self.load_component_properties()
        regular_properties = {
            k: v for k, v in properties.items()
            if not (isinstance(v, str) and v.startswith("var(--"))
        }
        if not regular_properties:
            return
        component = self.get_story_locator(selector)
        mismatches = []
        logger.info("Verifying %s component properties", len(regular_properties))
        for property_name, expected in regular_properties.items():
            js_code = """
                (element, propName) => {
                    const styles = window.getComputedStyle(element);
                    return styles.getPropertyValue(propName) || styles[propName] || '';
                }
            """
            actual_value = component.evaluate(js_code, property_name)
            if isinstance(expected, tuple):
                expected_value, tolerance = expected
                if tolerance is not None:
                    try:
                        actual_num = float(str(actual_value).replace("px", "").replace("%", ""))
                        expected_num = float(str(expected_value).replace("px", "").replace("%", ""))
                        if abs(actual_num - expected_num) > tolerance:
                            mismatches.append(f"Property '{property_name}' mismatch: expected {expected_value} (±{tolerance}), got {actual_value}")
                    except ValueError:
                        if not self._css_values_match(expected_value, actual_value):
                            mismatches.append(f"Property '{property_name}' mismatch: expected {expected_value}, got {actual_value}")
                else:
                    if not self._css_values_match(expected_value, actual_value):
                        mismatches.append(f"Property '{property_name}' mismatch: expected {expected_value}, got {actual_value}")
            else:
                if not self._css_values_match(expected, actual_value):
                    mismatches.append(f"Property '{property_name}' mismatch: expected {expected}, got {actual_value}")
        if mismatches:
            raise AssertionError("Found %s property mismatch(es):\n  - %s" % (len(mismatches), "\n  - ".join(mismatches)))

    def verify_component_css_variables(self, properties: Dict[str, Any] = None, selector: str = None):
        """
        Verify CSS variable properties (var(--name)) against components/css-variables.properties.
        selector: required CSS selector for the component element.
        """
        if selector is None:
            raise ValueError("selector parameter is required for verify_component_css_variables")
        component = self.get_story_locator(selector)
        if properties is None:
            properties = self.load_component_properties()
        css_var_properties = {
            k: v for k, v in properties.items()
            if isinstance(v, str) and v.startswith("var(--")
        }
        if not css_var_properties:
            return
        css_variables = self.load_css_variables()
        mismatches = []
        js_code = """
            (element, args) => {
                const propName = args.propName;
                const expectedValue = args.expectedValue;
                const styles = window.getComputedStyle(element);
                const actualValue = styles.getPropertyValue(propName) || styles[propName] || '';
                function normalizeColor(color) {
                    if (!color) return color;
                    if (color.startsWith('#')) {
                        const hex = color.slice(1);
                        const r = parseInt(hex.slice(0, 2), 16);
                        const g = parseInt(hex.slice(2, 4), 16);
                        const b = parseInt(hex.slice(4, 6), 16);
                        return `rgb(${r}, ${g}, ${b})`;
                    }
                    return color;
                }
                const varMatch = expectedValue.match(/var\\(--([^)]+)\\)/);
                if (varMatch) {
                    const varName = '--' + varMatch[1];
                    let rawVarValue = null;
                    try {
                        const rootStyles = window.getComputedStyle(document.documentElement);
                        rawVarValue = rootStyles.getPropertyValue(varName).trim();
                        if (!rawVarValue) rawVarValue = styles.getPropertyValue(varName).trim();
                    } catch (e) { rawVarValue = styles.getPropertyValue(varName).trim(); }
                    const temp = document.createElement('div');
                    temp.style.setProperty(propName, `var(${varName})`);
                    document.body.appendChild(temp);
                    const resolvedValue = window.getComputedStyle(temp).getPropertyValue(propName);
                    document.body.removeChild(temp);
                    const normalizedActual = normalizeColor(actualValue);
                    const normalizedResolved = normalizeColor(resolvedValue);
                    return { actual: normalizedActual || actualValue, resolved: normalizedResolved || resolvedValue || rawVarValue || null, rawVar: rawVarValue || null };
                }
                return { actual: actualValue, resolved: null, rawVar: null };
            }
        """
        for property_name, expected in css_var_properties.items():
            result = component.evaluate(js_code, {"propName": property_name, "expectedValue": expected})
            actual_value = result.get("actual", "")
            resolved_value = result.get("resolved")
            raw_var_value = result.get("rawVar")
            var_name_with_dash = "--" + expected[4:-1]
            predefined_value = css_variables.get(var_name_with_dash)
            if not predefined_value:
                mismatches.append(
                    "Property '%s': No predefined value for CSS variable '%s' in css-variables.properties." % (property_name, var_name_with_dash)
                )
                continue
            if resolved_value or actual_value:
                def _norm_color(s):
                    if not s:
                        return s
                    s = str(s).strip().lower()
                    if s.startswith("rgb"):
                        m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", s)
                        if m:
                            return "rgb(%s, %s, %s)" % m.groups()
                        return s
                    if s.startswith("#"):
                        h = s[1:]
                        if len(h) == 3:
                            h = "".join([c * 2 for c in h])
                        if len(h) == 6:
                            return "rgb(%d, %d, %d)" % (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
                    return s

                def _norm_hex(s):
                    if not s:
                        return s
                    s = str(s).strip().lower()
                    if s.startswith("#"):
                        h = s[1:]
                        if len(h) == 3:
                            h = "".join([c * 2 for c in h])
                        return "#" + h
                    return s

                actual_normalized = _norm_color(actual_value)
                resolved_normalized = _norm_color(resolved_value)
                predefined_normalized = _norm_color(predefined_value)
                if raw_var_value:
                    if _norm_hex(raw_var_value) != _norm_hex(predefined_value):
                        mismatches.append(
                            "Property '%s': CSS variable '%s' value '%s' does not match predefined '%s'" % (property_name, var_name_with_dash, raw_var_value, predefined_value)
                        )
                if str(actual_normalized).strip() != str(predefined_normalized).strip():
                    mismatches.append(
                        "Property '%s': Computed '%s' does not match predefined '%s' (var(%s))" % (property_name, actual_value, predefined_value, expected[4:-1])
                    )
            else:
                mismatches.append("Property '%s': CSS variable '%s' not found or could not be resolved" % (property_name, expected))
        if mismatches:
            raise AssertionError("Found %s CSS variable mismatch(es):\n  - %s" % (len(mismatches), "\n  - ".join(mismatches)))
    def get_all_css_variables_from_root(self) -> Dict[str, str]:
        """Extract all CSS variables from :root in the story iframe."""
        frame = self.get_story_frame_locator()
        js_code = """
            () => {
                const cssVars = {};
                try {
                    const rootStyles = window.getComputedStyle(document.documentElement);
                    try {
                        for (let i = 0; i < document.styleSheets.length; i++) {
                            try {
                                const sheet = document.styleSheets[i];
                                if (!sheet.cssRules) continue;
                                for (let rule of sheet.cssRules) {
                                    if (rule.selectorText && (rule.selectorText === ':root' || rule.selectorText === 'html' || rule.selectorText === 'html:root' || rule.selectorText.includes(':root'))) {
                                        if (rule.style) {
                                            for (let j = 0; j < rule.style.length; j++) {
                                                const prop = rule.style[j];
                                                if (prop && prop.startsWith('--')) {
                                                    const value = rule.style.getPropertyValue(prop).trim();
                                                    if (value) cssVars[prop] = value;
                                                }
                                            }
                                        }
                                    }
                                }
                            } catch (e) {}
                        }
                    } catch (e) {}
                    try {
                        const allProps = Array.from(rootStyles);
                        for (let prop of allProps) {
                            if (prop && prop.startsWith('--')) {
                                const value = rootStyles.getPropertyValue(prop).trim();
                                if (value && !cssVars.hasOwnProperty(prop)) cssVars[prop] = value;
                            }
                        }
                    } catch (e) {}
                } catch (e) {}
                return cssVars;
            }
        """
        try:
            body_locator = frame.locator("body")
            css_vars = body_locator.evaluate(js_code)
            return {k: v for k, v in (css_vars or {}).items() if v and v.strip()}
        except Exception as e:
            logger.warning("⚠️ Error extracting CSS variables from :root: %s", e)
            return {}

    def verify_all_css_variables(self, story_path: str, selector: str) -> Dict[str, Any]:
        """
        Verify CSS variables from components/css-variables.properties exist in the story iframe :root.
        Fails on value mismatches or variables in .properties missing in browser.
        """
        expected_url_patterns = [f"/?path=/story/{story_path}"]
        current_url = self.page.url
        needs_navigation = not any(p in current_url for p in expected_url_patterns)
        if needs_navigation:
            logger.info("Navigating to story: %s", story_path)
            self.navigate_to_story(story_path, wait_for_selector=selector)
        else:
            self.wait_for_component_ready(selector)
        browser_vars = self.get_all_css_variables_from_root()
        browser_vars = {k: v for k, v in browser_vars.items() if not k.startswith("--tw-")}
        properties_vars = self.load_css_variables()
        mismatches = []
        missing_in_browser = {}
        matched = {}

        def _norm_color(s):
            if not s:
                return s
            s = str(s).strip().lower()
            if s.startswith("rgb"):
                m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", s)
                if m:
                    return "rgb(%s, %s, %s)" % m.groups()
                return s
            if s.startswith("#"):
                h = s[1:]
                if len(h) == 3:
                    h = "".join([c * 2 for c in h])
                if len(h) == 6:
                    return "rgb(%d, %d, %d)" % (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
            return s

        def _norm_hex(s):
            if not s:
                return s
            s = str(s).strip().lower()
            if s.startswith("#"):
                h = s[1:]
                if len(h) == 3:
                    h = "".join([c * 2 for c in h])
                return "#" + h
            return s

        for var_name, predefined_value in properties_vars.items():
            browser_value = browser_vars.get(var_name)
            if browser_value is None:
                try:
                    frame = self.get_story_frame_locator()
                    body_locator = frame.locator("body")
                    browser_value = body_locator.evaluate(
                        "(varName) => { try { return window.getComputedStyle(document.documentElement).getPropertyValue(varName).trim() || null; } catch (e) { return null; } }",
                        var_name,
                    )
                except Exception:
                    browser_value = None
            if browser_value:
                browser_n = _norm_color(browser_value)
                predefined_n = _norm_color(predefined_value)
                browser_h = _norm_hex(browser_value)
                predefined_h = _norm_hex(predefined_value)
                if browser_n == predefined_n or browser_h == predefined_h or str(browser_value).strip().lower() == str(predefined_value).strip().lower():
                    matched[var_name] = {"browser_value": browser_value, "properties_value": predefined_value}
                else:
                    mismatches.append({"variable": var_name, "browser_value": browser_value, "properties_value": predefined_value, "type": "value_mismatch"})
            else:
                missing_in_browser[var_name] = predefined_value
        missing_in_properties = {k: v for k, v in browser_vars.items() if k not in properties_vars}
        if mismatches or missing_in_browser:
            parts = []
            if mismatches:
                parts.append("%s value mismatch(es)" % len(mismatches))
            if missing_in_browser:
                parts.append("%s variable(s) in .properties not found in browser" % len(missing_in_browser))
            msg = "CSS variable verification failed: " + ", ".join(parts)
            details = []
            for m in mismatches:
                details.append("  %s: browser='%s', properties='%s'" % (m["variable"], m["browser_value"], m["properties_value"]))
            for var_name, pv in missing_in_browser.items():
                details.append("  • %s: %s" % (var_name, pv))
            if details:
                msg += "\n" + "\n".join(details)
            raise AssertionError(msg)
        return {"mismatches": mismatches, "missing_in_properties": missing_in_properties, "missing_in_browser": missing_in_browser, "matched": matched}


class StorybookControlsManager(StorybookBase):
    """Base class for managing Storybook controls (args/props)"""
    
    def navigate_to_story_with_controls(self, story_path: str):
        """
        Navigate to a story in the full Storybook UI (not iframe) to access controls

        Args:
            story_path: Path to the story (e.g., "main-button--button-story")

        Note: This is now the default behavior of navigate_to_story().
        This method is kept for backward compatibility.
        """
        self.navigate_to_story(story_path)

    def navigate_to_story_with_args(
        self,
        story_path: str,
        args: Dict[str, Any],
        globals_: Optional[Dict[str, str]] = None,
        wait_for_selector: Optional[str] = None,
    ):
        """
        Navigate to a story with controls set via URL args (no API/UI needed).
        Example URL: ?path=/story/main-button--primary&args=variant:secondary;loading:!true;disabled:!true

        Args:
            story_path: Story id (e.g. "main-button--primary").
            args: Dict of story args/controls (e.g. {"variant": "primary", "disabled": True, "children": "Label"}).
            globals_: Optional globals (e.g. {"themeMode": "light"}).
            wait_for_selector: Optional selector to wait for inside the story iframe.
        """
        self.navigate_to_story(
            story_path,
            args=args,
            globals_=globals_,
            wait_for_selector=wait_for_selector,
        )

    
    def update_control_via_ui(self, story_path: str, arg_name: str, value: Any):
        """
        Update control via UI interaction (fallback method)
        
        Args:
            story_path: Path to the story
            arg_name: Name of the control
            value: New value
        """
        # Navigate to full Storybook UI
        self.navigate_to_story_with_controls(story_path)
        
        # Find the control input in the controls panel
        # Storybook controls are typically in a panel with data attributes
        control_selector = f"[data-testid='control-{arg_name}'], [name='{arg_name}'], input[name*='{arg_name}']"
        
        try:
            # Wait for control to be available
            self.page.wait_for_selector(control_selector, timeout=5000)
            
            # Determine control type and update accordingly
            control_element = self.page.locator(control_selector).first
            
            # Check if it's a checkbox
            input_type = control_element.get_attribute("type")
            
            if input_type == "checkbox":
                if value:
                    control_element.check()
                else:
                    control_element.uncheck()
            elif input_type in ["text", "number", "email", "url"]:
                control_element.fill(str(value))
            elif input_type == "color":
                control_element.fill(str(value))
            else:
                # Try select dropdown
                try:
                    control_element.select_option(str(value))
                except:
                    # Fallback: fill as text
                    control_element.fill(str(value))
            
            self.wait_for_animation()
        except Exception as e:
            raise Exception(f"Failed to update control '{arg_name}' via UI: {str(e)}")
    
    def get_control_value(self, story_path: str, arg_name: str) -> Any:
        """
        Get current value of a Storybook control
        
        Args:
            story_path: Path to the story
            arg_name: Name of the control/arg
            
        Returns:
            Current value of the control
        """
        self.navigate_to_story(story_path)
        
        # Try to get value from Storybook API
        result = self.page.evaluate(f"""() => {{
            if (window.parent && window.parent.__STORYBOOK_STORY_STORE__) {{
                const store = window.parent.__STORYBOOK_STORY_STORE__;
                const storyId = '{story_path}';
                const currentStory = store.getState().storiesHash[storyId];
                if (currentStory && currentStory.args) {{
                    return {{ success: true, value: currentStory.args['{arg_name}'] }};
                }}
            }}
            
            if (window.__STORYBOOK_STORY_STORE__) {{
                const store = window.__STORYBOOK_STORY_STORE__;
                const storyId = '{story_path}';
                const currentStory = store.getState().storiesHash[storyId];
                if (currentStory && currentStory.args) {{
                    return {{ success: true, value: currentStory.args['{arg_name}'] }};
                }}
            }}
            
            return {{ success: false }};
        }}""")
        
        if result.get("success"):
            return result.get("value")
        else:
            # Fallback: get from UI
            return self._get_control_value_via_ui(story_path, arg_name)
    
    def _get_control_value_via_ui(self, story_path: str, arg_name: str) -> Any:
        """Get control value from UI (fallback)"""
        self.navigate_to_story_with_controls(story_path)
        
        control_selector = f"[data-testid='control-{arg_name}'], [name='{arg_name}'], input[name*='{arg_name}']"
        
        try:
            self.page.wait_for_selector(control_selector, timeout=5000)
            control_element = self.page.locator(control_selector).first
            
            input_type = control_element.get_attribute("type")
            
            if input_type == "checkbox":
                return control_element.is_checked()
            elif input_type in ["text", "number", "email", "url", "color"]:
                return control_element.input_value()
            else:
                # Try select
                try:
                    return control_element.input_value()
                except:
                    return control_element.text_content()
        except Exception as e:
            raise Exception(f"Failed to get control value '{arg_name}' via UI: {str(e)}")
    
    def update_multiple_controls(
        self,
        story_path: str,
        controls: Dict[str, Any],
        wait_for_selector: Optional[str] = None,
    ):
        """
        Update multiple controls at once.
        By default uses URL args (single navigation with all controls set);

        Args:
            story_path: Path to the story
            controls: Dictionary of control names and values to update
            wait_for_selector: When use_url_args=True, optional selector to wait for after load.
        """
        self.navigate_to_story(
            story_path,
            args=controls,
            wait_for_selector=wait_for_selector,
            )
        self.wait_for_animation()
    
    def get_all_control_values(self, story_path: str) -> Dict[str, Any]:
        """
        Get all current control values for a story
        
        Args:
            story_path: Path to the story
            
        Returns:
            Dictionary of all control names and their current values
        """
        self.navigate_to_story(story_path)
        
        result = self.page.evaluate(f"""() => {{
            if (window.parent && window.parent.__STORYBOOK_STORY_STORE__) {{
                const store = window.parent.__STORYBOOK_STORY_STORE__;
                const storyId = '{story_path}';
                const currentStory = store.getState().storiesHash[storyId];
                if (currentStory && currentStory.args) {{
                    return {{ success: true, args: currentStory.args }};
                }}
            }}
            
            if (window.__STORYBOOK_STORY_STORE__) {{
                const store = window.__STORYBOOK_STORY_STORE__;
                const storyId = '{story_path}';
                const currentStory = store.getState().storiesHash[storyId];
                if (currentStory && currentStory.args) {{
                    return {{ success: true, args: currentStory.args }};
                }}
            }}
            
            return {{ success: false }};
        }}""")
        
        if result.get("success"):
            return result.get("args", {})
        else:
            return {}
    
    def reset_controls_to_defaults(self, story_path: str):
        """
        Reset all controls to their default values
        
        Args:
            story_path: Path to the story
        """
        self.navigate_to_story(story_path)
        
        # Get initial args (defaults)
        result = self.page.evaluate(f"""() => {{
            if (window.parent && window.parent.__STORYBOOK_STORY_STORE__) {{
                const store = window.parent.__STORYBOOK_STORY_STORE__;
                const storyId = '{story_path}';
                const currentStory = store.getState().storiesHash[storyId];
                if (currentStory && currentStory.initialArgs) {{
                    store.updateStoryArgs(storyId, currentStory.initialArgs);
                    return {{ success: true }};
                }}
            }}
            
            if (window.__STORYBOOK_STORY_STORE__) {{
                const store = window.__STORYBOOK_STORY_STORE__;
                const storyId = '{story_path}';
                const currentStory = store.getState().storiesHash[storyId];
                if (currentStory && currentStory.initialArgs) {{
                    store.updateStoryArgs(storyId, currentStory.initialArgs);
                    return {{ success: true }};
                }}
            }}
            
            return {{ success: false }};
        }}""")
        
        if not result.get("success"):
            raise Exception("Failed to reset controls to defaults")
        
        self.wait_for_animation()
    
    def get_component_text(self, selector: str) -> str:
        """
        Get text content of a component (helper method)
        
        Args:
            selector: CSS selector for the element
            
        Returns:
            Text content of the element
        """
        return self.page.locator(selector).text_content(timeout=self.timeout) or ""

