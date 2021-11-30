import time
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from nhInvest.items import NhinvestItem

CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
WINDOW_SIZE = '1920,1080'
MAX_SCROLL_PAGE_NUM = 0
SCROLL_PAUSE_TIME = 1 





class NhbotSpider(scrapy.Spider):
    name = 'nhBot'
    allowed_domains = ['https://www.nhqv.com']
    start_urls = ['https://www.nhqv.com/']


    def __init__(self):


        self.chrome_options = Options()
        self.chrome_options.add_argument( "--headless" )
        self.chrome_options.add_argument( "--no-sandbox" )
        self.chrome_options.add_argument( "--disable-gpu" )
        self.chrome_options.add_argument(f'user-agent={UserAgent().random}')
        self.chrome_options.add_argument( f"--window-size={ WINDOW_SIZE }" )
        
        self.base = 'https://www.nhqv.com'
        self.declare_xpath()
        self.cnt = 0
        self.total_cnt = 0


    def declare_xpath(self):
        self.main_category_url_xpath = '//*[@id="lay_all_mn"]/dl/dd/div[1]/dl/dd/div/a'
        self.sub_category_url_xpath = '//*[@id="lay_all_mn"]/dl/dd/div[1]/dl/dd/div/div/a'

        #self.getTopCategoriesXpath = '//*[@class="goods_detail"]/h2/text()'
        #/html/body/div[3]/div[1]/div[3]/div/ul/li[1]/div
    
    def parse(self, response):


        driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=self.chrome_options )
        driver.get(response.url)
        frames = driver.find_elements_by_tag_name('frame')
        driver.switch_to_frame(frames[0])

        main_category_list = driver.find_elements_by_xpath(self.main_category_url_xpath)
        sub_category_list = driver.find_elements_by_xpath(self.sub_category_url_xpath)
        category_list = main_category_list + sub_category_list
        self.total_cnt = len(category_list)

        for category in category_list[:]:
            url = category.get_attribute('url')
            if 'http' in url:
                next_url = url
            elif url == '':
                continue
            else:
                next_url = self.base + url
            yield self.parse_items(next_url)

    def parse_items(self, url):

        item = NhinvestItem()

        option = self.chrome_options
        option.add_argument(f'user-agent={UserAgent().random}')
        try:
            driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options = option )
            driver.get(url) 
            frames = driver.find_elements_by_tag_name('frame')
            driver.switch_to_frame(frames[0])

            element = driver.find_element_by_tag_name('body')
            item['text'] = element.text
            item['url'] = url

            print(f'processing url:{url} [{self.cnt}/{self.total_cnt}]')
            self.cnt += 1

            driver.close()
            return item

        except:
            print(f'exceptions while processing {url}')

        # frames = self.driver.find_elements_by_tag_name('frame')
        # self.driver.switch_to_frame(frames[0])

        # elemnet = self.driver.find_element_by_tag_name('body')
        # print('-------------------------------------------------------------')
        # print(f'----------------------{response.url}-------------------------------')
        # print(response.text)
        # print('-----------------------------------------------------')
        # print(f'processing main url:{response.url} | # items: {len(response.xpath(self.getAllSubCategoriesXpath))} | total processed item:{self.total_cnt}')
        
        # visited = set()

        # for i, href in enumerate(response.xpath(self.getAllSubCategoriesXpath)):
        #     url = response.urljoin(href.extract())

        #     # print(f'processing sub url is: {url}')
        #     #if i> 10: break

        #     if url not in visited:
        #         visited.add(url)
        #         yield scrapy.Request(url, callback=self.parse_main_item)

        #     #yield scrapy.Request(url,callback=self.parse_subcategory, dont_filter=True)
        # self.total_cnt += len(response.xpath(self.getAllSubCategoriesXpath))



        #print(driver.page_source)
        #print(response.text)

    # def parse(self, response):

    #     for i, href in enumerate(response.xpath(self.getAllCategoriesXpath)):

    #         url = response.urljoin(href.extract())

    #         #scrapy.logger.info(f'processing main url is: {url}')
    #         # print('-------------')
    #         #if i> 1: break

    #         if i % 50 == 0:

    #             print(f'Category gethering : [{i}/{len(response.xpath(self.getAllCategoriesXpath))}]')

    #         yield scrapy.Request(url=url, callback=self.parse_category, dont_filter=True)

    # def parse_category(self, response):

    #     print(f'processing main url:{response.url} | # items: {len(response.xpath(self.getAllSubCategoriesXpath))} | total processed item:{self.total_cnt}')
        
    #     visited = set()

    #     for i, href in enumerate(response.xpath(self.getAllSubCategoriesXpath)):
    #         url = response.urljoin(href.extract())

    #         # print(f'processing sub url is: {url}')
    #         #if i> 10: break

    #         if url not in visited:
    #             visited.add(url)
    #             yield scrapy.Request(url, callback=self.parse_main_item)

    #         #yield scrapy.Request(url,callback=self.parse_subcategory, dont_filter=True)
    #     self.total_cnt += len(response.xpath(self.getAllSubCategoriesXpath))
