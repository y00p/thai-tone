import thaiscript as ts
from thaianalysis import determine_tone

ts.load()

# input of syllable #####################################################
syllable = input("Please enter a Thai syllable: ")
tone = determine_tone( syllable, verbose=False )
print('\nThe syllable is spoken in {} tone.\n'.format(tone))
