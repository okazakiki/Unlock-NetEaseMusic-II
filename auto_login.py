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
    browser.add_cookie({"name": "MUSIC_U", "value": "00FDB4DE0DDB763D4F31BEF4AB1C644EEA3FCD62592731F97F6BB9233E30BE4C255D926117F13CB2276FF35C75F0388D4F53D096EF9DCD17D568518AE6D76B442AD0AE68ADE40650F87496759707BE5DC3B923C36E9C258BAF7717D1114452204F85AB938A69044B33E5D76E5C18ED2403771E86376F5032E7B549B11683544620DBE8D5051383A37FF746CE8ADCA14A7EBF581CE16432CF95F89E00A93A21EA92C6B8186457AD8CEA87EDC9C2A94E1F273421408291CA43B53ACA7CAD5120CB288BA55D85CA4ECE296894C91DBD45DB0DCA0203972D211D39B565DE13CA6F15030DE888E3532FFAD31DA5E85BFE99D8A3AB9E1C86E1FF253C6D9EC57BD6CD50EE4A92DCC53B3D8E52CA0355E32C0E61B2A749B1AB3139101249D106304327C42C241B5FF3AAFC7F8AED4763D657C7631FE604746361432E4FD19B8A04041A0508475F84F0CC05E7348A8CCA2ADB5313E19E1E86CAC50AFD046F8196499632AD1F"})
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
