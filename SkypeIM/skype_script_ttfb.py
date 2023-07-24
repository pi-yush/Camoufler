# -*- coding: UTF-8 -*-

from skpy import Skype, SkypeTextMsg
import time
import os


SLEEP_TIME = 0.5


def main():
	downloads_folder = r'/home/'

	client = Skype('', '') # receiver-email-id, own-email-is
	receiver_id = ''
	chat = client.contacts[receiver_id].chat

	print('      My UID:', client.user.id)
	print('Receiver UID:', receiver_id)

	start_time = time.time()

	for i in range(20000):
		messages = chat.getMsgs()
		if len(messages) == 0:
			time.sleep(SLEEP_TIME)
			continue

		substrings = []
		for message in messages:
			if isinstance(message, SkypeTextMsg) and len(message.content) != 0:
				print(message.content)
				substrings = message.content.split(' ')
				break

		if len(substrings) < 2:
			# print('ERROR: Invalid message')
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
		#file_to_send = downloads_folder + cur_time + '.gz'
		#os.system('gzip < ' + downloads_folder + 'index.html > ' + file_to_send)

		chat.sendMsg('A')
		# with open(file_to_send, 'rb') as f:
		# 	chat.sendFile(f, cur_time + '.gz')

		# os.system('rm ' + file_to_send)
		print()
		time.sleep(SLEEP_TIME)


if __name__ == '__main__':
	main()
