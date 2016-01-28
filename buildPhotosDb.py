import pymysql as mdb
import csv

con = mdb.connect('localhost', 'root', 'golgo13', 'picturesdb') #host, user, password, #database
#fields in photo#.csv are:

#   0* Photo/video identifier
#   1* User NSID
#   2* User nickname
#   3* Date taken
#   4* Date uploaded
#   5* Capture device
#   6* Title
#   7* Description
#   8* User tags (comma-separated)
#   9* Machine tags (comma-separated)
#   10* Longitude
#   11* Latitude
#   12* Accuracy
#   13* Photo/video page URL
#   14* Photo/video download URL
#   15* License name
#   16* License URL
#   17* Photo/video server identifier
#   18* Photo/video farm identifier
#   19* Photo/video secret
#   20* Photo/video secret original
#   21* Photo/video extension original
#   22* Photos/video marker (0 = photo, 1 = video)

numEntries = 0
numAttemptEntries = 0
with open('data/yfcc100m_dataset-9.csv', 'r') as f:
    with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS Photos4_9")
    	cur.execute("CREATE TABLE Photos4_9(Id INT PRIMARY KEY AUTO_INCREMENT," + \
					"PhotoID INT," + \
					"UserID CHAR(50)," + \
					"UserName CHAR(50)," + \
					"DateTaken CHAR(25)," + \
					"DateUpload INT," + \
					"Device CHAR(50)," + \
					"Title TEXT," + \
					"Description TEXT," + \
					"UserTags TEXT," + \
					"MachineTags TEXT," + \
					"Longitude FLOAT," + \
					"Latitude FLOAT," + \
					"Accuracy INT," + \
					"PageURL CHAR(100)," + \
					"DownURL CHAR(100)," + \
					"LicenseName CHAR(100)," + \
					"LicenseURL CHAR(100)," + \
					"ServerID INT," + \
					"FarmID INT," + \
					"Secret CHAR(20)," + \
					"SecretOrig CHAR(20)," + \
					"Ext CHAR(5)," + \
					"Marker INT )")
	reader=csv.reader(f,delimiter='\t')
        for PhotoID,UserID,UserName,DateTaken,DateUpload,Device,Title,Description,UserTags,MachineTags,\
		Longitude,Latitude,Accuracy,PageURL,DownURL,LicenseName,LicenseURL,ServerID,FarmID,\
		Secret,SecretOrig,Ext,Marker in reader:
	    photoIDnum = long(PhotoID)
	    dateUploadNum = int(DateUpload)
	    print Longitude
	    lonNum = float(Longitude)
	    latNum = float(Latitude)
	    accNum = int(Accuracy)
	    servIDnum = int(ServerID)
	    farmIDnum = int(FarmID)
	    markNum = int(Marker) 

            insertStatement = """INSERT INTO Photos4_9(PhotoID, UserID, UserName, DateTaken, DateUpload, Device, 
				Title, Description, UserTags, MachineTags, Longitude, Latitude, Accuracy, PageURL, 
				DownURL, LicenseName, LicenseURL, ServerID, FarmID, Secret, SecretOrig, Ext, Marker) 
				VALUES('%d', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s', '%f', '%f', '%d', '%s', '%s',
					'%s', '%s', '%d', '%d', '%s', '%s', '%s', '%d')""" % \
					(photoIDnum,UserID,UserName,DateTaken,dateUploadNum,Device,Title,Description,\
					UserTags,MachineTags,lonNum,latNum,accNum,PageURL,DownURL,\
					LicenseName,LicenseURL,servIDnum,farmIDnum,Secret,SecretOrig,Ext,markNum)
	    try:
		numAttemptEntries += 1
	    	cur.execute(insertStatement)
		con.commit()
		numSuccessEntries += 1
		print "Successfully entered row into table!"
	    except:
		con.rollback()
#    cur.execute("INSERT INTO Writers(Name) VALUES('Jack London')")
#    cur.execute("INSERT INTO Writers(Name) VALUES('Honore de Balzac')")
#    cur.execute("INSERT INTO Writers(Name) VALUES('Lion Feuchtwanger')")
#    cur.execute("INSERT INTO Writers(Name) VALUES('Emile Zola')")
#    cur.execute("INSERT INTO Writers(Name) VALUES('Truman Capote')")
#    cur.execute("INSERT INTO Writers(Name) VALUES('Terry Pratchett')")
#con.commit()

#with con: 
#    cur = con.cursor()
#    cur.execute("SELECT * FROM Writers")
#    rows = cur.fetchall()
#    for row in rows:
#        print row

cur.close()
con.close()
print numAttemptEntries, " attempted entries, and ", numSuccessEntries, " successful entries!"

