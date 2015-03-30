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


def play_sine_freq(wave_file, freq_hz, volume, time_ms):
    '''
    Pass in wave file, the frequency in Hertz, how long to play
    '''
    wvData = ""
    angular_frequency = 2.0 * pi * freq_hz
    num_samples = int(round(time_ms * RATE / 1000.0))

    for i in xrange(0, num_samples):
        t = i / float(RATE)
        wvData += pack('h', int(round(volume * sin(angular_frequency * t))))

    wave_file.writeframes(wvData)


def main():
    # Create a new wave file
    wv = wave.open('robot.wav', 'w')
    wv.setparams((CHANNELS, WIDTH, RATE, FRAMES, COMPRESSION_TYPE, COMPRESSION_NAME))
    
    NOTE_DURATION = 100
    NUMBER_OF_NOTES = 50
    MIN_FREQ = 28
    MAX_FREQ = 4186

    for note_num in xrange(0, NUMBER_OF_NOTES):
        freq = random.random() * (MAX_FREQ - MIN_FREQ) + MIN_FREQ
        play_sine_freq(wv, freq, MAXVOL, NOTE_DURATION)

    wv.close()
    
if __name__ == '__main__':
    main()
