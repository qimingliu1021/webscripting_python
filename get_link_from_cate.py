import scrapy
import os
import csv
import time
import datetime
from alibaba.items import ManufactureItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

category_to_go = category_to_go = {
"vehicle_parts_accessories": "https://www.alibaba.com/factory/Vehicle-Parts-Accessories_p34?spm=a2700.factory_home.category_nav.category_popup",
"vehicle_accessories_electronics_tools": "https://www.alibaba.com/factory/Vehicle-Accessories-Electronics-Tools_p202014504?spm=a2700.factory_home.category_nav.category_popup",
"vehicles_transportation": "https://www.alibaba.com/factory/Vehicles-Transportation_p201275273?spm=a2700.factory_home.category_nav.category_popup",
"industrial_machinery": "https://www.alibaba.com/factory/Industrial-Machinery_p43?spm=a2700.factory_home.category_nav.category_popup",
"construction_building_machinery": "https://www.alibaba.com/factory/Construction-Building-Machinery_p201943703?spm=a2700.factory_home.category_nav.category_popup",
"consumer_electronics": "https://www.alibaba.com/factory/Consumer-Electronics_p44?spm=a2700.factory_home.category_nav.category_popup",
"home_appliances": "https://www.alibaba.com/factory/Home-Appliances_p6?spm=a2700.factory_home.category_nav.category_popup",
"apparel_accessories": "https://www.alibaba.com/factory/Apparel-Accessories_p3?spm=a2700.factory_home.category_nav.category_popup",
"jewelry_eyewear_watches_accessories": "https://www.alibaba.com/factory/Jewelry-Eyewear-Watches-Accessories_p36?spm=a2700.factory_home.category_nav.category_popup",
"lights_lighting": "https://www.alibaba.com/factory/Lights-Lighting_p39?spm=a2700.factory_home.category_nav.category_popup",
"construction_real_estate": "https://www.alibaba.com/factory/Construction-Real-Estate_p13?spm=a2700.factory_home.category_nav.category_popup",
"home_garden": "https://www.alibaba.com/factory/Home-Garden_p15?spm=a2700.factory_home.category_nav.category_popup",
"furniture": "https://www.alibaba.com/factory/Furniture_p1503?spm=a2700.factory_home.category_nav.category_popup",
"pet_supplies": "https://www.alibaba.com/factory/Pet-Supplies_p201946504?spm=a2700.factory_home.category_nav.category_popup",
"fabric_textile_raw_material": "https://www.alibaba.com/factory/Fabric-Textile-Raw-Material_p4?spm=a2700.factory_home.category_nav.category_popup",
"beauty": "https://www.alibaba.com/factory/Beauty_p66?spm=a2700.factory_home.category_nav.category_popup",
"personal_care_household_cleaning": "https://www.alibaba.com/factory/Personal-Care-Household-Cleaning_p201951502?spm=a2700.factory_home.category_nav.category_popup",
"health_care": "https://www.alibaba.com/factory/Health-Care_p100002908?spm=a2700.factory_home.category_nav.category_popup",
"medical_devices_supplies": "https://www.alibaba.com/factory/Medical-devices-Supplies_p16?spm=a2700.factory_home.category_nav.category_popup",
"packaging_printing": "https://www.alibaba.com/factory/Packaging-Printing_p23?spm=a2700.factory_home.category_nav.category_popup",
"school_office_supplies": "https://www.alibaba.com/factory/School-Office-Supplies_p21?spm=a2700.factory_home.category_nav.category_popup",
"testing_instrument_equipment": "https://www.alibaba.com/factory/Testing-Instrument-Equipment_p201734802?spm=a2700.factory_home.category_nav.category_popup",
"tools_hardware": "https://www.alibaba.com/factory/Tools-Hardware_p1420?spm=a2700.factory_home.category_nav.category_popup",
"security": "https://www.alibaba.com/factory/Security_p30?spm=a2700.factory_home.category_nav.category_popup",
"safety": "https://www.alibaba.com/factory/Safety_p201727804?spm=a2700.factory_home.category_nav.category_popup",
"fabrication_services": "https://www.alibaba.com/factory/Fabrication-Services_p41?spm=a2700.factory_home.category_nav.category_popup",
"electrical_equipment_supplies": "https://www.alibaba.com/factory/Electrical-Equipment-Supplies_p5?spm=a2700.factory_home.category_nav.category_popup",
"electronic_components_accessories_telecommunications": "https://www.alibaba.com/factory/Electronic-Components-Accessories-Telecommunications_p502?spm=a2700.factory_home.category_nav.category_popup",
"sports_entertainment": "https://www.alibaba.com/factory/Sports-Entertainment_p18?spm=a2700.factory_home.category_nav.category_popup",
"mother_kids_toys": "https://www.alibaba.com/factory/Mother-Kids-Toys_p26?spm=a2700.factory_home.category_nav.category_popup",
"gifts_crafts": "https://www.alibaba.com/factory/Gifts-Crafts_p17?spm=a2700.factory_home.category_nav.category_popup",
"luggage_bags_cases": "https://www.alibaba.com/factory/Luggage-Bags-Cases_p1524?spm=a2700.factory_home.category_nav.category_popup",
"shoes_accessories": "https://www.alibaba.com/factory/Shoes-Accessories_p322?spm=a2700.factory_home.category_nav.category_popup",
"metals_alloys": "https://www.alibaba.com/factory/Metals-Alloys_p9?spm=a2700.factory_home.category_nav.category_popup",
"chemicals": "https://www.alibaba.com/factory/Chemicals_p8?spm=a2700.factory_home.category_nav.category_popup",
"rubber_plastics": "https://www.alibaba.com/factory/Rubber-Plastics_p80?spm=a2700.factory_home.category_nav.category_popup",
"agriculture": "https://www.alibaba.com/factory/Agriculture_p1?spm=a2700.factory_home.category_nav.category_popup",
"food_beverage": "https://www.alibaba.com/factory/Food-Beverage_p2?spm=a2700.factory_home.category_nav.category_popup",
"commercial_equipment_machinery": "https://www.alibaba.com/factory/Commercial-Equipment-Machinery_p2829?spm=a2700.factory_home.category_nav.category_popup",
"business_services": "https://www.alibaba.com/factory/Business-Services_p28?spm=a2700.factory_home.category_nav.category_popup",
"renewable_energy": "https://www.alibaba.com/factory/Renewable-Energy_p201726502?spm=a2700.factory_home.category_nav.category_popup",
"environment": "https://www.alibaba.com/factory/Environment_p11?spm=a2700.factory_home.category_nav.category_popup",
"power_transmission": "https://www.alibaba.com/factory/Power-Transmission_p201723202?spm=a2700.factory_home.category_nav.category_popup",
"material_handling": "https://www.alibaba.com/factory/Material-Handling_p201725504?spm=a2700.factory_home.category_nav.category_popup"
}

