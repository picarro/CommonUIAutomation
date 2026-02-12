"""
Minimal test - just opens browser and waits
Use this to verify browser stays open
"""
import pytest
import time
# Logger is automatically injected by conftest.py - use 'logger' directly


@pytest.mark.controls
def test_minimal_browser(page):
    """Minimal test - just opens browser"""
    logger.info("\n" + "="*60)
    logger.info("MINIMAL TEST - Just opening browser")
    logger.info("="*60 + "\n")
    
    logger.info("Step 1: Browser should be visible now")
    logger.info("Waiting 5 seconds so you can see it...")
    time.sleep(5)
    
    logger.info("\nStep 2: Navigating to a simple page...")
    try:
        page.goto("https://example.com", timeout=10000)
        logger.info("✅ Navigation successful")
        logger.info(f"Page title: {page.title()}")
    except Exception as e:
        logger.error(f"✗ Navigation failed: {e}")
        logger.info("But browser should still be open!")
    
    logger.info("\nStep 3: Waiting 10 more seconds...")
    logger.info("Browser should stay visible!")
    time.sleep(10)
    
    logger.info("\n✅ Test completed")
    logger.info("Browser will stay open for 30 seconds after this")

