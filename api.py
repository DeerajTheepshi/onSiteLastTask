import socket
import mimetypes
import MySQLdb
import hashlib
import re
import json

#Describe the client 
HOST = '0.0.0.0'
PORT = 9000

#Establish TCP connections using Ports
serSock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serSock.bind((HOST, PORT))
serSock.listen(0) #accept a maximum of only one request at a time
print('Listening on port %s ....' %PORT)
while True: 
	con, addr = serSock.accept() #accept requests from the client
	req = con.recv(1024).decode() #Recieve from the client
	print("REQUEST IS: ")
	print(req)
	print("-------------------------------------------------")

	#PARSE the request
	lines = req.split('\r\n')
	reqMethod = lines[0].split()[0]
	reqPath = lines[0].split()[1]
	content = ""

	print(reqPath)

	#GET REQUEST IS PLACED:
	if(reqMethod == "GET"):
		if(reqPath == "/getData"):
			fil = open('site.html');
			content += fil.read()
			fil.close()
		
			db = MySQLdb.connect("localhost","root","root","API")
			cursor = db.cursor()
			query = "SELECT * FROM SYSPROP"
			cursor.execute(query)
			data = cursor.fetchall()

			for row in data:
				content += "\n <tr><td>"+ str(row[0]) +"</td>"
				content += "<td>"+ row[1] +"</td>"
				content += "<td>"+ row[6] +"</td>"
				content += "<td>"+ row[2] +"</td>"			
				content += "<td>"+ row[3] +"</td>"
				content += "<td>"+ row[5] +"</td>"
				content += "<td>"+ row[4] +"</td></tr>"
			content += "</table>"
		
	#POST METHOD IS REQUESTED			
	if(reqMethod == "POST"):
		if(reqPath =="/postData"):
			vals = []
			reqPost = lines[-1]
			reqPost = reqPost[1:-1]
			reqList = reqPost.split(", \"".decode())
			for x in reqList:
				val = x.split(":")
				vals.append(val[1])
			db = MySQLdb.connect("localhost","root","root","API")
			cursor = db.cursor()
			query = "INSERT INTO SYSPROP (MEMORY, CPU_USAGE, SPACE, TIME, NETCOUNT, PROCESS) VALUES ('%s','%s','%s','%s','%s','%s');"%(vals[0],vals[1],vals[2],vals[3],vals[4],vals[5])
			print query;
			try:
				cursor.execute(query)
				db.commit()
			except:
				db.rollback()			
			print(vals)

	
	response = 'HTTP/1.0 200 OK\n'+'Content-type: text/html; charset=UTF-8\n\n'+content 
	#send the response to the client via the connection
	print("Response Sent:\n\n"+response+"\n\n------------------------------------------------------")
	con.sendall(response.encode())
	con.close()
serSock.close()


	
