"""
Main Tab component class with all Main Tab-specific functions
"""
from playwright.sync_api import Page, Locator
from typing import Optional, List
from framework.base import PropertyChecker
from components.main_tab.locators import MainTabLocators
from utils.logger import logger


class MainTabComponent(PropertyChecker):
    """
    Main Tab component class with all Main Tab-specific functionality
    """
    
    def __init__(self, page: Page, storybook_url: str = None):
        """
        Initialize Main Tab component
        
        Args:
            page: Playwright page object
            storybook_url: Optional Storybook URL override
        """
        super().__init__(page, storybook_url)
        self.locators = MainTabLocators()
    
    def get_tab(self, selector: Optional[str] = None) -> Locator:
        """
        Get tab locator inside iframe
        
        Args:
            selector: Optional custom selector, defaults to main tab selector
            
        Returns:
            Tab locator (first match if multiple tabs found)
        """
        return self.get_story_locator(selector or self.locators.TAB)
    
    def get_tab_by_text(self, text: str) -> Locator:
        """
        Get tab locator by text content
        
        Args:
            text: Text content of the tab
            
        Returns:
            Tab locator matching the text
        """
        selector = self.locators.tab_with_text(text)
        return self.get_story_locator(selector)
    
    def get_tab_by_index(self, index: int) -> Locator:
        """
        Get tab locator by index (0-based)
        
        Args:
            index: Index of the tab (0-based)
            
        Returns:
            Tab locator at the specified index
        """
        selector = self.locators.tab_by_index(index)
        return self.get_story_locator(selector)
    
    def get_all_tabs(self) -> List[Locator]:
        """
        Get all tab locators
        
        Returns:
            List of all tab locators
        """
        tabs_locator = self.get_story_locators(self.locators.TAB)
        count = tabs_locator.count()
        return [tabs_locator.nth(i) for i in range(count)]
    
    def click_tab(self, selector: Optional[str] = None):
        """
        Click on a tab
        
        Args:
            selector: Optional custom selector, defaults to main tab selector
        """
        tab = self.get_tab(selector)
        tab.click()
        self.wait_for_animation()
    
    def click_tab_by_text(self, text: str):
        """
        Click tab by its text content
        
        Args:
            text: Text content of the tab
        """
        tab = self.get_tab_by_text(text)
        tab.click()
        self.wait_for_animation()
    
    def click_tab_by_index(self, index: int):
        """
        Click tab by index
        
        Args:
            index: Index of the tab (0-based)
        """
        tab = self.get_tab_by_index(index)
        tab.click()
        self.wait_for_animation()
    
    def is_tab_active(self, selector: Optional[str] = None) -> bool:
        """
        Check if tab is active/selected
        
        Args:
            selector: Optional custom selector
            
        Returns:
            True if tab is active, False otherwise
        """
        try:
            tab = self.get_tab(selector)
            aria_selected = tab.get_attribute("aria-selected")
            if aria_selected == "true":
                return True
            
            # Check for active class
            class_name = tab.get_attribute("class") or ""
            if "active" in class_name.lower():
                return True
            
            return False
        except Exception as e:
            logger.warning(f"Error checking tab active state: {e}")
            return False
    
    def is_tab_inactive(self, selector: Optional[str] = None) -> bool:
        """
        Check if tab is inactive/unselected
        
        Args:
            selector: Optional custom selector
            
        Returns:
            True if tab is inactive, False otherwise
        """
        return not self.is_tab_active(selector)
    
    def get_tab_text(self, selector: Optional[str] = None) -> str:
        """
        Get tab text content
        
        Args:
            selector: Optional custom selector
            
        Returns:
            Tab text content
        """
        tab = self.get_tab(selector)
        return tab.inner_text().strip()
    
    def get_active_tab_text(self) -> Optional[str]:
        """
        Get text of the currently active tab
        
        Returns:
            Text of active tab, or None if no active tab found
        """
        try:
            active_tab = self.get_story_locator(self.locators.TAB_ACTIVE)
            if active_tab.count() > 0:
                return active_tab.first.inner_text().strip()
            return None
        except Exception:
            return None
    
    def get_tab_count(self) -> int:
        """
        Get total number of tabs
        
        Returns:
            Number of tabs
        """
        tabs = self.get_story_locator(self.locators.TAB)
        return tabs.count()
    
    def verify_tab_active(self, selector: Optional[str] = None):
        """
        Verify that a tab is active
        
        Args:
            selector: Optional custom selector
            
        Raises:
            AssertionError: If tab is not active
        """
        assert self.is_tab_active(selector), f"Tab should be active"
        logger.info("✅ Tab is active")
    
    def verify_tab_inactive(self, selector: Optional[str] = None):
        """
        Verify that a tab is inactive
        
        Args:
            selector: Optional custom selector
            
        Raises:
            AssertionError: If tab is not inactive
        """
        assert self.is_tab_inactive(selector), f"Tab should be inactive"
        logger.info("✅ Tab is inactive")
    
    def hover_tab(self, selector: Optional[str] = None):
        """
        Hover over a tab
        
        Args:
            selector: Optional custom selector
        """
        tab = self.get_tab(selector)
        tab.hover()
        self.wait_for_animation(0.3)
    
    def hover_tab_by_text(self, text: str):
        """
        Hover over tab by its text content
        
        Args:
            text: Text content of the tab
        """
        tab = self.get_tab_by_text(text)
        tab.hover()
        self.wait_for_animation(0.3)
    
    def get_tab_color(self, selector: Optional[str] = None) -> str:
        """
        Get tab text color (computed style)
        
        Args:
            selector: Optional custom selector
            
        Returns:
            RGB color value of tab text
        """
        tab = self.get_tab(selector)
        return tab.evaluate("el => window.getComputedStyle(el).color")
    
    def get_tab_indicator_color(self) -> Optional[str]:
        """
        Get color of the active tab indicator/underline
        
        Returns:
            RGB color value of indicator, or None if not found
        """
        try:
            # Try to find indicator element
            indicator = self.get_story_locator(self.locators.TAB_INDICATOR)
            if indicator.count() > 0:
                return indicator.first.evaluate("el => window.getComputedStyle(el).backgroundColor")
            
            # Fallback: check active tab's border-bottom or ::after pseudo-element
            active_tab = self.get_story_locator(self.locators.TAB_ACTIVE)
            if active_tab.count() > 0:
                # Try border-bottom color
                border_color = active_tab.first.evaluate(
                    "el => window.getComputedStyle(el).borderBottomColor"
                )
                if border_color and border_color != "rgba(0, 0, 0, 0)":
                    return border_color
                
                # Try ::after pseudo-element
                after_color = active_tab.first.evaluate(
                    "el => { const after = window.getComputedStyle(el, '::after'); return after.backgroundColor || after.borderBottomColor; }"
                )
                if after_color:
                    return after_color
            
            return None
        except Exception as e:
            logger.warning(f"Error getting tab indicator color: {e}")
            return None
    
    def verify_active_tab_has_indicator(self):
        """
        Verify that the active tab has a visible indicator (underline/border)
        
        Raises:
            AssertionError: If active tab doesn't have indicator
        """
        active_tab = self.get_story_locator(self.locators.TAB_ACTIVE)
        assert active_tab.count() > 0, "No active tab found"
        
        # Check for indicator element or border
        indicator_color = self.get_tab_indicator_color()
        assert indicator_color is not None and indicator_color != "rgba(0, 0, 0, 0)", \
            "Active tab should have a visible indicator"
        logger.info(f"✅ Active tab has indicator with color: {indicator_color}")
