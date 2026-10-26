#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2026 Albert Ganut
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
Problem 2
"""

from sys import flags

def keyScore(mapping: dict, ciphertext: str, frequencies: dict, n: int) -> float:

    deciphered_chars = [] # this holds the chars replaced using the mapping

    for char in ciphertext:

        deciphered_chars.append(mapping[char]) # finds the replacement char and then adds it to the list of deciphered chars

    deciphered_text = "".join(deciphered_chars)

    score = 0 # this is the score of the deciphered text based on the frequencies of n grams
    total_ngrams = len(deciphered_text) - n + 1

    for i in range(total_ngrams):

        ngram = deciphered_text[i:i + n]

        # if the current ngram is in the frequencies dict, then we add its frequency to the score
        if ngram in frequencies:
            score += frequencies[ngram]

    return float(score)
  

def test():
    "Run tests"

    mapping = {}
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

    for char in alphabet:
        mapping[char] = char

    # test 1
    frequencies = {"EE": 0.5, "EF": 0.2, "FE": 0.3}

    # line 77 written by Google Gemini
    score = keyScore(mapping, "EEFFFEEF", frequencies, 2)
    assert abs(score - 1.7) < 0.000000001
    print(f"Test 1 score: {score}")

    # test 2 --> with spaces
    frequencies = {
        "A ": 0.4,
        " B": 0.6
    }

    score = keyScore(mapping, "A B", frequencies, 2)
    assert abs(score - 1.0) < 0.000000001
    print(f"Test 2 score: {score}")

    # test 3 --> no ngrams
    frequencies = {"AB": 0.5}

    score = keyScore(mapping, "A", frequencies, 2)
    assert abs(score - 0.0) < 0.000000001
    print(f"Test 3 score: {score}")

    # lines 97-109 written by Google Gemini
    # test 4 --> check that the mapping actually replaces characters.
    # Swap A and E so that the mapping remains one-to-one.
    mapping["A"] = "E"
    mapping["E"] = "A"

    frequencies = {
        "EB": 0.7
    }

    score = keyScore(mapping, "AB", frequencies, 2)
    assert abs(score - 0.7) < 0.000000001
    print(f"Test 4 score: {score}")

    print("Problem 2 tests passed")

if __name__ == "__main__" and not flags.interactive:
    test()