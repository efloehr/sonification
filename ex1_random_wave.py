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
VOLRANGE = MAXVOL - MINVOL

def main():
    # Create a new wave file
    wv = wave.open('output/random.wav', 'w')

    # Set the parameters needed to define the wave file's structure
    wv.setparams((CHANNELS, WIDTH, RATE, FRAMES, COMPRESSION_TYPE, COMPRESSION_NAME))
    
    # We write the data to a binary string
    wvData = ""

    # RATE is the number of samples per second, so create a 4 second wave file
    for i in xrange(0, RATE * 4):
        # All pack does is takes an integer and turns it into a binary number and
        # not a Python object.
        # random() is a number between 0 and 1, and we want it to be between
        # MINVOL and MAXVOL
        wvData += pack('h', int((round(random.random() * VOLRANGE) + MINVOL)))

    # Write the binary string to the file and close
    wv.writeframes(wvData)
    wv.close()
    
if __name__ == '__main__':
    main()
