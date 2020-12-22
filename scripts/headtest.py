import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, quote_plus


def get_source(html):
	soup = BeautifulSoup(html,'html.parser')
	return soup

# for i in range(0,100):
	# time.sleep(1)
act_req = requests.get('https://www.indiacode.nic.in/handle/123456789/1362/simple-search?page-token=22921371b3ec&page-token-value=8e9c07c1df59a086914bcdf800089520&nccharset=8D6B271D&query=Factories Act, 1948&btngo=&searchradio=all')
act_soup = get_source(act_req.content)
result={}
# print(soup)
get_data = act_soup.find(id='myTabContent').div.table.tbody.tr.td.p.find_all('a')
for data in get_data:
	act_href=data['href']
	act_href_req = requests.get('https://www.indiacode.nic.in/'+act_href)
	act_href_soup=get_source(act_href_req.content)
	# print(soup1)
	act_name=act_href_soup.find(id='short_title').text
	result['act_name']=act_name
	sections=act_href_soup.find(id='myTableActSection').find_all('a','title')
	sec = []
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
		# sec={'name':section_name,'title':section_title, 'detail':section_soup}
		# print(soup2)
		section['name']=section_name
		section['title']=section_title
		section['detail']=section_soup
		sec.append(section)
	result['section']=sec
	# print(total_count.text)