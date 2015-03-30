from struct import pack
from math import sin, pi
import wave
import random


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


def play_sine_freq(wave_file, freq_hz, volume, time_ms, start_phase=0):
    '''
    Pass in wave file, the frequency in Hertz, how long to play, and the starting
    phase in radians.
    '''
    wvData = ""
    angular_frequency = 2.0 * pi * freq_hz
    num_samples = int(round(time_ms * RATE / 1000.0))
    phase = start_phase

    t = 0.0
    for i in xrange(0, num_samples):
        t = i / float(RATE)
        phase = angular_frequency * t + start_phase
        wvData += pack('h', int(round(volume * sin(phase))))

    wave_file.writeframes(wvData)
    return (angular_frequency * num_samples / float(RATE) + start_phase) % (2.0 * pi)


def main():
    # Create a new wave file
    wv = wave.open('robot_phased.wav', 'w')
    wv.setparams((CHANNELS, WIDTH, RATE, FRAMES, COMPRESSION_TYPE, COMPRESSION_NAME))
    
    NOTE_DURATION = 100
    NUMBER_OF_NOTES = 50
    MIN_FREQ = 28
    MAX_FREQ = 4186

    start_phase = 0
    for note_num in xrange(0, NUMBER_OF_NOTES):
        freq = random.random() * (MAX_FREQ - MIN_FREQ) + MIN_FREQ
        start_phase = play_sine_freq(wv, freq, MAXVOL, NOTE_DURATION, start_phase)

    wv.close()
    
if __name__ == '__main__':
    main()
