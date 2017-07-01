import unittest
import thaiscript
import thaianalysis

class TestSDetermineTone(unittest.TestCase):

    def test_determine_tone(self):
        ta = thaianalysis.ThaiAnalysis( lp )
        for syllable,target_tone in zip(lp.consonant_words,
                                        lp.consonant_words_tones):
            if len(target_tone)==1: # use monosyllabic words only
                result = ta.determine_tone(syllable,verbose=False);
                self.assertEqual(result,
                                 thaiscript.Tone(target_tone),
                                 syllable)

if __name__ == '__main__':
    lp = thaiscript.LetterProperties()
    lp.load( test_cases = True )
    unittest.main()
