from struct import pack
from math import sin, pi
import random
import wave

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
    for i in xrange(0, num_samples):
        # t is time in seconds, from the wikipedia article
        t = i / float(RATE)
        
        # Instead of a random number, we are using the sine function
        # which returns a number from -1 to 1, similar to random()
        # But to make things easy we want to scale it to a range
        # between 0 and 1
        sinval = (sin(angular_frequency * t) + 1.0) / 2.0 
        wvData += pack('h', volume_pct * int((round(sinval * VOLRANGE) + MINVOL)))

    # Write the binary string to the file
    wave_file.writeframes(wvData)


def main():
    # Create a new wave file
    wv = wave.open('output/robot.wav', 'w')

    # Set the parameters needed to define the wave file's structure
    wv.setparams((CHANNELS, WIDTH, RATE, FRAMES, COMPRESSION_TYPE, COMPRESSION_NAME))

    # Play each note for 1/10 second
    NOTE_DURATION = 100
    
    # Play a total of 50 notes
    NUMBER_OF_NOTES = 50
    
    # Approximately the piano scale (28Hz to 4,186Hz)
    MIN_FREQ = 28
    MAX_FREQ = 4186

    # Play the number of notes specified, between the frequencies, each for
    # the specified duration
    for note_num in xrange(0, NUMBER_OF_NOTES):
        freq = random.random() * (MAX_FREQ - MIN_FREQ) + MIN_FREQ
        play_sine_freq(wv, freq, 1.0, NOTE_DURATION)

    wv.close()
    
if __name__ == '__main__':
    main()
