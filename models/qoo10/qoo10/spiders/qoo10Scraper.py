import scrapy
from bs4 import BeautifulSoup

import re
from qoo10.items import Qoo10Item



class Qoo10scraperSpider(scrapy.Spider):
    name = 'qoo10Scraper'
    allowed_domains = ['www.qoo10.jp']
    start_urls = ['https://www.qoo10.jp/gmkt.inc/Bestsellers/']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'qoo10.middlewares.Qoo10DownloaderMiddleware': 100
        }
    }

    def __init__(self):
        self.declare_xpath()
        self.total_cnt=0
        
    def declare_xpath(self):

        self.getAllCategoriesXpath = '//*[@id="ul_default_major"]/li/div/div/ul/li/a/@href'
        self.getAllSubCategoriesXpath = '//*[@id="div_gallery_new"]/ul/li/div/div/a/@href'

        self.TitleXpath  = '//*[@class="goods_detail"]/h2/text()'
        self.CategoryXpath = '//*[@class="category_depth_list"]/li[5]/span/text()'
        self.QnAXpath  = '//*[@class="qna_board"]/div[2]//*[@class="row on"]'

        self.ReviewXpath = '//*[@class="review_list"]/li/p[descendant-or-self::text()]'


    def parse(self, response):

        for i, href in enumerate(response.xpath(self.getAllCategoriesXpath)):

            url = response.urljoin(href.extract())

            #scrapy.logger.info(f'processing main url is: {url}')
            # print('-------------')
            #if i> 1: break

            if i % 50 == 0:

                print(f'Category gethering : [{i}/{len(response.xpath(self.getAllCategoriesXpath))}]')

            yield scrapy.Request(url=url, callback=self.parse_category, dont_filter=True)
           
    def parse_category(self, response):

        print(f'processing main url:{response.url} | # items: {len(response.xpath(self.getAllSubCategoriesXpath))} | total processed item:{self.total_cnt}')
        
        visited = set()

        for i, href in enumerate(response.xpath(self.getAllSubCategoriesXpath)):
            url = response.urljoin(href.extract())

            # print(f'processing sub url is: {url}')
            #if i> 10: break

            if url not in visited:
                visited.add(url)
                yield scrapy.Request(url, callback=self.parse_main_item)

            #yield scrapy.Request(url,callback=self.parse_subcategory, dont_filter=True)
        self.total_cnt += len(response.xpath(self.getAllSubCategoriesXpath))
            
    def parse_main_item(self,response):
        item = Qoo10Item()
        
        # print(f'url:{response.url}')

        title = response.xpath(self.TitleXpath).extract()

        category = response.xpath(self.CategoryXpath).extract()
        
        qna_list = response.xpath(self.QnAXpath).extract()

        review_xpath_list = response.xpath(self.ReviewXpath)

        review_text = self.getReviewText(review_xpath_list)
        QnA_text = self.getQnAText(qna_list)

        # parsing items
        item['Title'] = self.cleanText(title[0])
        item['Category'] = self.cleanText(category[0])
        item['URL'] = response.url
        item['QnA'] = self.cleanText(QnA_text)
        item['Review'] = self.cleanText(review_text)
        
        return item


    # Methods to clean and format text to make it easier to work with later
    def listToStr(self, text_list):
        # dumm = ""
        # MyList = [i.encode('utf-8') for i in MyList]
        #for i in MyList:dumm = "{0}{1}".format(dumm,i)
        return ' '.join(text_list)

    def getReviewText(self, review_xpath_list):
        text=''

        for idx, review in enumerate(review_xpath_list):
            text += f"R{idx}:{review.xpath('string(.)').extract()[0]};\n"

        return text 


    def getQnAText(self,qna_list):
        text=''

        for idx, qna in enumerate(qna_list):
            text +=f'QnA-{idx}:['
            
            soup = BeautifulSoup(qna,'lxml')
            user_list = soup.find_all("div", {"class":"mode_user"})
            sllr_list = soup.find_all("div", {"class":"mode_sllr"})

            min_len = min(len(user_list),len(sllr_list))

            for i in range(min_len):
                Q_text = ''
                A_text = ''

                for q in user_list[i].select("p"):
                    Q_text += str(q)
                for a in sllr_list[i].select("p"):
                    A_text += str(a)
                text += f"\n[Q:{Q_text}]\n[A:{A_text}]"
            text += '];'
        
        return text



    def parseText(self, str):
        soup = BeautifulSoup(str, 'html.parser')
        return re.sub(" +|\n|\r|\t|\0|\x0b|\xa0",' ',soup.get_text()).strip()

    def cleanText(self, text):

        text = re.sub("(<br>|</br>|<br/>|<p>|</p>|\s+|\r|\n)",'',text)
        return text
        # soup = BeautifulSoup(text,'html.parser') 
        # text = soup.get_text()
        # text = re.sub("( +|\n|\r|\t|\0|\x0b|\xa0|\xbb|\xab)+",' ',text).strip()
        # return text