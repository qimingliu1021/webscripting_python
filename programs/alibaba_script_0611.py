from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import csv
import re

# Setup Selenium WebDriver
driver = webdriver.Chrome()  

directory = '../apparel_manufactures'
manufacturers_name_url = []

for filename in os.listdir(directory):
  if filename.endswith('.html'):  # Ensures only HTML files are processed
    # print(f"reading file: {filename}......")
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

detailed_manufacturers_data = []

count = 1

def categorize_capabilities(soup):
    services = []
    quality_control = []
    certificates = []

    list_items = soup.find_all('div', class_='list-item')
    for item in list_items:
        text = item.get_text(strip=True).lower()

        if len(text) < 50: 
        
            if any(keyword in text for keyword in ['supply chain', 'customization', 'warehouses', 'procurement', 'installation', 'technical support', 'design capabilities', 'factory', 'project solutions']):
                services.append(text)
            elif any(keyword in text for keyword in ['identification', 'inspection', 'inspectors', 'testing', 'traceability', 'warranty']):
                quality_control.append(text)
            else:
                certificates.append(text)
    
    return services, quality_control, certificates


# Visit each manufacturer's page
for name, url in manufacturers_name_url:

    ##############################           MONITORING 1            ##############################
    print(f"\nmanufacture {count}: \n")
    print(f"{name} please visit - {url}")

    count += 1
    # a switch - on/off to control the # number of manufactures
    # if count == 3: 
    #     break;

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    different_manufactures = {}

    all_tags_elements = driver.find_elements(By.CLASS_NAME, "all-tags")
    if all_tags_elements: 
        all_tags_elements[0].click()
        soup_opened = BeautifulSoup(driver.page_source, 'html.parser')
        services, quality_control, certificates = categorize_capabilities(soup_opened)
    else: 
        different_manufactures[name] = url
        services, quality_control, certificates = 'problem', 'problem', 'problem'


    #############################   order numbers and total amounts   #############################
    total_order_number = 'N/A'
    total_order_dollar = 'N/A'
    ability_container = soup.find('div', class_='ability-container')
    if ability_container: 
        order_info = {li.find('div', class_='title').text: li.find('strong').text for li in ability_container.find_all('li')}
        for key, value in order_info.items():
            if 'orders' in key:
                total_order_number = key.split()[0]
                total_order_dollar = re.sub(r'[^\d+]', '', value)
    
    #############################         Main categories           ###############################
    main_categories = ""
    soup_company_info = soup.find('div', class_='company-info')
    if soup_company_info:
        spans = soup_company_info.find_all('span')
        for span in spans:
            if 'Main categories' in span.text:
                main_categories = span.text.split(":")[1].rstrip(".").replace(" / ", ", ").strip()
                break
    
    #############################   MOQ and corresponding products  ###############################
    # imgs
    images = [img['src'] for img in soup.select('.next-slick-slide .product-image img') if 'src' in img.attrs][:4]
    images += ['N/A'] * (4 - len(images))

    # Orders so far
    orders_so_far_elements = soup.select('.next-slick-slide .sold-text')
    if [order.text.strip() if order else 'N/A' for order in orders_so_far_elements][:4]:
        orders_so_far = [order.text.strip() if order and order.text.strip() != '' else 'N/A' for order in orders_so_far_elements][:4]
        orders_so_far += ['N/A'] * (4 - len(orders_so_far))
    else:
        orders_so_far = ['N/A'] * 4

    # MOQ
    min_orders_elements = soup.select('.next-slick-slide .moq')
    if [order.text.strip() if order else 'N/A' for order in min_orders_elements][:4]:
        min_orders = [order.text.strip() if order and order.text.strip() != '' else 'N/A' for order in min_orders_elements][:4]
        min_orders += ['N/A'] * (4 - len(min_orders))
    else:
        min_orders = ['N/A'] * 4

    #############################          writing data             ################################
    data = {
        'Name':                         name,
        'URL':                          url,
        'Location':                     soup.find('div', class_='company-info').find('span').text.strip() if soup.find('div', class_='company-info') else 'N/A',
        'Score':                        soup.find('span', class_='score-text').text.strip() if soup.find('span', class_='score-text') else 'N/A',
        'Reviews':                      soup.find('a', class_='reviews-num').text.strip() if soup.find('a', class_='reviews-num') else 'N/A',
        "Main Categories":              main_categories,
        'Average Response Time':        soup.find('div', string='average response time').find_next('strong').text if soup.find('div', string='average response time') else 'N/A',
        'On time Delivery Rate':        soup.find('div', string='on-time delivery rate').find_next('strong').text if soup.find('div', string='on-time delivery rate') else 'N/A',
        "Total Orders so far":          total_order_number, 
        'Total Order Amount':           total_order_dollar,
        ##########################################    what is working on    ########################################## 
        'Services':                     services,
        'Quality Control':              quality_control,
        'Certificates':                 certificates,
        'Floor Space (㎡)':             soup.find(string='Floor space(㎡)').find_next('strong').text.strip() if soup.find(string='Floor space(㎡)') else 'N/A',
        'Annual Export Revenue (USD)':  soup.find(string='Annual export revenue (USD)').find_next('strong').text.strip() if soup.find(string='Annual export revenue (USD)') else 'N/A',
        'Production Lines':             soup.find(string='Production lines').find_next('strong').text.strip() if soup.find(string='Production lines') else 'N/A',
        'Total Annual Output (Units)':  soup.find(string='Total annual output (units)').find_next('strong').text.strip() if soup.find(string='Total annual output (units)') else 'N/A',
        'Production Machines':          soup.find(string='Production machines').find_next('strong').text.strip() if soup.find(string='Production machines') else 'N/A',
        'Quality Control on All Lines': soup.find(string='Quality control conducted on all production lines').find_next('strong').text.strip() if soup.find(string='Quality control conducted on all production lines') else 'N/A',
        'QA/QC Inspectors':             soup.find(string='QA/QC inspectors').find_next('strong').text.strip() if soup.find(string='QA/QC inspectors') else 'N/A',
        'Main Markets':                 soup.find(string='Main markets').find_next('strong').text.strip() if soup.find(string='Main markets') and soup.find(string='Main markets').find_next('strong') else 'N/A',
        'Supply Chain Partners':        soup.find(string='Supply chain partners').find_next('strong').text.strip() if soup.find(string='Supply chain partners') else 'N/A',
        'Main Client Types':            soup.find(string='Main client types').find_next('strong').text.strip() if soup.find(string='Main client types') and soup.find(string='Main client types').find_next('strong') else 'N/A',
        'Customization Options':        soup.find(string='Customization options').find_next('strong').text.strip() if soup.find(string='Customization options') else 'N/A',
        'New Products Launched Last Year': soup.find(string='New products launched in last year').find_next('strong').text.strip() if soup.find(string='New products launched in last year') else 'N/A',
        'R&D Engineers':                soup.find(string='R&D engineers').find_next('strong').text.strip() if soup.find(string='R&D engineers') else 'N/A',
        'Main Product 1':       "https:" + images[0],
        'Main Product 1 MOQ':   min_orders[0],
        'Product 1 Orders So far': orders_so_far[0],
        'Main Product 2':       "https:" + images[1],
        'Main Product 2 MOQ':   min_orders[1],
        'Product 2 Orders So far': orders_so_far[1],
        'Main Product 3':       "https:" + images[2],
        'Main Product 3 MOQ':   min_orders[2],
        'Product 3 Orders So far': orders_so_far[2],
        'Main Product 4':       "https:" + images[3],
        'Main Product 4 MOQ':   min_orders[3],
        'Product 4 Orders So far': orders_so_far[3],
    }

    detailed_manufacturers_data.append(data)

    ####################################  MONITORING 2  ####################################
    print("relevant parameters: ")
    print("Services: ", data['Services'])
    print("Quality Control ", data['Quality Control'])
    print("Certificates: ", data['Certificates'])
    print("\n")

driver.quit()

# Write to CSV
with open('manufacturers_data_06_10.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = list(detailed_manufacturers_data[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in detailed_manufacturers_data:
        # print("writing")
        writer.writerow(data)
