import time
import scrapy
import re, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from fake_useragent import UserAgent


CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
WINDOW_SIZE = '1920,1080'
MAX_SCROLL_PAGE_NUM = 999999
SCROLL_PAUSE_TIME = 3
SLEEP_TIME=2

class QnabotSpider(scrapy.Spider):
    name = 'qnaBot'
    allowed_domains = ['https://m.r114.com/?_c=service&_m=m4230']
    start_urls = ['https://m.r114.com/?_c=service&_m=m4230']

    def __init__(self):

        self.chrome_options = Options()
        self.chrome_options.add_argument( "--headless" )
        self.chrome_options.add_argument( "--no-sandbox" )
        self.chrome_options.add_argument( "--disable-gpu" )
        self.chrome_options.add_argument(f'user-agent={UserAgent().random}')
        self.chrome_options.add_argument( f"--window-size={ WINDOW_SIZE }" )
        
        self.base = self.start_urls[0]
        self.declare_xpath()
        self.cnt = 0
        self.total_cnt = 0

    def declare_xpath(self):
        self.button_xpath = '//a[@class="btn_view"]'
        self.text_xpath = '//div[@class="inner1"]//div[@class="txt"]'

    def scrollDown(self, driver, MAX_SCROLL_PAGE_NUM):

        # Get scroll height
        last_height = driver.execute_script("return document.body. scrollHeight")
        for i in range(MAX_SCROLL_PAGE_NUM):

            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print(f'here is bottom of page! scrolled {i} times')

                break
            last_height = new_height  
            if i % 10 == 0:
                print(f'scrolling down.. {i}  / {MAX_SCROLL_PAGE_NUM} times')


    def parse(self, response):
        driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=self.chrome_options )
        base_url = response.url
        driver.get(base_url)

        if not os.path.isfile('script_list.txt'):
            print('script_list.txt file not exist!')
            print('making script_list.txt file ..')
            self.scrollDown(driver, MAX_SCROLL_PAGE_NUM)

            button_list = driver.find_elements_by_xpath(self.button_xpath)

            scripts=[]
            for el in button_list:
                scripts.append(el.get_attribute('onclick'))
            
            with open('script_list.txt','w') as f:
                f.write('\n'.join(scripts))

        else:
            print('script_list.txt file already exist! skip this process')


        texts=[]
        with open('script_list.txt','r') as f:
            print('start crawling!')

            lines = f.readlines()

            for i, line in enumerate(lines[:]):
                try:
                    driver.execute_script(line)
                    time.sleep(1)
                    text = driver.find_elements_by_xpath(self.text_xpath)[0].text
                    texts.append(text)
                except:
                    prnit('Error!')
                    continue
                driver.get(base_url)
                time.sleep(1)

                if i % 10 == 0:
                    print(f'process: [{i}/{len(lines)}] ({int(i)/int(len(lines)) * 100:.2f} %)')
        
        with open('crawled.txt', 'w') as f:

            f.write('\n'.join(texts))
