import re

# Load a list of English words from a file and return them in uppercase
def load_dictionary(file_path="words_alpha.txt"):      
    try:                                                # Open the file in read mode
        with open(file_path, "r") as f:
            # Strip whitespace/newlines and convert each word to uppercase
            return [word.strip().upper() for word in f] 
    except FileNotFoundError:
        return []

def find_matches(pattern, dictionary_words):            # Find dictionary words matching a given pattern with wildcards.
    pattern = pattern.replace(" ", "_").upper()         # Normalize pattern: replace spaces with underscore and uppercase it
    # Build a regex: '_' becomes '.', matching any single character.
    regex_pattern = "^" + pattern.replace("_", ".") + "$"   # "^ start of the word, "$" end of word, "."/"_" Missing words

    try:
        # Compile the regex for efficient matching
        regex = re.compile(regex_pattern)
        # Filter the dictionary for words that match the regex
        return [word for word in dictionary_words if regex.match(word)]
    except re.error:
        return []

