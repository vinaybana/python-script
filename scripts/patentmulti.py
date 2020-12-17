from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time 
import csv
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import pytesseract
from PIL import Image 
import re
import io
import cv2
import numpy
import json
from bs4 import BeautifulSoup
import pyautogui
import os, sys
import datetime
from datetime import timedelta
from queue import *
from threading import Thread

concurrent = 2
que = Queue(concurrent*1)

def get_source(html):
	soup = BeautifulSoup(html,'html.parser')
	return soup

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
	browser.find_element_by_id('CaptchaText').send_keys(cap_text)
	try:
		browser.find_element_by_name('submit').click()
	except:
		return cap_text
	time.sleep(3)
	try:
		time.sleep(3)
		browser.find_element_by_id('tableData')
	except Exception as e:
		getDetail(browser,img_name)


def DataProcess():
	while True:
		param = que.get()
		options = Options()			
		# options.add_argument("--start-maximized")
		# options.add_argument('--ignore-certificate-errors')
		# options.add_argument('--ignore-ssl-errors')
		# options.add_argument("--remote-debugging-port=9222")
		# options.add_experimental_option('excludeSwitches', ['enable-logging'])
		# options.add_argument("--silent")
		browser = webdriver.Chrome('/var/www/Python-projects/python-script/chromedriver', options=options)
		browser.get('https://ipindiaservices.gov.in/PublicSearch')
		startingdate = browser.find_element_by_id("FromDate")
		startingdate.send_keys(param['starting_date'])
		enddate = browser.find_element_by_id("ToDate")
		enddate.send_keys(param['end_date'])
		getDetail(browser,'captcha.png')
		time.sleep(3)
		a =	browser.find_element_by_xpath("//p[contains(text(), 'Total Document(s):')]").text
		total_count = a.split(' ')[2]
		rows = len(browser.find_elements_by_xpath("//table/tbody/tr"))
		total_page = (int(total_count)//int(rows))+1

		try:
			for i in range(total_page):
				trs = browser.find_elements_by_xpath("//table/tbody/tr/td[1]")
				for i in trs:
					i.click()
					name = i.text
					cwd = os.getcwd()
					browser.switch_to.window(browser.window_handles[1])
					soup = get_source(browser.page_source)
					
					get_data = soup.find(id='home').table.tbody.find_all('tr')
				
					key = []
					value = []
					for data in get_data:
						try:
							key.append(data.find_all('td')[0].text.strip())
							value.append(data.find_all('td')[1].text.strip())
						except Exception as e:
							pass

						if data.find_all('td')[0].text == "Inventor":
							break
					key.pop(-1)
					all_data = dict(zip(key, value))
					tables = soup.find('table',{"class": "table-striped"}).find_all('table',{"class": "table-striped"})
					inventory_data = []
					inventory = {}
					# inventory_key = {}
					for table in tables[0].tbody.find_all('tr')[1:]:
						inventory_key = {}
						inventory_key['Name'] = table.find_all('td')[0].text
						inventory_key['Address'] = table.find_all('td')[1].text
						inventory_key['Country'] = table.find_all('td')[2].text
						inventory_key['Nationality'] = table.find_all('td')[3].text
						inventory_data.append(inventory_key)
					# print(inventory_data)
					all_data['Inventory'] = inventory_data
					applicant_data = []
					applicant = {}
					
					for table in tables[1].tbody.find_all('tr')[1:]:
						applicant_key = {}
						applicant_key['Name'] = table.find_all('td')[0].text
						applicant_key['Address'] = table.find_all('td')[1].text
						applicant_key['Country'] = table.find_all('td')[2].text
						applicant_key['Nationality'] = table.find_all('td')[3].text
						applicant_data.append(applicant_key)
					# print(applicant_data)
					all_data['Applicant'] = applicant_data
					for data in get_data:
						try:
							if "Abstract" in data.find_all('td')[0].text:
								all_data['Abstract'] = data.find_all('td')[0].text.split(':')[1].strip()
						except Exception as e:
							continue
					for data in get_data:
						try:
							if "Complete Specification" in data.find_all('td')[0].text:
								all_data['Complete Specification'] = data.find_all('td')[0].text.strip()
						except Exception as e:
							continue

					# print(all_data)


					browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					browser.find_element_by_name("submit").click()
					time.sleep(5)
					browser.switch_to.window(browser.window_handles[2])
					time.sleep(3)
					soup = get_source(browser.page_source)
					app_data = soup.find(id='Content').table.tbody.find_all('tr')
					detail_key = []
					detail_value = []
					for data in app_data:
						try:
							detail_key.append(data.find_all('td')[0].text.strip())
							detail_value.append(data.find_all('td')[1].text.strip())
						except Exception as e:
							pass
					
					a = browser.find_element_by_xpath("//table/tbody/tr/td/h3/strong").text
					detail_key.append('Application Status')
					detail_value.append(a)
					detail_data = dict(zip(detail_key, detail_value))
					new1_detail_data = {detail_key:detail_value for detail_key, detail_value in detail_data.items() if detail_key != 'APPLICATION NUMBER'}
					new2_detail_data = {detail_key:detail_value for detail_key, detail_value in new1_detail_data.items() if detail_key != 'APPLICANT NAME'}
					new3_detail_data = {detail_key:detail_value for detail_key, detail_value in new2_detail_data.items() if detail_key != 'TITLE OF INVENTION'}
					new_detail_data = {detail_key:detail_value for detail_key, detail_value in new3_detail_data.items() if detail_key != 'FIELD OF INVENTION'} 
					total_data = dict(list(all_data.items()) + list(new_detail_data.items()))
					

					browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					browser.find_element_by_name("SubmitAction").click()
					time.sleep(5)

					btns = browser.find_elements_by_name("DocumentName")
					v=1
					document_data = []
					document = {}
					for btn in btns:
						docname = btn.text
						docdate = btn.text.split(' [')[1].split('(')[0]
						document_key = {}
						document_key['Document'] = docname
						document_key['Date'] = docdate
						document_data.append(document_key)
						v+=1
					total_data['Documents'] = document_data
					print(total_data)
					newpath = cwd+"/ipindiadocs/"
					outfile = open("{0}.json".format(newpath+name),'w')
					json.dump(total_data,outfile)
					browser.close()
					browser.switch_to.window(browser.window_handles[1])
					browser.close()
					browser.switch_to.window(browser.window_handles[0])
		except Exception as e:
			print(e)
		que.task_done()
		time.sleep(5)

for i in range(concurrent):
	t = Thread(target=DataProcess)
	t.daemon = True
	t.start()

a = datetime.datetime.now()
numdays = 82000
date_list = []


for i in range(0, numdays, 365):
	y = str((a-datetime.timedelta(days=i)).year)
	m = str((a-datetime.timedelta(days=i)).strftime("%m"))
	d = str((a-datetime.timedelta(days=i)).strftime("%d"))
	ce = m+'/'+d+'/'+y
	date_list.append(ce)
# print(date_list)
list_length = len(date_list)

for i in range(list_length):
	param = {
		'starting_date': date_list[i+1],
		'end_date':date_list[i]
	}
	que.put(param)

que.join()