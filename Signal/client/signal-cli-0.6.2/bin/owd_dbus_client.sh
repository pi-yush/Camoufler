#!/bin/bash
# Usage : ./client.sh <Sender_Number> <Website> <Receiver_Number> <timeout>
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/jni/

./signal-cli --dbus send -m $1 $2
#./signal-cli -u $1 receive -t $4 | grep plaintext | cut -d ':' -f 2
