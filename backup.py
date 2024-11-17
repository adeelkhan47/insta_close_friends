import instaloader

import time
def login_with_2fa(username, password):
    # Initialize Instaloader instance
    loader = instaloader.Instaloader()

    # Attempt to log in
    try:
        loader.login(username, password)
        print("Login successful!")
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        print("2FA required! Please enter the 2FA code sent to your device:")
        two_factor_code = input("Enter 2FA code: ")
        try:
            loader.two_factor_login(two_factor_code)
            print("2FA verification successful!")
        except Exception as e:
            print("Failed to verify 2FA code:", e)
            return None

    return loader


def get_followers(loader, target_username):
    # Load profile
    profile = instaloader.Profile.from_username(loader.context, target_username)

    # Fetch followers
    followers = []
    for follower in profile.get_followers():
        followers.append(follower.username)
        print(f"Follower: {follower.username}")

    return followers


# Replace 'your_username' and 'your_password' with your actual Instagram login details
username = 'louie_the_lion'
password = 'Adeel1!'
# username = 'bf__lahore1'
# password = 'Ahmad47!'
loader = login_with_2fa(username, password)
followers = []
#
if loader:
#     # Replace 'your_username' with the account whose followers you want to fetch
    followers = get_followers(loader, username)
    print(f"Total Followers: {len(followers)}")
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login_to_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

    # Enter username and password
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    time.sleep(2)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    # Wait for login to complete
    time.sleep(5)
    print("Logged in successfully.")


def add_to_close_friends(driver, friend_username):
    time.sleep(2)
    driver.get("https://www.instagram.com/accounts/close_friends/")
    ""

    search_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
    )
    search_input.send_keys("adeelkhan6568")
    search_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[3]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div"))
    )
    search_input.click()


    # Go to the user's profile
#     time.sleep(2)
#     driver.get(f"https://www.instagram.com/{friend_username}/?next=%2F")
#     try:
#         following = WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Following')]")))
#     except:
#         following = None
#         print(f"Not following - {friend_username}.")
#     if following:
#         following.click()
#         try:
#             close_friend_button = WebDriverWait(driver, 5).until(
#                 EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Add to close friends list')]"))
#             )
#         except:
#             close_friend_button = None
#             print(f"Already Close Friend - {friend_username}.")
#         if close_friend_button:
#             close_friend_button.click()
#             print(f"Added {friend_username} to Close Friends.")
#
#
# # Replace these with your Instagram credentials
# username = 'bf__lahore1'
# password = 'Ahmad47!'

# Set up the Chrome driver
driver = webdriver.Chrome()  # Or path to your chromedriver if not in PATH
driver.implicitly_wait(10)

try:
    # login_to_instagram(driver, username, password)
    print("a")
    # add_to_close_friends(driver, "each")
    # for each in followers:
    #     add_to_close_friends(driver, each)
finally:
    driver.quit()
