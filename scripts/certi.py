from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time 
import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import requests
import json 

# prefs = {"download.default_directory" : '/var/www/seleniumtest/archive/'}
def get_source(html):
	soup = BeautifulSoup(html,'html.parser')
	return soup

options = Options()			
options.add_argument("--start-maximized")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("--remote-debugging-port=9222")
# options.add_experimental_option("prefs",prefs)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--silent")

apiurl = "http://13.127.92.196:8000/cvakilapi/v1/company/"
browser = webdriver.Chrome('/var/www/Python-projects/python-script/chromedriver', options=options)
while True:
	Cinlist = requests.get(url = apiurl+"?scrap_status=0&status=Active")
	cin_list = json.loads(Cinlist.text)
	for i in cin_list['results']:
		browser.get('http://www.mca.gov.in/mcafoportal/getCertifiedCopies.do')
		time.sleep(5)

		checkbox = browser.find_element_by_id("cinChk")
		checkbox.click()
		CINinput = browser.find_element_by_id("cinFDetails")
		CINinput.send_keys(i['cin']) 
		print(i['cin'])

		submit = browser.find_element_by_id("submitBtn")
		submit.click()
		browser.find_element_by_link_text(i['cin']).click()
		time.sleep(2)
		html = browser.page_source
		soup = get_source(html)
		opt = soup.find(id='searchCategoryDetails_categoryName').text.split('\n')
		docs = opt[2:-1]
		y = soup.find(id='searchCategoryDetails_finacialYear').text.split('\n')
		years = y[2:-1]

		for doc in docs:
			browser.find_element_by_xpath("//select[@id='searchCategoryDetails_categoryName']").send_keys(doc)
			doc_category = doc;
			time.sleep(2)
			for year in years:
				if year > '2020':
					break
				doc_year = year;
				browser.find_element_by_xpath("//select[@id='searchCategoryDetails_finacialYear']").send_keys(year)
				time.sleep(1)
				browser.find_element_by_id("searchCategoryDetails_0").click()
				time.sleep(3)
				try:
					browser.find_element_by_id("msgboxclose").click()
					continue
				except:
					pass
				html = browser.page_source
				soup = get_source(html)
				document = soup.find(id='results').tbody
				for doc in document.find_all('tr')[1:]:
					name = doc.find_all('td')[1].text.strip()
					d = doc.find_all('td')[2].text.strip().split("/")
					date = "-".join(reversed(d))
					try:
						data = {'company':i['id'],'category':doc_category, 'name':name,'year': doc_year,'date':date,'status':'Active'}
						req = requests.post(url="http://13.127.92.196:8000/cvakilapi/v1/document/",data=data)
						if req.status_code == 201 or req.status_code == 200:
							data2 = {'scrap_status':'1'}
							requ = requests.patch(url="http://13.127.92.196:8000/cvakilapi/v1/company/"+str(i["id"])+"/",data=data2 )
							print(requ.status_code, requ.text)	
						print(req.status_code, req.text)
						
					except Exception as e:
						print(e)					

	browser.quit()


