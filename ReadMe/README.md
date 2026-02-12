# Storybook Automation Framework

A comprehensive automation framework for testing Storybook components using Playwright and Python. This framework supports visual regression testing, interaction testing, state testing, and snapshot testing.

## Features

- **Visual Regression Testing**: Capture and compare screenshots of components
- **Interaction Testing**: Test user interactions (clicks, inputs, hovers, etc.)
- **State Testing**: Verify component state, attributes, classes, and text content
- **Snapshot Testing**: Capture and compare component structure and state as JSON
- **Multi-browser Support**: Test on Chromium, Firefox, and WebKit
- **Responsive Testing**: Test components at different viewport sizes
- **Pytest Integration**: Full pytest integration with fixtures and markers

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Install Playwright browsers:**
```bash
playwright install
```

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Storybook URL
STORYBOOK_URL=http://localhost:6006

# Browser settings
BROWSER=chromium  # chromium, firefox, webkit
HEADLESS=true
VIEWPORT_WIDTH=1280
VIEWPORT_HEIGHT=720

# Visual regression settings
VISUAL_THRESHOLD=0.2  # Pixel difference threshold (0-1)

# Timeouts
STORYBOOK_TIMEOUT=30000
```

### Configuration File

The `playwright.config.ini` file contains all configuration settings. You can modify it directly or use environment variables to override settings.

**Note:** The old `playwright.config.py` file has been replaced with `playwright.config.ini` for better maintainability. Environment variables still take precedence over the INI file settings.

## Project Structure

```
.
├── framework/
│   ├── __init__.py
│   ├── base.py           # Base classes for testing
│   ├── snapshot.py       # Snapshot testing functionality
│   └── conftest.py       # Pytest fixtures
├── tests/
│   ├── __init__.py
│   ├── test_visual_regression.py
│   ├── test_interaction.py
│   ├── test_state.py
│   └── test_snapshot.py
├── screenshots/          # Visual regression screenshots
├── snapshots/            # Snapshot JSON files
├── reports/              # Test reports
├── playwright.config.ini    # Configuration file (INI format)
├── playwright.config.py     # Deprecated - kept for reference only
├── pytest.ini
├── requirements.txt
└── README.md
```

## Usage

### Running Tests

**Run all tests:**
```bash
pytest
```

**Run specific test types:**
```bash
# Visual regression tests
pytest -m visual

# Interaction tests
pytest -m interaction

# State tests
pytest -m state

# Snapshot tests
pytest -m snapshot
```

**Run specific test file:**
```bash
pytest tests/test_visual_regression.py
```

**Run with HTML report:**
```bash
pytest --html=reports/report.html
```

### Visual Regression Testing

```python
import pytest
from framework.base import VisualRegressionBase

@pytest.mark.visual
def test_button_visual(visual_tester: VisualRegressionBase):
    story_path = "example-button--primary"
    visual_tester.navigate_to_story(story_path)
    
    visual_tester.compare_screenshot(
        story_path=story_path,
        name="default",
        threshold=0.2
    )
```

### Interaction Testing

```python
import pytest
from framework.base import InteractionBase

@pytest.mark.interaction
def test_button_click(interaction_tester: InteractionBase):
    story_path = "example-button--primary"
    interaction_tester.navigate_to_story(story_path)
    
    interaction_tester.click("button")
    interaction_tester.wait_for_visible(".result")
```

### State Testing

```python
import pytest
from framework.base import StateBase

@pytest.mark.state
def test_button_state(state_tester: StateBase):
    story_path = "example-button--primary"
    state_tester.navigate_to_story(story_path)
    
    state_tester.verify_attribute("button", "disabled", "")
    state_tester.verify_class("button", "btn-primary")
    state_tester.verify_text_content("button", "Click Me")
```

### Snapshot Testing

```python
import pytest
from framework.snapshot import SnapshotTester

@pytest.mark.snapshot
def test_component_snapshot(snapshot_tester: SnapshotTester):
    story_path = "example-button--primary"
    snapshot_tester.navigate_to_story(story_path)
    
    snapshot_tester.assert_snapshot(
        story_path=story_path,
        name="default",
        include_html=True,
        include_styles=True
    )
```

## Framework Classes

### StorybookBase
Base class providing common functionality:
- `navigate_to_story(story_path)`: Navigate to a Storybook story
- `get_component_state()`: Get current component state
- `set_viewport(width, height)`: Set viewport size

### VisualRegressionBase
Extends StorybookBase for visual testing:
- `compare_screenshot()`: Compare screenshot with baseline
- `take_screenshot()`: Take a screenshot manually

### InteractionBase
Extends StorybookBase for interaction testing:
- `click(selector)`: Click an element
- `fill(selector, value)`: Fill an input field
- `hover(selector)`: Hover over an element
- `wait_for_visible(selector)`: Wait for element to be visible
- `get_text(selector)`: Get element text content

### StateBase
Extends StorybookBase for state testing:
- `verify_attribute(selector, attribute, value)`: Verify attribute value
- `verify_class(selector, class_name)`: Verify element class
- `verify_text_content(selector, text)`: Verify text content
- `verify_count(selector, count)`: Verify element count

### SnapshotTester
Extends StorybookBase for snapshot testing:
- `assert_snapshot()`: Assert snapshot matches baseline
- `capture_snapshot()`: Capture current snapshot
- `compare_snapshot()`: Compare snapshots
- `save_snapshot()`: Save snapshot to file
- `load_snapshot()`: Load snapshot from file

## Updating Baselines

### Visual Regression
When visual changes are intentional, update baselines by:
1. Delete the old screenshot from `screenshots/` directory
2. Run the test again to generate new baseline

Or use Playwright's update mode:
```bash
pytest --update-snapshots
```

### Snapshots
Update snapshots by setting `update=True`:
```python
snapshot_tester.assert_snapshot(
    story_path=story_path,
    name="default",
    update=True
)
```

## Best Practices

1. **Story Paths**: Use consistent naming for story paths (e.g., `component-name--variant`)
2. **Test Isolation**: Each test should be independent and not rely on other tests
3. **Selectors**: Use stable, semantic selectors (data-testid, classes, etc.)
4. **Timeouts**: Adjust timeouts based on component load times
5. **Thresholds**: Set appropriate visual thresholds (0.2 is a good default)
6. **Snapshots**: Include HTML and styles only when necessary to reduce file size

## Troubleshooting

### Storybook not accessible
- Ensure Storybook is running on the configured URL
- Check firewall/network settings
- Verify STORYBOOK_URL environment variable

### Screenshots not matching
- Check if viewport size is consistent
- Verify browser and OS versions match
- Adjust visual threshold if needed
- Check for dynamic content (timestamps, random IDs, etc.)

### Tests timing out
- Increase STORYBOOK_TIMEOUT value
- Check Storybook server performance
- Verify network connectivity

## Contributing

1. Follow PEP 8 style guidelines
2. Add tests for new features
3. Update documentation
4. Use descriptive commit messages

## License

MIT License

