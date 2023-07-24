from telethon import TelegramClient
import time
import aiofiles
import asyncio
import sys

# Remember to use your own values from my.telegram.org!
api_id = 1
api_hash = ''
client = TelegramClient('client_requester', api_id, api_hash)

async def main():
    await client.send_message('', str(sys.argv[1] + ' ' + str(time.time())))
    
with client:
    client.loop.run_until_complete(main())
