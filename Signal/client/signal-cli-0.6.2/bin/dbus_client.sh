#!/bin/bash
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/jni/

./signal-cli --dbus send -m "URL "$1 $2

