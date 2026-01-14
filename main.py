"""
Chrome Automation Agent - Main Entry Point

This script demonstrates the Chrome automation agent by:
1. Opening Chrome browser
2. Searching for "abc" on Google
3. Displaying results
"""

import sys
import logging
from agent import ChromeAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function to run the Chrome automation agent"""
    
    logger.info("=" * 60)
    logger.info("Chrome Automation Agent - Starting")
    logger.info("=" * 60)
    
    try:
        # Use context manager to ensure browser closes properly
        with ChromeAgent() as agent:
            
            # Perform search for "abc"
            logger.info("\n🔍 Performing search for 'abc'...")
            success = agent.search("abc")
            
            if success:
                logger.info("✅ Search completed successfully!")
                
                # Display current page info
                current_url = agent.get_current_url()
                page_title = agent.get_page_title()
                
                logger.info(f"\n📄 Current Page Title: {page_title}")
                logger.info(f"🔗 Current URL: {current_url}")
                
                # Take a screenshot
                screenshot_path = "search_result.png"
                if agent.take_screenshot(screenshot_path):
                    logger.info(f"📸 Screenshot saved to: {screenshot_path}")
                
                # Wait a bit so you can see the results
                logger.info("\n⏳ Keeping browser open for 5 seconds to view results...")
                agent.wait(5)
                
            else:
                logger.error("❌ Search failed!")
                return 1
        
        logger.info("\n" + "=" * 60)
        logger.info("Chrome Automation Agent - Completed Successfully")
        logger.info("=" * 60)
        return 0
        
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Interrupted by user")
        return 130
        
    except Exception as e:
        logger.error(f"\n❌ An error occurred: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
