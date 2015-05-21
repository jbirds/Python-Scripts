#!/usr/bin/python

'''Walks through the specified file system, scanning for all media files, and inserts or updates a record of
 each file into the SQL table.'''

__author__ = "Jason Wu"
__date__ = "12/19/2013"
__version__ = "2.0"
__email__= "me@jasonalvinwu.com"
__status__ = "Pre-Production"
__python_version__ = "2.7"
__license__ = "GPL"

import os
import datetime
import re
import logging
import mysql.connector
from mysql.connector import errorcode
import sqlauthenticator

keyword = "sqladmin"
path_data = ""
cnx = ""
cur = ""

class MySQLCursorDict(mysql.connector.cursor.MySQLCursor):  # creates a custom cursor
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None

def whatshere():                                     # returns a list of movie files in file system
    cur.execute("DELETE FROM table_name")  # deletes all data from table before writing to it
    for dirpath, dirnames, files in os.walk("/Volumes/Volume Name", topdown=True):
        for f in files:
            joinedFiles = os.path.join(dirpath, f)   # intelligently links files in file system with their directory paths
            match = re.search('(\.DS_Store|\.plist|\.zip|\.doc|\.psd|\.layout|\.fcp|\.par|\.pts|\CF+apchappl|\CF+avc1appl'
                              '|\.|digitalvaulttracker.py)$', joinedFiles)             #
            if not match and (joinedFiles.find("._") == -1): # filter out Mac index files and non-movie files
				splitfile = joinedFiles.rpartition("/")
				filename = splitfile[2]
				filename = re.sub("'", "''", filename)
				modifiedtime = os.path.getmtime(joinedFiles)
				filepath = re.sub("'", "''", joinedFiles)   # replaces apostrophes with double apostrophes to meet SQL insertion requirements
				insertion = ("INSERT INTO table_name (file_name, file_path, date_modified, date_ran) VALUES ('" + filename + "', '" + str(filepath) + "', '" + str(datetime.datetime.fromtimestamp(int(modifiedtime)).strftime('%Y-%m-%d %H:%M:%S')) + "','" + str(datetime.datetime.now()) + "')")
				cur.execute(insertion)
				cnx.commit()
try:
    result = sqlauthenticator.password(keyword)     # Obtains SQL user log-in information for that respective job
    userpass = result[0]
    schema = result[1]
    sqlhost = result[2]
    cnx = mysql.connector.connect(user=keyword, password=userpass, host=sqlhost, database=schema)
    cur = cnx.cursor(cursor_class=MySQLCursorDict)  # creates cursor that reads the SQL table
    whatshere()                                     # runs the whatshere() function that writes media files to DB
    cur.close()
    cnx.close()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logging.basicConfig(filename="ERROR.log", level=logging.INFO)
        logging.info(str(datetime.datetime.now()) + " : Username or password invalid.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        logging.basicConfig(filename="ERROR.log", level=logging.INFO)
        logging.info(str(datetime.datetime.now()) + " : Database does not exist.")
    else:
        print (err)
else:
    cnx.close()