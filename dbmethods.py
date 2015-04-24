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

import db
import miscmethods
import datetime
import dbupdates
import sys
import MySQLdb
from models import *

def GetLabel(localsettings, field):
	
	return  localsettings.dictionary[field][localsettings.language]

def CreateVersionTable(connection):
	
	action = "CREATE TABLE version (ID int unsigned not null auto_increment primary key, VersionNo varchar(10))"
	db.SendSQL(action, connection)
	
	versionno = dbupdates.GetCurrentVersion()
	
	action = "INSERT INTO version (VersionNo) VALUES (\'" + versionno + "\')"
	db.SendSQL(action, connection)

def CreateAnimalTable(connection):
	
	action = "CREATE TABLE animal(ID int unsigned not null auto_increment primary key, OwnerID int, Name varchar(20) CHARACTER SET utf8, Sex int, Species varchar(20) CHARACTER SET utf8, Breed varchar(20) CHARACTER SET utf8, Colour varchar(20) CHARACTER SET utf8, DOB varchar(10) CHARACTER SET utf8, Comments text CHARACTER SET utf8, Neutered int, ChipNo varchar(20), ChangeLog text CHARACTER SET utf8, IsDeceased int, DeceasedDate date, CauseOfDeath text CHARACTER SET utf8, ASMRef varchar(10))"
	db.SendSQL(action, connection)

def WriteToAnimalTable(connection, animaldata):
	
	ID = animaldata.ID
	OwnerID = animaldata.ownerid
	Name = animaldata.name
	Sex = animaldata.sex
	Species = animaldata.species
	Breed = animaldata.breed
	Colour = animaldata.colour
	DOB = animaldata.dob
	Comments = miscmethods.ValidateEntryString(animaldata.comments)
	Neutered = animaldata.neutered
	ChipNo = animaldata.chipno
	IsDeceased = animaldata.deceased
	DeceasedDate = animaldata.deceaseddate
	CauseOfDeath = animaldata.causeofdeath
	ASMRef = animaldata.asmref
	
	fields = (ID, OwnerID, Name, Sex, Species, Breed, Colour, DOB, Comments, Neutered, ChipNo)
	
	if ID != False:
		
		action = "REPLACE INTO animal (ID, OwnerID, Name, Sex, Species, Breed, Colour, DOB, Comments, Neutered, ChipNo, ChangeLog, IsDeceased, DeceasedDate, CauseOfDeath, ASMRef) VALUES ( " + str(fields[0]) + ", " + str(fields[1]) + ", \'" + fields[2] + "\', " + str(fields[3]) + ", \'" + fields[4] + "\', \'" + fields[5] + "\', \'" + fields[6] + "\', \'" + fields[7] + "\', \'" + fields[8] + "\', " + str(fields[9]) + ", \'" + fields[10] + "\', \'" + animaldata.changelog + "\', " + str(IsDeceased) + ", \'" + str(DeceasedDate) + "\', \'" + CauseOfDeath + "\', \'" + ASMRef + "\' )"
		
		#print action
		
		db.SendSQL(action, connection)
	
	else:
		
		action = "INSERT INTO animal (OwnerID, Name, Sex, Species, Breed, Colour, DOB, Comments, Neutered, ChipNo, ChangeLog, IsDeceased, DeceasedDate, CauseOfDeath, ASMRef) VALUES ( " + str(fields[1]) + ", \'" + fields[2] + "\', " + str(fields[3]) + ", \'" + fields[4] + "\', \'" + fields[5] + "\', \'" + fields[6] + "\', \'" + fields[7] + "\', \'" + fields[8] + "\', " + str(fields[9]) + ", \'" + fields[10] + "\', \'" + animaldata.changelog + "\', " + str(IsDeceased) + ", \'" + str(DeceasedDate) + "\', \'" + CauseOfDeath + "\', \'" + ASMRef + "\' )"
		
		db.SendSQL(action, connection)
		action = "SELECT ID FROM animal"
		ID = db.SendSQL(action, connection)[-1][0]
	
	animaldata.ID = ID

def CreateClientTable(connection):
	
	action = "CREATE TABLE client(ID int unsigned not null auto_increment primary key, ClientTitle varchar(10), ClientForenames varchar(30), ClientSurname varchar(30), ClientAddress varchar(250), ClientPostcode varchar(10), ClientHomeTelephone varchar(20), ClientMobileTelephone varchar(20), ClientWorkTelephone varchar(20), ClientEmailAddress varchar(50), ClientComments text, ChangeLog text, PhonePermissions int)"
	db.SendSQL(action, connection)

