import requests


def get_play_latest(token, url):
	header = {
		"Accept": "application/json"
	}

	try:
		response = requests.get(url + "/status/sessions?X-Plex-Token=" + token, headers=header)
	except Exception as e:
		if "SSLError" in str(repr(e)):
			return "purpose"
		else:
			print(str(repr(e)))
			return "offline"
	print(response.text)
	data = response.json()
	try:
		d2 = data["MediaContainer"]["Metadata"]
	except:
		return []
	d3 = []
	plat = ''
	for i in d2:
		#print(i.get("Player").get("state"))
		if i.get("Player").get("state") == "playing":
			d3.append(i)
		plat = i.get("Player").get("platform")
	if d3 == []:
		return plat
	else:
		return d3

def get_resources(token, id):
	header = {
		"Accept": "application/json"
	}
	response = requests.get("https://plex.tv/api/v2/resources?X-Plex-Token=" + token + "&includeRelay=1&X-Plex-Client-Identifier=" + id, headers=header)
	data = response.json()
	return data

def clean_up(data):
	#print(data)
	if data == []:
		return '', '', '', '', ''
	if (not type(data) is list):
         return '', '', '', '', data
	data = data[0]
	#print(data)
	title = data["title"]
	artist = data["grandparentTitle"]
	icon = data["thumb"]
	user = data["User"]["title"]
	user_icon = data["User"]["thumb"]
	device_name = data["Player"]["title"]
	platform = (data.get("Player").get("platform") or "3rd-party")
	return title, artist, icon, device_name, platform

