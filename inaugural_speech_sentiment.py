# Ethan Gu

"""
Decided to seek similarities between presidents that were impeached vs 
presidents that were assassinated. The presidents I chose to look into were:
Impeached:
- Andrew Johnson
- Bill Clinton
- Donald Trump
Assassinated:
- Abe Lincoln
- William McKinley
- John F. Kennedy
"""
import wordcloud as wc
from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import numpy as np


def main():
    wordClouds(load())
    polar_vs_subject(score_speeches_overall(load()))
    plotCommonWords(common_words(load(), 3), 20)
    polarity_vs_subjectivity(score_speech_by_line(load()))

#function to unpack the txt files for the inaugural speeches
def load():
    files = {}
    files['Johnson'] = Path("Johnson.txt").read_text()
    files['Clinton'] = Path("Clinton.txt").read_text()
    files["Trump"] = Path("Trump.txt").read_text()
    files["Lincoln"] = Path("Lincoln.txt").read_text()
    files["McKinley"] = Path("McKinley.txt").read_text()
    files["Kennedy"] = Path("Kennedy.txt").read_text()
    return files
    
#construct wordclous from the speeches
def wordClouds(d):
    keys = list(d.keys())
    cloud = wc.WordCloud()
    rows = 2
    columns = 3
    fig = plt.figure(figsize=(rows, columns), dpi=200)
    index = 1
    for president in keys:
        speech = d[president]
        string_cloud = cloud.generate(speech)
        
        fig.add_subplot(rows, columns, index)
        plt.imshow(string_cloud)
        plt.title(president, fontsize=8)
        plt.axis('off')
        index += 1
    plt.show()

#using TextBlob, score the speeches for polarity and subjectivity by line
def score_speech_by_line(file, minsub=0.0, maxsub=1.0, minpol=-1.0, maxpol=1.0):
    speeches = list(file.values())
    presidents = list(file.keys())
    result = {}
    filtered = {}
    for speech in speeches:
        x = speeches.index(speech)
        president = presidents[x]
        lines = speech.splitlines()
        for line in lines:
            pol, sub = TextBlob(line).sentiment
            filtered[line] = (pol, sub)
        result[president] = filtered
        filtered = {}
    return result

#create scatter and kde plots for the speeches' polarity and subjectivity
def polarity_vs_subjectivity(d, title = '', marker = 'black'):
    rows = 2
    columns = 3
    index = 0
    fig, axes = plt.subplots(rows, columns, figsize=(18, 10))
    axis_list = [axes[0,0], axes[0,1], axes[0,2], axes[1,0], axes[1,1], axes[1,2]]
    for president in d:
        scored = d[president]
        scores = scored.values()
        polarity = [x[0] for x in scores]
        subjectivity = [x[1] for x in scores]
        
        
        sns.scatterplot(ax = axis_list[index], x=subjectivity, 
                        y=polarity, s=3, color=marker)
        sns.kdeplot(ax = axis_list[index], x=subjectivity, y=polarity, 
                    color=marker).set(title=president, 
                                      xlabel="Subjectivity", ylabel="Polarity")
        plt.xlabel("Subjectivity")
        plt.ylabel("Polarity")
        index += 1
    
#takes entire speeches and gets and overall polarity and subejctivity score
def score_speeches_overall(file, minsub=0.0, maxsub=1.0, minpol=-1.0, maxpol=1.0):
    filtered = {}
    speeches = list(file.values())
    presidents  = list(file.keys())
    for speech in speeches:
        x = speeches.index(speech)
        president = presidents[x]
        pol, sub = TextBlob(speech).sentiment
        filtered[president] = (pol, sub)
    return filtered

#uses Counter to get counts of all words over a given length
def common_words(file, length):
    counts = {}
    word_list = []
    for i in file:
        speech = file[i]
        words = speech.split()
        for word in words:
            if len(word) > length:
                word_list.append(word)
            count = Counter(word_list)
            counts[i] = count
    return counts

#take the top (num) numbers and creates a plot of how many times each president
#uses a common word
def plotCommonWords(count, num):
    values = list(count.values())
    presidents = list(count.keys())
    word_list = []
    cbp = {}     #count by president
    for i in values:
        top_words = i.most_common(num)
        word_list += top_words
    all_words = [x[0] for x in word_list]
    overall_top_words = list(set(all_words))
    
    for president in presidents:
        vocab = count[president]
        vec = [vocab[word] for word in overall_top_words]
        cbp[president] = vec
    
    x = np.arange(1, len(overall_top_words)+1)
    johnson = cbp["Johnson"]
    clinton = cbp["Clinton"]
    trump = cbp["Trump"]
    lincoln = cbp["Lincoln"]
    mckinley = cbp["McKinley"]
    kennedy = cbp["Kennedy"]
    
    plt.xticks(x, overall_top_words, rotation='vertical')
    plt.plot(x, johnson, label="Johnson (1865)")
    plt.plot(x, clinton, label="Clinton (1993)")
    plt.plot(x, trump, label="Trump (2017)")
    plt.plot(x, lincoln, label="Lincoln (1861)")
    plt.plot(x, mckinley, label="McKinley (1897)")
    plt.plot(x, kennedy, label="Kennedy (1961)")
    plt.text(x=12,y=98,s="will")
    plt.legend(prop={'size':8})
    plt.show()

#create a plot for the overall polarity and subjectivity of the speeches
def polar_vs_subject(scored):
    scores = scored.values()
    names = scored.keys()
    polarity = [x[0] for x in scores]
    subjectivity = [x[1] for x in scores]
    
    X_axis = np.arange(len(names))
    plt.bar(X_axis - 0.2, polarity, 0.4, label = "Polarity")
    plt.bar(X_axis + 0.2, subjectivity, 0.4, label = "Subjectivity")
    plt.xticks(X_axis, names)
    plt.xlabel("Presidents")
    plt.title("Polarity and Subjectivity by President")
    plt.legend()
    plt.show()
"""
When it comes to presidents that have been impeached or assassinated, the 
initial thought (or at least my initial thought) would be that their overall 
speech polarity would be more negative to result in general public discontent.
In the plot I made for the overall polarity and subjectivity of inaugural 
speeches we can see that the polarity, though not extremely positive is net
positive.
"""
    
main()
    
