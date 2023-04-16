import requests

def ipv4():
	response = requests.get('https://api.myip.com')
	data = response.json()['country']
	print(data)

def country():
	response = requests.get('https://api.myip.com')
	data = response.json()['country']
	print(data)