def WriteToClientTable(connection, clientdata):
	
	ID = clientdata.ID
	ClientTitle = clientdata.title
	ClientForenames = clientdata.forenames
	ClientSurname = clientdata.surname
	ClientAddress = clientdata.address
	ClientPostcode = clientdata.postcode
	ClientHomeTelephone = clientdata.hometelephone
	ClientMobileTelephone = clientdata.mobiletelephone
	ClientWorkTelephone = clientdata.worktelephone
	ClientPhonePermissions = clientdata.phonepermissions
	ClientEmailAddress = clientdata.emailaddress
	ClientComments = miscmethods.ValidateEntryString(clientdata.comments)
	
	#print "saving comments = " + ClientComments + " " + str(ClientComments.__class__)
	
	fields = (ID, ClientTitle, ClientForenames, ClientSurname, ClientAddress, ClientPostcode, ClientHomeTelephone, ClientMobileTelephone, ClientWorkTelephone, ClientEmailAddress, ClientComments, ClientPhonePermissions)
	
	if ID != False:
		
		action = "SELECT * FROM client WHERE ID = " + str(ID) + ""
		results = db.SendSQL(action, connection)
		
		newfields = []
		
		for a in range(0, len(fields)):
			
			if fields[a] == False:
				
				newfields.append(results[0][a])
				
			else:
				
				newfields.append(fields[a])
		action = "REPLACE INTO client (ID, ClientTitle, ClientForenames, ClientSurname, ClientAddress, ClientPostcode, ClientHomeTelephone, ClientMobileTelephone, ClientWorkTelephone, ClientEmailAddress, ClientComments, ChangeLog, PhonePermissions) VALUES ( " + str(newfields[0]) + ", \'" + newfields[1] + "\', \'" + newfields[2] + "\', \'" + newfields[3] + "\', \'" + newfields[4] + "\', \'" + newfields[5] + "\', \'" + newfields[6] + "\', \'" + newfields[7] + "\', \'" + newfields[8] + "\', \'" + newfields[9] + "\', \'" + newfields[10] + "\', \'" + clientdata.changelog + "\', " + str(clientdata.phonepermissions) + ")"
		
		#print action
		
		db.SendSQL(action, connection)
	
	else:
		
		newfields = fields
		
		action = "INSERT INTO client (ClientTitle, ClientForenames, ClientSurname, ClientAddress, ClientPostcode, ClientHomeTelephone, ClientMobileTelephone, ClientWorkTelephone, ClientEmailAddress, ClientComments, ChangeLog, PhonePermissions) VALUES ( \'" + newfields[1] + "\', \'" + newfields[2] + "\', \'" + newfields[3] + "\', \'" + newfields[4] + "\', \'" + newfields[5] + "\', \'" + newfields[6] + "\', \'" + newfields[7] + "\', \'" + newfields[8] + "\', \'" + newfields[9] + "\', \'" + newfields[10] + "\', \'" + clientdata.changelog + "\', " + str(clientdata.phonepermissions) + ")"
		
		db.SendSQL(action, connection)
		
		action = "SELECT LAST_INSERT_ID() FROM client"
		ID = db.SendSQL(action, connection)[0][0]
	
	clientdata.ID = ID

def CreateAppointmentTable(connection):
	
	action = "CREATE TABLE appointment(ID int unsigned not null auto_increment primary key, AnimalID int, OwnerID int, Date date, Time time, AppointmentReason text, Arrived int, WithVet int, Problem text, Notes text, Plan text, Done int, Operation int, Vet varchar(20), ChangeLog text, Staying int, ArrivalTime time)"
	db.SendSQL(action, connection)

def WriteToAppointmentTable(connection, appointmentdata):
	
	fields = (appointmentdata.ID, appointmentdata.animalid, appointmentdata.ownerid, appointmentdata.date, appointmentdata.time, miscmethods.ValidateEntryString(appointmentdata.reason), appointmentdata.arrived, appointmentdata.withvet, miscmethods.ValidateEntryString(appointmentdata.problem), miscmethods.ValidateEntryString(appointmentdata.notes), miscmethods.ValidateEntryString(appointmentdata.plan), appointmentdata.done, appointmentdata.operation, appointmentdata.vet)
	
	fieldnames = ("ID", "AnimalID", "OwnerID", "Date", "Time", "AppointmentReason", "Arrived", "WithVet", "Problem", "Notes", "Plan", "Done", "Operation", "Vet")
	
	if appointmentdata.ID != False:
		
		if appointmentdata.arrivaltime == None:
			
			arrivaltime = "NULL"
			
		else:
			
			arrivaltime = "\"" + str(appointmentdata.arrivaltime) + "\""
		
		action = "REPLACE INTO appointment (ID, AnimalID, OwnerID, Date, Time, AppointmentReason, Arrived, WithVet, Problem, Notes, Plan, Done, Operation, Vet, ChangeLog, Staying, ArrivalTime) VALUES ( " + str(fields[0]) + ", " + str(fields[1]) + ", " + str(fields[2]) + ", \'" + str(fields[3]) + "\', \'" + str(fields[4]) + "\', \'" + fields[5] + "\', " + str(fields[6]) + ", " + str(fields[7]) + ", \'" + fields[8] + "\', \'" + fields[9] + "\', \'" + fields[10] + "\', " + str(fields[11]) + ", " + str(fields[12]) + ", \'" + appointmentdata.vet + "\', \'" + appointmentdata.changelog + "\', " + str(appointmentdata.staying) + ", " + arrivaltime + " )"
		db.SendSQL(action, connection)
		
	
	else:
		
		action = "INSERT INTO appointment (AnimalID, OwnerID, Date, Time, AppointmentReason, Arrived, WithVet, Problem, Notes, Plan, Done, Operation, Vet, ChangeLog, Staying, ArrivalTime) VALUES ( " + str(fields[1]) + ", " + str(fields[2]) + ", \'" + str(fields[3]) + "\', \'" + str(fields[4]) + "\', \'" + fields[5] + "\', " + str(fields[6]) + ", " + str(fields[7]) + ", \'" + fields[8] + "\', \'" + fields[9] + "\', \'" + fields[10] + "\', " + str(fields[11]) + ", " + str(fields[12]) + ", \'" + appointmentdata.vet + "\', \'" + appointmentdata.changelog + "\', " + str(appointmentdata.staying) + ", NULL )"
		db.SendSQL(action, connection)
		action = "SELECT LAST_INSERT_ID() FROM appointment"
		appointmentdata.ID = db.SendSQL(action, connection)[0][0]
	

