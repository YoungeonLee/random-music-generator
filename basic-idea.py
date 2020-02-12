import random
from midiutil import MIDIFile
from midiutil.MidiFile import MIDIFile
import copy

# created by Youngeon Lee
# the program is limited to major and minor chords
# pitch of notes has to be in the form of list even if its a single note

notes  = None
degrees = {'C':60, 'D':62, 'E':64, 'F':65, 'G':67, 'A':69, 'B':71}
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


def notes_in_scale(scale):
    notes = []
    root = degrees[scale[:1]]
    notes.append(root)
    notes.append(root+2)
    notes.append(root+4)
    notes.append(root+5)
    notes.append(root+7)
    notes.append(root+9)
    notes.append(root+11)
    notes.append(root+12)
    return notes

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



def to_bass(lis):
    """lowers notes that are too high for bass"""
    for i in range(len(lis)):
        lis[i] -= 12
    for i in range(len(lis)):
        if lis[i] >= 60:
            lis[i] -= 12
    return lis


def no_bass(lis):
    """highers notes that fall into bass"""
    for i in range(len(lis)):
        if lis[i] < 60:
            lis[i] += 12
    return lis


def lower_octave(lis):
    """lowers notes an octave in the list"""
    for i in range(len(lis)):
        lis[i] -= 12
    return lis


def close_note(target, notes):
    """picks a closest note to a target from notes"""
    diff = 1
    coinflip = random.randint(0,1)
    notes = notes
    while True:
        note1 = target + diff
        note2 = target - diff
        if note1 in notes and note2 in notes:
            if coinflip == 1:
                note = note1
                break
            else:
                note = note2
                break
        elif note1 in notes:
            note = note1
            break
        elif note2 in notes:
            note = note2
            break
        else:
            diff += 1
    return note


def rand_chrd_prg():
    """creates a random chord progression using common chord patterns"""
    chrd_patt = {'C':['Am','G'],'Am':['C','G'],'G':['C','Dm','F','Am'],'Dm':["Am","F",'C'], 'F':['C','Am','G']}
    chrd_prg = []
    chrd_prg.append(random.choice(chrd_patt['C']))
    for i in range(2):
        chrd = chrd_patt[chrd_prg[-1]]
        chrd_prg.append(random.choice(chrd))
    chrd_prg.append('C')
    return chrd_prg[::-1]


                    
class Note():
    """made of a list of pitches and duration/length of the notes"""
    def __init__(self,pitch=[0],duration=1):
        self.pitch = pitch
        self.duration = duration
        assert type(self.pitch)==type([]), "Note.pitch isn't a list"

    def __repr__(self):
            return f"Pitch: {self.pitch} / Duration: {self.duration}\n"

        

