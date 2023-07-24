from pydbus import SessionBus
from gi.repository import GLib
import os
import time
import io
import gzip
import shutil

def msgRcv (timestamp, source, groupID, message, attachments):
   print ("Message", message, "source", source)
   ts = time.time()
   if (message.find("URL") >= 0):
       mess = message.split()
       wget = "timeout 10 wget -O index.html " + mess[1] + " --no-check-certificate"
       os.system(wget)
       #filename = open('./index.html','r')
       #content = filename.read()
       #encoded = content.encode('base64')
       
       with open('./index.html', 'rb') as f_in, gzip.open('./index.html.gz', 'wb') as f_out:
           shutil.copyfileobj(f_in, f_out)
       
       filename = open('./index.html.gz','r')
       content = filename.read()
       encoded = content.encode('base64')
       #print(encoded)
       ts1=time.time()
       #os.system("./signal-cli --dbus send -m 'Content' " + source + " -a index.html")
       os.system("./signal-cli --dbus send -m '" + encoded + "' " + source)
       os.system("rm index.html*")
       print("Time taken by proxy : " + str(time.time()-ts) + "\ntime to send : " + str(time.time()-ts1))
   return

#from pydbus import SessionBus
#from gi.repository import GLib

bus = SessionBus()
loop = GLib.MainLoop()

signal = bus.get('org.asamk.Signal')

signal.onMessageReceived = msgRcv
loop.run()
