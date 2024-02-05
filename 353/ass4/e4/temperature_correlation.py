import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def best_tmax(cities, stations):
    lst = distance(cities, stations)
    index = [np.argmin(lst)][0]
    return stations['avg_tmax'].values[index]


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
    cities['avg_tmax'] = cities.apply(best_tmax, stations=stations, axis=1)
    fit = stats.linregress(cities['density'].values, cities['avg_tmax'].values)
    cities['predictions'] = cities['density'].apply(lambda x: x*fit.slope + fit.intercept)
    print(stations)
    print(cities)
    r2 = np.corrcoef(cities['avg_tmax'].values, cities['predictions'].values)
    print(r2[0][1])

    
    plt.plot(cities['density'].values, cities['avg_tmax'].values, 'b.', alpha=0.5)
    plt.plot(cities['density'].values, cities['predictions'].values, 'r-', linewidth=2)
    plt.annotate("r-squared = {:.3f}".format(r2[0][1]), (0,0))
    plt.ylabel('Avg Max Temperatire (\u00b0C)')
    plt.xlabel('Population Density (people/km\u00b2)')
    plt.title('Tempurater vs Population Density')
    plt.savefig(sys.argv[3])

if __name__ == '__main__':
    main()