from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize ChromeOptions and setup Chrome driver
chrome_options = webdriver.ChromeOptions()

# Open URL
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

driver.get('https://www.google.com/')

# Open a new window
driver.execute_script("window.open('');")

# Switch to the new window
driver.switch_to.window(driver.window_handles[1])
driver.get("http://stackoverflow.com")
time.sleep(3)

# Open a new window
driver.execute_script("window.open('');")
# Switch to the new window
driver.switch_to.window(driver.window_handles[2])
driver.get("https://www.reddit.com/")
time.sleep(3)
# close the active tab
driver.close()
time.sleep(3)

# Switch back to the first tab
driver.switch_to.window(driver.window_handles[0])
driver.get("https://bing.com")
time.sleep(3)

# Close the only tab, will also close the browser.
driver.close()
