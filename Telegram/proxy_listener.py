from telethon import TelegramClient, events
import logging
import time
import aiofiles
import asyncio
import os

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=logging.WARNING)

client = TelegramClient('proxy', 1247726, '')


#@client.on(events.NewMessage(incoming=True))
@client.on(events.NewMessage(incoming=True, pattern=r'\www'))
async def my_event_handler(event):
    sender = await event.get_sender()
    #print(sender.username)
    #print(event.raw_text)
    text = event.raw_text
    web,ts = text.split()
    filename = web + '.html'
    curr_ts = time.time()
    p1 = time.time()-float(ts)
    print('Received request for ' + web + ' with timestamp '+ ts)
    #print("Time taken to receive by proxy : " + str(p1))
    os.system('timeout 5 wget -O ' + filename + ' https://' + web)
    if(os.stat(filename).st_size != 0):
        #os.system('mv index.html ' + filename)
        #await client([SendMessageRequest(sender.username, web + ' ' + ts, file = filename)])
        await client.send_message(sender.username, web + ' ' + ts, file = filename)
    os.system('rm ' + filename)
    p2 = time.time() - curr_ts

client.start()
client.run_until_disconnected()
