# Storybook Controls Manager Guide

The `StorybookControlsManager` class provides functionality to programmatically update and read Storybook controls (component args/props) during testing.

## Features

- ✅ Update single or multiple Storybook controls
- ✅ Get current control values
- ✅ Get all control values at once
- ✅ Reset controls to default values
- ✅ Support for all control types (text, number, boolean, object, array)
- ✅ Works with Storybook's internal API or UI fallback

## Usage

### Basic Setup

```python
import pytest
from framework.base import StorybookControlsManager

@pytest.mark.controls
def test_my_component(controls_manager: StorybookControlsManager):
    story_path = "my-component--default"
    controls_manager.navigate_to_story(story_path)
```

## Updating Controls

### Update Single Control

```python
# Update a single control value
controls_manager.update_control_via_api(story_path, "label", "New Label")
controls_manager.update_control_via_api(story_path, "disabled", True)
controls_manager.update_control_via_api(story_path, "count", 42)
```

### Update Multiple Controls

```python
# Update multiple controls at once
controls_manager.update_multiple_controls(story_path, {
    "label": "Updated Label",
    "disabled": False,
    "variant": "primary",
    "size": "large"
})
```

## Reading Control Values

### Get Single Control Value

```python
# Get current value of a control
label = controls_manager.get_control_value(story_path, "label")
disabled = controls_manager.get_control_value(story_path, "disabled")
```

### Get All Control Values

```python
# Get all control values for a story
all_values = controls_manager.get_all_control_values(story_path)
print(all_values)
# Returns: {
#     "label": "Button",
#     "disabled": False,
#     "variant": "primary",
#     ...
# }
```

## Control Types

### String Controls

```python
controls_manager.update_control_via_api(story_path, "text", "Hello World")
controls_manager.update_control_via_api(story_path, "label", "Click Me")
```

### Boolean Controls

```python
controls_manager.update_control_via_api(story_path, "disabled", True)
controls_manager.update_control_via_api(story_path, "loading", False)
```

### Number Controls

```python
controls_manager.update_control_via_api(story_path, "count", 42)
controls_manager.update_control_via_api(story_path, "width", 100.5)
```

### Array Controls

```python
controls_manager.update_control_via_api(story_path, "items", ["item1", "item2", "item3"])
controls_manager.update_control_via_api(story_path, "tags", ["tag1", "tag2"])
```

### Object Controls

```python
controls_manager.update_control_via_api(story_path, "config", {
    "key1": "value1",
    "key2": 123,
    "key3": True
})
```

## Resetting Controls

### Reset to Defaults

```python
# Reset all controls to their default values
controls_manager.reset_controls_to_defaults(story_path)
```

## Navigation

### Navigate to Story with Controls Panel

```python
# Navigate to full Storybook UI (not iframe) to access controls panel
controls_manager.navigate_to_story_with_controls(story_path)
```

### Navigate to Story (Iframe)

```python
# Navigate to story in iframe (standard navigation)
controls_manager.navigate_to_story(story_path)
```

## Complete Example

```python
import pytest
from framework.base import StorybookControlsManager

@pytest.mark.controls
def test_button_controls(controls_manager: StorybookControlsManager):
    """Comprehensive test for managing Storybook controls"""
    story_path = "example-button--primary"
    
    # 1. Navigate to story
    controls_manager.navigate_to_story(story_path)
    
    # 2. Get initial control values
    initial_values = controls_manager.get_all_control_values(story_path)
    print(f"Initial values: {initial_values}")
    
    # 3. Update single control
    controls_manager.update_control_via_api(story_path, "label", "Updated Button")
    
    # 4. Verify update
    new_label = controls_manager.get_control_value(story_path, "label")
    assert new_label == "Updated Button"
    
    # 5. Update multiple controls
    controls_manager.update_multiple_controls(story_path, {
        "label": "Multi Update",
        "disabled": True,
        "variant": "secondary"
    })
    
    # 6. Verify all updates
    all_values = controls_manager.get_all_control_values(story_path)
    assert all_values["label"] == "Multi Update"
    assert all_values["disabled"] == True
    assert all_values["variant"] == "secondary"
    
    # 7. Reset to defaults
    controls_manager.reset_controls_to_defaults(story_path)
    
    # 8. Verify reset
    reset_values = controls_manager.get_all_control_values(story_path)
    assert reset_values["label"] == initial_values["label"]
```

## Combining with Other Testers

You can combine controls management with other testers:

```python
import pytest
from framework.base import StorybookControlsManager, PropertyChecker

@pytest.mark.controls
@pytest.mark.property
def test_controls_and_properties(
    controls_manager: StorybookControlsManager,
    property_checker: PropertyChecker
):
    story_path = "example-button--primary"
    
    # Update control
    controls_manager.update_control_via_api(story_path, "label", "New Label")
    
    # Check component properties
    property_checker.navigate_to_story(story_path)
    property_checker.verify_component_text("button", "New Label")
    
    # Check dimensions
    property_checker.verify_width("button", 120.0, tolerance=5.0)
    
    # Check colors
    property_checker.verify_color("button", "#007bff", "background")
```

## How It Works

The `StorybookControlsManager` uses multiple strategies to update controls:

1. **Primary Method**: Uses Storybook's internal API (`__STORYBOOK_STORY_STORE__`) to update args programmatically
2. **Fallback Method**: If API is not available, navigates to full Storybook UI and updates controls via UI interaction

### API Methods

- `window.__STORYBOOK_STORY_STORE__`: Direct access to Storybook's story store
- `window.__STORYBOOK_ADDONS__`: Access via Storybook's addon channel
- UI Controls Panel: Direct interaction with control inputs

## Available Methods Summary

### Control Update Methods
- `update_control_via_api(story_path, arg_name, value)` - Update single control
- `update_multiple_controls(story_path, controls)` - Update multiple controls
- `reset_controls_to_defaults(story_path)` - Reset all controls

### Control Read Methods
- `get_control_value(story_path, arg_name)` - Get single control value
- `get_all_control_values(story_path)` - Get all control values

### Navigation Methods
- `navigate_to_story(story_path)` - Navigate to story (iframe)
- `navigate_to_story_with_controls(story_path)` - Navigate to full UI with controls panel

## Notes

- Control names must match the arg names defined in your Storybook stories
- The API method works best when testing from iframe context
- UI fallback method requires navigating to full Storybook UI
- Complex values (objects, arrays) are automatically serialized
- Control updates trigger component re-renders automatically

## Troubleshooting

### Controls Not Updating

1. Verify control names match your story args
2. Check if Storybook API is available (check browser console)
3. Try using `navigate_to_story_with_controls()` for UI fallback
4. Ensure story is fully loaded before updating controls

### API Not Found

If you see "Storybook API not found", the framework will automatically fall back to UI-based updates. Make sure:
- Storybook is running and accessible
- Controls panel is visible in full UI mode
- Control selectors match your Storybook version

