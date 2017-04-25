from enum import IntEnum
import csv

def determine_tone( syllable, verbose = False ):

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

    errmsg_notThai = 'This is not a proper Thai syllable.'

    # Replace the special character 'double r' (รร) by its equivalent 'a' (ั)
    syllable.replace('รร','ั')

    # define character groups
    tone_marks      = '่้๊๋'
    shortener       = 'ะ็ัิุึฤ'
    low_consonants  = 'คฅฆงชซฌญฑฒณทธนพฟภมยรลวฬฮ'
    high_consonants = 'ขฃฉฐถผฝศษสห'
    mid_consonants  = 'กจฎฏดตบปอ'
    plosives        = 'กขคฆปพภฟบตฏถฐทฒฑธจชฌสศษดฎ'
    preposed_vowels = 'เแโใไ'

    # does syllable end with a consonant?
    closed_bool = syllable[-2] not in preposed_vowels and \
                  ( syllable[-1] in mid_consonants  or \
                    syllable[-1] in high_consonants or \
                    syllable[-1] in low_consonants )

    # does syllable have a short vowel?
    short_bool = len( set(shortener).intersection(syllable) ) > 0 and \
                 'ๅ' not in syllable

    # is the syllable 'dead'?
    dead_bool = short_bool and not closed_bool or \
                closed_bool and syllable[-1] in plosives

    # is there a tone mark?
    found_tone_marks = list( set(tone_marks).intersection(syllable) )
    if len(found_tone_marks) > 1:
        raise ValueError( 'More than one tone mark found in syllable.\n' \
                          + errmsg_notThai )

    # determine class of first consonant
    # (For this check first two characters,
    #  because first character might be a preposed vowel.)
    first_consonant_position = 1 if syllable[0] in preposed_vowels else 0
    if syllable[ first_consonant_position ] in low_consonants:
        class_of_first_consonant = Class.LOW
    elif syllable[ first_consonant_position ] in high_consonants:
        class_of_first_consonant = Class.HIGH
    elif syllable[ first_consonant_position ] in mid_consonants:
        class_of_first_consonant = Class.MID
    else:
        raise ValueError('None of the first two characters is a consonant.\n' \
                         + errmsg_notThai )

    if verbose:
        print( 'The syllable ' + syllable )
        print( '* has tone mark:   ', found_tone_marks )
        print( '* is open:         ', not closed_bool )
        print( '* has short vowel: ', short_bool )
        print( '* first consonant class: ', class_of_first_consonant )

    # is there a tone mark?
    # (There is never more than one tone mark per syllable)
    if len(found_tone_marks) > 0:
        t = found_tone_marks[0]
        # first consonant low class?
        if class_of_first_consonant == Class.LOW:
            try:
                tone = tone_marks[0:2].index(t) + 2
            except:
                raise ValueError( 'The combination of tone mark', t, \
                      ' and a low consonant is invalid in Thai language.\n', \
                      errmsg_notThai )
        else:
            tone = tone_marks.index(t) + 1
    else:
        # dead ( or alive )?
        if dead_bool:
            if class_of_first_consonant == Class.LOW:
                tone = Tone.HIGH if short_bool else \
                       Tone.FALLING
            else:
                tone = Tone.LOW
        else: #live
            tone = Tone.RISING if class_of_first_consonant == Class.HIGH else \
                   Tone.MID

    return tone

# end of function determine_tone

# input of syllable
#syllable = input("Please enter a Thai syllable: ")
#tone = determine_tone( syllable, True )

# printing the result
tones        = [ 'mid', 'low', 'falling', 'high', 'rising' ]
tone_symbols = [ '', '`', '^', '´', 'ˇ']

# run test file
reader = csv.reader( open( 'testData.txt' ) )

for row in reader:
    print( row[0], row[1], '==', tones[ determine_tone( row[0] ) ][0] )
    if tones[ determine_tone( row[0] ) ][0] != row[1][1]:
        print( "Error for test data: ", row[0] )

#print( '\nThe syllable is spoken in ' + tones[tone] + ' tone.' )



