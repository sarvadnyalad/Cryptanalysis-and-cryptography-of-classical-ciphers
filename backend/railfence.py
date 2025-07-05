# function to encrypt text using railfence cipher
def railfence_encrypt(plaintext, rails):
    # Ensure that we have at least 2 rails to form a zigzag pattern
    if rails < 2:
        raise ValueError("Number of rails must be at least 2")
    # Create a list of empty strings for each rail
    # Each index represents a "rail" that will collect characters
    fence = [''] * rails    
    current_rail = 0                    # Start writing characters on the top rail (index 0)
    direction = 1                       # Direction to move through the rails: 1 = down, -1 = up

    # Go through each character in the plaintext
    for char in plaintext:
        fence[current_rail] += char     # Add the character to the current rail
        if current_rail == 0:           # Reverse direction when we hit the top or bottom rail
            direction = 1               # start moving downwards
        elif current_rail == rails - 1:
            direction = -1              # start moving upwards
        current_rail += direction       # Move to the next rail in the current direction

    return ''.join(fence)

# function to decrypt text using railfence cipher
def railfence_decrypt(ciphertext, rails):
    # Ensure a minimum of 2 rails to perform decryption
    if rails < 2:
        raise ValueError("Number of rails must be at least 2")
    
    # The pattern repeats every 'cycle' characters (down and up)
    cycle = 2 * rails - 2

    # Determine how many characters go into each rail
    # Initialize a list to keep the character count per rail
    lengths = [0] * rails

    # Loop through each character position to assign it to the correct rail
    for i in range(len(ciphertext)):
        remainder = i % cycle
        # Determine rail index based on zigzag logic
        rail = remainder if remainder < rails else 2 * rails - 2 - remainder
        lengths[rail] += 1

    # Based on the lengths, slice the ciphertext into rail segments
    fence = []
    index = 0
    for length in lengths:
        fence.append(list(ciphertext[index:index+length]))      # Create a list of characters for each rail segment
        index += length

    # Now reconstruct the original plaintext by reading in zigzag order
    plaintext = []
    current_rail = 0
    direction = 1

# Simulate zigzag reading of the rails to reconstruct original order
    for _ in range(len(ciphertext)):
        plaintext.append(fence[current_rail].pop(0))
        if current_rail == 0:       # Change direction when we hit the top or bottom rail
            direction = 1
        elif current_rail == rails - 1:
            direction = -1
        current_rail += direction   # Move to the next rail
    
    return ''.join(plaintext)       # Join the list of characters into the decrypted message
