#!/usr/bin/python

''' sqlauthentication.py: A universal script to be accessed by all other Python scripts accessing our SQL databases to
authenticate respective account credentials for each respective schema. This streamlines how we handle assigning script
access to our database.
'''

__author__ = "Jason Wu"
__date__ = "12/19/2013"
__version__ = "1.0"
__email__= "me@jasonalvinwu.com"
__status__ = "Pre-Production"
__python_version__ = "2.7"
__license__ = "GPL"

username = ""

def password(username):               # Returns a dictionary set for the username inserted (username, password, schema, DB server IP)
    return {
        "sqladmin":("12345Abc","Production", "8.8.8.8"),
        "regularuser":("6789Xyz", "Pre-Production", "8.8.8.8"),
        "thisoneguy":("AnotherDude1!", "TestDB", "8.8.8.7")
    }.get(username,)