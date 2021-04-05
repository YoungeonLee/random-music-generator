# random music generator

produces semi-random music
created by Youngeon Lee

aims to create music with structured randomness, using a bit of music theory.

to display the music created by this program, Midiutil library (https://pypi.org/project/MIDIUtil/) was utilized to creat a midi file

# main function

main(name='test', length=4, chrd_prg=['C','Am','F','G'], note_lengths={1:1,.5:1}, neg_harm=True)

parameters:  
&nbsp;&nbsp;&nbsp;&nbsp;name(str): name of the midi file  
&nbsp;&nbsp;&nbsp;&nbsp;length(even int): length ideas(4 measures)  
&nbsp;&nbsp;&nbsp;&nbsp;chrd_prg(str[] with length 4): chord has to be either 'C', 'Dm', 'Em', 'F', 'G', or 'Am'  
&nbsp;&nbsp;&nbsp;&nbsp;note_lengths({note_length: weight}): note_length 1 represents quaternote, 0.5 represents eighted notes and so on... weights decide how often they are used (higher means more)  
&nbsp;&nbsp;&nbsp;&nbsp;neg_harm(boolean): if True, the second half of the piece is the first converted into [negative harmony](https://hellomusictheory.com/learn/negative-harmony/)

returns name of the saved file
