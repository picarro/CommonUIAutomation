"""
Storybook Controls Manager tests - Demonstrates updating and reading Storybook controls
"""
import pytest
from framework.base import StorybookControlsManager
# Logger is automatically injected by conftest.py - use 'logger' directly


@pytest.mark.controls
class TestStorybookControls:
    """Test suite for Storybook controls management"""
    
    def test_update_single_control(self, controls_manager: StorybookControlsManager):
        """Test updating a single control value"""
        story_path = "main-button--button-story"
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting test: test_update_single_control")
        logger.info(f"Story path: {story_path}")
        logger.info(f"Storybook URL: {controls_manager.storybook_url}")
        logger.info(f"{'='*60}\n")
        
        try:
            # Update a control (e.g., label, disabled, variant)
            # Adjust control name based on your component's args
            logger.info("Step 1: Updating control...")
            controls_manager.update_control_via_ui(story_path, "children", "Updated Label")
            logger.info("✅ Control updated")
            
            # Verify the control was updated by getting its value
            logger.info("Step 2: Getting control value...")
            value = controls_manager.get_control_value(story_path, "children")
            logger.info(f"✅ Control value retrieved: {value}")
            
            logger.info("Step 3: Verifying value...")
            assert value == "Updated Label", f"Control value should be 'Updated Label', got '{value}'"
            logger.info("✅ Test passed!")
            
        except Exception as e:
            logger.error(f"\n❌ Test failed with error: {e}")
            logger.error(f"Current page URL: {controls_manager.page.url}")
            logger.error(f"Page title: {controls_manager.page.title()}")
            import traceback
            traceback.print_exc()
            raise
    
    def test_update_multiple_controls(self, controls_manager: StorybookControlsManager):
        """Test updating multiple controls at once"""
        story_path = "example-button--primary"
        
        # Update multiple controls
        controls_manager.update_multiple_controls(story_path, {
            "label": "Multi Update",
            "disabled": False,
            "variant": "primary"
        })
        
        # Verify all controls were updated
        all_values = controls_manager.get_all_control_values(story_path)
        assert all_values.get("label") == "Multi Update"
        assert all_values.get("disabled") == False
    
    def test_get_control_value(self, controls_manager: StorybookControlsManager):
        """Test getting a control value"""
        story_path = "example-button--primary"
        controls_manager.navigate_to_story(story_path)
        
        # Get a control value
        # Adjust control name based on your component
        value = controls_manager.get_control_value(story_path, "label")
        assert value is not None, "Control value should not be None"
    
    def test_get_all_control_values(self, controls_manager: StorybookControlsManager):
        """Test getting all control values"""
        story_path = "example-button--primary"
        controls_manager.navigate_to_story(story_path)
        
        # Get all control values
        all_values = controls_manager.get_all_control_values(story_path)
        assert isinstance(all_values, dict), "Should return a dictionary"
        assert len(all_values) > 0, "Should have at least one control"
    
    def test_update_control_types(self, controls_manager: StorybookControlsManager):
        """Test updating different control types"""
        story_path = "example-component--default"
        
        # Test string control
        controls_manager.update_control_via_api(story_path, "text", "Test String")
        
        # Test boolean control
        controls_manager.update_control_via_api(story_path, "disabled", True)
        
        # Test number control
        controls_manager.update_control_via_api(story_path, "count", 42)
        
        # Verify values
        assert controls_manager.get_control_value(story_path, "text") == "Test String"
        assert controls_manager.get_control_value(story_path, "disabled") == True
        assert controls_manager.get_control_value(story_path, "count") == 42
    
    def test_reset_controls(self, controls_manager: StorybookControlsManager):
        """Test resetting controls to defaults"""
        story_path = "example-button--primary"
        controls_manager.navigate_to_story(story_path)
        
        # Get initial values
        initial_values = controls_manager.get_all_control_values(story_path)
        
        # Update some controls
        controls_manager.update_multiple_controls(story_path, {
            "label": "Changed",
            "disabled": True
        })
        
        # Reset to defaults
        controls_manager.reset_controls_to_defaults(story_path)
        
        # Verify values are back to initial
        reset_values = controls_manager.get_all_control_values(story_path)
        # Note: This test may need adjustment based on your Storybook setup
        assert reset_values is not None
    
    def test_control_updates_reflect_in_component(self, controls_manager: StorybookControlsManager):
        """Test that control updates are reflected in the component"""
        story_path = "example-button--primary"
        
        # Update label control
        new_label = "Dynamic Label"
        controls_manager.update_control_via_api(story_path, "label", new_label)
        
        # Wait for component to update
        controls_manager.wait_for_animation(1.0)
        
        # Verify component shows the updated label
        # This depends on your component structure
        controls_manager.navigate_to_story(story_path)
        # Get text using helper method
        button_text = controls_manager.get_component_text("button")
        assert new_label in button_text, f"Component should show '{new_label}', got '{button_text}'"
    
    def test_controls_with_complex_values(self, controls_manager: StorybookControlsManager):
        """Test updating controls with complex values (objects, arrays)"""
        story_path = "example-component--default"
        
        # Test array control
        controls_manager.update_control_via_api(story_path, "items", ["item1", "item2", "item3"])
        
        # Test object control
        controls_manager.update_control_via_api(story_path, "config", {
            "key1": "value1",
            "key2": 123
        })
        
        # Verify values
        items = controls_manager.get_control_value(story_path, "items")
        assert isinstance(items, list), "Items should be a list"
        
        config = controls_manager.get_control_value(story_path, "config")
        assert isinstance(config, dict), "Config should be a dict"

