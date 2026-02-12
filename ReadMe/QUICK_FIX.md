# Quick Fix for Browser Closing Too Fast

## The Problem
Browser opens and closes quickly without showing what's happening.

## Solution

### 1. Run with these settings:

```bash
HEADLESS=false SLOW_MO=1000 STORYBOOK_TIMEOUT=10000 pytest tests/test_storybook_controls.py::TestStorybookControls::test_update_single_control -v -s
```

### 2. What Changed

- **Browser stays open for 15 seconds** after test completes (when HEADLESS=false)
- **Better error messages** showing what URL is being accessed
- **Step-by-step logging** of navigation
- **Network request/response logging** to see what's happening
- **Graceful error handling** - won't crash on cleanup

### 3. If Test Hangs

The test will now show:
- What URL it's trying to access
- Each step of navigation
- Any errors with details
- Network requests/responses

### 4. Check Your Storybook URL

Make sure your Storybook is running and accessible:

```bash
# Check if default URL works
curl https://picarro.github.io/picarro-common-ui

# Or if running locally
curl http://localhost:6006
```

If your Storybook is local, set:
```bash
STORYBOOK_URL=http://localhost:6006 HEADLESS=false pytest tests/test_storybook_controls.py::TestStorybookControls::test_update_single_control -v -s
```

### 5. Check Story Path

Make sure `"main-button--button-story"` matches your actual Storybook story path. You can check by:
- Opening Storybook in browser
- Finding your story
- Looking at the URL - it should be something like `?path=/story/main-button--button-story`

