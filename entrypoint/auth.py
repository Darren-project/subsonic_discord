import ngrok
import sys
sys.path.insert(0, '..')
from config import shared
import os
from flask import Flask, request
import random
import time

code = {}

app = Flask(__name__)

def end_ok():
 pass

@app.route('/')
def home():
    html = '''
    <script>
    ( async () => {
    let cj = await fetch("/api/client_id")
    let cid = await cj.text()
    let pr = await fetch("/api/product")
    let prd = await pr.text()
    let prs = await fetch('https://plex.tv/api/v2/pins', {
      method: 'POST',
      headers: {
        'Origin': window.location.host,
        'Accept': 'application/json'
      },
      body: new URLSearchParams({
        'strong': true,
        'X-Plex-Product': prd,
        'X-Plex-Client-Identifier': cid
      })
    })
    prs = await prs.json()
    await fetch('/api/update-code', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(prs)
    })
    let urrd = "https://app.plex.tv/auth#" + encodeURI("?clientID=" + cid + "&code=" + prs["code"] + "&context[device][product]=" + prd + "&forwardUrl=https://" + window.location.host + "/authdone")
    window.location.replace(urrd)
    })()
    </script>
    '''
    return html

@app.route('/api/client_id')
def push_client_id():
   return shared.client_id

@app.route('/api/product')
def push_product():
    return shared.product

@app.route('/api/update-code', methods=["POST"])
def update_code():
   global code
   code = request.get_json()
   print("Received code", code)
   return "code_done"

@app.route('/authdone')
def authdone():
   cd = os.system("python3 plex_pin.py " + code["code"] + " " + str(code["id"]))
   if cd == 0:
      end_ok()
      return "Auth done. You may close this page"
   else:
      return "Auth failed"

if __name__ == '__main__':
    # Generate a random port between 1024 and 65535
    port = random.randint(1024, 65535)
    print("Visit ", ngrok.forward(port, authtoken=shared.ngrok_auth).url(), "to auth")
    print(f"Running on port {port}")
    app.run(host='0.0.0.0', port=port)
