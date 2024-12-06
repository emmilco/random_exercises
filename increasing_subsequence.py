# Given an array of numbers, find the length of the longest
# increasing subsequence in the array. The subsequence does
# not necessarily have to be contiguous.

# For example, given the array
# [0, 80, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15],
# the longest increasing subsequence has length 6:
# it is 0, 2, 6, 9, 11, 15.


# naive solution
# generate all the subsequences
# this is O(2^n) space complexity or whatever

# what is an increasing subsequence?
# an ordered subset of the array, where for every nth element, arr[n] < arr[n+1]

# find every valid subsequence
# take the longest one


# Imagine building a list of trees, appending a number to each only if it meets the validity criterion.
# 0, 80, 4, 12

# 0 -> 80
# 80 -> nothing
# 0 -> [80], [4]
# 4 -> 12
# 0 -> 4 -> 12

inputs = [0, 80, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15, 0, 80, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]

def find_longest_non_contiguous_subsequence(inputs):
    valid_subsequences = []
    # where elements of valid_subsequences are tuples of the form [length, last_element]
    for n in inputs:
        for sub in valid_subsequences:
            length, last_element = sub
            if n > last_element:
                new_subsequence = (length + 1, n)
                valid_subsequences.append(new_subsequence)
        valid_subsequences.append([1, n])

    longest = 0
    for subsequence in valid_subsequences:
        if subsequence[0] > longest:
            longest = subsequence[0]

    print(f"NUM SUBSEQUENCES: {len(valid_subsequences)}")

    return longest

find_longest_non_contiguous_subsequence(inputs)
