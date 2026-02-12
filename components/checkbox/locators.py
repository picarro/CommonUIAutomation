"""
Locators for Checkbox component
All selectors are scoped to work within iframe
"""


class CheckboxLocators:
    """Locators for Checkbox component"""
    
    # Main checkbox selector - scoped to storybook root
    CHECKBOX = "#storybook-root input[type='checkbox']"
    CHECKBOX_BY_ROLE = "#storybook-root [role='checkbox']"
    
    # Checkbox states - scoped to storybook root
    CHECKBOX_CHECKED = "#storybook-root input[type='checkbox']:checked"
    CHECKBOX_UNCHECKED = "#storybook-root input[type='checkbox']:not(:checked)"
    CHECKBOX_DISABLED = "#storybook-root input[type='checkbox']:disabled"
    
    # Checkbox with label
    @staticmethod
    def checkbox_with_label(label_text: str) -> str:
        """Get checkbox locator by label text"""
        return f"#storybook-root label:has-text('{label_text}') input[type='checkbox'], #storybook-root label:has-text('{label_text}') + input[type='checkbox']"
    
    # Checkbox by id
    @staticmethod
    def checkbox_by_id(checkbox_id: str) -> str:
        """Get checkbox locator by id"""
        return f"#storybook-root input[type='checkbox'][id='{checkbox_id}']"
    
    # Checkbox in container
    @staticmethod
    def checkbox_in_container(container_selector: str) -> str:
        """Get checkbox locator within a specific container"""
        return f"{container_selector} input[type='checkbox']"

