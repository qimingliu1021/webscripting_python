# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import os
import datetime
from scrapy import signals

class AlibabaPipeline:

    keys = [
        "Name", "URL", "Location", "Score", "Reviews", "Main Categories", 
        "Average Response Time", "On time Delivery Rate", "Total Orders so far", 
        "Total Order Amount", "Services", "Quality Control", "Certificates", 
        "Floor Space", "Annual Export Revenue (USD)", "Production Lines", 
        "Total Annual Output (Units)", "Production Machines", 
        "Quality Control on All Lines", "QA/QC Inspectors", "Main Markets", 
        "Main Client Types", "Customization Options", 
        "New Products Launched Last Year", "R&D Engineers"
    ]
    csv_filename = ""

    def open_spider(self, spider): 

        os.makedirs(spider.csv_store_base, exist_ok=True)

    # Use the current date and manufacture name for the CSV filename
        print("\n-----------------------------------------\n")
        print("In pipeline.py open_spider() ... ")
        print(f"csv directory to write: {spider.csv_path}")
        print("\n-----------------------------------------\n")
        self.csv_filename = "{}_{}.csv".format(spider.csv_path, spider.now)
        self.file = open(self.csv_filename, "a", encoding="utf-8", newline="")
        self.csv_writer = csv.writer(self.file)
        self.csv_writer.writerow(self.keys) 

    def process_item(self, item, spider):
        print("\n-----------------------------------------\n")
        print("In pipeline.py process_item() ... ")
        row = [
            item.get("name"), item.get("url"), item.get("location"), item.get("score"), item.get("reviews"), item.get("main_categories"), 
            item.get("average_response_time"), item.get("on_time_delivery_rate"), item.get("total_orders_so_far"),
            item.get("total_order_amount"), item.get("services"), item.get("quality_control"), item.get("certificates"), 
            item.get("floor_space"), item.get("annual_export_revenue"), item.get("production_lines"), 
            item.get("total_annual_output"), item.get("production_machines"), 
            item.get("quality_control_on_all_lines"), item.get("qa_qc_inspectors"), item.get("main_markets"), 
            item.get("main_client_types"), item.get("customization_options"),
            item.get("new_products_launched_last_year"), item.get("r_d_engineers")
        ]
        print("writing to file: ", self.csv_filename)
        print("\n-----------------------------------------\n")
        self.csv_writer.writerow(row)  # Write the data row
    
    def close_spider(self, spider): 
        self.file.close()


'''
name, link
xxx, xxx
xxx, xxx
...
'''
