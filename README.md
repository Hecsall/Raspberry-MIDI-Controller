
# Raspberry Pi Zero - MIDI Controller

This is a project i did to make a midi controller using a Raspberry Pi Zero in "Gadget Mode" (a standalone device that's plug-and-play with a single USB cable just like every other MIDI controller).\
The script is still work in progress, at the moment i made only the "Sustain" button, but i'm planning to enhance it with more functions.

For this to work i user the g_midi module, gpiozero and python-rtmidi.


## Setting up the Raspberry
You will have to follow [this guide](https://blog.gbaman.info/?p=791) to enable the Programming-over-usb capability. This is needed to connect your Raspberry to your PC via usb and use it without the need of extra keyboard, mouse and screen.\
I'll write down here the steps:
1. [Flash Raspbian Full](https://www.raspberrypi.org/downloads/raspbian/) on the SD card;
2. With the SD still connected to your computer, open up the "boot" partition and find the "config.txt" file. At the bottom, on a new line, add `dtoverlay=dwc2`. Save and close the file;
3. Create a new file called **ssh** (**without** extension) in the SD card, this is required to enable SSH.
4. Open the "cmdline.txt" file. After "**rootwait**" insert `modules-load=dwc2,g_ether` (put a single space to separate rootwait and the modules... etc);
5. Eject the SD card from your computer, put it in your Raspberry and connect it via USB to your computer. Be sure to connect the USB cable on the middle micro USB port, because that port allow data transfer, the port on the "corner" is for power only.
6. Give it time to boot up, than it should be recognized from your computer. Now open a terminal window on your computer and try to ssh to the Raspberry like this:\
`ssh pi@raspberrypi.local`\
The default password is **raspberry**
7. Now that we are in, we need internet to install things. So, issue a `sudo raspi-config` and under the Network settings connect to a WiFi network and you are done.\
*NOTE:* once connected to the WiFi, use `ifconfig` and write down your wlan0 IP address, because once we setup the Raspberry as MIDI device, we won't be able to use raspberrypi.local to SSH to it, we will need to SSH using `ssh pi@<ip_address>`.

Now we can work on the raspberry, later we will set it as MIDI device.

### Requirements
First of all, make sure Raspbian is updated:\
`sudo apt-get update`

This script uses **Python 3**, so make sure to have it.

Ok now let's see what we need. I used **gpiozero** to control the GPIO pins on the Raspberry.\
`sudo apt install python3-gpiozero`

Now install **python-rtmidi**:\
`sudo pip3 install python-rtmidi`


### Raspberry MIDI Device
At this point we should have all the necessary files. Time to make our MIDI Gadget!\
Start by doing these steps:
1. `echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt`
2. `echo "dwc2" | sudo tee -a /etc/modules`
3. `echo "libcomposite" | sudo tee -a /etc/modules`
4. `echo "g_midi" | sudo tee -a /etc/modules`
5. Create midi_over_usb file:\
`sudo touch /usr/bin/midi_over_usb`
6. Make it executable:\
`sudo chmod +x /usr/bin/midi_over_usb`
7. Edit it:\
`sudo nano /usr/bin/midi_over_usb`\
paste the following and save it:
```
cd /sys/kernel/config/usb_gadget/
mkdir -p midi_over_usb
cd midi_over_usb
echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
mkdir -p strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "Your Name" > strings/0x409/manufacturer
echo "MIDI USB Device" > strings/0x409/product
ls /sys/class/udc > UDC
```
8. Now edit your rc.local:\
`sudo nano /etc/rc.local`\
and write this before "exit0", then save it:\
`/usr/bin/midi_over_usb`
9. Finally, you can reboot your Raspberry:\
`sudo reboot`

If everything was done correctly, after the reboot you should still be able to connect to the rasbperry using the raspberrypi.local address, thats because in our "cmdline.txt" it's still as "g_ether" and not "g_midi", so let's fix this:\
Open the "cmdline.txt" file:\
`sudo nano /boot/cmdline.txt`\
And at the end, replace "`g_ether`" with "`g_midi`", then save it (Ctrl+O, Enter, Ctrl+X)\
Take note of your raspberry pi IP address using `ifconfig`, we will need it in a minute.\
Now reboot again:\
`sudo reboot`

Good, once the reboot is done we should be able to connect to the raspberry using the IP.\
`ssh pi@<ip_address>`\
and we are in!

Let's quickly check if our "midi_over_usb" that we created is working.\
To do so, type `arecordmidi -l` and hit enter, you should see a list of midi ports looking like this:
```
14:0    Midi Through         Midi Through Port-0
16:0    f_midi               f_midi
```
That "f_midi" is our MIDI port that we will be using.

### The script
You are tired, i know, but this is the last step, hold on.\
For now we have:
- Set the Raspberry to be able to work on it via USB
- Installed all the required libraries that we need
- Created a MIDI port that we will use to send outputs

For the last step we need to make the python script execute at boot, so we don't need to do anything.\
For this purpose i used **Cronjob**.\
WIP


### Credits
[Raspberry Pi Zero - Programming over USB!](https://blog.gbaman.info/?p=791)\
[Setting up Raspberry Pi for MIDI](https://ixdlab.itu.dk/wp-content/uploads/sites/17/2017/10/Setting-Up-Raspberry-Pi-for-MIDI.pdf)\
(also i downloaded that PDF and uploaded in this git in the "other" folder, just to be sure not to lose it if the link goes down)\
[Python-RtMidi](https://pypi.org/project/python-rtmidi/)\
[RPi.GPIO](https://pypi.org/project/RPi.GPIO/)
