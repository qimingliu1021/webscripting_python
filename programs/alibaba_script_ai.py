from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
import time 
import os
import csv
import re

# Setup Selenium WebDriver
driver = webdriver.Chrome()  

file_path = "data_to_try.csv"

data_dict = {}

count = 1

with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['Name']  
        url = row['URL']    
        data_dict[name] = url

detailed_manufacturers_data = {}


GPT_4 = 'gpt-4'
OPENAI_KEY = "sk-proj-pPP9rymFehKkk2VNnEBYT3BlbkFJ8FIbmQ7JTSUAsLYZakBc"
llm = ChatOpenAI(temperature=0, model=GPT_4, openai_api_key=OPENAI_KEY)

def parsing_html(soup): 
    for script in soup(["script", "style"]): # Remove all javascript and stylesheet code
            script.extract()
    text = soup.get_text()
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines()) 
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) 
    data = '\n'.join(chunk for chunk in chunks if chunk) # Drop blank lines
    return data

# Visit each manufacturer's page one by one
for name, url in data_dict.items():

    ##############################           MONITORING 1            ##############################
    print(f"\nmanufacture {count}: \n")
    print(f"{name} please visit - {url}")

    count += 1
    # a switch - on/off to control the # number of manufactures
    # if count == 3: 
    #     break;

    ##############################      Accessing the website       ##############################
    driver.get(url)
    driver.implicitly_wait(3) # seconds
    soup =  BeautifulSoup(driver.page_source, 'html.parser')
    soup = parsing_html(soup)

    different_manufactures = {}

    # click to get "Verified capabilities"
    all_tags_elements = driver.find_elements(By.CLASS_NAME, "all-tags")
    if all_tags_elements: 
        all_tags_elements[0].click()
        time.sleep(3)
        soup_opened = BeautifulSoup(driver.page_source, 'html.parser')
        # soup_opened = parsing_html(soup_opened)
        schema = {
            "properties": {
            "services": {"type": "string"},
            "quality control": {"type": "string"}, 
            "certificates": {"type": "string"}, 
            }
        }
        # services, quality_control, certificates = categorize_capabilities(soup_opened)
        json_result = create_extraction_chain(schema, llm).invoke(soup_opened)
        print(json_result['text'])
    else: 
        print(f"problem getting verified manufacture, name is {name}, url is: {url}")
        different_manufactures[name] = url
        services, quality_control, certificates = 'problem', 'problem', 'problem'


    # #############################   order numbers and total amounts   #############################
    # total_order_number = 'N/A'
    # total_order_dollar = 'N/A'
    # ability_container = soup.find('div', class_='ability-container')
    # if ability_container: 
    #     order_info = {li.find('div', class_='title').text: li.find('strong').text for li in ability_container.find_all('li')}
    #     for key, value in order_info.items():
    #         if 'orders' in key:
    #             total_order_number = key.split()[0]
    #             total_order_dollar = re.sub(r'[^\d+]', '', value)
    
    # #############################         Main categories           ###############################
    # main_categories = ""
    # soup_company_info = soup.find('div', class_='company-info')
    # if soup_company_info:
    #     spans = soup_company_info.find_all('span')
    #     for span in spans:
    #         if 'Main categories' in span.text:
    #             main_categories = span.text.split(":")[1].rstrip(".").replace(" / ", ", ").strip()
    #             break

    # #############################          writing data             ################################
    # data = {
    #     'Name':                         name,
    #     'URL':                          url,
    #     'Location':                     soup.find('div', class_='company-info').find('span').text.strip() if soup.find('div', class_='company-info') else 'N/A',
    #     'Score':                        soup.find('span', class_='score-text').text.strip() if soup.find('span', class_='score-text') else 'N/A',
    #     'Reviews':                      soup.find('a', class_='reviews-num').text.strip() if soup.find('a', class_='reviews-num') else 'N/A',
    #     "Main Categories":              main_categories,
    #     'Average Response Time':        soup.find('div', string='average response time').find_next('strong').text if soup.find('div', string='average response time') else 'N/A',
    #     'On time Delivery Rate':        soup.find('div', string='on-time delivery rate').find_next('strong').text if soup.find('div', string='on-time delivery rate') else 'N/A',
    #     "Total Orders so far":          total_order_number, 
    #     'Total Order Amount':           total_order_dollar,
    #     ##########################################    what is working on    ########################################## 
    #     'Services':                     services,
    #     'Quality Control':              quality_control,
    #     'Certificates':                 certificates,
    #     'Floor Space (㎡)':             soup.find(string='Floor space(㎡)').find_next('strong').text.strip() if soup.find(string='Floor space(㎡)') else 'N/A',
    #     'Annual Export Revenue (USD)':  soup.find(string='Annual export revenue (USD)').find_next('strong').text.strip() if soup.find(string='Annual export revenue (USD)') else 'N/A',
    #     'Production Lines':             soup.find(string='Production lines').find_next('strong').text.strip() if soup.find(string='Production lines') else 'N/A',
    #     'Total Annual Output (Units)':  soup.find(string='Total annual output (units)').find_next('strong').text.strip() if soup.find(string='Total annual output (units)') else 'N/A',
    #     'Production Machines':          soup.find(string='Production machines').find_next('strong').text.strip() if soup.find(string='Production machines') else 'N/A',
    #     'Quality Control on All Lines': soup.find(string='Quality control conducted on all production lines').find_next('strong').text.strip() if soup.find(string='Quality control conducted on all production lines') else 'N/A',
    #     'QA/QC Inspectors':             soup.find(string='QA/QC inspectors').find_next('strong').text.strip() if soup.find(string='QA/QC inspectors') else 'N/A',
    #     'Main Markets':                 soup.find(string='Main markets').find_next('strong').text.strip() if soup.find(string='Main markets') and soup.find(string='Main markets').find_next('strong') else 'N/A',
    #     'Supply Chain Partners':        soup.find(string='Supply chain partners').find_next('strong').text.strip() if soup.find(string='Supply chain partners') else 'N/A',
    #     'Main Client Types':            soup.find(string='Main client types').find_next('strong').text.strip() if soup.find(string='Main client types') and soup.find(string='Main client types').find_next('strong') else 'N/A',
    #     'Customization Options':        soup.find(string='Customization options').find_next('strong').text.strip() if soup.find(string='Customization options') else 'N/A',
    #     'New Products Launched Last Year': soup.find(string='New products launched in last year').find_next('strong').text.strip() if soup.find(string='New products launched in last year') else 'N/A',
    #     'R&D Engineers':                soup.find(string='R&D engineers').find_next('strong').text.strip() if soup.find(string='R&D engineers') else 'N/A',
    # }

    # detailed_manufacturers_data.append(data)

    # ####################################  MONITORING 2  ####################################
    # print("relevant parameters: ")
    # print("Services: ", data['Services'])
    # print("Quality Control ", data['Quality Control'])
    # print("Certificates: ", data['Certificates'])
    print("\n")

driver.quit()

print("problem manufactures: ", different_manufactures)

# # Write to CSV
# with open('manufacturers_data_06_10.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     fieldnames = list(detailed_manufacturers_data[0].keys())
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     for data in detailed_manufacturers_data:
#         # print("writing")
#         writer.writerow(data)
