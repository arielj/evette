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

import wx
import miscmethods
import db
import dbmethods
import datetime
import customwidgets
import animalmethods
import clientmethods
import appointmentmethods

class MailShotPanel(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return  self.localsettings.t(field, idx)
	
	def __init__(self, notebook, localsettings):
		
		busy = wx.BusyCursor()
		
		self.localsettings = localsettings
		
		self.pagetitle = self.t("mailshotpagetitle")
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, self.pagetitle)
		
		wx.Panel.__init__(self, notebook)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		mainnotebook = wx.Notebook(self)
		
		self.vaccinationspanel = VaccinationsPanel(mainnotebook, self.localsettings)
		
		mainnotebook.AddPage(self.vaccinationspanel, self.t("animalvaccinationslabel"), select=True)
		
		topsizer.Add(mainnotebook, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		del busy

class VaccinationsPanel(wx.Panel):
	
	def t(self, field):
		
		return  self.localsettings.t(field)
	
	def GetButtonLabel(self, field, index):
		
		return  self.localsettings.dictionary[field][self.localsettings.language][index]
	
	def __init__(self, parent, localsettings):
		
		self.localsettings = localsettings
		
		wx.Panel.__init__(self, parent)
		
		horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		gridsizer = wx.FlexGridSizer(cols=2)
		
		gridsizer.AddGrowableCol(1)
		gridsizer.AddGrowableRow(4)
		gridsizer.AddGrowableRow(7)
		
		fromdatelabel = wx.StaticText(self, -1, self.t("fromlabel") + ": ")
		gridsizer.Add(fromdatelabel, 0, wx.ALIGN_RIGHT)
		
		fromdateentry = customwidgets.DateCtrl(self, self.localsettings)
		gridsizer.Add(fromdateentry, 1, wx.EXPAND)
		
		todatelabel = wx.StaticText(self, -1, self.t("tolabel") + ": ")
		gridsizer.Add(todatelabel, 0, wx.ALIGN_RIGHT)
		
		todateentry = customwidgets.DateCtrl(self, self.localsettings)
		gridsizer.Add(todateentry, 1, wx.EXPAND)
		
		specieslabel = wx.StaticText(self, -1, self.t("animalspecieslabel") + ": ")
		gridsizer.Add(specieslabel, 0, wx.ALIGN_RIGHT)
		
		action = "SELECT * FROM species ORDER BY SpeciesName"
		specieslist = db.SendSQL(action, self.localsettings.dbconnection)
		
		specieschoicelist = []
		for a in specieslist:
			specieschoicelist.append(a[1])
		
		specieschoicesizer = wx.BoxSizer(wx.HORIZONTAL)
		
		specieschoice = wx.Choice(self, -1, choices=specieschoicelist)
		specieschoice.Disable()
		specieschoicesizer.Add(specieschoice, 1, wx.EXPAND)
		
		speciestickbox = wx.CheckBox(self, -1, self.t("anyspecies"))
		speciestickbox.Bind(wx.EVT_CHECKBOX, self.AnySpecies)
		speciestickbox.SetValue(True)
		specieschoicesizer.Add(speciestickbox, 0, wx.EXPAND)
		
		
		gridsizer.Add(specieschoicesizer, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(self, -1, ""), 0, wx.EXPAND)
		
		speciesmovementsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		speciesmovementsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		downarrowbitmap = wx.Bitmap("icons/downarrow.png")
		addspeciesbutton = wx.BitmapButton(self, -1, downarrowbitmap)
		addspeciesbutton.Disable()
		addspeciesbutton.Bind(wx.EVT_BUTTON, self.AddSpecies)
		speciesmovementsizer.Add(addspeciesbutton, 0, wx.EXPAND)
		
		speciesmovementsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		uparrowbitmap = wx.Bitmap("icons/uparrow.png")
		removespeciesbutton = wx.BitmapButton(self, -1, uparrowbitmap)
		removespeciesbutton.Bind(wx.EVT_BUTTON, self.RemoveSpecies)
		removespeciesbutton.Disable()
		speciesmovementsizer.Add(removespeciesbutton, 0, wx.EXPAND)
		
		
		speciesmovementsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		gridsizer.Add(speciesmovementsizer, 0, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(self, -1, ""), 0, wx.EXPAND)
		
		specieslistbox = wx.ListBox(self, -1)
		specieslistbox.Bind(wx.EVT_LISTBOX, self.SpeciesSelected)
		gridsizer.Add(specieslistbox, 1, wx.EXPAND)
		
		if len(specieslist) == 0:
			addspeciesbutton.Disable()
			removespeciesbutton.Disable()
		
		#gridsizer.Add(wx.StaticText(self, -1, ""), 0, wx.EXPAND)
		#gridsizer.Add(wx.StaticText(self, -1, ""), 0, wx.EXPAND)
		
		vaccinelabel = wx.StaticText(self, -1, self.t("animalvaccinelabel") + ": ")
		gridsizer.Add(vaccinelabel, 0, wx.ALIGN_RIGHT)
		
		action = "SELECT * FROM medication WHERE Type = 1 ORDER BY Name"
		vaccinationslist = db.SendSQL(action, self.localsettings.dbconnection)
		
		vaccinationschoicelist = []
		for a in vaccinationslist:
			vaccinationschoicelist.append(a[1])
		
		
		
		vaccinechoicesizer = wx.BoxSizer(wx.HORIZONTAL)
		
		vaccinechoice = wx.Choice(self, -1, choices=vaccinationschoicelist)
		vaccinechoice.Disable()
		vaccinechoicesizer.Add(vaccinechoice, 1, wx.EXPAND)
		
		vaccinetickbox = wx.CheckBox(self, -1, self.t("anyvaccine"))
		vaccinetickbox.Bind(wx.EVT_CHECKBOX, self.AnyVaccine)
		vaccinetickbox.SetValue(True)
		vaccinechoicesizer.Add(vaccinetickbox, 0, wx.EXPAND)
		
		
		gridsizer.Add(vaccinechoicesizer, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(self, -1, ""), 0, wx.EXPAND)
		
		vaccinemovementsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		vaccinemovementsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		downarrowbitmap = wx.Bitmap("icons/downarrow.png")
		addvaccinebutton = wx.BitmapButton(self, -1, downarrowbitmap)
		addvaccinebutton.Disable()
		addvaccinebutton.Bind(wx.EVT_BUTTON, self.AddVaccine)
		vaccinemovementsizer.Add(addvaccinebutton, 0, wx.EXPAND)
		
		vaccinemovementsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		uparrowbitmap = wx.Bitmap("icons/uparrow.png")
		removevaccinebutton = wx.BitmapButton(self, -1, uparrowbitmap)
		removevaccinebutton.Bind(wx.EVT_BUTTON, self.RemoveVaccine)
		removevaccinebutton.Disable()
		vaccinemovementsizer.Add(removevaccinebutton, 0, wx.EXPAND)
		
		vaccinemovementsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		gridsizer.Add(vaccinemovementsizer, 0, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(self, -1, ""), 0, wx.EXPAND)
		
		vaccineslistbox = wx.ListBox(self, -1)
		vaccineslistbox.Bind(wx.EVT_LISTBOX, self.VaccineSelected)
		gridsizer.Add(vaccineslistbox, 1, wx.EXPAND)
		
		if len(vaccinationslist) == 0:
			addvaccinebutton.Disable()
			removevaccinebutton.Disable()
		
		topsizer.Add(gridsizer, 1, wx.EXPAND)
		
		#topsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		gobutton = wx.Button(self, -1, self.t("searchlabel"))
		gobutton.Bind(wx.EVT_BUTTON, self.Go)
		topsizer.Add(gobutton, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		#topsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		#gauge = wx.Gauge(self)
		#topsizer.Add(gauge, 0, wx.EXPAND)
		
		#topsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		horizontalsizer.Add(topsizer, 1, wx.EXPAND)
		
		horizontalsizer.Add(wx.StaticText(self, -1, "", size=(50,-1)), 0, wx.EXPAND)
		
		rightsizer = wx.BoxSizer(wx.VERTICAL)
		
		buttonssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		editanimalbutton = wx.Button(self, -1, self.GetButtonLabel("appointmenteditanimalbutton", 0))
		editanimalbutton.SetToolTipString(self.GetButtonLabel("appointmenteditanimalbutton", 1))
		editanimalbutton.Bind(wx.EVT_BUTTON, self.EditAnimal)
		editanimalbutton.SetForegroundColour("blue")
		editanimalbutton.Disable()
		buttonssizer.Add(editanimalbutton, 0, wx.EXPAND)
		
		editownerbutton = wx.Button(self, -1, self.GetButtonLabel("appointmenteditownerbutton", 0))
		editownerbutton.SetToolTipString(self.GetButtonLabel("appointmenteditownerbutton", 1))
		editownerbutton.Bind(wx.EVT_BUTTON, self.EditOwner)
		editownerbutton.SetForegroundColour("blue")
		editownerbutton.Disable()
		buttonssizer.Add(editownerbutton, 0, wx.EXPAND)
		
		createappointmentbutton = wx.Button(self, -1, self.GetButtonLabel("createvaccinationappointmentbutton", 0))
		createappointmentbutton.SetToolTipString(self.GetButtonLabel("createvaccinationappointmentbutton", 1))
		createappointmentbutton.Bind(wx.EVT_BUTTON, self.CreateAppointment)
		createappointmentbutton.SetForegroundColour("blue")
		createappointmentbutton.Disable()
		buttonssizer.Add(createappointmentbutton, 0, wx.EXPAND)
		
		buttonssizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		generatecvsbutton = wx.Button(self, -1, self.GetButtonLabel("generatevaccinationcsvbutton", 0))
		generatecvsbutton.SetToolTipString(self.GetButtonLabel("generatevaccinationcsvbutton", 1))
		generatecvsbutton.Bind(wx.EVT_BUTTON, self.GenerateCVSFile)
		generatecvsbutton.SetForegroundColour("red")
		generatecvsbutton.Disable()
		buttonssizer.Add(generatecvsbutton, 0, wx.EXPAND)
		
		rightsizer.Add(buttonssizer, 0, wx.EXPAND)
		
		listbox = VaccineMailShotListbox(self, localsettings)
		listbox.Bind(wx.EVT_LISTBOX, self.VaccinationSelected)
		rightsizer.Add(listbox, 1, wx.EXPAND)
		
		totallabel = wx.StaticText(self, -1, self.t("totallabel") + ": 0 ")
		rightsizer.Add(totallabel, 0, wx.ALIGN_RIGHT)
		
		horizontalsizer.Add(rightsizer, 2, wx.EXPAND)
		
		self.SetSizer(horizontalsizer)
		
		self.specieschoice = specieschoice
		self.specieslistbox = specieslistbox
		self.specieschoicelist = specieschoicelist
		self.removespeciesbutton = removespeciesbutton
		self.addspeciesbutton = addspeciesbutton
		
		self.vaccinechoice = vaccinechoice
		self.vaccineslistbox = vaccineslistbox
		self.vaccinationschoicelist = vaccinationschoicelist
		self.removevaccinebutton = removevaccinebutton
		self.addvaccinebutton = addvaccinebutton
		
		self.fromdateentry = fromdateentry
		self.todateentry = todateentry
		
		self.vaccinetickbox = vaccinetickbox
		self.speciestickbox = speciestickbox
		
		self.listbox = listbox
		
		self.totallabel = totallabel
		self.rightsizer = rightsizer
		
		self.editanimalbutton = editanimalbutton
		self.editownerbutton = editownerbutton
		self.createappointmentbutton = createappointmentbutton
		self.generatecvsbutton = generatecvsbutton
		
		self.includedspecieslist = []
		self.includedvaccinationslist = []
	
	def RefreshSpeciesList(self, ID=False):
		
		self.specieslistbox.Clear()
		for a in self.includedspecieslist:
			self.specieslistbox.Append(a)
		self.specieslistbox.SetSelection(-1)
		self.removespeciesbutton.Disable()
	
	def AddSpecies(self, ID=False):
		
		choiceid = self.specieschoice.GetSelection()
		
		if choiceid == -1:
			
			choiceid = 0
		
		species = self.specieschoicelist[choiceid]
		
		if self.includedspecieslist.__contains__(species) == False:
			
			self.includedspecieslist.append(species)
			
			self.RefreshSpeciesList()
	
	def SpeciesSelected(self, ID=False):
		
		self.removespeciesbutton.Enable()
	
	def RemoveSpecies(self, ID=False):
		
		listboxid = self.specieslistbox.GetSelection()
		
		species = self.includedspecieslist[listboxid]
		
		self.includedspecieslist.remove(species)
		
		self.RefreshSpeciesList()
	
	def RefreshVaccineList(self, ID=False):
		
		self.vaccineslistbox.Clear()
		for a in self.includedvaccinationslist:
			self.vaccineslistbox.Append(a)
		self.vaccineslistbox.SetSelection(-1)
		self.removevaccinebutton.Disable()
	
	def AddVaccine(self, ID=False):
		
		choiceid = self.vaccinechoice.GetSelection()
		
		if choiceid == -1:
			
			choiceid = 0
		
		vaccine = self.vaccinationschoicelist[choiceid]
		
		if self.includedvaccinationslist.__contains__(vaccine) == False:
			
			self.includedvaccinationslist.append(vaccine)
			
			self.RefreshVaccineList()
	
	def VaccineSelected(self, ID=False):
		
		self.removevaccinebutton.Enable()
	
	def RemoveVaccine(self, ID=False):
		
		listboxid = self.vaccineslistbox.GetSelection()
		
		vaccine = self.includedvaccinationslist[listboxid]
		
		self.includedvaccinationslist.remove(vaccine)
		
		self.RefreshVaccineList()
	
	def Go(self, ID=False):
		
		busy = wx.BusyCursor()
		
		self.listbox.RefreshList()
		
		del busy
	
	def AnySpecies(self, ID=False):
		
		if self.speciestickbox.GetValue() == False:
			
			self.specieschoice.Enable()
			self.addspeciesbutton.Enable()
			self.specieslistbox.Enable()
			
		else:
			
			self.specieschoice.Disable()
			self.addspeciesbutton.Disable()
			self.specieslistbox.SetSelection(-1)
			self.removespeciesbutton.Disable()
			self.specieslistbox.Disable()
	
	def AnyVaccine(self, ID=False):
		
		if self.vaccinetickbox.GetValue() == False:
			
			self.vaccinechoice.Enable()
			self.addvaccinebutton.Enable()
			self.vaccineslistbox.Enable()
			
		else:
			
			self.vaccinechoice.Disable()
			self.addvaccinebutton.Disable()
			self.vaccineslistbox.SetSelection(-1)
			self.removevaccinebutton.Disable()
			self.vaccineslistbox.Disable()
	
	def EditAnimal(self, ID=False):
		
		listboxid = self.listbox.GetSelection()
		animalid = self.listbox.htmllist[listboxid][5]
		animaldata = animalmethods.AnimalSettings(self.localsettings, False, animalid)
		
		notebook = self.GetGrandParent().GetGrandParent()
		
		animalpanel = animalmethods.AnimalPanel(notebook, animaldata)
		notebook.AddPage(animalpanel)
	
	def EditOwner(self, ID=False):
		
		listboxid = self.listbox.GetSelection()
		clientid = self.listbox.htmllist[listboxid][6]
		clientdata = clientmethods.ClientSettings(self.localsettings, clientid)
		
		notebook = self.GetGrandParent().GetGrandParent()
		
		clientpanel = clientmethods.ClientPanel(notebook, clientdata)
		notebook.AddPage(clientpanel)
	
	def VaccinationSelected(self, ID=False):
		
		self.editanimalbutton.Enable()
		self.editownerbutton.Enable()
		self.createappointmentbutton.Enable()
	
	def CreateAppointment(self, ID=False):
		
		listboxid = self.listbox.GetSelection()
		animalid = self.listbox.htmllist[listboxid][5]
		vaccinationtype = self.listbox.htmllist[listboxid][2]
		duedate = self.listbox.htmllist[listboxid][4]
		duedate = miscmethods.GetWXDateFromSQLDate(duedate)
		
		appointmentdata = appointmentmethods.AppointmentSettings(self.localsettings, animalid, False)
		
		notebook = self.GetGrandParent().GetGrandParent()
		
		appointmentpanel = appointmentmethods.AppointmentPanel(notebook, appointmentdata)
		
		appointmentpanel.reasonentry.SetValue(vaccinationtype)
		appointmentpanel.appointmententry.SetValue(duedate)
		appointmentpanel.RefreshAppointment()
		
		
		
		notebook.AddPage(appointmentpanel)
	
	def GenerateCVSFile(self, ID=False):
		
		fromdate = self.fromdateentry.GetValue()
		fromdate = miscmethods.GetSQLDateFromWXDate(fromdate)
		todate = self.todateentry.GetValue()
		todate = miscmethods.GetSQLDateFromWXDate(todate)
		
		action = "SELECT client.ClientTitle, client.ClientSurname, client.ClientAddress, client.ClientPostcode, animal.Name, animal.Species, medication.Name, medicationout.NextDue AS NextDue FROM medicationout INNER JOIN appointment ON medicationout.AppointmentID = appointment.ID INNER JOIN animal ON appointment.AnimalID = animal.ID INNER JOIN client ON appointment.OwnerID = client.ID INNER JOIN medication ON medicationout.MedicationID = medication.ID WHERE medicationout.NextDue BETWEEN \"" + str(fromdate) + "\" AND \"" + str(todate) + "\""
		
		if self.vaccinetickbox.GetValue() == False:
			
			if len(self.includedvaccinationslist) == 0:
				
				action = action + " AND medication.Name IS NULL"
				
			else:
				
				action = action + " AND ("
				
				for a in self.includedvaccinationslist:
					
					action = action + "medication.Name = \"" + a + "\" OR "
				
				action = action[:-4]
				
				action = action + ")"
		
		if self.speciestickbox.GetValue() == False:
			
			if len(self.includedspecieslist) == 0:
				
				action = action + " AND animal.Species IS NULL"
				
			else:
				
				action = action + " AND ("
				
				for a in self.includedspecieslist:
					
					action = action + "animal.Species = \"" + a + "\" OR "
				
				action = action[:-4]
				
				action = action + ")"
		
		action = action + " UNION SELECT client.ClientTitle, client.ClientSurname, client.ClientAddress, client.ClientPostcode, animal.Name, animal.Species, manualvaccination.Name, manualvaccination.Next AS NextDue FROM manualvaccination INNER JOIN animal ON manualvaccination.AnimalID = animal.ID INNER JOIN client ON animal.OwnerID = client.ID WHERE manualvaccination.Next BETWEEN \"" + str(fromdate) + "\" AND \"" + str(todate) + "\""
		
		if self.vaccinetickbox.GetValue() == False:
			
			if len(self.includedvaccinationslist) == 0:
				
				action = action + " AND manualvaccination.Name IS NULL"
				
			else:
				
				action = action + " AND ("
				
				for a in self.includedvaccinationslist:
					
					action = action + "manualvaccination.Name = \"" + a + "\" OR "
				
				action = action[:-4]
				
				action = action + ")"
		
		if self.speciestickbox.GetValue() == False:
			
			if len(self.includedspecieslist) == 0:
				
				action = action + " AND animal.Species IS NULL"
				
			else:
				
				action = action + " AND ("
				
				for a in self.includedspecieslist:
					
					action = action + "animal.Species = \"" + a + "\" OR "
				
				action = action[:-4]
				
				action = action + ")"
		
		action = action + " ORDER BY NextDue desc"
		
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		output = "\"title\",\"surname\",\"address\",\"postcode\",\"animalname\",\"species\",\"vaccinationtype\",\"duedate\"\n"
		
		for a in results:
			
			for b in range(0, len(a)):
				
				if b == 7:
					
					duedate = a[b]
					duedate = miscmethods.FormatSQLDate(duedate, self.localsettings)
					output = output + "\"" + str(duedate) + "\","
					
				elif b == 2:
					
					address = a[b]#.replace("\n", ", ")
					output = output + "\"" + str(address) + "\","
					
				else:
					
					output = output + "\"" + str(a[b]) + "\","
			
			output = output[:-1] + "\n"
		
		output = output[:-1]
		
		path = wx.SaveFileSelector("CSV", "csv", "duevaccinations.csv")
		
		out = open(path, "w")
		out.write(output)
		out.close()
		
		miscmethods.ShowMessage(self.t("csvsavedtolabel") + " " + path)

class VaccineMailShotListbox(wx.HtmlListBox):
	
	def __init__(self, parent, localsettings):
		
		wx.HtmlListBox.__init__(self, parent, -1)
		
		self.htmllist = []
		self.localsettings = localsettings
		self.parent = parent
		self.SetItemCount(0)
		self.SetSelection(-1)
	
	def OnGetItem(self, n):
		
		if len(self.htmllist) != 0:
			
			name = self.htmllist[n][0]
			surname = self.htmllist[n][1]
			vaccine = self.htmllist[n][2]
			date = self.htmllist[n][4]
			date = miscmethods.GetDateFromSQLDate(date)
			date = miscmethods.FormatDate(date, self.localsettings)
			
			return "<table width=100% cellspacing=0 cellpadding=0><tr><td align=left><font color=blue size=5><b>" + name + " " + surname + "</b> - " + vaccine + "</font></td><td align=right><font color=red size=5><b>" + str(date) + "</b></font>&nbsp;</td></tr></table>"
	
	def RefreshList(self, ID=False):
		
		self.Hide()
		
		self.SetSelection(-1)
		
		fromdate = self.parent.fromdateentry.GetValue()
		fromdate = miscmethods.GetSQLDateFromWXDate(fromdate)
		todate = self.parent.todateentry.GetValue()
		todate = miscmethods.GetSQLDateFromWXDate(todate)
		
		action = "SELECT animal.Name, client.ClientSurname, medication.Name, animal.Species, medicationout.NextDue AS NextDue, animal.ID, client.ID FROM medicationout INNER JOIN appointment ON medicationout.AppointmentID = appointment.ID INNER JOIN animal ON appointment.AnimalID = animal.ID INNER JOIN client ON appointment.OwnerID = client.ID INNER JOIN medication ON medicationout.MedicationID = medication.ID WHERE medicationout.NextDue BETWEEN \"" + str(fromdate) + "\" AND \"" + str(todate) + "\""
		
		if self.parent.vaccinetickbox.GetValue() == False:
			
			if len(self.parent.includedvaccinationslist) == 0:
				
				action = action + " AND medication.Name IS NULL"
				
			else:
				
				action = action + " AND ("
				
				for a in self.parent.includedvaccinationslist:
					
					action = action + "medication.Name = \"" + a + "\" OR "
				
				action = action[:-4]
				
				action = action + ")"
		
		if self.parent.speciestickbox.GetValue() == False:
			
			if len(self.parent.includedspecieslist) == 0:
				
				action = action + " AND animal.Species IS NULL"
				
			else:
				
				action = action + " AND ("
				
				for a in self.parent.includedspecieslist:
					
					action = action + "animal.Species = \"" + a + "\" OR "
				
				action = action[:-4]
				
				action = action + ")"
		
		action = action + " UNION SELECT animal.Name, client.ClientSurname, manualvaccination.Name, animal.Species, manualvaccination.Next AS NextDue, animal.ID, client.ID FROM manualvaccination INNER JOIN animal ON manualvaccination.AnimalID = animal.ID INNER JOIN client ON animal.OwnerID = client.ID WHERE manualvaccination.Next BETWEEN \"" + str(fromdate) + "\" AND \"" + str(todate) + "\""
		
		if self.parent.vaccinetickbox.GetValue() == False:
			
			if len(self.parent.includedvaccinationslist) == 0:
				
				action = action + " AND manualvaccination.Name IS NULL"
				
			else:
				
				action = action + " AND ("
				
				for a in self.parent.includedvaccinationslist:
					
					action = action + "manualvaccination.Name = \"" + a + "\" OR "
				
				action = action[:-4]
				
				action = action + ")"
		
		if self.parent.speciestickbox.GetValue() == False:
			
			if len(self.parent.includedspecieslist) == 0:
				
				action = action + " AND animal.Species IS NULL"
				
			else:
				
				action = action + " AND ("
				
				for a in self.parent.includedspecieslist:
					
					action = action + "animal.Species = \"" + a + "\" OR "
				
				action = action[:-4]
				
				action = action + ")"
		
		action = action + " ORDER BY NextDue desc"
		
		self.htmllist = db.SendSQL(action, self.parent.localsettings.dbconnection)
		
		self.SetItemCount(len(self.htmllist))
		
		if len(self.htmllist) == 0:
			self.Disable()
			self.parent.generatecvsbutton.Disable()
		else:
			self.Enable()
			self.parent.generatecvsbutton.Enable()
		
		self.Show()
		
		self.parent.editanimalbutton.Disable()
		self.parent.editownerbutton.Disable()
		self.parent.createappointmentbutton.Disable()
		
		self.parent.totallabel.SetLabel(self.parent.t("totallabel") + ": " + str(len(self.htmllist)) + " ")
		self.parent.rightsizer.Layout()
