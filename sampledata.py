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
import random
import miscmethods
import threading
import wx
import clientmethods
import animalmethods
import appointmentmethods
import datetime
import medicationmethods
#import vaccinationmethods

class RandomClientsThread(threading.Thread):
	
	def __init__(self, parent):
		
		threading.Thread.__init__(self)
		self.parent = parent
		self.start()
	
	def run(self):
		
		self.parent.submitbutton.Disable()
		
		noofclients = int(self.parent.noofclientsentry.GetValue())
		noofanimals = int(self.parent.noofanimalsentry.GetValue())
		noofappointments = int(self.parent.noofappointmentsentry.GetValue())
		noofoperations = int(self.parent.noofoperationsentry.GetValue())
		noofmedications = int(self.parent.noofmedicationsentry.GetValue())
		
		
		
		
		#connection = db.GetConnection(self.parent.localsettings)
		#action = "SELECT * FROM vaccinationtype"
		#results = db.SendSQL(action, connection)
		#
		
		#if len(results) == 0:
			
			#doggivac = vaccinationmethods.VaccinationTypeData()
			
			#doggivac.name = "Doggivac"
			#doggivac.description = "Vaccine for dogs"
			#doggivac.price = 2000
			#doggivac.batchno = "123456"
			
			#doggivac.Submit(self.parent.localsettings)
			
			#doggivacin = vaccinationmethods.VaccinationInData(doggivac.ID)
			#doggivacin.amount = 100
			#doggivacin.batchno = "123456"
			#doggivacin.wherefrom = "Big Fogs Veterinary Superstore"
			
			#doggivacin.Submit(self.parent.localsettings)
			
			#cattivac = vaccinationmethods.VaccinationTypeData()
			
			#cattivac.name = "Cattivac"
			#cattivac.description = "Vaccine for cats"
			#cattivac.price = 2000
			#cattivac.batchno = "123456"
			
			#cattivac.Submit(self.parent.localsettings)
			
			#cattivacin = vaccinationmethods.VaccinationInData(cattivac.ID)
			#cattivacin.amount = 100
			#cattivacin.batchno = "123456"
			#cattivacin.wherefrom = "Big Fogs Veterinary Superstore"
			
			#cattivacin.Submit(self.parent.localsettings)
		
		wx.CallAfter(self.parent.clientgauge.SetValue, 0)
		
		for a in range(0, noofclients):
			
			clientdata = clientmethods.ClientSettings(self.parent.localsettings, False)
			
			sex = GetRandomSex()
			
			clientdata.title = GetRandomTitle(sex)
			clientdata.forenames = GetRandomForenames(sex)
			clientdata.surname = GetRandomSurname()
			clientdata.address = GetRandomAddress()
			clientdata.postcode = GetRandomPostCode()
			clientdata.hometelephone = GetRandomLandLine()
			clientdata.mobiletelephone = GetRandomMobileNo()
			clientdata.worktelephone = GetRandomLandLine()
			clientdata.emailaddress = GetRandomEmailAddress(clientdata.surname)
			clientdata.comments = GetRandomClientComments()
			
			
			dbmethods.WriteToClientTable(self.parent.localsettings.dbconnection, clientdata)
			
			count = ( float(a) / float(noofclients) ) * 100
			count = int(count)
			
			lastcount = ( float(a - 1) / float(noofclients) ) * 100
			lastcount = int(lastcount)
			
			if count != lastcount:
				wx.CallAfter(self.parent.clientgauge.SetValue, count)
			
		wx.CallAfter(self.parent.clientgauge.SetValue, 100)
		
		
			
		wx.CallAfter(self.parent.animalgauge.SetValue, 0)
		
		action = "SELECT ID FROM client"
		results = db.SendSQL(action, self.parent.localsettings.dbconnection)
		
		clientids = []
		for a in results:
			clientids.append(a[0])
		
		for a in range(0, noofanimals):
			
			ownerid = GetRandomEntry(clientids)
			animaldata = animalmethods.AnimalSettings(self.parent.localsettings, ownerid, False)
			
			animaldata.ownerid = GetRandomEntry(clientids)
			animaldata.name = unicode(GetRandomAnimalName(sex))
			animaldata.sex = GetRandomEntry((1, 2))
			animaldata.neutered = 0
			animaldata.species = unicode(GetRandomSpecies())
			animaldata.breed = unicode(GetRandomBreed(animaldata.species))
			animaldata.colour = unicode(GetRandomColour(animaldata.species))
			animaldata.dob = unicode(GetRandomDOB(animaldata.species))
			animaldata.chipno = GetRandomChipNo(animaldata.species)
			animaldata.comments = unicode(GetRandomAnimalComments())
			
			dbmethods.WriteToAnimalTable(self.parent.localsettings.dbconnection, animaldata)
			
			action = "SELECT * FROM medication WHERE Type = 1"
			results = db.SendSQL(action, self.parent.localsettings.dbconnection)
			
			if len(results) != 0:
				
				noofvaccines = int(random.random() * 5)
				
				randno = int(random.random() * 365)
				
				date = datetime.date.today()
				datepivot = datetime.timedelta(days=randno)
				
				date = date + datepivot
				
				for b in range(0, noofvaccines):
					
					datedue = date + datepivot
					datedue = miscmethods.GetSQLDateFromDate(datedue)
					
					datepivot = datetime.timedelta(days=-365)
					
					dategiven = date + datepivot
					date = dategiven
					dategiven = miscmethods.GetSQLDateFromDate(dategiven)
					
					name = "Foggovac"
					
					batch = str(int(random.random() * 1000000))
					
					dbmethods.WriteToManualVaccinationTable(self.parent.localsettings.dbconnection, False, animaldata.ID, dategiven, name, batch, datedue)
				
			
			count = ( float(a) / float(noofanimals) ) * 100
			count = int(count)
			
			lastcount = ( float(a - 1) / float(noofanimals) ) * 100
			lastcount = int(lastcount)
			
			if count != lastcount:
				wx.CallAfter(self.parent.animalgauge.SetValue, count)
			
		wx.CallAfter(self.parent.animalgauge.SetValue, 100)
		
		
		
		
		
		
		wx.CallAfter(self.parent.appointmentgauge.SetValue, 0)
		
		action = "SELECT ID FROM animal"
		results = db.SendSQL(action, self.parent.localsettings.dbconnection)
		
		animalids = []
		for a in results:
			animalids.append(a[0])
		
		todaysdate = datetime.datetime.today()
		sqldate = miscmethods.GetSQLDateFromDate(todaysdate)
		
		for a in range(0, noofappointments):
			
			animalid = GetRandomEntry(animalids)
			
			CreateRandomAppointment(self.parent.localsettings.dbconnection, animalid, self.parent.localsettings)
			
			count = ( float(a) / float(noofappointments) ) * 100
			count = int(count)
			
			lastcount = ( float(a - 1) / float(noofappointments) ) * 100
			lastcount = int(lastcount)
			
			if count != lastcount:
				wx.CallAfter(self.parent.appointmentgauge.SetValue, count)
			
		wx.CallAfter(self.parent.appointmentgauge.SetValue, 100)
		
		
		
		wx.CallAfter(self.parent.operationgauge.SetValue, 0)
		
		for a in range(0, noofoperations):
			
			animalid = GetRandomEntry(animalids)
			
			CreateRandomOperation(self.parent.localsettings.dbconnection, animalid, self.parent.localsettings)
			
			count = ( float(a) / float(noofoperations) ) * 100
			count = int(count)
			
			lastcount = ( float(a - 1) / float(noofoperations) ) * 100
			lastcount = int(lastcount)
			
			if count != lastcount:
				wx.CallAfter(self.parent.operationgauge.SetValue, count)
			
		wx.CallAfter(self.parent.operationgauge.SetValue, 100)
		
		
		
		wx.CallAfter(self.parent.medicationgauge.SetValue, 0)
		
		medicationnames = []
		
		for a in range(0, noofmedications):
			
			success = False
			
			while success == False:
				medicationdata = GetRandomMedication()
				if medicationnames.__contains__(medicationdata.name) == False:
					success = True
					medicationnames.append(medicationdata.name)
			
			medicationdata.Submit(self.parent.localsettings)
			
			medicationindata = medicationmethods.MedicationInData(medicationdata.ID)
			medicationindata.amount = "200"
			medicationindata.batchno = "000000"
			medicationindata.wherefrom = "Big Fogs Veterinary Superstore"
			
			medicationindata.Submit(self.parent.localsettings)
			
			count = ( float(a) / float(noofmedications) ) * 100
			count = int(count)
			
			lastcount = ( float(a - 1) / float(noofmedications) ) * 100
			lastcount = int(lastcount)
			
			if count != lastcount:
				wx.CallAfter(self.parent.medicationgauge.SetValue, count)
			
		wx.CallAfter(self.parent.medicationgauge.SetValue, 100)
		
		self.parent.GetGrandParent().GetParent().Close()

