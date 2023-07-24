from telethon import TelegramClient, events
import logging
import time
import aiofiles
import asyncio
import socket

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=logging.WARNING)

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 9013

csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
csock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
csock.listen()
conn, addr = csock.accept()

client = TelegramClient('client_listener', 1, '') # api-id, api_hash


@client.on(events.NewMessage(incoming=True))
async def my_event_handler(event):
    msg = event.raw_text
    #web = event.raw_text.split()
    #ts = web[-1]
    #print(ts)
    #if('ts' in locals()):
    #print('Time to download ' + msg + ' is :' + str(time.time()-float(ts)))
    #print("Received Text :" + msg)
    print("Received Text!!")
    msg = msg.encode('ascii')
    #clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.send(msg)

client.start()
client.run_until_disconnected()
