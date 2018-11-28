import mido
import datetime


print("Started")


with mido.open_input('f_midi:f_midi 16:0') as inport:

    # Current start time
    last_time = datetime.datetime.now()
    new_time = datetime.datetime.now()

    for msg in inport:
        
        #Tempo di questo tic
        new_time = datetime.datetime.now()

        # Differenza di datetime
        diff = new_time - last_time
        
        # Differenza di secondi
        diff_seconds = diff.microseconds

        # Converto in millisecondi 
        ms = (diff_seconds / 1000) * 4
        
        bpm = 60000 / ms
        print(bpm)

        last_time = new_time

'''

BPM = 1 beat for minute

'''