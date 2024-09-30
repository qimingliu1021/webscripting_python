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
from scrapy_selenium import SeleniumRequest
from scrapy_splash import SplashRequest


# Set logging level to WARNING
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)

class ManufactureGroupOneSpider(scrapy.Spider):
    name = "manufacture_group_2"
    csv_store_base = "data_group_2"
    csv_path = "gruop_2"
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

                yield SplashRequest(link,
                            callback=self.parse_with_selenium,
                            args={'wait': 10}, # 最大超时时间，单位：秒
                            endpoint='render.html') # 使用splash服务的固定参数


    def parse_with_selenium(self, response):

        PROXY = response.meta.get('proxy')
        print(f"Using proxy: {PROXY}")
        user_agent = response.request.headers.get('User-Agent', None)
        print(f"User Agent being used: {user_agent.decode('utf-8')}")

        url = response.url
        print("response.url is: \n", url)

        if ("_____tmd_____/punish?" in response.text): 
          print("Met captcha. Dumping this request!")
        else: 
          print("Didn't meet captcha. Writting down the response! ")
          with open("page_source.html", "w") as f: 
            f.write(response.text)
        
