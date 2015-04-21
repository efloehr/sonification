from pyknon.genmidi import Midi
from pyknon.music import NoteSeq

notes1 = NoteSeq("D4 F#8 A Bb4")
midi = Midi(1, tempo=90, instrument=53)
midi.seq_notes(notes1, track=0)
midi.write("output/demo.mid")
