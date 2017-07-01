import csv

class LetterProperties:

    # order of the symbols is important!!
    # exceptions are 'shortener' and 'other_marks'

    shortener    = set('ะ็ัิุึฤ')
    tone_marks   = '่้๊๋'
    other_marks  = set('็์ฺ')

    consonants               = ''
    consonant_classes        = ''
    consonant_plosives       = []
    consonant_initial_sounds = []
    consonant_final_sounds   = []
    consonant_words          = []
    consonant_words_tones    = []

    vowels                   = []
    vowel_locations          = []
    vowel_sounds             = []

    # Load neccessary information about thai characters from files
    def load( self, basics = True, sound = False, test_cases = False ):

        file = open( 'Alphabet.csv' )
        reader = csv.reader( file )
        next(reader) #skip header
        for row in reader:
            if basics:
                self.consonants += row[0]
                self.consonant_classes += row[3]
                self.consonant_plosives.append(row[4] == '1')
            if sound:
                self.consonant_initial_sounds.append(row[1])
                self.consonant_final_sounds.append(row[2])
            if test_cases:
                self.consonant_words.append(row[5])
                self.consonant_words_tones.append(row[6])
        file.close()

        file = open('Vokale.csv')
        reader = csv.reader( file )
        next(reader) # skip header
        for row in reader:
            if basics:
                self.vowels.append(row[0])
                self.vowel_locations.append(row[2])
            if sound:
                self.vowel_sounds.append(row[1])
        file.close()


# <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>

# Represents the tone in which a Thai syllable is spoken
class Tone:

    tones = [ ('m', 'mid',     ' ', '0', 0),
              ('l', 'low',     '`', '1', 1),
              ('f', 'falling', '^', '2', 2),
              ('h', 'high',    '´', '3', 3),
              ('r', 'rising',  'ˇ', '4', 4) ]

    def __init__(self, tone):
        for t in self.tones:
            if str(tone).lower() in t:
                self.tone = t
                break
        else:
            raise ValueError('Input \'{}\' cannot be interpreted as one of '
                             'the five Thai tones: mid, low, falling, high, '
                             'or rising.'.format(tone) )

    def __str__(self):
        return self.tone[1]

    def __int__(self):
        return self.tone[4]

    def __eq__(self, other):
        return (int(self) == int(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def short(self):
        return self.tone[0]

    def symbol(self):
        return self.tone[2]


# <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>

# Represents the class of a Thai consonant
class ConsonantClass(Tone):
    def __init__(self, tone):
        for t in [self.tones[i] for i in [0,1,3]]:
            if str(tone).lower() in t:
                self.tone = t
                break
        else:
            raise ValueError('Input \'{}\' cannot be interpreted as one of '
                             'the three Thai consonant classes: mid, low, '
                             'or high.'.format(tone) )
