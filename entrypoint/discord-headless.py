import sys
sys.path.insert(0, '..')

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from config import shared

import sys
import logging
logging.basicConfig(format='%(message)s')
logging.root.setLevel(logging.NOTSET)
handler = logging.StreamHandler(sys.stdout)
log = logging.getLogger(__name__)
log.addHandler(handler)

def print(a):
   log.info(a)
# Set the Discord token
token = shared.dtoken

# Configure Chrome WebDriver options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome WebDriver in headless mode (without UI)
chrome_options.binary_location = "../external/ungoogled-chromium_130.0.6723.58-1_linux/chrome"
chrome_options.add_argument("--proxy-server=" + shared.socks)

#DEBUG ONLY
#chrome_options.add_argument("--remote-debugging-port=9222")

service = Service("../external/ungoogled-chromium_130.0.6723.58-1_linux/chromedriver")

# Start Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options, service=service)

# Open Discord login page
driver.get("https://discord.com/channels/@me")

# Inject token using JavaScript
script = f"""
    const token = "{token}";
    setInterval(() => {{
        document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage.token = `"${{token}}"`;
    }}, 50);
    setTimeout(() => {{
        location.reload();
    }}, 2500);
"""
driver.execute_script(script)

print("(Discord Headless) Logging in")

# Wait for the login process to complete
time.sleep(10)

print(driver.current_url)

# Verify if login was successful (you can add your own logic here)
if "discord.com/channels" in driver.current_url:
    print("(Discord) Login Successful")
else:
    print("(Discord) Login Failed")
    driver.quit()
    exit()

#exit() #test

#print("(ARRPC) Injecting Token")
#driver.execute_script("let token = '" + shared.dtoken +"'")

print("(ARRPC) Script injecting")
script = open('../external/arrpc/examples/bridge_mod.js', "r")
script = script.read().replace("TOKENHERE", shared.dtoken)
driver.execute_script(script)
print("(ARRPC) Setup done")

os.system("touch ../temp/.runlock-rich")

while True:
#   for entry in driver.get_log('browser'):
#    print(entry)
   time.sleep(1)

