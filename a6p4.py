#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2026 <<Insert your name here>>
#
# Redistribution is forbidden in all circumstances. Use of this software
# without explicit authorization from the author is prohibited.
#
# This software was produced as a solution for an assignment in the course
# CMPUT 331 - Computational Cryptography at the University of
# Alberta, Canada. This solution is confidential and remains confidential 
# after it is submitted for grading.
#
# Copying any part of this solution without including this copyright notice
# is illegal.
#
# If any portion of this software is included in a solution submitted for
# grading at an educational institution, the submitter will be subject to
# the sanctions for plagiarism at that institution.
#
# If this software is found in any public website or public repository, the
# person finding it is kindly requested to immediately report, including 
# the URL or other repository locating information, to the following email
# address:
#
#          gkondrak <at> ualberta.ca
#
#---------------------------------------------------------------

"""
Problem 4
"""

from sys import flags
import a6p1, a6p2, a6p3
from string import ascii_uppercase as upper_alpha


ETAOIN = "ETAOINSHRDLCUMWFGYPBVKJXQZ"   # This is the true English letter frequency

def readCipherText(filename): 
    """
    Reads a text file and then returns its contents
    """

    with open(filename, "r") as file:
        contents = file.read()

    return contents

def makeOriginalMapping(ciphertext):
    """
    Creates the starting mapping based on letter frequency from the ciphertext
    """

    letter_counts = {} # this dict will store the letter (as a key) and its count in the ciphertext (as a value)

    for letter in upper_alpha:

        letter_counts[letter] = 0 # adds the current letter to the dict with a count of 0

    for char in ciphertext:

        # if the char already exists in the dict, then we just increase its count by 1
        # we don't care about the characters that are not in the dict
        if char in letter_counts:
            letter_counts[char] += 1

    sorted_letters = sorted(letter_counts, key = letter_counts.get, reverse = True) # sorts the letters by decreasing frequency

    c2p_mapping = {} # maps each ciphertext letter to its guessed plaintext letter

    for i in range(len(upper_alpha)):

        # we get the ciphertext and plaintext letters at the current index 
        ciphertext_letter = sorted_letters[i]
        plaintext_letter = ETAOIN[i]

        c2p_mapping[ciphertext_letter] = plaintext_letter # adds the mapping from the ciphertext letter to the plaintext letter 
    # written by Google Gemini
    c2p_mapping[" "] = " " # needed to keep spaces unchanged and because the loop only handled letters

    return c2p_mapping

def decipherText(ciphertext, mapping):
    """
    Deciphers the ciphertext using the provided mapping
    """

    deciphered_chars = [] # holds the plaintext replacements in their original order

    for char in ciphertext:

        # uses the mapping dict to get the plaintext replacement for each ciphertext char 
        # then adds it to the deciphered chars list
        replacement_char = mapping[char]
        deciphered_chars.append(replacement_char)

    deciphered_text = "".join(deciphered_chars)

    return deciphered_text

def breakSub(cipherFile: str, textFile: str) -> None:
    """
    Inputs:
        cipherFile:
            'text_finnegan_cipher.txt' for testing
            'text_cipher.txt' for submission
            Path to the ciphertext file.

        textFile:
            'wells.txt'
            Path to the English reference text file.

    Outputs:
        Save deciphered text to the address 'text_plain.txt'
    """
    n = 4  # changed this to 4 because Bhavya, on Discord, said to change it

    ciphertext = readCipherText(cipherFile) # reads the ciphertext from the provided file
    reference_text = readCipherText(textFile) # reads the English reference text from the provided file
    mapping = makeOriginalMapping(ciphertext) # creates the initial mapping based on the letter frequency of the ciphertext
    frequencies = a6p1.ngramsFreqs(reference_text, n) # calculates the n-gram frequencies of the reference text

    # we keep improving the mapping there's no more two-letter swap that increases the n-gram score
    while True:

        new_mapping = a6p3.bestSuccessor(mapping, ciphertext, frequencies, n)

        # stop if we get the same mapping
        if new_mapping == mapping:
            break

        mapping = new_mapping

    plaintext = decipherText(ciphertext, mapping)

    # opens the file in write mode and writes the deciphered text to it
    with open("text_plain.txt", "w") as file:
        file.write(plaintext)





'''
Use this section to import your code from A6P1, A6P2, A6P3
-- Make sure to import the entire module, sometimes using import from your own files can cause issues in the grading script

'''
        
def test():
    """Generate and check the provided test decipherment."""

    # lines 160-168 written by Google Gemini
    # Run the provided test ciphertext.
    breakSub("text_finnegan_cipher.txt", "wells.txt")

    actual_plaintext = readCipherText("text_plain.txt")
    expected_plaintext = readCipherText("text_finnegan_plain.txt")

    if actual_plaintext == expected_plaintext:
        print("Finnegan output matches the reference.")
    else:
        print("Finnegan output does not match with the current n value.")

    breakSub("text_cipher.txt", "wells.txt")
    print("Main decipherment saved to text_plain.txt")

if __name__ == "__main__" and not flags.interactive:
    test()