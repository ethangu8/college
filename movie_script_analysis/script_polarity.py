#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 19:24:18 2021

@author: ryanhuang, ethangu
"""
from textblob import TextBlob
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from bs4 import BeautifulSoup


def polarity_subjectivity(text, minsub=0.0, maxsub=1.0, minpol=-1.0, maxpol=1.0):
    '''
    Input is a list of lines, not a file
    Generates a plot of the polarity of a movie script from beginning to end
    
    To get a graph of the polynomial fit,
        comment the plt.scatter line
    
    '''
    coordinates = []
    
    for line in text:
        
        pol, sub = TextBlob(str(line)).sentiment

        if minpol <= pol <= maxpol and minsub <= sub <= maxsub:
            coordinates.append([pol,sub])

    # polarity = [i[0] for i in coordinates if i[0] != 0]  # ignore the zero sentiment lines
    polarity = [i[0] for i in coordinates]
    subjectivity = [j[1] for j in coordinates]
    

    # plt.figure()
    # plt.title("Polarity of " + movie_title)
    # plt.ylabel("Polarity")
    # plt.xlabel("Lines")
    
    
    # calculates the moving average values to plot
    window_size = int(len(polarity)/2) # i haven't found a formula to generalize this to each movie
    
    numbers_series = pd.Series(polarity)
    windows = numbers_series.rolling(window_size)
    moving_averages = windows.mean()
    
    moving_averages_list = moving_averages.tolist()
    without_nans = moving_averages_list[window_size - 1:] # removes the nan values from the moving average
    x1 = list(range(0,len(without_nans))) # represents the line of the script graph is on
    

    # plt.scatter(x1, without_nans, s = 2)


    # polyfit_and_save(np.array(x1), np.array(without_nans), 4)
    classify(np.array(x1), np.array(without_nans), 8)

def polyfit_and_save(x, y, deg):
    '''Fits a polynomial of degree 12 to the polarity graph'''

    # plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, deg))(np.unique(x)), color="black")

    # removes all numbers/ticks from the axis
    # plt.tick_params(axis='both', which="both", 
    #             bottom=False, top=False, 
    #             labelbottom=False, right=False, 
    #             left=False, labelleft=False)
    
    # plt.savefig("/Users/ryanhuang/Desktop/ds2500/" + movie_title + "_polarity_test.png")
classif = []
def classify(x, y, deg):
    
    critical_points = []
    
    try:
        curve = np.polyfit(x, y, deg)

        derivative = np.polyder(curve)
        
        roots = np.roots(derivative).tolist()
        
        for point in roots:
            if point < x[0] or point > x[-1]:
                roots.remove(point)
    
        # append the boundaries
        
        critical_points.append(np.polyval(curve, x[0])) 
        critical_points.append(np.polyval(curve, x[-1]))
        
        for point in roots:
            critical_points.append(np.polyval(curve, point))
    
            
        maxima = max(critical_points)
        minima = min(critical_points)
        
        avg = np.real((maxima + minima) / 2)
        
        plt.axhline(y=avg)
        
        L, R = np.polyval(curve, x[0]) - avg, np.polyval(curve, x[-1]) - avg
        
        num_intersections = intersections(curve, avg, x)
    
        if num_intersections % 2 == 0 and L > 0 and R > 0:
            x = "man in a hole"
            classif.append(x)
            return x
            #print(f"{movie_title} is man in a hole arc")
        elif num_intersections % 2 == 0 and L < 0 and R < 0:
            x ="icarus"
            classif.append(x)
            return x
            #print(f"{movie_title} is icarus arc")
        elif num_intersections == 1 and L < 0 and R > 0:
            x = "rags to riches"
            classif.append(x)
            return x
            #print(f"{movie_title} is rags to riches arc")
        elif num_intersections == 1 and L > 0 and R < 0:
            x = "riches to rags"
            classif.append(x)
            return x
            #print(f"{movie_title} is riches to rags arc")
        elif num_intersections % 2 != 0 and L > 0 and R < 0:
            x = "oedipus"
            classif.append(x)
            return x
            #print(f"{movie_title} is oedipus arc")
        elif num_intersections % 2 != 0 and L < 0 and R > 0:
            x = "cindarella"
            classif.append(x)
            return x
            #print(f"{movie_title} is cinderella arc")
        else:
            x = "can't classify"
            classif.append(x)
            return x
    except:
        x = "can't classify"
        classif.append(x)
        return classif
    
def intersections(curve, C, x):
    ''' Counts the number of intersections between a curve and a line in a bounded region'''
    curve[-1] = np.real(curve[-1] - C)
    temp = curve
    
    intersect = np.roots(temp)
    intersect = [point for point in intersect if np.imag(point) == 0]
    intersect = np.real(intersect).tolist()
    
    for point in intersect.copy():
        if point < x[0] or point > x[-1]:
            intersect.remove(point)

    return len(intersect)

def get_stats_html(file):
    with open(file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    script = soup.pre
    text = script.get_text(strip = False)
    pol, sub = TextBlob(text).sentiment
    return (pol, sub)

print(polarity_subjectivity(get_stats_html("Joker.html")))
    
def main():

    df = pd.read_csv("data_with_profit.csv")
    scripts = df["script_file"].tolist()
    
    for file in scripts:
        os.chdir(r'C:/Users/ethan/Desktop/movie_scripts')
        with open(file, encoding="utf8") as script:
            lines = script.readlines()
            #print(lines)
            lines = lines[0].split(".")

  
    df["arcs"] = classif
    df.to_csv(r'C:\Users\ethan\Desktop\movie_df_with_arcs.csv', sep=",", header = True)

if __name__ == "__main__":
    main()
    
    
    