import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt

#read rocks versus mines data into pandas data frame
filename = 'data/photoData.csv'
photoLocations = pd.read_csv(filename)
numEntries = photoLocations['date'].count()

#plot lat/lon locations with semi-opaque points
plt.scatter(photoLocations['lon'], photoLocations['lat'], alpha=0.5)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
