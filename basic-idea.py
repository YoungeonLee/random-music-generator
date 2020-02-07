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

        

class BasicIdea():
    def __init__(self,)