class RandomDataPanel(wx.Panel):
	
	def GetLabel(self, field):
		
		return  self.localsettings.dictionary[field][self.localsettings.language]
	
	def __init__(self, notebook, localsettings):
		
		self.localsettings = localsettings
		
		wx.Panel.__init__(self, notebook)
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, self.GetLabel("randomdatapagetitle"))
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		gridsizer = wx.FlexGridSizer(rows=5, cols=2)
		
		noofclientslabel = wx.StaticText(self, -1, self.GetLabel("randomdatanoofclientslabel") + ": ")
		gridsizer.Add(noofclientslabel, 0, wx.ALIGN_RIGHT)
		
		noofclientsentry = wx.TextCtrl(self, -1, "50")
		gridsizer.Add(noofclientsentry, 0, wx.EXPAND)
		
		noofanimalslabel = wx.StaticText(self, -1, self.GetLabel("randomdatanoofanimalslabel") + ": ")
		gridsizer.Add(noofanimalslabel, 0, wx.ALIGN_RIGHT)
		
		noofanimalsentry = wx.TextCtrl(self, -1, "100")
		gridsizer.Add(noofanimalsentry, 0, wx.EXPAND)
		
		noofappointmentslabel = wx.StaticText(self, -1, self.GetLabel("randomdatanoofappointmentslabel") + ": ")
		gridsizer.Add(noofappointmentslabel, 0, wx.ALIGN_RIGHT)
		
		noofappointmentsentry = wx.TextCtrl(self, -1, "30")
		gridsizer.Add(noofappointmentsentry, 0, wx.EXPAND)
		
		noofoperationslabel = wx.StaticText(self, -1, self.GetLabel("randomdatanoofoperationslabel") + ": ")
		gridsizer.Add(noofoperationslabel, 0, wx.ALIGN_RIGHT)
		
		noofoperationsentry = wx.TextCtrl(self, -1, "10")
		gridsizer.Add(noofoperationsentry, 0, wx.EXPAND)
		
		noofmedicationslabel = wx.StaticText(self, -1, self.GetLabel("randomdatanoofmedicationslabel") + ": ")
		gridsizer.Add(noofmedicationslabel, 0, wx.ALIGN_RIGHT)
		
		noofmedicationsentry = wx.TextCtrl(self, -1, "10")
		gridsizer.Add(noofmedicationsentry, 0, wx.EXPAND)
		
		topsizer.Add(gridsizer, 0, wx.ALIGN_CENTER)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		submitbutton = wx.BitmapButton(self, -1, submitbitmap)
		submitbutton.SetToolTipString(self.GetLabel("randomdatasubmittooltip"))
		submitbutton.Bind(wx.EVT_BUTTON, self.Submit)
		topsizer.Add(submitbutton, 0, wx.ALIGN_CENTER)
		
		horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		spacer1 = wx.StaticText(self, -1, "")
		horizontalsizer.Add(spacer1, 1, wx.EXPAND)
		
		gaugessizer = wx.BoxSizer(wx.VERTICAL)
		
		clientgaugelabel = wx.StaticText(self, -1, self.GetLabel("randomdataclientslabel") + ":")
		gaugessizer.Add(clientgaugelabel, 0, wx.ALIGN_CENTER)
		clientgauge = wx.Gauge(self)
		gaugessizer.Add(clientgauge, 0, wx.EXPAND)
		
		animalgaugelabel = wx.StaticText(self, -1, self.GetLabel("randomdataanimalslabel") + ":")
		gaugessizer.Add(animalgaugelabel, 0, wx.ALIGN_CENTER)
		animalgauge = wx.Gauge(self)
		gaugessizer.Add(animalgauge, 0, wx.EXPAND)
		
		appointmentgaugelabel = wx.StaticText(self, -1, self.GetLabel("randomdataappointmentslabel") + ":")
		gaugessizer.Add(appointmentgaugelabel, 0, wx.ALIGN_CENTER)
		appointmentgauge = wx.Gauge(self)
		gaugessizer.Add(appointmentgauge, 0, wx.EXPAND)
		
		operationgaugelabel = wx.StaticText(self, -1, self.GetLabel("randomdataoperationslabel") + ":")
		gaugessizer.Add(operationgaugelabel, 0, wx.ALIGN_CENTER)
		operationgauge = wx.Gauge(self)
		gaugessizer.Add(operationgauge, 0, wx.EXPAND)
		
		medicationgaugelabel = wx.StaticText(self, -1, self.GetLabel("randomdatamedicationlabel") + ":")
		gaugessizer.Add(medicationgaugelabel, 0, wx.ALIGN_CENTER)
		medicationgauge = wx.Gauge(self)
		gaugessizer.Add(medicationgauge, 0, wx.EXPAND)
		
		horizontalsizer.Add(gaugessizer, 8, wx.EXPAND)
		
		spacer2 = wx.StaticText(self, -1, "")
		horizontalsizer.Add(spacer2, 1, wx.EXPAND)
		
		topsizer.Add(horizontalsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.noofclientsentry = noofclientsentry
		self.noofanimalsentry = noofanimalsentry
		self.noofappointmentsentry = noofappointmentsentry
		self.noofoperationsentry = noofoperationsentry
		self.noofmedicationsentry = noofmedicationsentry
		
		self.clientgauge = clientgauge
		self.animalgauge = animalgauge
		self.appointmentgauge = appointmentgauge
		self.operationgauge = operationgauge
		self.medicationgauge = medicationgauge
		
		self.submitbutton = submitbutton
	
	def Submit(self, ID):
		
		miscmethods.ShowMessage(self.GetLabel("randomdatawarningmessage"))
		RandomClientsThread(self)

def GetRandomEntry(tuple):
	
	return tuple[int(random.random() * len(tuple))]

def GetRandomLandLine():
	
	phoneno = "0114 2"
	for a in range(0, 6):
		phoneno = phoneno + str(int(random.random() * 10))
	
	return phoneno

def GetRandomMobileNo():
	
	phoneno = "07"
	
	for a in range(0, 3):
		phoneno = phoneno + str(int(random.random() * 10))
	
	phoneno = phoneno + " "
	
	for a in range(0, 6):
		phoneno = phoneno + str(int(random.random() * 10))
	
	return phoneno

def GetRandomBreed(species):
	
	if species == "Cat":
		randno = int(random.random() * 10)
		if randno < 7:
			breed = "SH Dom"
		elif randno < 8:
			breed = "SLH Dom"
		else:
			breed = "LH Dom"
	else:
		breed = "Crossbreed"
	
	return breed

def GetRandomSex():
	
	randno = int(str(random.random())[-1])
	
	if randno > 4:
		sex = "Male"
	else:
		sex = "Female"
	
	return sex

def GetRandomTitle(sex):
	
	if sex == "Male":
		title = "Mr"
	else:
		titles = ( "Ms", "Mrs", "Miss", "Ms" )
		title = GetRandomEntry(titles)
	
	return title

def GetRandomForenames(sex):
	
	
	if sex == "Male":
		forenames = ( "Gavin", "Patrick", "Giles", "Sam", "Fred", "Adam", "Terry", "Bob", "Gavin", "Archie", "Hank", "Chuck", "Jack", "Hugh", "Albert", "Bryan", "Brian", "Graham", "Graeme" )
	else:
		forenames = ( "Tammy", "Karen", "Kate", "Paula", "Sue", "Pat", "Laura", "Alex", "Eileen", "Alison", "Sandra", "Julie", "Sharon", "Tracey", "Helen", "Leanne", "Carol", "Anne", "Josey", "Bernadette", "Pauline", "Catherine", "Jessica", "Claire", "Clare", "Sarah", "Samantha", "Floella", "Polly", "Joanne" )
	
	return GetRandomEntry(forenames)

def GetRandomSurname():
	
	surnames = ( "Smith", "Spencer", "Wilson", "Pring", "Cattermole", "Tarplett", "Abdul-Jabar", "Jones", "Bloggs", "Reeves", "Pitt", "Stanley", "Simmons", "Criss", "Frehley", "Presley", "Higginbottom", "Bottomley", "Blair", "Prescott", "Major", "Thatcher", "Briggs", "Lynskey", "Rowbotham", "Hough", "Gough", "Houghton", "Gillott", "Gill", "Hawkins", "Johnson", "Allison", "Rawson-Tetley", "Bendin", "Steel", "Edley", "Pring", "Naylor" )
	
	return GetRandomEntry(surnames)

def GetRandomAddress():
	
	street1s = ( "Green", "Brown", "Lawrence", "Bawtry", "Maple", "Sycamore", "Shakespear", "Butt Hole", "Melciss", "Constable", "Foggy", "Maureen", "Spencer", "Ovaltine", "Titty Ho", "Plank", "Downing", "Maltravers", "Elm", "Forest", "Bolsover", "Whitby", "Scarborough", "Clifton", "Hyacinth", "Rose", "Gorse", "Bracken" )
	
	street2s = ( "Road", "Lane", "Close", "Avenue", "Crescent" )
	
	housenumber = random.random() * 200
	housenumber = str(housenumber).split(".")[0]
	
	address = housenumber + " " + GetRandomEntry(street1s) + " " + GetRandomEntry(street2s) + "\nSheffield"
	
	return address

def GetRandomPostCode():
	
	letters = "qwertyuiopasdfghjklzxcvbnm"
	
	postcode = "S" + str(int((random.random() * 35) + 1)) + " " + str(int((random.random() * 9) + 1)) + letters[int(random.random() * 26)].upper() + letters[int(random.random() * 26)].upper()
	
	return postcode

def GetRandomEmailAddress(name):
	
	if random.random() * 100 < 33:
		randno = str(random.random())[-3:]
		email = name + randno + "@" + "foggymail.net"
	else:
		email = ""
	return email

def GetRandomClientComments():
	
	if random.random() * 10 < 4:
		
		comments = ( "Deaf", "Blind", "Uses wheelchair", "Has tourettes", "Mute", "Doesn't speak English", "Has stutter", "Insist on payment in advance" )
		comment = GetRandomEntry(comments)
	else:
		comment = ""
	return comment

def GetRandomSpecies():
	
	if random.random() * 10 > 3:
		if random.random() * 10 > 5:
			species = "Dog"
		else:
			species = "Cat"
	else:
		specieslist = ( "Dog", "Cat", "Rabbit", "Hamster", "Guinea Pig", "Ferret", "Budgie", "Parrot" )
		species = GetRandomEntry(specieslist)
	
	return species

def GetRandomColour(species):
	
	if species == "Dog":
		colours = ( "Black", "White", "Black and White", "White and Black", "Ginger", "Ginger and White", "White and Ginger", "Grey", "Grey and White", "White and Grey", "Black and Tan", "Tan and Black", "Tricolour", "Brindle", "Brindle and White", "Blue Merle", "Liver", "Liver and White", "Tan")
	elif species == "Cat":
		colours = ( "Black", "White", "Black and White", "White and Black", "Ginger", "Ginger and White", "White and Ginger", "Grey", "Grey and White", "White and Grey", "Tabby", "Tabby amd White", "White and Tabby" )
	else:
		colours = ( "Black", "White", "Grey" )
	
	return GetRandomEntry(colours)

def GetRandomDOB(species):
	
	currentyear = datetime.date.today().year
	
	if species == "Dog" or species == "Cat":
		age = random.random() * 16
	else:
		age = random.random() * 5
	
	return str(int(currentyear) - int(age))

def GetRandomChipNo(species):
	
	chipno = ""
	
	if species == "Dog" or species == "Cat" or species == "Rabbit" or species == "Ferret":
		
		randno = str(random.random())[-1]
		
		if int(randno) > 4:
			chipno = "958000000"
			
			for c in range(0,6):
				
				randno = str(int(random.random() * 10))[0]
				chipno = chipno + randno
	
	return chipno

def GetRandomAnimalComments():
	
	if random.random() * 10 < 4:
		
		comments = ( "Hates vets - need muzzle", "Allergic to Spamulox!", "Doesn't like having feet touched", "Very nervous", "Wees when frightened" )
		comment = GetRandomEntry(comments)
	else:
		comment = ""
	return comment

def GetRandomAnimalName(sex):
	
	if sex == "Male":
		names = ( "Foggy", "Snoop", "Merlin", "Sam", "Stig", "Leo", "Lynx", "Bruno", "Tyson", "Max", "Jake", "Henry", "Buster", "Luke", "Duke", "Sabre", "Geordie", "Ben", "Rocky", "Archie", "Bruce", "Bailey", "Dude", "Ozzie", "Tosca", "Mickey", "Lachy", "Sam", "Benji", "Rex", "Jet", "Henry", "Jacques", "Sezer", "Patch" , "Samson", "Gabriel", "Jack" )
	else:
		names = ( "Maureen", "Jenna", "Connie", "Meryl", "Purdy", "Lucy", "Tess", "Barbara", "Avril", "Madge", "Nadia", "Sheba", "Flick", "Ellie", "Buffy", "Misty", "Sasha", "Zena", "Tara", "Zoe", "Tammy", "Ella", "Penny", "Molly", "Kelly", "Lady", "Elsa", "Agnes", "Nala", "Imogen", "Grace", "Heather", "Lola", "Tallulah", "Medusa", "Custard", "Violet", "Chardonnay", "Asti", "Jasmine", "Cleo", "Chloe", "Ruby" )
	
	return GetRandomEntry(names)

def GetRandomReason():
	
	reasons = ( "Coughing", "Diarrhoea", "Limping", "General Checkover", "Ate owners car keys", "Chewing itself", "Toileting in house", "Request PTS", "Microchipping" )
	
	return GetRandomEntry(reasons)

def GetRandomOpReason():
	
	reasons = ( "Leg Amputation", "Dental", "Dew Claw Removal", "Pin Removal", "Exploratory", "Tail Amputation" )
	
	return GetRandomEntry(reasons)

def GetRandomNotes(good):
	
	goodnotes = ( "Fine, bright, alert. Appetite fine, passing urine and stools, temperature normal.", "Very difficult to examine, very aggressive. Seems tender around abdomen, temperature temperature normal. Eating, drinking and toileting fine.", "A little underweight but very active. NAD." )
	
	badnotes = ( "Animal collapsed on entry, in and out of consciousness. Watery diarrhoea, nasal discharge, high temperature.", "8/10 lame on right leg. Painful on manipulation, no sign of a break, sprain?", "Absolutely wild!! Unable to examine.", "Open wound on back, pussy discharge, high temperature." )
	
	if good == True:
		
		return GetRandomEntry(goodnotes)
		
	else:
		
		return GetRandomEntry(badnotes)

def GetRandomPlan():
	
	plans = ( "Monitor", "No treatment required", "Advise full bloods", "Re-examine in 7 days" )
	
	return GetRandomEntry(plans)

def GetRandomProblem():
	
	problems = ( "No problem", "Underweight", "Overweight", "Anaemic" )
	
	return GetRandomEntry(problems)

def GetRandomMedication():
	
	purposes = ( "Antibiotic", "Eye drops", "Skin cream", "Pain relief", "Sedative", "Steriod", "Anti-inflammatory" )
	
	purpose = GetRandomEntry(purposes)
	
	part1 = ( "Fog", "Moz", "Men", "Mez", "Bob", "Nostr", "Snurt", "Tam", "Ad", "Ol", "Alex", "Jon", "Fil", "Sam", "Ben", "Sphinct", "Star", "Buf", "Rex", "Storm" )
	
	part2 = ( "a", "e", "i", "o", "u", "y" )
	
	name = GetRandomEntry(part1) + GetRandomEntry(part2)
	
	if purpose == "Antibiotic":
		suffixes = ( "cillin", "lox", "care", "doxine", "exine" )
		suffix = GetRandomEntry(suffixes)
		units = ( "tablet", "capsule", "ml" )
		unit = GetRandomEntry(units)
		if unit == "tablet" or unit == "capsule":
			weights = ( "10mg", "5mg", "100mg", "250mg" )
			weight = GetRandomEntry(weights)
			suffix = suffix + " " + weight
	elif purpose == "Eye drops":
		suffixes = ( "thalmic", "opti" )
		suffix = GetRandomEntry(suffixes)
		unit = "bottle"
		capacities = ( "100ml", "75ml", "50ml" )
		capacity = GetRandomEntry(capacities)
		suffix = suffix + " " + capacity
	elif purpose == "Skin Cream":
		suffixes = ( "derm", "dex", "lan", "gel", "otic" )
		suffix = GetRandomEntry(suffixes)
		unit = "Tube"
	elif purpose == "Steroid":
		suffix = "nisolone"
		units = ( "tablet", "capsule", "ml" )
		unit = GetRandomEntry(units)
		if unit == "tablet" or unit == "capsule":
			weights = ( "10mg", "5mg", "100mg", "250mg" )
			weight = GetRandomEntry(weights)
	else:
		suffixes = ( "cin", "fen", "n", "m", "sin", "ton" )
		suffix = GetRandomEntry(suffixes)
		units = ( "tablet", "capsule", "ml", "tube", "bottle" )
		unit = GetRandomEntry(units)
		if unit == "tablet" or unit == "capsule":
			weights = ( "10mg", "5mg", "100mg", "250mg" )
			weight = GetRandomEntry(weights)
			suffix = suffix + " " + weight
		elif unit == "bottle":
			capacities = ( "100ml", "75ml", "50ml" )
			capacity = GetRandomEntry(capacities)
			suffix = suffix + " " + capacity
	
	name = name + suffix
	
	batchno = str(int(random.random() * 1000000))
	
	price = str(random.random())[-3:]
	
	medicationdata = medicationmethods.MedicationData()
	medicationdata.name = name
	medicationdata.description = purpose
	medicationdata.unit = unit
	medicationdata.batchno = batchno
	medicationdata.price = price
	medicationdata.expiry = "0000-00-00"
	
	currenttime = datetime.datetime.today().strftime("%x %X")
	#medicationdata.changelog = currenttime + " (Random Data!!)%%%0"
	
	return (medicationdata)

def CreateRandomAppointment(connection, animalid, localsettings):
	
	appointmentdata = appointmentmethods.AppointmentSettings(localsettings, animalid, False)
	
	openfrom = localsettings.openfrom
	openfrom = int(openfrom[:2]) * 60 + int(openfrom[3:5])
	
	opento = localsettings.opento
	opento = int(opento[:2]) * 60 + int(opento[3:5])
	
	time = opento - openfrom
	
	time = int(random.random() * time) + openfrom
	
	time = miscmethods.GetTimeFromMinutes(time)
	
	if random.random() * 10 > 5:
		time = time[:-1] + "0"
	else:
		time = time[:-1] + "5"
	
	date = datetime.date.today()
	
	randno = int(random.random() * 300)
	
	if int(random.random() * 1000) < 500:
		
		randno = randno * -1
		appointmentdata.problem = GetRandomProblem()
		appointmentdata.notes = GetRandomNotes(True)
		appointmentdata.plan = GetRandomPlan()
	
	timedelta = datetime.timedelta(days=randno)
	date = date + timedelta
	
	date = miscmethods.GetSQLDateFromDate(date)
	
	appointmentdata.date = date
	
	appointmentdata.time = time + ":00"
	appointmentdata.reason = GetRandomReason()
	
	appointmentdata.operation = 0
	
	dbmethods.WriteToAppointmentTable(connection, appointmentdata)

def CreateRandomOperation(connection, animalid, localsettings):
	
	appointmentdata = appointmentmethods.AppointmentSettings(localsettings, animalid, False)
	
	time = "09:00:00"
	
	date = datetime.date.today()
	
	randno = int(random.random() * 300)
	
	if int(random.random() * 1000) < 500:
		
		randno = randno * -1
		appointmentdata.problem = GetRandomProblem()
		appointmentdata.notes = GetRandomNotes(True)
		appointmentdata.plan = GetRandomPlan()
	
	timedelta = datetime.timedelta(days=randno)
	date = date + timedelta
	
	date = miscmethods.GetSQLDateFromDate(date)
	
	appointmentdata.date = date
	
	appointmentdata.time = time
	appointmentdata.reason = GetRandomOpReason()
	
	appointmentdata.operation = 1
	
	dbmethods.WriteToAppointmentTable(connection, appointmentdata)
