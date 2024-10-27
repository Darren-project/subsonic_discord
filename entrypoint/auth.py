import sys
sys.path.insert(0, '..')

from config import shared

import time

import requests

headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',
}

data = 'strong=true&X-Plex-Product=' + shared.product + '&X-Plex-Client-Identifier=' + shared.client_id

response = requests.post('https://plex.tv/api/v2/pins', headers=headers, data=data)

#print(response.json())

code = response.json()["code"]
pin_id = str(response.json()["id"])

url = "https://app.plex.tv/auth#?clientID=" + shared.client_id + "&code=" + code + "&context[device][product]=" + shared.product.replace(" ", "%20")

print(url)

input("enter after you coppied the link")

while True:
	headers = {
	    'accept': 'application/json',
	    'content-type': 'application/x-www-form-urlencoded',
	}

	data = 'code=' + code + '&X-Plex-Client-Identifier=' + shared.client_id

	response = requests.get('https://plex.tv/api/v2/pins/' + pin_id, headers=headers, data=data)
	json = response.json()
	print(json)
	if json.get("authToken"):
		print("Saving Token")
		f = open("../config/plex_token.json", "w")
		f.write('{"plex_token": "' + json.get("authToken") + '"}')
		f.close()
		exit()
	time.sleep(5)
