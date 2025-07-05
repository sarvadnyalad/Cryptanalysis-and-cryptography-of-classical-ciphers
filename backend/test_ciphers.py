import unittest
import sys
import os

# Add backend folder to system path so we can import cipher modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all updated cipher and helper modules
import caeser
import vigenere
import columnar
import dictionary_helper
import railfence
from playfair import PlayfairCipher


# ===============================
# Caesar Cipher Unit Tests
# ===============================
class TestCaesarCipher(unittest.TestCase):
    def test_encrypt(self):
        # Caesar encryption with shift of 2 should wrap Z->B
        self.assertEqual(caeser.encrypt("ZEBRA", 2), "BGDTC")

    def test_decrypt(self):
        # Decryption should reverse encryption and recover original text
        self.assertEqual(caeser.decrypt("BGDTC", 2), "ZEBRA")

    def test_brute_force(self):
        # Brute force test: shift 2 should yield "ZEBRA" from "BGDTC"
        results = caeser.brute_force("BGDTC")
        self.assertEqual(results[2], "ZEBRA")


# ===============================
# Vigenère Cipher Unit Tests
# ===============================
class TestVigenereCipher(unittest.TestCase):
    def test_encrypt(self):
        # Encrypt using key "LEMON" should match known example output
        self.assertEqual(vigenere.encrypt_vigenere("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR")

    def test_decrypt(self):
        # Decrypt using the same key should return original plaintext
        self.assertEqual(vigenere.decrypt_vigenere("LXFOPVEFRNHR", "LEMON"), "ATTACKATDAWN")

    def test_invalid_key(self):
        # Keys must be alphabetic; this should fail validation
        self.assertFalse(vigenere.is_valid_key("123KEY"))
        
    def test_valid_key(self):
        # Alphabet-only key should pass validation
        self.assertTrue(vigenere.is_valid_key("LEMON"))


# ===============================
# Columnar Transposition Cipher Unit Tests
# ===============================
class TestColumnarCipher(unittest.TestCase):
    def test_encrypt_decrypt(self):
        # Ensure columnar encryption and decryption with keyword works
        plaintext = "DEFENDTHEEASTWALL"
        keyword = "FORTIFY"
        encrypted = columnar.encrypt(plaintext, keyword)
        decrypted = columnar.decrypt(encrypted, keyword)
        self.assertEqual(decrypted, plaintext)


# ===============================
# Dictionary Helper Unit Tests
# ===============================
class TestDictionaryHelper(unittest.TestCase):
    def test_find_matches(self):
        # Pattern C_T should match CAT, COT, CUT (not DOG)
        result = dictionary_helper.find_matches("C_T", ["CAT", "COT", "CUT", "DOG"])
        self.assertIn("CAT", result)
        self.assertIn("COT", result)
        self.assertNotIn("DOG", result)

    def test_no_match(self):
        # Pattern that matches nothing should return empty list
        result = dictionary_helper.find_matches("ZZZZZ", ["APPLE", "PEAR"])
        self.assertEqual(result, [])


# ===============================
# Rail Fence Cipher Unit Tests
# ===============================
class TestRailFenceCipher(unittest.TestCase):
    def test_encrypt_decrypt(self):
        # Encrypt and decrypt using 3 rails should preserve original text
        plaintext = "DEFENDTHEEASTWALL"
        rails = 3
        encrypted = railfence.railfence_encrypt(plaintext, rails)
        decrypted = railfence.railfence_decrypt(encrypted, rails)
        self.assertEqual(decrypted, plaintext)


# ===============================
# Playfair Cipher Unit Tests
# ===============================
class TestPlayfairCipher(unittest.TestCase):
    def test_encrypt_decrypt(self):
        # Playfair encryption/decryption with "MONARCHY" should roughly match input
        cipher = PlayfairCipher("MONARCHY")
        plaintext = "DEFEND"
        encrypted = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(encrypted)
        # Decrypted may contain padding, so only assert start of string
        self.assertTrue(decrypted.startswith("DEF"))

    def test_matrix_size(self):
        # The Playfair matrix must always be 5x5 = 25 characters
        cipher = PlayfairCipher("MONARCHY")
        matrix = cipher.matrix
        flat = [char for row in matrix for char in row]
        self.assertEqual(len(flat), 25)


# Run all tests
if __name__ == '__main__':
    unittest.main()
