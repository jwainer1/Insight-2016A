import networkx as nx
import numpy as np
import pandas as pd
import json
import smopy
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import osm2NetworkX as osm
import sys
import pickle

#print sys.path

EARTH_R = 6372.8
longestGraph = []

def geocalc(lat0, lon0, lat1, lon1):
    """Return the distance (in km) between two points in 
    geographical coordinates."""
    lat0 = np.radians(lat0)
    lon0 = np.radians(lon0)
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    dlon = lon0 - lon1
    y = np.sqrt(
        (np.cos(lat1) * np.sin(dlon)) ** 2
         + (np.cos(lat0) * np.sin(lat1) 
         - np.sin(lat0) * np.cos(lat1) * np.cos(dlon)) ** 2)
    x = np.sin(lat0) * np.sin(lat1) + \
        np.cos(lat0) * np.cos(lat1) * np.cos(dlon)
    c = np.arctan2(y, x)
    return EARTH_R * c

def get_path_length(path):
    return np.sum(geocalc(path[1:,0], path[1:,1],
                          path[:-1,0], path[:-1,1]))

def get_path(n0, n1, longestGraph):
    """If n0 and n1 are connected nodes in the graph, this function
    return an array of point coordinates along the road linking
    these two nodes."""

    #print "contents of the json tag in the node thing: ", longestGraph.edge[n0][n1]
    #return np.array(json.loads(longestGraph.edge[n0][n1]['Json'])['coordinates'])
    return np.array(json.loads(longestGraph[n0][n1]['Json'])['coordinates'])
    #print longestGraph[n0][n1]
    #print 
    #return np.array(longestGraph.node[n0]['lat'], longestGraph.node[n0]['lon'], longestGraph.node[n1]['lat'], longestGraph.node[n1]['lon'])

def get_full_path(path, longestGraph):
    """Return the positions along a path."""
    p_list = []
    curp = None
    for i in range(len(path)-1):
        p = get_path(path[i], path[i+1], longestGraph)
        if curp is None:
            curp = p
        if np.sum((p[0]-curp)**2) > np.sum((p[-1]-curp)**2):
            p = p[::-1,:]
        p_list.append(p)
        curp = p[-1]
    return np.vstack(p_list)

def get_new_weight(longestGraph,path,maximum,minimum,f,resolution,levels,distance):
    smallest_fraction = 1.0
    total_fraction = 0.0
    smallest = abs(f.min())
    f = f + smallest
    for each_coord in path:
	#print "   each_coordinate in path: ", each_coord
	sloty = int( ((each_coord[1] - minimum[1]) / (maximum[1] - minimum[1])) * resolution )
	slotx = int( ((each_coord[0] - minimum[0]) / (maximum[0] - minimum[0])) * resolution )
	#if we're out of bounds, don't change the weight
	if ( (slotx >= (resolution)) | (slotx < 0) ) | ( (sloty >= (resolution)) | (sloty < 0) ):
	    if ((each_coord[1] < 37.84) & (each_coord[1] > 37.7) & (each_coord[0] > 122.05) & (each_coord[0] < 122.3)): 
	    	print "coordinate ", each_coord, " in slot ", slotx, " ", sloty, " will not have a modded weight!"
	    total_fraction += 1
	else:
	    #templevels = np.array(levels)
	    #offset = abs(templevels[0])
	    #templevels = templevels + offset
	    #interval = templevels[1] - templevels[0]
	    #templevels[(templevels - (f[sloty][slotx] + offset)) > 0.0] = -50000
	    #index = templevels.argmax()
	    #current_fraction = 1.0 / ((index + 1.0) * 100.0)
	    index = f[sloty][slotx]
	    current_fraction = 1.0 / (math.pow(index + 1.0,3.0) * 100.0 )
	    if current_fraction < smallest_fraction:
		smallest_fraction = current_fraction
	    #total_fraction = total_fraction + ( 1.0 / (math.pow(index + 1.0,3.0)) )
	    ##print "partial fraction given weight of coordinate: ", ( 1.0 / (math.pow(index + 1.0,3.0)) )
    #total_fraction = total_fraction / len(path)
    total_fraction = smallest_fraction
    ##print "original distance: ", distance
    #print "total fraction given weights: ", total_fraction
    #print "modified distance: ", distance * total_fraction
    return (distance * total_fraction)


