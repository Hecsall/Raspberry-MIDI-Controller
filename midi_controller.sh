#!/bin/sh
# footswitch.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/midi_controller
sudo python3 midi_controller.py
cd /