import argparse
import logging
import shlex
import subprocess
import sys
import time
from os.path import exists
import rtmidi
from rtmidi.midiconstants import (
  CHANNEL_PRESSURE, 
  CONTROLLER_CHANGE, 
  NOTE_ON, 
  NOTE_OFF, 
  PITCH_BEND, 
  POLY_PRESSURE, 
  PROGRAM_CHANGE,
  # CC
  SUSTAIN,
  PORTAMENTO,
  SOSTENUTO,
  LEGATO
)



log = logging.getLogger('midi2command')


# Init GPIO
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

STATUS_MAP = {
  'noteon': NOTE_ON,
  'noteoff': NOTE_OFF,
  'programchange': PROGRAM_CHANGE,
  'controllerchange': CONTROLLER_CHANGE,
  'pitchbend': PITCH_BEND,
  'polypressure': POLY_PRESSURE,
  'channelpressure': CHANNEL_PRESSURE
}

CC_CONTROLS_MAP = {
  'sustain': SUSTAIN,
  'portamento': PORTAMENTO,
  'sostenuto': SOSTENUTO,
  'legato': LEGATO
}



def playNote(midiout, note, velocity=112):
  note_on = [STATUS_MAP.get('noteon'), note, velocity]
  midiout.send_message(note_on)


def stopNote(midiout, note):
  note_off = [STATUS_MAP.get('noteoff'), note, 0]
  midiout.send_message(note_off)


def controllerChange(midiout, control, value):
  if value == 'on':
    value = 64
  elif value == 'off':
    value = 63
  controller_change = [STATUS_MAP.get('controllerchange'), control, value]
  midiout.send_message(controller_change)



def main(args=None):
  parser = argparse.ArgumentParser()
  padd = parser.add_argument
  padd('-v', '--verbose',
        action="store_true", help='verbose output')
  
  args = parser.parse_args(args if args is not None else sys.argv[1:])

  logging.basicConfig(format="%(name)s: %(levelname)s - %(message)s",
                      level=logging.DEBUG if args.verbose else logging.INFO)


  # Apro porta MIDI virtuale (nome dispositivo che vedrà Ableton)
  midiout = rtmidi.MidiOut()
  midiout.open_virtual_port("Python MIDI")


  log.info("Entering main loop. Press Control-C to exit.")

  try:
    # just wait for keyboard interrupt in main thread
    while True:
      time.sleep(1)
      # Cose
      playNote(midiout, 60)
      time.sleep(1)
      stopNote(midiout, 60)
      time.sleep(1)
      controllerChange(midiout, CC_CONTROLS_MAP.get('sustain'), 'on')
      playNote(midiout, 64)
      time.sleep(1)
      stopNote(midiout, 64)
      time.sleep(1)
      controllerChange(midiout, CC_CONTROLS_MAP.get('sustain'), 'off')

  except KeyboardInterrupt:
    print('')
  finally:
    # GPIO.cleanup()
    del midiout


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]) or 0)