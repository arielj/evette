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
import wx.html
import miscmethods
import datetime
import animalmethods
import clientmethods
import db
import dbmethods
import customwidgets

class AppointmentSettings:
	
	def __init__(self, localsettings, animalid, ID):
		
		#(ID, AnimalID, OwnerID, Date, Time, AppointmentReason, Arrived, WithVet, Problem, Notes, Plan, Done, Operation, Vet)
		
		self.localsettings = localsettings
		
		
		
		if ID == False:
			
			self.ID = False
			self.animalid = animalid
			
			self.animaldata = animalmethods.AnimalSettings(self.localsettings, False, self.animalid)
			
			self.clientdata = clientmethods.ClientSettings(self.localsettings, self.animaldata.ownerid)
			
			self.ownerid = self.clientdata.ID
			self.date = datetime.date.today()
			self.date = miscmethods.GetSQLDateFromDate(self.date)
			self.time = "14:00"
			self.reason = "Checkover"
			self.arrived = 0
			self.withvet = 0
			self.problem = ""
			self.notes = ""
			self.plan = ""
			self.done = 0
			self.operation = 0
			self.vet = "None"
			currenttime = datetime.datetime.today().strftime("%x %X")
			self.changelog = str(currenttime) + "%%%" + str(self.localsettings.userid)
		else:
			
			action = "SELECT * FROM appointment WHERE ID = " + str(ID)
			results = db.SendSQL(action, localsettings.dbconnection)
			
			self.ID = ID
			self.animalid = results[0][1]
			self.ownerid = results[0][2]
			self.date = results[0][3]
			self.time = results[0][4]
			self.reason = results[0][5]
			self.arrived = results[0][6]
			self.withvet = results[0][7]
			self.problem = results[0][8]
			self.notes = results[0][9]
			self.plan = results[0][10]
			self.done = results[0][11]
			self.operation = results[0][12]
			self.vet = results[0][13]
			self.changelog = results[0][14]
			
			self.animaldata = animalmethods.AnimalSettings(self.localsettings, False, self.animalid)
			self.clientdata = clientmethods.ClientSettings(self.localsettings, self.animaldata.ownerid)
	
	def Submit(self):
		
		currenttime = datetime.datetime.today().strftime("%x %X")
		userid = self.localsettings.userid
		
		if self.changelog == "":
			self.changelog = currenttime + "%%%" + str(userid)
		else:
			self.changelog = currenttime + "%%%" + str(userid) + "$$$" + self.changelog
		
		self.ID = dbmethods.WriteToAppointmentTable(self.localsettings.dbconnection, self)
		

