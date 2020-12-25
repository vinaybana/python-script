import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, quote_plus


def get_source(html):
	soup = BeautifulSoup(html,'html.parser')
	return soup

act_req = requests.get('https://www.indiacode.nic.in/handle/123456789/1362/simple-search?page-token=22921371b3ec&page-token-value=8e9c07c1df59a086914bcdf800089520&nccharset=8D6B271D&query=Factories Act, 1948&btngo=&searchradio=all')
act_soup = get_source(act_req.content)
result={}
get_data = act_soup.find(id='myTabContent').div.table.tbody.tr.td.p.find_all('a')
for data in get_data:
	act_href=data['href']
	act_href_req = requests.get('https://www.indiacode.nic.in/'+act_href)
	act_href_soup=get_source(act_href_req.content)
	act_name=act_href_soup.find(id='short_title').text
	result['act_name']=act_name
	sections=act_href_soup.find(id='myTableActSection').find_all('a','title')
	sec = []
	rules=[]
	notifications=[]
	regulations=[]
	for s in sections:
		section={}
		section_text=s.text.strip()
		section_name=section_text.split('.')[0].strip()
		section_title=section_text.split('.')[1].strip()
		href=s['href']
		actss_id=href.split('=')[1].split('ion')[0]
		sec_id=href.split('=')[2].split('ion')[0]
		act_id=actss_id[:-1]
		section_id=sec_id[:-1]
		section_req=requests.get('https://www.indiacode.nic.in/SectionPageContent?actid='+act_id+'&sectionID='+section_id)
		section_soup=get_source(section_req.content)
		section['name']=section_name
		section['title']=section_title
		section['detail']=section_soup
		doc_req=requests.get('https://www.indiacode.nic.in/sectionlink?actid='+act_id+'&sectionID='+section_id)
		doc_soup=get_source(doc_req.content)
		try:
			docs=doc_soup.find(id='Rules'+section_id+'').table.tbody.find_all('tr')
			for doc in docs:
				rule={}
				year=doc.find_all('td')[0].text
				description=doc.find_all('td')[1].text
				pdf_href=doc.find_all('td')[2].a['href']
				rule['year']=year
				rule['description']=description
				rule['pdf_href']=pdf_href
				rules.append(rule)
			section['Rule']=rules
		except:
			pass
		try:
			docs=doc_soup.find(id='Notifications'+section_id+'').table.tbody.find_all('tr')
			for doc in docs:
				notification={}
				year=doc.find_all('td')[0].text
				description=doc.find_all('td')[1].text
				pdf_href=doc.find_all('td')[2].a['href']
				notification['year']=year
				notification['description']=description
				notification['pdf_href']=pdf_href
				notifications.append(notification)
			section['Notifications']=notifications
		except:
			pass
		try:
			docs=doc_soup.find(id='Regulations'+section_id+'').table.tbody.find_all('tr')
			for doc in docs:
				regulation={}
				year=doc.find_all('td')[0].text
				description=doc.find_all('td')[1].text
				pdf_href=doc.find_all('td')[2].a['href']
				regulation['year']=year
				regulation['description']=description
				regulation['pdf_href']=pdf_href
				regulations.append(regulation)
			section['Regulations']=regulations
		except:
			pass
		sec.append(section)
	result['section']=sec
	print(result)