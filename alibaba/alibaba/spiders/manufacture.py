import scrapy
import re
import os
import time
import pandas as pd
import datetime
from lxml import etree
from alibaba.items import ManufactureItem
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

# Set logging level to WARNING
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)


class ManufactureSpider(scrapy.Spider):
    name = "manufacture"
    allowed_domains = ["alibaba.com"]
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_count = 1
    csv_store = "data/business_services"
    log_store = "data/LOGS"


    def __init__(self):
        # Initialize Selenium WebDriver (Chrome)
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)


    def start_requests(self): 

        csv_path = os.path.join(self.csv_store, "business_services.csv")
        df = pd.read_csv(csv_path)
        for index, row in df.iterrows(): 
            self.file_count += 1
            time.sleep(3)
            # if self.file_count < 3: 
            link = row['link']
            print(f"getting {row['name']}, {link}")
            yield scrapy.Request(link, callback=self.parse_with_selenium)


    def parse_with_selenium(self, response):

        print("\n-------------- In parse_with_selenium() ... -------------- \n")

        if 'proxy' in response.meta:
            proxy = response.meta['proxy']
            print(f"Scrapy request used proxy: {proxy}")
        
        self.driver.get(response.url)
        
        # Optionally wait for certain elements to load
        time.sleep(1)  # Add explicit waits here if needed
        
        # Get the full page source after JavaScript execution
        rendered_html = self.driver.page_source

        # Save the rendered HTML to file
        cur_log_path = os.path.join(self.log_store, f"{self.file_count}_{self.now}.html")
        with open(cur_log_path, "w", encoding='utf-8') as f: 
            print(f"Get the response of file {self.file_count}, now writing to file")
            f.write(rendered_html)
        
        # Parse the rendered HTML with Scrapy's response object
        response = scrapy.http.TextResponse(url=response.url, body=rendered_html, encoding='utf-8')

        name = response.xpath("//div[@class='shop-sign']//h1/text()").get(default=-1)
        location = response.xpath("//div[@class='company-info']/span/text()").get(default=-1)
        score = response.xpath("//span[@class='score-text']/text()").get(default=-1)
        reviews = response.xpath(".//div[@class='rating-container']/a/text()").get(default=-1)
        # reviews_number = int(re.search(r'\d+', reviews).group()) if reviews != "-1" else -1

        average_response_time = response.xpath("//ul[@class='supplier-ability']/li[div[contains(text(), 'average response time')]]/strong/text()").get(default="-1")
        on_time_delivery_rate = response.xpath("//ul[@class='supplier-ability']/li[div[contains(text(), 'on-time delivery rate')]]/strong/text()").get(default="-1")
        # on_time_delivery_decimal = float(re.search(r'[\d.]+', on_time_delivery_rate).group()) / 100 if on_time_delivery_rate != "-1" else -1
        total_orders_so_far = response.xpath("//ul[@class='supplier-ability']/li[div[contains(text(), 'orders')]]/div[@class='title']/text()").get(default="-1")
        # total_orders_number = int(re.search(r'\d+', total_orders_so_far).group()) if total_orders_so_far != "-1" else -1
        total_order_amount = response.xpath("//ul[@class='supplier-ability']/li[div[contains(text(), 'orders')]]/strong[contains(text(), 'US')]/text()").get(default="-1")
        # total_order_amount_number = int(re.sub(r'[^\d]', '', total_order_amount)) if total_order_amount != "-1" else -1

        # Overview
        floor_space = response.xpath("//div[@class='profile-list authIndustryExperience']/div[@class='profile-detail'][contains(text(), 'Floor')]/strong/text()").get(default="-1")
        annual_export_revenue = response.xpath("//div[@class='profile-list authIndustryExperience']/div[@class='profile-detail'][contains(text(), 'Annual')]/strong/text()").get(default="-1")

        # Production capabilities
        production_lines = response.xpath("//div[@class='profile-list authProductionCapacity']/div[@class='profile-detail'][contains(text(), 'lines')]/strong/text()").get(default="-1")
        production_machines = response.xpath("//div[@class='profile-list authProductionCapacity']/div[@class='profile-detail'][contains(text(), 'machines')]/strong/text()").get(default="-1")
        total_annual_output = response.xpath("//div[@class='profile-list authProductionCapacity']/div[@class='profile-detail'][contains(text(), 'output')]/strong/text()").get(default="-1")

        # Quality control
        quality_control_on_all_lines = response.xpath("//div[@class='profile-list authQualityControlCapacity']/div[@class='profile-detail'][contains(text(), 'control')]/strong/text()").get(default="-1")
        qa_qc_inspectors = response.xpath("//div[@class='profile-list authQualityControlCapacity']/div[@class='profile-detail'][contains(text(), 'inspectors')]/strong/text()").get(default="-1")
        
        # Trade background
        main_markets = response.xpath("//div[@class='profile-list authMarketCooperation']/div[@class='profile-detail'][contains(text(), 'markets')]/strong/text()").get(default="-1")
        main_client_types = response.xpath("//div[@class='profile-list authMarketCooperation']/div[@class='profile-detail'][contains(text(), 'client')]/strong/text()").get(default="-1")

        # R&D capabilities
        customization_options = response.xpath("//div[@class='profile-list authRdCapacity']/div[@class='profile-detail'][contains(text(), 'options')]/strong/text()").get(default="-1")
        new_products_launched_last_year = response.xpath("//div[@class='profile-list authRdCapacity']/div[@class='profile-detail'][contains(text(), 'launched')]/strong/text()").get(default="-1")
        r_d_engineers = response.xpath("//div[@class='profile-list authRdCapacity']/div[@class='profile-detail'][contains(text(), 'engineers')]/strong/text()").get(default="-1")

        # Obtain product page link


        # execute js again for "See all verified capabilities (12)"
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "all-tags"))
        )
        view_capabilities_button = self.driver.find_element(By.CLASS_NAME, "all-tags")
        view_capabilities_button.click()
        try: 
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "tags-dialog"))
            )
        except TimeoutException: 
            try: 
                captcha = self.driver.find_element(By.XPATH, "//*[@id='baxia-punish']/div[2]/div/div[1]/div[2]/div")
                if captcha: 
                    print("!!!!!!!!!!!!!!!!!!!!!!!!! CAPTCHA VERIFICATION !!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("current PROXY: ")
                    print("current LOCATION: trying to visit 'all-tags'")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                else: 
                    print("Other situations for timeout. Not because captcha")
            except Exception as e: 
                print("Other time out issue")


        dialog_content = self.driver.find_element(By.CLASS_NAME, "tags-dialog").get_attribute('innerHTML')
        dialog_tree = etree.HTML(dialog_content)
        services = dialog_tree.xpath("//div[contains(@class, 'list') and contains(.//span, 'Service')]//div[contains(@class, 'list-item') and not(contains(@class, 'no-select-text'))]//span[@class='hover-span']/text()")
        quality_controls = dialog_tree.xpath("//div[contains(@class, 'list') and contains(.//span, 'Quality control')]//div[contains(@class, 'list-item') and not(contains(@class, 'no-select-text'))]//span[@class='hover-span']/text()")
        certifications = dialog_tree.xpath("//div[contains(@class, 'list') and contains(.//span, 'Certifications')]//div[contains(@class, 'list-item') and not(contains(@class, 'no-select-text'))]//span[@class='hover-span']/text()")

        # If any of these are empty, return -1 as a fallback
        services = ", ".join(services) if services else "-1"
        quality_controls = ", ".join(quality_controls) if quality_controls else "-1"
        certifications = ", ".join(certifications) if certifications else "-1"

        print("Services:", services)
        print("Quality Controls:", quality_controls)
        print("Certifications:", certifications)

        item = ManufactureItem(
            name=name, 
            location=location,
            score=score,
            reviews=reviews,
            average_response_time=average_response_time,
            on_time_delivery_rate=on_time_delivery_rate,
            total_orders_so_far=total_orders_so_far,
            total_order_amount=total_order_amount,
            floor_space=floor_space,
            annual_export_revenue=annual_export_revenue, 
            production_lines=production_lines,
            production_machines=production_machines, 
            total_annual_output=total_annual_output, 
            quality_control_on_all_lines=quality_control_on_all_lines, 
            qa_qc_inspectors=qa_qc_inspectors, 
            main_markets=main_markets,  
            main_client_types=main_client_types, 
            customization_options=customization_options, 
            new_products_launched_last_year=new_products_launched_last_year, 
            r_d_engineers=r_d_engineers,
            services = services, 
            quality_controls = quality_controls, 
            certifications = certifications
        )

        print("\n-----------------------------------------\n")
        print(f"Current manufacturer name: {item['name']}, all its data are below: \n")
        for key in item: 
            print(f"{key}: {item.get(key)}")
        print("\n-----------------------------------------\n")
        print("\n-------------- yielding item -------------- \n")
        yield item
        print("\n-------------- END OF parse_with_selenium() ... -------------- \n")


    def closed(self, reason):
        # Close the browser when the spider finishes
        self.driver.quit()



    def parse(self, response):

        cur_log_path = os.path.join(self.log_store, f"{self.file_count}_{self.now}.html")        
        with open(cur_log_path, "w", encoding='utf-8') as f: 
            print(f"Get the response of file {self.file_count}, now writing to file")
            f.write(response.text)

        name = response.xpath("//div[@class='shop-sign']//h1/text()").get(default=-1)
        
        location = response.xpath("//div[@class='company-info']/span/text()").get(default=-1)
        score = response.xpath("//span[@class='score-text']/text()").get(default=-1)
        reviews = response.xpath(".//div[@class='rating-container']/a/text()").get(default=-1)

        average_response_time = response.xpath("//ul[@class='supplier-ability']/li/strong[contains(text(), 'h')]").get(default="-1")
        on_time_delivery_rate = response.xpath("//ul[@class='supplier-ability']/li/strong[contains(text(), '%')]").get(default="-1")
        total_orders_so_far = response.xpath("//div[@class='title'][contains(text(), 'orders')]/text()").get(default="-1")
        total_orders_so_far = response.xpath("//div[@class='title'][contains(text(), 'orders')]/text()").get(default="-1")
        total_order_amount = response.xpath("//ul[@class='supplier-ability']/li/strong[contains(text(), 'US')]").get(default="-1")

        # Overview
        floor_space = response.xpath("//div[@class='profile-list authIndustryExperience']/div[@class='profile-detail'][contains(text(), 'Floor')]/strong/text()").get(default="-1")
        annual_export_revenue = response.xpath("//div[@class='profile-list authIndustryExperience']/div[@class='profile-detail'][contains(text(), 'Annual')]/strong/text()").get(default="-1")

        # Production capabilities
        production_lines = response.xpath("//div[@class='profile-list authProductionCapacity']/div[@class='profile-detail'][contains(text(), 'lines')]/strong/text()").get(default="-1")
        production_machines = response.xpath("//div[@class='profile-list authProductionCapacity']/div[@class='profile-detail'][contains(text(), 'machines')]/strong/text()").get(default="-1")
        total_annual_output = response.xpath("//div[@class='profile-list authProductionCapacity']/div[@class='profile-detail'][contains(text(), 'output')]/strong/text()").get(default="-1")

        # Quality control
        quality_control_on_all_lines = response.xpath("//div[@class='profile-list authQualityControlCapacity']/div[@class='profile-detail'][contains(text(), 'control')]/strong/text()").get(default="-1") , 
        qa_qc_inspectors = response.xpath("//div[@class='profile-list authQualityControlCapacity']/div[@class='profile-detail'][contains(text(), 'inspectors')]/strong/text()").get(default="-1"), 
        
        # Trade background
        main_markets = response.xpath("//div[@class='profile-list authMarketCooperation']/div[@class='profile-detail'][contains(text(), 'markets')]/strong/text()").get(default="-1"),  
        main_client_types = response.xpath("//div[@class='profile-list authMarketCooperation']/div[@class='profile-detail'][contains(text(), 'client')]/strong/text()").get(default="-1"),  

        # R&D capabilities
        customization_options = response.xpath("//div[@class='profile-list authRdCapacity']/div[@class='profile-detail'][contains(text(), 'options')]/strong/text()").get(default="-1"), 
        new_products_launched_last_year = response.xpath("//div[@class='profile-list authRdCapacity']/div[@class='profile-detail'][contains(text(), 'launched')]/strong/text()").get(default="-1"), 
        r_d_engineers = response.xpath("//div[@class='profile-list authRdCapacity']/div[@class='profile-detail'][contains(text(), 'engineers')]/strong/text()").get(default="-1")

        item = ManufactureItem(
            name=name, 
            # url = scrapy.Field()  
            location = location,
            score=score,
            reviews = reviews,
            # main_categories = scrapy.Field()  # product page has the complete info of it; for ex:https://zorssarhair.en.alibaba.com/productlist.html 
            average_response_time = average_response_time,
            on_time_delivery_rate = on_time_delivery_rate,
            total_orders_so_far = total_orders_so_far,
            total_order_amount = total_order_amount,
            floor_space = floor_space,
            annual_export_revenue = annual_export_revenue, 
            # services = scrapy.Field()  
            # quality_control = scrapy.Field()
            # certificates = scrapy.Field() 
            # floor_space = scrapy.Field()  
            # annual_export_revenue = scrapy.Field()
            production_lines = production_lines,
            production_machines = production_machines, 
            total_annual_output = total_annual_output, 
            
            quality_control_on_all_lines = quality_control_on_all_lines, 
            qa_qc_inspectors = qa_qc_inspectors, 
            main_markets = main_markets,  
            main_client_types = main_client_types, 
            customization_options = customization_options, 
            new_products_launched_last_year = new_products_launched_last_year, 
            r_d_engineers = r_d_engineers
        )

        print("\n-----------------------------------------\n")
        print(f"current manufacture name: {item['name']}, all its data are below: \n")
        for key in item: 
            print(f"{key}: {item.get(key)}")
        print("\n-----------------------------------------\n")
        yield item

