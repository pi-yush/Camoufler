from __future__ import print_function
import sys

import logging
# logging.basicConfig(level=logging.DEBUG)

import os
import json
import time
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import pprint


SLEEP_TIME = 0.7 # seconds
pp = pprint.PrettyPrinter(indent=2)


def print_error(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)


def main():
	downloads_folder = r''
	start_time = time.time()

	bot_id = ''
	channel_id = ''

	user_token = ''
	slack_signing_secret = ''
	slack_bot_token = ''

	client = WebClient(token=user_token)

	for _ in range(20000):
		response = client.conversations_history(channel=channel_id, limit=1)

		if not response['ok']:
			print_error('ERROR: Some error occured')
			time.sleep(SLEEP_TIME)
			continue

		messages = response['messages']
		if len(messages) == 0:
			print_error('WARNING: No messages')
			time.sleep(SLEEP_TIME)
			continue

		message = messages[0]
		#print(message)
		substrings = []
		if ('bot_id' in message) and (message['bot_id'] == bot_id):
			print_error('SKIP: Message from self')
			time.sleep(SLEEP_TIME)
			continue

		elif 'text' not in message:
			print_error('SKIP: Not a text message')
			time.sleep(SLEEP_TIME)
			continue

		elif len(message['text']) == 0:
			print_error('SKIP: Empty text message')
			time.sleep(SLEEP_TIME)
			continue

		elif message['text'] == 'FAILURE':
			print_error('SKIP: Failure message from self')
			time.sleep(SLEEP_TIME)
			continue

		else:
			substrings = message['text'].split(' ')


		timestamp = int(substrings[-1])
		if timestamp < start_time:
			print_error('WARNING: Old message')
			time.sleep(SLEEP_TIME)
			continue

		url = 'www.' + '.'.join(substrings[:-1])
		print('URL:', url, '\t', timestamp)

		# Save file as index.html
		os.system('wget -q --timeout=4s --tries=2 ' + url + ' -O ' + downloads_folder + 'index.html')

		if os.path.getsize(downloads_folder + 'index.html') == 0:
			print_error('ERROR: wget failed\n')
			client.chat_postMessage(text='FAILURE', channel=channel_id)
			continue

		# Update start time
		start_time = time.time()
		cur_time = str(int(start_time))
		file_to_send = downloads_folder + cur_time + '.gz'
		os.system('gzip < ' + downloads_folder + 'index.html > ' + file_to_send)

		client.files_upload(channels=channel_id, 
							file=file_to_send, 
							filename=cur_time+'.gz',
							filetype='gzip',
							title='Response')

		os.system('rm ' + file_to_send)
		print()
		time.sleep(SLEEP_TIME)


if __name__ == '__main__':
	while True:
		try:
			main()
		except Exception as e:
			print('Exception occured:', e)
			time.sleep(2)
