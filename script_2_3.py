from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re
import time
import datetime
import csv
import requests


now = datetime.datetime.now()
skipped_manufactures = []

html_dir = "html_2_3"
logs_dir = "log_manufacture_2_3"
img_dir = 'manufacture_2_3_pictures'
# Get manufactures from csv file
csv_dir = 'data/manufacture_2_3.csv'
csv_picture_dir = f'manufactures_2_3_pics_{now}.csv'
max_length = 0
os.makedirs(logs_dir, exist_ok=True)


def sanitize_filename(name):
    """ Sanitize the filename by removing or replacing unwanted characters """
    return re.sub(r'[\/:*?"<>|]', "_", name)

def download_image(image_url, image_file_name, sub_folder):

  image_file_name = sanitize_filename(image_file_name)

  with open(f"{logs_dir}/products_{now}.txt", "a") as f: 
    f.write(f"Getting image {image_file_name} ... \n")
  full_path = os.path.join(img_dir, sub_folder)

  os.makedirs(full_path, exist_ok=True)

  image_file_name = os.path.join(full_path, image_file_name)
  
  # Send a GET request to the image URL
  response = requests.get(image_url, stream=True)
  
  # Open a local file with write-binary mode
  with open(f"{image_file_name}.jpg", 'wb') as file:
      # Check if the request was successful
      if response.status_code == 200:
        # Write the contents of the response to a file
        for chunk in response.iter_content(chunk_size=128):
          file.write(chunk)
        with open(f"{logs_dir}/products_{now}.txt", "a") as f: 
          f.write(f"success! \n \n")
      else:
        with open(f"{logs_dir}/products_{now}.txt", "a") as f: 
          f.write(f"Failed to retrieve image. Status code: {response.status_code} \n \n")


# Get all manufactures as [(manufacture_name_1, link_1), (manufacture_name_2, link_2), ...] from stored file
def get_manufacture_from_dir(): 
  manufactures_dir = '../apparel_manufactures'
  manufacturers_name_url = []
  for filename in os.listdir(manufactures_dir):
    if filename.endswith('.html'):  # Ensures only HTML files are processed
      # print(f"reading file: {filename}......")
      filepath = os.path.join(manufactures_dir, filename)
      with open(filepath, 'r', encoding='utf-8') as file:
          content = file.read()
          soup = BeautifulSoup(content, 'html.parser')
          factory_cards = soup.find_all('div', class_='factory-card')

          for card in factory_cards:
            detail_info = card.find('div', class_='detail-info')
            if detail_info:
              name_tag = detail_info.find('h3')
              if name_tag and name_tag.find('a'):
                manufacturer_name = name_tag.find('a').text.strip()  
                manufacturer_link = name_tag.find('a')['href']       
                manufacturers_name_url.append((manufacturer_name, manufacturer_link))
  return manufacturers_name_url



