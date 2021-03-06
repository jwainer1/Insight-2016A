import MySQLdb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from sklearn.neighbors.kde import KernelDensity
import pickle
import smopy
import dbscanning
import math


def date_extract(date_taken):
    return date_taken.split(' ')[0].strip()

def time_extract(date_taken):
    return date_taken.split(' ')[1].strip()

def month_extract(date_taken):
    return int(date_taken.split(' ')[0].split('-')[1])

def day_extract(date_taken):
    return int(date_taken.split(' ')[0].split('-')[2])

def year_extract(date_taken):
    return int(date_taken.split(' ')[0].split('-')[0])

def season_extract(date_taken):
    #return season as winter=0, spring = 1, summer = 2, fall = 3
    month = int(date_taken.split(' ')[0].split('-')[1])
    day = int(date_taken.split(' ')[0].split('-')[2])
    #determine the season of date_taken based on equinoxes and solstices
    #spring = March 20, summer = June 21, autumnal = September 22, winter = December 21
    if (month < 3) | ((month == 3) & (day < 20)):
	return 0
    elif ((month == 3) & (day >= 20)) | ((month > 3) & (month < 6)) | ((month == 6) & (day < 21)):
	return 1
    elif ((month == 6) & (day >= 21)) | ((month > 6) & (month < 9)) | ((month == 9) & (day < 22)):
	return 2
    elif ((month == 9) & (day >= 22)) | ((month > 9) & (month < 12)) | ((month == 12) & (day < 21)):
	return 3
    elif ((month == 12) & (day >= 21)):
	return 0

cnxn = MySQLdb.connect("localhost","root","golgo13","picturesdb") 
cursor = cnxn.cursor()
sql = "SELECT * FROM PhotosPittsburgh"

allData = pd.read_sql(sql, cnxn)
print "Read the data from SQL"

allData['Season'] = allData['DateTaken'].apply(season_extract)
seasons = {0:'winter', 1:'spring', 2:'summer', 3:'fall'}

#*********************************************
for whichseason in range(4,5):
    if whichseason==4:
	print allData[['Longitude', 'Latitude']].describe()
    	#points = allData[['Longitude', 'Latitude']].values
	points = allData
    else:
    	print allData[allData['Season'] == whichseason][['Longitude', 'Latitude']].describe()
    	#points = allData[allData['Season'] == whichseason][['Longitude', 'Latitude']].values
	points = allData[allData['Season'] == whichseason]

    clusteredPoints = dbscanning.display_clusters(points, 0)
    print clusteredPoints.describe()
    #print clusteredPoints.groupby('Cluster').mean()
    print clusteredPoints[['Longitude', 'Latitude','Cluster']].groupby('Cluster').mean()
    returnedPoints = clusteredPoints[clusteredPoints['Cluster'] > -1][['Longitude', 'Latitude']].values
    min = allData[['Longitude', 'Latitude']].min()
    max = allData[['Longitude', 'Latitude']].max()

    resolution = 300j
    xx, yy = np.mgrid[min[0]:max[0]:resolution, min[1]:max[1]:resolution]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    #values = np.vstack([points[:,0], points[:,1]])
    values = np.vstack([returnedPoints[:,0], returnedPoints[:,1]])

    #using sci-kit learn's kde
    #kde = KernelDensity(kernel='exponential', bandwidth=0.0000002).fit(values.T)
    kde = KernelDensity(kernel='exponential', bandwidth=0.001).fit(values.T)
    #kde = KernelDensity(kernel = 'gaussian', bandwidth=0.0001).fit(values.T)
    log_dens = kde.score_samples(positions.T)
    otherf = np.reshape(log_dens, xx.shape)
    if (whichseason < 4):
	print "Finished getting exponential kde via scikit-learn for points in ", seasons[whichseason]
    else:
	print "Finished getting exponential kde via scikit-learn for all points"

    #map = smopy.Map((min[1],min[0]), (max[1],max[0]), z=13, margin=.1)
    map = smopy.Map((min[1],min[0]), (max[1],max[0]), z=13, margin=.1)
    #ax2= map.show_mpl();
    if whichseason < 4:
    	latlongpoints = allData[allData['Season'] == whichseason][['Longitude', 'Latitude']].values
    else:
	latlongpoints = allData[['Longitude', 'Latitude']].values
    x, y = map.to_pixels(latlongpoints[:,1], latlongpoints[:,0])
    ax2 = map.show_mpl(figsize=(8, 6))
    ax2.plot(x, y, '.b');


    #And now for the scikit-learn one!
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim(min[0], max[0])
    ax.set_ylim(min[1], max[1])

    # Contourf plot with black bars
    cfset = ax.contourf(xx, yy, otherf, cmap='hot')
    cset = ax.contour(xx, yy, otherf, colors='k')
    print "Levels: ", cset.levels
    print "Zmin: ", cset.zmin
    print "Zmax: ", cset.zmax

    # Label plot
    ax.clabel(cset, inline=1, fontsize=10)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Using exponential scikit-learn kernel')
    ax.plot(latlongpoints[:,0], latlongpoints[:,1], '.b');

    #Set up color bar
    cbar = plt.colorbar(cfset)
    cbar.ax.get_yaxis().set_ticks([])
    for j, lab in enumerate(cset.levels):
    	cbar.ax.text(3.0, ((j+1) / 7.0) + (1/14.0), math.pow(10,lab), ha='center', va='center')
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('Probability density', rotation=270)
    
    plt.show()

    if (whichseason < 4):
    	directory = "data/" + seasons[whichseason] + "/"
    	#pickle the variable f and the resolution
    	with open(directory + "kernel.pkl", 'wb') as file:
    	    pickle.dump(otherf, file)
    	with open(directory + "resolution.pkl", 'wb') as file:
    	    pickle.dump(resolution.imag, file)
    	with open(directory + "min.pkl", 'wb') as file:
    	    pickle.dump(min, file)
    	with open(directory + "max.pkl", 'wb') as file:
    	    pickle.dump(max, file)
    	with open(directory + "levels.pkl", 'wb') as file:
    	    pickle.dump(cset.levels, file)
    	with open(directory + "clusteredpoints.pkl", 'wb') as file:
    	    pickle.dump(clusteredPoints[clusteredPoints['Cluster'] > -1], file)
	#with open(directory + "clustercenters.pkl", 'wb') as file:
    	#    pickle.dump(clusteredPoints.groupby('Cluster').mean(), file)

cnxn.close()
