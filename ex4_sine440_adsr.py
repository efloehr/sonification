from struct import pack
from math import sin, pi
import wave
from adsr import ADSR

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

envelope = ADSR(10, 400, 0.6, 400, RATE)


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


def main():
    # Create a new wave file
    wv = wave.open('output/sine440_adsr.wav', 'w')

    # Set the parameters needed to define the wave file's structure
    wv.setparams((CHANNELS, WIDTH, RATE, FRAMES, COMPRESSION_TYPE, COMPRESSION_NAME))

    # Add the data points to create a sine wave with a frequency of 440Hz, with 100%
    # volume for 1 second
    play_sine_freq(wv, 440.0, 1, 1000)
        
    # Play a few more notes in the scale
    for note_hz in [493.88, 523.25, 587.33, 659.25, 698.46, 783.99]:
        play_sine_freq(wv, note_hz, 1, 1000)
    
    wv.close()
    
if __name__ == '__main__':
    main()
