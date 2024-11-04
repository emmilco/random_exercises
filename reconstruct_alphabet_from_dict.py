# You come across a dictionary of sorted words in a language you've never seen before. Write a program that returns the correct order of letters in this language.

# For example, given

# ['xww', 'wxyz', 'wxyw', 'ywx', 'ywz'],

#  you should return ['x', 'z', 'w', 'y'].


# x < w

# x < z < w < y


# iterate through the list considering item at index i and i+1
# ignore the initial shared letters between the two words
# the first non-shared letter gives us ordering information
# what do we do with it?


# [x, w]
# [z, w]
# [w, y]
# [x, z]

# Given a set of ordered pairs, construct a total ordering of the set from which the elements in the pairs are taken.


# take the list of elements
# swap elements within the list in order to make each partial ordering true

# S = [w,x,y,z]

# apply x < w
# index of x = 1
# index of w = 0
# swap x and w

# S = [x,w,y,z]

# apply z < w
# index of z = 3
# index of w = 1
# swap z and w

# S = [x,z,y,w]

# apply w < y
# index of w = 3
# index of y = 2
# swap w and y

# S = [x,z,w,y]

# apply x < z
# index of z = 1
# index of x = 0
# continue

# S = [x,z,w,y]

# after iterating over the rules completely,
# if you have made a change during this loop,
# iterate over them again

# apply x < w
# continue
# ...
# no change

# meaning the sequence in S respects all the partial orderings.

# DONE


word_list = ["xww", "wxyz", "wxyw", "ywx", "ywz"]


def extract_partial_orderings(word_list):
    ordered_pairs = list()

    for idx, word in enumerate(word_list):
        if idx == len(word_list) - 1:
            continue
        next_word = word_list[idx + 1]

        letter_idx = 0
        while True:
            if letter_idx >= len(next_word) or letter_idx >= len(word):
                break
            if word[letter_idx] == next_word[letter_idx]:
                letter_idx += 1
            else:
                ordered_pairs.append([word[letter_idx], next_word[letter_idx]])
                break
    print(ordered_pairs)
    return ordered_pairs


def get_sorted_alphabet(word_list):
    alphabet = list(set("".join(word_list)))

    orderings = extract_partial_orderings(word_list)

    changes_made = True
    while changes_made:
        changes_made = False

        for pair in orderings:
            lesser, greater = pair
            lesser_idx = alphabet.index(lesser)
            greater_idx = alphabet.index(greater)
            if lesser_idx > greater_idx:
                alphabet[lesser_idx] = greater
                alphabet[greater_idx] = lesser
                changes_made = True

    return alphabet


print(get_sorted_alphabet(word_list))
