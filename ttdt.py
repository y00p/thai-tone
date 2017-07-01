import sys
from unicodedata import category as uc_category
import thaiscript
import thaianalysis

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

lp = thaiscript.LetterProperties()

# PROCESS OF INPUT
if not lines[0]: # no input will reslt in lines=[''],
                 # so there is always one element
    # No input -> Run demo data
    lp.load(basics=True, test_cases=True)
    ta = thaianalysis.ThaiAnalysis( lp )
    for word, word_tone in zip(lp.consonant_words, lp.consonant_words_tones):
        if len(word_tone) == 1: # only monosyllabic words
            tone = ta.determine_tone( word, verbose=False )
            print('{}: {}'.format(word, tone))

elif ( len(lines)==1 and
     (not len([ i for i in '- \n' if i in lines[0] ]))):
    # single syllable (there is no delimiter found + one-liner)
    lp.load()
    ta = thaianalysis.ThaiAnalysis( lp )
    tone = ta.determine_tone( lines[0], verbose=True )
    print('\nThe syllable is spoken in {} tone.\n'.format(tone))

else:
    # text (multi-syllable, one or more lines)
    lp.load()
    ta = thaianalysis.ThaiAnalysis( lp )
    for line in lines:
        syllables = line.replace(' ', '-').split('-');
        print( line.strip('\n') )
        for syllable in syllables:
            tone   = ta.determine_tone( syllable, verbose=False )

            # Get length of syllable: count all characters that
            # do not have a zero width (category 'Mn' means zero width).
            length = len([ i for i in syllable if uc_category(i)!='Mn' ])

            # Print tone symbols, aligned with the script
            print( '{}{}'.format( tone.symbol(), ' '*length ), end='' )
        print('\n')
