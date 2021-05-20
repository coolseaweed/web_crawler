from bs4 import BeautifulSoup
import logging
import scrapy
import os, requests, sys
import re

logging.basicConfig(
    format="[%(asctime)s][%(levelname)s]:%(name)s|%(message)s",
    stream=sys.stdout, 
    level=logging.INFO
    )
logger = logging.getLogger(__name__)

class AliexpressTabletsSpider(scrapy.Spider):
    name = 'aliexpress_tablets'
    allowed_domains = ['aliexpress.com']
    start_urls = [
        'https://www.aliexpress.com/category/200216607/tablets.html',
        'https://www.aliexpress.com/category/200216607/tablets/2.html?site=glo&g=y&tag='
    ]
    def parse(self, response):

        print("procesing:"+response.url)
        #Extract data using css selectors
        product_name=response.css('.product::text').extract()
        price_range=response.css('.value::text').extract()
        #Extract data using xpath
        orders=response.xpath("//em[@title='Total Orders']/text()").extract()
        company_name=response.xpath("//a[@class='store $p4pLog']/text()").extract()

        row_data=zip(product_name,price_range,orders,company_name)
        
        for item in row_data:
            #create a dictionary to store the scraped info
            scraped_info = {
                #key:value
                'page':response.url,
                'product_name' : item[0], #item[0] means product in the list and so on, index tells what value to assign
                'price_range' : item[1],
                'orders' : item[2],
                'company_name' : item[3],
            }

            #yield or give the scraped info to scrapy
            yield scraped_info
# if __name__ == '__main__':

#     url='https://www.qoo10.jp/'

#     raw_dir = os.path.join("raw_data","qoo10")
#     export_dir = os.path.join("export","qoo10")
#     os.makedirs(raw_dir,exist_ok=True)
#     os.makedirs(export_dir,exist_ok=True)

#     raw_file = os.path.join(raw_dir,"corpus_qoo10.txt")
#     out_file = os.path.join(export_dir,"corpus_qoo10.txt")


#     getTextFromQoo10(url, raw_file)

