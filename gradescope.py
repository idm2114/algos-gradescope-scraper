#!/usr/bin/env python
# written by Ian Macleod : March 17 2021
# to run this script, first install chromedriver or firefox driver
# to your local path, ex. /usr/local/bin

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from datetime import datetime, timedelta
import os
import time
import pytz

GRADESCOPE_USERNAME = ''
GRADESCOPE_PASSWORD = ''
## this is currently hardcoded, would be much cooler if dynamic
## but having trouble parsing quizzes that are incomplete on selenium
LAST_NUM_QUIZZES = 11

## note that this is designed for MAC OSX 
## could easily be modified to send emails with SMTP for windows users
## or something else entirely (don't know about windows development)

def notify(title, text): 
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

def run_selenium():
    #selenium #runs in background 
    driver=webdriver
    try:
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless()
        driver = webdriver.Firefox(options=fireFoxOptions)
    except:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.gradescope.com")
#print(driver.title)

    search = driver.find_element_by_xpath('//button[text()="Log In"]')
    search.click()

    time.sleep(2)

    email = driver.find_element_by_name('session[email]')
    email.send_keys(GRADESCOPE_USERNAME)
    password = driver.find_element_by_name('session[password]')
    password.send_keys(GRADESCOPE_PASSWORD)

    search = driver.find_element_by_name('commit')
    search.click()

    time.sleep(5) #waiting for new page to load

    getclass = driver.find_element_by_xpath('//*[text() = "Analysis of Algorithms I"]')
    getclass.click()

    quizzes = driver.find_elements_by_xpath('//*[contains(text(), "Quiz")]')
    if len(quizzes) < LAST_NUM_QUIZZES:
        # send alert
        notify("ALGOS QUIZ WARNING", "NEW ALGOS QUIZ -- DO READING NOW!")
        LAST_NUM_QUIZZES = LAST_NUM_QUIZZES + 1
    time.sleep(5)

    driver.close()

def main():
    # the script checks at a decreasing interval as we get 
    # closer to the day of class
    while(1):
        tz = pytz.timezone('US/Eastern')
        current = datetime.now(tz=tz)
        if current.weekday() == 6 or current.weekday() == 1:
            if current.hour <= 20: 
                run_selenium()
                time.sleep(3600)
            else:
                run_selenium()
                time.sleep(30 * 60)
        elif current.weekday() == 0 or current.weekday() == 2:
            if current.hour <= 10:
                run_selenium()
                time.sleep(5*60)
            else:
                print("class has passed")
                time.sleep(3600)
        else:
            print("waiting for day to be closer to class day...")
            time.sleep(3600)

if __name__ == '__main__':
    main() 
