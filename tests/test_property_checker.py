"""
Property checker tests - Demonstrates checking properties, colors, dimensions, and text
"""
import pytest
from framework.base import PropertyChecker
# Logger is automatically injected by conftest.py - use 'logger' directly


@pytest.mark.property
class TestPropertyChecker:
    """Test suite for property checking functionality"""
    
    def test_check_css_properties(self, property_checker: PropertyChecker):
        """Test checking CSS properties"""
        story_path = "example-button--primary"
        property_checker.navigate_to_story(story_path)
        
        # Wait for element to be visible
        property_checker.wait_for_visible("button")
        
        # Check individual property
        display = property_checker.get_computed_style("button", "display")
        assert display in ["inline-block", "block", "flex", "inline-flex"], \
            f"Unexpected display value: {display}"
        
        # Verify property value
        property_checker.verify_property("button", "display", "inline-block")
        
        # Check multiple properties at once
        property_checker.verify_multiple_properties("button", {
            "display": "inline-block",
            "cursor": "pointer"
        })
    
    def test_check_colors(self, property_checker: PropertyChecker):
        """Test checking colors (background, text, border)"""
        story_path = "example-button--primary"
        property_checker.navigate_to_story(story_path)
        
        property_checker.wait_for_visible("button")
        
        # Get background color
        bg_color = property_checker.get_color("button", "background")
        assert bg_color, "Background color should not be empty"
        
        # Get text color
        text_color = property_checker.get_color("button", "color")
        assert text_color, "Text color should not be empty"
        
        # Verify colors (adjust expected values based on your component)
        # property_checker.verify_color("button", "#007bff", "background")
        # property_checker.verify_color("button", "#ffffff", "color")
    
    def test_check_dimensions(self, property_checker: PropertyChecker):
        """Test checking width and height"""
        story_path = "example-button--primary"
        property_checker.navigate_to_story(story_path)
        
        property_checker.wait_for_visible("button")
        
        # Get all dimensions
        dimensions = property_checker.get_dimensions("button")
        assert "width" in dimensions, "Width should be available"
        assert "height" in dimensions, "Height should be available"
        assert dimensions["width"] > 0, "Width should be greater than 0"
        assert dimensions["height"] > 0, "Height should be greater than 0"
        
        # Verify specific width (with tolerance for sub-pixel rendering)
        # property_checker.verify_width("button", 120.0, tolerance=5.0)
        
        # Verify specific height
        # property_checker.verify_height("button", 40.0, tolerance=5.0)
        
        # Verify both dimensions at once
        # property_checker.verify_dimensions("button", expected_width=120.0, expected_height=40.0, tolerance=5.0)
    
    def test_update_label(self, property_checker: PropertyChecker):
        """Test updating label/text content"""
        story_path = "example-button--primary"
        property_checker.navigate_to_story(story_path)
        
        property_checker.wait_for_visible("button")
        
        # Get original text
        original_text = property_checker.get_component_text("button")
        assert original_text, "Button should have text"
        
        # Update label
        new_text = "Updated Button Text"
        property_checker.update_label("button", new_text)
        
        # Verify text was updated
        property_checker.verify_component_text("button", new_text, exact_match=True)
        
        # Restore original text
        property_checker.update_label("button", original_text)
        property_checker.verify_component_text("button", original_text, exact_match=True)
    
    def test_check_component_text(self, property_checker: PropertyChecker):
        """Test checking component text"""
        story_path = "example-button--primary"
        property_checker.navigate_to_story(story_path)
        
        property_checker.wait_for_visible("button")
        
        # Get text content
        text = property_checker.get_component_text("button")
        assert text, "Component should have text"
        
        # Get inner text (excludes hidden elements)
        inner_text = property_checker.get_component_inner_text("button")
        assert inner_text, "Component should have inner text"
        
        # Verify text contains expected substring
        property_checker.verify_component_text("button", "Button", exact_match=False)
        
        # Verify exact text match
        # property_checker.verify_component_text("button", "Click Me", exact_match=True)
    
    def test_comprehensive_property_check(self, property_checker: PropertyChecker):
        """Comprehensive test checking multiple properties, colors, and dimensions"""
        story_path = "example-button--primary"
        property_checker.navigate_to_story(story_path)
        
        property_checker.wait_for_visible("button")
        
        # Check dimensions
        dimensions = property_checker.get_dimensions("button")
        logger.info(f"Button dimensions: {dimensions}")
        
        # Check colors
        bg_color = property_checker.get_color("button", "background")
        text_color = property_checker.get_color("button", "color")
        logger.info(f"Background color: {bg_color}, Text color: {text_color}")
        
        # Check properties
        display = property_checker.get_computed_style("button", "display")
        cursor = property_checker.get_computed_style("button", "cursor")
        logger.info(f"Display: {display}, Cursor: {cursor}")
        
        # Check text
        text = property_checker.get_component_text("button")
        logger.info(f"Button text: {text}")
        
        # Verify all together
        property_checker.verify_multiple_properties("button", {
            "display": "inline-block",
            "cursor": "pointer"
        })
        
        # Verify dimensions are reasonable
        assert dimensions["width"] > 0 and dimensions["height"] > 0, \
            "Button should have positive dimensions"
    
    def test_update_input_value(self, property_checker: PropertyChecker):
        """Test updating input field value"""
        story_path = "example-input--default"
        property_checker.navigate_to_story(story_path)
        
        property_checker.wait_for_visible("input")
        
        # Update input value
        new_value = "Test Input Value"
        property_checker.update_input_value("input", new_value)
        
        # Verify value was set
        actual_value = property_checker.get_attribute("input", "value")
        assert actual_value == new_value, f"Input value should be '{new_value}'"
    
    def test_check_all_computed_styles(self, property_checker: PropertyChecker):
        """Test getting all computed styles"""
        story_path = "example-button--primary"
        property_checker.navigate_to_story(story_path)
        
        property_checker.wait_for_visible("button")
        
        # Get all computed styles
        all_styles = property_checker.get_all_computed_styles("button")
        
        # Verify we got styles
        assert len(all_styles) > 0, "Should have computed styles"
        
        # Check that common properties are present
        assert "display" in all_styles or "display" in [k.lower() for k in all_styles.keys()], \
            "Display property should be available"
        
        logger.info(f"Total computed styles: {len(all_styles)}")
        logger.info(f"Sample styles: {dict(list(all_styles.items())[:10])}")

