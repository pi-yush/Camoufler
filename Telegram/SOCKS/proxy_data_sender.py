from telethon import TelegramClient
import time
import aiofiles
import asyncio
import sys

# Remember to use your own values from my.telegram.org!
api_id = 1
api_hash = ''
client = TelegramClient('proxy_data_sender', api_id, api_hash)

async def main():
    
    await client.send_message('imclient', str(sys.argv[1]))

with client:
    client.loop.run_until_complete(main())
