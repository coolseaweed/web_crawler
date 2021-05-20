from bs4 import BeautifulSoup
import logging

import os, requests, sys
import re

logging.basicConfig(
    format="[%(asctime)s][%(levelname)s]:%(name)s|%(message)s",
    stream=sys.stdout, 
    level=logging.INFO
    )
logger = logging.getLogger(__name__)



def getTextFromQoo10(url, out_fname):

    logger.info('--------------------------------------')
    logger.info(f'TARGET: {url}')
    logger.info(f'OUTPUT: {out_fname}')
    logger.info('--------------------------------------')

    
    main_html = BeautifulSoup(requests.get(url).text,'lxml')
    print(main_html)
    # region_link_list = html_base.find("div", class_="links").find_all("a")
    
    # with open(out_fname,'w') as f_out:

    #     # region fields
    #     total_cnt=0
    #     for region_cnt, region_item in enumerate(region_link_list[:]):
    #         try:
    #             region = region_item.text
    #             region_url = region_item.attrs['href']
    #             region_html = BeautifulSoup(requests.get(region_url).text,'lxml')
    #             city_link_list = region_html.find("div", class_="links").find_all("a")
    #             logger.info(f'processing on .. {region}')

    #             cnt=0
    #             # city fields
    #             for city_cnt, city_item in enumerate(city_link_list[:]):
    #                 try: 
    #                     city = city_item.text
    #                     city_url = region_url+ city_item.attrs['href']
    #                     city_html = BeautifulSoup(requests.get(city_url).text,'lxml')
    #                     dist_link_list = city_html.find("div", class_="links").find_all("a")

    #                     # distric fields
    #                     for dist_cnt, dist_item in enumerate(dist_link_list[:]):
    #                         try:
    #                             dist = dist_item.text
    #                             dist_url = city_url + dist_item.attrs['href']
    #                             dist_html = BeautifulSoup(requests.get(dist_url).text,'lxml')
    #                             out_text=f"{region} {city} {dist}\n"
    #                             f_out.write(out_text)
    #                         except:
    #                             logger.error(f'error got from {dist_url}')
    #                             continue
    #                     cnt += dist_cnt+1
    #                 except:
    #                     logger.error(f'error got from {city_url}')
    #                     continue
    #             logger.info(f'# of addr in {region}: {cnt}')
    #             total_cnt += cnt
    #         except:
    #             logger.error(f'error got from {region_url}')
    #             continue
    #     logger.info("-------------------------------------------")
    #     logger.info(f'# of total address: {total_cnt}')




if __name__ == '__main__':

    url='https://www.qoo10.jp/'

    raw_dir = os.path.join("raw_data","qoo10")
    export_dir = os.path.join("export","qoo10")
    os.makedirs(raw_dir,exist_ok=True)
    os.makedirs(export_dir,exist_ok=True)

    raw_file = os.path.join(raw_dir,"corpus_qoo10.txt")
    out_file = os.path.join(export_dir,"corpus_qoo10.txt")


    getTextFromQoo10(url, raw_file)

