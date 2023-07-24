from telethon import TelegramClient, events
import logging
import time
import aiofiles
import asyncio

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=logging.WARNING)

client = TelegramClient('client_listener', 1182520, '')


@client.on(events.NewMessage(incoming=True))
async def my_event_handler(event):
    web, ts=event.raw_text.split()
    #print(ts)
    #if('ts' in locals()):
    print('Time to download ' + web + ' is :' + str(time.time()-float(ts)))
    #else:
    #    print('Ignored Timestamp ' + str(time.time()))
    #sender = await event.get_sender()
    #print(sender)
    #print(event)
client.start()
client.run_until_disconnected()
