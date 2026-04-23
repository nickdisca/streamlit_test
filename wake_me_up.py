from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os
import time

# adapted from https://dev.to/virgoalpha/keeping-your-streamlit-app-awake-using-selenium-and-github-actions-4ajd

# url of the app
STREAMLIT_URL = "https://apptest-mcsmr8krzbi7muc339zkjs.streamlit.app"

def main():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # open the website
        driver.get(STREAMLIT_URL)
        print(f"Opened {STREAMLIT_URL}")

        # setup a waiting time, should be long enough to allow for app to be ready
        wait = WebDriverWait(driver, 30)

        try:
            # Look for the 'keep me up' button
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Yes, get this app back up')]")))
            print("Button found. Clicking...")

            # Do the actual clicking
            button.click()
            # driver.execute_script("arguments[0].click();", button)

            # Check that clicking is successful
            try:
                wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[contains(., 'Yes, get this app back up')]")))
                print("Button clicked and disappeared")

                # seems that we need to wait for some time
                time.sleep(1)

            except TimeoutException:
                print("Button clicked but not disappeared, possible failure")

        except TimeoutException:
            print("Button not found, app awake")

    # cannot access the website
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)

    # after everything, quit
    finally:
        driver.quit()
        print("Script finished")


if __name__ == "__main__":
    main()
