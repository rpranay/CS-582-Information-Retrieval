import os
import re
from nltk.stem.porter import *


path = os.getcwd() + "/citeseer"
all_words_dict = {}
optimized_words_dict = {}


def load_stop_words():
    f = open("stopwords.txt", "r")
    temp = []
    for x in f.readlines():
        temp.append(x.strip())
    return temp


def remove_special_characters(x):
    y = re.sub('\W+', '', x)
    return y


def find_words(fname):
    # print(fname)
    file = open(path + "/" + fname, "r")
    txt = file.read()
    unformatted_tokens = txt.lower().split()
    tokens = [remove_special_characters(x) for x in unformatted_tokens]
    stop_words = load_stop_words()
    temp_tokens = [x for x in tokens if not x in set(stop_words)]
    stemmer = PorterStemmer()
    optimized_tokens = [stemmer.stem(word) for word in temp_tokens]
    for x in tokens:
        if len(x) >= 1:
            # print(x)
            try:
                all_words_dict[x] += 1
            except KeyError:
                all_words_dict[x] = 1

    for x in optimized_tokens:
        if len(x) >= 1:
            try:
                optimized_words_dict[x] += 1
            except KeyError:
                optimized_words_dict[x] = 1


def find_stats(word_list):
    sum = 0
    unique_count = 0
    top_20_list = []
    counter = 20
    sw = []
    unique_words = 0

    for key, value in sorted(word_list.items(), key=lambda x: x[1], reverse=True):
        sum += value
        unique_count += 1
        if counter > 0:
            top_20_list.append(key)
        counter -= 1

    temp_sum = 0
    for key, value in sorted(word_list.items(), key=lambda x: x[1], reverse=True):
        if temp_sum/sum >= 0.15:
            break
        temp_sum += value
        unique_words += 1

    print("(2a) Total no. of Words: ", sum)
    print("(2b) Total vocabulary size: ", unique_count)
    stop_words = load_stop_words()
    print("(2c) Top 20 words")
    for idx, x in enumerate(top_20_list):
       print(str(idx+1) + ". " + x)
       if x in stop_words:
            sw.append(x)

    print("(2d) Stop words from the top 20 words:")
    for x in sw:
        print(x)
    print("(2e) " + str(unique_words) + " words account for 15% or more of the total number of words in the collection")


for filename in os.listdir(path + "/"):
    find_words(filename)
find_stats(all_words_dict)
print("-------------------------------------------------------------------------------------------")
print("Stats after removing stop words and applying Porter stemmer algorithm")
find_stats(optimized_words_dict)
