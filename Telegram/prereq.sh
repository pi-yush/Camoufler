#!/bin/bash
apt update
apt install python3-pip -y
pip3 install telethon
pip3 install asyncio
pip3 install aiofiles
cd tg_camoufler/
tmux new -s tg

