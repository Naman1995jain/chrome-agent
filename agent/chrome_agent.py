"""
Chrome Automation Agent - Main Agent Class
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from .config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ChromeAgent:
    """
    Chrome Automation Agent for performing automated browser tasks
    """
    
    def __init__(self):
        """Initialize the Chrome agent with WebDriver"""
        self.driver = None
        self.config = Config()
        self._setup_driver()
    
    def _setup_driver(self):
        """Set up Chrome WebDriver with configured options"""
        try:
            logger.info("Setting up Chrome WebDriver...")
            
            # Configure Chrome options
            chrome_options = Options()
            for option in self.config.get_chrome_options():
                chrome_options.add_argument(option)
            
            # Initialize the driver with automatic ChromeDriver management
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set timeouts
            self.driver.set_page_load_timeout(self.config.PAGE_LOAD_TIMEOUT)
            self.driver.implicitly_wait(self.config.IMPLICIT_WAIT)
            
            logger.info("Chrome WebDriver initialized successfully")
            
        except WebDriverException as e:
            logger.error(f"Failed to initialize Chrome WebDriver: {e}")
            raise
    
    def search(self, query):
        """
        Perform a search operation on Google
        
        Args:
            query (str): The search query to execute
            
        Returns:
            bool: True if search was successful, False otherwise
        """
        try:
            logger.info(f"Navigating to {self.config.SEARCH_ENGINE_URL}...")
            self.driver.get(self.config.SEARCH_ENGINE_URL)
            
            # Wait for the search box to be present
            logger.info("Waiting for search box to load...")
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            logger.info(f"Typing search query: '{query}'")
            search_box.clear()
            search_box.send_keys(query)
            
            # Submit the search
            logger.info("Submitting search...")
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results to load
            logger.info("Waiting for search results...")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            
            logger.info(f"Search for '{query}' completed successfully")
            
            # Wait a bit to view results
            time.sleep(self.config.SEARCH_DELAY)
            
            return True
            
        except TimeoutException:
            logger.error("Timeout waiting for page elements")
            return False
        except Exception as e:
            logger.error(f"Error during search: {e}")
            return False
    
    def navigate_to(self, url):
        """
        Navigate to a specific URL
        
        Args:
            url (str): The URL to navigate to
            
        Returns:
            bool: True if navigation was successful, False otherwise
        """
        try:
            logger.info(f"Navigating to {url}...")
            self.driver.get(url)
            logger.info(f"Successfully navigated to {url}")
            return True
        except Exception as e:
            logger.error(f"Error navigating to {url}: {e}")
            return False
    
    def get_current_url(self):
        """
        Get the current URL
        
        Returns:
            str: Current URL or None if error
        """
        try:
            return self.driver.current_url
        except Exception as e:
            logger.error(f"Error getting current URL: {e}")
            return None
    
    def get_page_title(self):
        """
        Get the current page title
        
        Returns:
            str: Page title or None if error
        """
        try:
            return self.driver.title
        except Exception as e:
            logger.error(f"Error getting page title: {e}")
            return None
    
    def take_screenshot(self, filename):
        """
        Take a screenshot of the current page
        
        Args:
            filename (str): Path to save the screenshot
            
        Returns:
            bool: True if screenshot was saved, False otherwise
        """
        try:
            logger.info(f"Taking screenshot: {filename}")
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return False
    
    def wait(self, seconds):
        """
        Wait for a specified number of seconds
        
        Args:
            seconds (int): Number of seconds to wait
        """
        logger.info(f"Waiting for {seconds} seconds...")
        time.sleep(seconds)
    
    def close(self):
        """Close the browser and clean up resources"""
        if self.driver:
            try:
                logger.info("Closing Chrome browser...")
                self.driver.quit()
                logger.info("Browser closed successfully")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures browser is closed"""
        self.close()
