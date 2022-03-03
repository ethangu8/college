"""
filename: Txet.py
description: A reusable library for text analysis and comparison
"""

from collections import Counter, defaultdict
from sankey import *
import matplotlib.pyplot as plt
import pandas as pd
import re
import os

'''
def top_k_words(df):
    top_dict = dict()
    word_dict = df.to_dict('index')
    for k,v in word_dict.items():
        valu = list(v.values())
        if valu[0] not in top_dict.keys():
            top_dict[valu[0]] = [valu[1]]
        else:
            top_dict[valu[0]].append(valu[1])

    return top_dict
'''

class Txet:

    def __init__(self):
        """Constructor"""
        self.data = defaultdict()

    def _save_results(self, label, results):
        counts, total = results.items()
        self.data[label] = [counts, total]

    def _clean_stop_words(string):
        stop_words = ["able", "about", "above", "abroad", "according", "accordingly", "across", "actually", "adj",
                      "after", "afterwards", "again", "against", "ago", "ahead", "ain't", "all", "allow", "allows",
                      "almost", "alone", "along", "alongside", "already", "also", "although", "always", "am", "amid",
                      "amidst", "among", "amongst", "an", "and", "another", "any", "anybody", "anyhow", "anyone",
                      "anything", "anyway", "anyways", "anywhere", "apart", "appear", "appreciate", "appropriate",
                      "are", "aren't", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "available",
                      "away", "awfully", "back", "backward", "backwards", "be", "became", "because", "become",
                      "becomes", "becoming", "been", "before", "beforehand", "begin", "behind", "being", "believe",
                      "below", "beside", "besides", "best", "better", "between", "beyond", "both", "brief", "but", "by",
                      "came", "can", "cannot", "cant", "can't", "caption", "cause", "causes", "certain", "certainly",
                      "changes", "clearly", "c'mon", "co", "co.", "com", "come", "comes", "concerning", "consequently",
                      "consider", "considering", "contain", "containing", "contains", "corresponding", "could",
                      "couldn't", "course", "c's", "currently", "dare", "daren't", "definitely", "described", "despite",
                      "did", "didn't", "different", "directly", "do", "does", "doesn't", "doing", "done", "don't",
                      "down", "downwards", "during", "each", "edu", "eg", "eight", "eighty", "either", "else",
                      "elsewhere", "end", "ending", "enough", "entirely", "especially", "et", "etc", "even", "ever",
                      "evermore", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly",
                      "example", "except", "fairly", "far", "farther", "few", "fewer", "fifth", "first", "five",
                      "followed", "following", "follows", "for", "forever", "former", "formerly", "forth", "forward",
                      "found", "four", "from", "further", "furthermore", "get", "gets", "getting", "given", "gives",
                      "go", "goes", "going", "gone", "got", "gotten", "greetings", "had", "hadn't", "half", "happens",
                      "hardly", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "hello", "help",
                      "hence", "her", "here", "hereafter", "hereby", "herein", "here's", "hereupon", "hers", "herself",
                      "he's", "hi", "him", "himself", "his", "hither", "hopefully", "how", "howbeit", "however",
                      "hundred", "i'd", "ie", "if", "ignored", "i'll", "i'm", "immediate", "in", "inasmuch", "inc",
                      "inc.", "indeed", "indicate", "indicated", "indicates", "inner", "inside", "insofar", "instead",
                      "into", "inward", "is", "isn't", "it", "it'd", "it'll", "its", "it's", "itself", "i've", "just",
                      "k", "keep", "keeps", "kept", "know", "known", "knows", "last", "lately", "later", "latter",
                      "latterly", "least", "less", "lest", "let", "let's", "like", "liked", "likely", "likewise",
                      "little", "look", "looking", "looks", "low", "lower", "ltd", "made", "mainly", "make", "makes",
                      "many", "may", "maybe", "mayn't", "me", "mean", "meantime", "meanwhile", "merely", "might",
                      "mightn't", "mine", "minus", "miss", "more", "moreover", "most", "mostly", "mr", "mrs", "much",
                      "must", "mustn't", "my", "myself", "name", "namely", "nd", "near", "nearly", "necessary", "need",
                      "needn't", "needs", "neither", "never", "neverf", "neverless", "nevertheless", "new", "next",
                      "nine", "ninety", "no", "nobody", "non", "none", "nonetheless", "noone", "no-one", "nor",
                      "normally", "not", "nothing", "notwithstanding", "novel", "now", "nowhere", "obviously", "of",
                      "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "one's", "only", "onto",
                      "opposite", "or", "other", "others", "otherwise", "ought", "oughtn't", "our", "ours", "ourselves",
                      "out", "outside", "over", "overall", "own", "particular", "particularly", "past", "per",
                      "perhaps", "placed", "please", "plus", "possible", "presumably", "probably", "provided",
                      "provides", "que", "quite", "qv", "rather", "rd", "re", "really", "reasonably", "recent",
                      "recently", "regarding", "regardless", "regards", "relatively", "respectively", "right", "round",
                      "said", "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing", "seem",
                      "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious",
                      "seriously", "seven", "several", "shall", "shan't", "she", "she'd", "she'll", "she's", "should",
                      "shouldn't", "since", "six", "so", "some", "somebody", "someday", "somehow", "someone",
                      "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified",
                      "specify", "specifying", "still", "sub", "such", "sup", "sure", "take", "taken", "taking", "tell",
                      "tends", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's",
                      "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there",
                      "thereafter", "thereby", "there'd", "therefore", "therein", "there'll", "there're", "theres",
                      "there's", "thereupon", "there've", "these", "they", "they'd", "they'll", "they're", "they've",
                      "thing", "things", "think", "third", "thirty", "this", "thorough", "thoroughly", "those",
                      "though", "three", "through", "throughout", "thru", "thus", "till", "to", "together", "too",
                      "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "t's", "twice", "two",
                      "un", "under", "underneath", "undoing", "unfortunately", "unless", "unlike", "unlikely", "until",
                      "unto", "up", "upon", "upwards", "us", "use", "used", "useful", "uses", "using", "usually", "v",
                      "value", "various", "versus", "very", "via", "viz", "vs", "want", "wants", "was", "wasn't", "way",
                      "we", "we'd", "welcome", "well", "we'll", "went", "were", "we're", "weren't", "we've", "what",
                      "whatever", "what'll", "what's", "what've", "when", "whence", "whenever", "where", "whereafter",
                      "whereas", "whereby", "wherein", "where's", "whereupon", "wherever", "whether", "which",
                      "whichever", "while", "whilst", "whither", "who", "who'd", "whoever", "whole", "who'll", "whom",
                      "whomever", "who's", "whose", "why", "will", "willing", "wish", "with", "within", "without",
                      "wonder", "won't", "would", "wouldn't", "yes", "yet", "you", "you'd", "you'll", "your", "you're",
                      "yours", "yourself", "yourselves", "you've", "zero", "a", "how's", "i", "when's", "why's", "b",
                      "c", "d", "e", "f", "g", "h", "j", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "uucp", "w",
                      "x", "y", "z", "I", "www", "amount", "bill", "bottom", "call", "computer", "con", "couldnt",
                      "cry", "de", "describe", "detail", "due", "eleven", "empty", "fifteen", "fifty", "fill", "find",
                      "fire", "forty", "front", "full", "give", "hasnt", "herse", "himse", "interest", "itse”", "mill",
                      "move", "myse”", "part", "put", "show", "side", "sincere", "sixty", "system", "ten", "thick",
                      "thin", "top", "twelve", "twenty", "abst", "accordance", "act", "added", "adopted", "affected",
                      "affecting", "affects", "ah", "announce", "anymore", "apparently", "approximately", "aren",
                      "arent", "arise", "auth", "beginning", "beginnings", "begins", "biol", "briefly", "ca", "date",
                      "ed", "effect", "et-al", "ff", "fix", "gave", "giving", "heres", "hes", "hid", "home", "id", "im",
                      "immediately", "importance", "important", "index", "information", "invention", "itd", "keys",
                      "kg", "km", "largely", "lets", "line", "'ll", "means", "mg", "million", "ml", "mug", "na", "nay",
                      "necessarily", "nos", "noted", "obtain", "obtained", "omitted", "ord", "owing", "page", "pages",
                      "poorly", "possibly", "potentially", "pp", "predominantly", "present", "previously", "primarily",
                      "promptly", "proud", "quickly", "ran", "readily", "ref", "refs", "related", "research",
                      "resulted", "resulting", "results", "run", "sec", "section", "shed", "shes", "showed", "shown",
                      "showns", "shows", "significant", "significantly", "similar", "similarly", "slightly", "somethan",
                      "specifically", "state", "states", "stop", "strongly", "substantially", "successfully",
                      "sufficiently", "suggest", "thered", "thereof", "therere", "thereto", "theyd", "theyre", "thou",
                      "thoughh", "thousand", "throug", "til", "tip", "ts", "ups", "usefully", "usefulness", "'ve",
                      "vol", "vols", "wed", "whats", "wheres", "whim", "whod", "whos", "widely", "words", "world",
                      "youd", "youre"]
        string_words = string.split()
        resultwords = [word for word in string_words if not word.lower() in stop_words]
        result = ' '.join(resultwords)
        return result

    @staticmethod
    def _default_parser(filename):
        filtered_text = str()
        original_text = str()
        with open(filename, encoding='utf-8') as file:
            for line in file:
                original_text += line
                new_line = line.lower()
                new_line = re.sub(r'[^\w\s]', '', new_line)
                new_line = new_line.replace("\n", ' ')
                line = Txet._clean_stop_words(new_line)
                line = line.strip()
                filtered_text += line + " "
        filtered_text = " ".join(filtered_text.split())
        results = {
            'wordcount': Counter(filtered_text.split(" ")),
            'numwords': len(original_text.split())
        }
        return results

    def load_text(self, filename, label=None, parser=None):
        if parser is None:
            results = Txet._default_parser(filename)
        else:
            results = parser(filename)
        if label is None:
            label = filename
        self._save_results(label, results)

    def wordcount_sankey(self, word_list=None, k=5):
        counts_by_story = pd.DataFrame(columns=['Story', 'Word', 'Count'])
        top_words_list = list()
        top_dict = {}
        for story in self.data:
            results = self.data[story]
            counts = results[0]
            counter = counts[1]
            top_words = counter.most_common(k)
            top_dict[story] = top_words
            for tuple in top_words:
                word = tuple[0]
                count = tuple[1]
                if word in top_words_list:
                    df_row = {'Story': story, 'Word': word, 'Count': count}
                    counts_by_story = counts_by_story.append(df_row, ignore_index=True)
                else:
                    top_words_list.append(word)
                    df_row = {'Story': story, 'Word': word, 'Count': count}
                    counts_by_story = counts_by_story.append(df_row, ignore_index=True)
        return top_dict, counts_by_story


def main():
    texter = Txet()
    os.chdir(r"/Users/ethan/Desktop/sherlock")
    texter.load_text('story1.txt', label='Story 1')
    texter.load_text('story2.txt', label='Story 2')
    texter.load_text('story3.txt', label='Story 3')
    texter.load_text('story4.txt', label='Story 4')
    texter.load_text('story5.txt', label='Story 5')
    texter.load_text('story6.txt', label='Story 6')
    texter.load_text('story7.txt', label='Story 7')
    texter.load_text('story8.txt', label='Story 8')
    vals, df = texter.wordcount_sankey()
    make_sankey(df, 'Story', 'Word', 'Count')
    #print(x)


main()


