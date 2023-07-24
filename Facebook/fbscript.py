# -*- coding: UTF-8 -*-

from itertools import islice
from fbchat import Client
from fbchat.models import *
import time
import os

# Use the below lines to find the receiver-uid
# client.send(Message(text='Hi me!'), thread_id=receiver_uid, thread_type=ThreadType.USER)
# client.sendLocalFiles(file_paths=[''], thread_id=receiver_uid, thread_type=ThreadType.USER)

SLEEP_TIME = 0.5


def main():
	downloads_folder = r'' # path you want to save the websites to

	client = Client('', '') # Receiver-email-ID, own-email-id 
	receiver_uid = ''  

	print('      My UID:', client.uid)
	print('Receiver UID:', receiver_uid)

	start_time = time.time()

	for i in range(20000):
		messages = client.fetchThreadMessages(thread_id=receiver_uid, limit=5)
		if len(messages) == 0:
			time.sleep(SLEEP_TIME)
			continue

		substrings = []
		for message in messages:
			if len(message.text) != 0:
				substrings = message.text.split(' ')
				break

		if len(substrings) < 2:
			print('ERROR: Invalid message')
			time.sleep(SLEEP_TIME)
			continue

		timestamp = int(substrings[-1])
		if timestamp < start_time:
			# print('WARNING: Old message')
			time.sleep(SLEEP_TIME)
			continue

		url = 'www.' + '.'.join(substrings[:-1])
		print('URL:', url)

		# Save file as index.html
		os.system('wget -q --timeout=4s --tries=2 ' + url + ' -O ' + downloads_folder + 'index.html')

		if os.path.getsize(downloads_folder + 'index.html') == 0:
			print('ERROR: wget failed\n')
			chat.sendMsg('FAILURE')
			continue

		# Update start time
		start_time = time.time()
		cur_time = str(int(start_time))
		file_to_send = downloads_folder + cur_time + '.txt'
		os.system('gzip < ' + downloads_folder + 'index.html > ' + file_to_send)

		client.sendLocalFiles(file_paths=[file_to_send], thread_id=receiver_uid, thread_type=ThreadType.USER)

		os.system('rm ' + file_to_send)
		print()
		time.sleep(SLEEP_TIME)

	client.logout()


if __name__ == '__main__':
	main()
