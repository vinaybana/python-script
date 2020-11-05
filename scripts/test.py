import requests

data = {
	'companyOrllp': 'C',
'__checkbox_companyChk': True,
'cinChk': True,
'__checkbox_cinChk': True,
'cinFDetails': 'U25191KA1982PTC004894',
'__checkbox_llpChk': True,
'__checkbox_llpinChk': True,
'__checkbox_regStrationNumChk': True,
'countryOrigin': 'INDIA',
'submitBtn': 'Submit'
}

req = requests.post('http://www.mca.gov.in/mcafoportal/companySearch.do',data=data)
print(req.text)