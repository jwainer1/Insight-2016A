import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN

#whichType == 0, photo points
#whichType == 1, business points
def display_clusters(points, whichType):
    #do dbscan clustering
    #clusteredPoints = []
    #points = allSanFranData[['Longitude', 'Latitude']].values
    thepoints = points[['Longitude', 'Latitude']].values
    values = np.vstack([thepoints[:,0], thepoints[:,1]])

    #photo min_samples=6, busines min_samples=3
    if (whichType == 0):
	numsamples = 6
    else:
	numsamples = 3	
    db = DBSCAN(eps=0.001, min_samples=numsamples).fit(values.T)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    points['Cluster'] = labels.tolist()
    print "The labels for the x,y entries:", labels
    print "Num labels: ", len(labels)
    print "Max and min: ", max(labels), " ", min(labels)
    print points.head(10)

    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    print('Estimated number of clusters: %d' % n_clusters_)

    #graph clusters from DBSCAN with black as noise
    unique_labels = set(labels)
    colors = plt.cm.Set1(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
    	if k == -1:
            # Black used for noise.
            col = 'k'

    	class_member_mask = (labels == k)

    	xy = values.T[class_member_mask & core_samples_mask]
    	plt.plot(xy[:, 0], xy[:, 1], '.', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)

    	xy = values.T[class_member_mask & ~core_samples_mask]
    	plt.plot(xy[:, 0], xy[:, 1], '.', markerfacecolor=col,
                 markeredgecolor='k', markersize=10)
	#if k != -1:
	#    xy = values.T[class_member_mask]
	#    print xy
	#    somePoints = size
	#    somePoints =  xy[:,0]
	#    somePoints[:,1] =  xy[:,1]
 	#    print somePoints
	#    clusteredPoints.append(somePoints)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()
    
    myFrame = pd.DataFrame()

    for i in xrange(n_clusters_):
	theVals = values.T[labels == i]
	numEntries = theVals.shape[0]
	print "In cluster #", i, ": ", numEntries, " points"
	#theLabel = np.zeros((numEntries,1))
	#theLabel[:] = i
	toReturn = pd.DataFrame(theVals, columns=['Longitude','Latitude'])
	toReturn['Cluster'] = i
	#print "dataframe toReturn:\n", toReturn
	myFrame = myFrame.append(toReturn)
	#print "dataframe myFrame: ", myFrame
    #toReturn = [values.T[labels == i] for i in xrange(n_clusters_)]
    
    #return myFrame
    return points
