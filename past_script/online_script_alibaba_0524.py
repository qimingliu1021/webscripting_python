import os
import requests
from bs4 import BeautifulSoup

# Directory containing the HTML files
directory = '../manufacturers'

# List to store all manufacturer names and links

####################   Getting all manufactures   ####################

manufacturers_data = []

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
              manufacturers_data.append((manufacturer_name, manufacturer_link))

#################  Visiting all manufacture links to script data   ##################

detailed_manufacturers_data = {}

total_count = 0
count_module_verifiedProfile = 0

for a_manufacture in manufacturers_data:
  total_count += 1
  # if total_count>3: 
  #   break
  print(f"Getting manufacture{total_count}'s data \n")
  try:
    # with open(f"manufacture_{i}.html", 'w') as file: 
    #   its_html = requests.get(a_manufacture[1])
    #   file.write(its_html.text)
    its_html = requests.get(a_manufacture[1])

    if its_html.status_code == 200:
      # print(f"Successfully received HTML for manufacture: {a_manufacture[0]}")
      soup = BeautifulSoup(its_html.content, 'html.parser')

      ###### basical info in class: "ability-container" ######
      ability_container = soup.find('div', class_='ability-container')
      if ability_container:
        # print("########## in ability container ##########")
        # print("type of module_verifiedProfile: " + str(type(ability_container)))
        score = ability_container.find('span', class_='score-text').text.strip() if ability_container.find('span', class_='score-text') else 'N/A'
        reviews = ability_container.find('a', class_='reviews-num').text.strip() if ability_container.find('a', class_='reviews-num') else 'N/A'
        
        abilities = {li.find('div', class_='title').text: li.find('strong').text for li in ability_container.find_all('li')}
        average_response_time = abilities.get('average response time', 'N/A')
        delivery_rate = abilities.get('on-time delivery rate', 'N/A')
        orders_info = abilities.get('{0} orders', 'N/A')
        tags = [tag.find('span', class_='tag-text').text for tag in ability_container.find_all('div', class_='tag')] if ability_container.find_all('div', class_='tag') else []

      ###### advanced info in class: "module-verifiedProfile" ######
      module_verifiedProfile = soup.find('div', class_='module-verifiedProfile')
      if module_verifiedProfile:
        count_module_verifiedProfile += 1
        floor_space = module_verifiedProfile.find(string='Floor space(㎡)').find_next('strong').text.strip() if module_verifiedProfile.find(string='Floor space(㎡)') else 'N/A'
        annual_export_value = module_verifiedProfile.find(string='Annual export revenue (USD)').find_next('strong').text.strip() if module_verifiedProfile.find(string='Annual export revenue (USD)') else 'N/A'
        production_lines = module_verifiedProfile.find(string='Production lines').find_next('strong').text.strip() if module_verifiedProfile.find(string='Production lines') else 'N/A'
        total_annual_output_units = module_verifiedProfile.find(string='Total annual output (units)').find_next('strong').text.strip() if module_verifiedProfile.find(string='Total annual output (units)') else 'N/A'
        production_machines = module_verifiedProfile.find(string='Production machines').find_next('strong').text.strip() if module_verifiedProfile.find(string='Production machines') else 'N/A'
        QC_on_all_lines = module_verifiedProfile.find(string='Quality control conducted on all production lines').find_next('strong').text.strip() if module_verifiedProfile.find(string='Quality control conducted on all production lines') else 'N/A'
        QAQC_inspectors = module_verifiedProfile.find(string='QA/QC inspectors').find_next('strong').text.strip() if module_verifiedProfile.find(string='QA/QC inspectors') else 'N/A'
        main_markets = module_verifiedProfile.find(string='Main markets').find_next('strong').text.strip() if module_verifiedProfile.find(string='Main markets') else 'N/A'
        supply_chain_partners = module_verifiedProfile.find(string='Supply chain partners').find_next('strong').text.strip() if module_verifiedProfile.find(string='Supply chain partners') else 'N/A'
        main_client_types = module_verifiedProfile.find(string='Main client types').find_next('strong').text.strip() if module_verifiedProfile.find(string='Main client types') else 'N/A'
        customization_options = module_verifiedProfile.find(string='Customization options').find_next('strong').text.strip() if module_verifiedProfile.find(string='Customization options') else 'N/A'
        new_product_launched_last_year = module_verifiedProfile.find(string='New products launched in last year').find_next('strong').text.strip() if module_verifiedProfile.find(string='New products launched in last year') else 'N/A'
        R_D_engineers = module_verifiedProfile.find(string='R&D engineers').find_next('strong').text.strip() if module_verifiedProfile.find(string='R&D engineers') else 'N/A'

        detailed_manufacturers_data[a_manufacture[0]] = {
          'score': score,
          'Reviews': reviews,
          'Average Response Time': average_response_time,
          'On time Delivery Rate': delivery_rate,
          'Order Info': orders_info,
          'Verified capabilities': tags,
          'Floor Space (㎡)': floor_space,
          'Annual Export Revenue (USD)': annual_export_value,
          'Production Lines': production_lines,
          'Total Annual Output (Units)': total_annual_output_units,
          'Production Machines': production_machines,
          'Quality Control on All Lines': QC_on_all_lines,
          'QA/QC Inspectors': QAQC_inspectors,
          'Main Markets': main_markets,
          'Supply Chain Partners': supply_chain_partners,
          'Main Client Types': main_client_types,
          'Customization Options': customization_options,
          'New Products Launched Last Year': new_product_launched_last_year,
          'R&D Engineers': R_D_engineers
        }

  except requests.exceptions.RequestException as e:
    print(f"An error occurred when trying to retrieve {a_manufacture[0]}: {str(e)}")

