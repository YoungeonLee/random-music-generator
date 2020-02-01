import random
from midiutil import MIDIFile
from midiutil.MidiFile import MIDIFile

notes  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
degrees = {'C':60, 'D':62, 'E':64, 'F':65, 'G':67, 'A':69, 'B':71}
#maj = 4+3
track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 120   # In BPM
volume   = 100  # 0-127, as per the MIDI standard



def chord(chord):
    """determines the notes in the chord and returns a list of notes"""
    if len(chord) == 1:
        root=degrees[chord]
        note_list = [root,root+4,root+7]
    elif chord[-1] =='m':
        root=degrees[chord[0]]
        note_list = [root,root+3,root+7]
    return note_list



class Note():
    def __init__(self,pitch=60,duration=1):
        self.pitch = pitch
        self.duration = duration

    def __repr__(self):
            return f"Pitch: {self.pitch} / Duration: {self.duration}\n"



class Measure():
    def __init__(self,length=4,chord='C',note_lengths={1:1,.5:1}):
        self.length = length
        self.chord = chord
        self.notes = []
        self.bass = []
        self.note_lengths = note_lengths

    def __repr__(self):
        return f"Notes: {self.notes}\nBass: {self.bass}"

    def add_note(self,Note):
        self.notes.append(Note)

    def add_bass(self,Note):
        self.bass.append(Note)

    def CA_notes(self):
        """create and add random notes"""
        beat = 0
        while beat < self.length:
            pitch = random.choice(chord(self.chord))
            duration = random.choices(list(self.note_lengths.keys()),list(self.note_lengths.values()))
            beat += duration[0]
            if beat > self.length:
                beat -= duration[0]
                duration = self.length - beat
                duration = [duration]
                beat += duration[0]
            rnote = Note(pitch, duration[0])
            self.add_note(rnote)
        assert beat == self.length

    def CA_bass(self):
        """create and add random bass"""
        chords = chord(self.chord)
        for note in chords:
            bass = Note(pitch = note - 12, duration = 4)
            self.add_bass(bass)

        



class Melody():
    def __init__(self,length=8,chrd_prg=['C','Am','F','G'],note_lengths={1:1,.5:1}):
        """chrd_prg = chord progression"""
        self.length = length
        self.measures = []
        self.chrd_prg = chrd_prg
        self.note_lengths=note_lengths

    def __repr__(self):
        return f'{self.measures}'

    def add_measure(self,Measure):
        self.measures.append(Measure)

    def CA_measures(self):
        """creates and add random measure"""
        for i in range(self.length):
            chord = self.chrd_prg[i%len(self.chrd_prg)]
            rmeasure = Measure(chord=chord, note_lengths=self.note_lengths)
            rmeasure.CA_notes()
            rmeasure.CA_bass()
            self.add_measure(rmeasure)




class Piece():
    def __init__(self,length=10,chrd_prg=['C','Am','F','G'],note_lengths={1:1,.5:1}):
        """chrd_prg = chord progression"""
        self.length = length
        self.melodies = []
        self.chrd_prg = chrd_prg
        self.note_lengths = note_lengths

    def __repr__(self):
        return f'{self.melodies}'

    def add_melody(self,Melody):
        self.melodies.append(Melody)

    def CA_melodies(self):
        """create and add random melodies"""
        for i in range(self.length):
            rmelody = Melody(chrd_prg=self.chrd_prg, note_lengths=self.note_lengths)
            rmelody.CA_measures()
            self.add_melody(rmelody)

    def write_midi(self):
        """writes midi file for the piece"""
        global time
        MyMIDI = MIDIFile(1)
        MyMIDI.addTempo(track, time, tempo)

        for melody in self.melodies:
            for measure in melody.measures:
                for note in measure.notes:
                    MyMIDI.addNote(track, channel, note.pitch, time, note.duration, volume)
                    time += note.duration

        # adding bass
        time = 0

        for melody in self.melodies:
            for measure in melody.measures:
                for note in measure.bass:
                    MyMIDI.addNote(track, channel + 1, note.pitch, time, note.duration, volume)
                time += 4


        with open("test.mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)
        print('Done! Midi file saved as "test.mid"')



def main():
    p=Piece(note_lengths={1:2,.5:1})
    p.CA_melodies()
    p.write_midi()

    

if __name__ == '__main__':
    main()



"""
degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 60   # In BPM
volume   = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)

for i, pitch in enumerate(degrees):
    MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
"""