def CreateMedicationTables(connection):
	
	action = "CREATE TABLE medication (ID int unsigned not null auto_increment primary key, Name varchar(50), Description varchar(250), Unit varchar(20), BatchNo varchar(30), CurrentPrice int, ChangeLog text, ReOrderNo int, ExpiryDate date, Type int, CostPrice int)"## -- Types(0 = medication, 1 = vaccination, 2 = consumable, 3 = shop, 4 = chip)
	db.SendSQL(action, connection)
	
	action = "CREATE TABLE medicationin (ID int unsigned not null auto_increment primary key, MedicationID int, Date date, Amount int, BatchNo varchar(30), Expires date, WhereFrom varchar(50), ChangeLog text)"
	db.SendSQL(action, connection)
	
	action = "CREATE TABLE medicationout (ID int unsigned not null auto_increment primary key, MedicationID int, Date date, Amount int, BatchNo varchar(30), WhereTo varchar(50), AppointmentID int, ChangeLog text, NextDue date)"
	db.SendSQL(action, connection)

def WriteToMedicationTable(connection, medicationdata):
	
	ID = medicationdata.ID
	name = medicationdata.name
	description = medicationdata.description
	unit = medicationdata.unit
	batchno = medicationdata.batchno
	price = medicationdata.price
	changelog = medicationdata.changelog
	reorderno = medicationdata.reorderno
	expiry = medicationdata.expirydate
	if str(expiry) == "" or str(expiry) == "None":
                expiry = "0000-00-00"
	consumabletype = medicationdata.consumabletype
	costprice = medicationdata.costprice
	
	if ID != False:
		
		action = "REPLACE INTO medication (ID, Name, Description, Unit, BatchNo, CurrentPrice, ChangeLog, ReOrderNo, ExpiryDate, Type, CostPrice) VALUES ( " + str(ID) + ", \'" + name + "\', \'" + description + "\', \'" + unit + "\', \'" + batchno + "\', \'" + str(price) + "\', \'" + changelog + "\', " + str(reorderno) + ", \"" + expiry + "\", " + str(consumabletype) + ", " + str(costprice) + " )"
		db.SendSQL(action, connection)
		ID = ID
	
	else:
		
		action = "INSERT INTO medication (Name, Description, Unit, BatchNo, CurrentPrice, ChangeLog, ReOrderNo, ExpiryDate, Type, CostPrice) VALUES ( \'" + name + "\', \'" + description + "\', \'" + unit + "\', \'" + batchno + "\', \'" + str(price) + "\', \'" + changelog + "\', " + str(reorderno) + ", \"" + expiry + "\", " + str(consumabletype) + ", " + str(costprice) + " )"
		db.SendSQL(action, connection)
		
		action = "SELECT ID FROM medication"
		ID = db.SendSQL(action, connection)[-1][0]
	
	medicationdata.ID = ID

def WriteToMedicationInTable(connection, medicationindata):
	
	#fields = (ID, MedicationID, Date, Amount, BatchNo, Expires, WhereFrom)
	
	ID = medicationindata.ID
	medicationid = medicationindata.medicationid
	date = medicationindata.date
	amount = medicationindata.amount
	batchno = medicationindata.batchno
	expires = medicationindata.expires
	if expires == None:
		expires = "0000-00-00"
	wherefrom = medicationindata.wherefrom
	changelog = medicationindata.changelog
	
	if ID != False:
		
		action = "REPLACE INTO medicationin (ID, MedicationID, Date, Amount, BatchNo, Expires, WhereFrom, ChangeLog) VALUES ( " + str(ID) + ", " + str(medicationid) + ", \'" + date + "\', " + str(amount) + ", \'" + batchno + "\', \'" + expires + "\', \'" + wherefrom + "\', \'" + changelog + "\' )"
		db.SendSQL(action, connection)
	
	else:
		
		action = "INSERT INTO medicationin (MedicationID, Date, Amount, BatchNo, Expires, WhereFrom, ChangeLog) VALUES ( " + str(medicationid) + ", \'" + date + "\', " + str(amount) + ", \'" + batchno + "\', \'" + expires + "\', \'" + wherefrom + "\', \'" + changelog + "\' )"
		db.SendSQL(action, connection)
		action = "SELECT ID FROM medicationin"
		ID = db.SendSQL(action, connection)[-1][0]
		medicationindata.ID = ID

def WriteToMedicationOutTable(connection, medicationoutdata):
	
	#fields = (ID, MedicationID, Date, Amount, BatchNo, WhereTo, AppointmentID)
	
	ID = medicationoutdata.ID
	medicationid = medicationoutdata.medicationid
	date = medicationoutdata.date
	amount = medicationoutdata.amount
	batchno = medicationoutdata.batchno
	whereto = medicationoutdata.whereto
	appointmentid = medicationoutdata.appointmentid
	changelog = medicationoutdata.changelog
	nextdue = medicationoutdata.nextdue
	if nextdue == None:
		nextdue = "0000-00-00"
	
	if ID != False:
		
		action = "REPLACE INTO medicationout (ID, MedicationID, Date, Amount, BatchNo, WhereTo, AppointmentID, ChangeLog, NextDue) VALUES ( " + str(ID) + ", " + str(medicationid) + ", \'" + date + "\', \'" + str(amount) + "\', \'" + batchno + "\', \'" + whereto + "\', " + str(appointmentid) + ", \'" + changelog + "\', \'" + str(nextdue) + "\' )"
		
		db.SendSQL(action, connection)
	
	else:
		
		action = "INSERT INTO medicationout (MedicationID, Date, Amount, BatchNo, WhereTo, AppointmentID, ChangeLog, NextDue) VALUES ( " + str(medicationid) + ", \'" + date + "\', \'" + str(amount) + "\', \'" + batchno + "\', \'" + whereto + "\', " + str(appointmentid) + ", \'" + changelog + "\', \'" + str(nextdue) + "\' )"
		
		db.SendSQL(action, connection)
		
		action = "SELECT ID FROM medicationout"
		ID = db.SendSQL(action, connection)[-1][0]
		medicationoutdata.ID = ID
	
	

