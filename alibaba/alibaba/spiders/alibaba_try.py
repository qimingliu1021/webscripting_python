import scrapy


class AlibabaTrySpider(scrapy.Spider):
    name = "alibaba_try"
    allowed_domains = ["www.alibaba.com"]
    start_urls = ["https://www.alibaba.com"]

    def parse(self, response):
        pass
