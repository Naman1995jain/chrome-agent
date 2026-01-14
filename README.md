# 🤖 Chrome Automation Agent

A powerful Python-based automation agent that can control Chrome browser and perform automated tasks like web searching, navigation, and more.

## ✨ Features

- 🌐 **Automated Browser Control**: Open and control Chrome programmatically
- 🔍 **Smart Search**: Perform automated Google searches
- 📸 **Screenshot Capture**: Take screenshots of web pages
- 🛠️ **Extensible Design**: Easy to add new automation tasks
- 📝 **Comprehensive Logging**: Detailed logs for debugging and monitoring
- ⚙️ **Configurable**: Customize browser behavior via configuration

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Google Chrome browser installed

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd chrome-test
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - `selenium`: Browser automation framework
   - `webdriver-manager`: Automatic ChromeDriver management (no manual driver download needed!)

### Running the Agent

Simply run the main script:

```bash
python main.py
```

The agent will:
1. ✅ Open Chrome browser
2. ✅ Navigate to Google
3. ✅ Search for "abc"
4. ✅ Display search results
5. ✅ Take a screenshot (`search_result.png`)
6. ✅ Close the browser automatically

## 📁 Project Structure

```
chrome-test/
├── agent/
│   ├── __init__.py          # Package initialization
│   ├── chrome_agent.py      # Main agent class with automation logic
│   └── config.py            # Configuration settings
├── main.py                  # Entry point script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## ⚙️ Configuration

Edit `agent/config.py` to customize the agent behavior:

```python
class Config:
    HEADLESS = False           # Set True to run browser in background
    WINDOW_SIZE = "1920,1080"  # Browser window size
    SEARCH_ENGINE_URL = "https://www.google.com"
    PAGE_LOAD_TIMEOUT = 30     # Page load timeout in seconds
    SEARCH_DELAY = 2           # Time to view results before closing
```

## 🎯 Usage Examples

### Basic Search

```python
from agent import ChromeAgent

# Using context manager (recommended - auto-closes browser)
with ChromeAgent() as agent:
    agent.search("abc")
```

### Custom Navigation

```python
from agent import ChromeAgent

with ChromeAgent() as agent:
    # Navigate to any URL
    agent.navigate_to("https://www.example.com")
    
    # Get current page info
    print(f"Title: {agent.get_page_title()}")
    print(f"URL: {agent.get_current_url()}")
    
    # Take screenshot
    agent.take_screenshot("example.png")
```

### Manual Browser Control

```python
from agent import ChromeAgent

agent = ChromeAgent()
try:
    agent.search("Python automation")
    agent.wait(10)  # Keep browser open for 10 seconds
finally:
    agent.close()  # Always close the browser
```

## 🔧 Advanced Features

### Available Methods

- `search(query)` - Perform Google search
- `navigate_to(url)` - Navigate to any URL
- `get_current_url()` - Get current page URL
- `get_page_title()` - Get current page title
- `take_screenshot(filename)` - Save screenshot
- `wait(seconds)` - Wait for specified time
- `close()` - Close browser and cleanup

### Headless Mode

To run the browser in the background (no visible window):

```python
# In agent/config.py
HEADLESS = True
```

## 🐛 Troubleshooting

### ChromeDriver Issues

The project uses `webdriver-manager` which automatically downloads and manages ChromeDriver. If you encounter issues:

1. Ensure Chrome browser is installed
2. Check your internet connection (needed for first-time driver download)
3. Try clearing the driver cache: Delete `~/.wdm` folder

### Common Errors

**"Chrome not found"**: Install Google Chrome browser

**"Timeout Exception"**: Increase `PAGE_LOAD_TIMEOUT` in config.py

**"Element not found"**: Website structure may have changed; check element selectors

## 🚀 Extending the Agent

Add new automation tasks by extending the `ChromeAgent` class:

```python
# In agent/chrome_agent.py

def click_element(self, selector):
    """Click an element by CSS selector"""
    element = self.driver.find_element(By.CSS_SELECTOR, selector)
    element.click()

def fill_form(self, field_name, value):
    """Fill a form field"""
    field = self.driver.find_element(By.NAME, field_name)
    field.send_keys(value)
```

## 📝 Future Enhancements

Potential features to add:
- 📧 Email automation
- 📊 Data scraping
- 🔄 Scheduled tasks (cron jobs)
- 💾 Database integration for storing results
- 🤖 AI-powered decision making
- 📱 Multi-browser support (Firefox, Edge)

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to extend and improve this automation agent!

---

**Made with ❤️ using Python & Selenium**
