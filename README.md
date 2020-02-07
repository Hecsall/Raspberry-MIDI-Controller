
# Raspberry Pi Zero - MIDI Controller

> **Before reading**:\
This project was a little experiment when i was approaching to MIDI controllers. It was fun (and stressful) to make, and i was pretty happy with the result, but keep in mind one thing: The Raspberry Pi is technically a computer, it needs some time to bootup when you plug the USB cable. So it's not really "plug and play", it's more like a "plug, wait some time, then play". Don't expect to plug it in and be instantly ready to jam.\
This is the reason why i made an **Arduino version** of this, you can find it (with images of the build process) at this link https://github.com/Hecsall/arduino-midi-footswitch . It is much faster, simple and reliable. So if you really need a custom built midi controller, i would suggest to take the Arduino approach.\
**Thank you for reading, and have fun!**

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

Install requirements for **python-rtmidi:**\
`sudo apt install libasound2-dev libjack0 libjack-dev`

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

### Autostarting the Script
You are tired, i know, but we are close to the end, hold on.\
For now we have:
- Set the Raspberry to be able to work on it via USB
- Installed all the required libraries that we need
- Created a MIDI port that we will use to send outputs

We need to make the python script execute at boot.\
For this purpose i used **Cronjob**.\
So, to make the script autostart at Raspberry Pi boot, i created a .sh file (midi_controller.sh) that executes the python script. Notice that the .sh script points to `/home/pi/midi_controller/midi_controller.py` so you may need to customize that path to reflect your script location.\
To add a cronjob entry, use the following command:
```
sudo crontab -e
```
This will open your crontab, than you can setup your cronjob pasting this line at the bottom:
```
@reboot sh /home/pi/midi_controller/midi_controller.sh >/home/pi/logs/cronlog 2>&1
```
Notice that you will have to edit that path, pointing to your midi_controller.sh file. That line of code will also output the python logs in a "cronlog" file under /home/pi/logs so if for some reason the script isn't working you can check if there are some errors there.

### Customizing the Python Script
By default you will find just things i setup for myself, but you would likely customize the script to add/remove/edit some buttons.\
I made it really simple, you just have to do 2 things:
1. **Add inizialization of GPIO Pins** inside the FootController Class (something around line 46).\
just copy what i already did, replacing the number with your GPIO pin number you want to use, for example:
```python
self.btn14 = Button(14)
```
So now our script can use that pin (refer to the "gpio_pinout.png" inside the "other" folder, GPIO pin numbers are the ones on the outside).

2. **Assign the GPIO pin to a MIDI message**, you can find some i did around line 90~.\
Here you will see 2 types of initialization:
- **Toggle mode**: when you press and release the button the message "ON" is sent, when you press and release it again the message "OFF" is sent.\
The code to do that is the following:
```python
footcontroller.btn0.when_pressed = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=0x66)
```
Where "btn0" is the name of the initialized button on Step 1.\
At the moment, when using Toggle mode, you can't specify a "value" option, because when i made it i was using it to control a "Controller Change" MIDI signal, that basically can only have 2 possible values, that are a number <= 63 for "OFF", and a number >= 64 for "ON", so i just "hardcoded" the ON signal to 100 and the OFF signal to 0. Maybe in the future i will change that to allow a "ON/OFF" value array.
- **Hold mode**: when you are pressing down the button the message "ON" is sent, when you release the button the message "OFF" is sent.\
The code to do that is the following:
```python
footcontroller.btn0.when_pressed = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=0x40, value=64)
footcontroller.btn0.when_released = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=0x40, value=0)
```
Where "btn0" is the name of the initialized button on Step 1.\
Here, when using Hold mode you need to specify the "value" that you want to send. (for NOTE_ON messages, the value is the velocity of the note)

In both Toggle and Hold modes, you see there is a **"type"** and a **"channel"**. I think those are theorically wrong names, i'll change them as soon as i can.\
Anyways, the "type" is the **MIDI message type** you want to send, like "NOTE_ON", "NOTE_OFF", "CONTROLLER_CHANGE" etc, i imported them from python-rtmidi, refer to [python-rtmidi's constants file](https://github.com/SpotlightKid/python-rtmidi/blob/master/rtmidi/midiconstants.py) to know more about them.\
The "channel" is the actual Hex message you want to send, so, if you used NOTE_ON for the type, the channel would be the actual note to send, like **0x48** to send a C2, or if you used CONTROLLER_CHANGE you will put **0x40** for the "Hold pedal".\
To know Hex codes for Notes, refer to [this table](https://www.wavosaur.com/download/midi-note-hex.php).\
To know Controller Change messages refer to the official [MIDI documentation table](https://www.midi.org/specifications-old/item/table-3-control-change-messages-data-bytes-2) (the numbers you have to use are on the "HEX" column)

### Credits
[Raspberry Pi Zero - Programming over USB!](https://blog.gbaman.info/?p=791)\
[Setting up Raspberry Pi for MIDI](https://ixdlab.itu.dk/wp-content/uploads/sites/17/2017/10/Setting-Up-Raspberry-Pi-for-MIDI.pdf)\
(also i downloaded that PDF and uploaded in this git in the "other" folder, just to be sure not to lose it if the link goes down)\
[Python-RtMidi](https://pypi.org/project/python-rtmidi/)\
[RPi.GPIO](https://pypi.org/project/RPi.GPIO/)\
[MIDI.org Controller Change](https://www.midi.org/specifications-old/item/table-3-control-change-messages-data-bytes-2)\
[Hex to MIDI note chart](https://www.wavosaur.com/download/midi-note-hex.php)
