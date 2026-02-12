# Running Tests with Visible Browser

This guide shows you how to run tests with the browser visible so you can watch the tests execute.

## Quick Start - See Browser in Action

### Method 1: Set Environment Variable (Recommended)

```bash
# Run with visible browser
HEADLESS=false pytest tests/test_storybook_controls.py -v

# Or with slow motion to see actions clearly
HEADLESS=false SLOW_MO=500 pytest tests/test_storybook_controls.py -v
```

### Method 2: Export Environment Variable

```bash
# Set for current session
export HEADLESS=false
export SLOW_MO=500  # 500ms delay between actions

# Then run tests
pytest tests/test_storybook_controls.py -v
```

### Method 3: One-liner with Environment Variables

```bash
# macOS/Linux
HEADLESS=false SLOW_MO=300 pytest tests/test_storybook_controls.py -v -s

# Windows (PowerShell)
$env:HEADLESS="false"; $env:SLOW_MO="300"; pytest tests/test_storybook_controls.py -v -s
```

## Options Explained

### HEADLESS
- `HEADLESS=false` - Browser window will be visible
- `HEADLESS=true` - Browser runs in background (default)

### SLOW_MO
- `SLOW_MO=0` - Normal speed (default)
- `SLOW_MO=500` - 500ms delay between actions (good for watching)
- `SLOW_MO=1000` - 1 second delay (very slow, good for debugging)

### Pytest Flags
- `-v` or `--verbose` - Show detailed test output
- `-s` or `--capture=no` - Show print statements and output
- `-vv` - Extra verbose output

## Examples

### Watch Controls Test with Visible Browser

```bash
# See browser and watch controls update
HEADLESS=false SLOW_MO=500 pytest tests/test_storybook_controls.py::TestStorybookControls::test_update_single_control -v -s
```

### Watch Property Checker Test

```bash
# See browser checking properties, colors, dimensions
HEADLESS=false SLOW_MO=300 pytest tests/test_property_checker.py -v -s
```

### Watch All Controls Tests

```bash
# Run all controls tests with visible browser
HEADLESS=false SLOW_MO=300 pytest -m controls -v -s
```

## Makefile Shortcuts

You can also add shortcuts to your Makefile. Here are some examples:

```makefile
test-visible:
	HEADLESS=false SLOW_MO=300 pytest -v -s

test-controls-visible:
	HEADLESS=false SLOW_MO=300 pytest -m controls -v -s

test-property-visible:
	HEADLESS=false SLOW_MO=300 pytest -m property -v -s
```

Then run:
```bash
make test-controls-visible
```

## Debugging Tips

### 1. Use Slow Motion
When debugging, use `SLOW_MO=1000` to see each action clearly:
```bash
HEADLESS=false SLOW_MO=1000 pytest tests/test_storybook_controls.py -v -s
```

### 2. Run Single Test
Focus on one test at a time:
```bash
HEADLESS=false SLOW_MO=500 pytest tests/test_storybook_controls.py::TestStorybookControls::test_update_single_control -v -s
```

### 3. Add Print Statements
Add print statements in your tests and use `-s` flag:
```python
def test_update_single_control(self, controls_manager: StorybookControlsManager):
    print("Starting test...")
    story_path = "main-button--button-story"
    controls_manager.update_control_via_api(story_path, "label", "Updated Label")
    print("Control updated!")
```

### 4. Pause Execution
You can add a pause in your test code:
```python
import time
time.sleep(5)  # Pause for 5 seconds
```

## Browser Options

### Change Browser
```bash
# Use Firefox
HEADLESS=false BROWSER=firefox pytest tests/test_storybook_controls.py -v

# Use WebKit (Safari)
HEADLESS=false BROWSER=webkit pytest tests/test_storybook_controls.py -v
```

### Change Viewport Size
```bash
# Larger viewport
HEADLESS=false VIEWPORT_WIDTH=1920 VIEWPORT_HEIGHT=1080 pytest tests/test_storybook_controls.py -v
```

## Complete Example

```bash
# Full command with all options
HEADLESS=false \
SLOW_MO=500 \
BROWSER=chromium \
VIEWPORT_WIDTH=1280 \
VIEWPORT_HEIGHT=720 \
pytest tests/test_storybook_controls.py::TestStorybookControls::test_update_single_control -v -s
```

## Troubleshooting

### Browser Not Showing
- Make sure `HEADLESS=false` (not `HEADLESS=0` or `HEADLESS=no`)
- Check that you're using the correct case: `false` (lowercase)

### Browser Closes Too Fast
- Increase `SLOW_MO` value (e.g., `SLOW_MO=2000` for 2 second delays)
- Add `time.sleep()` in your test code

### Can't See What's Happening
- Use `-s` flag to see print statements
- Use `-vv` for extra verbose output
- Increase `SLOW_MO` to slow down actions

## Quick Reference

| Command | Description |
|---------|-------------|
| `HEADLESS=false pytest ...` | Run with visible browser |
| `SLOW_MO=500 pytest ...` | Add 500ms delay between actions |
| `pytest ... -s` | Show print statements |
| `pytest ... -v` | Verbose output |
| `pytest ... -vv` | Extra verbose output |

