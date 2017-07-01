# README #

A Thai syllable can be spoken in five different tones: mid, low, falling, high and rising.
The same syllable spoken in different tones often have different meanings.
To determine the correct tone of a written syllable, you have to follow particular tone rules.

(This tool follows the tone rules presented by Kris Willems on 
http://womenlearnthai.com/index.php/finding-the-tone-of-a-thai-syllable/)

### What is this repository for? ###

This tool will automatically return the correct tone for the input of any Thai syllable, a line of text with syllables separated by dashes [-], or a text file with thai syllables separated by dashes [-].

v 0.1

### How do I get set up? ###

* Run `python3 ttdt.py` and enter a Thai syllable, a line of text, or hit Enter for processing prepared cases
* Run `python3 ttdt.py elephant_song.txt` or another file
* Run `python3 tests.py` for unittest of tone determination

### Future work ###

* Splitting Thai words into syllables
* ~~Decompose Thai syllable into its components (first and second consonant(cluster), vocal)~~
* ~~Check if input is a formally correct Thai syllable~~
* ~~Determine tone of a single Thai syllable~~


### Who can I talk to? ###

julia@portl.space
