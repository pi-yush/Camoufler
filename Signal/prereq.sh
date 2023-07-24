#!/bin/bash
sudo apt install libunixsocket-java
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/jni/
sudo dpkg -L libunixsocket-java
