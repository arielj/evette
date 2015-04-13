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
import dbmethods
import miscmethods
import datetime

versionno = "1.3.4"

def GetCurrentVersion():
	
	return versionno

def CheckVersion(localsettings):
	
	success = False
	
	try:
		connection = db.GetConnection(localsettings)
		action = "SELECT VersionNo FROM version"
		results = db.SendSQL(action, connection)
		oldversion = results[0][0]
		connection.close()
		success = True
	except:
		if miscmethods.ConfirmMessage(localsettings.t("versiontablenotfoundquestion")):
			
			action = "CREATE TABLE version (ID int unsigned not null auto_increment primary key, VersionNo varchar(10))"
			db.SendSQL(action, localsettings.dbconnection)
			
			action = "INSERT INTO version (VersionNo) VALUES (\"1.1.2\")"
			db.SendSQL(action, localsettings.dbconnection)
			
			oldversion = "1.1.2"
			
			success = True
	
	if success == True:
		
		if versionno > oldversion:
			
			if miscmethods.ConfirmMessage(localsettings.t("versionupdatequestion1") + " " + versionno + ", " + localsettings.t("versionupdatequestion2") + " " + oldversion + ". " + localsettings.t("versionupdatequestion3")):
				
				if oldversion == "1.1.2":
					
					action = "CREATE TABLE manualvaccination (ID int unsigned not null auto_increment primary key, AnimalID int, Date date, Name varchar(50), Batch varchar(50), Next date)"
					db.SendSQL(action, localsettings.dbconnection)
					
					currenttime = datetime.datetime.today().strftime("%x %X")
					
					for a in ( "medication", "medicationin", "medicationout", "vaccinationtype", "vaccinationin", "vaccinationout", "receipt" ):
						action = "ALTER TABLE " + a + " ADD ChangeLog text"
						db.SendSQL(action, localsettings.dbconnection)
						action = "UPDATE " + a + " SET ChangeLog = \"" + currenttime + "%%%" + str(localsettings.userid) + "\""
						db.SendSQL(action, localsettings.dbconnection)
					
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.1.3\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE settings DROP HTMLViewer"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE user ADD Permissions varchar(50)"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE user SET Permissions = \"111$11$111$11$11$11$11$111$111\""
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.1.3"
					
				if oldversion == "1.1.3":
					
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.1.4\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.1.4"
				
				if oldversion == "1.1.4":
					
					action = "ALTER TABLE animal ADD IsDeceased int"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE animal SET IsDeceased = 0"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE animal ADD DeceasedDate date"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE animal SET DeceasedDate = \"0000-00-00\""
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE animal ADD CauseOfDeath text"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE animal SET CauseOfDeath = \"\""
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.1.5\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.1.5"
				
				if oldversion == "1.1.5":
					
					action = "DROP TABLE staff"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "CREATE TABLE staff (ID int unsigned not null auto_increment primary key, Name varchar(20), Date date, Position varchar(20), TimeOn varchar(20), TimeOff varchar(20), Operating int)"
                                        db.SendSQL(action, localsettings.dbconnection)

                                        action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.1.6\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.1.6"
					
				if oldversion == "1.1.6":
					
					dbmethods.CreateDiaryTable(localsettings.dbconnection)

                                        action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.1.7\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE user SET Permissions = CONCAT(Permissions, \"$111\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.1.7"
				
				if oldversion == "1.1.7":
					
					dbmethods.CreateMediaTable(localsettings.dbconnection)
					
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.1.8\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.1.8"
					
				if oldversion == "1.1.8":
					
					dbmethods.CreateWeightTable(localsettings.dbconnection)
					
					action = "ALTER TABLE medication ADD ReOrderNo int"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE medication SET ReOrderNo = 0"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.1.9\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.1.9"
				
				if oldversion == "1.1.9" or oldversion == "1.2":
					
					action = "ALTER TABLE settings ADD PracticeAddress varchar(250)"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE settings ADD PracticePostcode varchar(10)"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE settings ADD PracticeTelephone varchar(20)"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE settings ADD PracticeEmail varchar(100)"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE settings ADD PracticeWebsite varchar(250)"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE settings SET PracticeAddress = \"\", PracticePostcode = \"\", PracticeTelephone = \"\", PracticeEmail = \"\", PracticeWebsite = \"\""
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE form ADD FormType varchar(50)"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE form SET FormType = \"animal\""
					db.SendSQL(action, localsettings.dbconnection)
					
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
					db.SendSQL(action, localsettings.dbconnection)
					
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
					db.SendSQL(action, localsettings.dbconnection)
					
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
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE medication ADD ExpiryDate date"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE medication SET ExpiryDate = \"0000-00-00\""
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "CREATE TABLE invoice (ID int unsigned not null auto_increment primary key, ClientID int, FromDate date, ToDate date, Total int, Body text, Paid int)"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.2.1\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.2.1"
				
				if oldversion == "1.2.1":
					
					action = "ALTER TABLE medication ADD Type int"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE medication SET Type = 0"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE medicationout ADD NextDue date"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE medicationout SET NextDue = \"0000-00-00\""
					db.SendSQL(action, localsettings.dbconnection)
					
					try:
						
						action = "SELECT * FROM vaccinationtype"
						results = db.SendSQL(action, localsettings.dbconnection)
					
						action = "SELECT * FROM vaccinationin"
						vaccinationindata = db.SendSQL(action, localsettings.dbconnection)
					
						action = "SELECT * FROM vaccinationout"
						vaccinationoutdata = db.SendSQL(action, localsettings.dbconnection)
					
						for a in results:
						
							#VaccinationType --- (ID, Name, Description, CurrentBatch, Price, ChangeLog)
						
							#MedicationType --- (ID, Name, Description, Unit, BatchNo, CurrentPrice, ChangeLog, ReOrderNo, ExpiryDate)
						
							vaccinationid = a[0]
						
							action = "INSERT INTO medication (Name, description, Unit, BatchNo, CurrentPrice, ChangeLog, ReOrderNo, ExpiryDate, Type) VALUES (\"" + a[1] + "\", \"" + a[2] + "\", \"" + localsettings.t("vaccinationsvaccinelabel").lower() + "\", \"" + a[3] + "\", " + str(a[4]) + ", \"" + a[5] + "\", 0, \"0000-00-00\", 1)"
							db.SendSQL(action, localsettings.dbconnection)
						
							#action = "SELECT LAST_INSERT_ID() FROM medication" 
							action = "SELECT ID from medication ORDER BY ID DESC LIMIT 1" 
							medicationid = db.SendSQL(action, localsettings.dbconnection)
						
							#print 'medicationid', type(medicationid), medicationid

							if type(medicationid) in [type(['array']), type(('touple'))]:
							
								pass
						
							medicationid = medicationid[0][0]
						
							print 'medicationid', type(medicationid), medicationid
						
							for b in vaccinationindata:
								if a[0] == b[1]:
								
									#Vaccinationin --- (ID, VaccinationID, Date, Amount, BatchNo, Expires, WhereFrom, ChangeLog)
								
									#Medicationin --- (ID, MedicationID, Date, Amount, BatchNo, Expires, WhereFrom, ChangeLog)
								
									action = "INSERT INTO medicationin (MedicationID, Date, Amount, BatchNo, Expires, WhereFrom, ChangeLog) VALUES (" + \
									str(medicationid) + ", \"" + str(b[2]) + "\", \"" + str(b[3]) + "\", \"" + b[4] + "\", \"" + str(b[5]) + "\", \"" + b[6] + "\", \"" + b[7] + "\")"
								
									db.SendSQL(action, localsettings.dbconnection)
							
							for b in vaccinationoutdata:
							
								if a[0] == b[1]:
								
									#Vaccinationout --- (ID, VaccinationID, Date, Amount, BatchNo, WhereTo, AppointmentID, NextDue, ChangeLog)
								
									#Medicationout --- (ID, MedicationID, Date, Amount, BatchNo, WhereTo, AppointmentID, ChangeLog, NextDue)
								
									action = "INSERT INTO medicationout (MedicationID, Date, Amount, BatchNo, WhereTo, AppointmentID, ChangeLog, NextDue) VALUES (" + str(medicationid) + ", \"" + str(b[2]) + "\",  \"" + str(b[3]) + "\", \"" + b[4] + "\", \"" + str(b[5]) + "\", " + str(b[6]) + ", \"" + b[8] + "\", \"" + str(b[7]) + "\")"
								
									db.SendSQL(action, localsettings.dbconnection)
				
						action = "DROP TABLE vaccinationtype"
						db.SendSQL(action, localsettings.dbconnection)
				
						action = "DROP TABLE vaccinationin"
						db.SendSQL(action, localsettings.dbconnection)
				
						action = "DROP TABLE vaccinationout"
						db.SendSQL(action, localsettings.dbconnection)
						
					except:
						
						print "Vaccination tables not found - ignored!"
					
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.2.2\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.2.2"
				
				if oldversion == "1.2.2":
					
					dbmethods.CreateKennelTables(localsettings.dbconnection)
					
					action = "ALTER TABLE appointment ADD Staying int"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE appointment SET Staying = 0"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE animal ADD ASMRef varchar(10)"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE animal SET ASMRef = \"\""
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE settings ADD ShelterID int"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE settings SET ShelterID = 0"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "CREATE TABLE reason (ID int unsigned not null auto_increment primary key, ReasonName varchar(200))"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.2.3\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.2.3"
					
				if oldversion == "1.2.3":
					
					action = "ALTER TABLE appointment ADD ArrivalTime time"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE appointment SET ArrivalTime = NULL"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "SELECT ID, Permissions FROM user"
					results = db.SendSQL(action, localsettings.dbconnection)
					
					for a in results:
						
						permissions = a[1]
						
						permissions = permissions[:30] + "1" + permissions[30:]
						
						action = "UPDATE user SET Permissions = \"" + str(permissions) + "\" WHERE ID = " + str(a[0])
						db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE medication ADD CostPrice int"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE medication SET CostPrice = 0"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.2.6\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.2.6"
				
				if oldversion == "1.2.6":
					
					action = "ALTER TABLE settings ADD MarkupMultiplyBy varchar(10)"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE settings SET MarkupMultiplyBy = \"1.175\""
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE settings ADD MarkupRoundTo int"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE settings SET MarkupRoundTo = 5"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.2.7\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.2.7"
					
				if oldversion == "1.2.7":
					
					dbmethods.CreateLostAndFoundTables(localsettings.dbconnection)
					
					action = "ALTER TABLE client ADD PhonePermissions int"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE client SET PhonePermissions = 0"
					db.SendSQL(action, localsettings.dbconnection)
					
					animalsexes = []
					
					action = "ALTER TABLE animal ADD TempSex int"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE animal SET TempSex = 0"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE animal SET TempSex = 1 WHERE Sex = \"" + localsettings.t("malelabel") + "\""
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE animal SET TempSex = 2 WHERE Sex = \"" + localsettings.t("femalelabel") + "\""
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE animal MODIFY Sex int"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE animal SET Sex = TempSex"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE animal DROP TempSex"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.2.8\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.2.8"
				
				if oldversion == "1.2.8":
					
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.2.9\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.2.9"
				
				if oldversion == "1.2.9":
					
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.3\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.3"

				if oldversion == "1.3":
					
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.3.1\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.3.1"
				
				if oldversion == "1.3.1":
					
					action = "ALTER TABLE settings ADD ASMVaccinationID int"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE settings SET ASMVaccinationID = 0"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE settings ADD PrescriptionFee int"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "UPDATE settings SET PrescriptionFee = 0"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "SELECT ID, Permissions FROM user"
					results = db.SendSQL(action, localsettings.dbconnection)
					
					for a in results:
						
						permissions = a[1]
						
						permissions = permissions[:31] + "0" + permissions[31:]
						
						action = "UPDATE user SET Permissions = \"" + str(permissions) + "\" WHERE ID = " + str(a[0])
						db.SendSQL(action, localsettings.dbconnection)
					
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.3.2\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.3.2"
					
					home = miscmethods.GetHome()
					out = open(home + "/.evette.conf", "w")
					out.write(localsettings.dbip + "\n" + localsettings.dbuser + "\n" + localsettings.dbpass + "\n\nuser\n" + str(localsettings.language) + "\n15")
					out.close()
				
				if oldversion == "1.3.2":
				  
					action = "ALTER TABLE breed ADD species varchar(20)"
					db.SendSQL(action, localsettings.dbconnection)
				  
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.3.3\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.3.3"
					
				if oldversion == "1.3.3":
				  
					action = "ALTER TABLE settings ADD COLUMN handle_rota_by_day int DEFAULT 1"
					db.SendSQL(action, localsettings.dbconnection)
					
					action = "ALTER TABLE user ADD COLUMN mon_from varchar(4)" #HHMM
					db.SendSQL(action, localsettings.dbconnection)
					action = "ALTER TABLE user ADD COLUMN mon_to varchar(4)"
					db.SendSQL(action, localsettings.dbconnection)
					action = "ALTER TABLE user ADD COLUMN tue_from varchar(4)"
					db.SendSQL(action, localsettings.dbconnection)
					action = "ALTER TABLE user ADD COLUMN tue_to varchar(4)"
					db.SendSQL(action, localsettings.dbconnection)
					action = "ALTER TABLE user ADD COLUMN wed_from varchar(4)"
					db.SendSQL(action, localsettings.dbconnection)
					action = "ALTER TABLE user ADD COLUMN wed_to varchar(4)"
					db.SendSQL(action, localsettings.dbconnection)
					action = "ALTER TABLE user ADD COLUMN thu_from varchar(4)"
					db.SendSQL(action, localsettings.dbconnection)
					action = "ALTER TABLE user ADD COLUMN thu_to varchar(4)"
					db.SendSQL(action, localsettings.dbconnection)
					action = "ALTER TABLE user ADD COLUMN fri_from varchar(4)"
					db.SendSQL(action, localsettings.dbconnection)
					action = "ALTER TABLE user ADD COLUMN fri_to varchar(4)"
					db.SendSQL(action, localsettings.dbconnection)
					action = "ALTER TABLE user ADD COLUMN sat_from varchar(4)"
					db.SendSQL(action, localsettings.dbconnection)
					action = "ALTER TABLE user ADD COLUMN sat_to varchar(4)"
					db.SendSQL(action, localsettings.dbconnection)
					action = "ALTER TABLE user ADD COLUMN sun_from varchar(4)"
					db.SendSQL(action, localsettings.dbconnection)
					action = "ALTER TABLE user ADD COLUMN sun_to varchar(4)"
					db.SendSQL(action, localsettings.dbconnection)
				  
					action = "REPLACE INTO version (ID, VersionNo) VALUES (1, \"1.3.4\")"
					db.SendSQL(action, localsettings.dbconnection)
					
					oldversion = "1.3.4"
				
			else:
				
				success = False
		
		elif versionno < oldversion:
			
			miscmethods.ShowMessage(localsettings.t("clientolderthanservermessage"))
			
			success = False
	
	return success
