# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import json
from scrapy import signals
import logging
import requests
import urllib3

# Disable urllib3 logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

# useful for handling different item types with a single interface
# from itemadapter import is_item, ItemAdapter

class AlibabaSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class AlibabaDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)



# 代理池接口
PROXY_URL = 'http://127.0.0.1:5010/get'

class ProxyMiddleware(object):
    # 初始化
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url
 
    # 获取随机代理IP
    def get_random_proxy(self):
        print("\n-------------- START OF get_random_proxy() -------------- \n")
        try:
            response = requests.get(self.proxy_url)
            print(f"Getting a proxy from http://127.0.0.1:5010/get. Response is {response.text}")
            if response.status_code == 200:
                global proxy
                p = json.loads(response.text)
                proxy = "http://" + "{}".format(p.get('proxy'))
                ip = {"http": proxy, "https": proxy}
                r = requests.get("https://betteractive.en.alibaba.com/factory.html", proxies=ip, timeout=60)
                print(f"Getting requests from baidu, response is {r}")
                print(f"response status code is {r.status_code}")
                if r.status_code == 200:
                    print(f"proxy works, using: {proxy}")
                    print("\n-------------- END OF get_random_proxy() -------------- \n")
                    return proxy
            else:
                print(f"Can't get proxy from {self.proxy_url}")
                return self.get_random_proxy()
        except Exception as e: 
            print("get_random_proxy() try failed. error is: \n", e)
            print("Trying again")
            return self.get_random_proxy()
 
    def process_request(self, request, spider):
        print("\n-------------- START OF MIDWARE process_request() -------------- \n")
        proxy = self.get_random_proxy()
        print(f"proxy is: {proxy}")
        if proxy:
            self.logger.debug('======' + '使用代理 ' + str(proxy) + "======")
            request.meta['proxy'] = proxy
            print("\n-------------- END OF MIDWARE process_request() -------------- \n")
 
    def process_response(self, request, response, spider):
        print("\n-------------- START OF MIDWARE process_response() -------------- \n")
        if response.status != 200:
            print(f"response.status not obtained, returning request: {request}\n")
            request.meta['proxy'] = proxy
            print("\n-------------- END OF MIDWARE process_response() code != 200 -------------- \n")
            return request

        # proxy = request.meta.get('proxy', None)
        # if proxy:
        #     self.logger.debug(f"Response from proxy: {proxy} for request: {request.url}")
        
        # if response.status != 200:
        #     self.logger.debug(f"Retrying request with proxy: {proxy}")
        #     return self.process_request(request, spider)
        print(f"Response: {response}\n")
        print("\n-------------- END OF MIDWARE process_response() code == 200 -------------- \n")
        return response
 
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )

