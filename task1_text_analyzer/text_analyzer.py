def analyze_text(text):
    """
    Analyzes input text and returns stats.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: word_count, average_word_length, longest_words, word_frequency
    """
    # handle empty or whitespace-only text
    if not text or not text.strip():
        return {
            "word_count": 0,
            "average_word_length": 0.00,
            "longest_words": [],
            "word_frequency": {}
        }
    
    # split into words, filter empty strings just in case
    words = [word for word in text.split() if word]
    
    word_count = len(words)
    
    # average word length
    total_length = sum(len(word) for word in words)
    average_word_length = round(total_length / word_count, 2) if word_count > 0 else 0.00
    
    # find longest word(s)
    max_length = max(len(word) for word in words)
    longest_words = [word for word in words if len(word) == max_length]
    longest_words = list(dict.fromkeys(longest_words))  # remove dupes, keep order
    
    # word frequency - case insensitive
    word_frequency = {}
    for word in words:
        word_lower = word.lower()
        word_frequency[word_lower] = word_frequency.get(word_lower, 0) + 1
    
    return {
        "word_count": word_count,
        "average_word_length": average_word_length,
        "longest_words": longest_words,
        "word_frequency": word_frequency
    }


if __name__ == "__main__":
    test_text = "The quick brown fox jumps over the lazy dog the fox"
    result = analyze_text(test_text)
    
    print("Input:", test_text)
    print("\nOutput:")
    print("{")
    print(f'  "word_count": {result["word_count"]},')
    print(f'  "average_word_length": {result["average_word_length"]},')
    print(f'  "longest_words": {result["longest_words"]},')
    print(f'  "word_frequency": {result["word_frequency"]}')
    print("}")
    
    # extra tests
    print("\n" + "="*50)
    print("Additional Test Cases:")
    print("="*50)
    
    print("\nEmpty string:")
    print(analyze_text(""))
    
    print("\nSingle word:")
    print(analyze_text("Hello"))
    
    print("\nMixed case:")
    print(analyze_text("Hello HELLO hello World"))
    
    print("\nLonger text:")
    longer_text = "Python is an amazing programming language that makes development easier"
    print("Input:", longer_text)
    print(analyze_text(longer_text))