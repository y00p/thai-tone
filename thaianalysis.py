import thaiscript as ts

def determine_tone( syllable, verbose = False ):

    errmsg_notThai = 'This is not a proper Thai syllable.'

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
    is_closed = (len([ i for i in syl if i in ts.consonants]) > 1
                 and syl[-1] in ts.consonants)

    # does syllable have a short vowel?
    is_short  = (len([ i for i in syl if i in ts.shortener]) > 0
                 and 'ๅ' not in syl )

    # last consonant is a plosive?
    has_plosive_ending = False
    if is_closed and dict(zip(ts.consonants, ts.consonant_plosives))[syl[-1]]:
        has_plosive_ending = True

    # is the syllable 'dead'?
    is_dead = (is_short and not is_closed or has_plosive_ending)

    # is there a tone mark? Which?
    found_tone_marks = [ i for i in syl if i in ts.tone_marks ]
    if len(found_tone_marks) == 0:
        tone_mark_index = 0
    elif len(found_tone_marks) == 1:
        tone_mark_index = ts.tone_marks.index(found_tone_marks[0])+1
    else:
        raise ValueError('More than one tone mark found in syllable.\n',
                          errmsg_notThai )

    # determine class of first consonant
    # (For this check first two characters,
    #  because first character might be a preposed vowel.)
    if syl[0] in ts.consonants:
        first_consonant = syl[0]
    elif syl[1] in ts.consonants:
        first_consonant = syl[1]
    else:
        raise ValueError('None of the first two characters is a consonant.\n',
                          errmsg_notThai)
    consonant_class = ts.Tone(dict(zip(ts.consonants,
                                       ts.consonant_classes))[first_consonant])

    # Print syllable properties
    if verbose:
        print('The syllable ' + syllable)
        print('* has tone mark:   ', tone_mark_index)
        print('* is open:         ', not is_closed)
        print('* has short vowel: ', is_short)
        print('* consonant class: ', consonant_class)
        print('* is dead:         ', is_dead)
        print('* end plosive:     ', has_plosive_ending)


    # <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>
    # Apply Thai tone rules
    # <<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>

    # is there a tone mark?
    if tone_mark_index:
        # first consonant low class?
        if consonant_class != ts.ConsonantClass('low'):
            # take tone at index
            tone = ts.Tone(tone_mark_index)
        else:
            # take next tone
            tone = ts.Tone(tone_mark_index+1)
    else:
        # dead ( or alive )?
        if is_dead:
            if consonant_class == ts.Tone('low'):
                tone = ts.Tone('high' if is_short else 'falling')
            else:
                tone = ts.Tone('low')
        else: #live
            if consonant_class == ts.ConsonantClass('high'):
                tone = ts.Tone('rising')
            else:
                tone = ts.Tone('mid')

    if verbose:
        print('{} is spoken in {} tone.'.format(syllable, tone))

    return tone

# end of function determine_tone
