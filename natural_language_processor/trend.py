from word_functions import *
from Text_with_topk import *
import math
import matplotlib.pyplot as plt


class Wordtrends:
    words_dict = generate_ngram_dictonary('1_pos_n_cs_n.txt')
    dcds = ['1810', '1820', '1830', '1840', '1850', '1860', '1870', '1880',
            '1890', '1900', '1910', '1920', '1930', '1940', '1950', '1960', '1970', '1980']

    def __init__(self, word, year):
        assert word in self.words_dict.keys(), "Word " + str(word) + " was not found in ngram database"
        self.word = word.lower()
        self.year = year
        codenumber, sample_size = year_to_decade_code(year)
        # Find frequency in a given decade, 0 if word is not used in decade
        if codenumber in self.words_dict[self.word]:
            frequency = int(self.words_dict[word][codenumber])
        else:
            frequency = 0
        self.frequency = frequency
        self.proportion = frequency / (int(sample_size))

    def print_ngram(self):
        """Print all the characteristics of the class"""
        return print([self.word, self.year, self.codenumber, self.frequency, self.proportion])

    def popularity_over_time(self):
        """Find the proportion of a word for each decade in the dataset"""
        word_timeline = []
        for item in self.dcds:
            word_and_year = Wordtrends(self.word, item)
            word_timeline.append(word_and_year.proportion)
        return word_timeline


def popularity_over_all_time(title, word_list, release_year, texter, k=5):
    """Find how popular a word is in each decade in the ngrams dataset"""
    # Use k most popular words if list is not provided, use k_most popular words
    if word_list == 0:
        word_list_k = []
        freq_text = texter.wordcount_sankey(k=k)[0]
        for word in freq_text[title]:
            word_list_k.append(word[0])
    else:
        word_list_k = word_list
    word_list_final = []
    data = []
    # If list is found, find the popularity over time for the words given
    for i in word_list_k:
        if i in Wordtrends.words_dict and i not in word_list_final:
            word_list_final.append(i)
    for i in word_list_final:
        word = Wordtrends(i, release_year)
        data.append(word.popularity_over_time())
    return word_list_final, data


def popularity_over_all_texts(word_list, release_year, texter, k=5):
    """Find how popular a word is in each decade in the ngrams dataset"""
    # Use k most popular words if list is not provided, use k_most popular words
    word_list_final = []
    data = []

    if word_list == 0:
        word_list_k = []
        freq_text = texter.wordcount_sankey(k=k)[0]
        for title in freq_text.keys():
            for i in range(k):
                print(freq_text[title][i][0])
                word_list_k.append(freq_text[title][i][0])
    else:
        word_list_k = word_list
    # If list is found, find the popularity over time for the words given
    for i in word_list_k:
        if i in Wordtrends.words_dict and i not in word_list_final:
            word_list_final.append(i)
    for i in word_list_final:
        word = Wordtrends(i, release_year)
        data.append(word.popularity_over_time())
    return word_list_final, data


def plot_one_text_timeline(title, word_list, release_year, texter, k=5):
    word_list_final, data = popularity_over_all_time(title, word_list, release_year, texter, k=k)
    plt.plot(figsize=(20, 5))
    # Plot each word in a line graph
    for i in range(len(data)):
        plt.plot(Wordtrends.dcds, data[i], label=word_list_final[i])
    plt.xlabel("Decades")
    plt.ylabel("Popularity")
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.show()


def plot_all_text_timeline(word_list, release_year, texter, k=5):
    word_list_final, data = popularity_over_all_texts(word_list, release_year, texter, k=k)
    plt.plot(figsize=(20, 5))
    # Plot each word in a line graph
    for i in range(len(data)):
        plt.plot(Wordtrends.dcds, data[i], label=word_list_final[i])
    plt.xlabel("Decades")
    plt.ylabel("Popularity")
    if word_list:
        plt.title("Popularity of Given Words Over Time")
    else:
        plt.title("Popularity of the " + str(k) + " Most Common Words In Each Text Over Time")
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()


def popularity_over_time_subplots(word_list, release_year, texter, k=5):
    # Set up lists
    words_each_story = []
    timelines = []
    # Calculate the approriate figure size to fit all the subplots
    amount = len(list(texter.data.keys()))
    rows = int(amount ** 0.5)
    columns = math.ceil(amount / rows)
    plt.figure(figsize=(amount * 4, amount))
    # Extrat timelines to be plotted
    for title in texter.data.keys():
        word_list_final, data = popularity_over_all_time(title, word_list, release_year, texter, k=k)
        timelines.append(data)
        words_each_story.append(word_list_final)
    # Create a subplot for each text
    for i in range(amount):
        position = i + 1
        plt.subplot(rows, columns, position)
        # Plot each line in each subplot
        for j in range(len(timelines[i])):
            plt.plot(Wordtrends.dcds, timelines[i][j], label=words_each_story[i][j])
        plt.xlabel("Decades")
        plt.ylabel("Popularity")
        plt.title(list(texter.data.keys())[i])
        plt.legend()
    plt.tight_layout()
    plt.show()


def proportion_text_vs_ngrams(word, year, title, texter):
    word_ngram = Wordtrends(word, year)
    x = word_ngram.proportion
    words_in_text = dict(texter.data[title][0][1])
    if word in words_in_text.keys():
        count = words_in_text[word]
    else:
        count = 0
    print(count)
    numwords = texter.data[title][1][1]
    y = count / numwords
    print([y, x])
    return [y, x]


def proportion_text_vs_ngrams_bars(word, year, texter):
    proportions = []
    text_titles = list(texter.data.keys())
    amount = len(text_titles)
    rows = int(amount ** 0.5)
    columns = math.ceil(amount / rows)
    plt.figure(figsize=(amount * 4, amount))
    for title in texter.data.keys():
        p = proportion_text_vs_ngrams(word, year, title, texter)
        proportions.append(p)
    for i in range(amount):
        position = i + 1
        plt.subplot(rows, columns, position)
        plt.bar([str(text_titles[i]), 'In Literature'], proportions[i], color=['red', 'blue'])
        plt.xlabel("Source")
        plt.ylabel("Popularity")
        plt.title(str(text_titles[i]))
    plt.title("Proportion in Text Vs. Literature")
    plt.tight_layout()
    plt.show()
