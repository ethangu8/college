# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 20:21:39 2021

@author: ethan gu
"""

import pandas as pd
from textblob import TextBlob
from bs4 import BeautifulSoup
pd.options.mode.chained_assignment = None

df1 = pd.read_csv("movie_df_with_arcs.csv")

attributes = df1[["primaryTitle", "runtimeMinutes", "polarity", "subjectivity", "genres", "arcs"]].copy()
attributes = attributes[attributes.runtimeMinutes != "\\N"]
attributes = attributes.astype({"runtimeMinutes": float})
with_profits = df1[["primaryTitle", "averageRating", "profit", "genres", "arcs"]].copy()

for_comparing = attributes.values.tolist()

def euclidean(p1, p2):
    """ Euclidean distance measure """
    return sum([(x1-x2)**2 for x1,x2 in zip(p1,p2)]) ** 0.5

def k_nearest(values, new, k, profits, genre, arc, func):
    runtime = new[0]
    new[0] = 1
    
    numeric_values = list()
    titles = list()
    distances = dict()
    cg = values[values["genres"].str.contains(genre)]
    same_arc = cg.loc[cg["arcs"].str.contains(arc)]
    for_comparing = same_arc.values.tolist()
    
    for value in for_comparing:
        title = value[0]
        comparing_values = value[1:]
        og_runtime = value[1]
        comparing_values[0] = og_runtime/runtime
        numeric_values.append(comparing_values)
        titles.append(title)
    
    for i in numeric_values:
        index = numeric_values.index(i)
        distance = func(new, i)
        distances[index] = distance
        
    distances_by_distance = sorted(distances.items(), key=lambda x: x[1])
    closest = distances_by_distance[:k]
    #return closest
    
    k_closest_movies = list()
    for i in closest:
        index = i[0]
        title = titles[index]
        k_closest_movies.append(title)
        
    result = profits.loc[(profits["primaryTitle"].isin(k_closest_movies))]
    result["profit"].replace({0.0:"Not in Database"}, inplace = True)
    result = result.iloc[:k]
    final = result[["primaryTitle", "averageRating", "profit"]].copy()
    
    return final

#print(k_nearest(attributes, [102, 0.04, 0.45], 3, with_profits, "Action", "icarus"))

def better_result(result):
    values = result.values.tolist()
    s = ""
    length = len(values)
    for i in range(length):
        if i == 0:
            s = values[i][0]
        elif i == length - 1:
            s = s + ", and " + values[i][0] + "."
        else:
            s = s + ", " + values[i][0]
    avg_rating = str(round(result["averageRating"].mean(), 5))
    avg_profit = str(round(result["profit"].mean(), 5))
    print("The most similar movies are " + s + "\n")
    print("The average rating of these movies is " + avg_rating)
    print("The average profit of these movies is " + avg_profit)
    print(result)
        
def get_stats_txt(file):
    #script = Path(file).read_text()
    with open(file, encoding = "utf-8") as f:
        text = f.read()
        pol, sub = TextBlob(text).sentiment
    return(pol, sub)    
    
def get_stats_html(file):
    with open(file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    script = soup.pre
    text = script.get_text(strip = False)
    pol, sub = TextBlob(text).sentiment
    return (pol, sub)


def main():
    while True:
        try:
            type_file = input("What type of file do you have for the script? (html or txt) ")
            if type_file in ["html", "txt"]:
                break;
            else:
                print("You did not enter an accepted file type.")
        except:
            continue
    
    if type_file == "html":
        script = input("What is the name of the html file for the movie? (Don't include .html) ")
        script += ".html"
        polarity, subjectivity = get_stats_html(script)
    if type_file == "txt":
        script = input("What is the name of the txt file for the movie? (Don't include .txt) ")
        script += ".txt"
        polarity, subjectivity = get_stats_txt(script)
    runtime = input("How long is this movie? (in minutes) ")
    genre = input("What genre is this movie? ")
    story_arc = input("What is the story arc of the movie? (man in a hole, icarus, rags to riches, riches to rags, oedipus, cinderella, unknown) ")
    
    stats = [float(runtime), polarity, subjectivity]
    k = input("How many nearest neighbors do you want to use? ")
    print("\n")
    
    if story_arc == "unknown":
        better_result(k_nearest(attributes, stats, int(k), with_profits, genre, " ", euclidean))
    else:
        better_result(k_nearest(attributes, stats, int(k), with_profits, genre, story_arc, euclidean))
    

if __name__ == "__main__":
    main()

