import time
import scrapy
import re, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from fake_useragent import UserAgent


CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
WINDOW_SIZE = '1920,1080'
MAX_SCROLL_PAGE_NUM = 99999
SCROLL_PAUSE_TIME = 10
SLEEP_TIME=5


class BotSpider(scrapy.Spider):

    name = 'bot'


    def __init__(self, category=None, *args, **kwargs):

        super(BotSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://note.com/topic/{category}']
        self.category = category
        self.chrome_options = Options()
        self.chrome_options.add_argument( "--headless" )
        self.chrome_options.add_argument( "--no-sandbox" )
        self.chrome_options.add_argument( "--disable-gpu" )
        self.chrome_options.add_argument(f'user-agent={UserAgent().random}')
        self.chrome_options.add_argument( f"--window-size={ WINDOW_SIZE }" )
        self.declare_xpath()


    def declare_xpath(self):


        self.button_entire_xpath = '//*[@class="a-button m-sectionBody__moreButton fn"]'

        self.button_more_xpath = '//div[@class="p-paging__footer"]//button[@class="a-button"]//div[@class="a-button__inner"]'
        self.url_xpath = '//*[@class="m-largeNoteWrapper__card"]/a'


        self.text_xpath = '//*[@class="note-common-styles__textnote-body"]'

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
                print(f'here is bottom of page! scrolled {i+1} times')

                break
            last_height = new_height  
            if i % 10 == 0:
                print(f'scrolling down.. {i+1}  / {MAX_SCROLL_PAGE_NUM} times')

    def parse(self, response):

        driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=self.chrome_options )
        base_url = response.url
        driver.get(base_url)

        # go to entire pages
        driver.find_elements_by_xpath(self.button_entire_xpath)[0].click()

        time.sleep(SLEEP_TIME)

        target = f'{self.category}_url.list'
        text_path = f'text/crawled_{self.category}.txt'


        if not os.path.isfile(target):
            print(f'{target} file not exist!')
            print(f'crawling url lists..')

            cnt = 0
            while cnt < MAX_SCROLL_PAGE_NUM:
                
                button = driver.find_elements_by_xpath(self.button_more_xpath)

                if len(button) == 0: break
    

                button[0].click()
                time.sleep(SLEEP_TIME)
                self.scrollDown(driver, 1)


                cnt += 1

                if cnt % 10 == 0: 
                    print(f'clicked {cnt} times')



            elements = driver.find_elements_by_xpath(self.url_xpath)
            url_list = [el.get_attribute('href') for el in elements]

            with open(target,'w') as f:
                f.write('\n'.join(url_list))

        else:
            print(f'{target} file already exist! skip this process')

        
        texts = []

        os.makedirs('text',exist_ok=True)
        with open(target,'r') as f:
            print('grep text data..')

            lines = f.readlines()
            for i, line in enumerate(lines[:]):
                
                try:
                    driver.get(line)
                    time.sleep(SLEEP_TIME)

                    text = driver.find_elements_by_xpath(self.text_xpath)[0].text
                    
                    texts.append(text)

                except:
                    print(f'Error! in {line}')
                    continue
        
                if i % 10 == 0:
                    print(f'process: [{i}/{len(lines)}] ({int(i)/int(len(lines)) * 100:.2f} %)')


        with open(text_path, 'w') as f:

            f.write('\n'.join(texts))


