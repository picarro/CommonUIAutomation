# Quick Start Guide

Get up and running with the Storybook Automation Framework in minutes!

## Prerequisites

- Python 3.8 or higher
- Node.js (for running Storybook)
- Your Storybook instance running

## Setup (5 minutes)

1. **Clone or navigate to the project directory:**
```bash
cd /Users/bhavikaranitn/Library/CloudStorage/OneDrive-Picarro,Inc/Documents/AutomationWorkSpace
```

2. **Run the setup script:**
```bash
./setup.sh
```

Or manually:
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Copy environment file
cp .env.example .env
```

3. **Configure your Storybook URL:**
Edit `.env` file and set your Storybook URL:
```bash
STORYBOOK_URL=http://localhost:6006
```

4. **Start your Storybook server:**
```bash
# In your Storybook project directory
npm run storybook
# or
yarn storybook
```

## Running Your First Test

1. **Update a test file:**
   - Open `tests/test_visual_regression.py`
   - Replace `"example-button--primary"` with your actual story path
   - Story paths format: `component-name--variant`

2. **Run the test:**
```bash
# Activate virtual environment first
source venv/bin/activate

# Run visual regression tests
pytest -m visual

# Or run all tests
pytest
```

## Understanding Story Paths

Story paths in Storybook follow the format: `component-name--variant`

To find your story path:
1. Open your Storybook in browser
2. Navigate to a story
3. Look at the URL: `http://localhost:6006/?path=/story/button--primary`
4. The story path is: `button--primary`

## Writing Your First Test

Here's a simple example:

```python
import pytest
from framework.base import VisualRegressionBase

@pytest.mark.visual
def test_my_component(visual_tester: VisualRegressionBase):
    story_path = "my-component--default"
    visual_tester.navigate_to_story(story_path)
    
    visual_tester.compare_screenshot(
        story_path=story_path,
        name="default",
        threshold=0.2
    )
```

## Common Commands

```bash
# Run all tests
pytest

# Run specific test type
pytest -m visual          # Visual regression
pytest -m interaction     # Interaction tests
pytest -m state           # State tests
pytest -m snapshot        # Snapshot tests

# Run with HTML report
pytest --html=reports/report.html

# Run specific test file
pytest tests/test_visual_regression.py

# Using Makefile (if available)
make test
make test-visual
make test-all
```

## Updating Baselines

When you make intentional visual changes:

1. **Visual Regression:**
   - Delete old screenshots from `screenshots/` directory
   - Run tests again to generate new baselines

2. **Snapshots:**
   - Set `update=True` in your test:
   ```python
   snapshot_tester.assert_snapshot(
       story_path=story_path,
       name="default",
       update=True
   )
   ```

## Troubleshooting

**Storybook not found:**
- Check that Storybook is running
- Verify STORYBOOK_URL in `.env` matches your Storybook URL
- Check firewall/network settings

**Tests timing out:**
- Increase `STORYBOOK_TIMEOUT` in `.env`
- Check Storybook server performance

**Screenshots not matching:**
- Ensure consistent viewport sizes
- Check for dynamic content (timestamps, random IDs)
- Adjust `VISUAL_THRESHOLD` in `.env`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check `tests/example_comprehensive_test.py` for advanced examples
- Customize tests for your components

## Getting Help

- Review test examples in `tests/` directory
- Check framework documentation in `framework/` directory
- Review pytest and Playwright documentation

Happy testing! 🚀

