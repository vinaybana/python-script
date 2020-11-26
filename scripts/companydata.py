from selenium import webdriver
import time
import csv
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import sqlite3
import pymysql
import sqlparse
import requests
import json
from queue import *
from threading import Thread
import os

def get_source(html):
	soup = BeautifulSoup(html,'html.parser')
	return soup

def get_list(arr):
	try:
		for i in arr:
			arr.remove('')
	except: pass
	return arr

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

concurrent = 2
que = Queue(concurrent*1)

def Query(sql):
	db = pymysql.connect("localhost","root","redhat@123","mca",charset='utf8mb4')
	dbc = db.cursor(pymysql.cursors.DictCursor)
	output = {}
	qcnt = -1
	for statement in sqlparse.split(sql):
			qcnt = qcnt + 1
			dbc.execute(statement)
			db.commit()
			output[qcnt] = dbc.fetchall()
	if qcnt == 0:
			output = output[0]
	dbc.close()
	db.close()
	return output



url ='https://www.mca.gov.in/mcafoportal/viewCompanyMasterData.do'
companyapi = "http://13.127.92.196:8000/cvakilapi/v1/company/"
chargeapi = "http://13.127.92.196:8000/cvakilapi/v1/charge/"
directorapi = 'http://13.127.92.196:8000/cvakilapi/v1/director/'

