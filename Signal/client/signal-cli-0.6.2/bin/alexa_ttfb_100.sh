#!/bin/bash
input="./alexa_20_www.txt"
while IFS= read -r line
do
  #$newline = "https://".$line
  #for i in (1..100)
  for ((i=1;i<=100;i++));
  do
	echo "$line"
	#time wget $line --no-check-certificate ; 2>> sample.txt
	time ./dbus_client.sh $line <destination-mobile-number-with-country-code> ; 2>> ttfb_download_time_alexa.txt
	sleep 15
  done
done < "$input"
