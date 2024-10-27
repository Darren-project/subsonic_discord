import requests


def get_play_latest(token, url):
	header = {
		"Accept": "application/json"
	}
	response = requests.get(url + "/status/sessions?X-Plex-Token=" + token, headers=header)
	data = response.json()
	try:
		d2 = data["MediaContainer"]["Metadata"]
	except:
		return []
	d3 = []
	for i in d2:
		#print(i.get("Player").get("state"))
		if i.get("Player").get("state") == "playing":
			d3.append(i)
	return d3

def get_resources(token, id):
	header = {
		"Accept": "application/json"
	}
	response = requests.get("https://plex.tv/api/v2/resources?X-Plex-Token=" + token + "&includeRelay=1&X-Plex-Client-Identifier=" + id, headers=header)
	data = response.json()
	return data

def clean_up(data):
	if (not data):
         return None
	data = data[0]
	title = data["title"]
	artist = data["grandparentTitle"]
	icon = data["thumb"]
	user = data["User"]["title"]
	user_icon = data["User"]["thumb"]
	device_name = data["Player"]["title"]
	return title, artist, icon, user, user_icon, device_name