def CreateProceduresTable(connection):
	
	action = "CREATE TABLE procedures (ID int unsigned not null auto_increment primary key, Name varchar(50), Description text, Price int)"
	db.SendSQL(action, connection)
	
	standardprocedures = ( ("General Checkover", "Full body check", 500), ("Clip Claws", "Claws clipped", 250) )
	
	for a in standardprocedures:
		
		action = "INSERT INTO procedures (Name, Description, Price) VALUES (\'" + a[0] + "\', \'" + a[1] + "\', " + str(a[2]) + ")"
		db.SendSQL(action, connection)
	
def WriteToProceduresTable(connection, ID=False, Name=False, Description=False, Price=False):
	
	fields = (ID, Name, Description, Price)
	
	if ID != False:
		
		action = "REPLACE INTO procedures (ID, Name, Description, Price) VALUES ( " + str(fields[0]) + ", \'" + str(fields[1]) + "\', \'" + fields[2] + "\', \'" + fields[3] + "\' )"
		db.SendSQL(action, connection)
		ID = fields[0]
	
	else:
		
		action = "INSERT INTO procedures ( Name, Description, Price) VALUES ( \'" + str(fields[1]) + "\', \'" + fields[2] + "\', \'" + fields[3] + "\' )"
		db.SendSQL(action, connection)
		action = "SELECT ID FROM procedures"
		ID = db.SendSQL(action, connection)[-1][0]
	
	return ID

def CreateReceiptTable(connection):
	
	#Types are: 0 = medication, 1 = procedure, 2 = vaccination, 3 = manual, 4 = payment
	
	action = "CREATE TABLE receipt (ID int unsigned not null auto_increment primary key, Date date, Description varchar(100), Price int, Type int, TypeID int, AppointmentID int, ChangeLog text)"
	db.SendSQL(action, connection)

def WriteToReceiptTable(connection, ID, Date, Description, Price, Type, TypeID, AppointmentID, userid):
	
	fields = (ID, Date, Description, Price, Type, TypeID, AppointmentID)
	
	currenttime = datetime.datetime.today().strftime("%x %X")
	
	if ID != False:
		
		action = "SELECT ChangeLog FROM receipt WHERE ID = " + str(ID)
		changelog = db.SendSQL(action, connection)[0][0]
		
		changelog = currenttime + "%%%" + str(userid) + "$$$" + changelog
		
		action = "REPLACE INTO receipt (ID, Date, Description, Price, Type, TypeID, AppointmentID, ChangeLog) VALUES ( " + str(fields[0]) + ", \'" + str(fields[1]) + "\', \'" + fields[2] + "\', " + str(fields[3]) + ", " + str(fields[4]) + ", " + str(fields[5]) + ", " + str(fields[6]) + ", \'" + changelog + "\' )"
		db.SendSQL(action, connection)
		ID = fields[0]
	
	else:
		
		changelog = currenttime + "%%%" + str(userid)
		
		action = "INSERT INTO receipt (Date, Description, Price, Type, TypeID, AppointmentID, ChangeLog) VALUES ( \'" + str(fields[1]) + "\', \'" + fields[2] + "\', " + str(fields[3]) + ", " + str(fields[4]) + ", " + str(fields[5]) + ", " + str(fields[6]) + ", \'" + changelog + "\' )"
		db.SendSQL(action, connection)
		
		action = "SELECT ID FROM receipt"
		ID = db.SendSQL(action, connection)[-1][0]
	
	
	
	return ID

def CreateLookupTables(connection):
	
	action = "CREATE TABLE species (ID int unsigned not null auto_increment primary key, SpeciesName varchar(20))"
	db.SendSQL(action, connection)
	
	defaultspecies = ( "Dog", "Cat", "Rabbit", "Ferret" )
	
	for a in range(0, len(defaultspecies)):
		action = "INSERT INTO species (SpeciesName) VALUES (\'" + defaultspecies[a] + "\')"
		db.SendSQL(action, connection)
	
	action = "CREATE TABLE breed (ID int unsigned not null auto_increment primary key, BreedName varchar(20), species varchar(20))"
	db.SendSQL(action, connection)
	
	defaultbreeds = ( "Crossbreed", "SH Dom", "LH Dom", "SLH Dom" )
	
	for a in range(0, len(defaultbreeds)):
		action = "INSERT INTO breed (BreedName) VALUES (\'" + defaultbreeds[a] + "\')"
		db.SendSQL(action, connection)
	
	action = "CREATE TABLE colour (ID int unsigned not null auto_increment primary key, ColourName varchar(20))"
	db.SendSQL(action, connection)
	
	defaultcolours = ( "Black", "Black and White", "Black and Tan", "White", "White and Black", "White and Torti", "White and Ginger", "White and Tan", "Torti", "Torti and White", "Tabby", "Tabby and Torti", "Ginger", "Ginger and White" )
	
	for a in range(0, len(defaultcolours)):
		action = "INSERT INTO colour (ColourName) VALUES (\'" + defaultcolours[a] + "\')"
		db.SendSQL(action, connection)
	
	action = "CREATE TABLE reason (ID int unsigned not null auto_increment primary key, ReasonName varchar(200))"
	db.SendSQL(action, connection)

