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


def get_sizes():
    sizes = []

    with open('size.txt') as size_file:
        for size in size_file:
            sizes.append(int(size))

    return sizes


def sizes_to_percentages(sizes):
    sizes = [size for size in sizes if size > 0] # No empties
    min_size = min(sizes)
    max_size = max(sizes)

    return [(float(size) - min_size)/(max_size - min_size) for size in sizes]


def percentages_to_volumes(size_percs):
    return [(size_perc - 0.5) * MAXVOL * 2.0 for size_perc in size_percs]


def percentage_to_frequency(perc):
    MIN_FREQ = 28
    MAX_FREQ = 4186
    return perc * (MAX_FREQ - MIN_FREQ) + MIN_FREQ


def main():
    # Create a new wave file
    wv = wave.open('timelapse_image_sizes_freq.wav', 'w')
    wv.setparams((CHANNELS, WIDTH, RATE, FRAMES, COMPRESSION_TYPE, COMPRESSION_NAME))
    
    sizes = get_sizes()
    samples = percentages_to_volumes(sizes_to_percentages(sizes))

    NOTE_DURATION = 50

    start_phase = 0
    for sample in samples:
        freq = percentage_to_frequency(sample)
        start_phase = play_sine_freq(wv, freq, MAXVOL, NOTE_DURATION, start_phase)

    wv.close()
    
if __name__ == '__main__':
    main()
