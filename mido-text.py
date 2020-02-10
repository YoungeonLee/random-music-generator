from mido import MidiFile

mid = MidiFile('test.mid')

for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        if msg.type != 'note_on' and msg.type != 'note_off':
            print(msg)


