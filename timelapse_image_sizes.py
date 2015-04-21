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


def main():
    # Create a new wave file
    wv = wave.open('output/timelapse_image_sizes.wav', 'w')
    wv.setparams((CHANNELS, WIDTH, RATE, FRAMES, COMPRESSION_TYPE, COMPRESSION_NAME))
    
    sizes = get_sizes()
    samples = percentages_to_volumes(sizes_to_percentages(sizes))

    wvData = ""
    for sample in samples:
        wvData += pack('h', int(round(sample)))

    wv.writeframes(wvData)
    wv.close()
    
if __name__ == '__main__':
    main()
