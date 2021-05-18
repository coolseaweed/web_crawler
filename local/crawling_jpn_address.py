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

addr = {}
pattern01 = re.compile(r'([\S]+)\／([\S]+)（([\S]+)\／([\S]+)）')
pattern02 = re.compile(r'([一-龯ぁ-ん０-９々モエヱケタクロミノツハ\／\（\）]+\／[一-龯ぁ-ん０-９々モエヱケタクロミノツハ\／\（\）]+)\（([ァ-ン０-９\／\（\）]+\／[ァ-ン０-９\（\）]+)）')
pattern03 = re.compile(r'([\S]+)（([\S]+)）（([\S]+)（([\S]+)））')
pattern04 = re.compile(r'([\S]+)（([\S]+)）')

def verify_text(line):

    output={}
    for i, word in enumerate(line.strip().split()):

        output[f'field{i}'] = set()
        if pattern01.fullmatch(word):
            if pattern02.fullmatch(word):
                group1 = pattern02.sub(r'\1',word)
                group2 = pattern02.sub(r'\2',word)

                # print(f"input_raw:{line}")
                # print(f"processing_line:{word}")
                # print(f":{group1} | {group2}")
                # print('--------------------------------')
                for item in zip(group1.split('／'),group2.split('／')):
                    kanji, kana = item
                    if pattern04.fullmatch(kanji):
                        kanji = pattern04.sub(r'\1',kanji)
                    if pattern04.fullmatch(kana):
                        kana = pattern04.sub(r'\1',kana)
                    output[f'field{i}'].add(f"{kanji}（{kana}）")
            else:
                logger.info(f"edge case detacted: {word}")
        else:
            if pattern03.fullmatch(word):
                group1 = pattern03.sub(r'\1',word)
                group2 = pattern03.sub(r'\3',word)
                # print(f"processing_line:{word}")
                # print(f":{group1} | {group2}")
                # print('--------------------------------')
                word=f"{group1}（{group2}）"
            output[f'field{i}'].add(word)
    
    output_text=''
    for field0 in output['field0']:
        for field1 in output['field1']:
            for field2 in output['field2']:
                output_text += f"{field0} {field1} {field2}\n"

    return output_text




def getTextFromJpnPost(url, out_fname):

    logger.info('--------------------------------------')
    logger.info(f'TARGET: {url}')
    logger.info(f'OUTPUT: {out_fname}')
    logger.info('--------------------------------------')

    
    html_base = BeautifulSoup(requests.get(url).text,'lxml')
    region_link_list = html_base.find("div", class_="links").find_all("a")
    
    with open(out_fname,'w') as f_out:

        # region fields
        total_cnt=0
        for region_cnt, region_item in enumerate(region_link_list[:]):
            try:
                region = region_item.text
                region_url = region_item.attrs['href']
                region_html = BeautifulSoup(requests.get(region_url).text,'lxml')
                city_link_list = region_html.find("div", class_="links").find_all("a")
                logger.info(f'processing on .. {region}')

                cnt=0
                # city fields
                for city_cnt, city_item in enumerate(city_link_list[:]):
                    try: 
                        city = city_item.text
                        city_url = region_url+ city_item.attrs['href']
                        city_html = BeautifulSoup(requests.get(city_url).text,'lxml')
                        dist_link_list = city_html.find("div", class_="links").find_all("a")

                        # distric fields
                        for dist_cnt, dist_item in enumerate(dist_link_list[:]):
                            try:
                                dist = dist_item.text
                                dist_url = city_url + dist_item.attrs['href']
                                dist_html = BeautifulSoup(requests.get(dist_url).text,'lxml')
                                out_text=f"{region} {city} {dist}\n"
                                f_out.write(out_text)
                            except:
                                logger.error(f'error got from {dist_url}')
                                continue
                        cnt += dist_cnt+1
                    except:
                        logger.error(f'error got from {city_url}')
                        continue
                logger.info(f'# of addr in {region}: {cnt}')
                total_cnt += cnt
            except:
                logger.error(f'error got from {region_url}')
                continue
        logger.info("-------------------------------------------")
        logger.info(f'# of total address: {total_cnt}')




if __name__ == '__main__':

    url='https://japan-postcode.810popo.net/ja/'

    raw_dir = os.path.join("raw_data","address")
    export_dir = os.path.join("export","address")
    print(raw_dir)
    os.makedirs(raw_dir,exist_ok=True)
    os.makedirs(export_dir,exist_ok=True)

    raw_file = os.path.join(raw_dir,"corpus_address.txt")
    out_file = os.path.join(export_dir,"corpus_address.txt")

    #getTextFromJpnPost(url, raw_file)

    with open (raw_file,'r') as f_in, open(out_file,'w') as f_out:
        cnt = 0
        for line in f_in:
            line = verify_text(line)

            f_out.write(line)
            cnt +=1

            #if cnt > 500: break
            if cnt % 1000 == 0:
                logger.info(f'progressed line num: {cnt}')
                
    logger.info('done!')

