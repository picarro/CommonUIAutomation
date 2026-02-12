# Chromium Issue on macOS

## Problem

Chromium crashes with a segmentation fault (`SEGV_ACCERR`) when running in non-headless mode on macOS, particularly on:
- macOS 15.3 (Sequoia) and newer
- Apple Silicon (M1/M2/M3) Macs
- Some Intel Macs with specific configurations

## Error Details

```
TargetClosedError: Target page, context or browser has been closed
Received signal 11 SEGV_ACCERR (segmentation fault)
```

The browser process crashes immediately after launch when trying to create a page in non-headless mode.

## Current Workaround

The framework automatically switches to **Firefox** when:
- `HEADLESS=false` 
- Browser is set to `chromium`

This ensures tests can run in visible mode without crashes.

## Solutions

### Option 1: Use Firefox (Recommended - Current Default)

Firefox works reliably in non-headless mode on macOS:

```bash
HEADLESS=false BROWSER=firefox pytest tests/test_simple.py -v -s
```

Or let the framework auto-switch (current behavior):
```bash
HEADLESS=false pytest tests/test_simple.py -v -s
```

### Option 2: Use WebKit

WebKit (Safari engine) also works well on macOS:

```bash
HEADLESS=false BROWSER=webkit pytest tests/test_simple.py -v -s
```

### Option 3: Force Chromium (Not Recommended)

If you want to try Chromium anyway, you can force it:

```bash
HEADLESS=false FORCE_CHROMIUM=true pytest tests/test_simple.py -v -s
```

**Warning:** This will likely crash. Only use for debugging.

### Option 4: Use Headless Mode

Chromium works fine in headless mode:

```bash
HEADLESS=true BROWSER=chromium pytest tests/test_simple.py -v -s
```

### Option 5: Update Playwright

Try updating Playwright to the latest version:

```bash
pip install --upgrade playwright
playwright install chromium
```

## Environment Variables

- `HEADLESS=false` - Run browser in visible mode
- `BROWSER=chromium|firefox|webkit` - Choose browser
- `FORCE_CHROMIUM=true` - Force Chromium even in non-headless mode (may crash)

## Technical Details

This is a known issue in the Playwright/Chromium ecosystem:
- [Playwright Issue #34693](https://github.com/microsoft/playwright/issues/34693)
- Related to Chromium's rendering engine on macOS
- Affects non-headless mode specifically
- Headless mode works fine

## Recommendations

1. **For development/debugging:** Use Firefox or WebKit with `HEADLESS=false`
2. **For CI/CD:** Use Chromium with `HEADLESS=true` (works fine)
3. **For visual testing:** Use Firefox with `HEADLESS=false` (most reliable)

## Status

- ✅ Firefox: Works perfectly in non-headless mode
- ✅ WebKit: Works well in non-headless mode  
- ✅ Chromium: Works in headless mode
- ❌ Chromium: Crashes in non-headless mode on macOS

