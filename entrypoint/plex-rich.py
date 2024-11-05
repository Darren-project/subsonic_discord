import sys
sys.path.insert(0, '..')
from component import url_adapt
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
from component import plex_q



# Open and read the JSON file
with open('../config/plex_token.json', 'r') as file:
    data = json.load(file)

   # Open and wipe the JSON file
with open('../temp/prevsong.json', 'w') as file:
      file.write('[]')

urls = url_adapt.adapt( plex_q.get_resources(data["plex_token"], shared.client_id))
url = urls[shared.cid]["relay"]
api = urls[shared.cid]["relay"]

while True:  # The presence will stay on as long as the program is running
    requests.get("http://127.0.0.1:1998/ping")
    music = plex_q.clean_up(plex_q.get_play_latest(data["plex_token"], api))
#    print("RPC Sent")
#    print(music[0])
    try:
      if music == last and not npc:
         pass
      else:
       img = url + music[2] + "?X-Plex-Token=" + data["plex_token"]
#       print(img)
       if music[0] == "":
        raise "2"
       RPC.update(
          large_image=img,
          large_text=music[0],
          state=music[0] + " by " + music[1],
          details="Playing on " + music[3],
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
         prev_songs.insert(0, {"songimg": url + last[2] + "?X-Plex-Token=" + data["plex_token"], "songname": last[0], "artistname": last[1], "devicename": last[3]})

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
       if sd:
        urls = url_adapt.adapt( plex_q.get_resources(data["plex_token"], shared.client_id))
        url = urls[shared.cid]["relay"]
        api = urls[shared.cid]["relay"]
       if music[4] == "purpose":
         exit(1)
       if not npc and music[4] == "offline":
         RPC.update(
            large_image="plex_icon",
            state="The server is down!",
            details="Fix it now!",
            buttons=[{"label": "History", "url": shared.dashboard_url}],
            pid=pid_c,
         )
         npc = True
         sd = True
       if tn < 6:
        if music[4] == "3rd-party":
         tn = tn + 1
        else:
         tn = 6
       elif npc:
          pass
       else:
         RPC.update(
            large_image="plex_icon",
            state="No music is playing",
            details="Play some music!",
            buttons=[{"label": "History", "url": shared.dashboard_url}],
            pid=pid_c
         )
         npc = True
    print(str(tn) + " " + str(last) + " " +str(npc)+" "+str(music))
    time.sleep(5) #Wait a wee bit


