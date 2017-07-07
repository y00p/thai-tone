import sys
from unicodedata import category as uc_category
from re import split
from csv import DictReader
from collections import  defaultdict


# Load Thai letter information
consonants, vowels = init()

# <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>

def determine_tone( syllable, verbose = False ):

    errmsg_notThai = 'This is not a proper Thai syllable.'

    shortener    = set('ะ็ัิุึฤ')
    tone_marks   = '่้๊๋'
    other_marks  = set('็์ฺ')

    # working copy
    syl = syllable

    # Replace the special character 'double r' (รร) by its equivalent 'a' (ั)
    syl = syl.replace('รร','ั')

    # Remove repetition character
    syl = syl.replace('ๆ','' );

    # Remove last consonant if silent (i.e. it has a ์ mark)
    if syl.endswith('์'):
        syl = syl[:-2]


    # <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>
    # Check Syllable properties
    # <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>

    # does syllable end with a consonant?
    is_closed = (len([ i for i in syl if i in consonants['Zeichen']]) > 1
                 and syl[-1] in consonants['Zeichen'])

    # does syllable have a short vowel?
    is_short  = (len([ i for i in syl if i in shortener]) > 0
                 and 'ๅ' not in syl )

    # last consonant is a plosive?
    has_plosive_ending = False
    if is_closed and dict(zip(consonants['Zeichen'],
                              consonants['Plosive']))[syl[-1]]=='1':
        has_plosive_ending = True

    # is the syllable 'dead'?
    is_dead = (is_short and not is_closed or has_plosive_ending)

    # is there a tone mark? Which?
    found_tone_marks = [ i for i in syl if i in tone_marks ]
    if len(found_tone_marks) == 0:
        tone_mark_index = 0
    elif len(found_tone_marks) == 1:
        tone_mark_index = tone_marks.index(found_tone_marks[0])+1
    else:
        raise ValueError('More than one tone mark found in syllable.\n',
                          errmsg_notThai )

    # determine class of first consonant
    # (For this check first two characters,
    #  because first character might be a preposed vowel.)
    if syl[0] in consonants['Zeichen']:
        first_consonant = syl[0]
    elif syl[1] in consonants['Zeichen']:
        first_consonant = syl[1]
    else:
        raise ValueError('None of the first two characters is a consonant.\n',
                          errmsg_notThai)
    consonant_class = Tone(dict(zip(consonants['Zeichen'],
                                    consonants['Klasse']))[first_consonant])

    # Print syllable properties
    if verbose:
        print('The syllable ' + syllable)
        print('* has tone mark:   ', tone_mark_index)
        print('* is open:         ', not is_closed)
        print('* has short vowel: ', is_short)
        print('* consonant class: ', consonant_class)
        print('* is dead:         ', is_dead)
        print('* end plosive:     ', has_plosive_ending)
        print('')


    # <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>
    # Apply Thai tone rules
    # <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>

    # is there a tone mark?
    if tone_mark_index:
        # first consonant low class?
        if consonant_class != ConsonantClass('low'):
            # take tone at index
            tone = Tone(tone_mark_index)
        else:
            # take next tone
            tone = Tone(tone_mark_index+1)
    else:
        # dead ( or alive )?
        if is_dead:
            if consonant_class == Tone('low'):
                tone = Tone('high' if is_short else 'falling')
            else:
                tone = Tone('low')
        else: #live
            if consonant_class == ConsonantClass('high'):
                tone = Tone('rising')
            else:
                tone = Tone('mid')

    return tone


# <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>
# Load thai script information
# <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>

def __columnwise_table( filename ):
    result = defaultdict(list)
    with open(filename,'rU') as f:
        reader = DictReader(f)
        for row in reader:
            for col,dat in row.items():
                result[col].append(dat)
    return result


def init():
    consonants = __columnwise_table('Alphabet.csv')
    vowels     = __columnwise_table('Vokale.csv')
    return consonants, vowels


# <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>
# Classes
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


# <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>
# Skript
# <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>

if __name__ == '__main__':


    # Output formats
    # A. (list of) 'syllable: tone'-pair
    # B. one line syllables, next line symbols

    # Input formats
    # 1. List of syllables or single syllable               (->A)
    # 2. Text (one or more lines with dashes and/or spaces) (->B)


    # <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>
    # Get input
    # <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>

    if len(sys.argv)>1:
        # There is an input file -> input format 3
        with open( sys.argv[1] ) as file:
            orig_input = file.readlines()

            # omit commented or empty lines
            orig_input = [line for line in orig_input
                          if not (line.startswith('#') or line.startswith('\n'))]
    else:
        orig_input = [input("Please enter a Thai syllable, "
                            "a text(separate syllables by using dashes [-]),"
                            "(or just hit Enter for demo data): ")]


    # <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>
    # Preprocess input
    # <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>

    if not orig_input[0]: # no input will result in inp=[''],
                     # so there is always one element
        # No input -> Run demo data
        syllables = [ word
                      for word,tone
                      in zip(consonants['Merkwort'], consonants['Tones Merkwort'])
                      if len(tone)==1 ]
    else:
        # text (multi-syllable, one or more lines)
        nested_syllables = [[ syllable
                              for syllable in split(' |-|\n', line) if syllable ]
                              for line in orig_input ]
        syllables = [ syllable
                      for syllable_list in nested_syllables
                      for syllable in syllable_list]


    # <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>
    # Process input
    # <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>

    tones = []
    for syllable in syllables:
        tones.append( determine_tone( syllable, len(syllables)==1 ) )


    # <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>
    # Output
    # <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>

    if set(' -').isdisjoint(''.join(orig_input)):
        # output format A
        for syllable, tone in zip(syllables, tones):
            print(syllable+': '+str(tone))

    else:
        #output format B
        tone_iterator = iter( tones )
        orig_input_line_iterator = iter( orig_input )
        for line in nested_syllables:
            print( next(orig_input_line_iterator).strip('\n') )
            for syllable in line:
                length = len([ i for i in syllable if uc_category(i)!='Mn' ])
                print( next(tone_iterator).symbol()+' '*length, end='')
            print('')
