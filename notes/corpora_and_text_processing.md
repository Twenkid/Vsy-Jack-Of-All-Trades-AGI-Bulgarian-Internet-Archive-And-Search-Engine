# VSY | ВСЕДЪРЖЕЦ

### Software, tools
(should do it automatically) 
Wordless, AntConc, aConcorde (simple, single files) ...  Concordance creators, viewers and more (Wordless 3.5.0)
Just regex (Notepad++ etc.)


* Readability estimation formulas ... (add, generate others incrementally)

* https://github.com/jamesturk/jellyfish - a python library for doing approximate and phonetic matching of strings.

**String comparison:**
```
Levenshtein Distance
Damerau-Levenshtein Distance
Jaccard Index
Jaro Distance
Jaro-Winkler Distance
Match Rating Approach Comparison
Hamming Distance
```
**Phonetic encoding:**
```
American Soundex
Metaphone
NYSIIS (New York State Identification and Intelligence System)
Match Rating Codex
```

```
import jellyfish
jellyfish.levenshtein_distance('jellyfish', 'smellyfish')
jellyfish.jaro_similarity('jellyfish', 'smellyfish')
jellyfish.damerau_levenshtein_distance('jellyfish', 'jellyfihs')
jellyfish.metaphone('Jellyfish')
jellyfish.soundex('Jellyfish')
jellyfish.nysiis('Jellyfish')
jellyfish.match_rating_codex('Jellyfish')
```

---> Apply if not matching with the applied exact or regex search etc., choose the best matches (or according to some constraints). Note 3.4.2025

