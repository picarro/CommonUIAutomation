"""
Pytest fixtures for Storybook testing
Root-level conftest.py - makes fixtures available to all tests in tests/ and components/
"""
import pytest
import logging
import os
import shutil
from playwright.sync_api import Page, Browser, BrowserContext
from pathlib import Path
from framework.framework_settings import (
    LOGS_DIR,
    SCREENSHOTS_DIR,
)

# Prevent pytest-playwright from auto-loading its fixtures
# We use our own custom browser fixture to avoid conflicts
pytest_plugins = []  # Empty list prevents auto-loading

# Load configuration from INI file
from framework.config_loader import get_config
from utils.logger import logger

config = get_config()


def pytest_collection_modifyitems(config, items):
    """
    Inject logger into test module namespace during collection.
    Test files can use 'logger' directly without importing it.
    This runs after modules are imported, so we inject logger into existing modules.
    """
    # Track which modules we've already injected logger into
    injected_modules = set()
    
    for item in items:
        # Get the module for this test item
        test_module = item.module
        if test_module and test_module not in injected_modules:
            # Inject logger into the module's namespace
            # This works because Python modules are mutable
            if not hasattr(test_module, 'logger'):
                test_module.logger = logger
            injected_modules.add(test_module)


@pytest.fixture(scope="session", autouse=True)
def configure_logging_once():
    """
    Initialize project-wide logging (once per session).
    Files:
    - reports/logs/test_execution_log_<worker>.log (master in serial; gwN in xdist)
    """
    logs_dir = Path(LOGS_DIR)
    logs_dir.mkdir(parents=True, exist_ok=True)

    worker_id = os.getenv("PYTEST_XDIST_WORKER") or "master"
    log_file = logs_dir / f"test_execution_log_{worker_id}.log"

    # Fresh file each run (safe with per-worker filename)
    try:
        if log_file.exists():
            log_file.unlink()
    except Exception:
        pass

    logger = logging.getLogger("commonui")
    if getattr(logger, "_configured", False):
        return

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # File handler (overwrite)
    fh = logging.FileHandler(str(log_file), encoding="utf-8", mode="w")
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmt)

    # Console handler
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt)

    logger.setLevel(logging.INFO)
    logger.addHandler(fh)
    logger.addHandler(sh)
    logger.propagate = False
    logger._configured = True

    logger.info(f"📝 Logging to: {log_file}")


@pytest.fixture(scope="session", autouse=True)
def cleanup_reports_before_session():
    """
    Clean old screenshots and logs before the test session starts.
    Args: None
    Yields: None
    """
    # Reset screenshots folder
    folders = [
        Path(SCREENSHOTS_DIR),
    ]

    for folder in folders:
        if folder.exists():
            logger.info(f"🧹 Cleaning up old {folder.name} before test run (recursive)...")
            try:
                shutil.rmtree(folder)
                logger.info(f"   🗑️ Removed: {folder}")
            except Exception as e:
                logger.warning(f"   ⚠️ Could not remove {folder}: {e}")
        folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Created fresh folder: {folder}")

    # Remove previous run logs (master + gwN) to avoid stale content in parallel runs
    logs_dir = Path(LOGS_DIR)
    if logs_dir.exists():
        for p in logs_dir.glob("test_execution_log*.log"):
            try:
                p.unlink()
                logger.info(f"🗑️ Removed old log: {p}")
            except Exception as e:
                logger.warning(f"⚠️ Could not remove log {p}: {e}")

    yield


