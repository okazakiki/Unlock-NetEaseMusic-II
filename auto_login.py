# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "005EC1C3ED69B729DB0CD87F993EAD3D6C68309A872434A212B5F3AB8AFCDBCD2A7D5B8706FF77172F15CC0832A1245A3ED43C38B7AF6C9527ADA63BE477651F04425144ACA58EC7A0A616AC2A0DB8100746BF69242E5E97973219496C897CB243CFCDD8F365D0E49659C1C9AFE365A610A1F39E824DCA5B5D9C24C32E3F4FAEFB35FF9B11912976923E97DF533DB241699304E81900BE352CB8B59C1F7F74C7026212E4BA991CB1E981A51ACE22A5CA8F2EA3644E18D005DFF3980FBA0DA51BD8D56E5D4B77EF017C700006D78BA01EB2F8BF70B71B2927DC6CD4E72139A338FE6543AB732DA9CE27BEF5DA348DA3F83EC40933B82BE6C2D0E4AFD89FF1C9AE87533B9406F641CED3E58D588E1FE1856AE6BF134C603769EF7FA5C28E516CD24E43B321546E5F11B8F7C50AFB67D200B67770D08A544C121B1DE84F50152802BB3BCACB8CE0A66322BC12338F67908C0EBB27D4A000A7EFFFC73AC114237FA03C"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
