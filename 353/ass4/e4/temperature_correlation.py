import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def best_tmax(cities, stations):
    lst = distance(cities, stations)
    cities['avg_tmax'] = lst[np.argmin(lst)]


def distance(points, points2):
    R = 6371
    p = np.pi/180
    #latitudes = np.subtract(points2['latitude'].values, points['latitude'].values)*p
    longitudes = np.subtract(points2['longitude'].values, points['longitude'])*p
    #print(latitudes)
    #print(longitudes)
    #a = 0.5 - np.cos(latitudes)/2 + np.cos((points['latitude'].values*p))*np.cos((points2['latitude'].values*p))*(1-(np.cos(longitudes)/2))
    h = np.arccos(np.sin(points['latitude']*p)*np.sin(points2['latitude'].values*p)
                  + np.cos(points['latitude']*p)*np.cos(points2['latitude'].values*p)
                  * np.cos(longitudes)) * R
    
    #dist = 2*R*np.arcsin(np.sqrt(a))
    #print(dist)
    #sum = np.sum(dist, where=boollist)
    return h

def main():
    stations = pd.read_json(sys.argv[1], lines=True)
    cities = pd.read_csv(sys.argv[2])
    
    #stations = stations.dropna(subset=['avg_tmax', 'latitude', 'longitude'])
    stations['avg_tmax'] = np.divide(stations['avg_tmax'].values, 10)
    cities = cities.dropna()
    cities['area'] = np.divide(cities['area'], 1000000)
    cities = cities[cities['area'] <= 10000]
    cities['density'] = cities['population']/cities['area']
    cities['avg_tmax'] = 0
    cities.apply(best_tmax, stations=stations)
    print(stations)
    print(cities)


if __name__ == '__main__':
    main()