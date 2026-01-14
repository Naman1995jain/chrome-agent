
import os
import time
import json
import traceback
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

# --- Configuration ---
# API Key provided by user
API_KEY = "nvapi-TT2DEmo61e6qZHfNJ3kxrO_K10Al2hzyoae5ADEqMUg9yjWvllESJqiW0GvV4F4U"
# NVIDIA API Endpoint
BASE_URL = "https://integrate.api.nvidia.com/v1"
MODEL_NAME = "meta/llama-3.2-90b-vision-instruct"

GOAL = """
1. Login to Google (email: naman.jain@techsarasolutions.com, pass: December11@2025).
2. Search for "panacea residency".
3. Click "Reviews" tab.
4. Click "Write a review".
5. Give 2 stars.
6. Write comment "nice".
7. Click Post.
"""

# Client setup
client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

def setup_driver():
    print("🚀 Setting up Chrome browser...")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_argument("--log-level=3") # Suppress logs for cleaner output
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_interactive_elements(driver):
    """
    Scans the page for interactive elements and returns a simplified textual representation
    with specific IDs/XPath hints for the LLM to choose from.
    """
    # This is a simplified heuristic. better would be Accessibility Tree, but this is faster for a script.
    candidates = driver.find_elements(By.XPATH, 
        "//button | //a | //input | //textarea | //div[@role='button'] | //div[@role='radio'] | //span[@role='button']"
    )
    
    visible_elements = []
    for i, el in enumerate(candidates):
        try:
            if not el.is_displayed():
                continue
            
            tag = el.tag_name
            text = el.text.strip().replace("\n", " ")
            aria_label = el.get_attribute("aria-label") or ""
            placeholder = el.get_attribute("placeholder") or ""
            role = el.get_attribute("role") or ""
            el_type = el.get_attribute("type") or ""
            
            # Construct a descriptive string
            desc = f"[{i}] <{tag}"
            if text: desc += f" text='{text}'"
            if aria_label: desc += f" aria-label='{aria_label}'"
            if placeholder: desc += f" placeholder='{placeholder}'"
            if role: desc += f" role='{role}'"
            if el_type: desc += f" type='{el_type}'"
            desc += ">"
            
            visible_elements.append((i, el, desc))
        except:
            continue
            
    return visible_elements

# Logger setup
import logging
logging.basicConfig(
    filename='agent_execution.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(message)s',
    filemode='w'
)

def log(msg):
    print(msg)
    logging.info(msg)

def run_agent():
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    
    # History of actions to give context
    history = []
    
    try:
        # Initial navigation
        driver.get("https://accounts.google.com")
        
        step_count = 0
        MAX_STEPS = 20
        
        while step_count < MAX_STEPS:
            step_count += 1
            log(f"\n --- Step {step_count} ---")
            time.sleep(2) # Give page time to settle
            
            # 1. Observe
            visible_elements = get_interactive_elements(driver)
            # Create a string list of elements for the LLM
            elements_prompt = "\n".join([item[2] for item in visible_elements])
            
            # Truncate if too long (simple heuristic)
            if len(elements_prompt) > 4000:
                elements_prompt = elements_prompt[:4000] + "\n...(truncated)..."

            prompt = f"""
You are an autonomous browser agent. Your goal is:
{GOAL}

Current URL: {driver.current_url}
History of last 5 actions: {history[-5:]}

Visible Interactive Elements on the screen:
{elements_prompt}

INSTRUCTION:
Analyze the screen and decide the NEXT SINGLE ACTION to move closer to the goal.
If you need to GO to a specific URL (like google.com to search), return: {{"action": "navigate", "url": "https://www.google.com"}}.
If you need to TYPING something, return a JSON: {{"action": "type", "element_index": <index>, "text": "<text>"}}.
If you need to CLICK something, return a JSON: {{"action": "click", "element_index": <index>}}.
If you are waiting or need to sleep, return: {{"action": "wait"}}.
If you have achieved the goal (review posted), return: {{"action": "finish"}}.

Return ONLY the JSON. No markdown formatting.
"""

            # 2. Think
            log(" Thinking...")
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                    max_tokens=200, # Ensure we get a complete JSON response
                )
                
                llm_output = response.choices[0].message.content.strip()
                # Clean up potential markdown code blocks
                llm_output = llm_output.replace("```json", "").replace("```", "").strip()
                
                log(f" Agent says: {llm_output}")
            except Exception as e:
                log(f" LLM Error: {e}")
                time.sleep(5)
                continue
            
            try:
                cmd = json.loads(llm_output)
            except:
                log(f" Failed to parse JSON: {llm_output}")
                continue
                
            action = cmd.get("action")
            
            # 3. Act
            if action == "finish":
                log(" Goal Achieved!")
                break
            
            elif action == "navigate":
                url = cmd.get("url")
                try:
                    driver.get(url)
                    log(f" Navigated to: {url}")
                    history.append(f"Navigated to {url}")
                except Exception as e:
                    log(f" Navigation failed: {e}")

            elif action == "wait":
                time.sleep(3)
                history.append("Waited 3s")
                
            elif action == "click":
                idx = cmd.get("element_index")
                # Validate index
                target_el_tuple = next((x for x in visible_elements if x[0] == idx), None)
                if target_el_tuple:
                    el = target_el_tuple[1]
                    desc = target_el_tuple[2]
                    try:
                        # Scroll to view
                        driver.execute_script("arguments[0].scrollIntoView(true);", el)
                        time.sleep(0.5)
                        el.click()
                        log(f" Clicked: {desc}")
                        history.append(f"Clicked {desc}")
                    except Exception as e:
                        log(f" Click failed, trying JS click: {e}")
                        driver.execute_script("arguments[0].click();", el)
                        history.append(f"JS Clicked {desc}")
                else:
                    log(f" Invalid element index: {idx}")
                    
            elif action == "type":
                idx = cmd.get("element_index")
                text_to_type = cmd.get("text")
                target_el_tuple = next((x for x in visible_elements if x[0] == idx), None)
                if target_el_tuple:
                    el = target_el_tuple[1]
                    desc = target_el_tuple[2]
                    try:
                        el.click() # Focus
                        el.clear()
                        el.send_keys(text_to_type)
                        el.send_keys(Keys.RETURN) # often helpful
                        log(f"  Typed '{text_to_type}' into {desc}")
                        history.append(f"Typed '{text_to_type}'")
                    except Exception as e:
                        log(f" Typing failed: {e}")
                else:
                    log(f" Invalid element index: {idx}")
            else:
                log(f" Unknown action: {action}")
                
            time.sleep(2)

    except Exception as e:
        log(f" Critical Error: {e}")
        # traceback.print_exc() # print to stderr
        logging.error(traceback.format_exc())
    finally:
        log(" Closing logic finished. Browser stays open for 30s...")
        time.sleep(30)
        driver.quit()

if __name__ == "__main__":
    run_agent()
