"""
Configuration settings for Chrome Automation Agent
"""

class Config:
    """Configuration class for the Chrome agent"""
    
    # Browser settings
    HEADLESS = False  # Set to True to run browser in background
    WINDOW_SIZE = "1920,1080"
    
    # Search settings
    SEARCH_ENGINE_URL = "https://www.google.com"
    
    # Timeout settings (in seconds)
    PAGE_LOAD_TIMEOUT = 30
    IMPLICIT_WAIT = 10
    SEARCH_DELAY = 2  # Time to wait after search to view results
    
    # Chrome options
    DISABLE_GPU = True
    NO_SANDBOX = False
    DISABLE_DEV_SHM = False
    
    @classmethod
    def get_chrome_options(cls):
        """
        Returns a list of Chrome options based on configuration
        
        Returns:
            list: Chrome options as strings
        """
        options = []
        
        if cls.HEADLESS:
            options.append("--headless")
        
        if cls.WINDOW_SIZE:
            options.append(f"--window-size={cls.WINDOW_SIZE}")
        
        if cls.DISABLE_GPU:
            options.append("--disable-gpu")
        
        if cls.NO_SANDBOX:
            options.append("--no-sandbox")
        
        if cls.DISABLE_DEV_SHM:
            options.append("--disable-dev-shm-usage")
        
        # Additional options for better stability
        options.extend([
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--disable-popup-blocking",
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ])
        
        return options
