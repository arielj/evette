#!/usr/bin/python
# -*- coding: UTF-8 -*-

#Copyright (C) 2007 Adam Spencer - Free Veterinary Management Suite

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

##Contact: evetteproject@dsl.pipex.com

import MySQLdb
import dbmethods
import os
import miscmethods

def CheckServer(dbsettings):
	
	dbip = dbsettings.dbip
	dbuser = dbsettings.dbuser
	dbpass = dbsettings.dbpass
	
	try:
		if dbpass == "" or dbpass == "None" or dbpass == "False":
			
			connection = MySQLdb.connect(host=dbip, user=dbuser)
			
		else:
			connection = MySQLdb.connect(host=dbip, user=dbuser, passwd=dbpass)
		
		connection.close()
		success = True
		
	#except MySQLdb.Error, e:
		#print "dbip = ",dbip,", dbuser = ",dbuser,", dbpass = ",dbpass
		#print "db: CheckServer: error: %d: %s " % (e.args[0], e.args[1])
		#success = False
		
	except:
		success = False
	
	return success

def GetASMDBSettings():

        home = miscmethods.GetHome()

        jdbcsettings = home + "/.asm/jdbc.properties"

        inp = open(jdbcsettings, "r")

        filecontents = inp.readlines()

        inp.close()

        filecontentsstring = ""

        for a in filecontents:

                filecontentsstring = filecontentsstring + a

        filecontents = filecontentsstring.replace("\\", "")

        dbip = filecontents.split("://")[1].split("/")[0]

        #print "dbip detected as " + str(dbip)

        dbuser = filecontents.split("user=")[1].split("&")[0]

        #print "dbuser detected as " + str(dbuser)

        if filecontents.__contains__("password") == False:

                dbpass = False
        else:

                dbpass = filecontents.split("password=")[1].split("&")[0]

        #print "dbpass detected as " + str(dbpass)

        return (dbip, dbuser, dbpass)

def GetASMConnection():
	
	asmdbsettings = GetASMDBSettings()
	
	dbip = asmdbsettings[0]
	dbuser = asmdbsettings[1]
	dbpass = asmdbsettings[2]
	dbname = "asm"
	
	try:
		if dbpass == "" or str(dbpass) == "None" or str(dbpass) == "False":
			connection = MySQLdb.connect(host=dbip, user=dbuser, db=dbname)
		else:
			connection = MySQLdb.connect(host=dbip, user=dbuser, db=dbname, passwd=dbpass)
		
		try:
			connection.set_character_set("utf8")
		except:
			pass
		
	except MySQLdb.Error, e:
			
		print "db: GetConnection: error: %d: %s " % (e.args[0], e.args[1])
		connection = False
		
	except:
		connection = False
	
	return connection

def GetConnection(dbsettings, dbname="evette"):
	
	dbip = dbsettings.dbip
	dbuser = dbsettings.dbuser
	dbpass = dbsettings.dbpass
	
	try:
		if dbpass == "" or str(dbpass) == "None" or str(dbpass) == "False":
			connection = MySQLdb.connect(host=dbip, user=dbuser, db=dbname)
		else:
			connection = MySQLdb.connect(host=dbip, user=dbuser, db=dbname, passwd=dbpass)
		
		try:
			connection.set_character_set("utf8")
		except:
			pass
		
	#except MySQLdb.Error, e:
			
		#print "db: GetConnection: error: %d: %s " % (e.args[0], e.args[1])
		#success = False
		#connection = False
		
	except:
		connection = False
	
	return connection

def SendSQL(action, connection):
	
	#print "action = " + action
	
	cursor = connection.cursor()
	cursor.execute(action)
	output = cursor.fetchall()
	cursor.close()
	connection.commit()
	
	return output

def CreateDatabase(dbsettings):
	
	success = False
	dbip = dbsettings.dbip
	dbuser = dbsettings.dbuser
	dbpass = dbsettings.dbpass
	
	if dbpass == "" or dbpass == "None" or dbpass == "False":
		
		connection = MySQLdb.connect(host=dbip, user=dbuser)
		
	else:
		connection = MySQLdb.connect(host=dbip, user=dbuser, passwd=dbpass)
	
	action = "CREATE DATABASE evette"
	SendSQL(action, connection)
	connection.close()
	
	connection = GetConnection(dbsettings)
	
	#print "Creating all tables"
	
	dbmethods.CreateAllTables(connection)
	
	#print "All tables created"
	
	connection.close()
	
	success = True
	
	return success