custom_settings = {
'DOWNLOAD_DELAY': 0.5,
'CONCURRENT_REQUESTS': 2
}

if __name__ == "__main": 
    for cur_category in category_to_go: 

        print(f"Now scraping {cur_category}")

        cur_category_dir = f"data/{cur_category}"
        os.makedirs(cur_category_dir, exist_ok=True)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(category_to_go[cur_category])

        # Scrolling all the way to bottom with lazy loading
        print("scrolling down page...")
        for i in range(1,30):
            increasing = str(1000*i)
            js = 'window.scrollTo(0, '+increasing+')'
            driver.execute_script(js)
            time.sleep(1)

        manufacture_names = driver.find_elements(By.XPATH, "//div[@class='hugo4-supplier-card-base-info']//span[@class='supplier-company-name']")
        link_elements = driver.find_elements(By.XPATH, "//div[@class='hugo4-supplier-card-base-info']//a[@class='hugo-dotelement base-info']")

        # filename = os.path.join(cur_category_dir, f"{cur_category}_{self.now}.csv")
        filename = os.path.join(cur_category_dir, f"{cur_category}.csv")
        manufactures = {}

        with open(filename, "a") as csv_file: 
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["name", "link"])

        for i in range(len(manufacture_names)):

            name = manufacture_names[i].text
            link = link_elements[i].get_attribute('href') 
            # Making manufacture dic - {"name": "url", ...}
            manufactures[name] = link       

            with open(filename, "a") as csv_file: 
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([name, link])

    driver.quit()

