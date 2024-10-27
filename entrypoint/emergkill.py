import os, signal

pids = []

try:
   f = open("../temp/pids.txt", "r")
   pd = f.read()
   pd = pd.replace("[","").replace("]","")
   pids = pd.split(",")
except:
   exit()
for i in pids:
   os.killpg(int(i), signal.SIGTERM)
   print("Killed process group", i)

os.system("rm pids.txt")
