"""
State tests for Storybook components
"""
import pytest
from framework.base import StateBase


@pytest.mark.state
class TestState:
    """State test suite"""
    
    def test_component_initial_state(self, state_tester: StateBase):
        """Test component initial state"""
        story_path = "example-button--primary"
        state_tester.navigate_to_story(story_path)
        
        # Verify initial state
        state = state_tester.get_component_state()
        assert state is not None
        assert "url" in state
        assert "viewport" in state
    
    def test_button_disabled_state(self, state_tester: StateBase):
        """Test button disabled state"""
        story_path = "example-button--disabled"
        state_tester.navigate_to_story(story_path)
        
        # Verify button has disabled attribute
        state_tester.verify_attribute("button", "disabled", "")
    
    def test_component_class_state(self, state_tester: StateBase):
        """Test component class state"""
        story_path = "example-button--primary"
        state_tester.navigate_to_story(story_path)
        
        # Verify button has expected class
        # Adjust class name based on your component
        state_tester.verify_class("button", "btn")
    
    def test_component_text_state(self, state_tester: StateBase):
        """Test component text content state"""
        story_path = "example-button--primary"
        state_tester.navigate_to_story(story_path)
        
        # Verify button text
        state_tester.verify_text_content("button", "Button")
    
    def test_component_count_state(self, state_tester: StateBase):
        """Test component count state"""
        story_path = "example-list--default"
        state_tester.navigate_to_story(story_path)
        
        # Verify number of list items
        state_tester.verify_count("li", 5)
    
    def test_component_state_after_interaction(self, state_tester: StateBase):
        """Test component state changes after interaction"""
        story_path = "example-button--primary"
        state_tester.navigate_to_story(story_path)
        
        # Get initial state
        initial_state = state_tester.get_component_state()
        
        # Perform interaction
        state_tester.click("button")
        
        # Verify state changed (adjust based on component behavior)
        # This is a placeholder - adjust based on your component's state changes
        final_state = state_tester.get_component_state()
        assert final_state is not None
    
    def test_form_state(self, state_tester: StateBase):
        """Test form component state"""
        story_path = "example-form--default"
        state_tester.navigate_to_story(story_path)
        
        # Fill form fields
        state_tester.fill("input[name='name']", "Test User")
        state_tester.fill("input[name='email']", "test@example.com")
        
        # Verify form values
        name_value = state_tester.get_attribute("input[name='name']", "value")
        email_value = state_tester.get_attribute("input[name='email']", "value")
        
        assert name_value == "Test User"
        assert email_value == "test@example.com"

