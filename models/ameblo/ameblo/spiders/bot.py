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


class BotSpider(scrapy.Spider):
    name = 'bot'
    allowed_domains = ['https://ameblo.jp/daitahikaru-blog/entrylist.html']
    start_urls = ['https://ameblo.jp/daitahikaru-blog/entrylist.html']


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
        self.url_xpath = '//h2[@data-uranus-component="entryItemTitle"]/a'
        self.next_page_xpath = '//a[@data-uranus-component="paginationNext"]'
        self.last_page_xpath = '//a[@data-uranus-component="paginationEnd"]'
        self.text_xpath = '//div[@data-uranus-component="entryBody"]'


    def parse(self, response):
        driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=self.chrome_options )
        base_url = response.url
        driver.get(base_url)


        target = 'daitahikaru_url_list.txt'
        text_path = 'text/crawled_daitahikaru.txt'



        if not os.path.isfile(target):
            print(f'{target} file not exist!')
            print(f'crawling url lists..')


            url_list = []
            last_page_url = driver.find_elements_by_xpath(self.last_page_xpath)[0].get_attribute('href')
            
            cnt = 1
            while True :
                driver.get(base_url)
                time.sleep(2)

                url_list += [el.get_attribute('href') for el in driver.find_elements_by_xpath(self.url_xpath)]
                next_page_url = driver.find_elements_by_xpath(self.next_page_xpath)[0].get_attribute('href')


                print(f'curr: {base_url} / last: {last_page_url} [{cnt}]')
                cnt += 1 
                
                if base_url == last_page_url: break
                else : base_url = next_page_url

    
            with open(target,'w') as f:
                f.write('\n'.join(url_list))
        
        else:
            print(f'{target}file already exist! skip this process')

        texts = []

        with open(target,'r') as f:
            print('grep text data..')

            lines = f.readlines()
            for i, line in enumerate(lines[:]):
                try:
                    driver.get(line)
                    time.sleep(1)

                    text = driver.find_elements_by_xpath(self.text_xpath)[0].text
                    texts.append(text)

                except:
                    print(f'Error! in {line}')
                    continue
        
                if i % 10 == 0:
                    print(f'process: [{i}/{len(lines)}] ({int(i)/int(len(lines)) * 100:.2f} %)')
        

        with open(text_path, 'w') as f:

            f.write('\n'.join(texts))




