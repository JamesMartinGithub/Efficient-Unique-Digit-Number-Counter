"""
Given a list of pairs of numbers, return the count of numbers
with unique digits between the pair of numbers (inclusive)
"""
import math
import re
import numpy as np


def countuniques(array: [[int]]) -> [int]:
    """
    Returns a list of counts of values between the given ranges that have all-unique digits (inclusive)
    Note: input array validity is not checked, for efficiency
    """
    result = []
    for i in range(0, len(array)):
        result.append(countunique(array[i]))
    return result


def countunique(rangev: [int]) -> int:
    """Returns the number of values between the given range that have all-unique digits (inclusive)"""
    count = 0
    a = rangev[0]  # Smallest value
    b = rangev[1]  # Largest value
    # Swap values if left value is larger
    if a > b:
        temp = b
        b = a
        a = temp
    # Cap at highest value with unique digits to avoid necessary computation
    if b >= 9876543210:
        if a <= 1000000000:
            b = 9999999999
        else:
            b = 9876543210
    # Split range into smaller, more easily processed ranges
    splits = split([[str(a), str(b)]], False)
    # Sum the count of numbers with unique values for each range in splits
    for i in range(0, len(splits)):
        ai = int(splits[i][0])
        bi = int(splits[i][1])
        sai = splits[i][0]
        sbi = splits[i][1]
        # 4 Cases:
        # Same numbers
        if a == b:
            if digitsUnique(a):
                count += 1
        # Range <10
        elif bi - ai < 10:
            for e in range(ai, bi+1):
                if digitsUnique(e):
                    count += 1
        # Zeros and Nines
        elif re.fullmatch("1(0+)", sai) and re.fullmatch("9+", sbi) and len(sai) == len(sbi):
            match (ai, bi):
                case (10, 99):
                    count += 81
                case (100, 999):
                    count += 648
                case (1000, 9999):
                    count += 4536
                case (10000, 99999):
                    count += 27216
                case (100000, 999999):
                    count += 136080
                case (1000000, 9999999):
                    count += 544320
                case (10000000, 99999999):
                    count += 1632960
                case (100000000, 999999999):
                    count += 3265920
                case (1000000000, 9999999999):
                    count += 3265921
        # Powers of ten
        elif ai%10 == 0 and bi%10 == 0 and len(sai) == len(sbi):
            # get number of zeros to right of first digit: z = which polynomial to use
            pos = len(sai) - 1
            counter = 0
            while True:
                if sai[pos] != '0' or sbi[pos] != '0':
                    break
                else:
                    counter += 1
                    pos -= 1
            z = counter
            # get length of number: l = related to n
            l = len(sai)
            # get number of clashes with range (2nd digit exclusive): c = reduces range for each clash
            firstDigit = int(sai[pos])
            secondDigit = int(sbi[pos])
            rnge = np.arange(firstDigit, secondDigit)
            c = 0
            for ds in range(0, pos):  # Left digits
                if rnge.__contains__(int(sai[ds])):
                    c += 1
            # Use polynomials* to get count; work out for range=1 then multiply to actual range
            # The polynomial coefficients are stirling numbers of the first kind, until case 8+
            # *This script uses pre-computation for efficiency, the coefficients are given in comments for each case
            multiplier = rnge.__len__() - c
            polyCount = 0
            leftDigits = l-z-1
            # Check first for repeat digits to left of first digit (from right)
            buffer = np.empty(0)
            for d in range(0, leftDigits):
                if buffer.__contains__(sai[d]):
                    multiplier = 0
                    break
                else:
                    buffer = np.append(buffer, sai[d])
            if multiplier != 0:
                # Match number of zeros on the right to get the precomputed polynomial value
                match(z):
                    case 1:  # 1
                        if leftDigits <= 7:
                            polyCount = (10 - leftDigits)
                        else:
                            polyCount = 0
                    case 2:  # 1 1
                        match (leftDigits):
                            case 0:
                                polyCount = 72
                            case 1:
                                polyCount = 56
                            case 2:
                                polyCount = 42
                            case 3:
                                polyCount = 30
                            case 4:
                                polyCount = 20
                            case 5:
                                polyCount = 12
                            case 6:
                                polyCount = 6
                            case 7:
                                polyCount = 2
                            case _:
                                polyCount = 0
                    case 3:  # 1 3 2
                        match (leftDigits):
                            case 0:
                                polyCount = 504
                            case 1:
                                polyCount = 336
                            case 2:
                                polyCount = 210
                            case 3:
                                polyCount = 120
                            case 4:
                                polyCount = 60
                            case 5:
                                polyCount = 24
                            case 6:
                                polyCount = 6
                            case _:
                                polyCount = 0
                    case 4:  # 1 6 11 6
                        match (leftDigits):
                            case 0:
                                polyCount = 3024
                            case 1:
                                polyCount = 1680
                            case 2:
                                polyCount = 840
                            case 3:
                                polyCount = 360
                            case 4:
                                polyCount = 120
                            case 5:
                                polyCount = 24
                            case _:
                                polyCount = 0
                    case 5:  # 1 10 35 50 24
                        match (leftDigits):
                            case 0:
                                polyCount = 15120
                            case 1:
                                polyCount = 6720
                            case 2:
                                polyCount = 2520
                            case 3:
                                polyCount = 720
                            case 4:
                                polyCount = 120
                            case _:
                                polyCount = 0
                    case 6:  # 1 15 85 225 274 120
                        match (leftDigits):
                            case 0:
                                polyCount = 60480
                            case 1:
                                polyCount = 20160
                            case 2:
                                polyCount = 5040
                            case 3:
                                polyCount = 720
                            case _:
                                polyCount = 0
                    case 7:  # 1 21 175 735 1624 1764 720
                        match (leftDigits):
                            case 0:
                                polyCount = 181440
                            case 1:
                                polyCount = 40320
                            case 2:
                                polyCount = 5040
                            case _:
                                polyCount = 0
                    case 8:  # 1 28 332 1930 6789 13132 13068 5040
                        match(leftDigits):
                            case 0:
                                polyCount = 362880
                            case 1:
                                polyCount = 40320
                            case _:
                                polyCount = 0
                    case 9:  # 1 33 526 4500 22400 67193 118224 109683 40320
                        polyCount = 362880
                    case _:
                        polyCount = 0
            polyCount *= multiplier
            if z == 1:
                if multiplier != 0:
                    # Subtract from count for every double-counted value
                    polyCount -= rnge.__len__() - 1 - c
                    if not digitsUnique(bi):
                        polyCount -= 1
                else:
                    # Check last value in range if not already considered
                    if digitsUnique(bi):
                        polyCount += 1
            # Add to the total count
            count += polyCount
        else:
            print("Error")
    return count


