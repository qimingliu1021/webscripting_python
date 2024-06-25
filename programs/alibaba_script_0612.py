from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import datetime
import time 
import os
import csv
import re

# Setup Selenium WebDriver
driver = webdriver.Edge()

directory = '../apparel_manufactures'
manufacturers_name_url = []
now = datetime.datetime.now()

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

all_service = ['minor customization', 'design-based customization', 'sample-based customization', 'full customization', 'agile supply chain', 'international warehouses', 'project solutions', 'project design capability', 'centralized procurement available', 'on-site installation', 'on-site technical support', 'one-stop procurement', '3d design capabilities', 'overseas partner factory']
all_qc = ['raw-material traceability identification', 'finished product inspection', 'qa/qc inspectors', 'on-site material inspection', 'quality traceability', 'warranty available', 'testing instruments']
html_directory = "htmls"
log_directory = "logs"

def categorize_capabilities(soup):
    services = []
    quality_control = []
    certificates = []

    list_items = soup.select('.list-item:not(.no-select-text)')
    for item in list_items:

        text = item.get_text(strip=True).lower()
        found_service = False
        for keyword in all_service:
            if keyword in text:
                services.append(keyword)
                found_service = True
                break  

        if not found_service:
            found_qc = False
            for keyword in all_qc:
                if keyword in text:
                    quality_control.append(keyword)
                    found_qc = True
                    break  # Stop checking after the first match to avoid duplicates

            if not found_qc:
                certificates.append(text)
    
    return services, quality_control, certificates


def must_get_page_source(url): 
    get_the_source = False
    while not get_the_source: 
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        if soup.find('div', class_='module-verifiedProfile'): 
            get_the_source = True
        # when there's 404 page
        if soup.find('div', 'info-404img'): 
            with open(f"PROBLEM_{now}") as file: 
                file.write(f"{url}\n \n")
            services, quality_control, certificates = ["problem"], ["problem"], ["problem"]
            break
        # For different html layout
        if soup.find('div', class_='icbu-mod-wrapper no-title icbu-pc-cpCompanyOverview false v2'): 
            services, quality_control, certificates = ["problem"], ["problem"], ["problem"]
            #
            with open(f"{log_directory}/{log_directory}/DIFFERENT_{now}", "a") as file: 
                file.write(f"{url}\n \n")
            break
        time.sleep(5)
    # Get the clicked page
    all_tags_elements = driver.find_elements(By.CLASS_NAME, "all-tags")
    all_tags_elements[0].click()
    time.sleep(3)
    soup_opened = BeautifulSoup(driver.page_source, 'html.parser')
    with open(f"{html_directory}/{count}_click.html", "w") as file:
        file.write(soup_opened.prettify())
    
    services, quality_control, certificates = categorize_capabilities(soup_opened)

    with open(f"{html_directory}/{count}.html", "w") as file: 
                file.write(soup.prettify())
    
    return soup, services, quality_control, certificates


# Visit each manufacturer's page
for name, url in manufacturers_name_url:

    ##############################           MONITORING 1            ##############################
    print(f"\nmanufacture {count}: \n")
    print(f"{name} please visit - {url}")

    count += 1
    # a switch - on/off to control the # number of manufactures
    # if count == 10: 
    #     break;

    ##############################      Accessing the website        ##############################
    
    soup = must_get_page_source(url)

    all_tags_elements = driver.find_elements(By.CLASS_NAME, "all-tags")
    if all_tags_elements: 
        
    else: 
        different_manufactures[name] = url
        services, quality_control, certificates = 'problem', 'problem', 'problem'
    
    different_manufactures = {}

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
    }

    detailed_manufacturers_data.append(data)

    ####################################  MONITORING 2  ####################################
    with open(f"{log_directory}/log_{now}.txt", "a") as file: 
        file.write(f"\nManufacture {count}......")
        for key, value in data.items(): 
            file.write(f"{key}: {value}\n")
        file.write("\n \n")
    print("relevant parameters: ")
    print("Services: ", data['Services'])
    print("Quality Control ", data['Quality Control'])
    print("Certificates: ", data['Certificates'])
    print("\n")

driver.quit()

# Write to CSV
with open(f'manufacturers_data_{now}.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = list(detailed_manufacturers_data[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in detailed_manufacturers_data:
        data['Services'] = ', '.join(data['Services'])
        data['Quality Control'] = ', '.join(data['Quality Control'])
        data['Certificates'] = ', '.join(data['Certificates'])
        writer.writerow(data)

