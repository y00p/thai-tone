import unicodedata as ucd
from enum import IntEnum

def foundin( listA, listB ):
    return list(set( listA ).intersection( listB ))

class Class(IntEnum):
    HIGH = 0
    MID  = 1
    LOW  = 2

class Tone(IntEnum):
    MID     = 0
    LOW     = 1
    FALLING = 2
    HIGH    = 3
    RISING  = 4

# input of syllable
syllable = input("Please enter a Thai syllable: ")

# Replace the special character 'double R' (รร) by
syllable.replace('รร','ั')

# define character groups
tone_marks      = '่้๊๋'
shortener       = 'ะ็ัิุึฤ'
low_consonants  = 'คฅฆงชซฌญฑฒณทธนพฟภมยรลวฬฮ'
high_consonants = 'ขฃฉฐถผฝศษสห'
mid_consonants  = 'กจฎฏดตบปอ'
plosives        = 'กขคฆปพภฟบตฏถฐทฒฑธจชฌสศษดฎ'

# does syllable end with a consonant?
closed_bool = syllable[-1] in mid_consonants  or \
              syllable[-1] in high_consonants or \
              syllable[-1] in low_consonants

# does syllable have a short vowel?
short_bool = len(foundin( shortener, syllable)) > 0 and \
             'ๅ' not in syllable

# is the syllable 'dead'?
dead_bool = short_bool and not closed_bool or \
            closed_bool and syllable[-1] in plosives

# is there a tone mark?
found_tone_marks = foundin( tone_marks, syllable)

# determine class of first consonant
for c in syllable[0:2]:
    if c in low_consonants:
        class_of_first_consonant = Class.LOW
        break
    elif c in high_consonants:
        class_of_first_consonant = Class.HIGH
        break
    elif c in mid_consonants:
        class_of_first_consonant = Class.MID
        break
else:
    raise ValueError('The syllable might not be proper Thai' )


try:
    class_of_first_consonant
except:
    ValueError('The syllable might not be proper Thai' )


#print( 'The syllable ' + syllable )
#print( '* has tone mark:   ', found_tone_marks )
#print( '* is open:         ', not closed_bool )
#print( '* has short vowel: ', short_bool )
#print( '* first consonant class: ', class_of_first_consonant )

# is there a tone mark?
# (There is never more than one tone mark per syllable)
if len(found_tone_marks) > 0:
    t = found_tone_marks[0]
    # first consonant low class?
    if class_of_first_consonant == Class.LOW:
        if t=='่':
            tone = Tone.FALLING
        elif t=='้':
            tone = Tone.HIGH
        else:
            raise ValueError('The syllable might not be proper Thai' )
    else:
        if t=='่':
            tone = Tone.LOW
        elif t=='้':
            tone = Tone.FALLING
        elif t=='๊':
            tone = Tone.HIGH
        elif t=='๋':
            tone = Tone.RISING
        else:
            raise ValueError('The syllable might not be proper Thai' )
else:
    # dead ( or alive )?
    if dead_bool:
        if class_of_first_consonant == Class.LOW:
            if short_bool:
                tone = Tone.HIGH
            else:
                tone = Tone.FALLING
        else:
            tone = Tone.LOW
    else: #live
        if class_of_first_consonant == Class.HIGH:
            tone = Tone.RISING
        else:
            tone = Tone.MID


# printing the result
tones        = [ 'mid', 'low', 'falling', 'high', 'rising' ]
tone_symbols = [ '', '`', '^', '´', 'ˇ']

print( '\nThe syllable is spoken in ' + tones[tone] + ' tone.' )


# check if syllable is proper thai language
# TODO