def DataProcess():
	while True:
		param = que.get()
		# req = requests.get(url=companyapi+'?status=Inactive')
		# cin_data = json.loads(req.text)
		print(param['cin'])

		# for cin_num in cin_data['results']:
		cin_id = param['id']
		cin = param['cin']
		name = ''
		roc = ''
		registration = ''
		category= ''
		subcategory = ''
		company_class = ''
		authorised_capital = ''
		paidup_capital = ''
		member = ''
		incorporation_date = ''
		address = ''
		alternate_address = ''
		email = ''
		listed = ''
		compliance = ''
		stock_exchange = ''
		agm = ''
		balancesheet = ''
		office = ''
		detail = ''
		activity = ''
		rawdata = ''
		country = ''
		company_status = ''
		company_share = ''
		partner = ''
		designated_partners = ''
		previous_firm = ''
		obligation = ''
		description = ''
		account = ''
		annual = ''
		previous_firm = ''
		present_filing = ''
		cirp = ''


		try:
			driver = webdriver.Chrome(executable_path='/var/www/Python-projects/python-script/chromedriver')
			driver.get(url)
			time.sleep(3)

			driver.find_element_by_id('companyID').send_keys(cin)
			# driver.find_element_by_id('companyID').send_keys('F03097')
			# driver.find_element_by_id('companyID').send_keys('AAL-9004')
			elem = driver.find_element_by_name('displayCaptcha')
			value = driver.execute_script('return arguments[0].value;', elem)
			driver.execute_script('''
				var elem = arguments[0];
				var value = arguments[1];
				elem.value = value;
			''', elem, 'false')
			value = driver.execute_script('return arguments[0].value;', elem)
			driver.find_element_by_id('companyLLPMasterData_0').click()
			time.sleep(3)

			try:
				html = driver.page_source
				soup = get_source(html)

				detail = []
				column = []
				table_data = soup.find('table','result-forms').find_all('tr')
			except:
				time.sleep(5)
				html = driver.page_source
				soup = get_source(html)
				detail = []
				column = []
				table_data = soup.find('table','result-forms').find_all('tr')

			for data in table_data:
				tr = get_list(data.text.split("\n"))
				detail.append(tr[1].replace("\t",''))
				column.append(tr[0])

			comp_dict = dict(zip(column, detail))

			test_dict = {}

			print(column[0].lower())
			if 'cin' in column[0].lower():
				for key,value in comp_dict.items():
					if 'cin' in key.lower():
						cin = comp_dict[key]
						test_dict[key] = comp_dict[key]
					if 'name' in key.lower():
						name = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'roc' in key.lower():
						roc = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'registration' in key.lower():
						registration = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'company category' in key.lower():
						category = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'company subcategory' in key.lower():
						subcategory = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'class of company' in key.lower():
						company_class = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'authorised capital' in key.lower():
						authorised_capital = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'paid up capital' in key.lower():
						paidup_capital = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'number of memebers' in key.lower() or 'members' in key.lower():
						member = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'date of incorporation' in key.lower() or 'incorporation' in key.lower():
						if comp_dict[key].strip() == '-' or comp_dict[key].strip() == '':
							incorporation_date = comp_dict[key].strip()
						else:	
							doi = comp_dict[key].strip().split("/")
							incorporation_date = '-'.join(reversed(doi))
						test_dict[key] = comp_dict[key]
					if 'registered address' in key.lower():
						address = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'address other than r/o where all' in key.lower():
						alternate_address = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'email id' in key.lower() or 'email' in key.lower():
						email = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'whether listed or not' in key.lower() or 'listed' in key.lower():
						listed = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'active compliance' in key.lower():
						compliance = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'companies present filing status' in key.lower():
						present_filing = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'suspended at stock exchange' in key.lower() or 'stock exchange' in key.lower():
						stock_exchange = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'date of last agm' in key.lower() or 'agm' in key.lower():
						if comp_dict[key].strip() == '-' or comp_dict[key].strip() == '':
							agm = comp_dict[key]
						else:	
							agm_date = comp_dict[key].strip().split("/")
							agm = '-'.join(reversed(agm_date))
						test_dict[key] = comp_dict[key]
					if 'date of balance sheet' in key.lower() or 'balance sheet' in key.lower():
						if comp_dict[key].strip() == '-' or comp_dict[key].strip() == '':
							balancesheet = comp_dict[key].strip()
						else:
							sheet_date = comp_dict[key].strip().split("/")
							balancesheet = '-'.join(reversed(sheet_date))
						test_dict[key] = comp_dict[key]
					if 'company status' in key.lower() or 'company status(for efiling)' in key.lower():
						company_status = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'status under cirp' in key.lower():
						cirp = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]

				data = {
					'id': cin_id, 
					'company_format': 'CIN',
					'name': name,
					'roc': roc,
					'registration': registration,
					'category': category,
					'subcategory': subcategory,
					'company_class': company_class,
					'authorised_capital': authorised_capital,
					'paidup_capital': paidup_capital,
					'member': member,
					'incorporation_date': incorporation_date,
					'address': address,
					'alternate_address': alternate_address,
					'email': email,
					'listed': listed,
					'compliance': compliance,
					'present_filing': present_filing,
					'stock_exchange': stock_exchange,
					'agm': agm,
					'balancesheet': balancesheet,
					'company_status': company_status,
					'cirp': cirp,
					'status': 'Active'
					}

				if present_filing == '' or present_filing == '-':
					data.pop('present_filing')
				if agm == '-' or agm =='':
					data.pop('agm')
				if balancesheet == '-' or balancesheet == '':
					data.pop('balancesheet')
				if cirp == '' or cirp == '-':
					data.pop('cirp')

			elif 'fcrn' in column[0].lower():
				for key,value in comp_dict.items():
					if 'fcrn' in key.lower():
						cin = comp_dict[key]
						test_dict[key] = comp_dict[key]
					if 'name' in key.lower():
						name = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'date of incorporation' in key.lower():
						incorporation_date = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'country of incorporation' in key.lower():
						country = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'registered address' in key.lower():
						address = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'email id' in key.lower() or 'email' in key.lower():
						email = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'foreign company with share capital' in key.lower():
						company_share = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'company status' in key.lower() or 'company status(for efiling)' in key.lower():
						company_status = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'type of office' in key.lower() or 'office' in key.lower():
						office = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'details' in key.lower():
						detail = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'main division of business activity' in key.lower() or 'business activity' in key.lower():
						activity = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'description of main division' in key.lower():
						description = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]

				data = {
					'id': cin_id,
					'company_format': 'FCRN',
					'name': name,
					'incorporation_date': incorporation_date,
					'country': country,
					'address': address,
					'email': email,
					'company_share': company_share,
					'company_status': company_status,
					'office': office,
					'detail': detail,
					'activity': activity,
					'description': description,
					'status': 'Active'
				}

			elif 'llpin' in column[0].lower():
				for key,value in comp_dict.items():
					if 'llpin' in key.lower():
						cin = comp_dict[key]
						test_dict[key] = comp_dict[key]
					if 'name' in key.lower():
						name = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'number of partners' in key.lower():
						partner = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'number of designated partners' in key.lower():
						designated_partners = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'roc' in key.lower():
						roc = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'date of incorporation' in key.lower() or 'incorporation' in key.lower():
						incorporation_date = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'registered address' in key.lower():
						address = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'email id' in key.lower() or 'email' in key.lower():
						email = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'previous firm/ company details' in key.lower():
						previous_firm = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'total obligation of contribution' in key.lower():
						obligation = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'main division of business activity' in key.lower() or 'business activity' in key.lower():
						activity = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'description of main division' in key.lower():
						description = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'date of last financial year end date for which statement of accounts and solvency filed' in key.lower():
						account = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'date of last financial year end date for which annual return filed' in key.lower():
						annual = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]
					if 'llp status' in key.lower():
						company_status = comp_dict[key].strip()
						test_dict[key] = comp_dict[key]

				data = {
					'id': cin_id,
					'company_format': "LLPIN",
					'name': name,
					'partner': partner,
					'designated_partners': designated_partners,
					'roc': roc,
					'incorporation_date': incorporation_date,
					'address': address,
					'email': email,
					'previous_firm': previous_firm,
					'obligation': obligation,
					'activity': activity,
					'description': description,
					'account': account,
					'annual': annual,
					'company_status': company_status,
					'status': 'Active'
					}

			for key in test_dict:
				comp_dict.pop(key)
			raw = comp_dict
			rawdata = json.dumps(raw)
			data['rawdata']= rawdata
			# print(data)
			# print(cin,name,roc,registration,partner,office,designated_partners,previous_firm,obligation,description,account,annual,category,subcategory,company_class,authorised_capital,paidup_capital,member,incorporation_date,address,alternate_address,email,listed,compliance,stock_exchange,agm,balancesheet,company_status,activity)
			
			######################## Charges ########################################
			charges = soup.find(id='chargesRegistered').table.tbody

			charges_list = []
			for crg in charges.find_all('tr')[1:]:
				assets = crg.find_all('td')[0].text.strip()
				if 'No Charges Exists for Company/LLP' in assets:
					break
				if assets == '':
					assets = '-'
				charge = crg.find_all('td')[1].text.strip()

				if crg.find_all('td')[2].text.strip() == '-' or crg.find_all('td')[2].text.strip() == '':
					created = crg.find_all('td')[2].text.strip()
				else:		
					bdate = crg.find_all('td')[2].text.strip().split('/')
					created = '-'.join(reversed(bdate))

				if crg.find_all('td')[3].text.strip() == '-' or crg.find_all('td')[3].text.strip() == '':	
					modification = crg.find_all('td')[3].text.strip()
				else:
					mdate = crg.find_all('td')[3].text.strip().split('/')
					modification = '-'.join(reversed(mdate))

				charge_status = crg.find_all('td')[4].text.strip()

				if modification == '-' or modification == '':
					chrg_data = {
						'company': cin_id,
						'assets': assets,
						'charge': charge,
						'created': created,
						'charge_status': charge_status,
						'status': 'Active'
					}
				else:
					chrg_data = {
					'company': cin_id,
					'assets': assets,
					'charge': charge,
					'created': created,
					'modification': modification,
					'charge_status': charge_status,
					'status': 'Active'
				}
				
				# print(chrg_data)
				charge_post = requests.post(url=chargeapi,data=chrg_data)
				print("charges",charge_post.status_code)
				
			######################## Directors/Signatory Details #####################
			dir_list_clm = soup.find(id='signatories').table.tbody

			for dirl in dir_list_clm.find_all('tr')[1:]:
				din = dirl.find_all('td')[0].text.strip()
				if 'No Signatory Exists for Company/LLP' in din:
					break
				name = dirl.find_all('td')[1].text.strip()

				if dirl.find_all('td')[2].text.strip() == '-' or dirl.find_all('td')[2].text.strip() == '':
					started = dirl.find_all('td')[2].text.strip()
				else: 
					begin_date = dirl.find_all('td')[2].text.strip().split("/")
					started = '-'.join(reversed(begin_date))

				if dirl.find_all('td')[3].text.strip() == '-' or dirl.find_all('td')[3].text.strip() == '':
					ended = dirl.find_all('td')[3].text.strip()
				else:
					end_date = dirl.find_all('td')[3].text.strip().split('/')
					ended = '-'.join(reversed(end_date))

				if dirl.find_all('td')[4].text.strip() == '-' or dirl.find_all('td')[4].text.strip() == '':
					surrendered = dirl.find_all('td')[4].text.strip()
				else:
					sdate = dirl.find_all('td')[4].text.strip().split('/')
					surrendered = '-'.join(reversed(sdate))
				if surrendered == "":
					surrendered = '-'
				# print(din,name,started,ended,surrendered)
				if ended == '-' or ended == '':
					dir_data = {
						'company_id': cin_id,
						'din': din,
						'name': name,
						'started': started,
						'surrendered': surrendered,
						'status': 'Active'
					}
				if surrendered == '-':
					dir_data = {
						'company_id': cin_id,
						'din': din,
						'name': name,
						'started': started,
						'ended': ended,
						'status': 'Active'
					}
				if ended == '-' and surrendered == '-':
					dir_data = {
						'company_id': cin_id,
						'din': din,
						'name': name,
						'started': started,
						'status': 'Active'
					}
				if ended != '-' and surrendered != "-":
					dir_data = {
						'company_id': cin_id,
						'din': din,
						'name': name,
						'started': started,
						'ended': ended,
						'surrendered': surrendered,
						'status': 'Active'
					}

				# print(dir_data)
				dir_post = requests.post(url=directorapi,data=dir_data)
				print("director",dir_post.status_code)

			company_patch = requests.patch(url=companyapi+str(cin_id)+"/",data=data)
			print("company",company_patch.status_code)

			driver.quit()
			# break
			print('\n','\n')
			
		except Exception as e:
			print(e)
			driver.quit()

		que.task_done()
	driver.quit()
	

