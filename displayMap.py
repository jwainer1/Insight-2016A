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
    smallest_fraction = 1000000.0
    total_fraction = 0.0
    smallest = abs(f.min())
    f = f + smallest
    levels = levels + levels[0]
    numLevels = len(levels)
    last = numLevels-1
    for each_coord in path:
	#print "   each_coordinate in path: ", each_coord
	sloty = int( ((each_coord[1] - minimum[1]) / (maximum[1] - minimum[1])) * resolution )
	slotx = int( ((each_coord[0] - minimum[0]) / (maximum[0] - minimum[0])) * resolution )
	#if we're out of bounds, don't change the weight
	if ( (slotx >= (resolution)) | (slotx < 0) ) | ( (sloty >= (resolution)) | (sloty < 0) ):
	    #if ((each_coord[1] < 37.84) & (each_coord[1] > 37.7) & (each_coord[0] > 122.05) & (each_coord[0] < 122.3)): 
	    	#print "coordinate ", each_coord, " in slot ", slotx, " ", sloty, " will not have a modded weight!"
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
	    #make highly clustered areas with lighter weights, and not-as-highly clustered heavier weights
	    if (index >= levels[last]):
	        current_fraction = 1.0 / (math.pow((index/levels[last]) + 2.0,3.0) )
	    else:
   		current_fraction = math.pow((levels[last] / index) + 2.0, 3.0 )		
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
seasons = {0:'winter', 1:'spring', 2:'summer', 3:'fall'}

#*********************************************
for whichseason in range(0,4):
    directory = "data/" + seasons[whichseason] + "/"
    f = pickle.load(open(directory + "kernel.pkl", "rb" ) )
    resolution = pickle.load(open(directory + "resolution.pkl", "rb" ) )
    maximum = pickle.load(open(directory + "max.pkl", "rb" ) )
    minimum = pickle.load(open(directory + "min.pkl", "rb" ) )
    levels = pickle.load(open(directory + "levels.pkl", "rb" ) )
    points = pickle.load(open(directory + "clusteredpoints.pkl", "rb" ) )

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

    #pos1 = (40.455763, -79.938615)
    #pos1 = (40.444216, -79.966203)
    #pos1 = (40.436941, -79.980789)
    #pos1 = (40.440429, -79.988102)
    #pos1 = (40.434896, -79.989431)
    pos1 = (40.442899, -79.965823)
    #pos0 = (40.4585706667, -80.0297088333)
    #pos0 = (40.455703, -80.015191)
    #pos0 = (40.442347, -80.007369)
    #pos0 = (40.443432, -80.004672)
    pos0 = (40.457242, -80.029383)
    numModded = 0
    numNormal = 0
    # Compute the length of the road segments.
    for n0, n1 in longestGraph.edges_iter():
    	path = get_path(n0, n1, longestGraph)
    	distance = get_path_length(path)
    	longestGraph.edge[n0][n1]['distance'] = distance
    	longestGraph.edge[n0][n1]['changedDistance'] = \
	    get_new_weight(longestGraph,path,maximum,minimum,f,resolution,levels,distance)
    	if (longestGraph.edge[n0][n1]['changedDistance'] != distance):
	    numModded += 1
    	else:
	    numNormal += 1

    print "Modded weights: ", numModded, " non-modded: ", numNormal

    with open(directory + "graphModdedWeights.pkl", 'wb') as file:
    	pickle.dump(longestGraph, file)

longestGraphSummer = pickle.load(open("data/summer/graphModdedWeights.pkl", "rb" ) )
longestGraphWinter = pickle.load(open("data/winter/graphModdedWeights.pkl", "rb" ) )
nodes = np.array(longestGraph.nodes())
winterNodes = np.array(longestGraphWinter.nodes())
summerNodes = np.array(longestGraphSummer.nodes())
# Get the closest nodes in the graph.
pos0_i = np.argmin(np.sum((nodes[:,::-1] - pos0)**2, axis=1))
pos1_i = np.argmin(np.sum((nodes[:,::-1] - pos1)**2, axis=1))


# Compute the shortest path.
path = nx.shortest_path(longestGraph, 
                        source=tuple(nodes[pos0_i]), 
                        target=tuple(nodes[pos1_i]),
                        weight='distance')
changed_path_summer = nx.shortest_path(longestGraphSummer, 
                        source=tuple(nodes[pos0_i]), 
                        target=tuple(nodes[pos1_i]),
                        weight='changedDistance')
