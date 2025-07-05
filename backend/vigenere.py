# function to encrypt text using vigenere cipher
import re   # import regular expressions for text validation

def generate_vigenere_key(text, key):
    key = key.upper()  # Convert key to uppercase to standardize
    expanded_key = ""  # Store the expanded version of the key
    key_index = 0  # Track which character from the key to use

    for char in text:
        if char.isalpha():  # Only expand key for letters
            expanded_key += key[key_index % len(key)]  # Repeat key letters cyclically
            key_index += 1  # Move to next key character for next letter
        else:
            expanded_key += char  # Non-letters (spaces, punctuation) are left unchanged

    return expanded_key  # Return the final expanded key


# Encrypt plaintext using Vigenère cipher
def encrypt_vigenere(plaintext, key):
    ciphertext = ""  # Initialize encrypted output string
    expanded_key = generate_vigenere_key(plaintext, key)  # Match key length with text

    for p, k in zip(plaintext, expanded_key):  # Iterate through both plaintext and expanded key together
        if p.isalpha():  # Encrypt only alphabetic characters
            shift = ord(k) - 65  # Determine shift amount from key letter (A=0)/ converts key letters to numbers
            shift_base = 65 if p.isupper() else 97  # ASCII base for uppercase or lowercase
            # Apply shift and wrap around alphabet
            ciphertext += chr((ord(p) - shift_base + shift) % 26 + shift_base)
        else:
            ciphertext += p  # Leave special characters as-is

    return ciphertext  # Return final encrypted string, += adds results to growing cipher text

# Decrypt ciphertext using Vigenère cipher
def decrypt_vigenere(ciphertext, key):
    plaintext = ""  # Initialize decrypted output string
    expanded_key = generate_vigenere_key(ciphertext, key)  # Match key length with text

    for c, k in zip(ciphertext, expanded_key):  # Iterate through ciphertext and key
        if c.isalpha():  # Decrypt only alphabetic characters
            shift = ord(k) - 65  # Shift determined from key letter
            shift_base = 65 if c.isupper() else 97  # ASCII base
            # Subtract shift and wrap around alphabet
            plaintext += chr((ord(c) - shift_base - shift) % 26 + shift_base)
        else:
            plaintext += c  # Leave non-letters unchanged

    return plaintext  # Return final decrypted string


# Check if the key is valid (only alphabet letters)
def is_valid_key(key):
    return bool(re.match("^[A-Za-z]+$", key))  # True if key has only letters


# Clean input text by removing spaces and converting to uppercase
def sanitize_input(text):
    return text.strip()  # Remove leading/trailing whitespace

