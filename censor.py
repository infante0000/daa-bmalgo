from tkinter import messagebox
import pandas as pd

NO_OF_CHARS = 256
list_index = []


def bad_char_heuristic(string, size):
    # Initialize all occurrence as -1
    bad_char = [-1] * NO_OF_CHARS

    # Fill the actual value of last occurrence
    for i in range(size):
        bad_char[ord(string[i])] = i

    # return initialized list
    return bad_char


def boyer_moore_match(text, pattern):
    # find the occurence of the patter in text
    m = len(pattern)
    n = len(text)

    bad_char = bad_char_heuristic(pattern, m)

    # s is shift of the pattern with respect to text
    s = 0
    while s <= n - m:
        j = m - 1

        # Keep reducing index j of pattern while
        # characters of pattern and text are matching
        # at this shift s
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        # If the pattern is present at current shift,
        # then index j will become -1 after the above loop
        if j < 0:
            occurrence(s)
            s += (m - bad_char[ord(text[s + m])] if s + m < n else 1)

        else:
            s += max(1, j - bad_char[ord(text[s + j])])


# store index of matched string
def occurrence(index):
    indexes = [index]
    list_index.append(indexes)


def censorFile(txt):
    # get the text

    # open list of words
    df = pd.read_excel('swear_words.xlsx', 'Sheet1')
    swear_words = df['swear_words_list'].values.tolist()

    # looping of censoring
    for word_list in swear_words:
        pattern = word_list
        boyer_moore_match(txt, pattern)

        print("\nPattern: " + pattern)
        print("List of Index: ")
        print(*list_index)
        for i in list_index:
            print("Replacing at Index: " + str(i)[1:-1])
            currIndex = int(str(i)[1:-1])
            censored_text = txt[:currIndex] + "*" * len(pattern) + txt[currIndex + len(pattern):]
            txt = censored_text
            print(txt)
        list_index.clear()

    return txt