def CreateUserTable(connection):
	
	action = "CREATE TABLE user (ID int unsigned not null auto_increment primary key, Name varchar(20), Password varchar(10), Position varchar(50), Permissions varchar(50), mon_from varchar(4), mon_to varchar(4), tue_from varchar(4), tue_to varchar(4), wed_from varchar(4), wed_to varchar(4), thu_from varchar(4), thu_to varchar(4), fri_from varchar(4), fri_to varchar(4), sat_from varchar(4), sat_to varchar(4), sun_from varchar(4), sun_to varchar(4))"
	db.SendSQL(action, connection)
	action = "INSERT INTO user (Name, Password, Position, Permissions) VALUES (\'user\', \'letmein\', \'Manager\', \'111$11$111$11$11$11$11$111$11110$111\')"
	db.SendSQL(action, connection)

def WriteToUserTable(connection, ID, name, password, position, permissions, schedules):
	
	fields = "Name, Password, Position, Permissions, mon_from, mon_to, tue_from, tue_to, wed_from, wed_to, thu_from, thu_to, fri_from, fri_to, sat_from, sat_to, sun_from, sun_to"
	
	values = name + "\', \'" + password + "\', \'" + position + "\', \'" + permissions + "\', \'" + schedules['mon']['from'] + "\', \'" + schedules['mon']['to'] + "\', \'" + schedules['tue']['from'] + "\', \'" + schedules['tue']['to'] + "\', \'" + schedules['wed']['from'] + "\', \'" + schedules['wed']['to'] + "\', \'" + schedules['thu']['from'] + "\', \'" + schedules['thu']['to'] + "\', \'" + schedules['fri']['from'] + "\', \'" + schedules['fri']['to'] + "\', \'" + schedules['sat']['from'] + "\', \'" + schedules['sat']['to'] + "\', \'" + schedules['sun']['from'] + "\', \'" + schedules['sun']['to']
	
	if ID == False:
		action = "INSERT INTO user (" + fields + ") VALUES (\'" + values + "\')"
	else:
		action = "REPLACE INTO user (ID, " + fields + ") VALUES (" + str(ID) + ", \'" + values + "\')"
	db.SendSQL(action, connection)

def CreateSettingsTable(connection):
	
	action = "CREATE TABLE settings (ID int unsigned not null auto_increment primary key, PracticeName varchar(100), OpenFrom varchar(10), OpenTo varchar(10), OperationTime varchar(10), PracticeAddress varchar(250), PracticePostcode varchar(10), PracticeTelephone varchar(20), PracticeEmail varchar(250), PracticeWebsite varchar(250), ShelterID int, MarkupMultiplyBy varchar(10), MarkupRoundTo int, ASMVaccinationID int, PrescriptionFee int, handle_rota_by_day int DEFAULT 1, startup_size varchar(9))"
	db.SendSQL(action, connection)
	
	action = "INSERT INTO settings (PracticeName, OpenFrom, OpenTo, OperationTime, PracticeAddress, PracticePostcode, PracticeTelephone, PracticeEmail, PracticeWebsite, ShelterID, MarkupMultiplyBy, MarkupRoundTo, ASMVaccinationID, PrescriptionFee) VALUES (\'Unnamed Surgery\', \'09:00\', \'17:00\', \'09:00\', \"\", \"\", \"\", \"\", \"\", 0, \"1.175\", 5, 0, 0)"
	db.SendSQL(action, connection)

def CreateStaffTable(connection):
	
	action = "CREATE TABLE staff (ID int unsigned not null auto_increment primary key, Name varchar(20), Date date, Position varchar(20), TimeOn varchar(20), TimeOff varchar(20), Operating int)"
	db.SendSQL(action, connection)
	
def WriteToStaffTable(connection, date, name, position, timeon, timeoff, operating, ID, localsettings):
	
	success = False
	
	if miscmethods.ValidateTime(timeon) == True and miscmethods.ValidateTime(timeoff) == True:
		
		timeonint = int(timeon[:2] + timeon[3:5])
		timeoffint = int(timeoff[:2] + timeoff[3:5])
		
		if timeonint < timeoffint:
			
			success = True
		else:
			
			miscmethods.ShowMessage(GetLabel(localsettings, "vetfinishedbeforestartingmessage"))
	
	if success == True:
		
		starttimesql = timeon[:2] + ":" + timeon[3:5] + ":00"
		offtimesql = timeoff[:2] + ":" + timeoff[3:5] + ":00"
		
		action = "SELECT ID FROM staff WHERE DATE = \'" + str(date) + "\' AND Name = \'" + name + "\' AND ( \'" + starttimesql + "\' BETWEEN TimeOn AND TimeOff OR \'" + offtimesql + "\' BETWEEN TimeOn AND TimeOff OR TimeOn BETWEEN \'" + starttimesql + "\' AND \'" + offtimesql + "\' OR TimeOff BETWEEN \'" + starttimesql + "\' AND \'" + offtimesql + "\' )"
		results = db.SendSQL(action, connection)
		
		if len(results) > 0 and ID == False:
			
			miscmethods.ShowMessage(GetLabel(localsettings, "vettwoplacesatoncemessage"))
			
			success = False
		else:
			
			if ID == False:
				action = "INSERT INTO staff (Name, Date, Position, TimeOn, TimeOff, Operating) VALUES (\'" + name + "\', \'" + str(date) + "\', \'" + position + "\', \'" + timeon + "\', \'" + timeoff + "\', " + str(operating) + ")"
			else:
				action = "REPLACE INTO staff (ID, Name, Date, Position, TimeOn, TimeOff, Operating) VALUES (" + str(ID) + ", \'"+ name + "\', \'" + str(date) + "\', \'" + position + "\', \'" + timeon + "\', \'" + timeoff + "\', " + str(operating) + ")"
			db.SendSQL(action, connection)
			
	else:
		
		miscmethods.ShowMessage(GetLabel(localsettings, "invalidtimemessage"))
	
	return success

