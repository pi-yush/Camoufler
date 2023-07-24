# -*- coding: UTF-8 -*-

from skpy import Skype, SkypeFileMsg, SkypeTextMsg
from urllib.request import urlopen
import time
import os


SLEEP_TIME = 0.5


def main():
	downloads_folder = r'/home/'
	safe_folder = r'/home/Downloaded_HTMLs/'
	log_file = r'/home/skype_ttfb.txt'

	client = Skype('', '') # receiver-email-id, own-email-is
	receiver_uid = '' 
	chat = client.contacts[receiver_uid].chat

	print('      My UID:', client.user.id)
	print('Receiver UID:', receiver_uid)

	websites = ['pages.tmall.com', 'weibo.com', 'reddit.com', 'live.com', 'zoom.us']

	# for website in websites[websites.index('redd.it') : ]:
	for website in websites:
		for i in range(1,100):
			print('\nWebsite:', website)
			with open(log_file, 'a') as f:
				f.write('\nWebsite: '+ website + '\n')

			start_time = int(time.time())
			cur_time = str(start_time)
			url = website + ' ' + cur_time

			chat.sendMsg(url)

			got_response = False
			server_error = False
			for i in range(40):
				messages = chat.getMsgs()
				if len(messages) == 0 or messages is None:
					time.sleep(SLEEP_TIME)
					continue

				for message in messages:
					if message.userId != receiver_uid:
						continue

					if isinstance(message, SkypeTextMsg):
						send_time = int(message.id) // 1000
						if message.content == 'FAILURE' and send_time >= start_time:
							print('ERROR: Server unable to fetch website')
							server_error = True
							break

						if message.content == 'A':
							time_now = time.time()
							print('Delay: ', time_now - start_time)

							with open(log_file, 'a') as f:
								f.write('Delay: ' + str(time_now - start_time) + '\n')

							start_time = time_now
							got_response = True
							break

				# else:
				# 	print('WARNING: Old file')

				if got_response or server_error:
					break

				time.sleep(SLEEP_TIME)


		if not got_response:
			print('ERROR: Unable to obtain file')
			with open(log_file, 'a') as f:
				f.write('ERROR: Unable to obtain file\n')


if __name__ == '__main__':
	main()
