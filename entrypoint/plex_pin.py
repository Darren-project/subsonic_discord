import sys
sys.path.insert(0, '..')

from config import shared

code = sys.argv[1]
pin = sys.argv[2]

import requests

if code:
	headers = {
	    'accept': 'application/json',
	    'content-type': 'application/x-www-form-urlencoded',
	}

	data = 'code=' + code + '&X-Plex-Client-Identifier=' + shared.client_id

	response = requests.get('https://plex.tv/api/v2/pins/' + pin, headers=headers, data=data)
	json = response.json()
	print(json)
	if json.get("authToken"):
		print("Saving Token")
		f = open("../config/plex_token.json", "w")
		f.write('{"plex_token": "' + json.get("authToken") + '"}')
		f.close()
		exit()
	else:
		exit(1)
