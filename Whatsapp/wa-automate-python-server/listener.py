#!/usr/bin/python3.6
import os
import sys
import time

from openwa import WhatsAPIDriver
from base64 import b64encode
from openwa.objects.message import Message

def run():
    

    #driver = WhatsAPIDriver(client='remote', command_executor=os.environ["SELENIUM"])
    driver = WhatsAPIDriver()
    print("Waiting for QR")
    while(driver.wait_for_login() == False):
        time.sleep(2)
    print("Bot started")
    while(True):
     for contact in driver.get_unread():
        for message in contact.messages:
            if isinstance(message, Message):
              ts=time.time()
              mess = message.content.split()
              cl_ts = float(mess[2])
              print('Time taken to receive the message : ' + str(ts-cl_ts))
              print(mess[0],mess[1],mess[2])
              wget = "timeout 10 wget -O index.html " + mess[1] + " --no-check-certificate"
              os.system(wget)
              '''filename = open('./index.html','rb')
              content = filename.read()
              print('Content Encoding')
              encoded=b64encode(content)
              #resp = driver.get_chat_from_phone_number(919868037125)
              print('Converting to ASCII')
              str_content = str(encoded)
              contact.chat.send_message(str_content)'''
              contact.chat.send_message("cont")
              #if (os.stat('index.html').st_size != 0):
              #  contact.chat.send_media('./index.html')
              #resp.send_message('Done sending')
              print("Time taken by proxy to respond: " + str(time.time() - ts) + "\n")
              time.sleep(1)

if __name__ == '__main__':
    run()

