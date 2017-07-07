import unittest
import ttdt

class TestSDetermineTone(unittest.TestCase):

    def test_determine_tone(self):
        for syllable,target_tone in zip(consonants['Merkwort'],
                                        consonants['Tones Merkwort']):
            if len(target_tone)==1: # use monosyllabic words only
                result = ttdt.determine_tone(syllable,verbose=False);
                self.assertEqual(str(result),
                                 str(ttdt.Tone(target_tone)),
                                 syllable)

if __name__ == '__main__':
    consonants, vowels = ttdt.init()
    unittest.main()
