# Testing accessing movie data
import pandas as pd
import os
from textblob import TextBlob
import matplotlib.pyplot as plt
#from Script_analysis import *

# Taking IMDB datasets, combining "important" ones
basics_tsv = "basics.tsv"
basics = pd.read_csv(basics_tsv, sep = "\t", low_memory = False)

ratings_tsv = "ratings.tsv"
ratings = pd.read_csv(ratings_tsv, sep = "\t", low_memory = False)

# merge the tables on their movieID, clean it to only the columns I thought 
# we'd need
data = pd.merge(basics, ratings, on ="tconst")
new_data = data[["tconst", "primaryTitle", "runtimeMinutes", 
                 "genres", "averageRating"]].copy()
new_data.to_csv(r'C:\Users\ethan\Desktop\movie_data.csv', sep=",", header=True)

# Make lists for titles and files to form into a dataframe
title_list = list()
file_list = list()

# Locate directory for the folder of scripts
for filename in os.listdir("/Users/ethan/Desktop/movie_scripts"):
    os.chdir(r'C:/Users/ethan/Desktop/movie_scripts')
    file_list.append(filename)
    # Extract the movie name from the file name, remove Script_ and the .txt
    if filename.startswith("Script_"):
        title = filename[7:]
        new_title = title.replace(".txt", "")
        title_list.append(new_title)
        
# Form the titles and scripts into a new data frame
scripts_df = pd.DataFrame({"primaryTitle": title_list, "script_file": file_list})
# merge the new script dataframe with the IMDB dataframe
merged_df = pd.merge(scripts_df, new_data, on = "primaryTitle")
# there are duplicates of the same movie for some reason, so drop all but the first
final_df = merged_df.drop_duplicates(subset=["primaryTitle"], keep="first")
final_df = final_df.reset_index(drop=True)


def get_stats(file):
    #script = Path(file).read_text()
    with open(file, encoding = "utf-8") as f:
        text = f.read()
        pol, sub = TextBlob(text).sentiment
        return(pol, sub)

#print(get_stats("Script_You've Got Mail.txt"))
list_of_scripts = final_df["script_file"].tolist()
sentiment_list = list()
polarity_list = list()
subjectivity_list = list()
for script in list_of_scripts:
    scores = get_stats(script)
    polarity = scores[0]
    subjectivity = scores[1]
    polarity_list.append(polarity)
    subjectivity_list.append(subjectivity)
    sentiment_list.append(scores)


final_df["polarity"] = polarity_list
final_df["subjectivity"] = subjectivity_list





final_df.to_csv(r'C:\Users\ethan\Desktop\final_df.csv', sep=",", header = True)


      
    
