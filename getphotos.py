import flickrapi

api_key = '56675a9ab1be04d06e950852977905ae'
secret_key = 'd9c16db695698cfe'
flickr = flickrapi.FlickrAPI(api_key, secret_key, cache=True)

#geo_context=2 means outdoors, lat='40.755815', lon='-73.986428' is times square (broadway & 42nd street) NYC
#min_taken_date='1420070400' means photo was taken, at earliest, after midnight of January 1st 2015 
photos = flickr.photos_search( lat='40.755815', lon='-73.986428', radius='0.01', min_taken_date='1420070400')

#Morgan Stanley, 1585 Broadway Ave
#New York, NY 10036
#40.755815, -73.986428

print len(photos[0])

for photo in photos[0]:
    print photo.attrib['title']
    photoInfo = flickr.photos_getInfo(photo_id=photo.attrib['id'])
    print "date taken: ", photoInfo[0][4].attrib['taken']
    #print photoInfo[0].attrib['dates']
    #for tag in photoInfo[u'tags'][0][u'tag']: 
	#print tag[u'text']

    photoLoc = flickr.photos_geo_getLocation(photo_id=photo.attrib['id'])
    print photoLoc[0][0].attrib['latitude']
    print photoLoc[0][0].attrib['longitude']
    #print photoLoc[0][0].attrib['date']
    photoSizes = flickr.photos_getSizes(photo_id=photo.attrib['id'])
    print photoSizes[0][1].attrib['source']
