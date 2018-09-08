
# Raspberry Pi Zero - MIDI Controller

This is a project i did to make a midi controller using a Raspberry Pi Zero in "Gadget Mode" (a standalone device that's plug-and-play with a single USB cable just like every other MIDI controller).\
The script is still work in progress, at the moment i made only the "Sustain" button, but i'm planning to enhance it with more functions.

For this to work i user the g_midi module, RPI.gpio and python-rtmidi.

First follow this guide to setup the Raspberry to work as MIDI gadget, and to create a "MIDI Device" that we will use to output MIDI signals.\
[Raspberry as MIDI Device Guide](https://ixdlab.itu.dk/wp-content/uploads/sites/17/2017/10/Setting-Up-Raspberry-Pi-for-MIDI.pdf)\
(also i downloaded that PDF and uploaded in this git in the "other" folder, just to be sure not to lose it if the link goes down)

Instructions Work in progress... I'll finish this readme as soon as i can.


## Setting up the Raspberry
You will have to follow [this guide](https://blog.gbaman.info/?p=791) to enable the Programming-over-usb capability. This is needed to connect your Raspberry to your PC via usb and use it without the need of extra keyboard, mouse and screen.\
I'll write down here the steps:
1. [Flash Raspbian Full](https://www.raspberrypi.org/downloads/raspbian/) on the SD card;
2. With the SD still connected to your computer, open up the "boot" partition and find the "config.txt" file. At the bottom, on a new line, add **dtoverlay=dwc2**. Save and close the file;
3. Create a new file called **ssh** (**without** extension) in the SD card, this is required to enable SSH.
4. Open the "cmdline.txt" file. After "**rootwait**" insert **modules-load=dwc2,g_ether** (put a single space to separate rootwait and the modules... etc);
5. Eject the SD card from your computer, put it in your Raspberry and connect it via USB to your computer. Be sure to connect the USB cable on the middle micro USB port, because that port allow data transfer, the port on the "corner" is for power only.
6. Give it time to boot up, than it should be recognized from your computer. Now open a terminal window on your computer and try to ssh to the Raspberry like this: **ssh pi@raspberrypi.local**\
The default password is **raspberry**


### Requirements
python-rtmidi
RPi.GPIO

### Cronjob

### Script Usage

### Credits