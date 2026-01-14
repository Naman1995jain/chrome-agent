"""
Gmail Automation Agent
Logs into Gmail, searches for content, and opens the first result
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Gmail credentials
GMAIL_EMAIL = "naman.jain@techsarasolutions.com"
GMAIL_PASSWORD = "December11@2025"
SEARCH_QUERY = "abc"

print("=" * 70)
print("📧 Gmail Automation Agent")
print("=" * 70)

try:
    print("\n🚀 Setting up Chrome browser...")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)
    
    # Step 1: Navigate to Gmail
    print("\n📬 Navigating to Gmail...")
    driver.get("https://mail.google.com")
    time.sleep(2)
    
    # Step 2: Enter email
    print(f"📝 Entering email: {GMAIL_EMAIL}")
    email_field = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    email_field.send_keys(GMAIL_EMAIL)
    email_field.send_keys(Keys.RETURN)
    time.sleep(3)
    
    # Step 3: Enter password
    print("🔑 Entering password...")
    password_field = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
    )
    password_field.send_keys(GMAIL_PASSWORD)
    password_field.send_keys(Keys.RETURN)
    
    print("⏳ Waiting for Gmail to load...")
    time.sleep(5)
    
    # Step 4: Wait for Gmail inbox to load
    print("📥 Waiting for inbox to load...")
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='main']"))
    )
    print("✅ Successfully logged into Gmail!")
    
    # Step 5: Search for "abc"
    print(f"\n🔍 Searching for '{SEARCH_QUERY}' in Gmail...")
    search_box = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search mail']"))
    )
    search_box.click()
    time.sleep(1)
    search_box.send_keys(SEARCH_QUERY)
    search_box.send_keys(Keys.RETURN)
    
    print("⏳ Waiting for search results...")
    time.sleep(4)
    
    # Step 6: Find and click the first email result
    print("📧 Looking for first email result...")
    try:
        # Wait for email results to appear
        first_email = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr.zA"))
        )
        
        print("✅ Found first email result!")
        print("🖱️  Clicking on first email...")
        first_email.click()
        
        time.sleep(3)
        
        # Step 7: Look for links in the email and open the first one
        print("\n🔗 Looking for links in the email...")
        try:
            # Wait for email body to load
            email_body = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='listitem']"))
            )
            
            # Find all links in the email
            links = driver.find_elements(By.CSS_SELECTOR, "a[href]")
            
            # Filter out Gmail UI links and get actual content links
            content_links = [link for link in links if link.get_attribute('href') 
                           and not any(x in link.get_attribute('href') for x in 
                           ['mail.google.com', 'accounts.google.com', 'support.google.com'])]
            
            if content_links:
                first_link = content_links[0]
                link_url = first_link.get_attribute('href')
                print(f"🔗 Found link: {link_url}")
                print("🖱️  Opening first link...")
                
                # Open link in new tab
                driver.execute_script("window.open(arguments[0], '_blank');", link_url)
                
                # Switch to new tab
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(3)
                
                print(f"✅ Opened link successfully!")
                print(f"📄 Current page: {driver.title}")
                print(f"🔗 URL: {driver.current_url}")
            else:
                print("⚠️  No external links found in the first email")
                
        except Exception as e:
            print(f"⚠️  Could not find/open links in email: {e}")
    
    except Exception as e:
        print(f"⚠️  No email results found for '{SEARCH_QUERY}': {e}")
    
    print("\n⏳ Keeping browser open for 10 seconds...")
    time.sleep(10)
    
    print("\n🔒 Closing browser...")
    driver.quit()
    
    print("\n" + "=" * 70)
    print("✅ Gmail automation completed successfully!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ Error occurred: {e}")
    print("\nTroubleshooting:")
    print("1. Check your email and password")
    print("2. You may need to approve the login from a new device")
    print("3. Check if 2-factor authentication is enabled")
    
    if 'driver' in locals():
        print("\n⏳ Keeping browser open for inspection...")
        time.sleep(30)
        driver.quit()
