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
from bs4 import BeautifulSoup
import json
import urllib
import urllib.request

def get_source(html):
    soup = BeautifulSoup(html,'html.parser')
    return soup

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
    # browser.find_element_by_xpath("//input[@value='Get Search']").click() 
    # time.sleep(15)
    total = browser.find_elements_by_class_name("sm")
    if len(total) == 0:
        getDetail(browser,img_name)
    else:
        # print(total)
        pass
        
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

# total = browser.find_elements_by_class_name("sm")
pages = browser.find_element_by_xpath("//div[@class='pagination-container']/ul/li[1]/a").text
pagination = pages.split(' ')[3][:-1]
print(pagination)
for page in pagination:
    sms = browser.find_elements_by_xpath("//div[@class='sm']/a")
    for sm in sms: 
        name = sm.text
        path = '/var/www/Python-projects/python-script/download/design/'
        print(sm.text)
        sm.click()
        time.sleep(4)
        soup = get_source(browser.page_source)
        get_data = soup.find("div", {"class": "modal-body"}).findAll("div",{"class":"row"})
        key = []
        value = []
        for data in get_data:
            # a = data.find_all("div",{"class":"col-lg-4"}).text.strip()
            # print('a', a)
            try:
                key.append(data.find("div",{"class":"col-lg-4"}).text.strip())
                value.append(data.find("div",{"class":"col-lg-8"}).text.strip())
            except Exception as e:
                pass

            all_data = dict(zip(key, value))
            tables = soup.find('table',{"class": "table-striped"})
            applicant_data = []
            applicant = {}
            applicant_key = {}
            for table in tables.tbody.find_all('tr'):
                applicant_key['Name']=table.find_all('td')[1].text.strip()
                applicant_key['Address']=table.find_all('td')[2].text.strip()
                applicant_data.append(applicant_key)
            all_data['Applicant'] = applicant_data
            priority_data = []
            priority = {}
            priority_key = {}
            try:
                priroitytable = soup.find(id="tblPCTPriority")
                priority_key['Number']=priroitytable.find('td')[1].text.strip()
                priority_key['Name']=priroitytable.find('td')[2].text.strip()
                priority_key['Date']=priroitytable.find('td')[3].text.strip()
                priority_data.append(priority_key)
            except:
                priority_data = 'Record Not Found !'
            all_data['Priority'] = priority_data

            # cap_img = browser.find_element_by_class_name('img-responsive').screenshot_as_png
            cap_img = browser.find_elements_by_class_name('img-responsive')[1].screenshot_as_png
            # print(cap_img)
            # for img in cap_img:
            #     print(img.get_attribute('src'))
            # src = cap_img[1].get_attribute('src')
            # print(src)
            # urllib.request.urlretrieve(src, "../download/design/" + name+".png")
            # imageStream = io.BytesIO(cap_img)
            # im = Image.open(imageStream)
            # im.save(path+'/'+name,'png')

            with open("%s.json" % name, "w") as outfile: 
                json.dump(all_data, outfile)
        
        print(all_data)
        browser.find_element_by_class_name("btn-warning").click()
    browser.find_element_by_xpath("//li[@class='PagedList-skipToNext']/a").click()
