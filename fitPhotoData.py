import MySQLdb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from sklearn.neighbors.kde import KernelDensity
import pickle
import smopy
import dbscanning

cnxn = MySQLdb.connect("localhost","root","golgo13","picturesdb") 
cursor = cnxn.cursor()
sql = "SELECT * FROM PhotosPittsburgh"

allData = pd.read_sql(sql, cnxn)
#someSanFranData = allSanFranData[allSanFranData['Longitude'] ]['all features']
print "Read the data from SQL"


points = allData[['Longitude', 'Latitude']].values

print points

clusteredPoints = dbscanning.display_clusters(points)
print clusteredPoints
returnedPoints = clusteredPoints[['Longitude', 'Latitude']].values
min = allData[['Longitude', 'Latitude']].min()
max = allData[['Longitude', 'Latitude']].max()

resolution = 300j
xx, yy = np.mgrid[min[0]:max[0]:resolution, min[1]:max[1]:resolution]
positions = np.vstack([xx.ravel(), yy.ravel()])
#values = np.vstack([points[:,0], points[:,1]])
values = np.vstack([returnedPoints[:,0], returnedPoints[:,1]])

#using scipy's gaussian kde
#kernel = gaussian_kde(values, bw_method='silverman')
#kernel = gaussian_kde(values, bw_method=0.15)
#f = np.reshape(kernel(positions).T, xx.shape)
#print "Finished getting gaussian kde via scipy!"

#using sci-kit learn's kde
#kde = KernelDensity(kernel='exponential', bandwidth=0.0000002).fit(values.T)
kde = KernelDensity(kernel='exponential', bandwidth=0.0003).fit(values.T)
#kde = KernelDensity(kernel = 'gaussian', bandwidth=0.0001).fit(values.T)
#kde = KernelDensity(kernel='tophat', bandwidth=0.01).fit(values.T)
log_dens = kde.score_samples(positions.T)
otherf = np.reshape(log_dens, xx.shape)
print "Finished getting exponential kde via scikit-learn!"

#print "Dimensions of f: ", f.shape
#print "Start from 1/3 way down, 1/4 way over from right...", f[33,75]
#for i in range(34):
#    print f[33+i,75]   
#print "Ending at 2/3 way down, 1/4 way over from right: ", f[66,75]

#print "Start from 1/3 way down, 3/4 way over from right...", f[33,25]
#for i in range(34):
#    print f[33+i,25]   
#print "Ending at 2/3 way down, 3/4 way over from right: ", f[66,25]

#map = smopy.Map((min[1],min[0]), (max[1],max[0]), z=13, margin=.1)
map = smopy.Map((min[1],min[0]), (max[1],max[0]), z=11, margin=.1)
#ax2= map.show_mpl();
x, y = map.to_pixels(points[:,1], points[:,0])
ax2 = map.show_mpl(figsize=(8, 6))
ax2.plot(x, y, ',b');


#fig = plt.figure()
#ax = fig.gca()
#ax.set_xlim(min[0], max[0])
#ax.set_ylim(min[1], max[1])

# Contourf plot with black bars
#cfset = ax.contourf(xx, yy, f, cmap='plasma')
#cset = ax.contour(xx, yy, f, colors='k')
#print "Levels: ", cset.levels
#print "Zmin: ", cset.zmin
#print "Zmax: ", cset.zmax

# Label plot
#ax.clabel(cset, inline=1, fontsize=10)
#ax.set_xlabel('Longitude')
#ax.set_ylabel('Latitude')
#ax.plot(points[:,0], points[:,1], ',r');
#plt.show()




#And now for the scikit-learn one!
fig = plt.figure()
ax = fig.gca()
ax.set_xlim(min[0], max[0])
ax.set_ylim(min[1], max[1])

# Contourf plot with black bars
cfset = ax.contourf(xx, yy, otherf, cmap='plasma')
cset = ax.contour(xx, yy, otherf, colors='k')
print "Levels: ", cset.levels
print "Zmin: ", cset.zmin
print "Zmax: ", cset.zmax

# Label plot
ax.clabel(cset, inline=1, fontsize=10)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Using exponential scikit-learn kernel')
ax.plot(points[:,0], points[:,1], ',r');
plt.show()


cnxn.close()


#pickle the variable f and the resolution
with open("data/kernel.pkl", 'wb') as file:
    pickle.dump(otherf, file)
with open("data/resolution.pkl", 'wb') as file:
    pickle.dump(resolution.imag, file)
with open("data/min.pkl", 'wb') as file:
    pickle.dump(min, file)
with open("data/max.pkl", 'wb') as file:
    pickle.dump(max, file)
with open("data/levels.pkl", 'wb') as file:
    pickle.dump(cset.levels, file)
with open("data/points.pkl", 'wb') as file:
    pickle.dump(returnedPoints, file)


