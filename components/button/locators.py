"""
Locators for Button component
All CSS selectors and locators for Button component are defined here.
"""


class ButtonLocators:
    """Locators for Button component"""

    # data-testid from Storybook (main-button--primary): <button data-testid="button-primary">
    BUTTON = "#storybook-root [data-testid='button-primary']"
    BUTTON_BY_TESTID = "#storybook-root [data-testid='button-primary']"

    # Fallback / legacy selectors
    BUTTON_XPATH = "//*[@id='storybook-root']//button[@data-testid='button-primary']"
    BUTTON_LEGACY = "#storybook-root div button"

    # More specific selectors for different Storybook setups
    BUTTON_IN_STORYBOOK = "#storybook-root button"
    BUTTON_IN_STORY = ".sb-story button"

    # Alternative selectors
    BUTTON_BY_ROLE = "#storybook-root [role='button']"
    BUTTON_BY_TYPE = "#storybook-root button[type='button']"

    # Button variants/styles - based on class names in DOM
    BUTTON_PRIMARY = "#storybook-root [data-testid='button-primary']"
    BUTTON_SECONDARY = "#storybook-root div button.bg-secondary"
    BUTTON_DANGER = "#storybook-root div button.bg-danger"
    
    # Button states - based on actual attributes in DOM
    BUTTON_DISABLED = "#storybook-root div button:disabled, #storybook-root div button[disabled], #storybook-root div button[aria-disabled='true']"
    BUTTON_ENABLED = "#storybook-root div button[aria-disabled='false']"
    BUTTON_LOADING = "#storybook-root div button[aria-busy='true']"
    BUTTON_NOT_LOADING = "#storybook-root div button[aria-busy='false']"
    BUTTON_ACTIVE = "#storybook-root div button[data-active='true']"
    
    @staticmethod
    def button_by_testid(test_id: str) -> str:
        """Get button locator by data-testid (e.g. 'button-primary', 'button-secondary')."""
        return f"#storybook-root [data-testid='{test_id}']"

    # Button with specific text
    @staticmethod
    def button_with_text(text: str) -> str:
        """Get button locator with specific text"""
        return f"#storybook-root div button:has-text('{text}')"
    
    # Button with specific label
    @staticmethod
    def button_by_label(label: str) -> str:
        """Get button locator by label/aria-label"""
        return f"#storybook-root div button[aria-label='{label}']"
    
    # Button in specific container
    @staticmethod
    def button_in_container(container_selector: str) -> str:
        """Get button locator within a specific container"""
        return f"{container_selector} button"
    
    # Storybook Actions Panel locators
    ACTIONS_TAB = "#tabbutton-storybook-actions-panel"
    ACTIONS_PANEL_CONTENT = "#panel-tab-content"
    ACTIONS_TREE = "#panel-tab-content ol[role='tree']"
    ACTION_ITEMS = "#panel-tab-content li[role='treeitem']"
    ACTION_CLEAR_BUTTON = "#panel-tab-content button:has-text('Clear'), #panel-tab-content .css-1fdphfk"
    
    # Action item specific selectors
    @staticmethod
    def action_item_by_name(action_name: str) -> str:
        """Get action item locator by action name (e.g., 'onClick')"""
        return f"#panel-tab-content li[role='treeitem']:has-text('{action_name}')"

