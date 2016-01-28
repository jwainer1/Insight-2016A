import MySQLdb
import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np
#from sklearn.cluster import DBSCAN
import dbscanning

#return specific parts of the date_taken feature as new feature

def date_extract(date_taken):
    #return word.split(',')[1].split('.')[0].strip()
    return date_taken.split(' ')[0].strip()

def time_extract(date_taken):
    #return word.split(',')[1].split('.')[0].strip()
    return date_taken.split(' ')[1].strip()

def month_extract(date_taken):
    return int(date_taken.split(' ')[0].split('-')[1])

def day_extract(date_taken):
    return int(date_taken.split(' ')[0].split('-')[2])

def year_extract(date_taken):
    return int(date_taken.split(' ')[0].split('-')[0])

#def season_extract(date_taken):
#    #return season as winter=0, spring = 1, summer = 2, fall = 3
#    #date_year = date_taken.split(' ')[0].strip()
#    month = int(date_taken.split(' ')[0].split('-')[1])
#    day = int(date_taken.split(' ')[0].split('-')[2])
#    #determine the season of date_taken based on equinoxes and solstices
#    #spring = March 20, summer = June 21, autumnal = September 22, winter = December 21
#    if (month < 3) | ((month == 3) & (day < 20)):
#	return 0
#    elif ((month >= 3) & (day >= 20)) & ((month <= 6) & (day < 21)):
#	return 1
#    elif ((month >= 6) & (day >= 21)) & ((month <= 9) & (day < 22)):
#	return 2
#    elif ((month >= 9) & (day >= 22)) & ((month <= 12) & (day < 21)):
#	return 3
#    elif ((month >= 12) & (day >= 21)):
#	return 0


cnxn = MySQLdb.connect("localhost","root","golgo13","picturesdb") 
cursor = cnxn.cursor()
sql = "SELECT * FROM PhotosPittsburgh"

allSanFranData = pd.read_sql(sql, cnxn)
allSanFranData['DayTaken'] = allSanFranData['DateTaken'].apply(day_extract)
allSanFranData['MonthTaken'] = allSanFranData['DateTaken'].apply(month_extract)
allSanFranData['YearTaken'] = allSanFranData['DateTaken'].apply(year_extract)

print allSanFranData['YearTaken'].describe()

dbscanning.display_clusters(allSanFranData[['Longitude', 'Latitude']].values)

#show all the points in all seasons
plt.scatter(allSanFranData['Longitude'], allSanFranData['Latitude'], marker = ',')
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("All photos")
plt.show()


#determine the season of date_taken based on equinoxes and solstices
#spring = March 20, summer = June 21, autumnal = September 22, winter = December 21
allSanFranData['Season'] = 4
allSanFranData.loc[ (allSanFranData['MonthTaken'] < 3) | \
		    ((allSanFranData['MonthTaken'] == 3) & (allSanFranData['DayTaken'] < 20)), 'Season'] = 0

allSanFranData.loc[ ((allSanFranData['MonthTaken'] == 3) & (allSanFranData['DayTaken'] >= 20)) |\
		    ((allSanFranData['MonthTaken'] > 3) & (allSanFranData['MonthTaken'] < 6)) |\
		    ((allSanFranData['MonthTaken'] == 6) & (allSanFranData['DayTaken'] < 21)), 'Season'] = 1

allSanFranData.loc[ ((allSanFranData['MonthTaken'] == 6) & (allSanFranData['DayTaken'] >= 21)) |\
		    ((allSanFranData['MonthTaken'] > 6) & (allSanFranData['MonthTaken'] < 9)) |\
		    ((allSanFranData['MonthTaken'] == 9) & (allSanFranData['DayTaken'] < 22)), 'Season'] = 2

allSanFranData.loc[ ((allSanFranData['MonthTaken'] == 9) & (allSanFranData['DayTaken'] >= 22)) |\
		    ((allSanFranData['MonthTaken'] > 9) & (allSanFranData['MonthTaken'] < 12)) |\
		    ((allSanFranData['MonthTaken'] == 12) & (allSanFranData['DayTaken'] < 21)), 'Season'] = 3

allSanFranData.loc[ (allSanFranData['MonthTaken'] == 12) & (allSanFranData['DayTaken'] >= 21), 'Season'] = 0


#print allSanFranData.head(10)

seasons = {0:'Winter', 1:'Spring', 2:'Summer', 3:'Fall'}

for season in range(0,4):
    plt.scatter(allSanFranData[allSanFranData['Season'] == season ]['Longitude'],\
		allSanFranData[allSanFranData['Season'] == season ]['Latitude'], marker = 'o', alpha = 0.1)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Distribution of photos in %s" % seasons[season])
    plt.show()

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
