# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import datetime
from scrapy import signals

class AlibabaPipeline:

    # keys = [
    #     "name", "link", "location", "score", "reviews", "average_response_time", 
    #     "on_time_delivery_rate", "total_orders_so_far", "total_order_amount", "services", "quality_controls", "certifications", 
    #     "floor_space", "annual_export_revenue", "production_lines", 
    #     "production_machines", "total_annual_output", "quality_control_on_all_lines", 
    #     "qa_qc_inspectors", "main_markets", "main_client_types", 
    #     "customization_options", "new_products_launched_last_year", 
    #     "r_d_engineers"
    # ]

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

    def open_spider(self, spider): 

    # Use the current date and manufacture name for the CSV filename
        csv_filename = "{}_{}.csv".format(spider.now, spider.file_count)
        self.file = open(csv_filename, "a", encoding="utf-8", newline="")
        self.csv_writer = csv.writer(self.file)
        self.csv_writer.writerow(self.keys)  # Write the header row

    def process_item(self, item, spider):
        row = [
            item.get("name"), item.get("url"), item.get("location"), item.get("score"),
            item.get("reviews"), 
            # item.get("main_categories"), 
            item.get("average_response_time"),
            item.get("on_time_delivery_rate"), item.get("total_orders_so_far"),
            item.get("total_order_amount"), item.get("services"), item.get("quality_control"),
            item.get("certificates"), item.get("floor_space"), item.get("annual_export_revenue"),
            item.get("production_lines"), item.get("total_annual_output"),
            item.get("production_machines"), item.get("quality_control_on_all_lines"),
            item.get("qa_qc_inspectors"), item.get("main_markets"), item.get("supply_chain_partners"),
            item.get("main_client_types"), item.get("customization_options"),
            item.get("new_products_launched_last_year"), item.get("r_d_engineers")
        ]
        self.csv_writer.writerow(row)  # Write the data row
    
    def close_spider(self, spider): 
        self.file.close()


'''
name, link
xxx, xxx
xxx, xxx
...
'''
