from struct import pack
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


def main():
    # Create a new wave file
    wv = wave.open('random.wav', 'w')
    wv.setparams((CHANNELS, WIDTH, RATE, FRAMES, COMPRESSION_TYPE, COMPRESSION_NAME))
    
    wvData = ""
    for i in xrange(0, RATE * 4):
        wvData += pack('h', int(round(random.random() * MAXVOL)))

    wv.writeframes(wvData)
    wv.close()
    
if __name__ == '__main__':
    main()