# Visit and get all info of all product from manufacture product page
def get_product_dic(driver, manufacture_name):

  print(f"Now scripting manufacture {manufacture_name}:  \n")

  with open(f"{logs_dir}/products_{now}.txt", "a") as f: 
    f.write(f"Manufacture name: {manufacture_name}: \n")
  
  wait = WebDriverWait(driver, 10)
  next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "next-btn.next-btn-normal.next-btn-medium.next-pagination-item.next")))

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
  product_dic["manufacture_name"] = manufacture_name

  while next_button.is_enabled(): 
    page_count += 1
    print(f"at page {page_count}......")
    with open(f"{logs_dir}/products_{now}.txt", "a") as f: 
      f.write(f"On page {page_count}... \n")
    soup_check = BeautifulSoup(driver.page_source, 'html.parser')
    if not soup_check.find('div', class_="no-data common"): 
      for point_class in stopping_point: 
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, point_class)))
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(2)
    else: 
      with open(f"{logs_dir}/products_{now}.txt", "a") as f: 
        f.write("No stopping point at this page.")  
      break
    with open(f"{logs_dir}/products_{now}.txt", "a") as f: 
      f.write(f"next_button is like: {next_button}")
    time.sleep(2)
    next_button.click()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if soup.find('div', class_="component-product-list"):
      component_product_list = soup.find('div', class_="component-product-list")
      if component_product_list.find_all('div', class_='icbu-product-card vertical large product-item'): 

        # LOGGING: Store the HTML page to check if any errors
        html_file_path = os.path.join(html_dir, manufacture_name)
        os.makedirs(html_file_path, exist_ok=True)
        html_file_path = os.path.join(html_file_path, f"html_page_{page_count}.html")
        with open(html_file_path, "w") as f: 
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
            # img_dir = 'manufacture_pictures' + def download_image(image_url, image_file_name, sub_folder):
            download_image(product_img, product_name, manufacture_name)
          else: 
            product_img = -1
          product_price = single_container.find("div", class_="price").text.strip() if single_container.find("div", class_="price") else -1
          product_shipping = single_container.find("div", class_="freight-str").text.strip() if single_container.find("div", class_="freight-str") else -1
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
  
  driver.quit()

  skipped_manufactures.append(manufacture_name)

  return product_dic



def get_the_normal_manufacture(driver): 
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  if soup.find('div', 'info-404img') or soup.find('div', class_='icbu-mod-wrapper no-title icbu-pc-cpCompanyOverview false v2'): 
    return False
  return True



def writing_to_csv(path_to_write, dict_to_write): 
  with open(path_to_write, "a") as csvfile: 
    fieldnames = list(dict_to_write.keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow(dict_to_write)


with open(csv_dir, "r") as csvfile: 
  next(csvfile)
  reader = csv.reader(csvfile, delimiter=',')       
  with open(f"{logs_dir}/products_{now}.txt", "a") as f: 
    f.write(f"existing column info: {reader} \n")
  count = 0

  # Get the link for current manufactures one by one
  for row in reader: 
    count += 1
    # if count > 4: 
    #   break
    manufacture_name = row[0]
    link_to_visit = row[1]

    # Skip the manufactures that already have pictures stored
    if row[0] in skipped_manufactures: 
      with open(f"{logs_dir}/products_{now}.txt", "a") as f: 
        f.write(f"Skipped {manufacture_name} , visit {link_to_visit} \n \n ")
      continue

    # navigate to the product page
    driver = webdriver.Edge()
    driver.get(link_to_visit)
    if not get_the_normal_manufacture(driver): 
      continue

    # scrolling down a bit
    wait = WebDriverWait(driver, 10)
    stopping_point = [
      "module-verifiedAllProducts", 
      "verified-all-button",
      ]
    for point_class in stopping_point: 
      element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, point_class)))
      ActionChains(driver).move_to_element(element).perform()
      time.sleep(2)
    parent_element = driver.find_element(By.CLASS_NAME, "module-verifiedAllProducts")
    view_more_button = parent_element.find_elements(By.CLASS_NAME, "verified-all-button")
    view_more_button[0].click()
    
    # Get the manufacture product infos and write them in dictionary
    product_dic = get_product_dic(driver, manufacture_name=manufacture_name)

    # Get the longest product dictionary and use its key as headers at last
    if len(product_dic) > max_length: 
      max_length = len(product_dic)
      max_dict = product_dic

    with open(f"{logs_dir}/products_{now}.txt", "a") as f: 
      f.write(f"Current max length dictionary length is: {max_length} \n")
      f.write(f"Skipped manufactures for now: \n {skipped_manufactures} \n \n ")

    # Writing to csv file...
    writing_to_csv(csv_picture_dir, product_dic)    

# Get the max length dictionary to make its keys as the header
with open(f"{logs_dir}/products_{now}.txt", "a") as f: 
  f.write(f"Max length dictionary is: {max_dict} \n")

