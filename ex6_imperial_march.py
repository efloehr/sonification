from struct import pack
from math import sin, pi
import random
import wave
from adsr import ADSR
from piano_notes import duration, piano_note

# Parameters for wave file
RATE=44100                        # Samples per second
RATE_MS=RATE/1000.0               # Samples per millisecond
CHANNELS=1                        # Number of channels
WIDTH=2                           # Number of bytes per sample
FRAMES=0                          # Starting number of frames
COMPRESSION_TYPE='NONE'           # Compression type of wave file
COMPRESSION_NAME='not compressed' # Name of compression type

# 16-bit signed integer values
MAXVOL = 2**15-1.0
MINVOL = -2**15
VOLRANGE = MAXVOL - MINVOL

envelope = ADSR(10, 40, 0.6, 40, RATE)


def play_sine_freq(wave_file, freq_hz, volume_pct, time_ms):
    '''
    This is just an implementation of the formula for a sine
    wave at: http://en.wikipedia.org/wiki/Sine_wave
    
    Pass in wave file, the frequency in Hertz,
    the volume in percent (0 to 1), and
    how long to play in milliseconds (1000 = 1 second)
    '''
    
    # Where we hold the sample data
    wvData = ""
    
    # Angular frequency is the rate of change of the function
    # argument in units of radians per second, so it will complete
    # a cycle freq_hz times per second
    angular_frequency = 2.0 * pi * freq_hz
    
    # The number of samples to make, which is just the number of
    # milliseconds to sustain the sound times the number of samples
    # per second.
    num_samples = int(round(time_ms * RATE_MS))

    # Create that many samples
    for i, level in enumerate(envelope.envelope(time_ms)):
        # t is time in seconds, from the wikipedia article
        t = i / float(RATE)
        
        # Instead of a random number, we are using the sine function
        # which returns a number from -1 to 1, similar to random()
        # But to make things easy we want to scale it to a range
        # between 0 and 1
        sinval = (sin(angular_frequency * t) + 1.0) / 2.0 
        wvData += pack('h', level * volume_pct * int((round(sinval * VOLRANGE) + MINVOL)))

    # Write the binary string to the file
    wave_file.writeframes(wvData)


def play_rest(wave_file, time_ms):
    wvData = ""
    num_samples = int(round(RATE_MS * time_ms))
    for i in xrange(0, num_samples):
        wvData += pack('h', 0)
    wave_file.writeframes(wvData)
    

def get_notes(filename):
    notes = []
    with open(filename) as f:
        for line in f:
            notes.append(line.strip().split(','))
    return notes


def main():
    # Create a new wave file
    wv = wave.open('output/imperial_march.wav', 'w')

    # Set the parameters needed to define the wave file's structure
    wv.setparams((CHANNELS, WIDTH, RATE, FRAMES, COMPRESSION_TYPE, COMPRESSION_NAME))

    # 1.5 second whole note
    WHOLE_NOTE_MS = 1500

    notes = get_notes('data/imperial_march.csv')
    for note in notes:
        freq, dur = note
        dur = duration[dur] * WHOLE_NOTE_MS
        if freq == 'REST':
            play_rest(wv, dur)
        else:
            freq = piano_note[freq]
            start_phase = play_sine_freq(wv, freq, 1.0, dur)
#            play_rest(wv, 5)

    wv.close()
    
if __name__ == '__main__':
    main()
