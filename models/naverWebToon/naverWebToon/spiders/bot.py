import scrapy


class BotSpider(scrapy.Spider):
    name = 'bot'
    allowed_domains = ['https://comic.naver.com/webtoon/list?titleId=703846']
    start_urls = [
        'https://comic.naver.com/webtoon/list?titleId=703846/']

    def parse(self, response):
        pass