class BasicIdea():
    """a musical idea; length == number of measures"""
    def __init__(self,length=4,chrd_prg=['C','Am','F','G'],note_lengths={1:1,.5:1},str_beat=[1,3],beats_per_measure = 4):
        self.length = length
        self.chrd_prg = chrd_prg
        self.note_lengths = note_lengths
        self.str_beat = str_beat
        self.beats_per_measure = beats_per_measure
        self.melody = []
        self.bass = []
        
    def __repr__(self):
        return f"Basic Idea:\nNotes: {self.melody}\nBass: {self.bass}"

    
    def add_note(self,Note):
        """add a note to melody"""
        self.melody.append(Note)

        
    def add_bass(self,Note):
        """add a note to bass"""
        self.bass.append(Note)


    def CA_notes(self):
        """creates list of durations first then fills in the pitch (strong notes followed by close notes)"""
        beat = 0
        # creating durations
        durations = []
        while beat < self.length*self.beats_per_measure:
            duration = random.choices(list(self.note_lengths.keys()),list(self.note_lengths.values()))[0]
            beat += duration
            if beat > self.length*self.beats_per_measure:
                beat -= duration
                duration = self.length*self.beats_per_measure - beat
                beat += duration
            durations.append(duration)

        # filling in pitches
        pitches = [[0]]*len(durations)
        # for strong beats
        beat = 0
        for i in range(len(durations)):
            if (beat+1)%self.beats_per_measure in self.str_beat:
                chrd = self.chrd_prg[int(beat // self.beats_per_measure)]
                pitch = [random.choice(chord(chrd))]
                pitches[i] = pitch
            beat += durations[i]
        # for 'weak' beats
        for i in range(len(durations)):
            if i == 0:
                root = degrees[self.chrd_prg[0][0]]
                pitches[-1] = [close_note(root,notes)]
            elif pitches[-(i+1)] == [0]:
                next_note = pitches[1-(i+1)]
                pitches[-(i+1)] = [close_note(next_note[0],notes)]

        # add the notes   
        for i in range(len(durations)):
            rnote = Note(pitches[i],durations[i])
            self.add_note(rnote)
                
            
            


##    def CA_notes1(self):
##        """create and add random notes (simple)"""
##        beat = 0
##        while beat < self.length*self.beats_per_measure:
##            if (beat+1)%self.beats_per_measure in self.str_beat:
##                chrd = self.chrd_prg[int(beat // 4)]
##                pitch = [random.choice(chord(chrd))]
##            else:
##                pitch = [random.choice(notes)]
##            duration = random.choices(list(self.note_lengths.keys()),list(self.note_lengths.values()))[0]
##            beat += duration
##            if beat > self.length*self.beats_per_measure:
##                beat -= duration
##                duration = self.length*self.beats_per_measure - beat
##                beat += duration
##            rnote = Note(pitch, duration)
##            self.add_note(rnote)
##        assert beat == self.length*self.beats_per_measure



    def CA_bass(self, durations=[1,1,1,1], pattern=[0,2,1,2]):
        """create and add quarter note bass based on given durations and pattern as lists"""
        assert sum(durations) == self.beats_per_measure
        assert len(durations) == len(pattern)
        
        for i in range(self.length):
            chrd = self.chrd_prg[i]
            chrd = to_bass(chord(chrd))
            chrd.sort()
            for j in range(len(durations)):
                pitch = [chrd[pattern[j]]]
                duration = durations[j]
                note = Note(pitch, duration)
                self.add_bass(note)
                
                
##    def CA_bass2(self):
##        """create and add quater note bass (1-3-2-3)"""
##        beat = 0
##        while beat < self.length*self.beats_per_measure:
##            chrd = self.chrd_prg[int(beat // self.beats_per_measure)]
##            chrd = to_bass(chord(chrd))
##            pitch = [min(chrd)]
##            duration = 1
##            beat += duration
##            rnote = Note(pitch, duration)
##            self.add_bass(rnote)
##            pitch = [max(chrd)]
##            beat += duration
##            rnote = Note(pitch, duration)
##            self.add_bass(rnote)
##            pitch = [median(chrd)]
##            beat += duration
##            rnote = Note(pitch, duration)
##            self.add_bass(rnote)
##            pitch = [max(chrd)]
##            beat += duration
##            rnote = Note(pitch, duration)
##            self.add_bass(rnote)
##            
##        assert beat == self.length*self.beats_per_measure
##
##    def CA_bass1(self):
##        """create and add plain bass"""
##        beat = 0
##        while beat < self.length*self.beats_per_measure:
##            chrd = self.chrd_prg[int(beat // 4)]
##            pitch = chord(chrd)
##            duration = 4
##            beat += duration
##            if beat > self.length*self.beats_per_measure:
##                beat -= duration
##                duration = self.length*self.beats_per_measure - beat
##                beat += duration
##            rnote = Note(to_bass(pitch), duration)
##            self.add_bass(rnote)
##        assert beat == self.length*self.beats_per_measure


    def CA_last(self):
        """creat and add melody and bass for the last measure"""
        mel = Note(chord(self.chrd_prg[0])[:1],self.beats_per_measure)
        bass = Note(to_bass(chord(self.chrd_prg[0])),self.beats_per_measure)
        self.add_note(mel)
        self.add_bass(bass)
        



class Piece():
    """basic ideas will be merged into Piece object"""
    def __init__(self,scale = 'C',length=4,chrd_prg=['C','Am','F','G'],note_lengths={1:1,.5:1},str_beat=[1,3],beats_per_measure = 4):
        """chrd_prg = chord progression
        note_lengths = {length1:length1 probability, ...
        1 is a quarter note and .5 is eight note and ..."""
        self.scale = scale
        self.length = length
        self.chrd_prg = chrd_prg
        self.note_lengths = note_lengths
        self.str_beat = str_beat
        self.beats_per_measure = beats_per_measure
        self.ideas = [] #made of BasicIdea objects
        global notes
        notes = notes_in_scale(self.scale)

    def __repr__(self):
        return f'Piece:\nNotes: {self.melodies}\nBass: {self.bass}'
    
    
    def add_idea(self,BasicIdea):
        """add ideas to the piece"""
        self.ideas.append(BasicIdea)


    def CA_ideas(self):
        """create and add random ideas
        adds an extra ending measure with a note from the chord """
        for i in range(self.length):
            idea = BasicIdea(chrd_prg=self.chrd_prg, note_lengths=self.note_lengths,str_beat=self.str_beat,beats_per_measure=self.beats_per_measure)
            idea.CA_notes()
            idea.CA_bass()
            self.add_idea(idea)



    def CA_last(self):
        """create and add the last notes"""
        eidea = BasicIdea(chrd_prg=self.chrd_prg)
        eidea.CA_last()
        self.add_idea(eidea)


    def CA_neg_harm(self):
        """create and add a negative harmony of the existing piece"""
        p = copy.deepcopy(self)
        for idea in p.ideas:
            for note in idea.melody:
                note.pitch = neg_harm(note.pitch, degrees[self.scale[:1]])
            for note in idea.bass:
                note.pitch = neg_harm(note.pitch, degrees[self.scale[:1]]-12)
        for idea in p.ideas:
            self.add_idea(idea)


    def write_midi(self,name):
        """writes midi file for the piece"""
        time = 0
        MyMIDI = MIDIFile(1)
        MyMIDI.addTempo(track, time, tempo)
        
        for idea in self.ideas:
            for note in idea.melody:
                for pitch in note.pitch:
                    MyMIDI.addNote(track, channel, pitch, time, note.duration, volume)
                time += note.duration

        # adding bass
        time = 0
        for idea in self.ideas:
            for note in idea.bass:
                for pitch in note.pitch:
                    MyMIDI.addNote(track, channel+1, pitch, time, note.duration, volume)
                time += note.duration
        


        with open(f"{name}.mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)
        print(f'Done! Midi file saved as "{name}.mid"')

        


def main():
    chord = []
    name = input('What will be the name of your piece?:')
    while True:
        length = input('How long do you want your piece to be? (ex... 4):' )
        try:
            length = int(length)
            break
        except:
            print('You need to type in a number')
        
    print('You need to pick 4 chords!')
    print('Recommened choices are: Am, C, Dm, Em, F, G')
    for i in range(4):
        user = input("Pick a chord!")
        if len(user)==2:
            user = user[0].upper()+user[1].lower()
        else:
            user = user.upper()
        chord.append(user)
    neg = input("Would you like to see a 'negative harmony' version of your piece as well? Yes or No:")
    print('Creating the piece')
    try:
        p=Piece(length = length,chrd_prg=chord,str_beat=[1,2,3,4])
        p.CA_ideas()
        p.CA_last()
        if neg.lower() == 'yes':
            p.CA_neg_harm()
            print('Created negative harmony')
        p.write_midi(name)
    except:
        print('Failed')
        print('You didnt follow my recommendation it seems')
    input('Press enter to exit')

if __name__ == '__main__':
    main()





