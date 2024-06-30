from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import datetime

url = "https://jinkecn.en.alibaba.com/productlist-1.html?filter=all&sortType=modified-desc&spm=a2700.shop_pl.41413.dbtmnavgo"
html_directory = 'htmls_single_extract'
html_logs = 'logs_single_extract'

driver = webdriver.Edge()
driver.get(url)
wait = WebDriverWait(driver, 10)
next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "next-btn.next-btn-normal.next-btn-medium.next-pagination-item.next")))
html_dir = "html_0304_28"
logs_dir = "log_0304_28"
now = datetime.datetime.now()

# Each webpage imitate scrolling down to let each html fully load
stopping_point = [
  "next-row.next-row-no-padding.next-row-justify-space-between.next-row-align-center.nav-content",
  "next-icon.next-icon-arrow-down.next-icon-medium", 
  "next-pagination-jump", 
  "copyright"
]

# Need to set back to 0 for every new product
page_count = 0
product_count = 0

product_dic = {}

while next_button.is_enabled(): 
  page_count += 1
  print(f"at page {page_count}......")
  with open(f"{html_directory}/html_page_{page_count}.html", "a") as f:
    f.write(f"On page {page_count}...\n")
  for point_class in stopping_point: 
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, point_class)))
    ActionChains(driver).move_to_element(element).perform()
    time.sleep(2)
  next_button.click()
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  if soup.find('div', class_="component-product-list"):
    component_product_list = soup.find('div', class_="component-product-list")
    if component_product_list.find_all('div', class_='icbu-product-card vertical large product-item'): 

      # LOGGING: Store the HTML page to check if any errors
      with open(f"{html_directory}/html_page_{page_count}.html", "w") as f: 
        f.write(component_product_list.prettify())

      img_containers = component_product_list.find_all('div', class_='icbu-product-card vertical large product-item')
      
      # Get all image containers at the current page
      # two type of images class in the page: 1. icbu-product-card vertical large product-item last   2. icbu-product-card vertical large product-item
      for with_last_img in component_product_list.find_all('div', class_='icbu-product-card vertical large product-item last'): 
        img_containers.append(with_last_img)
      print(f"find {len(img_containers)} images \n")

      # Get all information from every image container
      for single_container in img_containers: 
        product_count += 1
        product_name = single_container.find('span', class_="title-con").text.strip() if single_container.find('span', class_="title-con") else -1
        product_img_element = single_container.find("img", class_="react-dove-image")
        if product_img_element and 'src' in product_img_element.attrs: 
          product_img = "https:" + product_img_element['src']
        else: 
          product_img = -1
        product_price = single_container.find("div", class_="price").text.strip() if single_container.find("div", class_="price") else -1
        product_shipping = single_container.find("div", class_="freight-str").text.strip()[11:] if single_container.find("div", class_="freight-str").text.strip() else -1
        product_MOQ = single_container.find("div", "moq").text.strip()[12:20] if single_container.find("div", "moq") else -1

        product_dic[f'name_{product_count}'] = product_name
        product_dic[f'image_link_{product_count}'] = product_img
        product_dic[f'price_{product_count}'] = product_price 
        product_dic[f'shipping_price_{product_count}'] = product_shipping
        product_dic[f'MOQ_{product_count}'] = product_MOQ

        # LOGGING: Logging each scripting to trace
        with open(f"{logs_dir}/products_{now}.txt", "a") as f: 
          f.write(f"product_{product_count} name: {product_name}\n")
          f.write(f"product_{product_count} img link: {product_img}\n")
          f.write(f"product_{product_count} price: {product_price}\n")
          f.write(f"product_{product_count} shipping: {product_shipping}\n")
          f.write(f"product_{product_count} MOQ: {product_MOQ} \n \n")

  next_button = driver.find_element(By.CLASS_NAME, "next-btn.next-btn-normal.next-btn-medium.next-pagination-item.next")

# LOGGING: logging what the dictionary looks like. 
# with open(f"{logs_dir}/products_{now}.txt", "a") as f:
#   f.write("here is the whole dictionary in all: \n")
#   f.write(f"{product_dic} \n \n")

driver.quit()

