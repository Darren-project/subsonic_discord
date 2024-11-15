import sys
sys.path.insert(0, '..')
from pypresence import Presence
import time
import random
from config import shared
import sys
import os
import requests

last = ()
tn = 0
npc = False
sd = False
import logging
logging.basicConfig(format='%(message)s')
logging.root.setLevel(logging.NOTSET)
handler = logging.StreamHandler(sys.stdout)
log = logging.getLogger(__name__)
log.addHandler(handler)
def print(a):
    log.info(a)

pid_c = int(str(random.randint(0,5)) + str(random.randint(0,5)) + str(random.randint(0,5)) + str(random.randint(0,5)))

client_id = shared.d_app_cid  # Put your Client ID here, this is a fake ID
RPC = Presence(client_id)  # Initialize the Presence class
RPC.connect()  # Start the handshake loop

import json

if not os.path.exists('../temp/prevsong.json'):
  with open('../temp/prevsong.json', 'w') as file:
      file.write('[]')

username = shared.username
password = shared.password
url = shared.url
socks = "socks5://localhost:2056"

while True:  # The presence will stay on as long as the program is running
    pid_c = int(str(random.randint(0,5)) + str(random.randint(0,5)) + str(random.randint(0,5)) + str(random.randint(0,5)))
    requests.get("http://127.0.0.1:1998/ping")
    data = requests.get("http://" + url + "/rest/getNowPlaying?u=" + username + "&p=" + password + "&v=1.30.1&c=Discord&f=json",  proxies=dict(http=socks))
    data = data.json()["subsonic-response"]
    music = (data["nowPlaying"]["entry"][0]["title"], data["nowPlaying"]["entry"][0]["artist"], data["nowPlaying"]["entry"][0]["coverArt"], data["nowPlaying"]["entry"][0]["playerName"], data["nowPlaying"]["entry"][0]["playerType"], data["nowPlaying"]["entry"][0]["duration"])
    
    epoch_time = int(time.time())
#    print("RPC Sent")
#    print(music[0])
    try:
      if music == last and not npc:
         pass
      else:
       img = shared.dashboard_url + "/api/art/" + music[2]
#       print(img)
       if music[0] == "":
        raise "2"
       RPC.update(
          large_image=img,
          large_text=music[0],
          state=music[0] + " by " + music[1],
          details="Playing on " + music[3],
          #start=epoch_time,
          #end=epoch_time+(music[5]/1000),
          buttons=[{"label": "History", "url": shared.dashboard_url}],
          pid=pid_c,
       )
      # Read the previous songs from prevsong.json
       with open('../temp/prevsong.json', 'r') as file:
          try:
            prev_songs = json.load(file)
          except json.JSONDecodeError:
            prev_songs = []
       if not last:
         pass
       else:
         # Append the latest song to the list
         prev_songs.insert(0, {"songimg": img, "songname": last[0], "artistname": last[1], "devicename": last[3]})

      # Ensure the list contains no more than 4 songs
       if len(prev_songs) > 4:
          prev_songs.pop(-1)

      # Save the updated list back to prevsong.json
       with open('../temp/prevsong.json', 'w') as file:
          file.write(json.dumps(prev_songs))

      last = music
      tn = 0
      npc = False
    except:
#       pass
      if not npc:
       if tn < 6:
        if music[4] == "3rd-party":
         tn = tn + 1
        else:
         tn = 6
       elif npc:
          pass
       else:
         RPC.update(
            state="No music is playing",
            details="Play some music!",
            buttons=[{"label": "History", "url": shared.dashboard_url}],
            pid=pid_c
         )
         npc = True
    print(str(tn) + " " + str(last) + " " +str(npc)+" "+str(music))
    time.sleep(5) #Wait a wee bit


