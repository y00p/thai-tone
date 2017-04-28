import unittest
import thaiscript as ts
import thaianalysis as ta

class TestSDetermineTone(unittest.TestCase):

    def test_determine_tone(self):
        for syllable,target_tone in zip(ts.consonant_words,
                                        ts.consonant_words_tones):
            if len(target_tone)==1: # use monosyllabic words only
                result = ta.determine_tone(syllable,verbose=False);
                self.assertEqual(result, ts.Tone(target_tone), syllable)

if __name__ == '__main__':
    ts.load( test_cases = True )
    unittest.main()
