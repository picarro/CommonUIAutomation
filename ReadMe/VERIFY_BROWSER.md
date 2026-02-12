# How to Verify Browser is Opening

## Step 1: Check Environment Variable

Make sure you're setting `HEADLESS=false` (lowercase "false"):

```bash
# Correct - this will show browser
HEADLESS=false pytest tests/test_simple.py -v -s

# Wrong - these won't work
HEADLESS=0 pytest tests/test_simple.py -v -s
HEADLESS=no pytest tests/test_simple.py -v -s
HEADLESS=False pytest tests/test_simple.py -v -s  # Case sensitive!
```

## Step 2: Run the Test

```bash
HEADLESS=false SLOW_MO=1000 pytest tests/test_simple.py -v -s
```

You should see output like:
```
Browser Configuration:
  HEADLESS environment: false
  Final headless setting: False
  SLOW_MO: 1000ms

Launching chromium browser...
✓ Browser launched: chromium
  Headless mode: False
  Browser is VISIBLE - you should see the window!
```

## Step 3: Check for Browser Window

After "Browser launched", you should see:
1. A Chromium/Chrome browser window open
2. The window stays open for at least 3 seconds
3. Then it navigates to example.com
4. Window stays open for 10 seconds
5. Then stays open for 30 more seconds at the end

## Troubleshooting

### If you see "Headless mode: True"
- You didn't set `HEADLESS=false` correctly
- Check the output - it shows what value was used
- Make sure it's exactly `HEADLESS=false` (lowercase)

### If browser opens but closes immediately
- The test might be failing
- Check the error messages
- The browser should stay open even on errors now

### If you don't see any browser window
1. Check the output for "Headless mode: False"
2. If it says "True", the environment variable isn't being read
3. Try: `export HEADLESS=false` then run `pytest tests/test_simple.py -v -s`

### Verify Environment Variable

```bash
# Check what HEADLESS is set to
echo $HEADLESS

# Set it explicitly
export HEADLESS=false

# Verify it's set
echo $HEADLESS  # Should print "false"

# Now run test
pytest tests/test_simple.py -v -s
```

## Quick Test Command

```bash
HEADLESS=false SLOW_MO=2000 pytest tests/test_simple.py -v -s
```

This will:
- Show browser configuration
- Open visible browser
- Wait 2 seconds between actions (slow motion)
- Keep browser open for inspection

