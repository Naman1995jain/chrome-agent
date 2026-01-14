"""
Google Search Automation Agent
Logs into Google account, searches for "abc", and opens the first result
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Google account credentials
GOOGLE_EMAIL = "naman.jain@techsarasolutions.com"
GOOGLE_PASSWORD = "December11@2025"
SEARCH_QUERY = "panacea residency"

print("=" * 70)
print("🔍 Google Search Automation Agent", flush=True)
print("=" * 70)

try:
    print("\n🚀 Setting up Chrome browser...")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # Suppress console logs (fixes DEPRECATED_ENDPOINT error visibility)
    chrome_options.add_argument("--log-level=3")
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)
    short_wait = WebDriverWait(driver, 5)
    
    # Step 1: Navigate to Google and login
    print("\n🌐 Navigating to Google...")
    driver.get("https://accounts.google.com")
    time.sleep(2)
    
    # Step 2: Enter email
    print(f"📝 Entering email: {GOOGLE_EMAIL}")
    email_field = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    email_field.send_keys(GOOGLE_EMAIL)
    email_field.send_keys(Keys.RETURN)
    time.sleep(3)
    
    # Step 3: Enter password
    print("🔑 Entering password...")
    password_field = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
    )
    password_field.send_keys(GOOGLE_PASSWORD)
    password_field.send_keys(Keys.RETURN)
    
    print("⏳ Waiting for login to complete...")
    time.sleep(5)
    
    print("✅ Successfully logged into Google account!")
    
    # Step 4: Navigate to Google Search
    print(f"\n🔍 Navigating to Google Search...")
    driver.get("https://www.google.com")
    time.sleep(2)
    
    # Step 5: Perform search for "abc"
    print(f"⌨️  Searching for '{SEARCH_QUERY}'...")
    search_box = wait.until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys(SEARCH_QUERY)
    search_box.send_keys(Keys.RETURN)
    
    print("⏳ Waiting for search results...")
    time.sleep(3)
    
    # Step 6: Navigate to Reviews in Knowledge Panel
    print("\n🎯 Looking for Reviews tab...")
    try:
        # Looking for 'Reviews' tab/button in the Knowledge Panel
        # This is typically on the right side for desktop views of Google Search
        reviews_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Reviews')] | //span[contains(text(), 'Reviews')]"))
        )
        reviews_tab.click()
        print("✅ Clicked Reviews tab")
        time.sleep(2)
        
        # Step 7: Click 'Write a review'
        print("✍️ Looking for 'Write a review' button...")
        write_review_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Write a review')] | //div[contains(text(), 'Write a review')]"))
        )
        write_review_btn.click()
        print("✅ Clicked 'Write a review'", flush=True)
        time.sleep(3)
        
        # Step 8: Interact with Review Modal
        
        # 0. Removed blocking popup logic as it was causing tooltips to open
        # We will interact with the comment box first to clear focus/overlays

        # 1. Click Comment Box first (clears focus, dismisses tooltips)
        print("📝 Clicking comment box to clear overlays...", flush=True)
        comment_box = wait.until(
            EC.element_to_be_clickable((By.XPATH, 
                "//textarea[contains(@aria-label, 'Share details')] | " + 
                "//textarea[@aria-label='Share details of your own experience at this place'] | " +
                "//div[contains(text(), 'Share details')] | " + 
                "//textarea"
            ))
        )
        comment_box.click()
        time.sleep(1)

        # 2. Rate 1 Star
        print("⭐ Rating 1 star...", flush=True)
        # Save screenshot before clicking star to debug visibility
        driver.save_screenshot("before_star_click.png")
        
        try:
            # Try to find the element
            one_star = wait.until(
                EC.presence_of_element_located((By.XPATH, 
                    "//div[@class='s2g3Od'] | " + # Common container class for stars
                    "//div[@aria-label='Rating stars']/*[1] | " +
                    "//div[@aria-label='Rating stars']//span[@role='radio'][1] | " +
                    "//*[@aria-label='Rating stars']//*[@data-value='1'] | " +
                    "(//div[@role='radio'])[1]"
                ))
            )
            
            # Method 1: ActionChains (Move and Click)
            print("   Attempting ActionChains click...", flush=True)
            try:
                actions = webdriver.ActionChains(driver)
                actions.move_to_element(one_star).click().perform()
                print("✅ Selected 1 star (via ActionChains)", flush=True)
            except Exception as ac_e:
                print(f"   ActionChains failed ({ac_e}), trying standard click...", flush=True)
                
                # Method 2: Standard Click
                one_star.click()
                print("✅ Selected 1 star (via Standard Click)", flush=True)

        except Exception as e:
            print(f"⚠️ Failed to click star normally: {e}", flush=True)
            print("   Attempting JavaScript click fallback...", flush=True)
            try:
                # Fallback: Find 1st radio button and click via JS
                # Re-locate ensures we don't have a stale element
                one_star_js = driver.find_element(By.XPATH, "(//div[@role='radio'])[1] | //*[@data-value='1']")
                driver.execute_script("arguments[0].scrollIntoView(true);", one_star_js)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", one_star_js)
                print("✅ Selected 1 star (via JS)", flush=True)
            except Exception as js_e:
                 print(f"❌ JS Click also failed: {js_e}", flush=True)
                 driver.save_screenshot("star_click_failure.png")
                 raise e
        
        # 3. Enter comment "nice"
        print("📝 Entering comment...")
        # comment_box ALREADY defined above
        # comment_box.click() # Already clicked
        time.sleep(1)
        time.sleep(1)
        comment_box.send_keys("nice")
        print("✅ Entered comment: 'nice'")
        time.sleep(1)
        
        # 3. Click Post (Blue button)
        print("🚀 Clicking Post button...")
        post_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Post']] | //button[text()='Post'] | //div[@role='button'][.//span[text()='Post']]"))
        )
        post_btn.click()
        print("✅ Clicked Post button")
        
        # Wait for confirmation
        time.sleep(5)
        print("✅ Review process completed!")
        
    except Exception as e:
        print(f"❌ Error in review process: {e}")
        import traceback
        traceback.print_exc()
        
        # Capture screenshot on failure
        driver.save_screenshot("review_failure.png")
        print("📸 Screenshot saved as review_failure.png")

    
    print("\n⏳ Keeping browser open for 15 seconds to view the page...")
    time.sleep(15)
    
    print("\n🔒 Closing browser...")
    driver.quit()
    
    print("\n" + "=" * 70)
    print("✅ Google search automation completed successfully!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ Error occurred: {e}")
    import traceback
    traceback.print_exc()
    
    print("\nTroubleshooting:")
    print("1. Check your email and password")
    print("2. You may need to approve the login from a new device")
    print("3. Check if 2-factor authentication is enabled")
    print("4. Google may require additional verification")
    
    if 'driver' in locals():
        print("\n⏳ Keeping browser open for 30 seconds for inspection...")
        time.sleep(30)
        driver.quit()
