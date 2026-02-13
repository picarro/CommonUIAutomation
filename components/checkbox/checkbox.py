"""
Checkbox component class with all Checkbox-specific functions
"""
from playwright.sync_api import Page, Locator
from typing import Dict, Optional
from framework.base import PropertyChecker
from components.checkbox.locators import CheckboxLocators


class CheckboxComponent(PropertyChecker):
    """
    Checkbox component class with all Checkbox-specific functionality
    """
    
    def __init__(self, page: Page, storybook_url: str = None):
        """Initialize Checkbox component"""
        super().__init__(page, storybook_url)
        self.locators = CheckboxLocators()
    
    def get_checkbox(self, selector: Optional[str] = None) -> Locator:
        """Get checkbox icon (input) locator inside iframe. Use CHECKBOX_ICON by default."""
        return self.get_story_locator(selector or self.locators.CHECKBOX_ICON)
    
    def click_checkbox(self, selector: Optional[str] = None):
        """Click checkbox to toggle state"""
        checkbox = self.get_checkbox(selector)
        checkbox.click()
        self.wait_for_animation()
    
    def check_checkbox(self, selector: Optional[str] = None):
        """Check the checkbox (set to checked)"""
        checkbox = self.get_checkbox(selector)
        if not checkbox.is_checked():
            checkbox.check()
        self.wait_for_animation()
    
    def uncheck_checkbox(self, selector: Optional[str] = None):
        """Uncheck the checkbox (set to unchecked)"""
        checkbox = self.get_checkbox(selector)
        if checkbox.is_checked():
            checkbox.uncheck()
        self.wait_for_animation()
    
    def is_checked(self, selector: Optional[str] = None) -> bool:
        """Check if checkbox is checked"""
        checkbox = self.get_checkbox(selector)
        return checkbox.is_checked()
    
    def is_unchecked(self, selector: Optional[str] = None) -> bool:
        """Check if checkbox is unchecked"""
        return not self.is_checked(selector)
    
    def verify_checked(self, selector: Optional[str] = None):
        """Verify checkbox is checked"""
        assert self.is_checked(selector), "Checkbox should be checked"
    
    def verify_unchecked(self, selector: Optional[str] = None):
        """Verify checkbox is unchecked"""
        assert self.is_unchecked(selector), "Checkbox should be unchecked"
    
    def is_checkbox_disabled(self, selector: Optional[str] = None) -> bool:
        """Check if checkbox is disabled"""
        checkbox = self.get_checkbox(selector)
        return checkbox.is_disabled()
    
    def verify_checkbox_enabled(self, selector: Optional[str] = None):
        """Verify checkbox is enabled (not disabled)"""
        assert not self.is_checkbox_disabled(selector), "Checkbox should be enabled"
    
    def verify_checkbox_disabled(self, selector: Optional[str] = None):
        """Verify checkbox is disabled"""
        assert self.is_checkbox_disabled(selector), "Checkbox should be disabled"
    
    def hover_checkbox(self, selector: Optional[str] = None):
        """Hover over the checkbox"""
        checkbox = self.get_checkbox(selector)
        checkbox.hover()
        self.wait_for_animation(0.3)
    
    def load_checkbox_icon_properties(self, variant: str, state: str) -> Dict[str, str]:
        """
        Load expected CSS properties for the checkbox icon for a variant/state from checkbox.properties.
        Keys in file: icon.<variant>.<state>.<css-property>
        """
        prefix = f"icon.{variant.lower()}.{state.lower()}."
        return self.load_component_properties_by_prefix("checkbox", prefix)

    def load_checkbox_icon_color_properties(self, variant: str, state: str) -> Dict[str, str]:
        """Load only color-related properties for the checkbox icon (for declared style verification)."""
        CHECKBOX_ICON_COLOR_PROPERTIES = ("background-color", "color", "border-color")
        all_props = self.load_checkbox_icon_properties(variant, state)
        return {k: v for k, v in all_props.items() if k in CHECKBOX_ICON_COLOR_PROPERTIES}

    def load_checkbox_label_properties(self, variant: str, state: str) -> Dict[str, str]:
        """Load expected CSS properties for the checkbox label for a variant/state. Keys: label.<variant>.<state>.<css-property>."""
        prefix = f"label.{variant.lower()}.{state.lower()}."
        return self.load_component_properties_by_prefix("checkbox", prefix)

    def load_checkbox_label_color_properties(self, variant: str, state: str) -> Dict[str, str]:
        """Load only color-related properties for the label (for declared style verification)."""
        color_props = ("color", "background-color", "border-color")
        all_props = self.load_checkbox_label_properties(variant, state)
        return {k: v for k, v in all_props.items() if k in color_props}

    def load_checkbox_container_properties(self) -> Dict[str, str]:
        """Load container (flat) properties from checkbox.properties. Keys have no icon./label. prefix."""
        all_props = self.load_component_properties("checkbox")
        return {
            k: v
            for k, v in all_props.items()
            if not k.startswith("icon.") and not k.startswith("label.")
        }

    def get_checkbox_label(self, selector: Optional[str] = None) -> Optional[str]:
        """Get checkbox label text"""
        checkbox = self.get_checkbox(selector)
        # Try to find associated label
        checkbox_id = checkbox.get_attribute("id")
        if checkbox_id:
            # Use iframe frame locator to find label
            frame = self.get_iframe_frame_locator()
            label = frame.locator(f"label[for='{checkbox_id}']")
            if label.count() > 0:
                return label.first.inner_text()
        return None

