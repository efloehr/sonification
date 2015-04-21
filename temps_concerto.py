import math
from collections import Counter
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq, Rest


dur = 1/16.0

notes = []
for octave in range(3,7):
    for pitch in [0,2,4,5,7,8,10]:
        notes.append((octave, pitch))

def read_obs(filename):
    f = open(filename)
    days = []
    hours = []
    temps = []
    opacities = []
    precips = []
    for line in f:
        day,hour,temp,opacity,precip = line.split(',')
        days.append(day)
        hours.append(int(hour))
        temps.append(int(temp))
        opacities.append(opacity)
        precips.append(precip)
    f.close()
    return {'days': days, 'hours': hours, 'temps': temps, 'opacities': opacities, 'precips': precips}


def temp_to_note(temp, min_temp, max_temp):
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
    return Note(pitch, octave, dur, 127)

obs = read_obs('data/kcmh_2014_03_obs.csv')
temps = obs['temps']
min_temp = min(temps)
max_temp = max(temps)
temp_range = max_temp - min_temp
note_range = len(notes) - 1

obs_notes = NoteSeq()
prev_note = None
for temp in temps:
    note_index = int(math.floor((temp - min_temp) * (float(note_range) / temp_range)))
    print note_index
    octave, pitch = notes[note_index]
    note = Note(pitch, octave, dur, 127)
    if prev_note is not None and prev_note.value == note.value and prev_note.octave == note.octave:
        prev_note = Note(prev_note.value, prev_note.octave, prev_note.dur + dur, prev_note.volume)
    elif prev_note is None:
        prev_note = note
    else:
        obs_notes.append(prev_note)
        prev_note = None

if prev_note is not None:
    obs_notes.append(prev_note)

midi = Midi(1, tempo=110, instrument=1)
midi.seq_notes(obs_notes, track=0)
midi.write("output/temps_2014_03_concerto.mid")