def CreateManualVaccinationTable(connection):
	
	action = "CREATE TABLE manualvaccination (ID int unsigned not null auto_increment primary key, AnimalID int, Date date, Name varchar(50), Batch varchar(50), Next date)"
	db.SendSQL(action, connection)

def WriteToManualVaccinationTable(connection, ID, animalid, dategiven, name, batch, nextdue):
	
	if ID == False:
		action = "INSERT INTO manualvaccination ( AnimalID, Date, Name, Batch, Next ) VALUES ( " + str(animalid) + ", \'" + dategiven + "\', \'" + name + "\', \'" + batch + "\', \'" + nextdue + "\' )"
	else:
		action = "REPLACE INTO manualvaccination ( ID, AnimalID, Date, Name, Batch, Next ) VALUES ( " + str(ID) + ", " + str(animalid) + ", \'" + dategiven + "\', \'" + name + "\', \'" + batch + "\', \'" + nextdue + "\' )"
	
	db.SendSQL(action, connection)

def CreateFormTable(connection):
	
	action = "CREATE TABLE form (ID int unsigned not null auto_increment primary key, Title varchar(100), Body text, FormType varchar(50))"
	db.SendSQL(action, connection)
	
	formbody = """
<p>
<<PracticeName>><br>
<<PracticeAddress>><br>
<<PracticePostcode>><br>
<<PracticeTelephone>>
</p>

<p>
<<Today>>
</p>

<p>
<<ClientName>><br>
<<ClientAddress>><br>
<<ClientPostcode>>
</p>

<p>
Dear <<ClientName>>
</p>

<p>
We have been trying to contact you unsuccessfully for some time on the following numbers:
</p>

<p>
<ul>
<li><<ClientHomeTelephone>></li>
<li><<ClientMobileTelephone>></li>
<li><<ClientWorkTelephone>></li>
</ul>
</p>

<p>
Could you please contact us on <<PracticeTelephone>> so that we can update you record.
</p>

<p>
Thank you in advance
</p>

<p>
<<PracticeName>>
</p>
"""
	
	action = "INSERT INTO form (Title, Body, FormType) VALUES (\"Unable to contact letter\", \"" + formbody + "\", \"client\")"
	db.SendSQL(action, connection)
	
	formbody = """
<h2 align=center>Invoice #<<InvoiceNumber>></h2>

<p align=center>from <<FromDate>> to <<ToDate>></p>

<table align=center>
<tr>
<td valign=top>
<fieldset>
<legend>Client</legend>
<<ClientName>><br>
<<ClientAddress>><br>
<<ClientPostcode>>
</td>
<td width=20>
</td>
<td valign=top>
<<InvoiceBreakdown>>
<br>
<table align=right>
<tr>
<td>
<fieldset>
<legend>Total</legend>
<font size=5>&pound;<<InvoiceTotal>></font>
</fieldset>
</td>
</tr>
</table>
</td>
<td width=20>
</td>
<td valign=top>
<fieldset>
<legend>Payable to</legend>
<<PracticeName>><br>
<<PracticeAddress>><br>
<<PracticePostcode>>
</fieldset>
</td>
</tr>
</table>
"""
	
	action = "INSERT INTO form (Title, Body, FormType) VALUES (\"Standard Invoice\", \"" + formbody + "\", \"invoice\")"
	db.SendSQL(action, connection)
	
	formbody = """
<table width=300 align=center>
	<tr>
		<td colspan=2 align=center>
			<font size=2><b><<PracticeName>></b></font><br>
			<font size=1><<PracticeAddress>>, <<PracticePostcode>>, <<PracticeTelephone>>.</font>
		</td>
	</tr>
	<tr>
		<td valign=top>
			<fieldset><legend><font size=1>Client</font></legend>
			<font size=1><<ClientName>><br><<ClientAddress>><br><<ClientPostcode>></font>
			</fieldset>
		</td>
		<td valign=top>
			<fieldset><legend><font size=1>Animal</font></legend>
			<font size=1><<AnimalName>><br><<AnimalSpecies>><br><<AnimalColour>></font>
			</fieldset>
		</td>
	</tr>
	<tr>
		<td colspan=2>
			<fieldset><legend><div><font size=1>Medication</font></div></legend>
			<font size=2><b><<MedicationName>> x <<Quantity>></b></font>
			</fieldset>
		</td>
	</tr>
	<tr>
		<td colspan=2>
			<fieldset><legend><font size=1>Instructions</font></legend>
			<font size=2><b><<Instructions>></b></font>
			</fieldset>
		</td>
	</tr>
	<tr>
		<td colspan=2 align=center>
			<font size=1>Keep all medicines out of reach of children<br>ANIMAL TREATMENT ONLY</font>
		</td>
	</tr>
</table>
"""
	
	action = "INSERT INTO form (Title, Body, FormType) VALUES (\"Medication Label\", \"" + formbody + "\", \"medication\")"
	db.SendSQL(action, connection)
	
	formbody = """
<p>
I <b><<ClientName>></b> of <b><<ClientAddress>></b> give my permission for <b><<AnimalName>></b>, my <<AnimalSpecies>> to receive a general anaesthetic on <<Today>>.
</p>

<p>
Signed..............................................................................
</p>
"""
	
	action = "INSERT INTO form (Title, Body, FormType) VALUES (\'Anaesthetic Consent\', \"" + formbody + "\", \"animal\")"
	db.SendSQL(action, connection)
	
