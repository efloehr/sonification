from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest

dur = 1/16.0

notes = []
for octave in range(2,9):
    for pitch in range(0,12):
        notes.append((octave, pitch))

opacity_to_volume = {'0': 1, '250': 0.90, '500': 0.70, '750': 0.50, '1000': 0.40}

def read_obs(filename):
    f = open(filename)
    obs = []
    for line in f:
        day,hour,temp,opacity,precip = line.split(',')
        obs.append((day, hour, temp, opacity, precip))
    f.close()
    return obs


def obs_to_note(obs):
    global notes
    day, hour, temp, opacity, precip = obs
    # Temperature is note
    index = int(temp)
    if index < 7: index = 7
    elif index > 90: index = 90
    index -= 7
    octave, pitch = notes[index]
    # Sky cover is volume
    volume = 0
    try:
        volume = opacity_to_volume[opacity]
    except:
        pass
    return Note(pitch, octave, dur, int(volume * 120))

obs = read_obs('kcmh_2014_03_obs.csv')

obs_notes = NoteSeq()
for ob in obs:
    obs_notes.append(obs_to_note(ob))

midi = Midi(1, tempo=90, instrument=1)
midi.seq_notes(obs_notes, track=0)
midi.write("temps_2014_03.mid")
