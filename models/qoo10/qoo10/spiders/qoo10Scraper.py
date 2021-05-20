import scrapy
from bs4 import BeautifulSoup
import re
from qoo10.items import Qoo10Item




class Qoo10scraperSpider(scrapy.Spider):
    name = 'qoo10Scraper'
    allowed_domains = ['www.qoo10.jp']
    start_urls = ['https://www.qoo10.jp/gmkt.inc/Bestsellers/']

    def __init__(self):
        self.declare_xpath()
        
    def declare_xpath(self):

        self.getAllCategoriesXpath = '//*[@id="ul_default_major"]/li/div/div/ul/li/a/@href'
        self.getAllSubCategoriesXpath = '//*[@id="div_gallery_new"]/ul/li/div/div/a/@href'

        self.getAllItemsXpath  = ''
        self.TitleXpath  = '//*[@class="goods_detail"]/h2/text()'
        self.CategoryXpath = '//*[@class="category_depth_list"]/li[5]/span/text()'
        self.QuestionXpath  = '//*[@class="qna_board"]/div[2]//*[@class="row on"]/div[5]/div[2]/div/p[descendant-or-self::text()]'
        self.AnswerXpath  = '//*[@class="qna_board"]/div[2]//*[@class="row on"]/div[6]/div[2]/div/p[descendant-or-self::text()]'


        #/html/body/div[3]/div[3]/div[1]/div/div/div[4]/div[5]/div/div[1]/div[3]/div[2]
        # /html/body/div[3]/div[3]/div[1]/div/div/div[4]/div[5]/div/div[1]/div[3]/div[2]/div[5]/div[5]/div[2]/div/p
        # /html/body/div[3]/div[3]/div[1]/div/div/form/div[2]/div[1]/div/ul/li[5]

        # self.CategoryXpath = "/html/body/div[3]/div[3]/div[1]/div/div/div[4]/div[3]/div[1]/table/tbody"
        # self.PriceXpath = "/html/body/div[3]/div[3]/div[1]/div/div/form/div[2]/div[2]/div[2]/ul/li[1]/div/dl/dd"
        # self.FeaturesXpath = ""
        # self.DescriptionXpath = ""
        # self.SpecsXpath = ""

    def parse(self, response):

        for i, href in enumerate(response.xpath(self.getAllCategoriesXpath)):
            url = response.urljoin(href.extract())
            # print(f'processing main url is: {url}')
            # print('-------------')
            if i> 1: break
            yield scrapy.Request(url=url, callback=self.parse_category, dont_filter=True)
           
    def parse_category(self,response):
        visited = set()
        for i, href in enumerate(response.xpath(self.getAllSubCategoriesXpath)):
            url = response.urljoin(href.extract())
            # print(f'processing sub url is: {url}')
            if i> 3: break
            if url not in visited:
                visited.add(url)
                yield scrapy.Request(url, callback=self.parse_main_item)
            #yield scrapy.Request(url,callback=self.parse_subcategory, dont_filter=True)

    # def parse_subcategory(self,response):
    #     for href in response.xpath(self.getAllItemsXpath):
    #         url = response.urljoin(href.extract())
            #yield scrapy.Request(url,callback=self.parse_main_item)
            
    def parse_main_item(self,response):
        item = Qoo10Item()
        
        print(f'url:{response.url}')

        title = response.xpath(self.TitleXpath).extract()

        category = response.xpath(self.CategoryXpath).extract()
        
        question_list = response.xpath(self.QuestionXpath).extract()

        answer_list = response.xpath(self.AnswerXpath).extract()

        print(f"Q:{question_list}\nA:{answer_list}\nlength: Q-{len(question_list)} A-{len(answer_list)}")

        # parsing items
        item['Title'] = title
        item['Category'] = self.cleanText(category[0])
        item['URL'] = response.url
        item['Question'] = self.cleanText(self.listToStr(question_list))
        item['Answer'] = self.cleanText(self.listToStr(answer_list))


        # temp = self.listToStr(question_list)
        # print(temp)
        # temp = self.cleanText(temp)
        # print(temp)
        #Title = self.cleanText(self.parseText(self.listToStr(Title)))
 
        # Category = response.xpath(self.CategoryXpath).extract()
        # Category = self.cleanText(self.parseText(Category))
 
        # Price = response.xpath(self.PriceXpath).extract()
        # Price = self.cleanText(self.parseText(self.listToStr(Price)))
 
        # Features = response.xpath(self.FeaturesXpath).extract()
        # Features = self.cleanText(self.parseText(self.listToStr(Features)))
 
        # Description = response.xpath(self.DescriptionXpath).extract()
        # Description = self.cleanText(self.parseText(self.listToStr(Description)))

        # Specs = response.xpath(self.SpecsXpath).extract()
        # Specs = self.cleanText(self.parseText(Specs))

        #Put each element into its item attribute.
        #item['Title'] = Title
        # item['Category'] = Category
        # item['Price'] = Price
        # item['Features'] = Features
        # item['Description'] = Description
        # item['Specs'] = Specs
        
        return item


    # Methods to clean and format text to make it easier to work with later
    def listToStr(self, text_list):
        # dumm = ""
        # MyList = [i.encode('utf-8') for i in MyList]
        #for i in MyList:dumm = "{0}{1}".format(dumm,i)
        return ' '.join(text_list)

    def parseText(self, str):
        soup = BeautifulSoup(str, 'html.parser')
        return re.sub(" +|\n|\r|\t|\0|\x0b|\xa0",' ',soup.get_text()).strip()

    def cleanText(self, text):

        text = re.sub("(<br>|</br>|<p>|</p>|\s+|\r|\n)",'',text)
        return text
        # soup = BeautifulSoup(text,'html.parser') 
        # text = soup.get_text()
        # text = re.sub("( +|\n|\r|\t|\0|\x0b|\xa0|\xbb|\xab)+",' ',text).strip()
        # return text