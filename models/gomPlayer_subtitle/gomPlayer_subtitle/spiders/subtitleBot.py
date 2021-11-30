import time
import scrapy
import re, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains


from fake_useragent import UserAgent


CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
WINDOW_SIZE = '1920,1080'
MAX_SCROLL_PAGE_NUM = 0
SCROLL_PAUSE_TIME = 1 
SLEEP_TIME=2


class SubtitlebotSpider(scrapy.Spider):
    name = 'subtitleBot'
    allowed_domains = ['https://www.gomlab.com/subtitle/?preface=kr&keyword=']
    start_urls = ['https://www.gomlab.com/subtitle/?preface=kr&keyword=']


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
        self.main_page_xpath = '//*[@class="paging"]//a[@href]'

        self.subtitle_page_xpath = '//*[@class="tbl tbl_board transform"]/tbody/tr//a[@href]'
        self.button_xpath = '//a[@class="btn"]'


    def parse(self, response):
        driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=self.chrome_options )
        driver.get(response.url)


        if not os.path.isfile('url_list.txt'):
            print('url_list.txt file not exist!')
            print('making url_list.txt file ..')

            main_page_list = driver.find_elements_by_xpath(self.main_page_xpath)
            last_page_url = main_page_list[-1].get_attribute("href")
            base_url = re.search('(\S+page\=)([0-9]+)',last_page_url).group(1)
            last_page_num = re.search('(\S+page\=)([0-9]+)',last_page_url).group(2)


            url_list = []
            # for page in (1, int(last_page_num) + 1):
            for page in range(1,int(last_page_num) + 1):
                try:
                    driver.get(f'{base_url}{page}')
                    time.sleep(SLEEP_TIME)
                    subtitle_page_list = driver.find_elements_by_xpath(self.subtitle_page_xpath)

                    for subtitle_page in subtitle_page_list[:]:
                        url_list.append(subtitle_page.get_attribute("href"))
                except:
                    print(f'[ERROR] in {base_url}{page}')
                    continue
                if page % 10 == 0:
                    print(f'process: [{page}/{last_page_num}] ({int(page)/int(last_page_num) * 100:.2f} %)')
                
            with open('url_list.txt','w') as f:
                f.write('\n'.join(url_list))

            print('done!')

        else:
            print('url_list.txt file already exist! skip this process')


        with open('url_list.txt','r') as f:
            print('start crawling!')
            
            lines = f.readlines()

            for i, line in enumerate(lines[:]):
                url = line.strip()

                try:
                    driver.get(url)

                    seq = re.search('seq\=([0-9]+)\&',url).group(1)
                    driver.execute_script(f"subtitleDown({seq}, '')")
                    time.sleep(1)
                except:
                    print(f'[ERROR] in line:{i} {line}')
                    continue
                
                if i % 10 == 0:
                    print(f'process: [{i}/{len(lines)}] ({int(i)/int(len(lines)) * 100:.2f} %)')
                

        print('done!')




