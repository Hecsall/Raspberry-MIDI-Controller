# import argparse
import logging
# import shlex
# import subprocess
import sys
import time
from os.path import exists

import RPi.GPIO as GPIO
from gpiozero import Button
import rtmidi
from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import ( 
  CONTROLLER_CHANGE, 
  NOTE_ON, 
  NOTE_OFF, 
  # CC
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
  def __init__(self, name, midiout, status=0xB0):
    self.name = name
    self.controller_change_control = status
    self.midiout = midiout
    # CC
    self.sustain = False
    self.legato = False
    self.portamento = False

    # Init GPIO
    # GPIO.setwarnings(False)
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # GPIO PIN -> control
    self.gpio_channel_map = {
      # GPIO PIN, 'control'
      4: 'sustain'
    }

    # GPIO pins
    self.sustainbtn = Button(4)
  
    print('Initialized FootController \"' + self.name + '\"')

  

  def controllerChange(self, channel):
    control = self.gpio_channel_map.get(channel)
    attr = getattr(self, control)
    if attr == False:
      setattr(self, control, True)
      value = 64 # ON
      log.info(control + " ON")
    else:
      setattr(self, control, False)
      value = 63 # OFF
      log.info(control + " OFF")

    control = CC_CONTROLS_MAP.get(control)
    
    controller_change = [STATUS_MAP.get('controllerchange'), control, value]
    return self.midiout.send_message(controller_change)


  def note(self, note, status, velocity=112):
    if status == True:
      note = [STATUS_MAP.get('noteon'), note, velocity]
    elif status == False:
      note = [STATUS_MAP.get('noteoff'), note, 0]
    return self.midiout.send_message(note)



def test(channel):
  footcontroller.controllerChange('sustain')



def main():
  logging.basicConfig(format="%(name)s: %(levelname)s - %(message)s", level=logging.INFO)

  # Apro porta MIDI virtuale (nome dispositivo che vedrà Ableton)
  # midiout = rtmidi.MidiOut()
  midiout_name = "Python MIDI"
  # midiout.open_port(0)

  midiout, port_name = open_midioutput(1)

  # Inizializzo FootController
  footcontroller = FootController(midiout_name, midiout)

  log.info("Entering main loop. Press Control-C to exit.")

  try:
    # just wait for keyboard interrupt in main thread
    while True:
      footcontroller.sustainbtn.when_pressed = lambda : footcontroller.controllerChange(4)
      # footcontroller.sustainbtn.when_pressed = lambda : footcontroller.note(60, True)


  except KeyboardInterrupt:
    print('')
  finally:
    # GPIO.cleanup()
    del footcontroller
    del midiout


if __name__ == '__main__':
  sys.exit(main())