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

browser = webdriver.Chrome('/var/www/chromedriver', options=options)

browser.get('http://www.mca.gov.in/mcafoportal/getCertifiedCopies.do')
time.sleep(5)

checkbox = browser.find_element_by_id("cinChk")
checkbox.click()
CINinput = browser.find_element_by_id("cinFDetails")
CINinput.send_keys("U25191KA1982PTC004894") 
submit = browser.find_element_by_id("submitBtn")
submit.click()
browser.find_element_by_link_text("U25191KA1982PTC004894").click()
time.sleep(2)
html = browser.page_source
soup = get_source(html)
opt = soup.find(id='searchCategoryDetails_categoryName').text.split('\n')
docs = opt[2:-1]
y = soup.find(id='searchCategoryDetails_finacialYear').text.split('\n')
years = y[2:-1]

for doc in docs:
	browser.find_element_by_xpath("//select[@id='searchCategoryDetails_categoryName']").send_keys(doc)
	time.sleep(2)
	for year in years:
		browser.find_element_by_xpath("//select[@id='searchCategoryDetails_finacialYear']").send_keys(year)
		time.sleep(1)
		browser.find_element_by_id("searchCategoryDetails_0").click()
		time.sleep(3)
		try:
			# error = browser.find_element_by_class_name("error_overlay").text
			browser.find_element_by_id("msgboxclose").click()
			continue
		except:
			pass
		html = browser.page_source
		soup = get_source(html)


		document = soup.find(id='results').tbody

		for doc in document.find_all('tr')[1:]:
			print(doc.find_all('td')[1].text.strip())
			print(doc.find_all('td')[2].text.strip())
			print(doc.find_all('td')[3].text.strip())
			print("\n")

browser.quit()


