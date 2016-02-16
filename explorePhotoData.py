import MySQLdb
import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np
#from sklearn.cluster import DBSCAN
import dbscanning
import smopy
import urllib

#return specific parts of the date_taken feature as new feature

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

allSanFranData = pd.read_sql(sql, cnxn)
allSanFranData['DayTaken'] = allSanFranData['DateTaken'].apply(day_extract)
allSanFranData['MonthTaken'] = allSanFranData['DateTaken'].apply(month_extract)
allSanFranData['YearTaken'] = allSanFranData['DateTaken'].apply(year_extract)

print allSanFranData['YearTaken'].describe()

#dbscanning.display_clusters(allSanFranData[['Longitude', 'Latitude']])

#show all the points in all seasons
plt.scatter(allSanFranData['Longitude'], allSanFranData['Latitude'], marker = ',')
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("All photos")
plt.show()


#determine the season of date_taken based on equinoxes and solstices
#spring = March 20, summer = June 21, autumnal = September 22, winter = December 21
allSanFranData['Season'] = allSanFranData['DateTaken'].apply(season_extract)

#allSanFranData.loc[ (allSanFranData['MonthTaken'] < 3) | \
#		    ((allSanFranData['MonthTaken'] == 3) & (allSanFranData['DayTaken'] < 20)), 'Season'] = 0

#allSanFranData.loc[ ((allSanFranData['MonthTaken'] == 3) & (allSanFranData['DayTaken'] >= 20)) |\
#		    ((allSanFranData['MonthTaken'] > 3) & (allSanFranData['MonthTaken'] < 6)) |\
#		    ((allSanFranData['MonthTaken'] == 6) & (allSanFranData['DayTaken'] < 21)), 'Season'] = 1

#allSanFranData.loc[ ((allSanFranData['MonthTaken'] == 6) & (allSanFranData['DayTaken'] >= 21)) |\
#		    ((allSanFranData['MonthTaken'] > 6) & (allSanFranData['MonthTaken'] < 9)) |\
#		    ((allSanFranData['MonthTaken'] == 9) & (allSanFranData['DayTaken'] < 22)), 'Season'] = 2

#allSanFranData.loc[ ((allSanFranData['MonthTaken'] == 9) & (allSanFranData['DayTaken'] >= 22)) |\
#		    ((allSanFranData['MonthTaken'] > 9) & (allSanFranData['MonthTaken'] < 12)) |\
#		    ((allSanFranData['MonthTaken'] == 12) & (allSanFranData['DayTaken'] < 21)), 'Season'] = 3

#allSanFranData.loc[ (allSanFranData['MonthTaken'] == 12) & (allSanFranData['DayTaken'] >= 21), 'Season'] = 0

#print allSanFranData.head(10)
#print allSanFranData.info()
#print allSanFranData[['PageURL','DownURL']].head(10)
#print allSanFranData[['PageURL','DownURL']].tail(10)

#farmNum = allSanFranData.loc[[2],['FarmID']].values
#serverNum = allSanFranData.loc[[2],['ServerID']].values
#photoID = allSanFranData.loc[[2],['PhotoID']].values
#secret = allSanFranData.loc[[2],['Secret']].values
#ext = allSanFranData.loc[[2],['Ext']].values
#print farmNum
#print serverNum
#print photoID
#print secret
#print ext
#theURL = str(farmNum[0][0]) + ".staticflickr.com/" + str(serverNum[0][0]) + "/" + str(photoID[0][0]) + "_" + str(secret[0][0]) + "." + ext[0][0]
#fullURL = "http://farm" + theURL
#urllib.urlretrieve ("http://farm4.staticflickr.com/3276/3105580981_b3f19a726a.jpg", "test.jpg")
#urllib.urlretrieve (fullURL, "test2.jpg")


seasons = {0:'Winter', 1:'Spring', 2:'Summer', 3:'Fall'}
colors = {0:'blue', 1:'green', 2:'red', 3:'orange'}
pos0 = (40.441676, -80.000061)
pos1 = (40.441402, -79.995153)

min = allSanFranData[['Longitude', 'Latitude']].min()
max = allSanFranData[['Longitude', 'Latitude']].max()



for season in range(0,4):
    #map = smopy.Map((min[1],min[0]), (max[1],max[0]), z=13, margin=0.1)
    map = smopy.Map((min[1],min[0]), (max[1],max[0]), z=13, margin=0.1)
    ax2 = map.show_mpl(figsize=(8, 6))
    ax2.set_xlabel("Longitude")
    ax2.set_ylabel("Latitude")
    ax2.set_title("Distribution of photos throughout seasons")
    #print allSanFranData[allSanFranData['Season'] == season ][['Longitude', 'Latitude']].describe()
    points = allSanFranData[allSanFranData['Season'] == season ][['Longitude', 'Latitude']].values
    lons, lats = map.to_pixels(points[:,1], points[:,0]) 
    ax2.scatter(lons, lats, marker='o', s=70.0,color=colors[season], alpha=0.3, label=seasons[season])
    ax2.legend()
    plt.show()

    #plt.plot(lons, lats, 'or', alpha = 0.7);
    #plt.scatter(allSanFranData[allSanFranData['Season'] == season ]['Longitude'],\
#		allSanFranData[allSanFranData['Season'] == season ]['Latitude'], marker = 'o', alpha = 0.1)

#points = allSanFranData[['Longitude', 'Latitude']].values
#min = allSanFranData[['Longitude', 'Latitude']].min()
#max = allSanFranData[['Longitude', 'Latitude']].max()

#print min
#print max

#xx, yy = np.mgrid[min[0]:max[0]:1000j, min[1]:max[1]:1000j]
#positions = np.vstack([xx.ravel(), yy.ravel()])
#values = np.vstack([points[0], points[1]])
#kernel = gaussian_kde(values)
#f = np.reshape(kernel(positions).T, xx.shape)

cnxn.close()
