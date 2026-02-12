"""
Button component class with all Button-specific functions
"""
from playwright.sync_api import Page, Locator
from typing import Optional, Dict, Any
from framework.base import PropertyChecker
from components.button.locators import ButtonLocators
from utils.logger import logger

# Figma variant/state/size for tracking and verification (see button.properties)
BUTTON_VARIANTS = ("primary", "secondary", "ghost", "link", "warning")
BUTTON_STATES = ("active", "hover", "click", "disabled", "loading")
BUTTON_SIZES = ("large", "medium", "small")
THEME_MODES = ("light", "light-hc", "dark", "dark-hc")
BUTTON_COLOR_PROPERTIES = ("background-color", "color", "border-color")


class ButtonComponent(PropertyChecker):
    """
    Button component class with all Button-specific functionality
    """
    
    def __init__(self, page: Page, storybook_url: str = None):
        """
        Initialize Button component
        
        Args:
            page: Playwright page object
            storybook_url: Optional Storybook URL override
        """
        super().__init__(page, storybook_url)
        self.locators = ButtonLocators()
    
    def get_button(self, selector: Optional[str] = None) -> Locator:
        """
        Get button locator inside iframe
        
        Args:
            selector: Optional custom selector, defaults to main button selector
            
        Returns:
            Button locator (first match if multiple buttons found)
        """
        return self.get_story_locator(selector or self.locators.BUTTON)
    
    def click_button(self, selector: Optional[str] = None):
        """
        Click on button
        
        Args:
            selector: Optional custom selector, defaults to main button selector
        """
        button = self.get_button(selector)
        button.click()
        self.wait_for_animation()
    
    def click_button_by_text(self, text: str):
        """
        Click button by its text content
        
        Args:
            text: Text content of the button
        """
        selector = self.locators.button_with_text(text)
        self.click_button(selector)
    
    def is_button_enabled(self, selector: Optional[str] = None) -> bool:
        """
        Check if button is enabled
        
        Args:
            selector: Optional custom selector
            
        Returns:
            True if button is enabled, False otherwise
        """
        button = self.get_button(selector)
        return button.is_enabled()
    
    def is_button_disabled(self, selector: Optional[str] = None) -> bool:
        """
        Check if button is disabled
        
        Args:
            selector: Optional custom selector
            
        Returns:
            True if button is disabled, False otherwise
        """
        button = self.get_button(selector)
        aria_disabled = button.get_attribute("aria-disabled")
        return (
            button.is_disabled() or 
            button.get_attribute("disabled") is not None or
            aria_disabled == "true"
        )
    
    def get_button_text(self, selector: Optional[str] = None) -> str:
        """
        Get button text content
        
        Args:
            selector: Optional custom selector
            
        Returns:
            Button text content (from visible span if present, otherwise inner text)
        """
        button = self.get_button(selector)
        # Try to get text from visible span first (matches DOM structure)
        visible_span = button.locator("span.visible, span[class*='visible']")
        if visible_span.count() > 0:
            return visible_span.first.inner_text()
        return button.inner_text()
    
    def get_button_label(self, selector: Optional[str] = None) -> Optional[str]:
        """
        Get button label/aria-label
        
        Args:
            selector: Optional custom selector
            
        Returns:
            Button label from aria-label attribute, or None if not found
        """
        button = self.get_button(selector)
        aria_label = button.get_attribute("aria-label")
        return aria_label if aria_label else None
    
    def verify_button_text(self, expected_text: str, selector: Optional[str] = None):
        """
        Verify button text matches expected value
        
        Args:
            expected_text: Expected button text
            selector: Optional custom selector
        """
        actual_text = self.get_button_text(selector)
        assert actual_text == expected_text, \
            f"Button text mismatch: expected '{expected_text}', got '{actual_text}'"
    
    def verify_button_enabled(self, selector: Optional[str] = None):
        """
        Verify button is enabled
        
        Args:
            selector: Optional custom selector
        """
        assert self.is_button_enabled(selector), "Button should be enabled"
    
    def verify_button_disabled(self, selector: Optional[str] = None):
        """
        Verify button is disabled
        
        Args:
            selector: Optional custom selector
        """
        assert self.is_button_disabled(selector), "Button should be disabled"
    
    def verify_button_variant(self, variant: str, selector: Optional[str] = None):
        """
        Verify button variant/style
        
        Args:
            variant: Expected variant (primary, secondary, danger, etc.)
            selector: Optional custom selector
        """
        button = self.get_button(selector)
        button_class = button.get_attribute("class") or ""
        # Check for bg-{variant} class pattern (matches DOM structure)
        expected_class = f"bg-{variant.lower()}"
        assert expected_class in button_class, \
            f"Button variant mismatch: expected class '{expected_class}' in '{button_class}'"

    def load_button_variant_properties(
        self, variant: str, state: str, size: str
    ) -> Dict[str, str]:
        """
        Load expected CSS properties for a variant/state/size from button.properties.

        Args:
            variant: primary, secondary, ghost, link, warning
            state: active, hover, disabled, click, loading
            size: large, medium, small

        Returns:
            Dict of CSS property name -> expected value (e.g. {"background-color": "rgb(...)", ...})
        """
        return self.load_component_properties_for_variant(
            variant=variant, state=state, size=size, component_name="button"
        )

    def load_button_variant_color_properties(
        self, variant: str, state: str, size: str
    ) -> Dict[str, str]:
        """
        Load only color properties (background-color, color, border-color) for a variant/state/size
        from button.properties.
        """
        all_props = self.load_button_variant_properties(variant, state, size)
        return {k: v for k, v in all_props.items() if k in BUTTON_COLOR_PROPERTIES}

    def hover_button(self, selector: Optional[str] = None):
        """
        Hover over button
        
        Args:
            selector: Optional custom selector
        """
        button = self.get_button(selector)
        button.hover()
        self.wait_for_animation()
    
    def is_button_loading(self, selector: Optional[str] = None) -> bool:
        """
        Check if button is in loading state
        
        Args:
            selector: Optional custom selector
            
        Returns:
            True if button is loading, False otherwise
        """
        button = self.get_button(selector)
        aria_busy = button.get_attribute("aria-busy")
        return aria_busy == "true"
    
    def is_button_active(self, selector: Optional[str] = None) -> bool:
        """
        Check if button is active
        
        Args:
            selector: Optional custom selector
            
        Returns:
            True if button is active, False otherwise
        """
        button = self.get_button(selector)
        data_active = button.get_attribute("data-active")
        return data_active == "true"
    
    def verify_button_loading(self, selector: Optional[str] = None):
        """
        Verify button is in loading state
        
        Args:
            selector: Optional custom selector
        """
        assert self.is_button_loading(selector), "Button should be in loading state"
    
    def verify_button_not_loading(self, selector: Optional[str] = None):
        """
        Verify button is not in loading state
        
        Args:
            selector: Optional custom selector
        """
        assert not self.is_button_loading(selector), "Button should not be in loading state"
    
    def verify_button_active(self, selector: Optional[str] = None):
        """
        Verify button is active
        
        Args:
            selector: Optional custom selector
        """
        assert self.is_button_active(selector), "Button should be active"
    
    def get_button_from_storybook(self) -> Locator:
        """
        Get button from Storybook root container (inside iframe)
        
        Returns:
            Button locator within Storybook root inside iframe
        """
        return self.get_story_locator(self.locators.BUTTON_IN_STORYBOOK)
    
    def update_button_label(self, new_label: str, selector: Optional[str] = None):
        """
        Update button label via Storybook controls
        
        Args:
            new_label: New label value
            selector: Optional custom selector (not used for controls)
        """
        from framework.base import StorybookControlsManager
        controls_manager = StorybookControlsManager(self.page)
        controls_manager.update_control_via_api("main-button--button-story", "label", new_label)
        self.wait_for_animation()
    
    def click_actions_tab(self):
        """
        Click on the Actions tab in Storybook panel to view action logs
        """
        actions_tab = self.page.locator(self.locators.ACTIONS_TAB)
        actions_tab.click()
        self.wait_for_animation(0.3)
    
    def is_actions_tab_active(self) -> bool:
        """
        Check if Actions tab is currently active
        
        Returns:
            True if Actions tab is active, False otherwise
        """
        try:
            actions_tab = self.page.locator(self.locators.ACTIONS_TAB)
            return "tabbutton-active" in (actions_tab.get_attribute("class") or "")
        except:
            return False
    
    def get_action_items_from_panel(self) -> list:
        """
        Get all action items from the Actions panel
        
        Returns:
            List of action item text content
        """
        try:
            # Ensure Actions tab is active
            if not self.is_actions_tab_active():
                self.click_actions_tab()
            
            # Wait for panel content to be visible
            self.page.wait_for_selector(self.locators.ACTIONS_PANEL_CONTENT, timeout=3000)
            
            # Get all action items
            action_items = self.page.locator(self.locators.ACTION_ITEMS)
            count = action_items.count()
            
            actions = []
            for i in range(count):
                item = action_items.nth(i)
                if item.is_visible():
                    actions.append(item.inner_text())
            
            return actions
        except Exception as e:
            logger.warning(f"⚠️ Error getting action items: {e}")
            return []
    
    def get_action_count_from_panel(self, action_name: str) -> int:
        """
        Get the count of a specific action from the Actions panel UI
        
        Args:
            action_name: Name of the action (e.g., 'onClick')
            
        Returns:
            Number of times the action appears in the panel
        """
        try:
            actions = self.get_action_items_from_panel()
            count = sum(1 for action in actions if action_name in action)
            return count
        except:
            return 0
    
    def verify_action_in_panel(self, action_name: str, expected_count: int = 1, timeout: int = 3000) -> bool:
        """
        Verify that an action appears in the Actions panel
        
        Args:
            action_name: Name of the action to verify (e.g., 'onClick')
            expected_count: Expected number of times the action should appear (default: 1)
            timeout: Maximum time to wait in milliseconds
            
        Returns:
            True if action is found with expected count, False otherwise
        """
        import time
        start_time = time.time()
        
        # Ensure Actions tab is active
        if not self.is_actions_tab_active():
            self.click_actions_tab()
        
        while (time.time() - start_time) * 1000 < timeout:
            try:
                count = self.get_action_count_from_panel(action_name)
                if count >= expected_count:
                    return True
            except Exception as e:
                logger.warning(f"⚠️ Error verifying action: {e}")
            
            time.sleep(0.2)  # Small delay before checking again
        
        return False
    
    def clear_actions_panel(self):
        """
        Clear all actions from the Actions panel by clicking the Clear button
        """
        try:
            # Ensure Actions tab is active
            if not self.is_actions_tab_active():
                self.click_actions_tab()
            
            # Wait for clear button to be visible
            clear_button = self.page.locator(self.locators.ACTION_CLEAR_BUTTON)
            clear_button.wait_for(state="visible", timeout=2000)
            clear_button.click()
            self.wait_for_animation(0.3)
        except Exception as e:
            logger.warning(f"⚠️ Error clearing actions panel: {e}")
    
    def wait_for_action_in_panel(self, action_name: str, timeout: int = 5000):
        """
        Wait for an action to appear in the Actions panel
        
        Args:
            action_name: Name of the action to wait for
            timeout: Maximum time to wait in milliseconds
            
        Raises:
            TimeoutError if action doesn't appear within timeout
        """
        import time
        start_time = time.time()
        
        # Ensure Actions tab is active
        if not self.is_actions_tab_active():
            self.click_actions_tab()
        
        while (time.time() - start_time) * 1000 < timeout:
            try:
                count = self.get_action_count_from_panel(action_name)
                if count > 0:
                    return
            except Exception as e:
                pass
            
            time.sleep(0.2)
        
        raise TimeoutError(f"Action '{action_name}' did not appear in Actions panel within {timeout}ms")

