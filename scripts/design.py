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

def getDetail(browser,img_name):
    try:
        browser.find_element_by_xpath("//select[@name='ddlsearchoptioncell0']/option[text()='DATE OF FILING']").click()
        browser.find_element_by_id("textfieldnumbersnew0").send_keys('09/03/2020')
        browser.find_element_by_xpath("//select[@name='ddlandor0']/option[text()='OR']").click()
    except:
        print("222222222") 
        return None
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
    browser.find_element_by_class_name('pull-left').click()
    time.sleep(5)
    try:
        browser.find_element_by_class_name('box-header')
    except Exception as e:
        getDetail(browser,img_name)
    return cap_text

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
# browser.find_element_by_xpath("//select[@name='ddlsearchoptioncell0']/option[text()='DATE OF FILING']").click()
# browser.find_element_by_id("textfieldnumbersnew0").send_keys('09/03/2020')
# browser.find_element_by_xpath("//select[@name='ddlandor0']/option[text()='OR']").click()
# browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
img = browser.find_element_by_id("Captcha")
getDetail(browser, "captcha.png")