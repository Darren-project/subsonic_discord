import signal
import threading
import sys
import os
import subprocess
import logging
import time
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



# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

command = ["python3", "navidrome-rich.py"]

def webserver(state):
    app.config['STATE'] = state
    # If running on, say, a Raspberry Pi, use 0.0.0.0 so that
    # you can connect to the web server from your intranet.
    app.run(host='0.0.0.0', use_reloader=False, debug=True, port=1998)

def main():
    state = SharedState()
    web_thread = threading.Thread(target=webserver, args=(state,))
    web_thread.start()
    process = subprocess.Popen(command)
    pid = process.pid
    state.set('program_started', True)
    state.set('pid', pid)
    time.sleep(2)
    while True:
        # Do whatever you want in the foreground thread
        if state.get('program_started') == True:
          if state.get('last_ping') == True:
            state.set('last_ping', False)
          else:
            print("Restarting stalled app " + str(pid))
            state.set('program_started', False)
            state.set('last_ping', False)
            try:
              os.kill(state.get('pid'), signal.SIGTERM)
            except:
              pass
            time.sleep(2)
            process = subprocess.Popen(command)
            pid = process.pid
            time.sleep(2)
            state.set('program_started', True)
            state.set('pid', pid)
        time.sleep(7)

class SharedState():
    def __init__(self):
        self.lock = threading.Lock()
        self.state = dict()

    def get(self, key):
        with self.lock:
            return self.state.get(key)

    def set(self, key, value):
        with self.lock:
            self.state[key] = value


@app.route('/ping')
def home():
    state = app.config['STATE']
    state.set('last_ping', True)
    print("App pinged")
    return "pong"

main()
