from __future__ import print_function
import sys

import logging
# logging.basicConfig(level=logging.DEBUG)

from slack import WebClient
from slackeventsapi import SlackEventAdapter
import os
import json
import time
import pprint
from urllib.request import urlopen

website_idx = 0

SLEEP_TIME = 0.7 # seconds
pp = pprint.PrettyPrinter(indent=2)

def print_error(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)


def get_space_separated_url(website: str, ts: str):
	while '.' in website:
		website = website.replace('.', ' ')

	return website + ' ' + ts

websites = ['tmall.com', 'facebook.com', 'baidu.com', 'sohu.com', 'qq.com', 'login.tmall.com', 'taobao.com', '361.cn', 'wikipedia.org', 'jd.com', 'yahoo.com', 'amazon.com', 'sina.com.cn', 'netflix.com', 'pages.tmall.com', 'weibo.com', 'reddit.com', 'live.com']

#website_idx = 0

def main():
	downloads_folder = r''
	safe_folder = r''
	log_file = r''

	bot_id = ''
	channel_id = ''
	channel_name = ''

	user_token = ''
	slack_signing_secret = ''
	slack_bot_token = ''

	client = WebClient(token=user_token)
	# websites = ['google.com', 'youtube.com', 'tmall.com', 'facebook.com', 'baidu.com', 'sohu.com', 'qq.com', 'login.tmall.com', 'taobao.com', '360.cn', 'wikipedia.org', 'jd.com', 'yahoo.com', 'amazon.com', 'sina.com.cn', 'netflix.com', 'pages.tmall.com', 'weibo.com', 'reddit.com', 'live.com', 'zoom.us', 'vk.com', 'xinhuanet.com', 'okezone.com', 'blogspot.com', 'alipay.com', 'instagram.com', 'csdn.net', 'twitch.tv', 'yahoo.co.jp', 'microsoft.com', 'bing.com', 'bongacams.com', 'tribunnews.com', 'livejasmin.com', 'office.com', 'worldometers.info', 'google.com.hk', 'amazon.co.jp', 'tianya.cn', 'zhanqi.tv', 'twitter.com', 'stackoverflow.com', 'ebay.com', 'naver.com', 'aliexpress.com', 'google.co.in', 'panda.tv', 'chaturbate.com', 'mama.cn', 'apple.com', 'pornhub.com', 'microsoftonline.com', 'imdb.com', 'china.com.cn', 'myshopify.com', 'ok.ru', 'yandex.ru', 'mail.ru', 'msn.com', 'sogou.com', 'adobe.com', 'wordpress.com', 'whatsapp.com', 'imgur.com', 'aparat.com', 'google.co.jp', 'bilibili.com', 'bbc.com', 'huanqiu.com', 'grid.id', 'google.com.br', 'udemy.com', 'nytimes.com', 'yy.com', 'primevideo.com', 'kompas.com', 'fandom.com', 'cnn.com', 'detail.tmall.com', 'detik.com', 'medium.com', '17ok.com', 'linkedin.com', 'roblox.com', 'xvideos.com', 'google.de', 'dropbox.com', 'amazon.de', 'soso.com', 'spotify.com', 'rakuten.co.jp', 'instructure.com', 'discordapp.com', 'ettoday.net', 'hao123.com', 'soundcloud.com', 'walmart.com', 'amazon.co.uk', 'pixnet.net']

	# for website in websites:
	for website in websites:
		for i in range(1,100):
			#website = websites[website_idx]
			print('\nWebsite:', website)
			with open(log_file, 'a') as f:
				f.write('\nWebsite: '+ website + '\n')

			start_time = int(time.time())
			request_url = get_space_separated_url(website, str(start_time))
			client.chat_postMessage(text=request_url, channel=channel_id)

			got_response = False
			for _ in range(40):
				response = client.conversations_history(channel=channel_id, limit=1)
	
				if not response['ok']:
					print_error('ERROR: Some error occured')
					time.sleep(SLEEP_TIME)
					continue
	
				messages = response['messages']
				if len(messages) == 0:
					print_error('WARNING: No messages matched query')
					time.sleep(SLEEP_TIME)
					continue
	
				message = messages[0]
				if ('bot_id' in message) and (message['bot_id'] == bot_id):
					print_error('SKIP: Message from self')
					time.sleep(SLEEP_TIME)
					continue
	
				elif ('text' in message) and (message['text'] == 'FAILURE'):
					print_error('ERROR: Server could not fetch file')
					time.sleep(SLEEP_TIME)
					break

				elif 'files' not in message:
					print_error('SKIP: Not a file message')
					time.sleep(SLEEP_TIME)
					continue
	
				attachments = message['files']
				if len(attachments) == 0:
					print_error('ERROR: No files')
					time.sleep(SLEEP_TIME)
					continue

				attachment = attachments[0]
				print(attachment['name'])

				file_ctime = int(attachment['name'].split('.')[0])
				if file_ctime >= start_time:
					download_url = attachment['url_private_download']
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

					start_time = int(time_now)
					got_response = True
					break

				else:
					print_error('WARNING: Old file')


			if not got_response:
				print_error('ERROR: Unable to obtain file')
				with open(log_file, 'a') as f:
					f.write('ERROR: Unable to obtain file\n')

			#website_idx += 1
			time.sleep(SLEEP_TIME)


if __name__ == '__main__':
	main()