mpl.rcParams['figure.dpi'] = mpl.rcParams['savefig.dpi'] = 300
#G = osm.read_osm("data/manhattan.osm")
#G=osm.download_osm(-74.0252, 40.6983, -73.9064, 40.8891)
#G = nx.read_shp("data/new-york_new-york_osm_roads.shp")
G = pickle.load(open("data/pitt_g.pkl", "rb" ) )
f = pickle.load(open("data/kernel.pkl", "rb" ) )
resolution = pickle.load(open("data/resolution.pkl", "rb" ) )
maximum = pickle.load(open("data/max.pkl", "rb" ) )
minimum = pickle.load(open("data/min.pkl", "rb" ) )
levels = pickle.load(open("data/levels.pkl", "rb" ) )
points = pickle.load(open("data/points.pkl", "rb" ) )

print maximum
print minimum
print levels
print f.shape

#get the largest connected subgraph
longestLength = 0
allSubgraphs = list(nx.connected_component_subgraphs(G.to_undirected()))
for graph in allSubgraphs:
    currentLength = len(graph)
    if currentLength > longestLength:
	longestLength = currentLength
	longestGraph = graph

print len(longestGraph)

pos1 = (40.491616, -80.010195)
#pos1 = (40.493989, -79.995309)
pos0 = (40.456656, -79.939095)

numModded = 0
numNormal = 0
# Compute the length of the road segments.
for n0, n1 in longestGraph.edges_iter():
    path = get_path(n0, n1, longestGraph)
    distance = get_path_length(path)
    longestGraph.edge[n0][n1]['distance'] = distance
    longestGraph.edge[n0][n1]['changedDistance'] = get_new_weight(longestGraph,path,maximum,minimum,f,resolution,levels,distance)
    if (longestGraph.edge[n0][n1]['changedDistance'] != distance):
	numModded += 1
    else:
	numNormal += 1

print "Modded weights: ", numModded, " non-modded: ", numNormal

with open("data/graphModdedWeights.pkl", 'wb') as file:
    pickle.dump(longestGraph, file)

nodes = np.array(longestGraph.nodes())
# Get the closest nodes in the graph.
pos0_i = np.argmin(np.sum((nodes[:,::-1] - pos0)**2, axis=1))
pos1_i = np.argmin(np.sum((nodes[:,::-1] - pos1)**2, axis=1))


# Compute the shortest path.
path = nx.shortest_path(longestGraph, 
                        source=tuple(nodes[pos0_i]), 
                        target=tuple(nodes[pos1_i]),
                        weight='distance')
changed_path = nx.shortest_path(longestGraph, 
                        source=tuple(nodes[pos0_i]), 
                        target=tuple(nodes[pos1_i]),
                        weight='changedDistance')

print "Shortest path between points closest to ", pos0, " and ", pos1, " has ", len(path), " segments"
print "Modded shortest path between points closest to ", pos0, " and ", pos1, " has ", len(changed_path), " segments"

roads = pd.DataFrame([longestGraph.edge[path[i]][path[i + 1]] for i in range(len(path) - 1)], 
                     columns=['FULLNAME', 'MTFCC', 'RTTYP', 'distance'])
changed_roads = pd.DataFrame([longestGraph.edge[changed_path[i]][changed_path[i + 1]] for i in range(len(changed_path) - 1)], 
                     columns=['FULLNAME', 'MTFCC', 'RTTYP', 'distance'])

print roads
print "Distance of this shortest path: ", roads['distance'].sum()

print changed_roads
print "Distance of this changed shortest path: ", changed_roads['distance'].sum()


#map = smopy.Map(pos0, pos1, z=13, margin=.1)
map = smopy.Map(pos0, pos1, z=12, margin=0.4)
#convert path to pixels to display it on Smopy map
linepath = get_full_path(path, longestGraph)
linechangedpath = get_full_path(changed_path, longestGraph)

print linepath
with open("data/pathCoords.pkl", 'wb') as file:
    pickle.dump(linepath, file)

x, y = map.to_pixels(linepath[:,1], linepath[:,0])
xchange, ychange = map.to_pixels(linechangedpath[:,1], linechangedpath[:,0])

#plt.figure(figsize=(6,6));
map.show_mpl();

lons, lats = map.to_pixels(points[:,1], points[:,0])
plt.plot(lons, lats, ',m');
# Plot the itinerary.
plt.plot(x, y, '-k', lw=1.5);
plt.plot(xchange, ychange, '-g', lw=1.5);
# Mark our two positions.
plt.plot(x[0], y[0], 'ob', ms=5);
plt.plot(x[-1], y[-1], 'or', ms=5);

plt.show()