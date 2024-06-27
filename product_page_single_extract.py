from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url = "https://jinkecn.en.alibaba.com/productlist-1.html?filter=all&sortType=modified-desc&spm=a2700.shop_pl.41413.dbtmnavgo"
html_directory = 'htmls_single_extract'
html_logs = 'logs_single_extract'
count = 1

# driver = webdriver.Chrome()  
driver = webdriver.Edge()
driver.get(url)
# wait = WebDriverWait(driver, 10)
next_button = driver.find_elements(By.CLASS_NAME, "next-btn.next-btn-normal.next-btn-medium.next-pagination-item.next")
# next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "next-btn.next-btn-normal.next-btn-medium.next-pagination-item.next")))
# ActionChains(driver).move_to_element(next_button).perform()

# while next_button[0].is_enabled(): 
#   print(f"at page {count}......")
#   # ActionChains(driver).move_to_element(next_button).perform()
#   # next_button[0].click()
find_image = False

while not find_image: 
  count += 1
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  if soup.find('div', class_="component-product-list"):
    component_product_list = soup.find('div', class_="component-product-list")
    print(f"{count}th time grab the image container......")
    with open(f"{html_directory}/html_no_img_{count}.html", "w") as file: 
      file.write(soup.prettify())
    if component_product_list.find_all('img', class_='react-dove-image'): 
      img_list = component_product_list.find_all('img', class_='react-dove-image')
      print(f"find {len(img_list)} images \n")
      find_image = True
      products_images = img_list
  time.sleep(3)
time.sleep(3)

with open("single_extract.html", "w") as file: 
  file.write(soup.prettify())

driver.quit()

