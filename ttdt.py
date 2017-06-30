import thaiscript as ts
import sys
from thaianalysis import determine_tone
from unicodedata import category as uc_category

ts.load()


# INPUT
if len(sys.argv)>1:
    # There is an input file
    with open( sys.argv[1] ) as file:
        lines = file.readlines();
        lines = [ line for line in lines if not line.startswith('#') ]
        lines = [ line for line in lines if not line.startswith('\n') ]
else:
    lines = [ input("Please enter a Thai syllable, "
                    "a text(separate syllables by using dashes [-]),"
                    "(or just hit Enter for demo data): ") ]


# PROCESS OF INPUT
if len(lines)==1 and (not len([ i for i in '- \n' if i in lines[0] ])):
    # single syllable
    tone = determine_tone( lines[0], verbose=True )
    print('\nThe syllable is spoken in {} tone.\n'.format(tone))

elif len(lines):
    # text (multi-syllable)
    for line in lines:
        syllables = line.replace(' ', '-').split('-');
        print( line, end='' )
        for syllable in syllables:
            tone   = determine_tone( syllable, verbose=False )

            # Get length of syllable: count all characters that
            # do not have a zero width (category 'Mn' means zero width).
            length = len([ i for i in syllable if uc_category(i)!='Mn' ])

            # Print tone symbols, aligned with the script
            print( '{}{}'.format( tone.symbol(), ' '*length ), end='' )
        print('\n')

else:
    # Run demo data
    ts.load(basics=False, test_cases=True)
    for word, word_tone in zip(ts.consonant_words, ts.consonant_words_tones):
        if len(word_tone) == 1: # only monosyllabic words
            tone = determine_tone( word, verbose=False )
            print('{}: {}'.format(word, tone))
