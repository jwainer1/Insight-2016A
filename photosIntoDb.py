import pandas as pd
import MySQLdb

filename = 'data/yfcc100m_dataset-9.csv'
chunkSize = 5000
totalLines = 0
#filename = 'data/sampleYfcc.csv'
columnNames = ['PhotoID', 'UserID', 'UserName', 'DateTaken', 'DateUpload', 'Device', 'Title', 'Description',\
		'UserTags', 'MachineTags', 'Longitude', 'Latitude', 'Accuracy', 'PageURL', 'DownURL',\
		'LicenseName', 'LicenseURL', 'ServerID', 'FarmID', 'Secret', 'SecretOrig', 'Ext', 'Marker']
reader = pd.read_csv(filename, sep='\t', header=None, names=columnNames, chunksize=chunkSize)
print "Properly read data into pandas!"
con=MySQLdb.connect("localhost","root","golgo13","picturesdb")

#read data into database in chunks, specifically targeting data from San Fran
for chunk in reader:
	print "putting in next ", chunkSize, " entries into table!"
	partOfChunk = chunk[(chunk['Longitude'] >= -80.0972) & (chunk['Longitude'] <= -79.8658) &
			(chunk['Latitude'] >= 40.3766) & (chunk['Latitude'] <= 40.4992)][columnNames]
	partOfChunk.to_sql(name='PhotosPittsburgh', con=con, if_exists = 'append', index=False, flavor='mysql')
	#chunk.to_sql(name='PhotosTest', con=con, if_exists = 'append', index=False, flavor='mysql')
	print "actually put in ", len(partOfChunk), " entries of chunk, and did so successfully!"
	totalLines += len(partOfChunk)
	print "we now have ", totalLines, " entries in database!"

#error is pandas.io.sql.DatabaseError: Execution failed on sql 'SELECT name FROM sqlite_master WHERE type='table' AND name=?;': not all arguments converted during string formatting

