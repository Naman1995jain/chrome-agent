"""
Simple Chrome Automation Demo
A simplified version that searches for "abc" on Google
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("=" * 60)
print("🤖 Chrome Automation Agent - Simple Demo")
print("=" * 60)

try:
    print("\n📋 Setting up Chrome options...")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    print("🚀 Launching Chrome browser...")
    driver = webdriver.Chrome(options=chrome_options)
    
    print("🌐 Navigating to Google...")
    driver.get("https://www.google.com")
    
    print("⏳ Waiting for search box...")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    
    print("⌨️  Typing 'abc' in search box...")
    search_box.send_keys("abc")
    
    print("🔍 Submitting search...")
    search_box.send_keys(Keys.RETURN)
    
    print("⏳ Waiting for results...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search"))
    )
    
    print("\n✅ Search completed successfully!")
    print(f"📄 Page Title: {driver.title}")
    print(f"🔗 Current URL: {driver.current_url}")
    
    # Take screenshot
    screenshot_file = "search_result.png"
    driver.save_screenshot(screenshot_file)
    print(f"📸 Screenshot saved: {screenshot_file}")
    
    print("\n⏳ Keeping browser open for 5 seconds...")
    time.sleep(5)
    
    print("🔒 Closing browser...")
    driver.quit()
    
    print("\n" + "=" * 60)
    print("✅ Demo completed successfully!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error occurred: {e}")
    print("\nTroubleshooting tips:")
    print("1. Make sure Google Chrome is installed")
    print("2. Check your internet connection")
    print("3. Try running: python -m pip install --upgrade selenium")
    
    if 'driver' in locals():
        driver.quit()
