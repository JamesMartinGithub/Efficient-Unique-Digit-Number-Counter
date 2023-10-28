"""
Given a list of pairs of numbers, return the count of numbers
with unique digits between the pair of numbers (inclusive)
"""
import math


def countUnique(arr):
    results = []
    for i in range(0, len(arr)):
        a = arr[i][0]
        b = arr[i][1]
        count = 0
        for e in range(a, b+1):
            digits = []
            string = str(e)
            valid = True
            for a in range(0, len(string)):
                if (string[a]) in digits:
                    valid = False
                    break
                else:
                    digits.append(string[a])
            if valid:
                count += 1
        results.append(count)
    return results
