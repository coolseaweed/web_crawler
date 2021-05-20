from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import time

CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
WINDOW_SIZE = '1920,1080'
URL="https://www.qoo10.jp/cat/100000001/200000004"

def test01():

    driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', DesiredCapabilities.CHROME)
    driver.get(URL)

    print(driver.page_source)

def test02():


    chrome_options = Options()
    chrome_options.add_argument( "--headless" )
    chrome_options.add_argument( "--no-sandbox" )
    chrome_options.add_argument( "--disable-gpu" )
    chrome_options.add_argument( f"--window-size={ WINDOW_SIZE }" )
    
    driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options )
    SCROLL_PAUSE_TIME = 0.5
    driver.get(URL)

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height    

    print(driver.page_source)

test02()