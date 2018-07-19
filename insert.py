import sys
import MySQLdb

tableName = sys.argv[1]
fil = open("text.txt")
lines = fil.readlines()
fil.close()
lineNo = 1
for line in lines:
	vals = line.split(" ")
	col = len(vals)
	db = MySQLdb.connect("localhost","root","root","API")
	cursor = db.cursor()
	create = "CREATE TABLE "+tableName+"( "
	if(lineNo==1):
		for a in range(col):
			if(a+1!=col):
				create += vals[a] + " VARCHAR(50), "
			else:
				create += vals[a] + " VARCHAR(50));"	
	try:
		cursor.execute(create)
		db.commit()
	except:
		db.rollback()	
		var_string = ','.join('%s' for i in range(col))
		query = 'INSERT INTO '+tableName + ' VALUES (%s);' % var_string
		print(var_string)
		if(line!=1):
			try:
				cursor.execute(query,vals)
				db.commit()
			except:
				db.rollback()	
	line=2
