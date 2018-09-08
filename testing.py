
# Testing file, dont mind this.

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
    
    self.sustain = False
    self.legato = False
    self.portamento = False

    # GPIO pins
    # Here initialize GPIO pins you will use
    self.btn4 = Button(4)
    

    print('Initialized FootController')
    print("< Light a led now >")

  
  def sendMIDI(self, pin, type, channel, value=None):
    
    # This is a trigget button (press=ON, another press=OFF)
    if value is None: 
      if not getattr(self, type) or getattr(self, type) == False:
        setattr(self, type, True)
        controller_change = [type, channel, 64]
        return self.midiout.send_message(controller_change)

      elif getattr(self, type) == True:
        setattr(self, type, False)
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
    
      footcontroller.btn4.when_pressed  = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=SUSTAIN, value=64) # When pressed activate the CC
      footcontroller.btn4.when_released = lambda : footcontroller.sendMIDI(type=CONTROLLER_CHANGE, channel=SUSTAIN, value=0) # When released deactivate the CC
     

  except KeyboardInterrupt:
    print('')
  finally:
    del footcontroller
    del midiout


if __name__ == '__main__':
  sys.exit(main())