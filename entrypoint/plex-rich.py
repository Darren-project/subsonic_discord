import sys
sys.path.insert(0, '..')
from component import url_adapt
from pypresence import Presence
import time
import random
from config import shared
import sys
import os

last = {}
tn = 0
npc = False

import logging
logging.basicConfig(format='%(message)s')
logging.root.setLevel(logging.NOTSET)
handler = logging.StreamHandler(sys.stdout)
log = logging.getLogger(__name__)
log.addHandler(handler)
def print(a):
    log.info(a)

def startlock():
 try:
  r = open("../temp/.runlock-rich","r")
  r.close()
  return True
 except:
  return False



print("Waiting for discord-headless")

while not startlock():
   pass

print("Starting")
os.system("rm  ../temp/.runlock-rich")

pid_c = int(str(random.randint(0,5)) + str(random.randint(0,5)) + str(random.randint(0,5)) + str(random.randint(0,5)))

client_id = shared.d_app_cid  # Put your Client ID here, this is a fake ID
RPC = Presence(client_id)  # Initialize the Presence class
RPC.connect()  # Start the handshake loop

import json
from component import plex_q



# Open and read the JSON file
with open('../config/plex_token.json', 'r') as file:
    data = json.load(file)

urls = url_adapt.adapt( plex_q.get_resources(data["plex_token"], shared.client_id))
url = urls[shared.cid]

while True:  # The presence will stay on as long as the program is running
    music = plex_q.clean_up(plex_q.get_play_latest(data["plex_token"], url))
#    print("RPC Sent")
#    print(music[0])
    try:
      if music == last and not npc:
         pass
      else:
       img = url + music[2] + "?X-Plex-Token=" + data["plex_token"]
#       print(img)
       RPC.update(
          large_image=img,
          large_text=music[0],
          small_image=music[4],
          small_text=music[3],
          state="Currently playing " + music[0] + " by " + music[1],
          details="Playing on " + music[5],
          pid=pid_c
       )
       last = music
       tn = 0
       npc = False
    except:
#       pass
       if tn < 6:
         tn = tn + 1
       elif npc:
          pass
       else:
         RPC.update(
            large_image="plex_icon",
            state="No music is playing",
            details="Play some music!",
            pid=pid_c
         )
         npc = True
    print(str(tn) + " " + str(last) + " " +str(npc)+" "+str(music))
    time.sleep(5) #Wait a wee bit
