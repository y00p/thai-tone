import thaiscript as ts
from thaianalysis import determine_tone

ts.load()

syllable = input("Please enter a Thai syllable (or just hit Enter): ")

if syllable:
    # Process user input
    tone = determine_tone( syllable, verbose=True )
    print('\nThe syllable is spoken in {} tone.\n'.format(tone))
else:
    # Run demo data
    ts.load(basics=False, test_cases=True)
    for word, word_tone in zip(ts.consonant_words, ts.consonant_words_tones):
        if len(word_tone) == 1: # only monosyllabic words
            tone = determine_tone( word, verbose=False )
            print('{}: {}'.format(word, tone))




