# function to encrypt text using playfair cipher
import re   # import regular expressions for text validation

# a class for handling Playfair cipher operations
class PlayfairCipher:
    def __init__(self, key, merge_j=True):
        self.merge_j = merge_j  # Option to merge I and J as the same letter (standard Playfair behavior)
        self.matrix = self.generate_matrix(key)  # Generate 5x5 (or 6x5) matrix based on the key

    def generate_matrix(self, key):
        key = key.upper()  # Convert key to uppercase for consistency
        if self.merge_j:
            key = key.replace("J", "I")  # Standard Playfair replaces J with I

        key = "".join(dict.fromkeys(key))  # Remove duplicate letters from key while keeping order

        # Alphabet excluding J (if merge_j is True)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" if self.merge_j else "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # Build the matrix by adding key letters followed by remaining unused letters from alphabet
        matrix = list(key + "".join([c for c in alphabet if c not in key]))

        # Convert the flat list into 5x5 grid (or 6x5 if merge_j is False)
        return [matrix[i:i+5] for i in range(0, 25 if self.merge_j else 26, 5)]


    def display_matrix(self):
        #Displays the Playfair matrix neatly
        print("\nPlayfair Cipher Matrix:")
        for row in self.matrix:
            print(" ".join(row))
        print()

    def prepare_text(self, text, encrypting=True):
        # Prepares plaintext or ciphertext into digraphs for encryption or decryption
        text = text.upper()
        if self.merge_j:
            text = text.replace("J", "I")

        text = re.sub(r'[^A-Z]', '', text)  # Remove all non-letter characters
        pairs = []
        i = 0

        while i < len(text):
            a = text[i]
            b = ""

            if i + 1 < len(text):
                b = text[i + 1]
                if a == b:
                    b = "X"  # Insert X if two letters are the same
                    i += 1
                else:
                    i += 2
            else:
                b = "X"  # Append X if last letter has no pair
                i += 1

            pairs.append(a + b)

        return pairs
     
    def find_position(self, letter):
        # Search through the matrix to find the position (row, col) of a letter
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                if self.matrix[row][col] == letter:
                    return row, col

    def encrypt_pair(self, pair):
        row1, col1 = self.find_position(pair[0])
        row2, col2 = self.find_position(pair[1])

        if row1 == row2:  # If both letters are in the same row, shift right
            return self.matrix[row1][(col1 + 1) % 5] + self.matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:  # If both letters are in the same column, shift down
            return self.matrix[(row1 + 1) % 5][col1] + self.matrix[(row2 + 1) % 5][col2]
        else:  # If they form a rectangle, swap corners
            return self.matrix[row1][col2] + self.matrix[row2][col1]

    def decrypt_pair(self, pair):
        row1, col1 = self.find_position(pair[0])
        row2, col2 = self.find_position(pair[1])

        if row1 == row2:  # If same row, shift left
            return self.matrix[row1][(col1 - 1) % 5] + self.matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:  # If same column, shift up
            return self.matrix[(row1 - 1) % 5][col1] + self.matrix[(row2 - 1) % 5][col2]
        else:  # If rectangle, swap corners
            return self.matrix[row1][col2] + self.matrix[row2][col1]

    def encrypt(self, plaintext):
        pairs = self.prepare_text(plaintext)  # Convert text to digraphs
        encrypted_text = "".join(self.encrypt_pair(pair) for pair in pairs)  # Encrypt each digraph

        # Return in 2-letter blocks separated by spaces
        return " ".join([encrypted_text[i:i+2] for i in range(0, len(encrypted_text), 2)])
    
    def decrypt(self, ciphertext):
        # Decrypt the entire ciphertext using Playfair cipher
        pairs = self.prepare_text(ciphertext, encrypting=False)  # Get pairs from cipher text
        decrypted_text = "".join(self.decrypt_pair(pair) for pair in pairs)  # Decrypt each digraph

        # Optional: safely remove trailing 'X' if it was padding
        if decrypted_text.endswith("X"):
            decrypted_text = decrypted_text[:-1]

        return decrypted_text  # Return final decrypted message
        
