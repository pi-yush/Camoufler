#!/usr/bin/bash

# -------------------------
# GLOBAL VARIABLES
# -------------------------
# Zoom : 110%

readonly contact_client_request_x=300
readonly contact_client_request_y=350

readonly contact_server_response_x=300
readonly contact_server_response_y=430

readonly message_client_request_x=892
readonly message_client_request_y=750

readonly chat_input_x=892
readonly chat_input_y=865

readonly send_button_x=1130;
readonly send_button_y=880;

readonly attachment_symbol_x=1015
readonly attachment_symbol_y=885

readonly copy_link_address_offset_x=2
readonly copy_link_address_offset_y=-90

readonly url_prefix="https://www."

get_time()
{
	date "+%s"
}

get_time_millis()
{
	date "+%s.%3N"
}

# $1 : Starting time
calc_time()
{
	local tnow="$(get_time_millis)"
	echo "$tnow - $1" | bc -l
}

# Retrieve URL from the chat
retrieve_url ()
{
	# Place mouse to the left of recent message
	xdotool mousemove $message_client_request_x $message_client_request_y

	# Triple click to highlight link
	xdotool click 1
	xdotool click 1
	xdotool click 1

	# Copy link
	xdotool key ctrl+c

	# Output the URL
	xclip -o
}

# $1 is the URL to be downloaded
download_url ()
{
	local time_taken="$(get_time_millis)"
	wget $1 --timeout=4s --tries=3

	if [[ "$?" -ne 0 ]]
	then
		printf "ERROR: wget failed\n" >&2
		return 1
	fi

	time_taken="$(calc_time "$time_taken")"
	printf "TT > wget: %.3f" "$time_taken"

	if [[ "$2" == "--copy-to-clipboard" ]]
	then
		cat index.html | xclip -selection clipboard
	fi
}

# Send the compressed version of the HTML
compress_file ()
{
	local cur_time=$(get_time)

	if [[ "$1" == "--gzip" ]]
	then
		gzip < "index.html" > "${cur_time}.gz"
		cat "${cur_time}.gz" | xclip -selection clipboard

	elif [[ "$1" == "--bzip2" ]]
	then
		bzip2 < "index.html" > "${cur_time}.bz2"
		cat "${cur_time}.bz2" | xclip -selection clipboard

	else
		echo "No compression done"
		cat "index.html" | xclip -selection clipboard
	fi
}

# Paste content copied in clipboard in input box
# $1 : Type of encryption : gzip, bzip2 or None (leave blank)
send_response_as_text ()
{
	compress_file $1

	# Select the Server Response chat
	xdotool mousemove $contact_server_response_x $contact_server_response_y
	xdotool click 1

	# Not needed, as it gets selected automatically
	# xdotool mousemove $chat_input_x $chat_input_y
	# xdotool click 1

	xdotool key ctrl+v
	sleep 1s
	xdotool key Return

	# Remove index.html files, so that next time file name doesn't change
	rm index.html
}

# Send content as a Document's attachment 
# $1 : Type of encryption : gzip, bzip2 or None (leave blank)
send_response_as_attachment ()
{
	local time_taken="$(get_time_millis)"

	# Click on the attach file button
	xdotool mousemove $attachment_symbol_x $attachment_symbol_y
	xdotool click 1

	time_taken="$(calc_time "$time_taken")"
	printf "TT > Open attachment prompt: %.3f\n" "$time_taken"

	time_taken="$(get_time_millis)"

	local cur_time="$(get_time)"
	local file_name="index.html"

	if [[ "$1" == "--gzip" ]]
	then
		file_name="${cur_time}.gz"
		gzip < "index.html" > "$file_name"

	elif [[ "$1" == "--bzip2" ]]
	then
		file_name="${cur_time}.bz2"
		bzip2 < "index.html" > "$file_name"

	elif [[ "$1" == "--txt" ]]
	then
		file_name="${cur_time}.txt"
		mv "index.html" "$file_name"
		gzip < "index.html" > "$file_name"
	fi

	if ! [[ -f "$file_name" ]]
	then
		xdotool key Escape
		printf "ERROR: File not found\n" >&2
		return 1
	fi

	# Type the file name
	xdotool sleep 0.25s
	xdotool type "$cur_time" # "$file_name"
	xdotool sleep 0.1s
	xdotool key Return

	time_taken="$(calc_time "$time_taken")"
	printf "TT > Type name in prompt: %.3f\n" "$time_taken"

	time_taken="$(get_time_millis)"

	# Send attachment
	sleep 0.8s
	xdotool mousemove $send_button_x $send_button_y
	# sleep 0.1s
	xdotool click 1
	# sleep 0.1s
	# xdotool key Return

	time_taken="$(calc_time "$time_taken")"
	printf "TT > Send attachment: %.3f\n" "$time_taken"

	# Remove index.html files, so that next time file name doesn't change
	sleep 0.5s
	rm index.html*
	rm "${cur_time}"*
}

main()
{
	local url=""
	local last_timestamp="$(get_time)"

	for ((i = 0; i <= 2000; i++ ))
	do
		printf "\n"
		local time_taken="$(get_time_millis)"
		url="https://www.$(retrieve_url)"
		time_taken="$(calc_time "$time_taken")"
		printf "TT > Get URL from client: %.3f\n" "$time_taken"

		if [[ -z "$url" ]]
		then
			printf "ERROR: Empty URL\n" >&2
			continue
		fi

		printf "Retrieved URL: %s\n" "$url"

		IFS='#' read -ra url_timestamp <<< "$url"
		url="${url_timestamp[0]}"
		timestamp="${url_timestamp[1]}"

		printf "URL: %s    TS: %lld\n" "$url" "$timestamp"

		if [[ -z "$timestamp" ]]
		then
			printf "ERROR: Empty Timestamp\n" >&2
			continue
		fi

		if [[ "$timestamp" == "exit" ]]
		then
			break
		fi

		if (( "$timestamp" >= "$last_timestamp" ))
		then
			printf "Retrieved URL: %s\n" "$url"
			printf "Timestamp %lld is more recent\n" "$timestamp"
			last_timestamp="$(get_time)"

			download_url "$url"
			# send_response_as_text --bzip2
			send_response_as_attachment --txt
		# else
			# printf "%lld is an old timestamp\n" "$timestamp"
		fi

		sleep 0.5s
	done
}

# ----------------------------------------
# MAIN METHOD
# ----------------------------------------
main
