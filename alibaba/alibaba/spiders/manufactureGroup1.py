import scrapy
import re
import os
import time
import random
import pandas as pd
import datetime
from lxml import etree
from urllib.parse import urlparse
from alibaba.items import ManufactureItem
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# Set logging level to WARNING
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)

class ManufactureGroupOneSpider(scrapy.Spider):
    name = "manufacture_group_1"
    csv_store_base = "data_group_1"
    csv_path = "gruop_1"
    allowed_domains = ["alibaba.com"]
    now = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    file_count = 1
    begin_time = datetime.datetime.now()
    log_store = os.makedirs("LOGS", exist_ok=True)
    log_store = "LOGS"
    current_manufacture_name = ""
    csv_directories = []
    chrome_options = webdriver.ChromeOptions()

    # Different page positions for random scrolling at main page
    scrolling_class = [".//div[@class='module-verifiedAllProducts']", 
                        "//div[@class='module-verifiedVlog']", 
                        "//div[@class='J_module']", 
                        "//div[@class='module-ratingsAndReviews']", 
                        "//div[@class='module-verifiedProfile']"]


    def __init__(self):

        # Get all manufacture directories in list for later go through
        self.csv_directories = [d for d in os.listdir(self.csv_store_base)
                                if os.path.isdir(os.path.join(self.csv_store_base, d)) and d != "LOGS"]
        
        # Debug purposes
        print("categories are: ", self.csv_directories)
        
        if not self.csv_directories:
            raise ValueError("No valid directories found under 'data/' except 'LOGS'.")

        # Initialize Selenium WebDriver (Chrome)
        # chrome_options.add_argument("--headless")  # Run in headless mode
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-software-rasterizer")
        
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.chrome_options)


    def start_requests(self): 
        print("csv_directories: ", self.csv_directories)
        for directory in self.csv_directories:
            self.csv_path = os.path.join(self.csv_store_base, directory, f"{directory}.csv")
            print("self.csv_path at start_requests() is: ", self.csv_path)
            if not os.path.exists(self.csv_path):
                print(f"CSV file not found in directory: {directory}, skipping.")
                continue
            df = pd.read_csv(self.csv_path)
            for index, row in df.iterrows(): 
                self.file_count += 1
                time.sleep(2)
                link = row['link']
                
                # for debug purpose
                print(f"------------------------------------------")
                print(f"Time begins: {self.begin_time}, \nTime now: {datetime.datetime.now()}")
                print(f"On directory {directory}")
                print(f"getting {row['name']}, {link}")
                print(f"------------------------------------------")

                yield scrapy.Request(link, callback=self.parse_with_selenium)


    def parse_with_selenium(self, response):

        # Checking what proxy is being used now
        PROXY = response.meta.get('proxy')
        if PROXY:
            print(f"Using proxy: {PROXY}")
        else:
            print("No proxy is being used for this request.")
        
        # Checking what user-agent is being used now
        user_agent = response.request.headers.get('User-Agent', None)

        if user_agent:
            print(f"User Agent being used: {user_agent.decode('utf-8')}")
        else:
            print("No User Agent set for this request")

        url = response.url
        parsed_url = urlparse(url)
        
        # set up the link for the page that has complete "main categories" by changing the url
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # Make sure the proxy is being used by selenium
        self.chrome_options.add_argument('--proxy-server=%s' % PROXY)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.chrome_options)
        self.driver.get(response.url)
        print("self.driver.get(response.url) GETTING URL...")
        # ENHANCEMENT NEEDED - with captcha. Once met captcha, change UA and proxy
        if ("_____tmd_____/punish?" in self.driver.current_url): 
            print("-------------- met captcha --------------")
            print("Consider changing a proxy or UA")
        
        rendered_html = self.driver.page_source
        
        # supplement response with the response obtained by selenium
        response = scrapy.http.TextResponse(url=response.url, body=rendered_html, encoding='utf-8')

        name = response.xpath("//div[@class='shop-sign']//h1/text()").get(default=-1)
        location = response.xpath("//div[@class='company-info']/span/text()").get(default=-1)

        # Main categories are often incomplete, checking if incomplete, then click "visit store" to get complete main category data there
        main_categories = response.xpath("//div[@class='company-info']/span[contains(text(), 'Main categories')]/text()").get(default=-1)
        re_scrape = False
        if main_categories != -1 and "..." in main_categories:
            re_scrape = True
            main_categories = main_categories[17:].rsplit(' ', 1)[0]
        print("main category: ", main_categories)

        wait = WebDriverWait(self.driver, 10)

        # Mimic human operation - random page class navigation and random time staying in the page
        for point_class in self.scrolling_class: 
            try: 
                # Haven't implement random class selection yet
                element = wait.until(EC.element_to_be_clickable((By.XPATH, point_class)))
                ActionChains(self.driver).move_to_element(element).perform()
                time.sleep(random.uniform(1, 3))
            except TimeoutException: 
                print("Should change proxy and start again")

        score = response.xpath("//span[@class='score-text']/text()").get(default=-1)
        
        reviews = response.xpath(".//div[@class='rating-container']/a/text()").get(default=-1)
        reviews_number = (lambda reviews: int(reviews[:-8]) if reviews != -1 and len(reviews)>8 else -1)(reviews)

        average_response_time = response.xpath("//ul[@class='supplier-ability']/li[div[contains(text(), 'average response time')]]/strong/text()").get(default="-1")
        on_time_delivery_rate = response.xpath("//ul[@class='supplier-ability']/li[div[contains(text(), 'on-time delivery rate')]]/strong/text()").get(default="-1")
        on_time_delivery_rate_decimal = float(re.search(r'[\d.]+', on_time_delivery_rate).group()) / 100 if on_time_delivery_rate != "-1" else -1
        total_orders_so_far = response.xpath("//ul[@class='supplier-ability']/li[div[contains(text(), 'orders')]]/div[@class='title']/text()").get(default="-1")

        if total_orders_so_far != "-1": 
            match = re.search(r"\d+", total_orders_so_far)
            total_orders_so_far_number = int(match.group()) if match else -1
        else: 
            total_orders_so_far_number = -1

        total_order_amount = response.xpath("//ul[@class='supplier-ability']/li[div[contains(text(), 'orders')]]/strong[contains(text(), 'US')]/text()").get(default="-1")
        total_order_amount_number = (lambda total_order_amount: int(total_order_amount[4:-1].replace(",", "")) 
                             if isinstance(total_order_amount, str) and total_order_amount != "-1" and len(total_order_amount) > 5 
                             else -1)(total_order_amount)

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

        # Click "See all verified capabilities (12)" button to get "verified capabilities"
        view_capabilities_button = self.driver.find_element(By.CLASS_NAME, "all-tags")
        view_capabilities_button.click()
        time.sleep(random.uniform(1, 5))

        dialog_content = self.driver.find_element(By.CLASS_NAME, "tags-dialog").get_attribute('innerHTML')
        print(dialog_content)
        dialog_tree = etree.HTML(dialog_content)

        services = dialog_tree.xpath("//span[text()='Service']/following-sibling::div[@class='list-item']//span[@class='hover-span']/text()")
        quality_control = dialog_tree.xpath("//span[text()='Quality control']/following-sibling::div[@class='list-item']//span[@class='hover-span']/text()")
        certificates = dialog_tree.xpath("//span[text()='Certifications']/following-sibling::div[@class='list-item']//span[@class='hover-span']/text()")

        services = ", ".join(services) if services else "-1"
        quality_control = ", ".join(quality_control) if quality_control else "-1"
        certificates = ", ".join(certificates) if certificates else "-1"

        try:
            close_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='next-dialog-close']"))
            )
            close_button.click()
            print("Dialog closed successfully.")
        except Exception as e:
            print(f"Failed to close the dialog: {e}")
        
        self.driver.get(base_url)
        
        # If "visit store" page has no "main category" to scrape then remains what gets from main page
        if re_scrape:
            try:
                main_categories_element = self.driver.find_element(By.XPATH, "//div[contains(@class, 'info-line') and contains(text(), 'Main categories')]")
                main_categories = main_categories_element.text
                main_categories[17:]
                time.sleep(2)
                print(f"Main category: {main_categories}")
            except TimeoutException: 
                print(f"Main category remains the same for {name}")
            except NoSuchElementException: 
                print(f"Main category remains the same for {name}")

        # According to definitions in items.py
        item = ManufactureItem(
            name=name, 
            url=url,
            location=location,
            score=score,
            reviews=reviews_number,
            main_categories=main_categories,
            average_response_time=average_response_time,
            on_time_delivery_rate=on_time_delivery_rate_decimal,
            total_orders_so_far=total_orders_so_far_number,
            total_order_amount=total_order_amount_number,
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
            quality_control = quality_control, 
            certificates = certificates
        )

        print("\n-----------------------------------------\n")
        print(f"Current manufacturer name: {item['name']}, link is {url} \nall its data are below: \n")

        for key in item: 
            print(f"{key}: {item.get(key)}")
        
        print("In spider file - yielding item...")
        yield item

    def closed(self, reason):
        # Close the browser when the spider finishes
        self.driver.quit()
