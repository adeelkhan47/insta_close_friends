import logging
import time

from selenium.common import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers.common import get_mac_chrome_driver

def slow_scroll_to_bottom(driver, scroll_pause_time=1, scroll_increment=500, max_attempts=10):
    last_height = driver.execute_script("return document.body.scrollHeight")
    attempts = 0

    while True:
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return window.pageYOffset + window.innerHeight")
        current_scroll_height = driver.execute_script("return document.body.scrollHeight")

        if new_height >= current_scroll_height:
            break

        if last_height == current_scroll_height:
            attempts += 1
            if attempts >= max_attempts:
                break
        else:
            attempts = 0
        last_height = current_scroll_height

def beverlyonescottsdalFloorPlan00908():
    print("beverlyonescottsdalFloorPlan00908_in")
    data = []
    driver = get_mac_chrome_driver()
    wait = WebDriverWait(driver, 10)  # increase wait time to handle loading
    try:
        url = f"https://thebeverlyonescottsdale.com/floorplans/"
        driver.get(url)

        element = wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()="Floorplans"]')))
        element.click()
        slow_scroll_to_bottom(driver)
        items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "floorplan-listing__item")))
        time.sleep(1)
        for item in items:
            # Extract the name
            name = item.find_element(By.CLASS_NAME, "floorplan-listing__title").text.strip()
            print(f'{name}-processed')
            img_url = item.find_element(By.CLASS_NAME, "floorplan-listing__image").get_attribute("src")
            spans = item.find_elements(By.CSS_SELECTOR, ".floorplan-listing__info--wrap span")
            floorplan_details = [span.text.strip() for span in spans]
            if len(floorplan_details) >= 3:
                floorplan_type = floorplan_details[0]
                bath_count = floorplan_details[1]
                size = floorplan_details[2]
            else:
                floorplan_type = bath_count = size = "N/A"
            price = item.find_element(By.CLASS_NAME, "floorplan-listing__info--price").text.strip()
            driver.execute_script("arguments[0].scrollIntoView(true); window.scrollBy(0, -100);", item)
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable(item))
            try:
                item.click()
            except ElementClickInterceptedException:
                print(f"Click intercepted on item {name}. Retrying after scrolling.")
                driver.execute_script("arguments[0].scrollIntoView(true); window.scrollBy(0, -100);", item)
                time.sleep(1)  # Give the UI a bit of time to adjust
                item.click()
            availability = ""
            booking_link = ""
            tour_link = "https://thebeverlyonescottsdale.com/schedule-a-tour/"
            try:
                time.sleep(1)
                # slow_scroll_to_bottom(driver)
                wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='page']/div/div[1]/div[2]/ul/li[2]/button/span"))).click()
                # time.sleep(1)
                time.sleep(1)
                table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "check-availability__table")))
                time.sleep(1)
                rows = table.find_elements(By.CLASS_NAME, "check-availability__row")
                time.sleep(1)
                if rows:
                    first_row = rows[1]
                    availability_date = WebDriverWait(first_row, 3).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "check-availability__cell--availability"))).text.strip()
                    link_element = WebDriverWait(first_row, 3).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "check-availability__cell-links"))
                    )
                    a_tag = link_element.find_element(By.TAG_NAME, "a")

                    # Extract the 'href' attribute from the 'a' tag
                    link = a_tag.get_attribute("href")
                    booking_link = link.replace("&MoveInDate={date}","")
                    availability = availability_date
                else:
                    availability = "N/A"

            except Exception as e:
                logging.exception(e)
                availability = "-------"
            data.append({
                "name": name,
                "img_url": img_url,
                "size": size,
                "type": floorplan_type,
                "bath_count": bath_count,
                "price": price,
                "availability": availability,
                "booking_link":booking_link,
                "book_tour":tour_link
            })
            for each in data:
                print(each)
            time.sleep(1)
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="floorplan-modal"]/div/div/a')))
                driver.execute_script("arguments[0].scrollIntoView(true); window.scrollBy(0, -100);", element)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element))

                try:
                    # Try clicking the element
                    element.click()
                except ElementClickInterceptedException:
                    print("Click intercepted. Retrying after scrolling.")
                    driver.execute_script("arguments[0].scrollIntoView(true); window.scrollBy(0, -100);", element)
                    time.sleep(1)  # Pause to allow the view to adjust
                    element.click()

            except TimeoutException:
                print("Timeout: Could not find or click the element.")
            except Exception as e:
                print(f"An error occurred: {e}")
            ###


            # Print or return the data
        return data
    except Exception as e:
        logging.exception(e)
        print("lol")

    finally:
        driver.quit()

def smbhollywoodFloorPlan_00876():
    data = []
    driver = get_mac_chrome_driver()
    wait = WebDriverWait(driver, 10)  # increase wait time to handle loading
    try:
        url = f"https://smbhollywood.securecafe.com/onlineleasing/smb-hollywood/floorplans/"
        driver.get(url)
        slow_scroll_to_bottom(driver)
        section = wait.until(EC.presence_of_element_located((By.ID, "floorplanCards")))
        cards = WebDriverWait(section, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "fp-card")))
        count = 0
        book_tour = "https://www.smbhollywood.com/scheduletour"

        for each in cards:
            fp_name = each.find_element(By.CLASS_NAME, 'fp-description.fp-name').text
            fp_sqft = each.find_element(By.CSS_SELECTOR, f'[data-selenium-id="FPsqft_{count}"]').text
            bed_bath_info = each.find_element(By.CSS_SELECTOR, f'[data-selenium-id="FPType_{count}"]').text.strip()
            price = each.find_element(By.CLASS_NAME, 'amount').text
            mage_element = each.find_element(By.CSS_SELECTOR, 'img[min-width="400"]')
            img_src = mage_element.get_attribute('data-src')
            img_src = f"https://cdngeneral.rentcafe.com/{img_src}"
            booking_link = f"https://smbhollywood.securecafe.com/onlineleasing/smb-hollywood/floorplans/{fp_name.lower()}"
            count+=1
            # each.click()
            print(f"Floorplan Name: {fp_name}, Size: {fp_sqft}, Typs: {bed_bath_info}, Price: {price}, Image:{img_src},book_tour:{booking_link}")
    except Exception as e:
        logging.exception(e)
        print("failed")
    finally:
        driver.quit()
