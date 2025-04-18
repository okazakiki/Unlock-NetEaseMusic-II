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
    browser.add_cookie({"name": "MUSIC_U", "value": "00070E47C63DDD2E10C12B72867C42951100E1438D6EF78B1E7988C6D33D70686B512ECE247257D4A6B12FE5E72B61EABF1BA8CC7277D4B2996C8EC7DAA01F239055CE2D8C6E55CCF51F5BC16CB46FFFD2753B63AAB41ED88184B02BEF978F3C058D74DD200EEA3B979280DB50D3F5003AC6B05DEB275A3773E84C7FCBC16F0433B3260E974882847F7B3836E0ACCD45602A469DAA89F479657AA159E02A7ABD56C63160C74EBD355E3AC2E8D46252263C8E5A84F9CAC12B1BB1EC459BF12156F9BD9E2BAEB4139FD061938A928FD3BAC9105AD0F1A4870A2CD8D5C90694D948A8B20602C815863D4D558809A57041DCC2C2D354998090881276F0315F21E11AD3671A1960534B54730C03F9D20939DBA88078AA1F128A90FFD1DC79F8C4A688076A52DA5C19EB8E6AC794E4C32C1FF56C35DFAA516E328509C5A73A7247E26A26EF1E84343EC32EAD0C76049FF70CBA67B6116084599AFC07CDFA99F94B89A898"})
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
