import requests
import time


for i in range(0,100):
	time.sleep(1)
	req = requests.head('https://www.mca.gov.in/mcafoportal/viewCompanyMasterData.do')
	print(req.status_code)