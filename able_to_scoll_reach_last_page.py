from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

url = "https://jinkecn.en.alibaba.com/productlist-1.html?filter=all&sortType=modified-desc&spm=a2700.shop_pl.41413.dbtmnavgo"
html_directory = 'htmls_single_extract'
html_logs = 'logs_single_extract'
page_count = 0
driver = webdriver.Edge()
driver.get(url)
wait = WebDriverWait(driver, 10)
next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "next-btn.next-btn-normal.next-btn-medium.next-pagination-item.next")))
btm_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "copyright")))

while next_button.is_enabled(): 
  page_count += 1
  print(f"at page {page_count}......")
  ActionChains(driver).move_to_element(btm_element).perform()
  time.sleep(3)
  next_button.click()
  find_image = False
  # 
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  if soup.find('div', class_="component-product-list"):
    component_product_list = soup.find('div', class_="component-product-list")
    if component_product_list.find_all('img', class_='react-dove-image'): 
      img_list = component_product_list.find_all('img', class_='react-dove-image')
      print(f"find {len(img_list)} images \n")
  next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "next-btn.next-btn-normal.next-btn-medium.next-pagination-item.next")))

with open("single_extract.html", "w") as file: 
  file.write(soup.prettify())

driver.quit()

