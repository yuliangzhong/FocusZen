#!/bin/bash
cd ~/GitHub/FocusZen
nohup python3 main.py &
rm nohup.out
# exit
kill -HUP $PPID