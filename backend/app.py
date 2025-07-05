import string
from flask import Flask, request, jsonify  # Import necessary Flask modules
from flask_cors import CORS  # Import CORS to enable cross-origin requests
import re  # Import regex module for input validation
from collections import Counter  # Import Counter for frequency analysis

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for handling cross-origin requests

# Import encryption and decryption functions from external files
from caeser import encrypt as caesar_encrypt, decrypt as caesar_decrypt         # Import Caesar cipher functions, # type: ignore
from vigenere import encrypt_vigenere, decrypt_vigenere         # Import Vigenere cipher functions, # type: ignore
from playfair import PlayfairCipher         # Import Playfair cipher class, # type: ignore
from railfence import railfence_encrypt, railfence_decrypt      # type: ignore
from columnar import encrypt as columnar_encrypt, decrypt as columnar_decrypt, keyword_to_numeric_key   # type: ignore
from dictionary_helper import load_dictionary, find_matches # type: ignore
from detector import detect_cipher_type # type: ignore

# Define a route to process text encryption or decryption
@app.route("/process", methods=["POST"])
def process_text():
    data = request.json  # Get JSON data from the request
    text = data.get("text", "")  # Extract text input
    action = data.get("action")  # Get the action (encrypt/decrypt)
    cipher = data.get("cipher")  # Get the cipher type
    output = ""  # Initialize output variable

    if not text.strip():
        return jsonify({"output": "Error: Text input cannot be empty."})

    # Handle Caesar cipher
    if cipher == "caesar":
        try:
            shift = int(data.get("shift", 3))  # Get shift value, default is 3
            if action == "encrypt":
                output = caesar_encrypt(text, shift)  # Encrypt text using Caesar cipher
            else:
                output = caesar_decrypt(text, shift)  # Decrypt text using Caesar cipher
        except ValueError:
            return jsonify({"output": "Error: Invalid shift value."})  # Handle invalid shift values

    # Handle Vigenere cipher
    elif cipher == "vigenere":
        key = data.get("key", "")  # Get key for Vigenere cipher
        if not re.match("^[A-Za-z]+$", key):  # Validate key
            return jsonify({"output": "Error: Key must contain only letters."})
        if action == "encrypt":
            output = encrypt_vigenere(text, key)  # Encrypt text using Vigenere cipher
        else:
            output = decrypt_vigenere(text, key)  # Decrypt text using Vigenere cipher

    # Handle Playfair cipher
    elif cipher == "playfair":
        key = data.get("key", "")  # Get key for Playfair cipher
        if not re.match("^[A-Za-z]+$", key):  # Validate key format
            return jsonify({"output": "Error: Key must contain only letters."})

        cipher = PlayfairCipher(key)  # Create Playfair cipher object

        if action == "encrypt":
            output = cipher.encrypt(text)  # Encrypt text using Playfair cipher
        else:
            output = cipher.decrypt(text)  # Decrypt text using Playfair cipher
            
    # handle railfence
    elif cipher == "railfence":
        try:
            rails = int(data.get("rails", 2))  # Default to 2 rails if not specified
            if rails < 2:
                return jsonify({"output": "Error: Number of rails must be at least 2."})
            if action == "encrypt":
                output = railfence_encrypt(text, rails)  # Encrypt using Rail Fence
            else:
                output = railfence_decrypt(text, rails)  # Decrypt using Rail Fence
        except Exception as e:
            return jsonify({"output": f"Error: {str(e)}"})
        
    # Handle Columnar cipher
    elif cipher == "columnar":
        # Read the key as a string and strip whitespace
        key_str = data.get("key", "").strip()

        # If the key looks like numbers separated by dashes, treat it as a numeric permutation
        if re.fullmatch(r'\d+(?:-\d+)*', key_str):
            # Convert "3-0-2-1" → [3, 0, 2, 1]
            key_list = [int(n) for n in key_str.split('-')]
            # Check it’s a proper 0..N–1 permutation
            if sorted(key_list) != list(range(len(key_list))):
                return jsonify({"output": "Error: Numeric key must be a 0..N-1 permutation."})

        else:
            # Otherwise expect an alphabetic keyword
            if not key_str.isalpha():
                return jsonify({"output": "Error: Keyword must be letters only."})
            # Convert e.g. "ZEBRA" → [4, 1, 3, 0, 2] based on alphabetical order
            key_list = keyword_to_numeric_key(key_str)

        # Perform the chosen action
        if action == "encrypt":
            output = columnar_encrypt(text, key_list)   # scramble columns
        else:
            output = columnar_decrypt(text, key_list)   # unscramble columns


    else:
        output = "Error: Invalid cipher selection."  # Handle invalid cipher selection

    return jsonify({"output": output})  # Return processed text as JSON response



# Route for trying every possible Caesar shift on the input text
@app.route("/bruteforce", methods=["POST"])
def brute_force_caesar():
    # 1. Parse the incoming JSON and pull out the ciphertext
    data = request.json
    text = data.get("text", "")

    # 2. Quick sanity check: make sure there's actually something to decrypt
    if not text.strip():
        return jsonify({"output": "Error: Text input cannot be empty."})

    # 3. Bring in our Caesar decrypt function, renaming it for clarity
    from caeser import decrypt as caesar_decrypt

    # 4. Build a dictionary mapping each shift (1–25) to its decrypted candidate
    possibilities = {
        shift: caesar_decrypt(text, shift)
        for shift in range(1, 26)
    }

    # 5. Send back all 25 decryption guesses for the user to inspect
    return jsonify({"output": possibilities})



