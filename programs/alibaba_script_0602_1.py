from selenium import webdriver
from bs4 import BeautifulSoup
import os
import csv

# Setup Selenium WebDriver
driver = webdriver.Chrome()  

directory = '../apparel_manufactures'
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

detailed_manufacturers_data = []

count = 0

# Visit each manufacturer's page
for name, url in manufacturers_data:
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    images = [img['src'] for img in soup.select('.next-slick-slide .product-image img') if 'src' in img.attrs][:4]
    images += ['N/A'] * (4 - len(images))

    data = {
        'Name':                         name,
        'URL':                          url,
        'Location':                     soup.find('div', class_='company-info').find('span').text.strip() if soup.find('div', class_='company-info') else 'N/A',
        'Score':                        soup.find('span', class_='score-text').text.strip() if soup.find('span', class_='score-text') else 'N/A',
        'Reviews':                      soup.find('a', class_='reviews-num').text.strip() if soup.find('a', class_='reviews-num') else 'N/A',
        'Average Response Time':        soup.find('div', text='average response time').find_next('strong').text if soup.find('div', text='average response time') else 'N/A',
        'On time Delivery Rate':        soup.find('div', text='on-time delivery rate').find_next('strong').text if soup.find('div', text='on-time delivery rate') else 'N/A',
        'Verified capabilities':        ', '.join([tag.text.strip() for tag in soup.find_all('div', class_='tag')]) if soup.find_all('div', class_='tag') else 'N/A',
        'Floor Space (㎡)':             soup.find(string='Floor space(㎡)').find_next('strong').text.strip() if soup.find(string='Floor space(㎡)') else 'N/A',
        'Annual Export Revenue (USD)':  soup.find(string='Annual export revenue (USD)').find_next('strong').text.strip() if soup.find(string='Annual export revenue (USD)') else 'N/A',
        'Production Lines':             soup.find(string='Production lines').find_next('strong').text.strip() if soup.find(string='Production lines') else 'N/A',
        'Total Annual Output (Units)':  soup.find(string='Total annual output (units)').find_next('strong').text.strip() if soup.find(string='Total annual output (units)') else 'N/A',
        'Production Machines':          soup.find(string='Production machines').find_next('strong').text.strip() if soup.find(string='Production machines') else 'N/A',
        'Quality Control on All Lines': soup.find(string='Quality control conducted on all production lines').find_next('strong').text.strip() if soup.find(string='Quality control conducted on all production lines') else 'N/A',
        'QA/QC Inspectors':             soup.find(string='QA/QC inspectors').find_next('strong').text.strip() if soup.find(string='QA/QC inspectors') else 'N/A',
        'Main Markets':                 soup.find(string='Main markets').find_next('strong').text.strip() if soup.find(string='Main markets') and soup.find(string='Main markets').find_next('strong') else 'N/A',
        'Supply Chain Partners':        soup.find(string='Supply chain partners').find_next('strong').text.strip() if soup.find(string='Supply chain partners') else 'N/A',
        'Main Client Types':            soup.find(string='Main client types').find_next('strong').text.strip() if soup.find(string='Main client types') else 'N/A',
        'Customization Options':        soup.find(string='Customization options').find_next('strong').text.strip() if soup.find(string='Customization options') else 'N/A',
        'New Products Launched Last Year': soup.find(string='New products launched in last year').find_next('strong').text.strip() if soup.find(string='New products launched in last year') else 'N/A',
        'R&D Engineers':                soup.find(string='R&D engineers').find_next('strong').text.strip() if soup.find(string='R&D engineers') else 'N/A',
        'Main Product Picture 1':       "https:" + images[0],
        'Main Product Picture 2':       "https:" + images[1],
        'Main Product Picture 3':       "https:" + images[2],
        'Main Product Picture 4':       "https:" + images[3],
    }

    ####################################  MONITORING  ####################################
    count += 1
    print(f"\nThis is {count} manufacture")
    print(f"Here is its information: {name}, {url}\n")

    detailed_manufacturers_data.append(data)

driver.quit()

# Write to CSV
with open('manufacturers_data_5pm.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = list(detailed_manufacturers_data[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in detailed_manufacturers_data:
        writer.writerow(data)

print("Data extraction complete and saved to CSV.")
