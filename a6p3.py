#!/usr/bin/env python3

# ---------------------------------------------------------------
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
# ---------------------------------------------------------------

"""
Problem 3
"""

from sys import flags
from itertools import combinations 
import a6p2 
from string import ascii_uppercase as upper_alpha


'''
Use this section to import your code from A6P2 
-- Make sure to import the entire module, sometimes using import from your own files can cause issues in the grading script


def keyScore(mapping: dict, ciphertext: str, frequencies: dict, n: int) -> float:
    raise NotImplementedError()
'''



def bestSuccessor(mapping: dict, ciphertext: str, frequencies: dict, n: int) -> dict:

    original_score = a6p2.keyScore(mapping, ciphertext, frequencies, n) # uses keyScore from a6p2.py to get the score of the originl mapping as a baseline

    # at first, we say that the best mapping is the original mapping and the best score is the original score.
    # these will be updated if we find better ones
    best_mapping = mapping
    best_score = original_score

    # using combinations() instead of permutations() so that we only generate each letter pairs once
    # ex: AB and BA are considered the same, combinations() only generates AB
    for letter_1, letter_2 in combinations(upper_alpha, 2):

        swapped_mapping = mapping.copy()

        swapped_mapping[letter_1], swapped_mapping[letter_2] = swapped_mapping[letter_2], swapped_mapping[letter_1] # swap values

        new_score = a6p2.keyScore(swapped_mapping, ciphertext, frequencies, n)

        # if the score after swapping is better than the current best score, then we update the best score and the best mapping to the new ones
        if new_score > best_score:
            best_score = new_score
            best_mapping = swapped_mapping
        # lines 81-82 written by Google Gemini
        # if the score after swapping is the same and the new score is better than the original, then we perform a tie breaker where the letter that alphabetically comes first is chosen
        # if the score after the swap is the same but it's not better than the original, then nothign happens
        elif new_score == best_score:
            if new_score > original_score:
                best_mapping = breakKeyScoreTie(mapping, best_mapping, swapped_mapping)

    return best_mapping


def breakKeyScoreTie(originalMapping, successorMappingA, successorMappingB):
    """
    Break the tie between two successor mappings that have the same keyscore

    originalMapping: mapping the the other parameters are successors to
    successorMappingA: mapping that has had two keys swapped
    successorMappingB: mapping that has had two other keys swapped

    Example usage:
    originalMapping = {"A": "A", "B": "B", "C": "C"}
    # Mapping with B and C switched
    successorMappingA = {"A": "A", "B": "C", "C": "B"}
    # Mapping with A and C switched
    successorMappingB = {"A": "C", "B": "B", "C": "A"}

    # AC < BC so this function will return successorMappingB
    assert breakKeyScoreTie(originalMapping, successorMappingA, successorMappingB) == successorMappingB
    """
    aSwapped = "".join(sorted(k for k, v in (
        set(successorMappingA.items()) - set(originalMapping.items()))))
    bSwapped = "".join(sorted(k for k, v in (
        set(successorMappingB.items()) - set(originalMapping.items()))))
    return successorMappingA if aSwapped < bSwapped else successorMappingB

def test():
    "Run tests"

    mapping = {}

    for letter in upper_alpha + " ":

        mapping[letter] = letter

    original_mapping = mapping.copy()   

    assert breakKeyScoreTie({"A": "A", "B": "B", "C": "C"}, {"A": "A", "B": "C", "C": "B"}, {
                            "A": "C", "B": "B", "C": "A"}) == {"A": "C", "B": "B", "C": "A"}
    assert breakKeyScoreTie({"A": "A", "B": "B", "C": "C", "D": "D"}, {
                            "A": "B", "B": "A", "C": "C", "D": "D"}, {"A": "A", "B": "B", "C": "D", "D": "C"}) == {"A": "B", "B": "A", "C": "C", "D": "D"}

    # test 1 --> normal swapping
    frequencies = {"AB": 0.2, "CB": 0.8}

    expected_mapping = mapping.copy()
    expected_mapping["A"], expected_mapping["C"] = expected_mapping["C"], expected_mapping["A"]

    result = bestSuccessor(mapping, "AB", frequencies, 2)

    assert result == expected_mapping, "Test 1: Expected A and C to swap"
    assert mapping == original_mapping, "Test 1: Input mapping was changed"

    print("Test 1 passed")

    # test 2 --> swapping with tie
    frequencies = {"CB": 0.5, "DB": 0.5}

    expected_mapping = mapping.copy()
    expected_mapping["A"], expected_mapping["C"] = expected_mapping["C"], expected_mapping["A"]

    result = bestSuccessor(mapping, "AB", frequencies, 2)

    assert result == expected_mapping, "Test 2: Expected A/C to win the tie"
    assert mapping == original_mapping, "Test 2: Input mapping was changed"

    print("Test 2 passed")

    # lines 153-223 written by Google Gemini
    # Test 3: Keep the original when a successor ties its score.
    # Original "AB" and swapped "CB" both score 0.5.
    frequencies = {"AB": 0.5, "CB": 0.5}

    expected_mapping = mapping.copy()

    result = bestSuccessor(mapping, "AB", frequencies, 2)

    assert result == expected_mapping, "Test 3: Should keep original mapping"
    assert mapping == original_mapping, "Test 3: Input mapping was changed"

    print("Test 3 passed")

    # Test 4: Break a tie between two improving successors.
    # A/C and A/D both score 0.5, beating the original score of 0.
    # The tie-breaker should choose A/C.
    frequencies = {"CB": 0.5, "DB": 0.5}

    expected_mapping = mapping.copy()
    expected_mapping["A"] = "C"
    expected_mapping["C"] = "A"

    result = bestSuccessor(mapping, "AB", frequencies, 2)

    assert result == expected_mapping, "Test 4: Incorrect tie-breaking"
    assert mapping == original_mapping, "Test 4: Input mapping was changed"

    print("Test 4 passed")

    # Test 5: Handle spaces and trigrams.
    # Swapping A/C changes "A B" into "C B", scoring 1.0.
    frequencies = {"C B": 1.0}

    expected_mapping = mapping.copy()
    expected_mapping["A"] = "C"
    expected_mapping["C"] = "A"

    result = bestSuccessor(mapping, "A B", frequencies, 3)

    assert result == expected_mapping, "Test 5: Wrong trigram successor"
    assert result[" "] == " ", "Test 5: Space must map to itself"
    assert mapping == original_mapping, "Test 5: Input mapping was changed"

    print("Test 5 passed")

    # Test 6: No complete n-grams because the text is shorter than n.
    # Every mapping scores 0, so keep the original.
    frequencies = {"AB": 1.0}

    expected_mapping = mapping.copy()

    result = bestSuccessor(mapping, "A", frequencies, 2)

    assert result == expected_mapping, "Test 6: Should keep original mapping"
    assert mapping == original_mapping, "Test 6: Input mapping was changed"

    print("Test 6 passed")

    # Test 7: No n-grams match the frequency dictionary.
    # No swap can turn "AB" into "ZZ", so every score is 0.
    frequencies = {"ZZ": 1.0}

    expected_mapping = mapping.copy()

    result = bestSuccessor(mapping, "AB", frequencies, 2)

    assert result == expected_mapping, "Test 7: Should keep original mapping"
    assert mapping == original_mapping, "Test 7: Input mapping was changed"

    print("Test 7 passed")

    print("Problem 3 tests passed")
if __name__ == "__main__" and not flags.interactive:
    test()