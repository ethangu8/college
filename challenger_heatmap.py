# Ethan Gu

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import math
import matplotlib.pyplot as plt
import numpy as np

def main():
    df = nearCapeC(filterFiles('stations.csv', 'temp_1986.csv', 1))
    temp_plot(temp_est(df))
    imgPlot(makeCoords(filterFiles('stations.csv', 'temp_1986.csv', 1), 28))
    imgPlot(makeCoords(filterFiles('stations.csv', 'temp_1986.csv', 2), 1))

#Filters and combines the two csv files
#removes rows containing NA, "invalid" coordinates (0,0)
#also takes in a month, and returns only values in given month
def filterFiles(file1, file2, month):
    #read the csv files into separate dataframes
    df1 = pd.read_csv(file1, 
                      names=['Station ID', 'WBAN ID', 'Latitude', 'Longitude'])
    df2 = pd.read_csv(file2,  names=['Station ID', 'WBAN ID', 'Month', 
                              'Day', 'Temperature'])
    
    #combine the dataframes into one
    #note:used both IDs to avoid WBAN ID_x and WBAN ID_y when merging
    combined = pd.merge(df1, df2, on=["Station ID", "WBAN ID"])

    #filtering the combined dataframe
    combined = combined.drop(columns = 'WBAN ID')
    combined = combined.dropna(how='any', axis=0) 
    
    #filtering out points where Latitude and Longitude both were 0.0
    invalid_coords = combined[(combined['Latitude'] == 0.0) & 
                              (combined['Longitude'] == 0.0)].index
    combined.drop(invalid_coords, inplace=True)
    
    #filtering to only have January data points
    combined_jan = combined.loc[combined['Month'] == month]
    return combined_jan

'''
used: https://www.geeksforgeeks.org/haversine-formula-to-find-distance-
between-two-points-on-a-sphere/'''
def haversine(lat1, lon1, lat2, lon2):
     
    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2));
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

#uses haversine to calculate the distance of each weather station from Cape
#Canaveral, and stores this distance in a new column in the dataframe
def nearCapeC(df):
    validIndexes = []
    distances = []
    lat1 = float(28.396837)
    lon1 = float(-80.605659)
    for i in range(len(df)):
        station = df.iat[i, 0]
        lat2 = df.iat[i, 1]
        lon2 = df.iat[i, 2]
        distance = haversine(lat1, lon1, lat2, lon2)    
        if distance < 100:            
            validIndexes.append(station)
            distances.append(distance)
    valid = set(validIndexes)
    closeStations = df[df['Station ID'].isin(valid)]
    closeStations["Distance"] = distances
    return closeStations

#uses inverse distance weighting to make an estimate for the temperature in
#Cape Canaveral
def temp_est(df):
    p = 1
    df['inv_dist'] = 1 / (df.Distance ** p)
    df['weighted'] = df.Temperature * df.inv_dist
    df2 = df[df['Day'] == 28]
    #used inverse distance weighting formula from class
    temp_estimate = df2.weighted.sum()/df2.inv_dist.sum()
    print("The temperature at Cape Canaveral on January 28, 1986 was approx. " 
          + str(temp_estimate) + " degrees Fahrenheit")
    return df

#utilizes the columns made in temp_est to make an estimate for Cape Canaveral
#on every day in January and plot these values
def temp_plot(df):
    estimates = {}
    list_of_days = df["Day"].to_list()
    #makes into a set to remove duplicates
    set_of_days = set(list_of_days)
    for i in set_of_days:
        temps = df.loc[df["Day"] == i]
        estimate = temps.weighted.sum()/temps.inv_dist.sum()
        estimates[i] = estimate
    days = estimates.keys()
    temp_estimates = estimates.values()
    plt.plot(days, temp_estimates)
    plt.xlabel("Day (in January)")
    plt.ylabel("Temperature")
    plt.title("Temperature by Day in January (Cape Canaveral)")
    plt.show()

#makes x and y coordinates from the longitude and latitude values
def makeCoords(df, day):
    df = df[df['Day'] == day]
    #taking only coordinates that would fall into the "boundaries" of the US
    df = df[(df.Latitude > 25.0) & (df.Latitude < 50) &
                     (df.Longitude > -125.0) & (df.Longitude < -65.0)]
    df = df.reset_index()
    # finding the indexes/y/x-coord
    #actual formula would be (longitude-(-125)/(-65-(-125))), but simplified
    df['x_coord'] = ((df.Longitude + 125)/60) * 150
    df['x_coord'] = df.x_coord.astype(int)
    #actual formula would be ((latitude - 50)/(25-50))
    df['y_coord'] = ((df.Latitude - 50)/-25) * 100
    df['y_coord'] = df.y_coord.astype(int)
    df = df[["x_coord", "y_coord", "Temperature"]]
    df = df.sort_values('Temperature') 
    return df

#takes in a float temperature and returns an RGB color
#hard coded colors for temperature ranges 
def tempToColor(temp):
    color  = [0] * 3
    if temp < 10:
        color = [0, 0, 255]
    elif temp < 20:
        color = [0, 188, 255]
    elif temp < 30:
        color = [0, 239, 255]
    elif temp < 40:
        color = [0, 255, 205]
    elif temp < 50:
        color = [0, 255, 68]
    elif temp < 60:
        color = [171, 255, 0]
    elif temp < 70:
        color = [255, 213, 0]
    elif temp < 80:
        color = [255, 154, 0]
    else:
        color = [255, 0, 0]
    return color

#plots the coordinates as an array
def imgPlot(df):
    x_coords = df["x_coord"].tolist()
    y_coords = df["y_coord"].tolist()
    temps = df["Temperature"].tolist()
    
    #creates an array to store the values
    x = 100
    y = 150
    image = np.zeros((x, y, 3), dtype = int)
    numstations = len(x_coords)
    for i in range(numstations):
        xpos = x_coords[i]
        ypos = y_coords[i]
        temp = temps[i]
        color = tempToColor(temp)
        image[ypos, xpos] = color            
    plt.figure(figsize = (10,10))
    plt.imshow(image, interpolation = "none")
    plt.show()
    
main()
