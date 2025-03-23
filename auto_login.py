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
    browser.add_cookie({"name": "MUSIC_U", "value": "00841A2C1A05D93377CD3DBA1546C40417F4B09DC2D687E8D9263B53CBB57585C4BDF092DE005F3D2595781E0F6AA15C41DC87F7766A5EF78F13FA096972AEF283C83598E39531067C839AE86FE9ED2E080A8D3F8F3EF8221B2C08BF0FD2B0F5D5B6ED751A7694F96004F3EB2EC87C62BA867EA1873BDADBE104AFAC900EAD433A3DB2122622B2DC57A5E4C8D7506FE8F73CCB023035E834B85ADD404C0BC7DAB31C5B69170C6049BFEFF3F5CB9AFB6E6612E07A01930F903D1347809E752A6D85792EE67144B81C15F5E6EF0719A10427496B02E824814459563ED0FF26F5CCF13A94948AED2006DC3CF2122EA65F35B36DD955A4AAF19F6A6977F8C66F97DA0AF90EA405DAB026B8ACD245DCE44FFDFC35C078EA47070F1F518A551B07D53AEED5B70B70659242F1E0416DDA36598869129B02204BCCDAE0FEDD19532898D6BA469723C1800184219E84FDCB92B928955966F2F26E2DCBA99389AA357B23A353"})
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
