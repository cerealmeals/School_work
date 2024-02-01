import sys
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pykalman import KalmanFilter

def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

def get_data(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    
    lststr = []
    for child in root.iter('{http://www.topografix.com/GPX/1/0}trkpt'):
        lststr.append(child.attrib)

    
    df = pd.DataFrame(lststr)
    df['lat'] = (df['lat'].astype(float))
    df['lon'] = (df['lon'].astype(float))
    #print(df)
    return df

def distance(points):
    R = 6371
    p = np.pi/180
    boollist= [True]*points.shape[0]
    boollist[points.shape[0]-1] = False
    points2 = points.shift(periods=-1)
    lats = np.subtract(points2['lat'].values, points['lat'].values)*p
    lons = np.subtract(points2['lon'].values, points['lon'].values)*p
    #print(lats)
    #print(lons)
    a = 0.5 - np.cos(lats)/2 + np.cos((points['lat'].values*p))*np.cos((points2['lat'].values*p))*(1-(np.cos(lons)/2))
    #h = np.square(np.sin(lons))+np.cos((points['lat'].values*p))*np.cos((points2['lat'].values*p))*np.square(np.sin(lons))
    #sum = np.sum(((2*R)*np.arcsin(np.sqrt(h))), where=boollist, dtype=np.float64)
    dist = 2*R*np.arcsin(np.sqrt(a))
    #print(dist)
    sum = np.sum(dist, where=boollist)
    return sum

def smooth(points):

    initial_state = points.iloc[0]
    print(points.iloc[0])
    observation_covariance = np.diag([0.05, 0.05]) ** 2 # TODO: shouldn't be zero
    transition_covariance = np.diag([1, 1]) ** 2 # TODO: shouldn't be zero
    transition = [[1,0.1], [0.1,1]]

    kf = KalmanFilter(
    initial_state_mean=initial_state,
    initial_state_covariance=observation_covariance,
    observation_covariance=observation_covariance,
    transition_covariance=transition_covariance,
    transition_matrices=transition
    )

    pred_state, state_cov = kf.smooth(points)
    df = pd.DataFrame(pred_state, columns=['lat','lon'])
    print(df)
    return df

def main():
    points = get_data(sys.argv[1])
    print(points)
    # points = pd.DataFrame({
    # 'lat': [49.28, 49.26, 49.26],
    # 'lon': [123.00, 123.10, 123.05]})
    # print(distance(points).round(6))
    udistance = (distance(points),)
    print('Unfiltered distance: %0.2f' % udistance)
    #print(points)
    smoothed_points = smooth(points)
    fdistance = (distance(smoothed_points),)
    print('Filtered distance: %0.2f' % fdistance)
    output_gpx(smoothed_points, 'out.gpx')

    file = open('calc_distance.txt', 'w')
    file.write('Unfiltered distance: %0.2f\n' % udistance)
    file.write('Filtered distance: %0.2f' % fdistance)
    file.close


if __name__ == '__main__':
    main()