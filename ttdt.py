import thaiscript as ts
from thaianalysis import determine_tone

ts.load()

inputstring = input("Please enter a Thai syllable, "
                    "a text(separate syllables by using dashes [-]),"
                    "(or just hit Enter for demo data): ")

if inputstring:
    # Process user input
    if '-' not in inputstring:
        # single syllable
        tone = determine_tone( inputstring, verbose=True )
        print('\nThe syllable is spoken in {} tone.\n'.format(tone))
    else:
        # text (multi-syllable)
        syllables = inputstring.replace(' ', '-').split('-');
        print( inputstring )
        for syllable in syllables:
            tone = determine_tone( syllable, verbose=False )
            print( '{}{}'.format( tone.symbol(), ' '*len(syllable) ), end='' )
        print('')
else:
    # Run demo data
    ts.load(basics=False, test_cases=True)
    for word, word_tone in zip(ts.consonant_words, ts.consonant_words_tones):
        if len(word_tone) == 1: # only monosyllabic words
            tone = determine_tone( word, verbose=False )
            print('{}: {}'.format(word, tone))
