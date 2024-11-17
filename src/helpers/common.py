import logging
import logging
import re

import pytesseract
from PIL import Image
from deathbycaptcha import deathbycaptcha
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def extract_using_GBC(path):
    username = "adeelkhan47"
    password = "Adeelk47!"

    # Initialize the client with your credentials
    client = deathbycaptcha.SocketClient(username, password)
    try:
        # Get your current balance
        # balance = client.get_balance()
        # print(f"Current Balance: {balance}")

        # Send the CAPTCHA for solving
        captcha = client.decode(path, timeout=60)  # Increased timeout for better chance of accurate solution
        if captcha:
            # The CAPTCHA was solved
            print(f"CAPTCHA {captcha['captcha']} solved: {captcha['text']}")
            return captcha['text']
        else:
            print("CAPTCHA was not solved")
            return "0000"

    except deathbycaptcha.AccessDeniedException as e:
        print(f"Access denied: {e}")
        return "0000"
    except Exception as e:
        # Handle any other errors that might occur
        logging.exception(f"An error occurred: {e}")
        return "0000"


def close_and_quit_driver(driver):
    try:
        driver.close()
    except Exception as e:
        print("Error while closing the browser:", e)

    try:
        driver.quit()
    except Exception as e:
        print("Error while quitting the driver:", e)


def extract_text_from_image(image_path):
    """
    Extract text from an image using Tesseract OCR.

    Args:
    - image_path (str): path to the image from which text needs to be extracted

    Returns:
    - str: extracted text from the image
    """
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, config='outputbase digits')
    numeric_text = ''.join(re.findall(r'\d', text))

    if not numeric_text:
        return 0000

    return numeric_text


def get_mac_chrome_driver():
    options = ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    path_to_driver = ChromeDriverManager().install()
    driver = webdriver.Chrome(options=options)
    return driver


def get_ubuntu_chrome_driver() -> object:
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
        return driver

    except Exception as e:
        logging.exception(f"Error occurred while getting Chrome driver: {e}")
        return None
