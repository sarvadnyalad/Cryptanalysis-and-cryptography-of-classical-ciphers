# function to encrypt text using caeser cipher
def encrypt(plaintext, rotation):
    ciphertext = "" # Initialize an empty string for storing encyrpted text
    for char in plaintext:  # for loop  
        if char.isalpha():  # Check if the character is a letter 
            shift_base = 65 if char.isupper() else 97   # shift_base is ascii value of 'A' or 'a' depends
            # Shift character and wrap around the alphabet,   actual encryption formula
            shifted_char = chr((ord(char) - shift_base + rotation) % 26 + shift_base)    # chr() - converts number to char, ord(chr) - converts char to ascii number   
            ciphertext += shifted_char  
        else:
            ciphertext += char  # Non-alphabetic characters remain unchanged
    return ciphertext

# Function to decrypt text using Caesar cipher
def decrypt(ciphertext, rotation):
    # to decrypt caeser it is just encryption with negative shift
    return encrypt(ciphertext, -rotation)

# Function to brute-force all possible Caesar shift, really helpful when shift is unknown 
def brute_force(ciphertext):
    possibilities = {}  # Dictionary to store all possible shift results
    
    for rotation in range(26):  # for is used to Loop through all 26 possible shift values from 0-25
        decrypted_text = decrypt(ciphertext, rotation)  # Try decrypting with each shift
        possibilities[rotation] = decrypted_text  # Save result along with the shift used
    
    return possibilities        
    
