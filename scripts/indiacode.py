from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import json
import csv
from bs4 import BeautifulSoup
import os, sys
import datetime
from datetime import timedelta

def get_source(html):
	soup = BeautifulSoup(html,'html.parser')
	return soup


options = Options()			
options.add_argument("--start-maximized")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("--remote-debugging-port=9222")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--silent")

# filepath="/var/www/Python-projects/python-script/script/"

# with open('/var/www/Python-projects/python-script/script/IndiaCode-Analytics_Page-1_Table.csv') as csv_file:
# 	csv_reader = csv.reader(csv_file)
# 	for row in csv_reader:
# 		print(row)

browser = webdriver.Chrome('/var/www/Python-projects/python-script/chromedriver', options=options)
browser.get('https://www.indiacode.nic.in/')
time.sleep(2)
browser.find_element_by_xpath("//input[@value='all']").click()
time.sleep(1)
browser.find_element_by_id("tequery").send_keys('Motor Vehicles Act, 1988')
browser.find_element_by_id("btngo").click()
name=browser.find_element_by_xpath("//ul[@id='myTab']/li/a[@id='all-tab']/span").text
total_docs = name.split('(')[1].split(')')[0]
print(total_docs)
browser.find_element_by_xpath("//ul[@id='myTab']/li/a[@id='all-tab']").click()
# for tab in tabs:
# 	tab_name=tab.text
# 	# if int(tab_name.split('(')[1].split(')')[0])>0:
# 	if tab_name.split('(')[0]=='All Results':
# 		tab.click()
# 		# time.sleep(2)
		# docs=browser.find_elements_by_xpath("//div[@id='myTabContent']/div/p/a")
docs=browser.find_elements_by_xpath("//table[@id='myTableSection']/tbody/tr/td/p/a")
for doc in docs:
	# doc_name=doc.text
	doc.click()

	

time.sleep(5)
browser.quit()