#!/bin/bash
#input="./alexa_1000_www.txt"
input=$1
while IFS= read -r line
do
  #$newline = "https://".$line
  echo "$line"
  #time wget $line --no-check-certificate ; 2>> sample.txt
  time ./dbus_client.sh $line <destination-mobile-number-with-country-code> ; 2>> trial_results.txt
  #sleep 15
done < "$input"
