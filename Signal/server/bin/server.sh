#!/bin/bash
# Usage <Server_Number> <timeout_value> <Client_Number>
./signal-cli -u $1 receive -t $2 | grep Body | cut -d ':' -f 2 | wget -i -
./signal-cli -u $1 send -m "Content" $3 -a index.html
