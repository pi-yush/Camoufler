from telethon import TelegramClient, events
import logging
import time
import aiofiles
import asyncio
import os
import base64
import socket

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=logging.WARNING)

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 9014

client = TelegramClient('proxy', 1, '') # api-id, api-hash


@client.on(events.NewMessage(incoming=True))
#@client.on(events.NewMessage(incoming=True, pattern=r'abc'))
async def my_event_handler(event):
    sender = await event.get_sender()
    #print(sender.username)
    #print(event.raw_text)

    #Create a UDP socket to listen for replies from intermediary
    int_listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    int_listener.bind((UDP_IP_ADDRESS, 9015))

    text = event.raw_text
    print("New Text : " + text)
    int_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = bytes(text, 'ascii')
    int_sender.sendto(text, (UDP_IP_ADDRESS, UDP_PORT_NO))

client.start()
client.run_until_disconnected()
