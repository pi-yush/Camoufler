from pydbus import SessionBus
from gi.repository import GLib
import os
import time
import io
import gzip
import shutil

def msgRcv (timestamp, source, groupID, message, attachments):
   print ("Message", message, "source", source)
   #ts = time.time()
   #mess = message.split()
   print("OWD time = " + str(time.time()-float(message)))
   

bus = SessionBus()
loop = GLib.MainLoop()

signal = bus.get('org.asamk.Signal')

signal.onMessageReceived = msgRcv
loop.run()