print(f"{count_module_verifiedProfile} manufactures have module_verifiedProfile Class")

######################## store manufactures from dictionary to csv file ##########################

import csv

headers = [
    'Manufacturer Name', 'Score', 'Reviews', 'Average Response Time', 'On-time Delivery Rate', 
    'Order Info', 'Verified Capabilities', 'Floor Space (㎡)', 'Annual Export Revenue (USD)', 
    'Production Lines', 'Total Annual Output (Units)', 'Production Machines', 
    'Quality Control on All Lines', 'QA/QC Inspectors', 'Main Markets', 
    'Supply Chain Partners', 'Main Client Types', 'Customization Options', 
    'New Products Launched Last Year', 'R&D Engineers'
]

with open("manufacture_info_0531.csv", 'w', newline='', encoding='utf-8') as csvfile: 

  print("writing to csv files ... ")
  writer = csv.DictWriter(csvfile, fieldnames=headers)

  writer.writeheader()

  for name, details in detailed_manufacturers_data.items():
    print(f"writing {name}...")
    row = {
            'Manufacturer Name': name,
            'Score': details['score'],
            'Reviews': details['Reviews'],
            'Average Response Time': details['Average Response Time'],
            'On-time Delivery Rate': details['On time Delivery Rate'],
            'Order Info': details['Order Info'],
            'Verified Capabilities': details['Verified capabilities'],
            'Floor Space (㎡)': details['Floor Space (㎡)'],
            'Annual Export Revenue (USD)': details['Annual Export Revenue (USD)'],
            'Production Lines': details['Production Lines'],
            'Total Annual Output (Units)': details['Total Annual Output (Units)'],
            'Production Machines': details['Production Machines'],
            'Quality Control on All Lines': details['Quality Control on All Lines'],
            'QA/QC Inspectors': details['QA/QC Inspectors'],
            'Main Markets': details['Main Markets'],
            'Supply Chain Partners': details['Supply Chain Partners'],
            'Main Client Types': details['Main Client Types'],
            'Customization Options': details['Customization Options'],
            'New Products Launched Last Year': details['New Products Launched Last Year'],
            'R&D Engineers': details['R&D Engineers']
        }
        
    writer.writerow(row)
