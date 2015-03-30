from struct import pack
from math import sin, pi
import wave
import random
from piano_notes import duration, piano_note

# Parameters for wave file
RATE=44100                        # Samples per second
CHANNELS=1                        # Number of channels
WIDTH=2                           # Number of bytes per sample
FRAMES=0                          # Starting number of frames
COMPRESSION_TYPE='NONE'           # Compression type of wave file
COMPRESSION_NAME='not compressed' # Name of compression type

# 16-bit signed integer values
MAXVOL = 2**15-1.0
MINVOL = -2**15


def ms_to_samples(time_ms):
    return int(round(time_ms * RATE / 1000.0))


def play_sine_freq(wave_file, freq_hz, volume, time_ms, start_phase=0):
    '''
    Pass in wave file, the frequency in Hertz, how long to play, and the starting
    phase in radians.
    '''
    wvData = ""
    angular_frequency = 2.0 * pi * freq_hz
    num_samples = ms_to_samples(time_ms)
    phase = start_phase

    t = 0.0
    for i in xrange(0, num_samples):
        t = i / float(RATE)
        phase = angular_frequency * t + start_phase
        wvData += pack('h', int(round(volume * sin(phase))))

    wave_file.writeframes(wvData)
    return (angular_frequency * num_samples / float(RATE) + start_phase) % (2.0 * pi)


def play_rest(wave_file, time_ms):
    wvData = ""
    num_samples = ms_to_samples(time_ms)
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
    wv = wave.open('imperial_march.wav', 'w')
    wv.setparams((CHANNELS, WIDTH, RATE, FRAMES, COMPRESSION_TYPE, COMPRESSION_NAME))
    
    WHOLE_NOTE_MS = 1500

    start_phase = 0
    notes = get_notes('imperial_march.csv')
    for note in notes:
        freq, dur = note
        freq = piano_note[freq]
        dur = duration[dur] * WHOLE_NOTE_MS
        print note, freq, dur
        start_phase = play_sine_freq(wv, freq, MAXVOL, dur, start_phase)
	play_rest(wv, 5)

    wv.close()
    
if __name__ == '__main__':
    main()