for i in range(concurrent):
	t = Thread(target=DataProcess)
	t.daemon = True
	t.start()

# a = Query("SELECT * FROM CIN_NO where status=0")
aa = requests.get(url=companyapi+"?status=Inactive")
companies = json.loads(aa.text)

for i in companies['results']:
	# print(i)
	param = {'cin':i['cin'],
			'id':i['id']
			}
	que.put(param)

que.join()


			###################### Companies #################################################
		# 	dir_list1 = soup.find_all(id='aShowDirectorMasterdata')
		# 	for dirl in dir_list1:
		# 		actions = ActionChains(driver)
		# 		find = driver.find_element_by_link_text(dirl.text)
		# 		actions.key_down(Keys.CONTROL).click(find).key_up(Keys.CONTROL).perform()

		# 		driver.switch_to.window(driver.window_handles[-1])
		# 		time.sleep(5)
		# 		try:
		# 			html2 = driver.page_source
		# 			soup2 = get_source(html2)
		# 			dirname = soup2.find('table', 'result-forms').tbody
		# 		except:
		# 			time.sleep(10)
		# 			html2 = driver.page_source
		# 			soup2 = get_source(html2)
		# 			dirname = soup2.find('table', 'result-forms').tbody

		# 		din_names = get_list(dirname.text.split("\n"))
		# 		print(din_names)
		# 		dir1 = soup2.find(id='resultsTab3').find_all('tr')
		# 		for d in dir1[1:]:
		# 			# print(d.text.strip().split("\n"))
		# 			cin_fcrn = d.text.strip().split("\n")[0]
		# 			cname = d.text.strip().split("\n")[1].replace("'",'')
		# 			bdate = d.text.strip().split("\n")[2]
		# 			edate = d.text.strip().split("\n")[3]

		# # 			Query("insert into companies(comp_id,din_no,dir_name,cin_fcrn,cname,bdate,edate) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(int(cin['id']),din_names[1],din_names[-1],cin_fcrn,cname,bdate,edate))
		# # 		companies_data = Query("SELECT * FROM companies")
		# # 		# print(companies_data)

		# 		try:
		# 			llp = soup2.find('tr','table-row').find_all('td')
		# 			for l in llp:
		# 				llpin = l.text.strip().split("\n")[0]
		# 				if 'No LLP exists for a Director' in llpin:
		# 					break
		# 		except:
		# 			llp = soup2.find_all(id='resultsTab3')[-1]
		# 			for l in llp.tbody.find_all('tr')[1:]:
		# 				llpin = l.text.split("\n")[1:-1][0]
		# 				llp_name = l.text.split("\n")[1:-1][1]
		# 				begin = l.text.split("\n")[1:-1][2]
		# 				end = l.text.split("\n")[1:-1][3]

		# # 				Query("insert into llp(llp_id,llpin_fllpin,llp_name,bdate,edate) values('{0}','{1}','{2}','{3}','{4}')".format(int(cin['id']),llpin,llp_name,begin,end))

		# # 		llp_data = Query("SELECT * FROM llp")
		# # 		# print(llp_data)

		# 		driver.close()
		# 		driver.switch_to.window(driver.window_handles[0])
		# 		time.sleep(1)