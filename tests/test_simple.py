"""
Simple test to verify browser stays open
"""
import pytest
import time
# Logger is automatically injected by conftest.py - use 'logger' directly


@pytest.mark.controls
def test_simple_browser_check(page):
    """Simple test to check if browser stays open - uses page directly"""
    logger.info("\n" + "="*60)
    logger.info("Starting simple test")
    logger.info("Browser should be visible now!")
    logger.info("="*60 + "\n")
    
    # Wait a bit so user can see browser
    logger.info("Step 1: Waiting 5 seconds - you should see browser window...")
    logger.info("If you see the browser window, it's working!")
    time.sleep(5)
    
    # Just navigate to a simple page first (not Storybook)
    logger.info("\nStep 2: Navigating to example.com (simple page)...")
    navigation_success = False
    try:
        response = page.goto("https://example.com", timeout=15000, wait_until="domcontentloaded")
        logger.info("✅ Navigation successful")
        logger.info(f"  Status: {response.status if response else 'N/A'}")
        logger.info(f"  Page title: {page.title()}")
        navigation_success = True
    except Exception as e:
        logger.error(f"✗ Navigation failed: {type(e).__name__}: {e}")
        logger.info("But browser should still stay open!")
        # Don't raise - let test continue so browser stays open
    
    logger.info("\nStep 3: Test will pause here for 15 seconds...")
    if navigation_success:
        logger.info("You should see the browser window with example.com!")
    else:
        logger.info("You should see the browser window (even though navigation failed)")
    time.sleep(15)
    
    logger.info("\n✅ Test completed successfully")
    logger.info("Browser will stay open for 30 seconds after all tests")
    logger.info("You can inspect it now!")
