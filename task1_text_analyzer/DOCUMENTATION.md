# Task 1 - Smart Text Analyzer (Python) - Process Notes

Used Python for this, tried to keep it simple. These are basically my working notes - what I searched, how I built it, issues I ran into etc



## 1. What the task asked for (in my words)

- Take a text string
- Return a few stats:
  - total word count
  - average word length (2 decimal places)
  - list of longest word
  - word frequency map (case‑insensitive)

Decided to wrap everything in a single function that returns a dictionary since the example output in the PDF looks like a JSON object


## 2. Search log (Google / docs / Stack Overflow)

as per the instructions in the email, here are the main searches I did while working on this:

1. **Whitespace splitting in Python**  
   Search: `python split multiple spaces`  
   URL: https://stackoverflow.com/questions/8113782/split-string-on-whitespace-in-python
   - wanted to confirm split() handles multiple spaces, it does

2. **Removing duplicates while keeping order**  
   Search: `python remove duplicates list keep order dict fromkeys`  
   URL: https://stackoverflow.com/questions/480214/how-do-i-remove-duplicates-from-a-list-while-preserving-order
   - needed this for the longest words list

3. **Quick sanity check on word frequency patterns**  
Search: `python count word frequency case insensitive`  
   - ended up just using dict.get(), simple enough



## 3. Thought process / design decisions

- Use plain str.split() instead of regex. The example input is clean and split() without arguments already handles multiple spaces/tabs
- Return one dict with four keys so caller only deals with single return value
- Keep everything O(n) over number of words - one pass to collect lengths and build frequency map, one pass for longest words
- Make function handle empty / whitespace‑only strings so it doesnt crash or divide by zero

Considered using `re.findall(r"\w+", text)` to strip punctuation but the assignment example didn't show any punctuation so I stayed with split(). 


## 4. Step‑by‑step implementation

1. **Function skeleton + empty input handling**  
   Started with `analyze_text(text)` and added a guard right away - if text is None/empty/whitespace only, return dict with zeros/empty structures

2. **Split into words**  
   Used `text.split()` with a list comp to be safe: `[w for w in text.split() if w]`

3. **Word count**  
   Just `len(words)`

4. **Average word length**  
   - `sum(len(w) for w in words)` for total
   - divide by word_count, wrap in `round(..., 2)`
   - kept defensive `if word_count > 0` even tho empty case is handled earlier..

5. **Longest word(s)**  
   - `max_length = max(len(w) for w in words)`
   - filter all words with that length
   - initially had duplicates issue (same longest word appearing twice)
   - fixed with `list(dict.fromkeys(longest_words))`

6. **Word frequency (case‑insensitive)**  
   - empty dict, loop thru words, lowercase, increment with dict.get
   - kept original case for longest_words tho, so output shows what actually appeared

7. **Manual tests**  
   - used example from PDF + few extra cases (empty string, single word, mixed case)
   - these are at bottom of text_analyzer.py



## 5. Problems / gotchas

1. **Duplicate longest words**  
   If same longest word appeared twice, it showed up twice in the list. Fixed with dict.fromkeys

2. **Expected frequency for "the" in the example**  
   The sample output in the PDF shows `"the": 2` but in the actual input `"The quick brown fox jumps over the lazy dog the fox"` the word "the" appears 3 times (case-insensitive). Counted it myself like 3 times. My function returns 3, sure that the PDF example is just wrong



## 6. Why this approach

- **Simple to read** - only built-in types and basic comprehensions
- **Linear time** - one or two passes over word list, no nested loops
- **No dependencies** - runs anywhere with python
- **Easy to extend** - could add median length, top N words etc without changing structure

For this task (short texts, clear requirements) felt like good balance between correct + readable + not over-engineering



