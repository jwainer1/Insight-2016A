import flickrapi
import math
import time

api_key = '56675a9ab1be04d06e950852977905ae'
secret_key = 'd9c16db695698cfe'
flickr = flickrapi.FlickrAPI(api_key, secret_key, cache=True)

#geo_context=2 means outdoors, lat='40.755815', lon='-73.986428' is times square (broadway & 42nd street) NYC
#lat = '40.764650', lon = '-73.995601' is 11th ave and 48th street
#lat = '40.753811', lon = '-73.983801' is bryant park
#min_taken_date='1420070400' means photo was taken, at earliest, after midnight of January 1st 2015 
#photos = flickr.photos_search( lat='40.756615' , lon='-73.986428', radius='0.01', radius_units='mi', min_taken_date='1420070400')

#print len(photos[0]), " photos in a 0.01 mi radius of times square"



#photos = flickr.photos_search( lat='40.764650' , lon='-73.995601', radius='0.01', radius_units='mi', min_taken_date='1420070400')

#print len(photos[0]), " photos in a 0.01 mi radius of 11th ave and 48th street"

#photos = flickr.photos_search( lat = '40.753811', lon = '-73.983801', radius='0.01', radius_units='mi', min_taken_date='1420070400')

#print len(photos[0]), " photos in a 0.01 mi radius of the middle of bryant park"


#rasterize the island's photo spots in 0.02 mi increments, (direction perpendicular to the avenues is -28.9' below equator)
#and print the date/lat/long into a file

with open('data/photoData.csv','a') as tfout:
    #outer loop - go down the length of the island, along the avenues
    for length in range(0,8):
    	#start from 12th ave and 43rd st: 40.762807, -74.000634
	print "++++++++++++"
    	startLat = 40.762807 - (length * 0.0004 * math.cos(28.9 * math.pi / 180.0)) 
    	startLon = -74.000634 - (length * 0.0004 * math.sin(28.9 * math.pi / 180.0))
    	#inner loop - go down the width of the island, along the streets
        for width in range(0,116):
	    print "ooooooooooooo"
	    startLat -= (width * 0.0004 * math.cos(61.1 * math.pi / 180.0))
	    startLon += (width * 0.0004 * math.sin(61.1 * math.pi / 180.0))
	
	    photos = flickr.photos_search( lat=str(startLat) , lon=str(startLon), radius='0.01', radius_units='mi', min_taken_date='1420070400')
	    print "&&&&&& ", len(photos[0]), " photos in this small radius"
	    time.sleep(1)
	#photos = flickr.photos_search( lat='40.756615' , lon='-73.986428', radius='0.01', radius_units='mi', min_taken_date='1420070400')

	    for photo in photos[0]:
		print photo.attrib['title']
		photoInfo = flickr.photos_getInfo(photo_id=photo.attrib['id'])
		theDate = photoInfo[0][4].attrib['taken']
	        print "date taken: ", theDate
		time.sleep(1)
	        photoLoc = flickr.photos_geo_getLocation(photo_id=photo.attrib['id'])
		theLat = photoLoc[0][0].attrib['latitude']
		theLon = photoLoc[0][0].attrib['longitude']
    		print "lat = ", theLat, ".... lon = ", theLon

        	tfout.write("{},{},{}\n".format(theDate,theLat,theLon))
		time.sleep(1)
    #photoSizes = flickr.photos_getSizes(photo_id=photo.attrib['id'])
    #print photoSizes[0][1].attrib['source']
