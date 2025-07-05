import re
from collections import Counter


def detect_cipher_type(ciphertext):
    if not ciphertext or len(ciphertext.strip()) < 20:
        return {"suggestion": "Text too short (min 20 chars)"}
    
    clean_text = re.sub(r'[^A-Za-z]', '', ciphertext.upper())
    if not clean_text:
        return {"suggestion": "No letters detected"}
    
    # Basic frequency analysis
    freqs = Counter(clean_text)
    total_chars = len(clean_text)

    # Digraph analysis (for transposition detection)
    digraphs = [clean_text[i]+clean_text[i+1] for i in range(len(clean_text)-1)]
    repeated_digraphs = sum(count > 1 for _, count in Counter(digraphs).items())
    
    # Simple English frequency check
    common_english = {'E', 'T', 'A', 'O', 'I', 'N'}
    top_letters = {letter for letter, _ in freqs.most_common(3)}
    
    # Decision logic
    is_transposition = (
        repeated_digraphs / len(digraphs) > 0.25  # This checks if more than 25% of digraphs repeat — which is a sign of transposition ciphers
        and len(top_letters & common_english) < 2  # This checks how many of the top 3 letters in the ciphertext match common English letters like E, T, A, O, I, N.
    )
    
    if is_transposition:
        return {"suggestion": "Transposition cipher"}
    else:
        return {"suggestion": "Substitution cipher"}
    
