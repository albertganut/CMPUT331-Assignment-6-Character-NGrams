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
Problem 1
"""

from sys import flags

def ngramsFreqs(text: str, n: int) -> dict:
    """
    text: the content string
    n: the size of the n-grams
    """

    ngrams_frequencies = {} # this dictionary will hold the n-grams and their frequencies as key-value pairs

    total_ngrams = len(text) - n + 1 # len(text) gives the number of chars in the text, and we subtract n-1 to get the number of n-grams

    # we return the dictionary if there are no n-grams or if the text is too short to form any n-grams
    # ex: "A" with n = 2 has no 2-grams, so we return an empty dictionary
    if n <= 0 or total_ngrams <= 0:

        return ngrams_frequencies

    for i in range(total_ngrams):

        # uses list slicing to get the specific n-gram from thet text
        # ex: "ABAB" with n = 2 will start at index 0 and get "AB", then start at index 1 and get "BA", then start at index 2 and get "AB"
        # the right side of the colon is exclusive, so it won't count the character at that exact index
        ngram = text[i:i + n]

        # if the n-gram already exists in the dictionary, then we just increase the count by 1
        # if it doesn't exist, then we add it to the dictionary
        if ngram in ngrams_frequencies:
            ngrams_frequencies[ngram] += 1

        else:
            ngrams_frequencies[ngram] = 1

    # goes through all the n-grams in the dictionary and divides their counts by the total number of n-grams to get their frequencies as a percentage
    for ngram in ngrams_frequencies:

        ngrams_frequencies[ngram] /= total_ngrams   

    return ngrams_frequencies
    

def test():
    "Run tests"

    assert ngramsFreqs("ABABA", 2) == {"AB": 0.5, "BA": 0.5}
    assert ngramsFreqs("abcde", 2) == {'ab': 0.25, 'bc': 0.25, 'cd': 0.25, 'de': 0.25}
    assert ngramsFreqs("abcde", 3) == {'abc':  1 / 3, 'bcd': 1 / 3, 'cde': 1 / 3}

    # lines 86-107 from Google Gemini
    assert ngramsFreqs("AAAA", 2) == {
        "AA": 1.0
    }

    assert ngramsFreqs("A B", 2) == {
        "A ": 0.5,
        " B": 0.5
    }

    assert ngramsFreqs("AAB", 1) == {
        "A": 2 / 3,
        "B": 1 / 3
    }

    assert ngramsFreqs("ABC", 3) == {
        "ABC": 1.0
    }

    assert ngramsFreqs("", 2) == {}
    assert ngramsFreqs("A", 2) == {}

    print("Problem 1 tests passed")

if __name__ == "__main__" and not flags.interactive:
    test()
