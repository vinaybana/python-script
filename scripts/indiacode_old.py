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


browser = webdriver.Chrome('/var/www/Python-projects/python-script/chromedriver', options=options)
browser.get('https://www.indiacode.nic.in/')
time.sleep(2)
browser.find_element_by_xpath("//input[@value='all']").click()
time.sleep(1)
browser.find_element_by_id("tequery").send_keys('The Motor Vehicles Act, 1988')
browser.find_element_by_id("btngo").click()
name=browser.find_element_by_xpath("//ul[@id='myTab']/li/a[@id='all-tab']/span").text
total_docs = name.split('(')[1].split(')')[0]
browser.find_element_by_xpath("//ul[@id='myTab']/li/a[@id='all-tab']").click()

soup = get_source(browser.page_source)
docs = soup.find_all('tr')[1:]
for doc in docs:
	browser.get('https://www.indiacode.nic.in'+doc.find('td').p.a['href'])
	result={}
	time.sleep(2)
	try:
		act_name=browser.find_element_by_xpath("//div[@class='container']/div/p").text
		result['act_name']=act_name
		act_parts=browser.find_elements_by_xpath("//div[@class='container']/ul/li")
		for part in act_parts:
			part_name=part.text
			# part_name.click()
			if part_name=='Sections':
				soup1 = get_source(browser.page_source)
				get_data = soup1.find(id='myTableActSection_wrapper').table.tbody.find_all('tr')
				i=1				
				for data in get_data:
					print(i)
					sec_name=data.find('td').div.a.span.text
					title=data.find('td').div.a.text.split('.')[1]
					browser.find_element_by_class_name("secbtn").click()
					# des=data.find('td').find('p').text
					time.sleep(2)
					# des = browser.find_element_by_xpath("//div[@class='panel-body']/p")
					# des = browser.find_element_by_id('accordion'+str(i))
					soup2 = get_source(browser.page_source)
					des=soup2.find(id='accordion'+str(i)).div.div.find('p')
					print(des.text)
					print(des)
					i+=1

					
					# print(data.find('td').div.div.div.text.strip())
					# part_name={
					# 	'section':sec_name,
					# 	'title':title,
					# 	# 'detail':des
					# }
					# part_name['section']=data.find_all('td')[0].text.strip()
					# part_name['title']=data.find_all('td')[1].text.strip()
					# part_name['detail']=data.find_all('td')[2].text.strip()
			# part_name2=dict(part_name)
			# print(part_name2)
			# result[part_name]=part_name
			print(result)
	except Exception as e:
		print(e,'1111111111111111')


	

# time.sleep(5)
# browser.quit()