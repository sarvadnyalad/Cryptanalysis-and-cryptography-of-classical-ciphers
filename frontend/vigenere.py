import re

def generate_vigenere_key(text, key):
    key = key.upper()
    expanded_key = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            expanded_key += key[key_index % len(key)]
            key_index += 1
        else:
            expanded_key += char  # Keep spaces and special characters unchanged
    return expanded_key


def encrypt_vigenere(plaintext, key):
    ciphertext = ""
    expanded_key = generate_vigenere_key(plaintext, key)
    
    for p, k in zip(plaintext, expanded_key):
        if p.isalpha():
            shift = ord(k) - 65
            shift_base = 65 if p.isupper() else 97
            ciphertext += chr((ord(p) - shift_base + shift) % 26 + shift_base)
        else:
            ciphertext += p  # Keep non-alphabetic characters unchanged
    
    return ciphertext


def decrypt_vigenere(ciphertext, key):
    plaintext = ""
    expanded_key = generate_vigenere_key(ciphertext, key)
    
    for c, k in zip(ciphertext, expanded_key):
        if c.isalpha():
            shift = ord(k) - 65
            shift_base = 65 if c.isupper() else 97
            plaintext += chr((ord(c) - shift_base - shift) % 26 + shift_base)
        else:
            plaintext += c  # Keep non-alphabetic characters unchanged
    
    return plaintext


def is_valid_key(key):
    """Check if the key contains only alphabetic characters."""
    return bool(re.match("^[A-Za-z]+$", key))


def sanitize_input(text):
    """Removes leading/trailing spaces and converts to uppercase for consistency."""
    return text.strip()


# Interactive usage
if __name__ == "__main__":
    print("--- Vigenère Cipher Tool ---")
    while True:
        choice = input("Do you want to (E)ncrypt, (D)ecrypt, or (Q)uit? ").strip().upper()
        
        if choice == 'Q':
            print("Exiting...!")
            break
        
        if choice in ['E', 'D']:
            text = sanitize_input(input("Enter the text: "))
            key = sanitize_input(input("Enter the key (only letters): "))
            
            while not is_valid_key(key):
                print("Invalid key! The key should contain only letters.")
                key = sanitize_input(input("Enter the key (only letters): "))
            
            if choice == 'E':
                result = encrypt_vigenere(text, key)
                print(f"Encrypted Text: {result}")
            else:
                result = decrypt_vigenere(text, key)
                print(f"Decrypted Text: {result}")
        else:
            print("Invalid choice. Please select E, D, or Q.")
