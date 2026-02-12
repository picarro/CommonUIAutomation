# Property Checker Framework Guide

The `PropertyChecker` class provides comprehensive functionality for checking component properties, colors, dimensions, updating labels, and verifying component text.

## Features

- ✅ Check CSS properties (any property)
- ✅ Check colors (background, text, border)
- ✅ Check height and width (dimensions)
- ✅ Update labels and text content
- ✅ Check component text (exact or substring match)

## Usage

### Basic Setup

```python
import pytest
from framework.base import PropertyChecker

@pytest.mark.property
def test_my_component(property_checker: PropertyChecker):
    story_path = "my-component--default"
    property_checker.navigate_to_story(story_path)
    property_checker.wait_for_visible("button")
```

## Checking CSS Properties

### Get a Single Property

```python
# Get computed style value
display = property_checker.get_computed_style("button", "display")
font_size = property_checker.get_computed_style("button", "font-size")
```

### Verify a Property

```python
# Verify exact match
property_checker.verify_property("button", "display", "inline-block")
property_checker.verify_property("button", "cursor", "pointer")

# Verify with tolerance for numeric values
property_checker.verify_property("button", "font-size", "16px", tolerance=0.5)
```

### Get All Computed Styles

```python
# Get all computed CSS properties
all_styles = property_checker.get_all_computed_styles("button")
print(all_styles)  # Dictionary of all CSS properties
```

### Verify Multiple Properties

```python
# Verify multiple properties at once
property_checker.verify_multiple_properties("button", {
    "display": "inline-block",
    "cursor": "pointer",
    "position": "relative"
})

# With tolerance for numeric values
property_checker.verify_multiple_properties("button", {
    "font-size": ("16px", 0.5),  # (value, tolerance)
    "line-height": ("24px", 1.0)
})
```

## Checking Colors

### Get Colors

```python
# Get text color
text_color = property_checker.get_color("button", "color")
# or
text_color = property_checker.get_color("button", "text")

# Get background color
bg_color = property_checker.get_color("button", "background")
# or
bg_color = property_checker.get_color("button", "bg")

# Get border color
border_color = property_checker.get_color("button", "border")
```

### Verify Colors

```python
# Verify text color (supports hex, rgb, rgba, named colors)
property_checker.verify_color("button", "#ffffff", "color")
property_checker.verify_color("button", "rgb(255, 255, 255)", "color")
property_checker.verify_color("button", "white", "color")

# Verify background color
property_checker.verify_color("button", "#007bff", "background")

# Verify border color
property_checker.verify_color("button", "#000000", "border")
```

## Checking Dimensions

### Get Dimensions

```python
# Get all dimension information
dimensions = property_checker.get_dimensions("button")
print(dimensions)
# Returns: {
#     "width": 120.0,
#     "height": 40.0,
#     "top": 100.0,
#     "left": 50.0,
#     "right": 170.0,
#     "bottom": 140.0,
#     "clientWidth": 120,
#     "clientHeight": 40,
#     "offsetWidth": 120,
#     "offsetHeight": 40,
#     "scrollWidth": 120,
#     "scrollHeight": 40
# }
```

### Verify Width

```python
# Verify width with tolerance (default: 1.0px)
property_checker.verify_width("button", 120.0)
property_checker.verify_width("button", 120.0, tolerance=5.0)
```

### Verify Height

```python
# Verify height with tolerance (default: 1.0px)
property_checker.verify_height("button", 40.0)
property_checker.verify_height("button", 40.0, tolerance=5.0)
```

### Verify Both Dimensions

```python
# Verify both width and height
property_checker.verify_dimensions("button", expected_width=120.0, expected_height=40.0)

# Verify only width
property_checker.verify_dimensions("button", expected_width=120.0)

# Verify only height
property_checker.verify_dimensions("button", expected_height=40.0)

# With custom tolerance
property_checker.verify_dimensions("button", 
    expected_width=120.0, 
    expected_height=40.0, 
    tolerance=5.0
)
```

