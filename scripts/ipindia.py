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
import numpy



def getDetail(browser,img_name):
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
	browser.find_element_by_id('CaptchaText').send_keys(cap_text)
	time.sleep(5)
	browser.find_element_by_name('submit').click()
	time.sleep(5)
	try:
		browser.find_element_by_name('ApplicationNumber')
		# time.sleep(5)
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

browser.get('https://ipindiaservices.gov.in/PublicSearch')
startingdate = browser.find_element_by_id("FromDate")
startingdate.send_keys('01/01/1800')
enddate = browser.find_element_by_id("ToDate")
enddate.send_keys('12/29/2020')

# browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

getDetail(browser,'captcha.png')

# a = browser.findElements(By.xpath("//*[contains(text(),'Total Document(s): 624074')]"))
# print(a)

browser.quit()