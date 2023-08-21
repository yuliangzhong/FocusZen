#!/bin/bash
cd ~/GitHub/FocusZen
nohup python3 focus_zen_main.py &
rm nohup.out
# exit
kill -HUP $PPID