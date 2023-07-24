from telethon import TelegramClient
import time
import aiofiles
import asyncio

# Remember to use your own values from my.telegram.org!
api_id = 1
api_hash = ''
client = TelegramClient('client_requester', api_id, api_hash)

async def main():
    # Getting information about yourself
    ##me = await client.get_me()

    # "me" is an User object. You can pretty-print
    # any Telegram object with the "stringify" method:
    ##print(me.stringify())

    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    ##username = me.username
    ##print(username)
    ##print(me.phone)
    async with aiofiles.open('alexa_100.txt', mode='r') as f:
        async for website in f:
            print(website)
    
            await client.send_message('n1nj4tor', website + ' ' + str(time.time()))
            time.sleep(7)

    '''# You can print all the dialogs/conversations that you are part of:
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

    # You can print the message history of any chat:
    async for message in client.iter_messages('me'):
        print(message.id, message.text)

        # You can download media from messages, too!
        # The method will return the path where the file was saved.
        if message.photo:
            path = await message.download_media()
            print('File saved to', path)  # printed after download is done
'''
with client:
    client.loop.run_until_complete(main())
