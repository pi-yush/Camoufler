## Telegram implementation of Camoufler

## About
This repository is about tunelling web traffic through the Telegram Messenger using the Telethon library.

## Dependncies & Requisites
- Telethon
- asyncio
- aiofiles
- You would additionaly require to get the API_ID and API_HASH for both the client and the server.
- Add the corrsponding values of API in the respectve files (proxy_listener/client_listener/client_requester), before proceeding.

## How to run
1. Make sure that the dependencies are installed.
2. Execute the proxy_listener.py on the server side.
4. Execute the client_listener.py anywhere to calculate the time taken to fetch the web pages.
3. Then execute the client_requester.py on the client side to request web pages.

