import logging
import sys
import time
from os.path import exists

from gpiozero import LED, Button
import rtmidi
from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import ( 
  NOTE_OFF,
  NOTE_ON,
  POLYPHONIC_PRESSURE,
  CONTROLLER_CHANGE,
  PROGRAM_CHANGE,
  CHANNEL_PRESSURE,
  PITCH_BEND
)





log = logging.getLogger('pyFootController')


class FootController(object):
  def __init__(self, midiout, status=0xB0):
    self.controller_change_control = status
    self.midiout = midiout
    
    # GPIO pins
    # Here initialize GPIO pins you will use
    self.btn4 = Button(4)
    self.btn17 = Button(17)
    
    self.btn5 = Button(5)
    self.btn6 = Button(6)
    self.btn13 = Button(13)
    self.btn19 = Button(19)
    self.btn26 = Button(26)

    print('Initialized FootController')

  
  def sendMIDI(self, type, channel, value=None):
    
    # This is a trigget button (press=ON, another press=OFF)
    if value is None: 
      if not getattr(self, str(channel), None) or getattr(self, str(channel), None) == False:
        setattr(self, str(channel), True)
        controller_change = [type, channel, 100]
        return self.midiout.send_message(controller_change)

      elif getattr(self, str(channel)) == True:
        setattr(self, str(channel), False)
        controller_change = [type, channel, 0]
        return self.midiout.send_message(controller_change)

    # This is a hold button (press=ON, release=OFF)
    else:
      controller_change = [type, channel, value]
      return self.midiout.send_message(controller_change)



def main():
  logging.basicConfig(format="%(name)s: %(levelname)s - %(message)s", level=logging.INFO)

  midiout, port_name = open_midioutput(1)

  # Init FootController
  footcontroller = FootController(midiout)

  # A status indicator, will light up after the FootController is initialized,
  # to let you know that now it's able to send midi signals
  statusLed = LED(18)
  statusLed.on()

  log.info("Entering main loop. Press Control-C to exit.")

  try:
    while True:
    
      # Hold behaviour (Press=ON, Release=OFF)
      # footcontroller.btn4.when_pressed = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=0x40, value=64)
      # footcontroller.btn4.when_released = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=0x40, value=0)
      
      # Toggle behaviour (Press=ON, Press again=OFF)
      footcontroller.btn5.when_pressed = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=0x66)
      footcontroller.btn6.when_pressed = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=0x67)
      footcontroller.btn13.when_pressed = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=0x67)
      footcontroller.btn19.when_pressed = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=0x67)
      footcontroller.btn26.when_pressed = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=0x67)
      
      # Usually free MIDI Channels:
      # 0x50, 0x51, 0x52, 0x53, 0x55, 0X56, 0X57, 0X59, 0X5A, 
      # 0X66, 0X67, 0X68, 0X69, 0X6A, 0X6B, 0X6C, 0X6D, 0X6E, 
      # 0X6F, 0X70, 0X71, 0X72, 0X73, 0X74, 0X75, 0X76, 0X77

  except KeyboardInterrupt:
    print('')
  finally:
    del footcontroller
    del midiout


if __name__ == '__main__':
  sys.exit(main())