from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 
import csv
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import pytesseract
from PIL import Image 
import re
import io
import urllib.request
import cv2
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getDetail(browser,img_name):
    browser.find_element_by_xpath("//select[@name='ddlsearchoptioncell0']/option[text()='DATE OF FILING']").click()
    time.sleep(1)
    browser.find_element_by_xpath("//select[@name='ddltypeofserch0']/option[text()='Greater Than']").click()
    time.sleep(1)
    browser.find_element_by_id("textfieldnumbersnew0").send_keys('01/01/2020')
    time.sleep(1)
    browser.find_element_by_xpath("//select[@name='ddlsearchoptioncell1']/option[text()='DATE OF FILING']").click()
    time.sleep(1)
    browser.find_element_by_xpath("//select[@name='ddltypeofserch1']/option[text()='Less Than']").click()
    time.sleep(1)
    browser.find_element_by_id("textfieldnumbersnew1").send_keys('01/01/2021')
    time.sleep(1)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    cap_img = browser.find_element_by_id('Captcha').screenshot_as_png
    imageStream = io.BytesIO(cap_img)
    im = Image.open(imageStream)
    im.save(img_name,'png')
    img = cv2.imread(img_name, 0) 
    ret,thresh = cv2.threshold(img,55,255,cv2.THRESH_BINARY)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT,(2,2)))
    cv2.imwrite('captcha.png', opening)
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    cap_text = pytesseract.image_to_string(Image.open(img_name),lang='eng')
    print(cap_text)
    text = browser.find_element_by_id('CaptchaText')
    text.clear()
    text.send_keys(cap_text)
    time.sleep(5)
    # browser.find_element_by_class_name('pull-left').click()
    browser.find_element_by_xpath("//input[@value='Get Search']").click() 
    time.sleep(5)
    try:
        time.sleep(5)
        print('hiiiiiiiiiiiii')
        total = browser.find_element_by_xpath("//div[@id='hidemeForDisplayChallan']/section/div/div[@class='row']").text
        # total = browser.findElement(By.partialLinkText ("Page 1 of")).text;
        print(total)
        # a=browser.find_element_by_class_name("pagination-container")
        # total = browser.find_element_by_partial_link_text("Page 1 of").text
        print("tryyyyyy")
        # return a

    except Exception as e:
        print(e)
        getDetail(browser,img_name)
    # return cap_text

options = Options()         
options.add_argument("--start-maximized")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("--remote-debugging-port=9222")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--silent")

browser = webdriver.Chrome('/var/www/Python-projects/python-script/chromedriver', options=options)

browser.get('https://ipindiaservices.gov.in/designsearch/')
time.sleep(3)
getDetail(browser, "captcha.png")
time.sleep(5)
# total = browser.find_element_by_xpath("//div[contains(text(), 'Total Document(s):')]").text
total = browser.find_element_by_xpath("//div[@id='hidemeForDisplayChallan']/section/div/div/ul/li[1]/a").text
# total = browser.find_element_by_partial_link_text("Page 1 of").text
print(total)