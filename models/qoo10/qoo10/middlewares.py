# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.option.desired_capabilities import DesiredCapabilities


CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
WINDOW_SIZE = '1920,1080'
MAX_SCROLL_PAGE_NUM = 1
SCROLL_PAUSE_TIME = 1 

class Qoo10SpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):

        # This method is used by Scrapy to create your spiders.
        print("This is Qoo10SpiderMiddleware from crawler ===============")
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
        spider.logger.info('Spider opened: %s' % spider.name)


class Qoo10DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        print("This is Qoo10SpiderMiddleware from crawler +++++++++++++++")
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s


    def spider_opened(self, spider):

        spider.logger.info('Spider opened: %s' % spider.name)

        chrome_options = Options()
        chrome_options.add_argument( "--headless" )
        chrome_options.add_argument( "--no-sandbox" )
        chrome_options.add_argument( "--disable-gpu" )
        chrome_options.add_argument( f"--window-size={ WINDOW_SIZE }" )
        
        driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options )
        self.driver = driver   
             

    def spider_closed(self, spider):
        self.driver.close()


    def process_request(self, request, spider):

        spider.logger.info(f'request_url is: {request.url}')
 
        if ('cat' in request.url) or ('Category' in request.url):

            self.driver.get(request.url)

            #print(f'[Middleware] url:{request.url} scrolling down..')
            # button = self.driver.find_elements_by_xpath('//input[]')
            # button.click()

            # Get scroll height
            last_height = self.driver.execute_script("return document.body. scrollHeight")
            for _ in range(MAX_SCROLL_PAGE_NUM):

                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height  

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            body = to_bytes(text=self.driver.page_source)
            return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

        else:
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