def CreateDiaryTable(connection):
	
	action = "CREATE TABLE diary (ID int unsigned not null auto_increment primary key, Date date, Name varchar(20), Position varchar(20), Subject varchar(150), Note text, Removed date, LinkType int, LinkID int, ChangeLog text)"
	db.SendSQL(action, connection)
	
def WriteToDiaryTable(connection, diarydata):
	
	if diarydata.ID == False:
		
		action = "INSERT INTO diary (Date, Name, Position, Subject, Note, Removed, LinkType, LinkID, ChangeLog) VALUES (\'" + diarydata.date + "\', \'" + diarydata.name + "\', \'" + diarydata.position + "\', \'" + diarydata.subject + "\', \'" + diarydata.note + "\', \'" + str(diarydata.removed) + "\', " + str(diarydata.linktype) + ", " + str(diarydata.linkid) + ", \'" + diarydata.changelog + "\')"
		db.SendSQL(action, connection)
		
		action = "SELECT LAST_INSERT_ID() FROM diary"
		diarydata.ID = db.SendSQL(action, connection)
		
	else:
		
		action = "REPLACE INTO diary (ID, Date, Name, Position, Subject, Note, Removed, LinkType, LinkID, ChangeLog) VALUES (" + str(diarydata.ID) + ", \'" + diarydata.date + "\', \'" + diarydata.name + "\', \'" + diarydata.position + "\', \'" + diarydata.subject + "\', \'" + diarydata.note + "\', \'" + str(diarydata.removed) + "\', " + str(diarydata.linktype) + ", " + str(diarydata.linkid) + ", \'" + diarydata.changelog + "\')"
		db.SendSQL(action, connection)

def CreateMediaTable(connection):
	
	action = "CREATE TABLE media (ID int unsigned not null auto_increment primary key, LinkType int, LinkID int, FileName varchar(50), Description text, FileSize int, Content longtext, UploadedBy varchar(50))"
	db.SendSQL(action, connection)

def WriteToMediaTable(connection, ID, linktype, linkid, filename, description, filesize, content, uploadedby):
	
	#linktypes: 0 = client, 1 = animal
	
	if ID == False:
		
		action = "INSERT INTO media (LinkType, LinkID, FileName, Description, FileSize, Content, UploadedBy) VALUES (" + str(linktype) + ", " + str(linkid) + ", \'" + filename + "\', \'" + description + "\', " + str(filesize) + ", \'" + MySQLdb.escape_string(content) + "\', \'" + uploadedby + "\')"
		db.SendSQL(action, connection)
		
		action = "SELECT LAST_INSERT_ID() FROM media"
		ID = db.SendSQL(action, connection)
		
	else:
		
		action = "REPLACE INTO media (ID, LinkType, LinkID, FileName, Description, FileSize, Content, UploadedBy) VALUES (" + str(ID) + ", " + str(linktype) + ", " + str(linkid) + ", \'" + filename + "\', \'" + description + "\', " + str(filesize) + ", \'" + MySQLdb.escape_string(content) + "\', \'" + uploadedby + "\')"
		db.SendSQL(action, connection)

def CreateWeightTable(connection):
	
	action = "CREATE TABLE weight (ID int unsigned not null auto_increment primary key, Date date, AnimalID int, Weight int, Changelog text)"
	db.SendSQL(action, connection)

def WriteToWeightTable(connection, ID, animalid, date, weight, localsettings, changelog=False):
	
	currenttime = datetime.datetime.today().strftime("%x %X")
	userid = localsettings.userid
	
	if ID == False:
		
		changelog = currenttime + "%%%" + str(userid)
		
		action = "INSERT INTO weight (Date, AnimalID, Weight, Changelog) VALUES (\'" + date + "\', " + str(animalid) + ", " + str(weight) + ", \'" + changelog + "\')"
		db.SendSQL(action, connection)
		
		action = "SELECT LAST_INSERT_ID() FROM weight"
		ID = db.SendSQL(action, connection)[0][0]
		
	else:
		
		changelog = currenttime + "%%%" + str(userid) + "$$$" + changelog
		
		action = "REPLACE INTO weight (ID, Date, AnimalID, Weight, Changelog) VALUES (" + str(ID) + ", \'" + date + "\', " + str(animalid) + ", " + str(weight) + ", \'" + changelog + "\')"
		db.SendSQL(action, connection)
	
	return ID

def CreateInvoiceTable(connection):
	
	action = "CREATE TABLE invoice (ID int unsigned not null auto_increment primary key, ClientID int, FromDate date, ToDate date, Total int, Body text, Paid int)"
	db.SendSQL(action, connection)

def WriteToInvoiceTable(connection, ID, clientid, fromdate, todate, total, body, paid=0):
	
	if ID == False:
		
		action = "INSERT INTO invoice (ClientID, FromDate, ToDate, Total, Body, Paid) VALUES (\'" + str(clientid) + "\', \'" + fromdate + "\', \'" + todate + "\', " + str(total) + ", \'" + body + "\', " + str(paid) + ")"
		db.SendSQL(action, connection)
		
		action = "SELECT LAST_INSERT_ID() FROM invoice"
		ID = db.SendSQL(action, connection)[0][0]
		
	else:
		
		action = "REPLACE INTO invoice (ID, ClientID, FromDate, ToDate, Total, Body, Paid) VALUES (" + str(ID) + ", \'" + str(clientid) + "\', \'" + fromdate + "\', \'" + todate + "\', " + str(total) + ", \'" + body + "\', " + str(paid) + ")"
		db.SendSQL(action, connection)
	
	return ID

