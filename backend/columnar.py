import re
import math

def keyword_to_numeric_key(keyword: str) -> list[int]:
    """ Turn a keyword into a numeric permutation. E.g. "SECRET" → [4,2,0,3,1,5] """
    # Keep only letters, uppercase
    kw = re.sub(r'[^A-Z]', '', keyword.upper())
    # Pair letters with original indices
    indexed = list(enumerate(kw))  # [(0,'S'), (1,'E'), ...]
    # Sort by letter, then index (to break ties for repeated letters)
    sorted_by_letter = sorted(indexed, key=lambda x: (x[1], x[0]))
    # Build numeric key: original_index -> rank
    numeric_key = [0] * len(kw)
    for rank, (orig_idx, _) in enumerate(sorted_by_letter):
        numeric_key[orig_idx] = rank
    return numeric_key

def encrypt(plaintext: str, key: str | list[int]) -> str:
    """ Columnar encryption. Key may be a keyword (str) or numeric list. Non-letters are stripped, text is uppercased, and padded with 'X'. """
    # 1) Derive numeric key
    if isinstance(key, str):
        key_list = keyword_to_numeric_key(key)
    else:
        key_list = key

    # 2) Normalize text: letters only, uppercase
    text = re.sub(r'[^A-Za-z]', '', plaintext).upper()

    # 3) Pad with 'X' so length % cols == 0
    cols = len(key_list)
    pad_len = (-len(text)) % cols
    text += 'X' * pad_len

    # 4) Build row-wise grid
    rows = len(text) // cols
    grid = [list(text[r*cols:(r+1)*cols]) for r in range(rows)]

    # 5) Read columns in key order
    ciphertext = []
    for _, col_idx in sorted((k, i) for i, k in enumerate(key_list)):
        for r in range(rows):
            ciphertext.append(grid[r][col_idx])
    return ''.join(ciphertext)

def decrypt(ciphertext: str, key: str | list[int]) -> str:
    """ Columnar decryption. Accepts same key types. Strips trailing 'X' padding. """
    # 1) Numeric key
    if isinstance(key, str):
        key_list = keyword_to_numeric_key(key)
    else:
        key_list = key
    cols = len(key_list)
    length = len(ciphertext)
    rows = length // cols

    # 2) calculates column heights (all equal since we padded)
    col_heights = {i: rows for i in range(cols)}

    # 3) Slice ciphertext into each column by key order
    cols_data = {}
    pos = 0
    for _, orig_idx in sorted((k, i) for i, k in enumerate(key_list)):
        cols_data[orig_idx] = list(ciphertext[pos:pos+rows])
        pos += rows

    # 4) Read off row-wise to rebuild plaintext
    plaintext = []
    for r in range(rows):
        for c in range(cols):
            plaintext.append(cols_data[c].pop(0))
    plaintext = ''.join(plaintext)

    # 5) Strip padding
    return plaintext.rstrip('X')


