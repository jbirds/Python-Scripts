#!/usr/bin/python

''' clearoldmediafiles.py: A script intended to clear out the current directory of all media files of given extensions
that have not been worked on in over a day. Logs in a MySQL database the success of the actions daily.
'''

import os
import datetime
import re
from pprint import pprint
from time import mktime
import glob
import mysql.connector
import socket
import logging
from mysql.connector import errorcode

class MySQLCursorDict(mysql.connector.cursor.MySQLCursor): # creates custom cursor
	def _row_to_python(self, rowdata, desc=None):
		row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
		if row:
			return dict(zip(self.column_names, row))
		return None
try:
	cnx = mysql.connector.connect(user='username', password='password', host='127.0.0.1', database='DATABASENAME')
	cur = cnx.cursor(cursor_class=MySQLCursorDict)		
	for dirpath, dirnames, files in os.walk(os.path.expanduser("~")):
		for file in files:
			curpath = os.path.join(dirpath, file)	       
			match = re.search('(\.mov|\.mp4|\.mpg|\.flv|\.avi|\.wmv|\.mpeg|\.f4v|\.m4v|\.mxf|\.ts|\.dv)$', file)
			create_date = str(datetime.datetime.now())
			ip_address = str(socket.gethostbyname(socket.gethostname()))
			computer_name = str(socket.gethostname())
			
			if match:
				print curpath
				file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
				if datetime.datetime.now() - file_modified > datetime.timedelta(hours=24):
					try:
						os.remove(curpath)	
					except OSError:
						status = "ERROR deleting file"
						insertion = ("INSERT INTO clear_media (create_date, file_path, status, ip_address, computer_name) VALUES ('" + create_date + "', '" + curpath + "', '" + status + "', '" + ip_address + "', '" + computer_name + "')")
						cur.execute(insertion)
						cnx.commit()
						continue

					status = "Successfully deleted!"
					insertion = ("INSERT INTO clear_media (create_date, file_path, status, ip_address, computer_name) VALUES ('" + create_date + "', '" + curpath + "', '" + status + "', '" + ip_address + "', '" + computer_name + "')")
					cur.execute(insertion)
					cnx.commit()

		
	status = "No (more) applicable files found to be deleted."
	insertion = ("INSERT INTO clear_media (create_date, status, ip_address, computer_name) VALUES ('" + create_date + "', '" + status + "', '" + ip_address + "', '" + computer_name + "')")
	cur.execute(insertion)
	cnx.commit()	
	cur.close()
	cnx.close()
					
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		logging.basicConfig(filename="ERRROR.log", level=logging.INFO)
		logging.info(str(datetime.datetime.now()) + " : Username or password invalid.")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		logging.basicConfig(filename="ERROR.log", level=logging.INFO)
		logging.info(str(datetime.datetime.now()) + " : Database does not exist.")
	else:
		logging.basicConfig(filename="ERROR.log", level=logging.INFo)
		logging.info(str(datetime.datetime.now()) + " : " + err)
else:
	cnx.close()
