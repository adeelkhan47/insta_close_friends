import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def login_and_verify(driver, username, password):
    # Go to Instagram login page
    driver.get("https://www.instagram.com/accounts/login/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

    # Enter username and password
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    try:
        # Check for Two-Factor Authentication (2FA) prompt
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='verificationCode']")))
        print("Two-Factor Authentication required. Please enter the code sent to your device.")

        # Get the 2FA code from the user
        return 1
    except Exception:
        print("No 2FA required or 2FA process skipped.")

    try:
        # Check for checkpoint (unusual login attempt) challenge
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(text(), 'We Detected An Unusual Login Attempt')]")))
        print("Checkpoint verification required. Requesting verification code via email or phone.")

        # Request verification code (email or phone)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Continue')]"))).click()

        return 2

    except Exception as e:
        print("No checkpoint verification needed.")

    return 0

def login_challenge(driver,code):

    code_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "security_code")))
    code_input.send_keys(code)
    code_input.send_keys(Keys.RETURN)

    # Wait for Instagram home page to load after verification
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Home')]")))
    print("Checkpoint verification complete. Logged in successfully.")
    return True

def login_2fa(driver,code):
    driver.find_element(By.NAME, "verificationCode").send_keys(code)
    driver.find_element(By.NAME, "verificationCode").send_keys(Keys.RETURN)
    print("2FA code entered successfully.")
    return True


def scrape_followers(driver, target_username,limit=10000,scroll_pause_time=3):
    followers = set()
    try:
        driver.get(f"https://www.instagram.com/{target_username}")
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[text()='followers']")))
        time.sleep(2)

        # Open the followers dialog
        followers_link = driver.find_element(By.XPATH, "//a[contains(@href, '/followers')]")
        followers_link.click()
        time.sleep(5)
        count = 1
        followers = set()
        ###
        while True:
            try:
                follower = WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                    (By.XPATH,
                     f"(//span[@class='_ap3a _aaco _aacw _aacx _aad7 _aade'])[{count}]")
                ))
                print(f"Follower {count}: {follower.text}")
                followers.add(follower.text)

                time.sleep(0.5)
                # Scroll to the current element to ensure it's loaded
                # follower_element = driver.find_element(By.XPATH,
                #                                        f"/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{count}]/div/div/div/div[2]/div/div/div/div/div/a/div/div/span")
                driver.execute_script("arguments[0].scrollIntoView(true);", follower)
                count += 1
                if count >= limit+1:
                    break
            except Exception as e:
                logging.exception(e)
                logging.info(e)
                break
        return list(followers)
    except Exception as e:
        logging.info(e)
        return list(followers)

def wait_for_at_least_two_elements(driver, xpath):
    return lambda driver: len(driver.find_elements(By.XPATH, xpath)) >= 2
def add_to_close_friends(driver, friend_username):
    try:

        time.sleep(1)
        xpath = "//div[(contains(@data-bloks-name, 'ig.components.Icon') or contains(@style, 'circle__outline')) and not(contains(@style, 'circle-check__filled'))]"
        elements = WebDriverWait(driver, 3).until(
            wait_for_at_least_two_elements(driver, xpath)
        )
        # Retrieve the first two elements
        record = driver.find_elements(By.XPATH, xpath)[1]
        record.click()
        logging.debug(f"Add {friend_username} to close friend.")
        return True
    except Exception as e:
        logging.error("Failed.")
        logging.exception(e)
        return False
