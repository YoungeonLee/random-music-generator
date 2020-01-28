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
tempo    = 60   # In BPM
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
cd=chord('Cm')

"""
MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)

for i, pitch in enumerate(degrees):
    MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
    """
class Note():
    def __init__(self,pitch=60,duration=1):
        self.pitch = pitch
        self.duration = duration
    def __repr__(self):
    	return f"Pitch: {self.pitch} / Duration: {self.duration}\n"

class Measure():
	def __init__(self,duration=4,chord='C'):
		self.duration = duration
		self.chord = chord
		self.notes = []
	def __repr__(self):
		return f"{self.notes}"
	def add_note(self,Note):
		self.notes.append(Note)
	def CA_notes(self):
		"""create and add random notes"""
		for i in range(4):
			rnote = Note(random.choice(notes))
			self.add_note(rnote)



class Melody():
	def __init__(self,length=8):
		self.length = length
		self.measures = []
	def __repr__(self):
		return f'{self.measures}'
	def add_measure(self,Measure):
		self.measures.append(Measure)
	def CA_measures(self):
		"""creates and add random measure"""
		for i in range(8):
			rmeasure = Measure()
			rmeasure.CA_notes()
			self.add_measure(rmeasure)

class Piece():
	def __init__(self,length=100,scale='C'):
		self.length = length
		self.scale = scale
		self.melodies = []
	def __repr__(self):
		return f'{self.melodies}'
	def add_melody(self,Melody):
		self.melodies.append(Melody)
	def CA_melodies(self):
		"""create and add random melodies"""
		for i in range(4):
			rmelody = Melody()
			rmelody.CA_measures()
			self.add_melody(rmelody)
#test
p=Piece()


        

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
