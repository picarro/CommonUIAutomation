"""
Locators for Main Tab component
All CSS selectors and locators for Main Tab component are defined here
"""


class MainTabLocators:
    """Locators for Main Tab component"""
    
    # Main tab container
    TAB_CONTAINER = "#storybook-root div"
    TABS_WRAPPER = "#storybook-root [role='tablist'], #storybook-root .tabs, #storybook-root [class*='tab']"
    
    # Individual tab selectors
    TAB = "#storybook-root [role='tab'], #storybook-root button[class*='tab'], #storybook-root [class*='tab-item']"
    TAB_BUTTON = "#storybook-root button[role='tab']"
    
    # Tab states
    TAB_ACTIVE = "#storybook-root [role='tab'][aria-selected='true'], #storybook-root [class*='tab'][class*='active'], #storybook-root button[aria-selected='true']"
    TAB_INACTIVE = "#storybook-root [role='tab'][aria-selected='false'], #storybook-root [class*='tab']:not([class*='active'])"
    
    # Tab with specific text
    @staticmethod
    def tab_with_text(text: str) -> str:
        """Get tab locator with specific text"""
        return f"#storybook-root [role='tab']:has-text('{text}'), #storybook-root button:has-text('{text}')"
    
    # Tab by index
    @staticmethod
    def tab_by_index(index: int) -> str:
        """Get tab locator by index (0-based)"""
        return f"#storybook-root [role='tab']:nth-of-type({index + 1}), #storybook-root button[role='tab']:nth-of-type({index + 1})"
    
    # Tab indicator/underline (for active state)
    TAB_INDICATOR = "#storybook-root [class*='indicator'], #storybook-root [class*='underline'], #storybook-root ::after"
    
    # Tab content/panel
    TAB_PANEL = "#storybook-root [role='tabpanel'], #storybook-root [class*='tab-panel'], #storybook-root [class*='tab-content']"
