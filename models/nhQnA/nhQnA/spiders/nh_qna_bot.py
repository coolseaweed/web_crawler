import time
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from nhQnA.items import NhqnaItem


CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
WINDOW_SIZE = '1920,1080'
MAX_SCROLL_PAGE_NUM = 0
SCROLL_PAUSE_TIME = 1 




class NhQnaBotSpider(scrapy.Spider):
    name = 'nh_qna_bot'
    allowed_domains = ['www.nhqv.com/']
    start_urls = ['https://www.nhqv.com/wooriwmBoard/boardList.action?sBoard_Id=149&sType_Cd=3000000000']



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

        # //*[@id="contents"]/div[3]/div
        # //*[@id="contents"]/div[5]/div/div[1]/p/a


    def declare_xpath(self):
        self.qna_xpath = '//*[@id="dataTable"]/tbody/tr/td[2]/a'
        self.qna_next_xpath = ''

        
    def parse(self, response):

        driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=self.chrome_options )
        driver.get(response.url)
        frames = driver.find_elements_by_tag_name('frame')
        driver.switch_to_frame(frames[0])

        qna_first = driver.find_elements_by_xpath(self.qna_xpath)[0]
        title = qna_first.text
        qna_first.click()
        #print(driver.page_source)
        element = driver.find_element_by_class_name('viewContents')
        print(title)
        print(element.text)

        temp = driver.find_elements_by_xpath(self.qna_xpath)[0]
        
        # #//*[@id="contents"]/div[3]/div
        # for base in qna_list:
        #     href = base.get_attribute("href")
        #     print('-------------------')
        #     if href is not None and "javascript:void" in href:
        #         try:
        #             print(base.text)
        #             base.click()
        #             time.sleep(2)
        #             element = driver.find_element_by_class_name('viewContents')
        #             #print(element)
        #             print(element.text)
        #         except selenium.common.exceptions.UnexpectedAlertPresentException :
        #             driver.clear()

        #             driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=self.chrome_options )
        #             driver.get(response.url)
        #             frames = driver.find_elements_by_tag_name('frame')
        #             driver.switch_to_frame(frames[0])
        #     time.sleep(5)
        #     # print(driver.page_source)
        #     # print(sleep(5))

        #driver.switch_to_frame(frames[0])
