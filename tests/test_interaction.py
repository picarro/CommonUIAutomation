"""
Interaction tests for Storybook components
"""
import pytest
from framework.base import InteractionBase


@pytest.mark.interaction
class TestInteractions:
    """Interaction test suite"""
    
    def test_button_click(self, interaction_tester: InteractionBase):
        """Test button click interaction"""
        story_path = "example-button--primary"
        interaction_tester.navigate_to_story(story_path)
        
        # Verify button is visible
        interaction_tester.wait_for_visible("button")
        
        # Click the button
        interaction_tester.click("button")
        
        # Verify button was clicked (example: check for disabled state or text change)
        # Adjust based on your component's behavior
        assert interaction_tester.is_visible("button")
    
    def test_input_fill(self, interaction_tester: InteractionBase):
        """Test input field interaction"""
        story_path = "example-input--default"
        interaction_tester.navigate_to_story(story_path)
        
        # Fill input field
        test_value = "Test input"
        interaction_tester.fill("input", test_value)
        
        # Verify value was entered
        value = interaction_tester.get_attribute("input", "value")
        assert value == test_value
    
    def test_dropdown_selection(self, interaction_tester: InteractionBase):
        """Test dropdown selection"""
        story_path = "example-select--default"
        interaction_tester.navigate_to_story(story_path)
        
        # Select an option
        interaction_tester.select_option("select", "option1")
        
        # Verify selection
        selected_value = interaction_tester.get_attribute("select", "value")
        assert selected_value == "option1"
    
    def test_hover_interaction(self, interaction_tester: InteractionBase):
        """Test hover interaction"""
        story_path = "example-button--primary"
        interaction_tester.navigate_to_story(story_path)
        
        # Hover over element
        interaction_tester.hover("button")
        
        # Verify hover state (e.g., tooltip appears, class changes)
        # Adjust based on your component
        assert interaction_tester.is_visible("button")
    
    def test_keyboard_interaction(self, interaction_tester: InteractionBase):
        """Test keyboard interactions"""
        story_path = "example-input--default"
        interaction_tester.navigate_to_story(story_path)
        
        # Focus input
        interaction_tester.click("input")
        
        # Press Enter key
        interaction_tester.keyboard_press("input", "Enter")
        
        # Verify interaction (adjust based on component behavior)
        assert interaction_tester.is_visible("input")
    
    def test_toggle_interaction(self, interaction_tester: InteractionBase):
        """Test toggle/checkbox interaction"""
        story_path = "example-checkbox--default"
        interaction_tester.navigate_to_story(story_path)
        
        # Click checkbox
        interaction_tester.click("input[type='checkbox']")
        
        # Verify checkbox is checked
        checked = interaction_tester.get_attribute("input[type='checkbox']", "checked")
        assert checked is not None
    
    def test_modal_interaction(self, interaction_tester: InteractionBase):
        """Test modal open/close interaction"""
        story_path = "example-modal--default"
        interaction_tester.navigate_to_story(story_path)
        
        # Open modal
        interaction_tester.click("button:has-text('Open')")
        
        # Verify modal is visible
        interaction_tester.wait_for_visible(".modal")
        
        # Close modal
        interaction_tester.click("button:has-text('Close')")
        
        # Verify modal is hidden
        interaction_tester.wait_for_hidden(".modal")

