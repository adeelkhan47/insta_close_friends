import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import instaloader

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
        two_factor_code = input("Enter the 2FA code: ")
        driver.find_element(By.NAME, "verificationCode").send_keys(two_factor_code)
        driver.find_element(By.NAME, "verificationCode").send_keys(Keys.RETURN)
        print("2FA code entered successfully.")

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

        # Wait for user to input the received verification code
        verification_code = input("Enter the verification code sent to your phone or email: ")
        code_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "security_code")))
        code_input.send_keys(verification_code)
        code_input.send_keys(Keys.RETURN)

        # Wait for Instagram home page to load after verification
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Home')]")))
        print("Checkpoint verification complete. Logged in successfully.")

    except Exception as e:
        print("No checkpoint verification needed.")

    return True

def scrape_followers(driver, target_username,scroll_pause_time=3):
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
                # Locate the follower by dynamic XPath
                follower = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                    (By.XPATH,
                     f"/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{count}]/div/div/div/div[2]/div/div/div/div/div/a/div/div/span")
                ))

                print(f"Follower {count}: {follower.text}")
                followers.add(follower.text)

                time.sleep(0.5)
                # Scroll to the current element to ensure it's loaded
                # follower_element = driver.find_element(By.XPATH,
                #                                        f"/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{count}]/div/div/div/div[2]/div/div/div/div/div/a/div/div/span")
                driver.execute_script("arguments[0].scrollIntoView(true);", follower)
                count += 1

            except Exception as e:
                # print(f"Error at count {count}: {e}")
                break

        ###
        # count  = 1
        # followers = set()
        # while True:
        #     try:
        #         follower = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
        #                                                                          f"/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{count}]/div/div/div/div[2]/div/div/div/div/div/a/div/div/span"))).text
        #         print(follower)
        #         followers.add(follower)
        #         count += 1
        #     except Exception:
        #         break
        # Scroll and load more followers
        # last_height = driver.execute_script("return arguments[0].scrollHeight", followers_list)
        # followers = set()  # Use a set to avoid duplicates
        #
        # while True:
        #     # Scroll to the end of the follower list
        #     driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_list)
        #     time.sleep(1)  # Wait for more followers to load
        #
        #     # Extract follower usernames
        #     followers_elements = driver.find_elements(By.CLASS_NAME, '_ap3a _aaco _aacw _aacx _aad7 _aade')
        #     for elem in followers_elements:
        #         followers.add(elem.text())  # Add only the username
        #
        #     # Check if more followers loaded
        #     new_height = driver.execute_script("return arguments[0].scrollHeight", followers_list)
        #     if new_height == last_height:
        #         break
        #     last_height = new_height
        return list(followers)
    except Exception:
        return []
def add_to_close_friends(driver, friend_username):
    time.sleep(2)
    driver.get("https://www.instagram.com/accounts/close_friends/")
    ""

    search_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
    )
    search_input.send_keys(friend_username)
    try:
        records = WebDriverWait(WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "wbloks_1"))), 5).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains(@style, 'circle__outline') or contains(@style, 'search__outline')]")
            )
        )
        if len(records) > 1:
            print(f"Add {friend_username} to close friend.")
            records[1].click()
    except:
        print("Already close friend.")
    # WebDriverWait(driver, 5).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "wbloks_1")))
    # search_input = WebDriverWait(driver, 5).until(
    #     EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[3]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div"))
    # )
    # search_input.click()


# Replace these with your Instagram credentials
# username = "michaelangelogerardi"
# password = "Adeel123!"
username = "louie_the_lion"
password = "Adeel1!"
# username = "adeelkhan_47"
# password = "Mazink47!"
# username = "bf__lahore1"
# password = "Ahmad47!"

# Set up the Chrome driver
driver = webdriver.Chrome()  # Or path to your chromedriver if not in PATH
driver.implicitly_wait(5)

try:
    if login_and_verify(driver, username, password):
        followers = scrape_followers(driver,username)
        print(len(followers))
        for each in followers:
            time.sleep(1)
            add_to_close_friends(driver, each)
finally:
    driver.quit()
