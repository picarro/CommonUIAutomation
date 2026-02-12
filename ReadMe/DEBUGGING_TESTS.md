# Debugging Tests Guide

When tests fail or hang, here's how to debug them.

## Common Issues

### Browser Opens and Closes Quickly

This usually means:
1. **Storybook URL is incorrect or not accessible**
2. **Selector not found** - The page loaded but the expected element isn't there
3. **Timeout** - The page is taking too long to load
4. **Network error** - Can't reach the Storybook server

## Debugging Steps

### 1. Check Storybook is Running

```bash
# Check if Storybook is accessible
curl http://localhost:6006
# or
curl https://picarro.github.io/picarro-common-ui
```

### 2. Run with Verbose Output

```bash
# See all print statements and browser console
HEADLESS=false SLOW_MO=500 pytest tests/test_storybook_controls.py::TestStorybookControls::test_update_single_control -v -s
```

### 3. Check the Storybook URL

The default URL is: `https://picarro.github.io/picarro-common-ui`

If your Storybook runs locally, set:
```bash
STORYBOOK_URL=http://localhost:6006 HEADLESS=false pytest tests/test_storybook_controls.py -v -s
```

### 4. Increase Timeout

If pages are slow to load:
```bash
STORYBOOK_TIMEOUT=60000 HEADLESS=false pytest tests/test_storybook_controls.py -v -s
```

### 5. Keep Browser Open on Failure

The framework now keeps the browser open for 10 seconds when a test fails (if HEADLESS=false).

### 6. Check Browser Console

The framework now logs browser console messages. Look for:
- JavaScript errors
- Network errors
- Warnings

### 7. Add Manual Pauses

Add this to your test to pause and inspect:
```python
import time
time.sleep(10)  # Pause for 10 seconds
```

## Common Error Messages

### "Selector not found"
- The page loaded but the expected element (`.sb-story`) isn't there
- Check if your Storybook uses a different selector
- The test will continue but warn you

### "Navigation timeout"
- The page took too long to load
- Check if Storybook is running
- Check network connectivity
- Increase `STORYBOOK_TIMEOUT`

### "Network error"
- Can't reach the Storybook server
- Check the `STORYBOOK_URL` is correct
- Check if Storybook is running

## Debugging Commands

### Full Debug Mode
```bash
HEADLESS=false \
SLOW_MO=1000 \
STORYBOOK_TIMEOUT=60000 \
pytest tests/test_storybook_controls.py::TestStorybookControls::test_update_single_control -v -s -vv
```

### Check What URL is Being Used
```bash
# The test will print the URL it's trying to access
HEADLESS=false pytest tests/test_storybook_controls.py::TestStorybookControls::test_update_single_control -v -s
```

### Test Storybook Connection
```python
# Add this to a test to check connection
def test_storybook_connection(controls_manager):
    url = controls_manager.storybook_url
    print(f"Trying to connect to: {url}")
    controls_manager.page.goto(url)
    print(f"Connected! Title: {controls_manager.page.title()}")
```

## Tips

1. **Always use `-s` flag** to see print statements
2. **Use `HEADLESS=false`** to see what's happening
3. **Use `SLOW_MO=1000`** to slow down actions
4. **Check browser console** for JavaScript errors
5. **Verify Storybook URL** matches your setup