# Define a route to analyze letter frequency and compare it with English
@app.route("/frequency-analysis", methods=["POST"])
def frequency_analysis():
    # 1. Parse JSON and normalize to uppercase
    data = request.json
    text = data.get("text", "").upper()

    # 2. Ensure there's actual text to process
    if not text.strip():
        return jsonify({"error": "Text input cannot be empty."})

    # 3. Strip out anything that isn’t A–Z
    filtered_text = re.sub(r"[^A-Z]", "", text)

    # 4. Count how often each letter appears
    letter_counts = Counter(filtered_text)

    # 5. Sum to get the total letters counted
    total_letters = sum(letter_counts.values())

    # 6. Reference English letter frequencies for comparison
    english_frequencies = {
        'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
        'S': 6.3,  'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8,
        'U': 2.8,  'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0,
        'P': 1.9,  'B': 1.5, 'V': 1.0, 'K': 0.8, 'J': 0.2, 'X': 0.2,
        'Q': 0.1,  'Z': 0.1
    }

    # 7. Compute the percentage frequency of each observed letter
    frequencies = {
        letter: round((count / total_letters) * 100, 2)
        for letter, count in letter_counts.items()
    }

    # 8. Return both the observed and standard English frequencies
    return jsonify({
        "frequencies": frequencies,
        "english_frequencies": english_frequencies
    })



# Apply a user-defined letter mapping to the ciphertext
@app.route("/apply-mapping", methods=["POST"])
def apply_mapping():
    # Parse JSON payload and get ciphertext & mapping dict
    data = request.get_json()
    ciphertext = data.get("ciphertext", "")
    mapping = data.get("mapping", {})

    # Initialize the result container
    plaintext = ""
    # For each character in the input text
    for char in ciphertext:
        # If there's a mapping for this letter (ignore case) and it's non-empty
        if char.upper() in mapping and mapping[char.upper()]:
            sub_char = mapping[char.upper()]
            # Preserve original case of the character
            plaintext += sub_char.lower() if char.islower() else sub_char.upper()
        else:
            # No mapping: leave character (including punctuation/spaces) as-is
            plaintext += char

    # Send back the partially or fully decoded preview
    return jsonify({"plaintext_preview": plaintext})



# Define a POST endpoint for manual frequency breakdown of ciphertext
@app.route("/manual-frequency", methods=["POST"])
def manual_frequency():
    try:
        # 1. Parse JSON payload and extract the ciphertext (default to empty string)
        data = request.get_json()
        ciphertext = data.get("ciphertext", "")
        # 2. Validate input: reject if it's all whitespace or empty
        if not ciphertext.strip():
            return jsonify({"error": "No ciphertext provided."}), 400

        # 3. Filter: keep only A–Z letters, converted to uppercase
        filtered = [c.upper() for c in ciphertext if c.upper() in string.ascii_uppercase]
        # 4. Count occurrences of each letter
        counts = Counter(filtered)
        # 5. Compute total number of letters found
        total = sum(counts.values())

        # 6. If there are no letters, return an empty frequencies list
        if total == 0:
            return jsonify({"frequencies": []})

        # 7. Build an ordered list of frequency data, sorted by descending count
        frequency_data = [
            {
                "letter": letter,
                "count": counts[letter],
                "percent": round((counts[letter] / total) * 100, 2)
            }
            for letter in sorted(counts, key=counts.get, reverse=True)
        ]
        # 8. Return the list of {letter, count, percent} objects as JSON
        return jsonify({"frequencies": frequency_data})

    except Exception as e:
        # 9. On unexpected errors, report the exception message with HTTP 500
        return jsonify({"error": str(e)}), 500
    


# Auto detection 
@app.route("/detect-cipher-type", methods=["POST"])
def detect_cipher_route():
    try:
        # 1: Validate that the incoming request is JSON
        if not request.is_json:
            return jsonify({"suggestion": "Request must be JSON"}), 400

        # 2: Parse the JSON payload and pull out the ciphertext
        data = request.get_json()
        ciphertext = data.get("ciphertext", "")

        # 3: Ensure the ciphertext is a string
        if not isinstance(ciphertext, str):
            return jsonify({"suggestion": "Input must be text"}), 400

        # 4: Enforce a minimum length to make detection reliable
        if len(ciphertext.strip()) < 20:
            return jsonify({"suggestion": "Text too short (min 20 chars)"}), 400

        # 5: Invoke the detection logic
        result = detect_cipher_type(ciphertext)

        # 6: Check that the detector returned a valid dictionary
        if not result or not isinstance(result, dict):
            return jsonify({"suggestion": "Detection service error"}), 500

        # 7: Return the detector’s suggestion with a success status
        return jsonify({
            "suggestion": result.get("suggestion", "Unknown cipher type"),
            "status": "success"
        })

    except Exception as e:
        # 8: Log unexpected errors and inform the client
        app.logger.error(f"Cipher detection error: {str(e)}")
        return jsonify({
            "suggestion": "Detection service unavailable",
            "status": "error",
            "details": str(e)
        }), 500

  
# Dictionary match
@app.route("/dictionary-suggest", methods=["POST"])
def dictionary_suggest():
    # Parse JSON body to get the pattern, trimming whitespace
    data = request.get_json()
    pattern = data.get("pattern", "").strip()
    
    # If no pattern provided, return an error and empty match list
    if not pattern:
        return jsonify({"matches": [], "error": "Empty pattern provided."})

    # Load the full dictionary of words
    dictionary_words = load_dictionary()
    # Find all words matching the pattern
    matches = find_matches(pattern, dictionary_words)
    # Return up to 50 matches to keep response size reasonable
    return jsonify({"matches": matches[:50]})


if __name__ == "__main__":
    app.run(debug=True)