changed_path_winter= nx.shortest_path(longestGraphWinter, 
                        source=tuple(nodes[pos0_i]), 
                        target=tuple(nodes[pos1_i]),
                        weight='changedDistance')

print "Shortest path between points closest to ", pos0, " and ", pos1, " has ", len(path), " segments"
print "Summer shortest path between points closest to ", pos0, " and ", pos1, " has ", len(changed_path_summer), " segments"
print "Winter modded shortest path between points closest to ", pos0, " and ", pos1, " has ", len(changed_path_winter), " segments"

roads = pd.DataFrame([longestGraph.edge[path[i]][path[i + 1]] for i in range(len(path) - 1)], 
                     columns=['FULLNAME', 'MTFCC', 'RTTYP', 'distance'])
changed_roads_summer = pd.DataFrame([longestGraphSummer.edge[changed_path_summer[i]][changed_path_summer[i + 1]] for i in range(len(changed_path_summer) - 1)], 
                     columns=['FULLNAME', 'MTFCC', 'RTTYP', 'distance'])
changed_roads_winter = pd.DataFrame([longestGraphWinter.edge[changed_path_winter[i]][changed_path_winter[i + 1]] for i in range(len(changed_path_winter) - 1)], 
                     columns=['FULLNAME', 'MTFCC', 'RTTYP', 'distance'])


print roads
print "Distance of this shortest path: ", roads['distance'].sum()

print changed_roads_summer
print "Distance of this changed shortest path in autumn: ", changed_roads_summer['distance'].sum()

print changed_roads_winter
print "Distance of this changed shortest path in spring: ", changed_roads_winter['distance'].sum()


min = min(pos0,pos1)
max = max(pos0,pos1)
#map = smopy.Map(pos0, pos1, z=13, margin=.1)
map = smopy.Map((min[0],min[1]), (max[0],max[1]), z=12, margin=0.1)
#convert path to pixels to display it on Smopy map
linepath = get_full_path(path, longestGraph)
linechangedsummerpath = get_full_path(changed_path_summer, longestGraphSummer)
linechangedwinterpath = get_full_path(changed_path_winter, longestGraphWinter)

print linepath
with open("data/pathCoords.pkl", 'wb') as file:
    pickle.dump(linepath, file)

x, y = map.to_pixels(linepath[:,1], linepath[:,0])
xchangesummer, ychangesummer = map.to_pixels(linechangedsummerpath[:,1], linechangedsummerpath[:,0])
xchangewinter, ychangewinter = map.to_pixels(linechangedwinterpath[:,1], linechangedwinterpath[:,0])

#plt.figure(figsize=(6,6));
map.show_mpl();

summerpoints = pickle.load(open("data/summer/clusteredpoints.pkl", "rb" ) )
winterpoints = pickle.load(open("data/winter/clusteredpoints.pkl", "rb" ) )
thepoints = points[points['Season'] == 3][['Longitude', 'Latitude']].values
thesummerpoints = summerpoints[summerpoints['Season'] == 2][['Longitude', 'Latitude']].values
thewinterpoints = winterpoints[winterpoints['Season'] == 0][['Longitude', 'Latitude']].values
summerlons, summerlats = map.to_pixels(thesummerpoints[:,1], thesummerpoints[:,0])
winterlons, winterlats = map.to_pixels(thewinterpoints[:,1], thewinterpoints[:,0])
plt.plot(summerlons, summerlats, '.r', alpha = 0.4, label = "Fall points");
plt.plot(winterlons, winterlats, '.b', alpha = 0.4, label = "Winter points");
# Plot the itinerary.
plt.plot(x, y, '-k', lw=1.0, alpha = 0.7, label = "Shortest path");
plt.plot(xchangesummer, ychangesummer, '-r', lw=1.0, alpha = 0.7, label = "Summer path");
plt.plot(xchangewinter, ychangewinter, '-b', lw=1.0, alpha = 0.7, label = "Winter path");
# Mark our two positions.
plt.plot(x[0], y[0], 'ow', ms=5);
plt.plot(x[-1], y[-1], 'ok', ms=5);

plt.legend(loc=2,prop={'size':4})
#leg = plt.gca().get_legend()
#ltext  = leg.get_texts()  # all the text.Text instance in the legend
#plt.setp(ltext, fontsize='small') 


plt.show()
