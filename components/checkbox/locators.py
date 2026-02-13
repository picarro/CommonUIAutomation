"""
Locators for Checkbox component (main-checkbox--default).
Storybook: https://picarro.github.io/picarro-common-ui/?path=/story/main-checkbox--default
All selectors are scoped to the story iframe (use with get_story_locator).
"""


class CheckboxLocators:
    """Locators for Checkbox component (main-checkbox--default)"""

    STORY_ROOT = "#storybook-root"

    # -------------------------------------------------------------------------
    # Primary: data-testid from story (main-checkbox--default)
    # -------------------------------------------------------------------------
    # Icon (the checkbox input/box)
    CHECKBOX = "#storybook-root [data-testid='checkbox-default']"
    CHECKBOX_ICON = "#storybook-root [data-testid='checkbox-default-checkbox']"
    CHECKBOX_LABEL = "#storybook-root [data-testid='checkbox-default-label']"

    CHECKBOX_BY_ROLE = "#storybook-root [role='checkbox']"

    # State-specific (for input)
    CHECKBOX_CHECKED = "#storybook-root input[type='checkbox']:checked"
    CHECKBOX_UNCHECKED = "#storybook-root input[type='checkbox']:not(:checked)"
    CHECKBOX_DISABLED = "#storybook-root input[type='checkbox']:disabled"

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    @staticmethod
    def checkbox_with_label(label_text: str) -> str:
        """Checkbox inside a label that contains the given text."""
        return f"#storybook-root label:has-text('{label_text}') input[type='checkbox'], #storybook-root label:has-text('{label_text}') + input[type='checkbox']"

    @staticmethod
    def checkbox_by_id(checkbox_id: str) -> str:
        """Checkbox by id attribute."""
        return f"#storybook-root input[type='checkbox'][id='{checkbox_id}']"

    @staticmethod
    def label_for_id(checkbox_id: str) -> str:
        """Label associated with checkbox by for attribute."""
        return f"#storybook-root label[for='{checkbox_id}']"

    @staticmethod
    def checkbox_in_container(container_selector: str) -> str:
        """Checkbox inside a given container."""
        return f"{container_selector} input[type='checkbox']"

    @staticmethod
    def checkbox_by_testid(test_id: str) -> str:
        """Checkbox icon by data-testid (e.g. 'checkbox-default-checkbox')."""
        return f"#storybook-root [data-testid='{test_id}']"
