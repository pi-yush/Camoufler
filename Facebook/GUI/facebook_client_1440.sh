#!/usr/bin/bash

# -------------------------
# GLOBAL VARIABLES
# -------------------------
# Res : 1440 x 900
# Zoom : 110%
# Make sure the downloads bar in chrome is visible

readonly message_server_response_x=905
readonly message_server_response_y=745

readonly chat_input_x=905
readonly chat_input_y=850

readonly server_response_folder="$HOME/"
readonly safe_place_folder="$HOME/Facebook_URLs"

get_time()
{
	date "+%s"
}

get_time_millis()
{
	date "+%s.%3N"
}

# $1 : Start time
calc_time()
{
	local tnow="$(get_time_millis)"
	echo "$tnow - $1" | bc -l
}

# $1 : File
get_time_modified()
{
	date -r "$1" "+%s"
}

# $1 : File
get_time_modified_millis()
{
	date -r "$1" "+%s.%3N"
}

# $1 : URL to be requested from server
send_url_to_server ()
{
	local time_taken="$(get_time_millis)"

	# Select the input box
	xdotool mousemove $chat_input_x $chat_input_y
	xdotool click 1

	local time="$(get_time)"
	local request_url="$1#${time}"
	# printf "Requst URL: %s" "$request_url"
	xdotool type "$request_url"
	xdotool key Return

	time_taken="$(calc_time "$time_taken")"
	printf "TT > Type and send URL : %.3f\n" "$time_taken"

	# xdotool mousemove 1230 950
	# xdotool click 1
	sleep 1s
}

download_server_response()
{
	xdotool mousemove $message_server_response_x $message_server_response_y
	xdotool click 1
}

# $1 : Folder to be polled
check_for_response_in_folder()
{
	local start_time="$(get_time_millis)"

	local folder="$1"
	local latest_file=""
	local latest_time_modified=0.0

	find "$folder" -name "*.gz" -type f -delete
	# find "$folder" -name "*.bz2" -type f -delete

	printf "Checking for new files in %s\n" "$folder"

	for ((i = 0; i <= 20; i++))
	do
		download_server_response
		sleep 1s

		file="$(ls "$folder" -t | head -1)"

		if [[ -z "$file" ]]
		then
			printf "WARNING: No file in folder\n\n" >&2
			sleep 0.1s
			continue
		fi

		# printf "Current latest file: %s %lld\n" "$latest_file" "$latest_time_modified"
		file="${folder}${file}"
		local time_modified="$(get_time_modified_millis "$file")"

		if (( $(echo "$time_modified > $start_time" | bc -l) ))
		then
			if (( $(echo "$time_modified > $latest_time_modified" | bc -l) ))
			then
				printf "New file found: %s %.3f\n" "$file" "$time_modified"

				IFS='.' read -ra temp <<< "$file"
				IFS='/' read -ra temp <<< "${temp[0]}"
				file_ctime="${temp[-1]}"

				if [[ ${#file_ctime[@]} -gt 1 ]]
				then
					printf "WARNING: Duplicate download\n" >&2
					rm "$file"
					continue
				fi


				if (( $(echo "$file_ctime > $start_time" | bc -l) ))
				then
					latest_file="$file"
					latest_time_modified="$time_modified"

					local delay=$(echo "$latest_time_modified - $start_time" | bc -l)
					local send_delay=$(echo "$latest_time_modified - $file_ctime" | bc -l)
					printf "Delay: %.3f seconds\n" "$delay"
					printf "Receive Delay: %.3f seconds\n" "$send_delay"

					# Relocate correct file
					printf "File saved as: %s\n" "$file_ctime"
					mv "$file" "${safe_place_folder}/${file_ctime}"
					return 0
				fi

			fi
		fi

		sleep 0.5s
		find "$folder" -name "*.gz" -type f -delete
		# find "$folder" -name "*.bz2" -type f -delete
		# printf "\n"
	done

	return 1
}

# $1 : URL to be requested from server
main()
{
	send_url_to_server $1
	check_for_response_in_folder "$server_response_folder"
}

# ----------------------------------------
# MAIN METHOD
# ----------------------------------------
declare -a websites=("google.com") # "youtube.com" "tmall.com" "facebook.com" "baidu.com" "sohu.com" "qq.com" "login.tmall.com" "taobao.com" "360.cn" "wikipedia.org" "jd.com" "yahoo.com" "amazon.com" "sina.com.cn" "netflix.com" "pages.tmall.com" "weibo.com" "reddit.com" "live.com" "zoom.us" "vk.com" "xinhuanet.com" "okezone.com" "blogspot.com" "alipay.com" "instagram.com" "csdn.net" "twitch.tv" "yahoo.co.jp" "microsoft.com" "bing.com" "bongacams.com" "tribunnews.com" "livejasmin.com" "office.com" "worldometers.info" "google.com.hk" "amazon.co.jp" "tianya.cn" "zhanqi.tv" "twitter.com" "stackoverflow.com" "ebay.com" "naver.com" "aliexpress.com" "google.co.in" "panda.tv" "chaturbate.com" "mama.cn" "apple.com" "pornhub.com" "microsoftonline.com" "imdb.com" "china.com.cn" "myshopify.com" "ok.ru" "yandex.ru" "mail.ru" "msn.com" "sogou.com" "adobe.com" "wordpress.com" "whatsapp.com" "imgur.com" "aparat.com" "google.co.jp" "bilibili.com" "bbc.com" "huanqiu.com" "grid.id" "google.com.br" "udemy.com" "nytimes.com" "yy.com" "primevideo.com" "kompas.com" "fandom.com" "cnn.com" "detail.tmall.com" "detik.com" "medium.com" "17ok.com" "linkedin.com" "roblox.com" "xvideos.com" "google.de" "dropbox.com" "amazon.de" "soso.com" "spotify.com" "rakuten.co.jp" "instructure.com" "discordapp.com" "ettoday.net" "hao123.com" "soundcloud.com" "walmart.com" "amazon.co.uk" "pixnet.net")


for website in "${websites[@]}"
do
	printf "Website: %s\n" "$website"
	main "$website"

	if [[ "$?" -ne 0 ]]
	then
		printf "ERROR: Couldn't fetch website\n" >&2
	fi

	printf "\n"
done

# main $1
