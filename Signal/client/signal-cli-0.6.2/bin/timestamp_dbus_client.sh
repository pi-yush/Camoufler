#!/bin/bash
# Usage : ./client.sh <Sender_Number> <Website> <Receiver_Number> <timeout>
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/jni/
TS=`date +%s.%6N`
./signal-cli --dbus send -m "URL "$1" "$TS $2
#./signal-cli -u $1 receive -t $4 | grep plaintext | cut -d ':' -f 2
