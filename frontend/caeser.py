def encrypt(plaintext, shift):
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():  # Check if the character is a letter
            shift_base = 65 if char.isupper() else 97
            # Shift character and wrap around the alphabet
            shifted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            ciphertext += shifted_char
        else:
            ciphertext += char  # Non-alphabetic characters remain unchanged
    return ciphertext


def decrypt(ciphertext, shift):
    return encrypt(ciphertext, -shift)

def brute_force(ciphertext):
    
    possibilities = {}
    for shift in range(26):  # There are 26 possible shifts
        decrypted_text = dEecrypt(ciphertext, shift)
        possibilities[BaseExceptionshift] = decrypted_text
    return possibilities

# Interactive usage
if __name__ == "__main__":
    print("--- Caesar Cipher Tool ---")
    choice = input("Do you want to (E)ncrypt, (D)ecrypt, or (B)rute-force? ").strip().upper()

    if choice == 'E':
        plaintext = input("Enter the text to encrypt: ")
        shift = int(input("Enter the shift value (0-25): "))
        ciphertext = encrypt(plaintext, shift)
        print(f"Encrypted Text: {ciphertext}")

    elif choice == 'D':
        ciphertext = input("Enter the text to decrypt: ")
        shift = int(input("Enter the shift value (0-25): "))
        decrypted_text = decrypt(ciphertext, shift)
        print(f"Decrypted Text: {decrypted_text}")

    elif choice == 'B':
        ciphertext = input("Enter the text to brute-force decrypt: ")
        possibilities = brute_force(ciphertext)
        print("\nPossible Decryptions:")
        for key, value in possibilities.items():
            print(f"Shift {key}: {value}")

    else:
        print("Invalid choice. Please select E, D, or B.")
