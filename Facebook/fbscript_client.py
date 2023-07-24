# -*- coding: UTF-8 -*-

from itertools import islice
from fbchat import Client
from fbchat.models import *
import time
import os
from urllib.request import urlopen


# client.send(Message(text='Hi me!'), thread_id=receiver_uid, thread_type=ThreadType.USER)
# client.sendLocalFiles(file_paths=[''], thread_id=receiver_uid, thread_type=ThreadType.USER)

SLEEP_TIME = 0.5

def main():
	downloads_folder = r''
	safe_folder = r''
	log_file = r''

	client = Client('practicensl@gmail.com', 'hungamma@123') # receiver-email-id, own-email-id
	receiver_uid = ''

	print('      My UID:', client.uid)
	print('Receiver UID:', receiver_uid)

	websites = ['google.com', 'youtube.com', 'tmall.com', 'facebook.com', 'baidu.com', 'sohu.com', 'qq.com', 'login.tmall.com', 'taobao.com', '360.cn', 'wikipedia.org', 'jd.com', 'yahoo.com', 'amazon.com', 'sina.com.cn', 'netflix.com', 'pages.tmall.com', 'weibo.com', 'reddit.com', 'live.com', 'zoom.us', 'vk.com', 'xinhuanet.com', 'okezone.com', 'blogspot.com', 'alipay.com', 'instagram.com', 'csdn.net', 'twitch.tv', 'yahoo.co.jp', 'microsoft.com', 'bing.com', 'bongacams.com', 'tribunnews.com', 'livejasmin.com', 'office.com', 'worldometers.info', 'google.com.hk', 'amazon.co.jp', 'tianya.cn', 'zhanqi.tv', 'twitter.com', 'stackoverflow.com', 'ebay.com', 'naver.com', 'aliexpress.com', 'google.co.in', 'panda.tv', 'chaturbate.com', 'mama.cn', 'apple.com', 'pornhub.com', 'microsoftonline.com', 'imdb.com', 'china.com.cn', 'myshopify.com', 'ok.ru', 'yandex.ru', 'mail.ru', 'msn.com', 'sogou.com', 'adobe.com', 'wordpress.com', 'whatsapp.com', 'imgur.com', 'aparat.com', 'google.co.jp', 'bilibili.com', 'bbc.com', 'huanqiu.com', 'grid.id', 'google.com.br', 'udemy.com', 'nytimes.com', 'yy.com', 'primevideo.com', 'kompas.com', 'fandom.com', 'cnn.com', 'detail.tmall.com', 'detik.com', 'medium.com', '17ok.com', 'linkedin.com', 'roblox.com', 'xvideos.com', 'google.de', 'dropbox.com', 'amazon.de', 'soso.com', 'spotify.com', 'rakuten.co.jp', 'instructure.com', 'discordapp.com', 'ettoday.net', 'hao123.com', 'soundcloud.com', 'walmart.com', 'amazon.co.uk', 'pixnet.net']


	for website in websites:
		print('\nWebsite:', website)
		with open(log_file, 'a') as f:
			f.write('\nWebsite: '+ website + '\n')

		start_time = int(time.time())
		cur_time = str(start_time)
		url = website + ' ' + cur_time

		try:
			client.send(Message(text=url), thread_id=receiver_uid, thread_type=ThreadType.USER)
		except Exception as e:
			with open(log_file, 'a') as f:
				f.write('Exception occured\n')

			continue

		got_response = False
		server_error = False
		for i in range(40):
			messages = client.fetchThreadMessages(thread_id=receiver_uid, limit=5)
			if len(messages) == 0 or messages is None:
				time.sleep(SLEEP_TIME)
				continue

			for message in messages:
				# if message.author != receiver_uid:
				# 	continue

				if len(message.text) != 0 and message.text == 'FAILURE':
					print('TS:', message.timestamp)
					if message.timestamp >= start_time:
						print('ERROR: Server unable to fetch website')
						server_error = True
						break

				if len(message.attachments) > 0:
					attachment = message.attachments[0]
					file_ctime = int(attachment.name.split('.')[0])

					if file_ctime >= start_time:
						page = urlopen(attachment.url)
						if 'Refresh' not in page.headers:
							print('ERROR: URL not found in headers')

						download_url = page.headers['Refresh'][6:]
						file_path = safe_folder + str(file_ctime) + '.gz'
						with open(file_path, 'wb') as f:
							content = urlopen(download_url).read()
							f.write(content)


						time_now = time.time()
						print('Delay: ', time_now - start_time)
						print('Receive Delay:', time_now - file_ctime)

						with open(log_file, 'a') as f:
							f.write('Delay: ' + str(time_now - start_time) + '\n')
							f.write('Receive Delay: ' + str(time_now - file_ctime) + '\n')

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

	client.logout()


if __name__ == '__main__':
	main()
