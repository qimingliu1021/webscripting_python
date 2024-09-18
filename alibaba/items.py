# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ManufactureItem(scrapy.Item):
    name = scrapy.Field() 
    url = scrapy.Field()  
    location = scrapy.Field()  
    score = scrapy.Field() 
    reviews = scrapy.Field()  
    main_categories = scrapy.Field()  # product page has the complete info of it; for ex:https://zorssarhair.en.alibaba.com/productlist.html 
    average_response_time = scrapy.Field()
    on_time_delivery_rate = scrapy.Field()
    total_orders_so_far = scrapy.Field()
    total_order_amount = scrapy.Field()
    services = scrapy.Field()  
    quality_controls = scrapy.Field()
    certifications = scrapy.Field() 
    floor_space = scrapy.Field()  
    annual_export_revenue = scrapy.Field()
    production_lines = scrapy.Field()  
    total_annual_output = scrapy.Field()
    production_machines = scrapy.Field()
    quality_control_on_all_lines = scrapy.Field() 
    qa_qc_inspectors = scrapy.Field()
    main_markets = scrapy.Field()  
    main_client_types = scrapy.Field()  
    customization_options = scrapy.Field()  
    new_products_launched_last_year = scrapy.Field()
    r_d_engineers = scrapy.Field()  


class VerifiedCapabilitiesItem(scrapy.Item): 
    service = scrapy.Field()
    quality_control = scrapy.Field()
    certificates = scrapy.Field()

class ManufactureProductItem(scrapy.Item):
    product_name = scrapy.Field()       # //div[@class='component-product-list']//span[@class='title-con']
    price = scrapy.Field()      # //div[@class='component-product-list']//div[@class='price']
    shipping_requirement = scrapy.Field()      # //div[@class='component-product-list']//div[@class='freight-str']
    moq = scrapy.Field()        # //div[@class='component-product-list']//div[@class='moq']


