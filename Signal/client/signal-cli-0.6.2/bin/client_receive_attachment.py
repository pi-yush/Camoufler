from pydbus import SessionBus
from gi.repository import GLib
import os
import gzip
import time
#import base64

def msgRcv (timestamp, source, groupID, message, attachments):
   #print ("Message", message.decode('base64'), "source", source, "Attachment link", attachments)
   #print ("source", source, "Attachment link", attachments)
   print ("Time to download : " + str(time.time() - float(message)))   
   

   '''#with gzip.open('file.txt.gz', 'rb') as f:
   #   file_content = f.read()
   decoded = message.decode('base64')
   open('./index.html.gz','w').write(decoded)
   with gzip.open('./index.html.gz', 'rb') as f:
      file_content = f.read()
   #ascii_message = message.encode('ascii')
   #decoded_bytes = base64.b64decode(message.encode('ascii'))
   #decoded = decoded_bytes.decode('ascii')
   saved_content = open('./index.html','w')
   #saved_content.write(message.decode('base64'))
   #saved_content.write(file_content.decode('base64'))
   saved_content.write(file_content)
   saved_content.close()'''
   return

#from pydbus import SessionBus
#from gi.repository import GLib

bus = SessionBus()
loop = GLib.MainLoop()

signal = bus.get('org.asamk.Signal')

signal.onMessageReceived = msgRcv
loop.run()
