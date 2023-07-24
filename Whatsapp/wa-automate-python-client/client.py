import time
from openwa import WhatsAPIDriver
from openwa.objects.message import Message

driver = WhatsAPIDriver()
print("Waiting for QR")
while(driver.wait_for_login() == False):
    time.sleep(2)

print("Client Bot started")

proxy = driver.get_chat_from_phone_number('')

f = open('alexa_1000.txt','r')
for files in f:
  ts = time.time()
  proxy.send_message('URL https://' + files + ' ' + str(time.time()))
  wait_time = 0
  recv = 0
  while(wait_time != 15):
    for contact in driver.get_unread():
      if (contact.chat == proxy):
        #print('Content for ' + files + ' received')
        #print(contact.messages)
        recv = 1
        break
    if(recv == 1):
      break
    time.sleep(1)
    wait_time = wait_time + 1
  if(recv == 1):
    print('Time to download ' + files + ' = ' + str(ts-time.time()))
