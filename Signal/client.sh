#!/bin/bash
# Usage : ./client.sh <Sender_Number> <Website> <Receiver_Number> <timeout>
./signal-cli -u $1 send -m "URL "$2 $3
./signal-cli -u $1 receive -t $4 | grep plaintext | cut -d ':' -f 2
