import random
from midiutil import MIDIFile
from midiutil.MidiFile import MIDIFile
import copy

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

def neg_harm(pitches, root=60):
    """rotates the pitches to negative harmony
    with root(scale) as the base for rotation axis
    major -> minor"""
    neg_pitches = []
    for pitch in pitches:
        root_diff = pitch - root
        shift = 7 - root_diff*2
        neg_pitch = pitch + shift
        neg_pitches.append(neg_pitch)
    return neg_pitches



class Pitch():
    """pitch class can contain multiple pitches (in list form) to be played at the same time"""
    def __init__(self,pitch=[60]):
        self.pitches = pitch


        
class Note():
    def __init__(self,pitch=[60],duration=1):
        self.pitch = pitch
        self.duration = duration
        assert type(self.pitch)==type([]), "p=note.pitch isn't a list"

    def __repr__(self):
            return f"Pitch: {self.pitch} / Duration: {self.duration}\n"



class Measure():
    def __init__(self,length=4,chord='C',note_lengths={1:1,.5:1},str_beat=[1,3]):
        self.length = length
        self.chord = chord
        self.notes = []
        self.bass = []
        self.note_lengths = note_lengths
        self.str_beat=str_beat

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
            if beat+1 in self.str_beat:
                pitch = [random.choice(chord(self.chord))]
            else:
                pitch = [random.choice(notes)]
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
        bass = Note(pitch = chords, duration = 4)
        self.add_bass(bass)

    def CA_Lnote(self):
        """create and add last note"""
        pitch = [random.choice(chord(self.chord))]
        duration = 4
        lnote = Note(pitch, duration)
        self.add_note(lnote)

    def CA_Lbass(self):
        """create and add last bass"""
        chords = chord(self.chord)
        bass = Note(pitch = chords, duration = 4)
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
        """creates and add random measures"""
        for i in range(self.length):
            chord = self.chrd_prg[i%len(self.chrd_prg)]
            rmeasure = Measure(chord=chord, note_lengths=self.note_lengths)
            rmeasure.CA_notes()
            rmeasure.CA_bass()
            self.add_measure(rmeasure)

    def CA_Lmeasure(self):
        """creates and add last measure"""
        chord = self.chrd_prg[0]
        lmeasure = Measure(chord=chord, note_lengths=self.note_lengths)
        lmeasure.CA_Lnote()
        lmeasure.CA_Lbass()
        self.add_measure(lmeasure)




class Piece():
    def __init__(self,length=2,chrd_prg=['C','Am','F','G'],note_lengths={1:1,.5:1}):
        """chrd_prg = chord progression
        note_lengths = {length1:length1 probability, ...
        1 is a quarter note and .5 is eight note and ..."""
        self.length = length
        self.melodies = []
        self.chrd_prg = chrd_prg
        self.note_lengths = note_lengths

    def __repr__(self):
        return f'{self.melodies}'
    
    def add_melody(self,Melody):
        self.melodies.append(Melody)

    def CA_melodies(self):
        """create and add random melodies
        adds an extra ending measure with a note from the chord """
        for i in range(self.length):
            rmelody = Melody(chrd_prg=self.chrd_prg, note_lengths=self.note_lengths)
            rmelody.CA_measures()
            self.add_melody(rmelody)

        # ending note
        emelody = Melody(chrd_prg=self.chrd_prg)
        emelody.CA_Lmeasure()
        self.add_melody(emelody)

    def in_notes(self):
        """breaks down the piece to only notes
        (returns notes as list made of list [[notes][bass_notes]])"""
        notes = []
        bass_notes = []
        # notes
        for melody in self.melodies:
            for measure in melody.measures:
                for note in measure.notes:
                    notes.append(note)
        # bass
        for melody in self.melodies:
            for measure in melody.measures:
                for note in measure.bass:
                    bass_notes.append(note)

        return [notes,bass_notes]

    def CA_neg_harm(self):
        """create and add a negative harmony of the existing piece"""
        p = copy.deepcopy(self)
        for melody in p.melodies:
            for measure in melody.measures:
                for note in measure.notes:
                    note.pitch = neg_harm(note.pitch, degrees[self.chrd_prg[0]])
                for note in measure.bass:
                    note.pitch = neg_harm(note.pitch, degrees[self.chrd_prg[0]]) 
        for melody in p.melodies:
            self.add_melody(melody)
                    
            
        

    def write_midi(self):
        """writes midi file for the piece"""
        time = 0
        MyMIDI = MIDIFile(1)
        MyMIDI.addTempo(track, time, tempo)
        piece = self.in_notes()
        # adding notes
        for note in piece[0]:
            for pitch in note.pitch:
                MyMIDI.addNote(track, channel, pitch, time, note.duration, volume)
            time += note.duration
                    
        
        # adding bass
        time = 0
        for note in piece[1]:
            for pitch in note.pitch:
                MyMIDI.addNote(track, channel + 1, pitch - 12, time, note.duration, volume)
            time += note.duration
        


        with open("test.mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)
        print('Done! Midi file saved as "test.mid"')



def main():
    p=Piece(chrd_prg=['C','G','Am','F'])
    print("created class piece")
    p.CA_melodies()
    print("created and added melodies")
    p.CA_neg_harm()
    print("created and added negative harmonies")
    p.write_midi()
    print("Finished!")

    

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
