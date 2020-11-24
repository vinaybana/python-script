import requests
import time 

for i in range(87071, 4500100):
	print(i)
	data = {
			'tmno': i,
			'status': 'Inactive'
			}
	req = requests.post(url="http://13.127.92.196:8000/cvakilapi/v1/tmno/",data=data)
	print(data, '---->', req.status_code)
	time.sleep(3)