@pytest.fixture(scope="session")
def browser_context_args():
    """Browser context arguments"""
    return {
        "viewport": {
            "width": config.VIEWPORT_WIDTH,
            "height": config.VIEWPORT_HEIGHT,
        },
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def playwright_instance():
    """Session-scoped Playwright instance"""
    from playwright.sync_api import sync_playwright
    playwright = sync_playwright().start()
    yield playwright
    playwright.stop()


@pytest.fixture(scope="session")
def browser(playwright_instance):
    """
    Create a browser instance per test function.
    Args:
      - playwright_instance: Session-scoped Playwright handle.
      - request (pytest.FixtureRequest): Access to CLI opts (e.g., --headed).
    Yields:
      - browser: Playwright Browser instance.
    """

    browser_name = config.BROWSER
    is_headless = config.HEADLESS
    browser_type = getattr(playwright_instance, browser_name)
    
    # Launch arguments
    launch_args = {
        "headless": is_headless,
    }
    
    # Add slow_mo for visible mode
    if not is_headless:
        launch_args["slow_mo"] = 250
    
    # Add launch arguments for Chromium
    if browser_name == "chromium":
        launch_args["args"] = ["--start-maximized", "--window-size=1920,1080"]
    
    logger.info(f"Launching {browser_name} browser...")
    logger.info(f"Headless mode: {is_headless}")
    
    browser = browser_type.launch(**launch_args)
    
    yield browser
    
    browser.close()
    
@pytest.fixture(scope="session")
def page(browser, request):
    """Page fixture for test execution"""
    
    # Create browser context with viewport settings
    context = browser.new_context(
        viewport={
            "width": config.VIEWPORT_WIDTH,
            "height": config.VIEWPORT_HEIGHT,
        },
        ignore_https_errors=True,
    )
    
    page = context.new_page()
    
    # Store for hooks
    test_name = request.node.nodeid.replace("/", "_").replace("\\", "_").replace(":", "_")
    request.node._test_name = test_name
    request.node._browser_context = context
    request.node._page = page
    
    logger.info(f"▶ TEST START: {test_name}")
    
    # Add console logging to see what's happening
    def handle_console(msg):
        logger.debug(f"Browser Console: {msg.type} - {msg.text}")
    page.on("console", handle_console)
    
    # Add page error logging
    def handle_page_error(error):
        logger.error(f"Page Error: {error}")
    page.on("pageerror", handle_page_error)
    
    # Add request/response logging (only errors to reduce noise)
    def handle_request(request):
        if request.resource_type in ["document", "xhr", "fetch"]:
            logger.debug(f"Request: {request.method} {request.url}")
    def handle_response(response):
        if response.status >= 400:
            logger.warning(f"Response Error: {response.status} {response.url}")
    page.on("request", handle_request)
    page.on("response", handle_response)
    
    yield page
    
    logger.info(f"⏹ TEST END: {test_name}")


@pytest.fixture(scope="function")
def logger_fixture():
    """
    Logger fixture - available to all test functions.
    Use it as a parameter in test functions: def test_something(logger_fixture):
    Framework code can still import directly: from utils.logger import logger
    """
    return logger


@pytest.fixture(scope="function")
def storybook_base(page: Page):
    """Storybook base fixture"""
    from framework.base import StorybookBase
    return StorybookBase(page)


@pytest.fixture(scope="function")
def visual_tester(page: Page):
    """Visual regression tester fixture"""
    from framework.base import VisualRegressionBase
    return VisualRegressionBase(page)


@pytest.fixture(scope="function")
def interaction_tester(page: Page):
    """Interaction tester fixture"""
    from framework.base import InteractionBase
    return InteractionBase(page)


@pytest.fixture(scope="function")
def state_tester(page: Page):
    """State tester fixture"""
    from framework.base import StateBase
    return StateBase(page)


@pytest.fixture(scope="function")
def snapshot_tester(page: Page):
    """Snapshot tester fixture"""
    from framework.snapshot import SnapshotTester
    return SnapshotTester(page)


@pytest.fixture(scope="function")
def property_checker(page: Page):
    """Property checker fixture"""
    from framework.base import PropertyChecker
    return PropertyChecker(page)


@pytest.fixture(scope="function")
def controls_manager(page: Page):
    """Storybook controls manager fixture"""
    from framework.base import StorybookControlsManager
    return StorybookControlsManager(page)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Attach screenshot artifacts on test failure and close browser context after each test call.
    Args:
      - item (pytest.Item): Test node object.
      - call (CallInfo): Call outcome info injected by pytest.
    Yields:
      - None (hookwrapper).
    """
    outcome = yield
    report = outcome.get_result()
    
    test_name = getattr(item, "_test_name", item.nodeid.replace(":", "_").replace("/", "_").replace("\\", "_"))
    context = getattr(item, '_browser_context', None)
    page_obj = getattr(item, '_page', None)

    screenshots_root = Path(SCREENSHOTS_DIR)

    # Attach screenshot on failure (BEFORE closing context)
    if report.failed and page_obj:
        try:
            # Check if page is still valid
            if not page_obj.is_closed():
                screenshots_root.mkdir(parents=True, exist_ok=True)
                screenshot_path = screenshots_root / f"{test_name}_failure_{report.when}.png"
                
                # Take screenshot with full_page option
                page_obj.screenshot(path=str(screenshot_path), full_page=True)
                
                # Verify screenshot was created and has content
                if screenshot_path.exists() and screenshot_path.stat().st_size > 0:
                    logger.info(f"📸 Screenshot saved: {screenshot_path}")
                else:
                    logger.warning(f"⚠️ Screenshot file is empty or doesn't exist: {screenshot_path}")
            else:
                logger.warning(f"⚠️ Page is closed, cannot take screenshot for {test_name}")
        except Exception as e:
            logger.error(f"❌ Screenshot capture failed for {test_name}: {e}")
            import traceback
            logger.debug(traceback.format_exc())

    # Close context after test (only for call phase)
    if report.when == "call" and context:
        try:
            context.close()
            logger.debug(f"🔒 Closed browser context for: {test_name}")
        except Exception as e:
            logger.warning(f"⚠️ Could not close context: {e}")