def split(array: [[str]], isLayered: bool) -> [[str]]:
    """
    Splits a range or list of ranges into smaller ranges that fit any of 4 categories for fast processing:
    1) Same numbers  2) Range <10  3) Zeros and Nines  4) Powers of ten
    """
    # If multiple ranges are provided, recurse; split each range separately then join
    if len(array) > 1:
        tempArray = array.copy()
        tempArray.remove(array[0])
        return split([array[0]], isLayered) + split(tempArray, isLayered)
    # Setup local variables
    a = int(array[0][0])
    b = int(array[0][1])
    sa = array[0][0]
    sb = array[0][1]
    # Check if splitting is needed
    if (((b-a) < 10) or ((len(sa) == len(sb)) and (a%10) == 0 and (b%10) == 0 and isTens(sa,sb))
            or (not isLayered and (re.fullmatch("1(0+)", sa) and re.fullmatch("9+", sb) and len(sa) == len(sb)))):
        return array
    # Choose how to split
    if len(sa) == len(sb):
        # Numbers are the same length
        if sa[0] != sb[0]:
            # Numbers start with different digits
            # Calculate a middle value and split into two ranges about that value
            if (a%10) == 0 and (b%10) != 0:
                middle2 = int((int(sb[0])) * math.pow(10, len(sb)-1))
                return split([[sa, str(middle2)], [str(min(middle2+1, b)), sb]], isLayered)
            elif (a%10) != 0 and (b%10) == 0:
                middle1 = int((int(sa[0])+1) * math.pow(10, len(sa)-1))
                return split([[sa, pad(str(middle1-1),len(sa))], [str(middle1), sb]], isLayered)
            elif (a%10) != 0 and (b%10) != 0:
                middle1 = int((int(sa[0]) + 1) * math.pow(10, len(sa)-1))
                middle2 = int((int(sb[0])) * math.pow(10, len(sb)-1))
                return split([[sa, pad(str((middle1-1)),len(sa))], [str(middle1), str(middle2)], [str(min(middle2 + 1, b)), sb]], isLayered)
            else:
                # Both numbers are multiples of 10, first check if the first number's first digit is 0
                if sa[0] == '0' and a != 0:
                    # Left number starts with 0, range can be split with multiple of 10 jump
                    # get index of first non-zero
                    nonZeroIndex = 0
                    while True:
                        if sa[nonZeroIndex] != '0':
                            break
                        else:
                            nonZeroIndex += 1
                    middle = int(math.pow(10, len(sa)-nonZeroIndex))
                    return split([[sa, pad(str(middle-1),len(sa))], [str(middle), sb]], isLayered)
                else:
                    # Left number digit not 0, check if left number is power of 10 instead
                    if a == 0 or re.fullmatch("[1-9](0*)0$", sa):
                        # Range can be split nicely with multiple of 10
                        middle = str(int(int(sb[0]) * math.pow(10, len(sb) - 1)))
                        return [[sa, middle]] + split([[middle, sb]], isLayered)
                    else:
                        # Range has to be split to next order of magnitude of first digit (from right)
                        # get index of first non-zero from right
                        nonZeroIndex = len(sa) - 1
                        while True:
                            if sa[nonZeroIndex] != '0':
                                nonZeroVal = int(sa[nonZeroIndex])
                                nonZeroIndex -= 1
                                break
                            else:
                                nonZeroIndex -= 1
                        middle = int(a + math.pow(10, len(sa) - nonZeroIndex - 1) - (nonZeroVal * math.pow(10, len(sa) - nonZeroIndex - 2)))
                        return split([[sa, str(middle-1)], [str(middle), sb]], isLayered)
        else:
            # Numbers start with the same digits
            # Go 1 layer deeper; repeat the split with the first digit removed from each number
            difference = int((int(sa[0])) * math.pow(10, len(sa) - 1))
            nparray = np.array(split([[sa[1:len(sa)], sb[1:len(sb)]]], True)).astype(dtype=int) + difference
            return nparray.astype(dtype=str).tolist()
    else:
        # Numbers are different lengths
        # Split the range such that the difference in length is reduced by 1
        middle = int(math.pow(10, len(sa)))
        return split([[sa, str(middle-1)], [str(middle), sb]], isLayered)


def isTens(sa: str, sb: str) -> bool:
    """Returns true if the values form a range that can be processed in the 'Power of ten' category"""
    pos = len(sa) - 1
    while True:
        if sa[pos] == '0' and sb[pos] == '0':
            pos -= 1
        elif sa[pos] != '0' and sb[pos] != '0' and (pos == 0 or int(sa[0:pos]) == int(int(sb[0:pos]))):
            return True
        else:
            if sa[pos] == '0' and pos == 0:
                return True
            break
    return False


def pad(s: str, l: int) -> str:
    """Pads s with zeros on the left to reach length l"""
    diff = l - len(s)
    for i in range (0, diff):
        s = "0" + s
    return s


def digitsUnique(number: int) -> bool:
    """Returns true if number contains only unique digits"""
    digits = []
    string = str(number)
    valid = True
    for a in range(0, len(string)):
        if (string[a]) in digits:
            valid = False
            break
        else:
            digits.append(string[a])
    if valid:
        return True
    else:
        return False
