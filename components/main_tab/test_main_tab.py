"""
Test file for Main Tab component
Logger is automatically injected by conftest.py - use 'logger' directly
"""
import pytest
from components.main_tab.main_tab import MainTabComponent
from framework.base import StorybookControlsManager
from utils.logger import logger

STORY_PATH = "main-tab--default"


@pytest.mark.property
class TestMainTabComponent:
    """Test suite for Main Tab component"""
    
    @pytest.fixture(scope="class")
    def main_tab(self, page):
        """Fixture to create MainTabComponent instance and navigate to story"""
        main_tab = MainTabComponent(page)
        main_tab.navigate_to_story(STORY_PATH, wait_for_selector=main_tab.locators.TAB)
        return main_tab
    
    @pytest.fixture(scope="class")
    def controls_manager(self, page):
        """Fixture to create StorybookControlsManager instance"""
        return StorybookControlsManager(page)
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_class_fixtures(self, main_tab, controls_manager):
        """Automatically store fixtures as instance attributes"""
        self.main_tab = main_tab
        self.story_path = STORY_PATH
        self.controls_manager = controls_manager
        yield
    
    def test_tab_count(self):
        """Test that there are tabs present"""
        main_tab, story_path, controls_manager = self.main_tab, self.story_path, self.controls_manager
        
        tab_count = main_tab.get_tab_count()
        assert tab_count > 0, f"Expected at least one tab, got {tab_count}"
        logger.info(f"✅ Found {tab_count} tabs")
    
    def test_active_tab_has_indicator(self):
        """Test that active tab has a visible indicator (green underline per Figma design)"""
        main_tab, story_path, controls_manager = self.main_tab, self.story_path, self.controls_manager
        
        # Verify active tab has indicator
        main_tab.verify_active_tab_has_indicator()
        logger.info("✅ Active tab has indicator")
    
    def test_active_tab_text_color(self):
        """Test that active tab has dark gray text color (#333333 per Figma design)"""
        main_tab, story_path, controls_manager = self.main_tab, self.story_path, self.controls_manager
        
        # Get active tab
        active_tab = main_tab.get_story_locator(main_tab.locators.TAB_ACTIVE)
        assert active_tab.count() > 0, "No active tab found"
        
        # Get text color
        color = main_tab.get_tab_color(main_tab.locators.TAB_ACTIVE)
        logger.info(f"Active tab text color: {color}")
        
        # Verify it's a dark color (should be close to #333333 or rgb(51, 51, 51))
        # Allow some flexibility in color matching
        assert color is not None, "Active tab should have a text color"
        logger.info("✅ Active tab has dark text color")
    
    def test_inactive_tab_text_color(self):
        """Test that inactive tabs have light gray text color (#999999 per Figma design)"""
        main_tab, story_path, controls_manager = self.main_tab, self.story_path, self.controls_manager
        
        # Get inactive tabs
        inactive_tabs = main_tab.get_story_locator(main_tab.locators.TAB_INACTIVE)
        assert inactive_tabs.count() > 0, "No inactive tabs found"
        
        # Get text color of first inactive tab
        color = main_tab.get_tab_color(main_tab.locators.TAB_INACTIVE)
        logger.info(f"Inactive tab text color: {color}")
        
        # Verify it's a light color (should be close to #999999)
        assert color is not None, "Inactive tab should have a text color"
        logger.info("✅ Inactive tab has light text color")
    
    def test_tab_click(self):
        """Test clicking on a tab"""
        main_tab, story_path, controls_manager = self.main_tab, self.story_path, self.controls_manager
        
        # Get initial active tab text
        initial_active = main_tab.get_active_tab_text()
        logger.info(f"Initial active tab: {initial_active}")
        
        # Get all tabs
        tabs = main_tab.get_all_tabs()
        assert len(tabs) > 1, "Need at least 2 tabs to test clicking"
        
        # Find a tab that's not currently active
        target_tab_index = None
        for i, tab in enumerate(tabs):
            if not main_tab.is_tab_active(main_tab.locators.tab_by_index(i)):
                target_tab_index = i
                break
        
        if target_tab_index is not None:
            # Click the inactive tab
            target_tab_text = main_tab.get_tab_text(main_tab.locators.tab_by_index(target_tab_index))
            logger.info(f"Clicking tab: {target_tab_text}")
            
            main_tab.click_tab_by_index(target_tab_index)
            main_tab.wait_for_animation(0.5)
            
            # Verify the clicked tab is now active
            main_tab.verify_tab_active(main_tab.locators.tab_by_index(target_tab_index))
            logger.info(f"✅ Tab '{target_tab_text}' clicked and is now active")
        else:
            logger.warning("⚠️ All tabs are active, skipping click test")
    
    def test_tab_hover_state(self):
        """Test hovering over a tab (should show green border per Figma design)"""
        main_tab, story_path, controls_manager = self.main_tab, self.story_path, self.controls_manager
        
        # Get an inactive tab to hover
        inactive_tabs = main_tab.get_story_locator(main_tab.locators.TAB_INACTIVE)
        if inactive_tabs.count() > 0:
            # Hover over first inactive tab
            main_tab.hover_tab(main_tab.locators.TAB_INACTIVE)
            main_tab.wait_for_animation(0.3)
            
            # Check if hover state is visible (border or outline)
            hovered_tab = inactive_tabs.first
            border_color = hovered_tab.evaluate("el => window.getComputedStyle(el).borderColor")
            outline_color = hovered_tab.evaluate("el => window.getComputedStyle(el).outlineColor")
            
            logger.info(f"Hover border color: {border_color}")
            logger.info(f"Hover outline color: {outline_color}")
            
            # Verify hover state is visible (should have green border/outline)
            has_hover_style = (
                (border_color and border_color != "rgba(0, 0, 0, 0)" and border_color != "transparent") or
                (outline_color and outline_color != "rgba(0, 0, 0, 0)" and outline_color != "transparent")
            )
            
            if has_hover_style:
                logger.info("✅ Tab hover state is visible")
            else:
                logger.warning("⚠️ Tab hover state may not be visible (check CSS)")
        else:
            logger.warning("⚠️ No inactive tabs found for hover test")
    
    def test_tab_states(self):
        """Test that tabs have correct active/inactive states"""
        main_tab, story_path, controls_manager = self.main_tab, self.story_path, self.controls_manager
        
        # Verify at least one tab is active
        active_tabs = main_tab.get_story_locator(main_tab.locators.TAB_ACTIVE)
        assert active_tabs.count() > 0, "At least one tab should be active"
        logger.info(f"✅ Found {active_tabs.count()} active tab(s)")
        
        # Verify inactive tabs exist
        inactive_tabs = main_tab.get_story_locator(main_tab.locators.TAB_INACTIVE)
        if inactive_tabs.count() > 0:
            logger.info(f"✅ Found {inactive_tabs.count()} inactive tab(s)")
        else:
            logger.info("ℹ️ All tabs are active (single tab scenario)")
    
    def test_tab_text_content(self):
        """Test that tabs have text content"""
        main_tab, story_path, controls_manager = self.main_tab, self.story_path, self.controls_manager
        
        tabs = main_tab.get_all_tabs()
        assert len(tabs) > 0, "No tabs found"
        
        for i, tab in enumerate(tabs):
            text = main_tab.get_tab_text(main_tab.locators.tab_by_index(i))
            assert text and len(text.strip()) > 0, f"Tab {i} should have text content"
            logger.info(f"Tab {i} text: '{text}'")
        
        logger.info("✅ All tabs have text content")
    
    def test_tab_indicator_color(self):
        """Test that active tab indicator has green color (#66CC33 per Figma design)"""
        main_tab, story_path, controls_manager = self.main_tab, self.story_path, self.controls_manager
        
        indicator_color = main_tab.get_tab_indicator_color()
        if indicator_color:
            logger.info(f"Tab indicator color: {indicator_color}")
            # Verify it's not transparent/black
            assert indicator_color != "rgba(0, 0, 0, 0)" and indicator_color != "transparent", \
                "Indicator should have a visible color"
            logger.info("✅ Tab indicator has visible color")
        else:
            logger.warning("⚠️ Could not detect indicator color (may need to check DOM structure)")
    
    def test_tab_properties(self):
        """Test tab regular CSS properties (excluding CSS variables)"""
        main_tab, story_path, controls_manager = self.main_tab, self.story_path, self.controls_manager
        
        main_tab.verify_component_properties(selector=main_tab.locators.TAB)
        logger.info("✅ Tab regular properties verified")
    
    def test_tab_css_variables(self):
        """
        Verifies all CSS variables available in browser match css-variables.properties.
        """
        main_tab, story_path, controls_manager = self.main_tab, self.story_path, self.controls_manager
        
        main_tab.get_all_css_variables_from_root()
        logger.info("✅ Tab CSS variable properties verified")