def CreateKennelTables(connection):
	
	action = "CREATE TABLE kennelblock (ID int unsigned not null auto_increment primary key, Name varchar(100), Description varchar(250))"
	db.SendSQL(action, connection)
	
	action = "CREATE TABLE kennel (ID int unsigned not null auto_increment primary key, KennelBlockID int, Name varchar(100), Description varchar(250))"
	db.SendSQL(action, connection)
	
	action = "CREATE TABLE kennelstay (ID int unsigned not null auto_increment primary key, AnimalID int, KennelID int, DateIn date, TimeIn varchar(10), DateOut date, TimeOut varchar(10), Comments text)"
	db.SendSQL(action, connection)

def CreateLostAndFoundTables(connection):
	
	action = "CREATE TABLE lostandfound (ID int unsigned not null auto_increment primary key, LostOrFound int, ContactID int, Species varchar(100), Date date, Sex int, Neutered int, FurLength int, Colour1 varchar(10), Colour2 varchar(10), Colour3 varchar(10), Collar int, CollarDescription varchar(100), Size int, Age int, IsChipped int, ChipNo varchar(20), Temperament int, Comments text, DateComplete date, ChangeLog text, Area varchar(50), AnimalID int)"
	db.SendSQL(action, connection)

def WriteToLostAndFoundTable(connection, lostandfounddata):
	
	if lostandfounddata.ID == False:
		
		action = "INSERT INTO lostandfound (ChangeLog) VALUES (\"" + lostandfounddata.changelog + "\")"
		db.SendSQL(action, connection)
		
		action = "SELECT LAST_INSERT_ID() FROM lostandfound"
		lostandfounddata.ID = db.SendSQL(action, connection)[0][0]
	
	action = "UPDATE lostandfound SET LostOrFound = " + str(lostandfounddata.lostorfound) + ", ContactID = " + str(lostandfounddata.contactid) + ", Species = \"" + str(lostandfounddata.species) + "\", Date = \"" + str(lostandfounddata.date) + "\", Sex = " + str(lostandfounddata.sex) + ", Neutered = "  + str(lostandfounddata.neutered) + ", FurLength = " + str(lostandfounddata.furlength) + ", Colour1 = \"" + str(lostandfounddata.colour1) + "\", Colour2 = \"" + str(lostandfounddata.colour2) + "\", Colour3 = \"" + str(lostandfounddata.colour3) + "\", Collar = "  + str(lostandfounddata.collar) + ", CollarDescription = \""  + str(lostandfounddata.collardescription) + "\", Size = "  + str(lostandfounddata.size) + ", Age = "  + str(lostandfounddata.age) + ", IsChipped = "  + str(lostandfounddata.ischipped) + ", ChipNo = \""  + str(lostandfounddata.chipno) + "\", Temperament = "  + str(lostandfounddata.temperament) + ", Comments = \""  + str(lostandfounddata.comments) + "\", DateComplete = \""  + str(lostandfounddata.datecomplete) + "\", ChangeLog = \""  + str(lostandfounddata.changelog) + "\", Area = \"" + str(lostandfounddata.area) + "\", AnimalID = " + str(lostandfounddata.animalid) + " WHERE ID = "  + str(lostandfounddata.ID)
	
	db.SendSQL(action, connection)

def GetNextVaccinations(settings):
  date_range = "`Next` >= CURDATE() AND  `Next` <= DATE_ADD(CURDATE() , INTERVAL 7 DAY)"

  action = "SELECT ID, AnimalID, Date, Name, Batch, Next FROM manualvaccination WHERE " + date_range
  results = db.SendSQL(action, settings.dbconnection)
  
  res = []
  for r in results:
    aux = []
    animal = Animal.find(settings, r[1])
    client = Client.find(settings, animal.OwnerID)
    aux.append(animal.OwnerID)
    aux.append(client.to_label())
    aux.append(animal.Name)
    aux.append(r[5])
    aux.append(client.ClientMobileTelephone)
    res.append(aux)
  
  action = "SELECT appointment.AnimalID, appointment.OwnerID, NextDue FROM medicationout LEFT JOIN appointment ON medicationout.AppointmentID = appointment.ID LEFT JOIN medication ON medicationout.MedicationID = medication.ID WHERE medication.Type = 1 AND " + date_range
  
  results = db.SendSQL(action, settings.dbconnection)
  for r in results:
    aux = []
    animal = Animal.find(settings, r[0])
    client = Client.find(settings, r[1])
    aux.append(animal.OwnerID)
    aux.append(client.to_label())
    aux.append(animal.Name)
    aux.append(r[2])
    aux.append(client.ClientMobileTelephone)
    res.append(aux)

  return res

def CreateAllTables(connection):
	
	CreateAnimalTable(connection)
	CreateClientTable(connection)
	CreateAppointmentTable(connection)
	CreateMedicationTables(connection)
	CreateProceduresTable(connection)
	CreateReceiptTable(connection)
	CreateLookupTables(connection)
	CreateUserTable(connection)
	CreateSettingsTable(connection)
	CreateStaffTable(connection)
	CreateManualVaccinationTable(connection)
	CreateFormTable(connection)
	CreateVersionTable(connection)
	CreateDiaryTable(connection)
	CreateMediaTable(connection)
	CreateWeightTable(connection)
	CreateInvoiceTable(connection)
	CreateKennelTables(connection)
	CreateLostAndFoundTables(connection)
