"""
Visual regression tests for Storybook components
"""
import pytest
from framework.base import VisualRegressionBase


@pytest.mark.visual
class TestVisualRegression:
    """Visual regression test suite"""
    
    def test_button_primary_visual(self, visual_tester: VisualRegressionBase):
        """Test visual appearance of primary button"""
        story_path = "main-button--button-story"
        visual_tester.navigate_to_story(story_path)
        
        # Take initial screenshot
        visual_tester.compare_screenshot(
            story_path=story_path,
            name="default",
            threshold=0.2
        )
    
    def test_button_secondary_visual(self, visual_tester: VisualRegressionBase):
        """Test visual appearance of secondary button"""
        story_path = "example-button--secondary"
        visual_tester.navigate_to_story(story_path)
        
        visual_tester.compare_screenshot(
            story_path=story_path,
            name="default",
            threshold=0.2
        )
    
    def test_button_hover_state(self, visual_tester: VisualRegressionBase):
        """Test button hover state visual"""
        story_path = "example-button--primary"
        visual_tester.navigate_to_story(story_path)
        
        # Hover over button
        visual_tester.hover("button")
        
        # Compare hover state
        visual_tester.compare_screenshot(
            story_path=story_path,
            name="hover",
            threshold=0.2
        )
    
    def test_component_responsive(self, visual_tester: VisualRegressionBase):
        """Test component at different viewport sizes"""
        story_path = "example-button--primary"
        visual_tester.navigate_to_story(story_path)
        
        # Test mobile viewport
        visual_tester.set_viewport(375, 667)
        visual_tester.compare_screenshot(
            story_path=story_path,
            name="mobile",
            threshold=0.2
        )
        
        # Test tablet viewport
        visual_tester.set_viewport(768, 1024)
        visual_tester.compare_screenshot(
            story_path=story_path,
            name="tablet",
            threshold=0.2
        )
        
        # Test desktop viewport
        visual_tester.set_viewport(1920, 1080)
        visual_tester.compare_screenshot(
            story_path=story_path,
            name="desktop",
            threshold=0.2
        )

