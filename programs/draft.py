from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import os

driver = webdriver.Chrome()

directory = 'draft_manufactures/'

# print(os.listdir(directory))

manufacturers_name_url = []

for filename in os.listdir(directory):
    if filename.endswith('1.html'): 
        filepath = os.path.join(directory, filename)
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

# print(manufacturers_name_url)

# i = 0
# for name, url in manufacturers_name_url: 
    
#     print(f"it's manufacture {name}")
#     print(f"url is {url} \n")
#     i += 1
#     driver.get('https://xfsilicon.en.alibaba.com/factory.html')

#     soup_url_original = BeautifulSoup(driver.page_source, 'html.parser')
#     # with open(f"manufacture {i}_original.html", 'w')as file: 
#     #     file.write(str(soup_url_original))
    
#     driver.find_element(By.CLASS_NAME, "all-tags").click()
#     soup_url_opened = BeautifulSoup(driver.page_source, 'html.parser')
#     verified_capabilities = soup.find('div', class_='next-dialog-body')
    

#     if i == 3: 
#         break


driver.get('https://xfsilicon.en.alibaba.com/factory.html')

soup_url_original = BeautifulSoup(driver.page_source, 'html.parser')
# with open(f"manufacture {i}_original.html", 'w')as file: 
#     file.write(str(soup_url_original))

driver.find_element(By.CLASS_NAME, "all-tags").click()
soup_url_opened = BeautifulSoup(driver.page_source, 'html.parser')
verified_capabilities = soup.find('div', class_='next-dialog-body')