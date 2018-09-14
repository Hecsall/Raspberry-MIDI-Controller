import logging
import sys
import time
from os.path import exists

from gpiozero import Button
import rtmidi
from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import ( 
  CONTROLLER_CHANGE, 
  NOTE_ON, 
  NOTE_OFF, 
  # CC - Controller Change
  SUSTAIN,
  PORTAMENTO,
  SOSTENUTO,
  LEGATO
)



log = logging.getLogger('pyFootController')


STATUS_MAP = {
  'noteon': NOTE_ON,
  'noteoff': NOTE_OFF,
  'controllerchange': CONTROLLER_CHANGE
}

CC_CONTROLS_MAP = {
  'sustain': SUSTAIN,
  'portamento': PORTAMENTO,
  'sostenuto': SOSTENUTO,
  'legato': LEGATO
}


class FootController(object):
  def __init__(self, midiout, status=0xB0):
    self.controller_change_control = status
    self.midiout = midiout
    
    # GPIO pins
    # Here initialize GPIO pins you will use
    self.btn4 = Button(4)
    self.btn17 = Button(17)
    
    #self.0x66 = False
    #self.0x67 = False

    print('Initialized FootController')
    print("< Light a led now >")

  
  def sendMIDI(self, type, channel, value=None):
    
    # This is a trigget button (press=ON, another press=OFF)
    if value is None: 
      if not getattr(self, str(channel), None) or getattr(self, str(channel), None) == False:
        setattr(self, str(channel), True)
        controller_change = [type, channel, 64]
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

  log.info("Entering main loop. Press Control-C to exit.")

  try:
    while True:
    
      # Hold behaviour (Press=ON, Release=OFF)
      # footcontroller.btn4.when_pressed  = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=SUSTAIN, value=64)
      # footcontroller.btn4.when_released = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=SUSTAIN, value=0)
      
      # Toggle behaviour (Press=ON, Press again=OFF)
      footcontroller.btn4.when_pressed  = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=0x66) # 0x50 = General purpose controller 1
      
      footcontroller.btn17.when_pressed  = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=0x67) # 0x51 = General purpose controller 2
      
      # Possible free MIDI Channels:
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