class AppointmentPanel(wx.Panel):
	
	def t(self, field, idx = 0):
		return  self.appointmentdata.localsettings.t(field,idx)
	
	def __init__(self, notebook, appointmentdata):
		
		self.appointmentdata = appointmentdata
		
		wx.Panel.__init__(self, notebook)
		
		self.viewappointmentspanel = False
		
		if self.appointmentdata.operation == 0:
			pagetitle = self.t("appointmentappointmentforlabel") + " " + self.appointmentdata.animaldata.name + " " + self.appointmentdata.clientdata.surname
		else:
			pagetitle = self.t("appointmentoperationforlabel") + " " + self.appointmentdata.animaldata.name + " " + self.appointmentdata.clientdata.surname
		self.pagetitle = miscmethods.GetPageTitle(notebook, pagetitle)
		
		datesizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.appointmententry = customwidgets.DateCtrl(self, self.appointmentdata)
		appointmentdate = miscmethods.GetWXDateFromSQLDate(self.appointmentdata.date)
		self.appointmententry.SetValue(appointmentdate)
		
		action = "SELECT Name FROM user WHERE Position = \"Vet\" OR Position = \"Manager\""
		results = db.SendSQL(action, self.appointmentdata.localsettings.dbconnection)
		
		vets = []
		if len(results) != 0:
			for a in results:
				vets.append(a[0])
		
		self.vetcombobox = wx.ComboBox(self, -1, "Vet", choices=vets)
		if self.appointmentdata.vet != "None":
			self.vetcombobox.SetValue(str(self.appointmentdata.vet))
		self.vetcombobox.Bind(wx.EVT_CHAR, self.UseVetComboBox)
		self.vetcombobox.SetToolTipString(self.t("appointmententervettooltip"))
		
		
		refreshbitmap = wx.Bitmap("icons/refresh.png")
		refreshappointmentsbutton = wx.BitmapButton(self, -1, refreshbitmap)
		refreshappointmentsbutton.Bind(wx.EVT_BUTTON, self.RefreshAppointment)
		refreshappointmentsbutton.SetToolTipString(self.t("appointmentrefreshtooltip"))
		
		datesizer.Add(self.appointmententry, 1, wx.EXPAND)
		datesizer.Add(self.vetcombobox, 1, wx.EXPAND)
		datesizer.Add(refreshappointmentsbutton, 0, wx.ALIGN_LEFT)
		
		reasonsizer = wx.BoxSizer(wx.VERTICAL)
		self.reasonlabel = wx.StaticText(self, -1, self.t("appointmentreasonlabel"))
		reasonsizer.Add(self.reasonlabel, 0, wx.ALIGN_LEFT)
		
		self.reasonentry = wx.TextCtrl(self, -1, self.appointmentdata.reason, style=wx.TE_MULTILINE, size=(-1,100))
		self.reasonentry.SetFocus()
		
		reasonsizer.Add(self.reasonentry, 0, wx.EXPAND)
		
		searchsizer = wx.BoxSizer(wx.VERTICAL)
		searchsizer.Add(datesizer, 0, wx.EXPAND)
		searchsizer.Add(reasonsizer, 0, wx.EXPAND)
		
		searchspacer2 = wx.StaticText(self, -1, "", size=(-1,10))
		searchsizer.Add(searchspacer2, 0, wx.EXPAND)
		
		appointmenttimesizer = wx.BoxSizer(wx.HORIZONTAL)
		self.appointmenttimelabel = wx.StaticText(self, -1, self.t("appointmenttimelabel"))
		
		time = str(self.appointmentdata.time)
		
		if len(str(time)) == 7:
			time = "0" + time[:4]
		else:
			time = time[:5]
		
		self.appointmenttimeentry = wx.TextCtrl(self, -1, time)
		appointmenttimesizer.Add(self.appointmenttimelabel, 0, wx.ALIGN_CENTER)
		appointmenttimesizer.Add(self.appointmenttimeentry, 0, wx.EXPAND)
		
		appointmenttimespacer = wx.StaticText(self, -1, "")
		appointmenttimesizer.Add(appointmenttimespacer, 1, wx.EXPAND)
		
		self.opcheckbox = wx.CheckBox(self, -1, self.t("appointmentisopcheckbox", 0))
		self.opcheckbox.Bind(wx.EVT_CHECKBOX, self.SwitchToOps)
		self.opcheckbox.SetToolTipString(self.t("appointmentisopcheckbox", 1))
		appointmenttimesizer.Add(self.opcheckbox, 0, wx.ALIGN_CENTER)
		
		appointmenttimespacer1 = wx.StaticText(self, -1, "")
		appointmenttimesizer.Add(appointmenttimespacer1, 1, wx.EXPAND)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		appointmentsubmitbutton = wx.BitmapButton(self, -1, submitbitmap)
		appointmentsubmitbutton.Bind(wx.EVT_BUTTON, self.Submit)
		appointmentsubmitbutton.SetToolTipString(self.t("appointmentsubmittooltip"))
		appointmenttimesizer.Add(appointmentsubmitbutton)
		
		searchsizer.Add(appointmenttimesizer, 0, wx.EXPAND)
		
		searchspacer3 = wx.StaticText(self, -1, "", size=(-1,10))
		searchsizer.Add(searchspacer3, 0, wx.EXPAND)
		
		buttonssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		deletebitmap = wx.Bitmap("icons/delete.png")
		deletebutton = wx.BitmapButton(self, -1, deletebitmap)
		deletebutton.SetToolTipString(self.t("appointmentdeletetooltip"))
		deletebutton.Bind(wx.EVT_BUTTON, self.Delete)
		buttonssizer.Add(deletebutton, 0, wx.EXPAND)
		
		if self.appointmentdata.localsettings.deleteappointments == 0:
			deletebutton.Disable()
		
		buttonsspacer = wx.StaticText(self, -1, "")
		buttonssizer.Add(buttonsspacer, 1, wx.EXPAND)
		
		statuslabel = wx.StaticText(self, -1, self.t("appointmentstatuslabel"))
		buttonssizer.Add(statuslabel, 0, wx.ALIGN_CENTER)
		
		statuschoice = wx.Choice(self, -1, choices=(self.t("appointmentnotarrivedlabel"), self.t("appointmentwaitinglabel"), self.t("appointmentwithvetlabel"), self.t("appointmentdonelabel")))
		if self.appointmentdata.done == 1:
			statuschoice.SetSelection(3)
		elif self.appointmentdata.withvet == 1:
			statuschoice.SetSelection(2)
		elif self.appointmentdata.arrived == 1:
			statuschoice.SetSelection(1)
		else:
			statuschoice.SetSelection(0)
		
		buttonssizer.Add(statuschoice, 0, wx.EXPAND)
		
		searchsizer.Add(buttonssizer, 0, wx.EXPAND)
		
		searchspacer = wx.StaticText(self, -1, "", size=(-1,10))
		searchsizer.Add(searchspacer, 0, wx.EXPAND)
		
		owneranimalsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		editownerbutton = wx.Button(self, -1, self.t("appointmenteditownerbutton", 0))
		editownerbutton.SetForegroundColour("blue")
		editownerbutton.SetToolTipString(self.t("appointmenteditownerbutton", 1))
		editownerbutton.Bind(wx.EVT_BUTTON, self.OpenClientRecord)
		owneranimalsizer.Add(editownerbutton, 0, wx.EXPAND)
		
		if self.appointmentdata.localsettings.editclients == 0:
			editownerbutton.Disable()
		
		owneranimalspacer = wx.StaticText(self, -1, "")
		owneranimalsizer.Add(owneranimalspacer, 1, wx.EXPAND)
		
		editanimalbutton = wx.Button(self, -1, self.t("appointmenteditanimalbutton", 0))
		editanimalbutton.SetForegroundColour("blue")
		editanimalbutton.SetToolTipString(self.t("appointmenteditanimalbutton", 1))
		editanimalbutton.Bind(wx.EVT_BUTTON, self.OpenAnimalRecord)
		owneranimalsizer.Add(editanimalbutton, 0, wx.EXPAND)
		
		if self.appointmentdata.localsettings.editanimals == 0:
			editanimalbutton.Disable()
		
		searchsizer.Add(owneranimalsizer, 0, wx.EXPAND)
		
		searchspacer1 = wx.StaticText(self, -1, "")
		searchsizer.Add(searchspacer1, 1, wx.EXPAND)
		
		#Right hand pane
		
		date = self.appointmententry.GetValue()
		date = miscmethods.GetDateFromWXDate(date)
		date = miscmethods.FormatDate(date, self.appointmentdata.localsettings)
		
		appointmentslistboxlabeltext = self.t("appointmentappointmentsforlabel") + " "  + str(date)
		
		self.appointmentslistboxlabel = wx.StaticText(self, -1, appointmentslistboxlabeltext)
		
		self.appointmentslistbox = customwidgets.DayPlannerListbox(self, appointmentdata.localsettings, date, 10)
		self.appointmentslistbox.Bind(wx.EVT_LISTBOX_DCLICK, self.GetTime)
		
		appointmentslistboxsizer = wx.BoxSizer(wx.VERTICAL)
		
		appointmentslistboxsizer.Add(self.appointmentslistboxlabel, 0, wx.EXPAND)
		appointmentslistboxsizer.Add(self.appointmentslistbox, 1, wx.EXPAND)
		
		self.appointmentlistboxtotal = wx.StaticText(self, -1, self.t("totallabel") + ": 0")
		appointmentslistboxsizer.Add(self.appointmentlistboxtotal, 0, wx.ALIGN_RIGHT)
		
		mainsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		mainsizer.Add(searchsizer, 1, wx.EXPAND)
		
		spacer = wx.StaticText(self, -1, "", size=(50,-1))
		mainsizer.Add(spacer, 0, wx.EXPAND)
		
		mainsizer.Add(appointmentslistboxsizer, 2, wx.EXPAND)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		closebuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		closebuttonspacer2 = wx.StaticText(self, -1, "")
		closebuttonsizer.Add(closebuttonspacer2, 1, wx.EXPAND)
		
		topsizer.Add(closebuttonsizer, 0, wx.EXPAND)
		topsizer.Add(mainsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.appointmentslistboxsizer = appointmentslistboxsizer
		self.statuschoice = statuschoice
		
		if self.appointmentdata.operation == 1:
			self.opcheckbox.SetValue(True)
			self.SwitchToOps()
		
		self.RefreshAppointment()
	
	def UseVetComboBox(self, ID=False):
		
		parent = ID.GetEventObject()
		
		if parent.GetValue() == "Vet":
			parent.SetValue("")
		
		ID.Skip()
	
	def RefreshTotal(self, ID=False):
		
		date = self.appointmententry.GetValue()
		sqldate = miscmethods.GetSQLDateFromWXDate(date)
		
		if self.opcheckbox.GetValue() == True:
			operation = 1
		else:
			operation = 0
		
		action = "SELECT ID FROM appointment WHERE appointment.Date = \"" + sqldate + "\" AND appointment.Operation = " + str(operation)
		results = db.SendSQL(action, self.appointmentdata.localsettings.dbconnection)
		
		
		total = len(results)
		
		self.appointmentlistboxtotal.SetLabel(self.t("totallabel") + ": " + str(total))
		
		self.appointmentslistboxsizer.Layout()
	
	def SwitchToOps(self, ID=False):
		
		isop = self.opcheckbox.GetValue()
		date = self.appointmententry.GetValue()
		
		weekday = date.GetWeekDay()
		weekday = miscmethods.GetDayNameFromID(weekday, self.appointmentdata.localsettings)
		sqldate = miscmethods.GetSQLDateFromWXDate(date)
		datestring = miscmethods.GetDateFromWXDate(date)
		datestring = miscmethods.FormatDate(datestring, self.appointmentdata.localsettings)
		
		
		
		if isop == True:
			self.appointmenttimeentry.SetValue("09:00")
			self.appointmenttimeentry.Disable()
			
		else:
			self.appointmenttimeentry.Enable()
		
		self.RefreshAppointment()
		self.RefreshTotal()
	
	def Submit(self, ID):
		
		if self.opcheckbox.GetValue() == True:
			self.SubmitOperation(ID)
		else:
			self.SubmitAppointment(ID)
	
	def SubmitOperation(self, ID):
		
		
		self.appointmentdata.date = miscmethods.GetSQLDateFromWXDate(self.appointmententry.GetValue())
		self.appointmentdata.time = self.appointmentdata.localsettings.operationtime
		self.appointmentdata.vet = self.vetcombobox.GetValue()
		
		self.appointmentdata.reason = self.reasonentry.GetValue()
		self.appointmentdata.operation = 1
		
		choice = self.statuschoice.GetSelection()
		
		if choice == 0:
			self.appointmentdata.arrived = 0
			self.appointmentdata.withvet = 0
			self.appointmentdata.done = 0
		elif choice == 1:
			self.appointmentdata.arrived = 1
			self.appointmentdata.withvet = 0
			self.appointmentdata.done = 0
		elif choice == 2:
			self.appointmentdata.arrived = 1
			self.appointmentdata.withvet = 1
			self.appointmentdata.done = 0
		elif choice == 3:
			self.appointmentdata.arrived = 1
			self.appointmentdata.withvet = 0
			self.appointmentdata.done = 1
		
		self.appointmentdata.Submit()
		
		try:
			self.parent.RefreshAppointments()
		except:
			miscmethods.LogException()
		
		self.Close()
	
	def SubmitAppointment(self, ID):
		
		time = self.appointmenttimeentry.GetValue()
		
		success = False
		
		if miscmethods.ValidateTime(time) == True:
			
			if miscmethods.GetMinutesFromTime(time) < miscmethods.GetMinutesFromTime(self.appointmentdata.localsettings.opento) + 1:
				
				if miscmethods.GetMinutesFromTime(time) > miscmethods.GetMinutesFromTime(self.appointmentdata.localsettings.openfrom) - 1:
					
					time = time[:2] + ":" + time[3:5]
					success = True
				else:
					failurereason = self.t("appointmenttimetooearlymessage")
			else:
				failurereason = self.t("appointmenttimetoolatemessage")
		else:
			failurereason = self.t("appointmentinvalidtimemessage")
		
		if success == True:
			
			self.appointmentdata.date = miscmethods.GetSQLDateFromWXDate(self.appointmententry.GetValue())
			self.appointmentdata.time = time
			
			self.appointmentdata.reason = self.reasonentry.GetValue()
			self.appointmentdata.operation = 0
			if self.vetcombobox.GetValue() == "Vet":
				self.appointmentdata.vet = "None"
			else:
				self.appointmentdata.vet = self.vetcombobox.GetValue()
			
			choice = self.statuschoice.GetSelection()
			
			if choice == 0:
				self.appointmentdata.arrived = 0
				self.appointmentdata.withvet = 0
				self.appointmentdata.done = 0
			elif choice == 1:
				self.appointmentdata.arrived = 1
				self.appointmentdata.withvet = 0
				self.appointmentdata.done = 0
			elif choice == 2:
				self.appointmentdata.arrived = 1
				self.appointmentdata.withvet = 1
				self.appointmentdata.done = 0
			elif choice == 3:
				self.appointmentdata.arrived = 1
				self.appointmentdata.withvet = 0
				self.appointmentdata.done = 1
			
			self.appointmentdata.Submit()
			
			try:
				self.parent.RefreshAppointments()
			except:
				miscmethods.LogException()
			
			self.Close()
			
		else:
			
			miscmethods.ShowMessage(failurereason)
	
	def RefreshAppointment(self, ID=False):
		
		localsettings = self.appointmentdata.localsettings
		
		date = self.appointmententry.GetValue()
		weekday = date.GetWeekDay()
		weekday = miscmethods.GetDayNameFromID(weekday, self.appointmentdata.localsettings)
		sqldate = miscmethods.GetSQLDateFromWXDate(date)
		datestring = miscmethods.GetDateFromWXDate(date)
		datestring = miscmethods.FormatDate(datestring, self.appointmentdata.localsettings)
		
		isop = self.opcheckbox.GetValue()
		
		if isop == True:
			appointmentslistboxlabeltext = self.t("appointmentoperationsforlabel") + " " + weekday + " " + str(datestring)
		else:
			appointmentslistboxlabeltext = self.t("appointmentappointmentsforlabel") + " " + weekday + " " + str(datestring)
		self.appointmentslistboxlabel.SetLabel(appointmentslistboxlabeltext)
		
		self.appointmentslistbox.sqldate = sqldate
		
		self.appointmentslistbox.RefreshList()
		
		self.RefreshTotal()
	
	def GetTime(self,ID):
		
		listboxid = self.appointmentslistbox.GetSelection()
		
		action = "SELECT * FROM settings"
		results = db.SendSQL(action, self.appointmentdata.localsettings.dbconnection)
		
		
		openfromraw = results[0][2]
		openfromtime = ( int(str(openfromraw)[:2]) * 60 ) + int(str(openfromraw)[3:5])
		
		appointmenttime = openfromtime + (listboxid * 10)
		appointmenttime = miscmethods.GetTimeFromMinutes(appointmenttime)[:5]
		
		self.appointmenttimeentry.SetValue(appointmenttime)
	
	def Delete(self, ID):
		
		if miscmethods.ConfirmMessage("Are you sure that you want to delete this appointment?") == True:
			
			action = "DELETE FROM appointment WHERE ID = " + str(self.appointmentdata.ID)
			db.SendSQL(action, self.appointmentdata.localsettings.dbconnection)
			
			
			self.Close(self)
	
	def OpenAnimalRecord(self, ID):
		
		notebook = ID.GetEventObject().GetGrandParent()
		
		animaldata = self.appointmentdata.animaldata
		
		animalpanel = animalmethods.AnimalPanel(notebook, animaldata)
		
		notebook.AddPage(animalpanel)
	
	def OpenClientRecord(self, ID):
		
		notebook = ID.GetEventObject().GetGrandParent()
		
		clientdata = self.appointmentdata.clientdata
		
		clientpanel = clientmethods.ClientPanel(notebook, clientdata)
		
		notebook.AddPage(clientpanel)
	
	def Close(self, ID=False):
		
		if self.viewappointmentspanel != False:
			self.viewappointmentspanel.RefreshLists()
		
		miscmethods.ClosePanel(self)