## Updating Labels and Text

### Update Label Text

```python
# Update text content (plain text)
property_checker.update_label("button", "New Button Text")

# Update with HTML (preserves HTML structure)
property_checker.update_label_by_inner_html("button", "<span>New <strong>Text</strong></span>")
```

### Update Input Value

```python
# Update input field value
property_checker.update_input_value("input", "New Input Value")
```

## Checking Component Text

### Get Text

```python
# Get text content (includes hidden elements)
text = property_checker.get_component_text("button")

# Get inner text (excludes hidden elements)
inner_text = property_checker.get_component_inner_text("button")
```

### Verify Text

```python
# Verify text contains substring (default)
property_checker.verify_component_text("button", "Click")

# Verify exact text match
property_checker.verify_component_text("button", "Click Me", exact_match=True)

# Verify inner text
property_checker.verify_component_inner_text("button", "Click", exact_match=False)
property_checker.verify_component_inner_text("button", "Click Me", exact_match=True)
```

## Complete Example

```python
import pytest
from framework.base import PropertyChecker

@pytest.mark.property
def test_button_properties(property_checker: PropertyChecker):
    """Comprehensive test checking all property checker features"""
    story_path = "example-button--primary"
    property_checker.navigate_to_story(story_path)
    property_checker.wait_for_visible("button")
    
    # 1. Check CSS Properties
    property_checker.verify_property("button", "display", "inline-block")
    property_checker.verify_property("button", "cursor", "pointer")
    
    # 2. Check Colors
    property_checker.verify_color("button", "#007bff", "background")
    property_checker.verify_color("button", "#ffffff", "color")
    
    # 3. Check Dimensions
    property_checker.verify_width("button", 120.0, tolerance=5.0)
    property_checker.verify_height("button", 40.0, tolerance=5.0)
    
    # 4. Check Text
    property_checker.verify_component_text("button", "Button", exact_match=False)
    
    # 5. Update Label
    original_text = property_checker.get_component_text("button")
    property_checker.update_label("button", "Updated Text")
    property_checker.verify_component_text("button", "Updated Text", exact_match=True)
    
    # Restore original
    property_checker.update_label("button", original_text)
    
    # 6. Verify Multiple Properties at Once
    property_checker.verify_multiple_properties("button", {
        "display": "inline-block",
        "cursor": "pointer",
        "position": "relative"
    })
```

## Available Methods Summary

### Property Methods
- `get_computed_style(selector, property_name)` - Get single CSS property
- `get_all_computed_styles(selector)` - Get all CSS properties
- `verify_property(selector, property_name, expected_value, tolerance=None)` - Verify property
- `verify_multiple_properties(selector, properties)` - Verify multiple properties

### Color Methods
- `get_color(selector, color_type)` - Get color value
- `verify_color(selector, expected_color, color_type)` - Verify color

### Dimension Methods
- `get_dimensions(selector)` - Get all dimensions
- `verify_width(selector, expected_width, tolerance=1.0)` - Verify width
- `verify_height(selector, expected_height, tolerance=1.0)` - Verify height
- `verify_dimensions(selector, expected_width=None, expected_height=None, tolerance=1.0)` - Verify dimensions

### Text Methods
- `get_component_text(selector)` - Get text content
- `get_component_inner_text(selector)` - Get inner text
- `verify_component_text(selector, expected_text, exact_match=False)` - Verify text
- `verify_component_inner_text(selector, expected_text, exact_match=False)` - Verify inner text

### Update Methods
- `update_label(selector, new_text)` - Update text content
- `update_label_by_inner_html(selector, new_html)` - Update HTML content
- `update_input_value(selector, new_value)` - Update input value

### Utility Methods
- `wait_for_visible(selector)` - Wait for element to be visible
- `get_attribute(selector, attribute)` - Get element attribute

