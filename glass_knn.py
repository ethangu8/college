# Homework 5: Machine Learning
# Ethan Gu

import pandas as pd
import csv
import random as rnd
import copy
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.metrics import classification_report

"""
Glass attributes and classes
1. Id number: 1 to 214
2. RI: refractive index
3. Na: Sodium (unit measurement: weight percent in corresponding oxide, as are attributes 4-10)
4. Mg: Magnesium
5. Al: Aluminum
6. Si: Silicon
7. K: Potassium
8. Ca: Calcium
9. Ba: Barium
10. Fe: Iron
11. Type of glass: (class attribute)
-- 1 building_windows_float_processed
-- 2 building_windows_non_float_processed
-- 3 vehicle_windows_float_processed
-- No 4 in database
-- 5 containers
-- 6 tableware
-- 7 headlamps
"""

def read_data(filename):
    """ Read file into attributes data and list of targets """
    data = []
    targets = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for col in range(len(row)-1):
                row[col] = float(row[col])
            data.append(row[1:10])
            targets.append(row[10])
    return (data, targets)

def euclidean(p1, p2):
    """ Euclidean distance measure """
    return sum([(x1-x2)**2 for x1,x2 in zip(p1,p2)]) ** 0.5

def k_nearest(data, k, func):
    """find the k nearest neighbors in the data set"""
    values = data[0]
    classes = data[1]
    nearest_neighbors = list()
    result = dict()
    count = 0
    for i in values:
        distances = list()
        index = 0
        
        for j in values:
            if j != i:
                distance = func(i, j)
                distances.append((classes[index], distance))
            else:
                pass
            index += 1
            distances.sort(key=lambda tup: tup[1])
        top = distances[:k] 
        distances.clear()
        result[count] = top
        count += 1
        
    return result

def classify(data):
    '''classify a data point based on the most frequent result'''
    estimate_dict = dict()
    for point in data:
        class_list = list()
        values = data[point]
        for value in values:
            class_list.append(value[0])
        counts = Counter(class_list)
        estimate = max(class_list, key=counts.get)
        estimate_dict[point] = estimate
        counts.clear()
    return list(estimate_dict.values())

def accuracy(data, estimates):
    '''find the overall accuracy of our estimates'''
    og_classes = data[1]
    result = [i for i, j in zip(og_classes, estimates) if i == j]
    accuracy = len(result)/len(estimates)
    return accuracy

def classification(actual, estimated, names):
    '''get a classification report with sklearn.metrics'''
    '''remove support since we are not interested in that statistic'''
    new_dict = dict()
    stats_dict = classification_report(actual, estimated, target_names=names, 
                                output_dict = True, zero_division=0)
    classes_dict = {name: stats_dict[name] for name in names}
    for i in classes_dict:
        values = classes_dict[i]
        del values['support']
        new_dict[i] = values 
    print(new_dict)
    return new_dict

def extract_value(data, name, parameter):
    '''extract a value from the classification report'''
    values = data[name]
    value = values[parameter]
    return value

def visualize_data(data, kvals, title):
    '''create the visualization, 6 line plots interweaved for each statistic'''
    building_f = data["Buildings (Float)"]
    building_nf = data["Buildings (Non-Float)"]
    vehicles = data["Vehicles"]
    containers = data["Containers"]
    tableware = data["Tableware"]
    headlamps = data["Headlamps"]
    
    
    plt.plot(kvals, building_f, label="Buildings (Float)")
    plt.plot(kvals, building_nf, label="Buildings (Non-Float)")
    plt.plot(kvals, vehicles, label="Vehicles")
    plt.plot(kvals, containers, label="Containers")
    plt.plot(kvals, tableware, label="Tableware")
    plt.plot(kvals, headlamps, label="Headlamps")
    plt.legend(prop={'size':7})
    plt.title(title)
    plt.show()
    
    
 
def main():
    data = read_data("glass.data")
    values = data[0]
    actual = data[1]
    names = ["Buildings (Float)", "Buildings (Non-Float)", "Vehicles",
             "Containers", "Tableware", "Headlamps"]
    k_values = [1, 3, 5, 10, 15, 20, 25, 30]
    accuracies = dict()
    
    precisions = dict()
    recalls = dict()
    f1_scores = dict()
    for name in names:
        precisions[name] = list()
        recalls[name] = list()
        f1_scores[name] = list()
    for k in k_values:
        estimates = classify(k_nearest(data, k, euclidean))
        overall_accuracy = round(accuracy(data, estimates), 5)
        accuracies[k] = overall_accuracy
        
        stats_dict = classification(actual, estimates, names)
        for name in names:
            point_p = extract_value(stats_dict, name, 'precision')
            precisions[name].append(point_p)
        for name in names:
            point_r = extract_value(stats_dict, name, 'recall')
            recalls[name].append(point_r)
        for name in names:
            point_f = extract_value(stats_dict, name, 'f1-score')
            f1_scores[name].append(point_f)
    
    visualize_data(precisions, k_values, "Precision by K-Value")
    visualize_data(recalls, k_values, "Recall by K-Value")
    visualize_data(f1_scores, k_values, "F1-Score by K-Value")
        
    k_num = k_values
    percentage = accuracies.values()
    plt.plot(k_num, percentage)
    plt.title("Overall Percent Accuracy by Number of Nearest Neighbors")
    plt.xlabel("K Value")
    plt.ylabel("Percent Accurate")
    plt.show()

       
main()
