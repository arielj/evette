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
import db
import dbmethods
import datetime
import appointmentmethods
import clientmethods
import customwidgets
import formmethods
import vetmethods
import diarymethods
import os
import threading
import sys
import medicationmethods
import lostandfound
import attachedfilemethods

ADD_LOST = 4001
ADD_FOUND = 4002
EDIT_LOST_AND_FOUND = 4003
EDIT_OWNER = 4004
EVETTE_ANIMAL_NAME_SYNC = 4005
ASM_ANIMAL_NAME_SYNC = 4006
EVETTE_ANIMAL_DOB_SYNC = 4007
ASM_ANIMAL_DOB_SYNC = 4008
EVETTE_ANIMAL_CHIPNO_SYNC = 4009
ASM_ANIMAL_CHIPNO_SYNC = 4010
EVETTE_ANIMAL_DECEASEDDATE_SYNC = 4011
ASM_ANIMAL_DECEASEDDATE_SYNC = 4012
IMPORT_NEW_ASM_OWNER = 4013
UPDATE_OWNER_ASM_SYNC = 4014
UPDATE_OWNER_EVETTE_SYNC = 4015
CHANGE_OWNER = 4016
ADD_APPOINTMENT = 4017
EDIT_APPOINTMENT = 4018
DELETE_APPOINTMENT = 4019
REFRESH_APPOINTMENTS = 4020
PRINT_APPOINTMENT = 4021
VET_FORM = 4022
VIEW_APPOINTMENT = 4023
APPOINTMENT_CHANGELOG = 4024
ADD_VACCINATION = 4025
EDIT_VACCINATION = 4026
DELETE_VACCINATION = 4027
REFRESH_VACCINATIONS = 4028
ADD_WEIGHT = 4029
EDIT_WEIGHT = 4030
DELETE_WEIGHT = 4031
REFRESH_WEIGHTS = 4032

class AnimalSettings:
	
	def __init__(self, localsettings, ownerid=False, ID=False):
		
		#(ID, OwnerID, Name, Sex, Species, Breed, Colour, DOB, Comments, Neutered, ChipNo)
		
		self.localsettings = localsettings
		
		if ID == False:
			self.ID = ID
			self.ownerid = ownerid
			self.name = u""
			self.sex = 0
			self.species = u""
			self.breed = u""
			self.colour = u""
			self.dob = u""
			self.comments = u""
			self.neutered = 0
			self.chipno = ""
			self.deceased = False
			self.deceaseddate = "0000-00-00"
			self.causeofdeath = u""
			currenttime = datetime.datetime.today().strftime("%x %X")
			self.changelog = str(currenttime) + "%%%" + str(self.localsettings.userid)
			self.asmref = ""
		else:
			
			action = "SELECT * FROM animal WHERE ID = " + str(ID)
			results = db.SendSQL(action, localsettings.dbconnection)
			
			self.ID = ID
			self.ownerid = results[0][1]
			self.name = unicode(results[0][2], "utf8")
			self.sex = results[0][3]
			self.species = unicode(results[0][4], "utf8")
			self.breed = unicode(results[0][5], "utf8")
			self.colour = unicode(results[0][6], "utf8")
			self.dob = unicode(results[0][7], "utf8")
			self.comments = unicode(results[0][8], "utf8")
			self.neutered = results[0][9]
			self.chipno = results[0][10]
			self.changelog = results[0][11]
			self.deceased = results[0][12]
			
			self.deceaseddate = results[0][13]
			
			if self.deceaseddate == None:
				
				self.deceaseddate = "0000-00-00"
			
			self.causeofdeath = unicode(results[0][14], "utf8")
			self.asmref = results[0][15]
	
	def Submit(self):
		
		locked = False
		
		if self.ID != False:
			
			action = "SELECT ChangeLog FROM animal WHERE ID = " + str(self.ID)
			changelog = db.SendSQL(action, self.localsettings.dbconnection)[0][0]
			
			if changelog != self.changelog:
				
				locked = True
				
				miscmethods.ShowMessage(self.localsettings.dictionary["filealteredmessage"][self.localsettings.language])
		
		if locked == False:
			
			currenttime = datetime.datetime.today().strftime("%x %X")
			userid = self.localsettings.userid
			
			if self.changelog == "":
				
				self.changelog = currenttime + "%%%" + str(userid)
			else:
				self.changelog = currenttime + "%%%" + str(userid) + "$$$" + self.changelog
			
			dbmethods.WriteToAnimalTable(self.localsettings.dbconnection, self)

class AnimalPanel(wx.Panel):
	
	def t(self, field, idx = 0):
		return  self.animaldata.localsettings.t(field, idx)
	
	def __init__(self, notebook, animaldata, clientpanel=False):
		
		busy = wx.BusyCursor()
		
		self.animaldata = animaldata
		
		self.clientpanel = clientpanel
		
		self.clientdata = clientmethods.ClientSettings(self.animaldata.localsettings, self.animaldata.ownerid)
		
		if self.animaldata.ID == False:
			
			self.pagetitle = self.t("newanimalpagetitle")
			
		else:
			
			self.pagetitle = animaldata.name + " " + self.clientdata.surname
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, self.pagetitle)
		self.pageimage = "icons/editanimal.png"
		
		wx.Panel.__init__(self, notebook)
		
		lostandfound = wx.StaticText(self, -1, "")
		
		action = "SELECT ID, LostOrFound FROM lostandfound WHERE AnimalID = " + str(animaldata.ID) + " AND DateComplete = \"0000-00-00\""
		results = db.SendSQL(action, animaldata.localsettings.dbconnection)
		
		if len(results) > 0 and animaldata.ID > 0:
			
			self.animallostorfound = True
			
			#font = lostandfound.GetFont()
			#font.SetPointSize(font.GetPointSize() + 2)
			#lostandfound.SetFont(font)
			lostandfound.SetForegroundColour("red")
			
			if results[0][1] == 0:
				
				lostandfound.SetLabel(miscmethods.NoWrap(self.t("lostanimallabel") + ": " + str(results[0][0])))
				
			else:
				
				lostandfound.SetLabel(miscmethods.NoWrap(self.t("foundanimallabel") + ": " + str(results[0][0])))
			
			lostandfound.Bind(wx.EVT_RIGHT_DOWN, self.LostAndFoundPopup)
			
			lostandfound.ID = results[0][0]
			
		else:
			
			self.animallostorfound = False
		
		fields = ( (animaldata.name, self.t("animalnamelabel"), "small"), (animaldata.sex, self.t("animalsexlabel"), "sex"), (animaldata.species, self.t("animalspecieslabel"), "species"), (animaldata.breed, self.t("animalbreedlabel"), "breed"), (animaldata.colour, self.t("animalcolourlabel"), "colour"), (animaldata.dob, self.t("animaldoblabel"), "small"), (animaldata.chipno, self.t("animalchipnolabel"), "small"), (animaldata.comments, self.t("animalcommentslabel"), "large") )
		
		#noofrows = len(fields) + 1
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		#sizer.AddGrowableCol(1)
		#sizer.AddGrowableRow(8)
		
		#labels = []
		#inputfields = []
		
		label = wx.StaticText(self, -1, self.t("animalownerlabel") + ": ", style=wx.ALIGN_RIGHT)
		font = label.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		label.SetFont(font)
		sizer.Add(label, 0, wx.ALIGN_LEFT)
		
		ownerdetailssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		ownername = self.clientdata.title + " " + self.clientdata.surname + " "
		ownernamelabel = wx.StaticText(self, -1, ownername)
		font = ownernamelabel.GetFont()
		font.SetPointSize(font.GetPointSize() + 3)
		ownernamelabel.SetFont(font)
		ownernamelabel.SetForegroundColour("blue")
		ownernamelabel.SetToolTipString(self.t("rightclickformenutooltip"))
		ownernamelabel.Bind(wx.EVT_RIGHT_DOWN, self.OwnerPopup)
		ownerdetailssizer.Add(ownernamelabel, 1, wx.ALIGN_CENTER)
		
		sizer.Add(ownerdetailssizer, 0, wx.EXPAND)
		
		namelabel = wx.StaticText(self, -1, self.t("animalnamelabel") + ":")
		font = namelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		namelabel.SetFont(font)
		sizer.Add(namelabel, 0, wx.EXPAND)
		
		nameentry = wx.TextCtrl(self, -1, animaldata.name)
		nameentry.Bind(wx.EVT_CHAR, self.EnableSave)
		sizer.Add(nameentry, 0, wx.EXPAND)
		
		sexlabel = wx.StaticText(self, -1, self.t("animalsexlabel") + ":")
		sexlabel.SetFont(font)
		sizer.Add(sexlabel, 0, wx.EXPAND)
		
		sexsizer  = wx.BoxSizer(wx.HORIZONTAL)
		
		sexentry = wx.Choice(self, -1, choices=(self.t("unknownlabel"), self.t("malelabel"), self.t("femalelabel")))
		sexentry.SetSelection(self.animaldata.sex)
		sexentry.Bind(wx.EVT_CHAR, self.EnableSave)
		sexentry.Bind(wx.EVT_CHOICE, self.EnableSave)
		sexsizer.Add(sexentry, 1, wx.EXPAND)
		
		self.neuteredcheckbox = wx.CheckBox(self, -1, self.t("neuteredlabel"))
		self.neuteredcheckbox.SetFont(font)
		self.neuteredcheckbox.Bind(wx.EVT_CHECKBOX, self.EnableSave)
		self.neuteredcheckbox.SetToolTipString(self.t("animalneuteredtooltip"))
		sexsizer.Add(self.neuteredcheckbox, 0, wx.EXPAND)
		
		if self.animaldata.neutered == 1:
			self.neuteredcheckbox.SetValue(True)
		
		sizer.Add(sexsizer, 0, wx.EXPAND)
		
		specieslabel = wx.StaticText(self, -1, self.t("animalspecieslabel") + ":")
		specieslabel.SetFont(font)
		sizer.Add(specieslabel, 0, wx.EXPAND)
		
		specieslist = self.GetLookupsList("species")
		speciesentry = wx.ComboBox(self, -1, animaldata.species, choices=specieslist)
		speciesentry.Bind(wx.EVT_CHAR, self.EnableSave)
		speciesentry.Bind(wx.EVT_COMBOBOX, self.EnableSave)
		sizer.Add(speciesentry, 0, wx.EXPAND)
		
		breedlabel = wx.StaticText(self, -1, self.t("animalbreedlabel") + ":")
		breedlabel.SetFont(font)
		sizer.Add(breedlabel, 0, wx.EXPAND)
		
		breedlist = self.GetLookupsList("breed")
		breedentry = wx.ComboBox(self, -1, animaldata.breed, choices=breedlist)
		breedentry.Bind(wx.EVT_CHAR, self.EnableSave)
		breedentry.Bind(wx.EVT_COMBOBOX, self.EnableSave)
		sizer.Add(breedentry, 0, wx.EXPAND)
		
		colourlabel = wx.StaticText(self, -1, self.t("animalcolourlabel") + ":")
		colourlabel.SetFont(font)
		sizer.Add(colourlabel, 0, wx.EXPAND)
		
		colourlist = self.GetLookupsList("colour")
		colourentry = wx.ComboBox(self, -1, animaldata.colour, choices=colourlist)
		colourentry.Bind(wx.EVT_CHAR, self.EnableSave)
		colourentry.Bind(wx.EVT_COMBOBOX, self.EnableSave)
		sizer.Add(colourentry, 0, wx.EXPAND)
		
		chipnolabel = wx.StaticText(self, -1, self.t("animalchipnolabel") + ":")
		chipnolabel.SetFont(font)
		sizer.Add(chipnolabel, 0, wx.EXPAND)
		
		chipnoentry = wx.TextCtrl(self, -1, animaldata.chipno)
		chipnoentry.Bind(wx.EVT_CHAR, self.EnableSave)
		sizer.Add(chipnoentry, 0, wx.EXPAND)
		
		doblabel = wx.StaticText(self, -1, self.t("animaldoblabel") + ":")
		doblabel.SetFont(font)
		sizer.Add(doblabel, 0, wx.EXPAND)
		
		dobsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		dobentry = wx.TextCtrl(self, -1, animaldata.dob)
		dobentry.Bind(wx.EVT_CHAR, self.EnableSave)
		dobentry.Bind(wx.EVT_TEXT, self.UpdateAge)
		dobsizer.Add(dobentry, 1, wx.EXPAND)
		
		sizer.Add(dobsizer, 0, wx.EXPAND)
		
		commentslabel = wx.StaticText(self, -1, self.t("animalcommentslabel") + ":")
		commentslabel.SetFont(font)
		sizer.Add(commentslabel, 0, wx.EXPAND)
		
		commentsentry = wx.TextCtrl(self, -1, animaldata.comments, style=wx.TE_MULTILINE)
		commentsentry.Bind(wx.EVT_CHAR, self.EnableSave)
		sizer.Add(commentsentry, 1, wx.EXPAND)
		
		deceasedtickbox = wx.CheckBox(self, -1, self.t("deceasedlabel"))
		deceasedtickbox.SetFont(font)
		deceasedtickbox.Bind(wx.EVT_CHECKBOX, self.DeathTickBox)
		sizer.Add(deceasedtickbox, 0, wx.ALIGN_LEFT)
		
		deathpanel = wx.Panel(self, style=wx.SIMPLE_BORDER)
		
		deathbordersizer = wx.BoxSizer(wx.HORIZONTAL)
		
		deathbordersizer.Add(wx.StaticText(deathpanel, -1, "", size=(5,5)), 0, wx.EXPAND)
		
		deathsizer = wx.BoxSizer(wx.VERTICAL)
		
		deathsizer.Add(wx.StaticText(deathpanel, -1, "", size=(5,5)), 0, wx.EXPAND)
		
		deceaseddatelabel = wx.StaticText(deathpanel, -1, self.t("datelabel") + ": ")
		deceaseddatelabel.SetFont(font)
		deathsizer.Add(deceaseddatelabel, 0, wx.ALIGN_LEFT)
		
		deceaseddatectrl = customwidgets.DateCtrl(deathpanel, self.animaldata.localsettings)
		deceaseddatectrl.Bind(wx.EVT_CHAR, self.EnableSave)
		deathsizer.Add(deceaseddatectrl, 0, wx.EXPAND)
		
		deathreasonlabel = wx.StaticText(deathpanel, -1, self.t("causeofdeathlabel"))
		deathreasonlabel.SetFont(font)
		deathsizer.Add(deathreasonlabel, 0, wx.ALIGN_LEFT)
		
		deathreasonentry = wx.TextCtrl(deathpanel, -1, "", style=wx.TE_MULTILINE, size=(-1,30))
		deathreasonentry.Bind(wx.EVT_CHAR, self.EnableSave)
		deathsizer.Add(deathreasonentry, 0, wx.EXPAND)
		
		deathsizer.Add(wx.StaticText(deathpanel, -1, "", size=(5,5)), 0, wx.EXPAND)
		
		deathbordersizer.Add(deathsizer, 1, wx.EXPAND)
		
		deathbordersizer.Add(wx.StaticText(deathpanel, -1, "", size=(5,5)), 0, wx.EXPAND)
		
		deathpanel.SetSizer(deathbordersizer)
		
		if self.animaldata.deceased == 1:
			
			deceasedtickbox.SetValue(True)
			
			deceaseddate = self.animaldata.deceaseddate
			
			if str(deceaseddate) != "0000-00-00":
				
				deceaseddate = miscmethods.GetWXDateFromSQLDate(deceaseddate)
				
				deceaseddatectrl.SetValue(deceaseddate)
				
			else:
				
				deceaseddatectrl.Clear()
			
			deathreasonentry.SetValue(self.animaldata.causeofdeath)
			
		else:
			deceaseddatectrl.Clear()
			deathpanel.Hide()
		
		sizer.Add(deathpanel, 0, wx.EXPAND)
		
		animaldetailssizer = wx.BoxSizer(wx.VERTICAL)
		
		animaldetailssizer.Add(sizer, 1, wx.EXPAND)
		
		mainsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		mainsizer.Add(animaldetailssizer, 1, wx.EXPAND)
		
		mainsizer.Add(wx.StaticText(self, -1, "", size=(20,-1)), 0, wx.EXPAND)
		
		animalnotebook = wx.Notebook(self)
		
		########Appointment Browser###############
		
		animaldetailspanel = AnimalAppointmentBrowser(animalnotebook, self.animaldata)
		
		animalnotebook.AddPage(animaldetailspanel, self.t("animalappointmentslabel"), select=True)
		
		#Vaccinations sizer
		
		vaccinationlistpanel = wx.Panel(animalnotebook)
		
		vaccinationssizer = wx.BoxSizer(wx.VERTICAL)
		
		vaccinationlistpanel.vaccinationslistbox = customwidgets.VaccinationSummaryListbox(vaccinationlistpanel, self.animaldata)
		#vaccinationlistpanel.vaccinationslistbox.Bind(wx.EVT_LISTBOX, self.VaccinationSelected)
		vaccinationlistpanel.vaccinationslistbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EditVaccination)
		vaccinationlistpanel.vaccinationslistbox.Bind(wx.EVT_RIGHT_DOWN, self.VaccinationPopup)
		vaccinationssizer.Add(vaccinationlistpanel.vaccinationslistbox, 1, wx.EXPAND)
		
		if self.animaldata.localsettings.editmedication == 0:
			
			vaccinationpanel.Disable()
		
		vaccinationlistpanel.SetSizer(vaccinationssizer)
		
		animalnotebook.AddPage(vaccinationlistpanel, self.t("animalvaccinationslabel"), select=False)
		
		weightpanel = WeightPanel(animalnotebook, animaldata)
		
		animalnotebook.AddPage(weightpanel, self.t("weightpanelpagetitle"), select=False)
		
		mediapanel = attachedfilemethods.AttachedFilesPanel(animalnotebook, self.animaldata.localsettings, 1, self.animaldata.ID)
		
		animalnotebook.AddPage(mediapanel, self.t("attachedfileslabel"), select=False)
		
		mainsizer.Add(animalnotebook, 2, wx.EXPAND)
		
		#RefreshVaccinations(self)
		
		#mainsizer.Add(vaccinationssizer, 2, wx.EXPAND)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		closebuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		savebuttonbitmap = wx.Bitmap("icons/save.png")
		
		savebutton = wx.BitmapButton(self, -1, savebuttonbitmap)
		savebutton.SetToolTipString(self.t("animalsavebuttontooltip"))
		savebutton.Bind(wx.EVT_BUTTON, self.Save)
		savebutton.Disable()
		closebuttonsizer.Add(savebutton, 0, wx.ALIGN_RIGHT)
		
		bookbitmap = wx.Bitmap("icons/diary.png")
		creatediarynotebutton = wx.BitmapButton(self, -1, bookbitmap)
		creatediarynotebutton.SetToolTipString(self.t("createassociateddiarynotetooltip"))
		creatediarynotebutton.Bind(wx.EVT_BUTTON, self.CreateDiaryNote)
		
		if self.animaldata.ID == False or self.animaldata.localsettings.addtodiary == 0:
			
			creatediarynotebutton.Disable()
			animalnotebook.Disable()
		
		closebuttonsizer.Add(creatediarynotebutton, 0, wx.EXPAND)
		
		
		printbuttonbitmap = wx.Bitmap("icons/printer.png")
		printbutton = wx.BitmapButton(self, -1, printbuttonbitmap)
		printbutton.Bind(wx.EVT_BUTTON, self.PrintAllAppointmentDetails)
		printbutton.SetToolTipString(self.t("animalprintentirerecordtooltip"))
		closebuttonsizer.Add(printbutton, 0, wx.EXPAND)
		
		formbitmap = wx.Bitmap("icons/form.png")
		formbutton = wx.BitmapButton(self, -1, formbitmap)
		formbutton.SetToolTipString(self.t("animalgenerateformtooltip"))
		formbutton.Bind(wx.EVT_BUTTON, self.GenerateForm)
		closebuttonsizer.Add(formbutton, 0, wx.EXPAND)
		
		#changeownerbitmap = wx.Bitmap("icons/reset.png")
		#changeownerbutton = wx.BitmapButton(self, -1, changeownerbitmap)
		#changeownerbutton.SetToolTipString(self.t("changeownershiptooltip"))
		#changeownerbutton.Bind(wx.EVT_BUTTON, TransferOwnerShip)
		#closebuttonsizer.Add(changeownerbutton, 0, wx.EXPAND)
		
		lostandfoundbitmap = wx.Bitmap("icons/lostandfound.png")
		lostandfoundbutton = wx.BitmapButton(self, -1, lostandfoundbitmap)
		lostandfoundbutton.SetToolTipString(self.t("lostandfoundmenu"))
		lostandfoundbutton.Bind(wx.EVT_BUTTON, self.AddToLostAndFound)
		closebuttonsizer.Add(lostandfoundbutton, 0, wx.EXPAND)
		
		if self.animaldata.asmref != "":
			
			if self.animaldata.localsettings.asmsync == 1:
				
				asmbutton = wx.BitmapButton(self, -1, wx.Bitmap("icons/asm.png"))
				asmbutton.Bind(wx.EVT_BUTTON, self.ASMSync)
				asmbutton.SetToolTipString(self.t("asmsynctooltip"))
				closebuttonsizer.Add(asmbutton, 0, wx.EXPAND)
				self.asmbutton = asmbutton
				
				if self.animaldata.ID == False:
					
					asmbutton.Disable()
			
			asmreflabel = wx.StaticText(self, -1, miscmethods.NoWrap(" " + self.t("asmreflabel") + ": " + self.animaldata.asmref))
			asmreflabel.SetForegroundColour("red")
			closebuttonsizer.Add(asmreflabel, 0, wx.ALIGN_CENTER)
		
		if self.animaldata.ID == False:
			
			printbutton.Disable()
			formbutton.Disable()
			lostandfoundbutton.Disable()
		
		closebuttonsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		closebuttonsizer.Add(lostandfound, 0, wx.ALIGN_CENTER)
		
		topsizer.Add(closebuttonsizer, 0, wx.EXPAND)
		
		topsizer.Add(wx.StaticText(self, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		topsizer.Add(mainsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.notebook = notebook
		
		
		self.localsettings = self.animaldata.localsettings
		
		
		if self.animaldata.ID == False:
			
			animalnotebook.Disable()
		
		self.sizer = sizer
		self.animalnotebook = animalnotebook
		#self.editanimalappointmentbutton = editanimalappointmentbutton
		#self.deleteanimalappointmentbutton = deleteanimalappointmentbutton
		#self.printanimalappointmentbutton = printanimalappointmentbutton
		#self.formmenu = formmenu
		#self.formlist = formlist
		self.vaccinationlistpanel = vaccinationlistpanel
		self.attachedfilespanel = mediapanel
		#self.vetformbutton = vetformbutton
		#self.makeappointmentbutton = makeappointmentbutton
		self.creatediarynotebutton = creatediarynotebutton
		self.printbutton = printbutton
		self.formbutton = formbutton
		#self.changeownerbutton = changeownerbutton
		self.lostandfoundbutton = lostandfoundbutton
		
		self.savebutton = savebutton
		
		self.deathpanel = deathpanel
		self.deceasedtickbox = deceasedtickbox
		self.deceaseddatectrl = deceaseddatectrl
		self.deathreasonentry = deathreasonentry
		
		#self.editvaccinationbutton = editvaccinationbutton
		#self.deletevaccinationbutton = deletevaccinationbutton
		
		self.nameentry = nameentry
		self.speciesentry = speciesentry
		self.sexentry = sexentry
		self.breedentry = breedentry
		self.colourentry = colourentry
		self.chipnoentry = chipnoentry
		self.dobentry = dobentry
		self.commentsentry = commentsentry
		
		self.ownernamelabel = ownernamelabel
		
		vaccinationlistpanel.vaccinationslistbox.RefreshList()
		
		if self.animaldata.ID != False:
			self.RefreshAppointments()
			self.UpdateAge()
		
		del busy
	
	def AnimalAppointmentPopup(self, ID):
		
		popupmenu = wx.Menu()
		popupmenu.animalpanel = self
		
		if self.animaldata.localsettings.editappointments == 1:
			
			addappointment = wx.MenuItem(popupmenu, ADD_APPOINTMENT, self.t("addlabel"))
			addappointment.SetBitmap(wx.Bitmap("icons/new.png"))
			popupmenu.AppendItem(addappointment)
			wx.EVT_MENU(popupmenu, ADD_APPOINTMENT, self.CreateAppointment)
		
		if self.animalappointmentslistbox.listctrl.GetSelectedItemCount() > 0:
			
			if self.animaldata.localsettings.editappointments == 1:
				
				editappointment = wx.MenuItem(popupmenu, EDIT_APPOINTMENT, self.t("editlabel"))
				editappointment.SetBitmap(wx.Bitmap("icons/edit.png"))
				popupmenu.AppendItem(editappointment)
				wx.EVT_MENU(popupmenu, EDIT_APPOINTMENT, self.Edit)
			
			if self.animaldata.localsettings.deleteappointments == 1:
				
				deleteappointment = wx.MenuItem(popupmenu, DELETE_APPOINTMENT, self.t("deletelabel"))
				deleteappointment.SetBitmap(wx.Bitmap("icons/delete.png"))
				popupmenu.AppendItem(deleteappointment)
				wx.EVT_MENU(popupmenu, DELETE_APPOINTMENT, self.Delete)
			
			viewappointment = wx.MenuItem(popupmenu, VIEW_APPOINTMENT, self.t("viewvetnoteslabel"))
			viewappointment.SetBitmap(wx.Bitmap("icons/form.png"))
			popupmenu.AppendItem(viewappointment)
			wx.EVT_MENU(popupmenu, VIEW_APPOINTMENT, self.ViewAppointment)
			
			printappointment = wx.MenuItem(popupmenu, PRINT_APPOINTMENT, self.t("printtooltip"))
			printappointment.SetBitmap(wx.Bitmap("icons/printer.png"))
			popupmenu.AppendItem(printappointment)
			wx.EVT_MENU(popupmenu, PRINT_APPOINTMENT, self.PrintAppointmentDetails)
			
			if self.animaldata.localsettings.vetform == 1:
				
				popupmenu.AppendSeparator()
				
				vetform = wx.MenuItem(popupmenu, VET_FORM, self.t("vetformpagetitle"))
				vetform.SetBitmap(wx.Bitmap("icons/vetform.png"))
				popupmenu.AppendItem(vetform)
				wx.EVT_MENU(popupmenu, VET_FORM, self.VetForm)
			
			if self.animaldata.localsettings.changelog == 1:
				
				popupmenu.AppendSeparator()
				
				changelog = wx.MenuItem(popupmenu, APPOINTMENT_CHANGELOG, self.t("viewchangeloglabel"))
				changelog.SetBitmap(wx.Bitmap("icons/log.png"))
				popupmenu.AppendItem(changelog)
				wx.EVT_MENU(popupmenu, APPOINTMENT_CHANGELOG, self.AppointmentChangeLog)
		
		refresh = wx.MenuItem(popupmenu, REFRESH_APPOINTMENTS, self.t("refreshlabel"))
		refresh.SetBitmap(wx.Bitmap("icons/refresh.png"))
		popupmenu.AppendItem(refresh)
		wx.EVT_MENU(popupmenu, REFRESH_APPOINTMENTS, self.RefreshAppointments)
		
		self.PopupMenu(popupmenu)
	
	def OwnerPopup(self, ID):
		
		popupmenu = wx.Menu()
		popupmenu.animalpanel = self
		
		editowner = wx.MenuItem(popupmenu, EDIT_OWNER, self.t("appointmenteditownerbutton")[0])
		editowner.SetBitmap(wx.Bitmap("icons/edit.png"))
		popupmenu.AppendItem(editowner)
		wx.EVT_MENU(popupmenu, EDIT_OWNER, self.OpenClientRecord)
		
		changeowner = wx.MenuItem(popupmenu, CHANGE_OWNER, self.t("changeownershiptooltip"))
		changeowner.SetBitmap(wx.Bitmap("icons/reset.png"))
		popupmenu.AppendItem(changeowner)
		wx.EVT_MENU(popupmenu, CHANGE_OWNER, TransferOwnerShip)
		
		self.PopupMenu(popupmenu)
	
	def VaccinationPopup(self, ID):
		
		listbox = ID.GetEventObject()
		
		popupmenu = wx.Menu()
		popupmenu.animalpanel = self
		
		addvaccination = wx.MenuItem(popupmenu, ADD_VACCINATION, self.t("addlabel"))
		addvaccination.SetBitmap(wx.Bitmap("icons/new.png"))
		popupmenu.AppendItem(addvaccination)
		wx.EVT_MENU(popupmenu, ADD_VACCINATION, self.AddVaccination)
		
		if listbox.GetSelection() > -1:
			
			editvaccination = wx.MenuItem(popupmenu, EDIT_VACCINATION, self.t("editlabel"))
			editvaccination.SetBitmap(wx.Bitmap("icons/edit.png"))
			popupmenu.AppendItem(editvaccination)
			wx.EVT_MENU(popupmenu, EDIT_VACCINATION, self.EditVaccination)
			
			deletevaccination = wx.MenuItem(popupmenu, DELETE_VACCINATION, self.t("deletelabel"))
			deletevaccination.SetBitmap(wx.Bitmap("icons/delete.png"))
			popupmenu.AppendItem(deletevaccination)
			wx.EVT_MENU(popupmenu, DELETE_VACCINATION, self.DeleteVaccination)
		
		popupmenu.AppendSeparator()
		
		refreshvaccinations = wx.MenuItem(popupmenu, REFRESH_VACCINATIONS, self.t("refreshlabel"))
		refreshvaccinations.SetBitmap(wx.Bitmap("icons/refresh.png"))
		popupmenu.AppendItem(refreshvaccinations)
		wx.EVT_MENU(popupmenu, REFRESH_VACCINATIONS, self.vaccinationlistpanel.vaccinationslistbox.RefreshList)
		
		self.PopupMenu(popupmenu)
	
	def EnableSave(self, ID):
		
		self.savebutton.Enable()
		
		ID.Skip()
	
	def LostAndFoundPopup(self, ID):
		
		label = ID.GetEventObject()
		
		popupmenu = wx.Menu()
		
		lostandfound = wx.MenuItem(popupmenu, EDIT_LOST_AND_FOUND, self.t("editlabel"))
		lostandfound.SetBitmap(wx.Bitmap("icons/edit.png"))
		popupmenu.AppendItem(lostandfound)
		wx.EVT_MENU(popupmenu, EDIT_LOST_AND_FOUND, self.EditLostAndFoundRecord)
		
		popupmenu.lostandfoundid = label.ID
		
		self.PopupMenu(popupmenu)
	
	def EditLostAndFoundRecord(self, ID):
		
		menu = ID.GetEventObject()
		
		lostandfoundid = menu.lostandfoundid
		
		lostandfounddata = lostandfound.LostAndFoundSettings(self.animaldata.localsettings, lostandfoundid)
		
		lostandfoundpanel = lostandfound.EditLostAndFoundPanel(self.notebook, lostandfounddata)
		
		self.notebook.AddPage(lostandfoundpanel)
	
	def AddToLostAndFound(self, ID):
		
		if self.animallostorfound == False:
			
			popupmenu = wx.Menu()
			
			#popupmenu.parent = ID.GetEventObject()
			
			lost = wx.MenuItem(popupmenu, ADD_LOST, self.t("lostlabel"))
			lost.SetBitmap(wx.Bitmap("icons/lostandfound.png"))
			popupmenu.AppendItem(lost)
			wx.EVT_MENU(popupmenu, ADD_LOST, self.AddLost)
			
			found = wx.MenuItem(popupmenu, ADD_FOUND, self.t("foundlabel"))
			found.SetBitmap(wx.Bitmap("icons/lostandfound.png"))
			popupmenu.AppendItem(found)
			wx.EVT_MENU(popupmenu, ADD_FOUND, self.AddFound)
			
			self.PopupMenu(popupmenu)
			
		else:
			
			miscmethods.ShowMessage(self.t("alreadyonlostandfoundmessage"), self)
	
	def AddLost(self, ID):
		
		lostandfounddata = lostandfound.LostAndFoundSettings(self.animaldata.localsettings, False)
		lostandfounddata.lostorfound = 0
		
		self.EditLostAndFound(lostandfounddata)
	
	def AddFound(self, ID):
		
		lostandfounddata = lostandfound.LostAndFoundSettings(self.animaldata.localsettings, False)
		lostandfounddata.lostorfound = 1
		
		self.EditLostAndFound(lostandfounddata)
	
	def EditLostAndFound(self, lostandfounddata):
		
		lostandfounddata.animalid = self.animaldata.ID
		lostandfounddata.contactid = self.animaldata.ownerid
		
		panel = lostandfound.EditLostAndFoundPanel(self.notebook, lostandfounddata)
		panel.UpdateContactInfo(lostandfounddata.contactid)
		
		panel.speciesentry.SetValue(self.animaldata.species)
		
		panel.sexentry.SetSelection(self.animaldata.sex)
		
		if int(self.animaldata.neutered) == 1:
			
			panel.neuteredentry.SetSelection(1)
		
		if self.animaldata.chipno != "":
			
			panel.chippedentry.SetSelection(1)
		
		self.notebook.AddPage(panel)
	
	def UpdateAge(self, ID=False):
		
		dob = self.dobentry.GetValue()
		
		age = miscmethods.GetAgeFromDOB(dob, self.animaldata.localsettings)
		
		self.dobentry.SetToolTipString(age)
	
	def UpdateOwnerLabel(self):
		
		self.ownernamelabel.SetLabel(self.clientdata.title + " " + self.clientdata.surname)
	
	def VaccinationSelected(self, ID):
		
		self.editvaccinationbutton.Enable()
		self.deletevaccinationbutton.Enable()
	
	def AddVaccination(self, ID):
		
		self.EditVaccinationDialog()
	
	def EditVaccination(self, ID):
		
		listboxid = self.vaccinationlistpanel.vaccinationslistbox.GetSelection()
		
		#print "listboxid = " + str(listboxid)
		
		if listboxid > -1:##editing an existing vaccination
			
			medicationoutid = self.vaccinationlistpanel.vaccinationslistbox.htmllist[listboxid][1]
			medicationid = self.vaccinationlistpanel.vaccinationslistbox.htmllist[listboxid][5]
			
			#print "outid = " + str(medicationoutid)
			#print "id = " + str(medicationid)
		
		self.EditVaccinationDialog(medicationid, medicationoutid)
	
	def EditVaccinationDialog(self, medicationid=False, medicationoutid=False):
		
		if medicationid !=  False:
			
			listboxid = self.vaccinationlistpanel.vaccinationslistbox.GetSelection()
			
			name = self.vaccinationlistpanel.vaccinationslistbox.htmllist[listboxid][2]
			given = self.vaccinationlistpanel.vaccinationslistbox.htmllist[listboxid][0]
			given = miscmethods.GetWXDateFromDate(given)
			next = self.vaccinationlistpanel.vaccinationslistbox.htmllist[listboxid][4]
			if str(next) != "None":
				next = miscmethods.GetWXDateFromDate(next)
			batch = self.vaccinationlistpanel.vaccinationslistbox.htmllist[listboxid][3]
			
		elif medicationoutid != False:
			
			listboxid = self.vaccinationlistpanel.vaccinationslistbox.GetSelection()
			
			name = self.vaccinationlistpanel.vaccinationslistbox.htmllist[listboxid][2]
			given = self.vaccinationlistpanel.vaccinationslistbox.htmllist[listboxid][0]
			given = miscmethods.GetWXDateFromDate(given)
			next = self.vaccinationlistpanel.vaccinationslistbox.htmllist[listboxid][4]
			if str(next) != "None":
				next = miscmethods.GetWXDateFromDate(next)
			batch = self.vaccinationlistpanel.vaccinationslistbox.htmllist[listboxid][3]
			
		else:
			
			name = ""
			given = ""
			next = ""
			batch = ""
		
		dialog = wx.Dialog(self, -1, self.t("vaccinationsvaccinelabel"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		topsizer.Add(wx.StaticText(self, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		namelabel = wx.StaticText(panel, -1, self.t("animalvaccinelabel"))
		font = namelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		namelabel.SetFont(font)
		topsizer.Add(namelabel, 0, wx.ALIGN_LEFT)
		
		action = "SELECT Name FROM medication WHERE Type = 1"
		results = db.SendSQL(action, self.animaldata.localsettings.dbconnection)
		
		vaccinelist = []
		
		for a in results:
			
			vaccinelist.append(a[0])
		
		namechoice = wx.ComboBox(panel, -1, name, choices=vaccinelist)
		topsizer.Add(namechoice, 0, wx.EXPAND)
		
		batchlabel = wx.StaticText(panel, -1, self.t("animalvaccinationbatchlabel"))
		batchlabel.SetFont(font)
		topsizer.Add(batchlabel, 0, wx.ALIGN_LEFT)
		
		batchentry = wx.TextCtrl(panel, -1, batch, size=(100,-1))
		topsizer.Add(batchentry, 0, wx.EXPAND)
		
		topsizer.Add(wx.StaticText(self, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		givenlabel = wx.StaticText(panel, -1, self.t("animalgivenlabel"))
		givenlabel.SetFont(font)
		topsizer.Add(givenlabel, 0, wx.ALIGN_LEFT)
		
		givenentry = customwidgets.DateCtrl(panel, self.animaldata.localsettings)
		
		if str(given) != "":
			givenentry.SetValue(given)
		
		topsizer.Add(givenentry, 0, wx.EXPAND)
		
		nextlabel = wx.StaticText(panel, -1, self.t("animalnextlabel"))
		nextlabel.SetFont(font)
		topsizer.Add(nextlabel, 0, wx.ALIGN_LEFT)
		
		nextentry = customwidgets.DateCtrl(panel, self.animaldata.localsettings)
		
		if str(next) != "":
			nextentry.SetValue(next)
		
		topsizer.Add(nextentry, 0, wx.EXPAND)
		
		topsizer.Add(wx.StaticText(self, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		submitbutton = wx.Button(panel, -1, self.t("submitlabel"))
		submitbutton.SetBackgroundColour("green")
		submitbutton.Bind(wx.EVT_BUTTON, self.SubmitVaccination)
		submitbutton.SetToolTipString(self.t("animalsubmitvaccinationtooltip"))
		
		topsizer.Add(submitbutton, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		panel.SetSizer(topsizer)
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		panel.namechoice = namechoice
		panel.givenentry = givenentry
		panel.nextentry = nextentry
		panel.batchentry = batchentry
		panel.medicationid = medicationid
		panel.medicationoutid = medicationoutid
		
		dialog.SetSizer(dialogsizer)
		
		dialog.Fit()
		
		dialog.ShowModal()
	
	def SubmitVaccination(self, ID):
		
		parent = ID.GetEventObject().GetParent()
		
		name = parent.namechoice.GetValue()
		given = parent.givenentry.GetValue()
		given = miscmethods.GetSQLDateFromWXDate(given)
		
		next = parent.nextentry.GetValue()
		
		if str(next) == "None" or str(next) == "":
			
			next = "0000-00-00"
			
		else:
			
			next = miscmethods.GetSQLDateFromWXDate(next)
		
		batch = parent.batchentry.GetValue()
		
		medicationoutid = parent.medicationoutid
		medicationid = parent.medicationid
		
		if medicationid != False:
			
			print str(medicationoutid) + ", " + str(medicationid)
			
			medicationoutdata = medicationmethods.MedicationOutData(medicationid, medicationoutid)
			medicationoutdata.GetSettings(self.animaldata.localsettings)
			
			print "medicationoutdata.appointmentid = " + str(medicationoutdata.appointmentid)
			
			medicationoutdata.date = given
			medicationoutdata.batchno = batch
			medicationoutdata.nextdue = next
			
			dbmethods.WriteToMedicationOutTable(self.animaldata.localsettings.dbconnection, medicationoutdata)
			
		else:
			
			animalid = self.animaldata.ID
			dbmethods.WriteToManualVaccinationTable(self.animaldata.localsettings.dbconnection, medicationoutid, animalid, given, name, batch, next)
		
		self.vaccinationlistpanel.vaccinationslistbox.RefreshList()
		
		parent.GetParent().Close()
	
	def DeleteVaccination(self, ID):
		
		listboxid = self.vaccinationlistpanel.vaccinationslistbox.GetSelection()
		
		ID = self.vaccinationlistpanel.vaccinationslistbox.htmllist[listboxid][1]
		vaccinationid = self.vaccinationlistpanel.vaccinationslistbox.htmllist[listboxid][5]
		
		if miscmethods.ConfirmMessage(self.t("animalconfirmdeletevaccinationmessage")):
			
			if vaccinationid == 0:
				
				action = "DELETE FROM manualvaccination WHERE ID = " + str(ID)
				
			else:
				
				action = "DELETE FROM medicationout WHERE ID = " + str(ID)
			
			db.SendSQL(action, self.localsettings.dbconnection)
			
			self.vaccinationlistpanel.vaccinationslistbox.RefreshList()
	
	def CreateDiaryNote(self, ID=False):
		
		title = self.animaldata.name + " (" + self.animaldata.species + ")"
		diarynotepanel = diarymethods.DiaryNotePanel(self.notebook, self.animaldata.localsettings, 2, self.animaldata.ID, title)
		self.notebook.AddPage(diarynotepanel)
	
	def DeathTickBox(self, ID=False):
		
		self.savebutton.Enable()
		
		if self.deceasedtickbox.GetValue() == True:
			
			self.deathpanel.Show()
			
		else:
			self.deceaseddatectrl.Clear()
			self.deathreasonentry.Clear()
			self.deathpanel.Hide()
		
		self.sizer.Layout()
	
	def VetForm(self, ID):
		
		listboxid = self.animalappointmentslistbox.GetFocusedItem()
		appointmentid = self.animalappointmentslistbox.GetItemData(listboxid)
		appointmentdata = appointmentmethods.AppointmentSettings(self.animaldata.localsettings, self.animaldata.ID, appointmentid)
		
		vetform = vetmethods.VetForm(self.notebook, appointmentdata, self.localsettings, self)
		
		self.notebook.AddPage(vetform)
		
	
	def AppointmentChangeLog(self, ID):
		
		listboxid = self.animalappointmentslistbox.GetFocusedItem()
		appointmentid = self.animalappointmentslistbox.GetItemData(listboxid)
		appointmentdata = appointmentmethods.AppointmentSettings(self.animaldata.localsettings, self.animaldata.ID, appointmentid)
		
		miscmethods.ShowChangeLog(miscmethods.FormatSQLDate(appointmentdata.date, self.animaldata.localsettings) + " " + appointmentdata.reason, appointmentdata.changelog, self.animaldata.localsettings.dbconnection)
	
	def GenerateForm(self, ID):
		
		ChooseAnimalForm(self)
		
		#choicesid = self.formmenu.GetSelection()
		
		#formname = self.formlist[choicesid]
		
		#formmethods.GenerateAnimalForm(formname, self.clientdata, self.animaldata)
	
	def OpenClientRecord(self, ID):
		
		clientpanel = clientmethods.ClientPanel(self.notebook, self.clientdata)
		self.notebook.AddPage(clientpanel)
	
	def ViewAppointment(self, ID):
		
		listboxid = self.animalappointmentslistbox.GetFocusedItem()
		appointmentid = self.animalappointmentslistbox.GetItemData(listboxid)
		
		output = miscmethods.GetAppointmentDetailsHtml(self.localsettings, appointmentid, False)
		
		#dialog = wx.Dialog(self, -1, self.t("viewvetnoteslabel"))
		
		#dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		#panel = wx.Panel(dialog)
		
		#topsizer = wx.BoxSizer(wx.VERTICAL)
		
		#htmlwindow = wx.
		
		#panel.SetSizer(topsizer)
		
		#dialogsizer.Add(panel, 1, wx.EXPAND)
		
		#dialog.SetSizer(dialogsizer)
		
		#dialog.ShowModal()
		
		
		#self.appointmentdetailswindow.SetPage(output)
		
		dialog = wx.Dialog(self, -1, self.t("viewvetnoteslabel"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		summarywindow = wx.html.HtmlWindow(panel)
		topsizer.Add(summarywindow, 1, wx.EXPAND)
		
		summarywindow.SetPage(output)
		
		panel.SetSizer(topsizer)
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		dialog.SetSize((400,400))
		
		dialog.ShowModal()
	
	def PrintAppointmentDetails(self, ID):
		
		listboxid = self.animalappointmentslistbox.GetFocusedItem()
		appointmentid = self.animalappointmentslistbox.GetItemData(listboxid)
		
		output = miscmethods.GetAnimalDetailsHTML(self.animaldata) + miscmethods.GetAppointmentDetailsHtml(self.localsettings, appointmentid)
		formmethods.BuildForm(self.localsettings, output)
	
	def PrintAllAppointmentDetails(self, ID):
		
		output = miscmethods.GetAnimalDetailsHTML(self.animaldata) + "<hr>"
		
		for a in self.animalappointmentslistbox.htmllist:
			
			output = output + miscmethods.GetAppointmentDetailsHtml(self.localsettings, a[0]) + "<hr>"
		
		formmethods.BuildForm(self.localsettings, output)
	
	def GetLookupsList(self, table):
		
		columnname = table[0].upper() + table[1:] + "Name"
		
		action = "SELECT " + columnname + " FROM " + table + " ORDER BY " + columnname
		results = db.SendSQL(action, self.animaldata.localsettings.dbconnection)
		
		lookups = []
		
		for a in range(0, len(results)):
			
			lookups.append(results[a][0])
		
		return lookups
	
	def ClosePage(self, ID=False):
		
		if self.savebutton.IsEnabled() == True:
			
			return miscmethods.ConfirmMessage(self.t("animalunsavedchangesmessage"))
			
		else:
			
			return True
	
	def Save(self, ID):
		
		ownerid = self.animaldata.ownerid
		
		
		self.animaldata.name = self.nameentry.GetValue()
		self.animaldata.sex = self.sexentry.GetSelection()
		self.animaldata.species = self.speciesentry.GetValue()
		self.animaldata.breed = self.breedentry.GetValue()
		self.animaldata.colour = self.colourentry.GetValue()
		self.animaldata.dob = self.dobentry.GetValue()
		self.animaldata.chipno = self.chipnoentry.GetValue()
		self.animaldata.comments = self.commentsentry.GetValue()
		
		if self.neuteredcheckbox.GetValue() == True:
			
			self.animaldata.neutered = "1"
			
		else:
			
			self.animaldata.neutered = "0"
		
		self.animaldata.comments = self.animaldata.comments
		self.animaldata.chipno = self.animaldata.chipno.upper()
		
		if self.deceasedtickbox.GetValue() == True:
			
			self.animaldata.deceased = 1
			
			deceaseddate = self.deceaseddatectrl.GetValue()
			
			if str(deceaseddate) == "":
				deceaseddate = "0000-00-00"
			else:
				deceaseddate = miscmethods.GetSQLDateFromWXDate(deceaseddate)
			
			self.animaldata.deceaseddate = deceaseddate
			
			self.animaldata.causeofdeath = self.deathreasonentry.GetValue()
			
		else:
			
			self.animaldata.deceased = 0
			
			self.animaldata.deceaseddate = "0000-00-00"
			
			self.animaldata.causeofdeath = ""
		
		self.animaldata.Submit()
		
		if self.clientpanel != False:
			
			try:
				
				self.clientpanel.RefreshAnimals()
				
			except:
				
				pass
		
		
		self.printbutton.Enable()
		
		if self.localsettings.asmsync == 1 and self.animaldata.asmref != "":
			
			self.asmbutton.Enable()
		#self.changeownerbutton.Enable()
		
		self.lostandfoundbutton.Enable()
		
		self.savebutton.Disable()
		
		self.attachedfilespanel.listbox.linkid = self.animaldata.ID
		
		self.animalnotebook.Enable()
	
	def CreateAppointment(self, ID):
		
		appointmentsettings = appointmentmethods.AppointmentSettings(self.animaldata.localsettings, self.animaldata.ID, False)
		appointmentpanel = appointmentmethods.AppointmentPanel(self.notebook, appointmentsettings)
		appointmentpanel.parent = self
		self.notebook.AddPage(appointmentpanel)
	
	def RefreshAppointments(self, ID=False):
		
		self.animalappointmentslistbox.RefreshList()
	
	def Edit(self, ID=False):
		
		listboxid = self.animalappointmentslistbox.GetFocusedItem()
		appointmentid = self.animalappointmentslistbox.GetItemData(listboxid)
		appointmentdata = appointmentmethods.AppointmentSettings(self.animaldata.localsettings, self.animaldata.ID, appointmentid)
		appointmentpanel = appointmentmethods.AppointmentPanel(self.notebook, appointmentdata)
		appointmentpanel.parent = self
		self.notebook.AddPage(appointmentpanel)
	
	def Delete(self, ID=False):
		
		listboxid = self.animalappointmentslistbox.GetFocusedItem()
		appointmentid = self.animalappointmentslistbox.GetItemData(listboxid)
		if miscmethods.ConfirmMessage(self.t("animalconfirmdeleteappointmentmessage")):
			
			action = "DELETE FROM appointment WHERE ID = " + str(appointmentid)
			db.SendSQL(action, self.animaldata.localsettings.dbconnection)
			
			self.RefreshAppointments()
	
	def ASMSync(self, ID):
		
		dialog = wx.Dialog(self, -1, self.t("asmsynctooltip"), size=(600,400))
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		panel = wx.Panel(dialog)
		topsizer = wx.BoxSizer(wx.VERTICAL)
		panel.topsizer = topsizer
		
		gridsizer = wx.FlexGridSizer(cols=7)
		
		gridsizer.AddGrowableCol(2)
		gridsizer.AddGrowableCol(4)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.ALIGN_LEFT)
		gridsizer.Add(wx.StaticText(panel, -1, "", size=(20,-1)), 0, wx.EXPAND)
		gridsizer.Add(wx.StaticBitmap(panel, -1, wx.Bitmap("icons/evettelogo.png")), 0, wx.ALIGN_CENTER)
		gridsizer.Add(wx.StaticText(panel, -1, "", size=(20,-1)), 0, wx.EXPAND)
		gridsizer.Add(wx.StaticBitmap(panel, -1, wx.Bitmap("icons/asm.png")), 0, wx.ALIGN_CENTER)
		gridsizer.Add(wx.StaticText(panel, -1, "", size=(20,-1)), 0, wx.EXPAND)
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		########################################################################
		
		gridsizer.Add(wx.StaticText(panel, -1, self.t("appointmentsearchanimalnamelabel")), 0, wx.ALIGN_LEFT)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.evetteanimalnameentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY, size=(200,-1))
		gridsizer.Add(panel.evetteanimalnameentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.asmanimalnameentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY, size=(200,-1))
		gridsizer.Add(panel.asmanimalnameentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.animalnamesyncbutton = wx.BitmapButton(panel, -1, wx.Bitmap("icons/refresh.png"))
		panel.animalnamesyncbutton.Bind(wx.EVT_BUTTON, self.SyncAnimalName)
		panel.animalnamesyncbutton.SetToolTipString(self.t("asmsyncbuttontooltip"))
		gridsizer.Add(panel.animalnamesyncbutton, 0, wx.ALIGN_CENTER)
		
		########################################################################
		
		gridsizer.Add(wx.StaticText(panel, -1, self.t("animaldoblabel")), 0, wx.ALIGN_LEFT)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.evetteanimaldobentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.evetteanimaldobentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.asmanimaldobentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.asmanimaldobentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.animaldobsyncbutton = wx.BitmapButton(panel, -1, wx.Bitmap("icons/refresh.png"))
		panel.animaldobsyncbutton.Bind(wx.EVT_BUTTON, self.SyncAnimalDOB)
		panel.animaldobsyncbutton.SetToolTipString(self.t("asmsyncbuttontooltip"))
		gridsizer.Add(panel.animaldobsyncbutton, 0, wx.ALIGN_CENTER)
		
		########################################################################
		
		gridsizer.Add(wx.StaticText(panel, -1, self.t("deceasedlabel")), 0, wx.ALIGN_LEFT)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.evetteanimaldeceaseddateentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.evetteanimaldeceaseddateentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.asmanimaldeceaseddateentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.asmanimaldeceaseddateentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.animaldeceaseddatesyncbutton = wx.BitmapButton(panel, -1, wx.Bitmap("icons/refresh.png"))
		panel.animaldeceaseddatesyncbutton.Bind(wx.EVT_BUTTON, self.SyncAnimalDeceasedDate)
		panel.animaldeceaseddatesyncbutton.SetToolTipString(self.t("asmsyncbuttontooltip"))
		gridsizer.Add(panel.animaldeceaseddatesyncbutton, 0, wx.ALIGN_CENTER)
		
		########################################################################
		
		gridsizer.Add(wx.StaticText(panel, -1, self.t("animalchipnolabel")), 0, wx.ALIGN_LEFT)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.evetteanimalchipnoentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.evetteanimalchipnoentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.asmanimalchipnoentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.asmanimalchipnoentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.animalchipnosyncbutton = wx.BitmapButton(panel, -1, wx.Bitmap("icons/refresh.png"))
		panel.animalchipnosyncbutton.Bind(wx.EVT_BUTTON, self.SyncAnimalChipNo)
		panel.animalchipnosyncbutton.SetToolTipString(self.t("asmsyncbuttontooltip"))
		gridsizer.Add(panel.animalchipnosyncbutton, 0, wx.ALIGN_CENTER)
		
		########################################################################
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		########################################################################
		
		gridsizer.Add(wx.StaticText(panel, -1, self.t("animalownerlabel")), 0, wx.ALIGN_LEFT)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.evetteownernameentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.evetteownernameentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.asmownernameentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.asmownernameentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.ownersyncbutton = wx.BitmapButton(panel, -1, wx.Bitmap("icons/refresh.png"))
		panel.ownersyncbutton.Bind(wx.EVT_BUTTON, self.SyncOwner)
		panel.ownersyncbutton.SetToolTipString(self.t("asmsyncbuttontooltip"))
		gridsizer.Add(panel.ownersyncbutton, 0, wx.ALIGN_CENTER)
		
		
		########################################################################
		
		gridsizer.Add(wx.StaticText(panel, -1, self.t("clientsearchaddresslabel")), 0, wx.ALIGN_LEFT)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.evetteowneraddressentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY | wx.TE_MULTILINE)
		gridsizer.Add(panel.evetteowneraddressentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.asmowneraddressentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY | wx.TE_MULTILINE)
		gridsizer.Add(panel.asmowneraddressentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		#owneraddresssyncbutton = wx.BitmapButton(panel, -1, wx.Bitmap("icons/refresh.png"))
		#owneraddresssyncbutton.SetToolTipString(self.t("asmsyncbuttontooltip"))
		#gridsizer.Add(owneraddresssyncbutton, 0, wx.ALIGN_TOP)
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		########################################################################
		
		gridsizer.Add(wx.StaticText(panel, -1, self.t("clientsearchpostcodelabel")), 0, wx.ALIGN_LEFT)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.evetteownerpostcodeentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.evetteownerpostcodeentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.asmownerpostcodeentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.asmownerpostcodeentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		#ownerpostcodesyncbutton = wx.BitmapButton(panel, -1, wx.Bitmap("icons/refresh.png"))
		#ownerpostcodesyncbutton.SetToolTipString(self.t("asmsyncbuttontooltip"))
		#gridsizer.Add(ownerpostcodesyncbutton, 0, wx.ALIGN_CENTER)
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		########################################################################
		
		gridsizer.Add(wx.StaticText(panel, -1, self.t("clienthomephonelabel")), 0, wx.ALIGN_LEFT)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.evetteownerhometelephoneentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.evetteownerhometelephoneentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.asmownerhometelephoneentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.asmownerhometelephoneentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		#ownerhometelephonesyncbutton = wx.BitmapButton(panel, -1, wx.Bitmap("icons/refresh.png"))
		#ownerhometelephonesyncbutton.SetToolTipString(self.t("asmsyncbuttontooltip"))
		#gridsizer.Add(ownerhometelephonesyncbutton, 0, wx.ALIGN_CENTER)
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		########################################################################
		
		gridsizer.Add(wx.StaticText(panel, -1, self.t("clientmobilephonelabel")), 0, wx.ALIGN_LEFT)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.evetteownermobiletelephoneentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.evetteownermobiletelephoneentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.asmownermobiletelephoneentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.asmownermobiletelephoneentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		#ownermobiletelephonesyncbutton = wx.BitmapButton(panel, -1, wx.Bitmap("icons/refresh.png"))
		#ownermobiletelephonesyncbutton.SetToolTipString(self.t("asmsyncbuttontooltip"))
		#gridsizer.Add(ownermobiletelephonesyncbutton, 0, wx.ALIGN_CENTER)
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		########################################################################
		
		gridsizer.Add(wx.StaticText(panel, -1, self.t("clientworkphonelabel")), 0, wx.ALIGN_LEFT)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.evetteownerworktelephoneentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.evetteownerworktelephoneentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.asmownerworktelephoneentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.asmownerworktelephoneentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		#ownerworktelephonesyncbutton = wx.BitmapButton(panel, -1, wx.Bitmap("icons/refresh.png"))
		#ownerworktelephonesyncbutton.SetToolTipString(self.t("asmsyncbuttontooltip"))
		#gridsizer.Add(ownerworktelephonesyncbutton, 0, wx.ALIGN_CENTER)
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		########################################################################
		
		gridsizer.Add(wx.StaticText(panel, -1, self.t("clientemailaddresslabel")), 0, wx.ALIGN_LEFT)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.evetteowneremailaddressentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.evetteowneremailaddressentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		panel.asmowneremailaddressentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
		gridsizer.Add(panel.asmowneremailaddressentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		#owneremailaddresssyncbutton = wx.BitmapButton(panel, -1, wx.Bitmap("icons/refresh.png"))
		#owneremailaddresssyncbutton.SetToolTipString(self.t("asmsyncbuttontooltip"))
		#gridsizer.Add(owneremailaddresssyncbutton, 0, wx.ALIGN_CENTER)
		gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		########################################################################
		
		#gridsizer.Add(wx.StaticBitmap(panel, -1, wx.Bitmap("icons/refresh.png")), 0, wx.ALIGN_CENTER)
		
		self.UpdateEvetteInfo(panel)
		self.UpdateASMInfo(panel)
		self.MatchASMEvetteInfo(panel)
		
		topsizer.Add(gridsizer, 1, wx.EXPAND)
		
		panel.SetSizer(topsizer)
		panel.asmref = self.animaldata.asmref
		dialogsizer.Add(panel, 1, wx.EXPAND)
		dialog.SetSizer(dialogsizer)
		
		dialog.Fit()
		
		dialog.ShowModal()
	
	def UpdateEvetteInfo(self, panel):
		
		evetteid = self.animaldata.ID
		asmref = self.animaldata.asmref
		
		#print "Evette ID = " + str(evetteid)
		#print "ASM Ref = " + str(asmref)
		
		panel.evetteanimalnameentry.SetValue(self.animaldata.name)
		panel.evetteanimaldobentry.SetValue(self.animaldata.dob)
		
		if self.animaldata.deceaseddate != "0000-00-00":
			
			panel.evetteanimaldeceaseddateentry.SetValue(miscmethods.FormatSQLDate(self.animaldata.deceaseddate, self.localsettings))
			
		elif self.animaldata.deceased == 1:
			
			panel.evetteanimaldeceaseddateentry.SetValue(self.t("yeslabel"))
			
		else:
			
			panel.evetteanimaldeceaseddateentry.SetValue(self.t("nolabel"))
		
		
		panel.evetteanimalchipnoentry.SetValue(self.animaldata.chipno)
		
		action = "SELECT client.ClientTitle, client.ClientForenames, client.ClientSurname, client.ClientAddress, client.ClientPostcode, client.ClientHomeTelephone, client.ClientMobileTelephone, client.ClientWorkTelephone, client.ClientEmailAddress FROM animal INNER JOIN client ON animal.OwnerID = client.ID WHERE animal.ID = " + str(self.animaldata.ID)
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		evetteowner = ""
		
		if results[0][0] != "":
			
			evetteowner = evetteowner + results[0][0] + " "
		
		if results[0][1] != "":
			
			evetteowner = evetteowner + results[0][1] + " "
		
		if results[0][2] != "":
			
			evetteowner = evetteowner + results[0][2]
		
		panel.evetteownernameentry.SetValue(evetteowner)
		
		panel.evetteowneraddressentry.SetValue(results[0][3])
		panel.evetteownerpostcodeentry.SetValue(results[0][4])
		
		panel.evetteownerhometelephoneentry.SetValue(results[0][5])
		panel.evetteownermobiletelephoneentry.SetValue(results[0][6])
		panel.evetteownerworktelephoneentry.SetValue(results[0][7])
		panel.evetteowneremailaddressentry.SetValue(results[0][8])
	
	def UpdateASMInfo(self, panel):
		
		asmref = self.animaldata.asmref
		
		asmconnectionavailable = True
		
		try:
			
			asmconnection = db.GetASMConnection()
			
		except:
			
			miscmethods.ShowMessage(self.t("asmconnectionerrormessage"), panel)
			
			asmconnectionavailable = False
		
		asmref = self.animaldata.asmref
		
		if asmconnectionavailable == True:
			
			action = "SELECT animal.AnimalName, animal.DateOfBirth, animal.IdentichipNumber, owner.OwnerTitle, owner.OwnerForenames, owner.OwnerSurname, owner.OwnerAddress, owner.OwnerPostcode, owner.HomeTelephone, owner.MobileTelephone, owner.WorkTelephone, owner.EmailAddress, animal.DeceasedDate FROM animal INNER JOIN adoption ON adoption.ID = animal.ActiveMovementID AND adoption.MovementType != 2 INNER JOIN owner ON adoption.OwnerID = owner.ID WHERE animal.ShelterCode = \"" + str(asmref) + "\""
			results = db.SendSQL(action, asmconnection)
			
			if len(results) == 0:
				
				action = "SELECT animal.AnimalName, animal.DateOfBirth, animal.IdentichipNumber, animal.DeceasedDate FROM animal WHERE animal.ShelterCode = \"" + str(asmref) + "\""
				results = db.SendSQL(action, asmconnection)
				
				panel.asmanimalnameentry.SetValue(results[0][0])
				asmdob = results[0][1]
				panel.asmanimaldobentry.SetValue(miscmethods.FormatSQLDate(asmdob, self.localsettings))
				
				asmdeceaseddate = results[0][3]
				
				if asmdeceaseddate == None:
					
					asmdeceaseddate = self.t("nolabel")
					
				else:
					
					asmdeceaseddate = miscmethods.GetDateFromSQLDate(asmdeceaseddate)
					asmdeceaseddate = miscmethods.FormatDate(asmdeceaseddate, self.localsettings)
				
				panel.asmanimaldeceaseddateentry.SetValue(asmdeceaseddate)
				
				panel.asmanimalchipnoentry.SetValue(results[0][2])
				
				action = "SELECT ShelterID FROM settings"
				shelterid = db.SendSQL(action, self.localsettings.dbconnection)[0][0]
				
				action = "SELECT client.ClientTitle, client.ClientForenames, client.ClientSurname, client.ClientAddress, client.ClientPostcode, client.ClientHomeTelephone, client.ClientMobileTelephone, client.ClientWorkTelephone, client.ClientEmailAddress FROM client WHERE client.ID = " + str(shelterid)
				results = db.SendSQL(action, self.localsettings.dbconnection)
				
				evetteowner = ""
				
				if miscmethods.CorrectNullString(results[0][0]) != "":
					
					evetteowner = evetteowner + results[0][0] + " "
				
				if miscmethods.CorrectNullString(results[0][1]) != "":
					
					evetteowner = evetteowner + results[0][1] + " "
				
				if miscmethods.CorrectNullString(results[0][2]) != "":
					
					evetteowner = evetteowner + results[0][2]
				
				panel.asmownernameentry.SetValue(evetteowner)
				
				panel.asmowneraddressentry.SetValue(miscmethods.CorrectNullString(results[0][3]))
				panel.asmownerpostcodeentry.SetValue(miscmethods.CorrectNullString(results[0][4]))
				
				panel.asmownerhometelephoneentry.SetValue(miscmethods.CorrectNullString(results[0][5]))
				panel.asmownermobiletelephoneentry.SetValue(miscmethods.CorrectNullString(results[0][6]))
				panel.asmownerworktelephoneentry.SetValue(miscmethods.CorrectNullString(results[0][7]))
				panel.asmowneremailaddressentry.SetValue(miscmethods.CorrectNullString(results[0][8]))
				
				panel.asmonshelter = True
				
			else:
				
				panel.asmanimalnameentry.SetValue(results[0][0])
				asmdob = results[0][1]
				panel.asmanimaldobentry.SetValue(miscmethods.FormatSQLDate(asmdob, self.localsettings))
				
				asmdeceaseddate = results[0][12]
				
				if asmdeceaseddate == None:
					
					asmdeceaseddate = self.t("nolabel")
					
				else:
					
					asmdeceaseddate = miscmethods.GetDateFromSQLDate(asmdeceaseddate)
					asmdeceaseddate = miscmethods.FormatDate(asmdeceaseddate, self.localsettings)
				
				panel.asmanimaldeceaseddateentry.SetValue(asmdeceaseddate)
				
				panel.asmanimalchipnoentry.SetValue(results[0][2])
				
				asmowner = ""
				
				if miscmethods.CorrectNullString(results[0][3]) != "":
					
					asmowner = asmowner + results[0][3] + " "
				
				if miscmethods.CorrectNullString(results[0][4]) != "":
					
					asmowner = asmowner + results[0][4] + " "
				
				if miscmethods.CorrectNullString(results[0][5]) != "":
					
					asmowner = asmowner + results[0][5]
				
				panel.asmownernameentry.SetValue(asmowner)
				
				panel.asmowneraddressentry.SetValue(miscmethods.CorrectNullString(results[0][6]))
				panel.asmownerpostcodeentry.SetValue(miscmethods.CorrectNullString(results[0][7]))
				
				panel.asmownerhometelephoneentry.SetValue(miscmethods.CorrectNullString(results[0][8]))
				
				panel.asmownermobiletelephoneentry.SetValue(miscmethods.CorrectNullString(results[0][9]))
				panel.asmownerworktelephoneentry.SetValue(miscmethods.CorrectNullString(results[0][10]))
				panel.asmowneremailaddressentry.SetValue(miscmethods.CorrectNullString(results[0][11]))
				
				panel.asmonshelter = False
			
			asmconnection.close()
	
	def MatchASMEvetteInfo(self, panel):
		
		if panel.asmanimalnameentry.GetValue() == panel.evetteanimalnameentry.GetValue():
			
			panel.asmanimalnameentry.SetBackgroundColour("green")
			panel.evetteanimalnameentry.SetBackgroundColour("green")
			panel.animalnamesyncbutton.Disable()
			
		else:
			
			panel.asmanimalnameentry.SetBackgroundColour("red")
			panel.evetteanimalnameentry.SetBackgroundColour("red")
		
		if panel.asmanimaldobentry.GetValue() == panel.evetteanimaldobentry.GetValue():
			
			panel.asmanimaldobentry.SetBackgroundColour("green")
			panel.evetteanimaldobentry.SetBackgroundColour("green")
			panel.animaldobsyncbutton.Disable()
			
		else:
			
			panel.asmanimaldobentry.SetBackgroundColour("red")
			panel.evetteanimaldobentry.SetBackgroundColour("red")
		
		if panel.asmanimaldeceaseddateentry.GetValue() == panel.evetteanimaldeceaseddateentry.GetValue():
			
			panel.asmanimaldeceaseddateentry.SetBackgroundColour("green")
			panel.evetteanimaldeceaseddateentry.SetBackgroundColour("green")
			panel.animaldeceaseddatesyncbutton.Disable()
			
		else:
			
			panel.asmanimaldeceaseddateentry.SetBackgroundColour("red")
			panel.evetteanimaldeceaseddateentry.SetBackgroundColour("red")
		
		if panel.asmanimalchipnoentry.GetValue() == panel.evetteanimalchipnoentry.GetValue():
			
			panel.asmanimalchipnoentry.SetBackgroundColour("green")
			panel.evetteanimalchipnoentry.SetBackgroundColour("green")
			panel.animalchipnosyncbutton.Disable()
			
		else:
			
			panel.asmanimalchipnoentry.SetBackgroundColour("red")
			panel.evetteanimalchipnoentry.SetBackgroundColour("red")
		
		ownermatch = True
		
		if panel.asmownernameentry.GetValue() == panel.evetteownernameentry.GetValue():
			
			panel.asmownernameentry.SetBackgroundColour("green")
			panel.evetteownernameentry.SetBackgroundColour("green")
			#ownernamesyncbutton.Disable()
			
		else:
			
			panel.asmownernameentry.SetBackgroundColour("red")
			panel.evetteownernameentry.SetBackgroundColour("red")
			ownermatch = False
		
		if panel.asmowneraddressentry.GetValue() == panel.evetteowneraddressentry.GetValue():
			
			panel.asmowneraddressentry.SetBackgroundColour("green")
			panel.evetteowneraddressentry.SetBackgroundColour("green")
			#owneraddresssyncbutton.Disable()
			
		else:
			
			panel.asmowneraddressentry.SetBackgroundColour("red")
			panel.evetteowneraddressentry.SetBackgroundColour("red")
			ownermatch = False
		
		if panel.asmownerpostcodeentry.GetValue() == panel.evetteownerpostcodeentry.GetValue():
			
			panel.asmownerpostcodeentry.SetBackgroundColour("green")
			panel.evetteownerpostcodeentry.SetBackgroundColour("green")
			#ownerpostcodesyncbutton.Disable()
			
		else:
			
			panel.asmownerpostcodeentry.SetBackgroundColour("red")
			panel.evetteownerpostcodeentry.SetBackgroundColour("red")
			ownermatch = False
		
		if panel.asmownerhometelephoneentry.GetValue() == panel.evetteownerhometelephoneentry.GetValue():
			
			panel.asmownerhometelephoneentry.SetBackgroundColour("green")
			panel.evetteownerhometelephoneentry.SetBackgroundColour("green")
			#ownerhometelephonesyncbutton.Disable()
			
		else:
			
			panel.asmownerhometelephoneentry.SetBackgroundColour("red")
			panel.evetteownerhometelephoneentry.SetBackgroundColour("red")
			ownermatch = False
		
		if panel.asmownermobiletelephoneentry.GetValue() == panel.evetteownermobiletelephoneentry.GetValue():
			
			panel.asmownermobiletelephoneentry.SetBackgroundColour("green")
			panel.evetteownermobiletelephoneentry.SetBackgroundColour("green")
			#ownermobiletelephonesyncbutton.Disable()
			
		else:
			
			panel.asmownermobiletelephoneentry.SetBackgroundColour("red")
			panel.evetteownermobiletelephoneentry.SetBackgroundColour("red")
			ownermatch = False
		
		if panel.asmownerworktelephoneentry.GetValue() == panel.evetteownerworktelephoneentry.GetValue():
			
			panel.asmownerworktelephoneentry.SetBackgroundColour("green")
			panel.evetteownerworktelephoneentry.SetBackgroundColour("green")
			#ownerworktelephonesyncbutton.Disable()
			
		else:
			
			panel.asmownerworktelephoneentry.SetBackgroundColour("red")
			panel.evetteownerworktelephoneentry.SetBackgroundColour("red")
			ownermatch = False
		
		if panel.asmowneremailaddressentry.GetValue() == panel.evetteowneremailaddressentry.GetValue():
			
			panel.asmowneremailaddressentry.SetBackgroundColour("green")
			panel.evetteowneremailaddressentry.SetBackgroundColour("green")
			#owneremailaddresssyncbutton.Disable()
			
		else:
			
			panel.asmowneremailaddressentry.SetBackgroundColour("red")
			panel.evetteowneremailaddressentry.SetBackgroundColour("red")
			ownermatch = False
		
		if ownermatch == True:
			
			panel.ownersyncbutton.Disable()
		
                for a in (
                panel.asmanimalnameentry,
		panel.evetteanimalnameentry,
		panel.asmanimaldobentry,
		panel.evetteanimaldobentry,
		panel.asmanimaldeceaseddateentry,
		panel.evetteanimaldeceaseddateentry,
		panel.asmanimalchipnoentry,
		panel.evetteanimalchipnoentry,
		panel.asmownernameentry,
		panel.evetteownernameentry,
		panel.asmowneraddressentry,
		panel.evetteowneraddressentry,
		panel.asmownerpostcodeentry,
		panel.evetteownerpostcodeentry,
		panel.asmownerhometelephoneentry,
		panel.evetteownerhometelephoneentry,
		panel.asmownermobiletelephoneentry,
		panel.evetteownermobiletelephoneentry,
		panel.asmownerworktelephoneentry,
		panel.evetteownerworktelephoneentry,
		panel.asmowneremailaddressentry,
		panel.evetteowneremailaddressentry ):
			
                        value = a.GetValue()
                        a.Clear()
                        a.SetValue(value)
	
	def SyncAnimalName(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		popupmenu = wx.Menu()
		popupmenu.asmref = panel.asmref
		popupmenu.panel = panel
		
		evettesync = wx.MenuItem(popupmenu, EVETTE_ANIMAL_NAME_SYNC, self.t("synctoevettelabel"))
		evettesync.SetBitmap(wx.Bitmap("icons/evettelogo.png"))
		popupmenu.AppendItem(evettesync)
		wx.EVT_MENU(popupmenu, EVETTE_ANIMAL_NAME_SYNC, self.SyncAnimalNameToEvette)
		
		asmsync = wx.MenuItem(popupmenu, ASM_ANIMAL_NAME_SYNC, self.t("synctoasmlabel"))
		asmsync.SetBitmap(wx.Bitmap("icons/asm.png"))
		popupmenu.AppendItem(asmsync)
		wx.EVT_MENU(popupmenu, ASM_ANIMAL_NAME_SYNC, self.SyncAnimalNameToASM)
		
		self.PopupMenu(popupmenu)
	
	def SyncAnimalNameToEvette(self, ID):
		
		popupmenu = ID.GetEventObject()
		asmref = popupmenu.asmref
		panel = popupmenu.panel
		
		asmconnection = db.GetASMConnection()
		
		action = "UPDATE animal SET AnimalName = \"" + self.animaldata.name + "\", LastChangedBy = \"Evette\", LastChangedDate =\"" + str(datetime.datetime.today()) + "\" WHERE ShelterCode = \"" + str(asmref) + "\""
		db.SendSQL(action, asmconnection)
		
		asmconnection.close()
		
		panel.asmanimalnameentry.SetValue(self.animaldata.name)
		panel.asmanimalnameentry.SetBackgroundColour("green")
		panel.evetteanimalnameentry.SetBackgroundColour("green")
		panel.animalnamesyncbutton.Disable()
	
	def SyncAnimalNameToASM(self, ID):
		
		popupmenu = ID.GetEventObject()
		panel = popupmenu.panel
		
		self.animaldata.name = panel.asmanimalnameentry.GetValue()
		self.nameentry.SetValue(panel.asmanimalnameentry.GetValue())
		self.animaldata.Submit()
		
		panel.evetteanimalnameentry.SetValue(panel.asmanimalnameentry.GetValue())
		panel.asmanimalnameentry.SetBackgroundColour("green")
		panel.evetteanimalnameentry.SetBackgroundColour("green")
		panel.animalnamesyncbutton.Disable()
	
	def SyncAnimalDOB(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		popupmenu = wx.Menu()
		popupmenu.asmref = panel.asmref
		popupmenu.panel = panel
		
		evettesync = wx.MenuItem(popupmenu, EVETTE_ANIMAL_DOB_SYNC, self.t("synctoevettelabel"))
		evettesync.SetBitmap(wx.Bitmap("icons/evettelogo.png"))
		popupmenu.AppendItem(evettesync)
		wx.EVT_MENU(popupmenu, EVETTE_ANIMAL_DOB_SYNC, self.SyncAnimalDOBToEvette)
		
		asmsync = wx.MenuItem(popupmenu, ASM_ANIMAL_DOB_SYNC, self.t("synctoasmlabel"))
		asmsync.SetBitmap(wx.Bitmap("icons/asm.png"))
		popupmenu.AppendItem(asmsync)
		wx.EVT_MENU(popupmenu, ASM_ANIMAL_DOB_SYNC, self.SyncAnimalDOBToASM)
		
		self.PopupMenu(popupmenu)
	
	def SyncAnimalDOBToEvette(self, ID):
		
		popupmenu = ID.GetEventObject()
		asmref = popupmenu.asmref
		panel = popupmenu.panel
		
		value = self.animaldata.dob
		
		try:
			
			if self.localsettings.dictionary["dateformat"][self.localsettings.language] == "DDMMYYYY":
				
				if len(value) == 4:
					
					day = "01"
					month = "01"
					year = value
					
				elif len(value) == 7:
					
					day = "01"
					month = value[:2]
					year = value[-4:]
					
				else:
					
					day = value[0:2]
					month = value[3:5]
					year = value[6:10]
				
			elif self.localsettings.dictionary["dateformat"][self.localsettings.language] == "MMDDYYYY":
				
				if len(value) == 4:
					
					day = "01"
					month = "01"
					year = value
					
				elif len(value) == 7:
					
					day = "01"
					month = value[:2]
					year = value[-4:]
					
				else:
					
					day = value[3:5]
					month = value[0:2]
					year = value[6:10]
				
			else:
				
				if len(value) == 4:
					
					day = "01"
					month = "01"
					year = value
					
				elif len(value) == 7:
					
					day = "01"
					month = value[:2]
					year = value[-4:]
					
				else:
					
					day = value[-2:]
					month = value[5:7]
					year = value[:4]
				
				
			dob = datetime.date(int(year), int(month), int(day))
			
			dob = miscmethods.GetSQLDateFromDate(dob)
			
			asmconnection = db.GetASMConnection()
			
			action = "UPDATE animal SET DateOfBirth = \"" + dob + "\", LastChangedBy = \"Evette\", LastChangedDate =\"" + str(datetime.datetime.today()) + "\" WHERE ShelterCode = \"" + str(asmref) + "\""
			db.SendSQL(action, asmconnection)
			
			asmconnection.close()
			
			panel.asmanimaldobentry.SetValue(self.animaldata.dob)
			panel.asmanimaldobentry.SetBackgroundColour("green")
			panel.evetteanimaldobentry.SetBackgroundColour("green")
			panel.animaldobsyncbutton.Disable()
			
		except:
			
			miscmethods.ShowMessage(self.t("invaliddobtooltip"), panel)
	
	def SyncAnimalDOBToASM(self, ID):
		
		popupmenu = ID.GetEventObject()
		panel = popupmenu.panel
		
		self.animaldata.dob = panel.asmanimaldobentry.GetValue()
		self.dobentry.SetValue(panel.asmanimaldobentry.GetValue())
		self.animaldata.Submit()
		
		panel.evetteanimaldobentry.SetValue(panel.asmanimaldobentry.GetValue())
		panel.asmanimaldobentry.SetBackgroundColour("green")
		panel.evetteanimaldobentry.SetBackgroundColour("green")
		panel.animaldobsyncbutton.Disable()
	
	def SyncAnimalDeceasedDate(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		popupmenu = wx.Menu()
		popupmenu.asmref = panel.asmref
		popupmenu.panel = panel
		
		evettesync = wx.MenuItem(popupmenu, EVETTE_ANIMAL_DECEASEDDATE_SYNC, self.t("synctoevettelabel"))
		evettesync.SetBitmap(wx.Bitmap("icons/evettelogo.png"))
		popupmenu.AppendItem(evettesync)
		wx.EVT_MENU(popupmenu, EVETTE_ANIMAL_DECEASEDDATE_SYNC, self.SyncAnimalDeceasedDateToEvette)
		
		asmsync = wx.MenuItem(popupmenu, ASM_ANIMAL_DECEASEDDATE_SYNC, self.t("synctoasmlabel"))
		asmsync.SetBitmap(wx.Bitmap("icons/asm.png"))
		popupmenu.AppendItem(asmsync)
		wx.EVT_MENU(popupmenu, ASM_ANIMAL_DECEASEDDATE_SYNC, self.SyncAnimalDeceasedDateToASM)
		
		self.PopupMenu(popupmenu)
	
	def SyncAnimalDeceasedDateToEvette(self, ID):
		
		popupmenu = ID.GetEventObject()
		asmref = popupmenu.asmref
		panel = popupmenu.panel
		
		asmconnection = db.GetASMConnection()
		
		if str(self.animaldata.deceaseddate) == "0000-00-00":
			
			action = "UPDATE animal SET DeceasedDate = NULL, LastChangedBy = \"Evette\", LastChangedDate =\"" + str(datetime.datetime.today()) + "\", PTSReason = \"\" WHERE ShelterCode = \"" + str(asmref) + "\""
			db.SendSQL(action, asmconnection)
			
		else:
			
			action = "SELECT Archived FROM animal WHERE ShelterCode = \"" + str(asmref) + "\""
			archived = db.SendSQL(action, asmconnection)[0][0]
			
			action = "UPDATE animal SET DeceasedDate = \"" + str(self.animaldata.deceaseddate) + "\", LastChangedBy = \"Evette\", LastChangedDate =\"" + str(datetime.datetime.today()) + "\", PTSReason = \"" + self.t("evettedeathreasonlabel") + "\" WHERE ShelterCode = \"" + str(asmref) + "\""
			db.SendSQL(action, asmconnection)
			
			if archived == 1:
				
				action = "UPDATE animal SET DiedOffShelter = 1 WHERE ShelterCode = \"" + str(asmref) + "\""
				
			else:
				
				action = "UPDATE animal SET DiedOffShelter = 0 WHERE ShelterCode = \"" + str(asmref) + "\""
			
			db.SendSQL(action, asmconnection)
		
		asmconnection.close()
		
		if self.animaldata.deceaseddate != "0000-00-00":
			
			output = miscmethods.FormatSQLDate(self.animaldata.deceaseddate, self.localsettings)
			
		elif self.animaldata.deceased == 1:
			
			output = self.t("yeslabel")
			
		else:
			
			output = self.t("nolabel")
		
		panel.asmanimaldeceaseddateentry.SetValue(output)
		panel.asmanimaldeceaseddateentry.SetBackgroundColour("green")
		panel.evetteanimaldeceaseddateentry.SetBackgroundColour("green")
		panel.animaldeceaseddatesyncbutton.Disable()
	
	def SyncAnimalDeceasedDateToASM(self, ID):
		
		popupmenu = ID.GetEventObject()
		panel = popupmenu.panel
		
		deceaseddate = panel.asmanimaldeceaseddateentry.GetValue()
		
		if deceaseddate == self.t("nolabel"):
			
			deceaseddate = "0000-00-00"
			self.animaldata.deceased = 0
			
			self.deathreasonentry.Clear()
			
			wx.TextCtrl.Clear(self.deceaseddatectrl)
			
			self.deathpanel.Disable()
			self.deceasedtickbox.SetValue(False)
			
			
		else:
			
			self.animaldata.deceased = 1
			self.animaldata.causeofdeath = self.t("asmdeathreasonlabel")
			self.deathreasonentry.SetValue(self.t("asmdeathreasonlabel"))
			
			wx.TextCtrl.SetValue(self.deceaseddatectrl, deceaseddate)
			
			self.deathpanel.Enable()
			self.deceasedtickbox.SetValue(True)
			
			value = deceaseddate
			
			if self.localsettings.dictionary["dateformat"][self.localsettings.language] == "DDMMYYYY":
				
				if len(value) == 4:
					
					day = "01"
					month = "01"
					year = value
					
				elif len(value) == 7:
					
					day = "01"
					month = value[:2]
					year = value[-4:]
					
				else:
					
					day = value[0:2]
					month = value[3:5]
					year = value[6:10]
				
			elif self.localsettings.dictionary["dateformat"][self.localsettings.language] == "MMDDYYYY":
				
				if len(value) == 4:
					
					day = "01"
					month = "01"
					year = value
					
				elif len(value) == 7:
					
					day = "01"
					month = value[:2]
					year = value[-4:]
					
				else:
					
					day = value[3:5]
					month = value[0:2]
					year = value[6:10]
				
			else:
				
				if len(value) == 4:
					
					day = "01"
					month = "01"
					year = value
					
				elif len(value) == 7:
					
					day = "01"
					month = value[:2]
					year = value[-4:]
					
				else:
					
					day = value[-2:]
					month = value[5:7]
					year = value[:4]
			
			deceaseddate = datetime.date(int(year), int(month), int(day))
			
			deceaseddate = miscmethods.GetSQLDateFromDate(deceaseddate)
		
		self.animaldata.deceaseddate = deceaseddate
		self.animaldata.Submit()
		
		panel.evetteanimaldeceaseddateentry.SetValue(panel.asmanimaldeceaseddateentry.GetValue())
		panel.asmanimaldeceaseddateentry.SetBackgroundColour("green")
		panel.evetteanimaldeceaseddateentry.SetBackgroundColour("green")
		panel.animaldeceaseddatesyncbutton.Disable()
	
	def SyncAnimalChipNo(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		popupmenu = wx.Menu()
		popupmenu.asmref = panel.asmref
		popupmenu.panel = panel
		
		evettesync = wx.MenuItem(popupmenu, EVETTE_ANIMAL_CHIPNO_SYNC, self.t("synctoevettelabel"))
		evettesync.SetBitmap(wx.Bitmap("icons/evettelogo.png"))
		popupmenu.AppendItem(evettesync)
		wx.EVT_MENU(popupmenu, EVETTE_ANIMAL_CHIPNO_SYNC, self.SyncAnimalChipNoToEvette)
		
		asmsync = wx.MenuItem(popupmenu, ASM_ANIMAL_CHIPNO_SYNC, self.t("synctoasmlabel"))
		asmsync.SetBitmap(wx.Bitmap("icons/asm.png"))
		popupmenu.AppendItem(asmsync)
		wx.EVT_MENU(popupmenu, ASM_ANIMAL_CHIPNO_SYNC, self.SyncAnimalChipNoToASM)
		
		self.PopupMenu(popupmenu)
	
	def SyncAnimalChipNoToEvette(self, ID):
		
		popupmenu = ID.GetEventObject()
		asmref = popupmenu.asmref
		panel = popupmenu.panel
		
		asmconnection = db.GetASMConnection()
		
		if self.animaldata.chipno != "":
			
			action = "UPDATE animal SET Identichipped = 1, IdentichipNumber = \"" + self.animaldata.chipno + "\", IdentichipDate = \"" + str(datetime.datetime.today()) + "\", LastChangedBy = \"Evette\", LastChangedDate =\"" + str(datetime.datetime.today()) + "\" WHERE ShelterCode = \"" + str(asmref) + "\""
			
		else:
			
			action = "UPDATE animal SET Identichipped = 0, IdentichipNumber = \"\", IdentichipDate = NULL, LastChangedBy = \"Evette\", LastChangedDate =\"" + str(datetime.datetime.today()) + "\" WHERE ShelterCode = \"" + str(asmref) + "\""
		
		db.SendSQL(action, asmconnection)
		
		asmconnection.close()
		
		panel.asmanimalchipnoentry.SetValue(self.animaldata.chipno)
		panel.asmanimalchipnoentry.SetBackgroundColour("green")
		panel.evetteanimalchipnoentry.SetBackgroundColour("green")
		panel.animalchipnosyncbutton.Disable()
	
	def SyncAnimalChipNoToASM(self, ID):
		
		popupmenu = ID.GetEventObject()
		panel = popupmenu.panel
		
		self.animaldata.chipno = panel.asmanimalchipnoentry.GetValue()
		self.chipnoentry.SetValue(panel.asmanimalchipnoentry.GetValue())
		self.animaldata.Submit()
		
		panel.evetteanimalchipnoentry.SetValue(panel.asmanimalchipnoentry.GetValue())
		panel.asmanimalchipnoentry.SetBackgroundColour("green")
		panel.evetteanimalchipnoentry.SetBackgroundColour("green")
		panel.animalchipnosyncbutton.Disable()
	
	def SyncOwner(self, ID):
		
		#panel.asmanimalnameentry,
		#panel.evetteanimalnameentry,
		#panel.asmanimaldobentry,
		#panel.evetteanimaldobentry,
		#panel.asmanimaldeceaseddateentry,
		#panel.evetteanimaldeceaseddateentry,
		#panel.asmanimalchipnoentry,
		#panel.evetteanimalchipnoentry,
		#panel.asmownernameentry,
		#panel.evetteownernameentry,
		#panel.asmowneraddressentry,
		#panel.evetteowneraddressentry,
		#panel.asmownerpostcodeentry,
		#panel.evetteownerpostcodeentry,
		#panel.asmownerhometelephoneentry,
		#panel.evetteownerhometelephoneentry,
		#panel.asmownermobiletelephoneentry,
		#panel.evetteownermobiletelephoneentry,
		#panel.asmownerworktelephoneentry,
		#panel.evetteownerworktelephoneentry,
		#panel.asmowneremailaddressentry,
		#panel.evetteowneremailaddressentry
		
		panel = ID.GetEventObject().GetParent()
		
		popupmenu = wx.Menu()
		popupmenu.asmref = panel.asmref
		popupmenu.panel = panel
		popupmenu.notebook = panel.GetGrandParent().GetParent()
		
		if self.animaldata.ownerid == self.localsettings.shelterid:
			
			importnewasmowner = wx.MenuItem(popupmenu, IMPORT_NEW_ASM_OWNER, self.t("importnewasmownermenuitem"))
			importnewasmowner.SetBitmap(wx.Bitmap("icons/new.png"))
			popupmenu.AppendItem(importnewasmowner)
			wx.EVT_MENU(popupmenu, IMPORT_NEW_ASM_OWNER, self.ImportNewASMOwner)
			
		elif panel.asmonshelter == False:
			
			importnewasmowner = wx.MenuItem(popupmenu, IMPORT_NEW_ASM_OWNER, self.t("importnewasmownermenuitem"))
			importnewasmowner.SetBitmap(wx.Bitmap("icons/new.png"))
			popupmenu.AppendItem(importnewasmowner)
			wx.EVT_MENU(popupmenu, IMPORT_NEW_ASM_OWNER, self.ImportNewASMOwner)
			
			evettesync = wx.MenuItem(popupmenu, UPDATE_OWNER_EVETTE_SYNC, self.t("updateownermenuitem") + " - " + self.t("synctoevettelabel"))
			evettesync.SetBitmap(wx.Bitmap("icons/evettelogo.png"))
			popupmenu.AppendItem(evettesync)
			wx.EVT_MENU(popupmenu, UPDATE_OWNER_EVETTE_SYNC, self.SyncOwnerToEvette)
			
			asmsync = wx.MenuItem(popupmenu, UPDATE_OWNER_ASM_SYNC, self.t("updateownermenuitem") + " - " + self.t("synctoasmlabel"))
			asmsync.SetBitmap(wx.Bitmap("icons/asm.png"))
			popupmenu.AppendItem(asmsync)
			wx.EVT_MENU(popupmenu, UPDATE_OWNER_ASM_SYNC, self.SyncOwnerToASM)
			
		else:
			
			returntoshelter = wx.MenuItem(popupmenu, IMPORT_NEW_ASM_OWNER, self.t("returntoshelterlabel"))
			returntoshelter.SetBitmap(wx.Bitmap("icons/asm.png"))
			popupmenu.AppendItem(returntoshelter)
			wx.EVT_MENU(popupmenu, IMPORT_NEW_ASM_OWNER, self.ReturnEvetteAnimalToShelter)
		
		self.PopupMenu(popupmenu)
	
	def ReturnEvetteAnimalToShelter(self, ID):
		
		panel = ID.GetEventObject().panel
		
		self.animaldata.ownerid = self.localsettings.shelterid
		self.animaldata.Submit()
		
		self.clientdata = clientmethods.ClientSettings(self.localsettings, self.localsettings.shelterid)
		
		self.UpdateOwnerLabel()
		
		self.UpdateEvetteInfo(panel)
		self.MatchASMEvetteInfo(panel)
	
	def ImportNewASMOwner(self, ID):
		
		popupmenu = ID.GetEventObject()
		panel = popupmenu.panel
		notebook = popupmenu.notebook
		
		asmconnection = db.GetASMConnection()
		action = "SELECT owner.ID, owner.OwnerName, owner.OwnerAddress, owner.OwnerPostcode, owner.OwnerTitle, owner.OwnerForenames, owner.OwnerSurname, owner.HomeTelephone, owner.MobileTelephone, owner.WorkTelephone, owner.EmailAddress, owner.Comments FROM animal INNER JOIN adoption ON animal.ActiveMovementID = adoption.ID INNER JOIN owner ON adoption.OwnerID = owner.ID WHERE animal.ShelterCode = \"" + str(panel.asmref) + "\""
		results = db.SendSQL(action, asmconnection)
		asmconnection.close()
		
		clientdata = results[0]
		
		title = miscmethods.CorrectNullString(clientdata[4])
		forenames = miscmethods.CorrectNullString(clientdata[5])
		surname = miscmethods.CorrectNullString(clientdata[6])
		address = miscmethods.CorrectNullString(clientdata[2])
		postcode = miscmethods.CorrectNullString(clientdata[3])
		hometelephone = miscmethods.CorrectNullString(clientdata[7])
		mobiletelephone = miscmethods.CorrectNullString(clientdata[8])
		worktelephone = miscmethods.CorrectNullString(clientdata[9])
		emailaddress = miscmethods.CorrectNullString(clientdata[10])
		comments = miscmethods.CorrectNullString(clientdata[11])
		
		clientsettings = clientmethods.ClientSettings(self.localsettings)
		
		clientsettings.title = str(title)
		clientsettings.forenames = str(forenames)
		clientsettings.surname = str(surname)
		clientsettings.address = str(address)
		clientsettings.postcode = str(postcode)
		clientsettings.hometelephone = str(hometelephone)
		clientsettings.mobiletelephone = str(mobiletelephone)
		clientsettings.worktelephone = str(worktelephone)
		clientsettings.emailaddress = str(emailaddress)
		clientsettings.comments = self.t("asmimportlabel") + ":\n" + str(comments)
		
		clientsettings = clientmethods.CheckForExistingClient(self, clientsettings, False).clientdata
		
		clientsettings.Submit()
		
		self.clientdata = clientsettings
		
		self.animaldata.ownerid = self.clientdata.ID
		self.animaldata.Submit()
		
		self.UpdateOwnerLabel()
		
		self.UpdateEvetteInfo(panel)
		self.MatchASMEvetteInfo(panel)
	
	def SyncOwnerToEvette(self, ID):
		
		popupmenu = ID.GetEventObject()
		panel = popupmenu.panel
		
		asmconnection = db.GetASMConnection()
		
		action = "SELECT owner.ID FROM animal INNER JOIN adoption ON animal.ActiveMovementID = adoption.ID INNER JOIN owner ON adoption.OwnerID = owner.ID WHERE animal.ShelterCode = \"" + str(panel.asmref) + "\""
		clientid = db.SendSQL(action, asmconnection)[0][0]
		
		action = "UPDATE owner SET OwnerTitle = \"" + self.clientdata.title + "\", OwnerForenames = \"" + self.clientdata.forenames + "\", OwnerSurname = \"" + self.clientdata.surname + "\", OwnerAddress = \"" + self.clientdata.address + "\", OwnerPostcode = \"" + self.clientdata.postcode + "\", HomeTelephone = \"" + self.clientdata.hometelephone + "\", MobileTelephone = \"" + self.clientdata.mobiletelephone + "\", WorkTelephone = \"" + self.clientdata.worktelephone + "\", EmailAddress = \"" + self.clientdata.emailaddress + "\", Comments = CONCAT(Comments, \"" + "\n" + self.t("evettedeathreasonlabel") + "\"), LastChangedBy = \"Evette\", LastChangedDate = \"" + str(datetime.datetime.today()) + "\" WHERE ID = \"" + str(clientid) + "\""
		db.SendSQL(action, asmconnection)
		
		asmconnection.close()
		
		self.UpdateASMInfo(panel)
		self.MatchASMEvetteInfo(panel)
		
	def SyncOwnerToASM(self, ID):
		
		popupmenu = ID.GetEventObject()
		panel = popupmenu.panel
		
		asmconnection = db.GetASMConnection()
		action = "SELECT owner.ID, owner.OwnerName, owner.OwnerAddress, owner.OwnerPostcode, owner.OwnerTitle, owner.OwnerForenames, owner.OwnerSurname, owner.HomeTelephone, owner.MobileTelephone, owner.WorkTelephone, owner.EmailAddress FROM animal INNER JOIN adoption ON animal.ActiveMovementID = adoption.ID INNER JOIN owner ON adoption.OwnerID = owner.ID WHERE animal.ShelterCode = \"" + str(panel.asmref) + "\""
		results = db.SendSQL(action, asmconnection)
		asmconnection.close()
		
		clientdata = results[0]
		
		self.clientdata.title = miscmethods.CorrectNullString(clientdata[4])
		self.clientdata.forenames = miscmethods.CorrectNullString(clientdata[5])
		self.clientdata.surname = miscmethods.CorrectNullString(clientdata[6])
		self.clientdata.address = miscmethods.CorrectNullString(clientdata[2])
		self.clientdata.postcode = miscmethods.CorrectNullString(clientdata[3])
		self.clientdata.hometelephone = miscmethods.CorrectNullString(clientdata[7])
		self.clientdata.mobiletelephone = miscmethods.CorrectNullString(clientdata[8])
		self.clientdata.worktelephone = miscmethods.CorrectNullString(clientdata[9])
		self.clientdata.emailaddress = miscmethods.CorrectNullString(clientdata[10])
		
		self.clientdata.Submit()
		
		self.UpdateOwnerLabel()
		
		self.UpdateEvetteInfo(panel)
		self.MatchASMEvetteInfo(panel)

class VaccinationPanel(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return  self.parent.animaldata.localsettings.t(field,idx)
	
	def __init__(self, parent):
		
		self.parent = parent.GetGrandParent()
		
		wx.Panel.__init__(self, parent)
		
		parent.vaccinationslistbox.Bind(wx.EVT_LISTBOX, self.VaccinationSelected)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		topspacer = wx.StaticText(self, -1, "", size=(-1,10))
		topsizer.Add(topspacer, 0, wx.EXPAND)
		
		toolssizer1 = wx.BoxSizer(wx.HORIZONTAL)
		
		resetbitmap = wx.Bitmap("icons/reset.png")
		resetbutton = wx.BitmapButton(self, -1, resetbitmap)
		resetbutton.Bind(wx.EVT_BUTTON, self.Reset)
		resetbutton.SetToolTipString(self.t("animalresetvaccinationentries"))
		toolssizer1.Add(resetbutton, 0, wx.EXPAND)
		
		toolssizer1.Add(wx.StaticText(self, -1, "", size=(5,-1)), 0, wx.EXPAND)
		
		namelabel = wx.StaticText(self, -1, self.t("animalvaccinelabel") + ":")
		toolssizer1.Add(namelabel, 0, wx.ALIGN_CENTER)
		
		action = "SELECT Name FROM medication WHERE Type = 1"
		results = db.SendSQL(action, self.parent.animaldata.localsettings.dbconnection)
		
		
		vaccinelist = []
		
		for a in results:
			vaccinelist.append(a[0])
		
		namechoice = wx.ComboBox(self, -1, "", choices=vaccinelist, size=(300,-1))
		toolssizer1.Add(namechoice, 1, wx.EXPAND)
		
		topsizer.Add(toolssizer1, 0, wx.ALIGN_CENTER)
		
		topspacer1 = wx.StaticText(self, -1, "", size=(-1,10))
		topsizer.Add(topspacer1, 0, wx.EXPAND)
		
		toolssizer2 = wx.BoxSizer(wx.HORIZONTAL)
		
		givenlabel = wx.StaticText(self, -1, self.t("animalgivenlabel"))
		toolssizer2.Add(givenlabel, 0, wx.ALIGN_CENTER)
		
		givenentry = customwidgets.DateCtrl(self, self.parent.animaldata.localsettings)
		toolssizer2.Add(givenentry, 1, wx.EXPAND)
		
		nextlabel = wx.StaticText(self, -1, self.t("animalnextlabel"))
		toolssizer2.Add(nextlabel, 0, wx.ALIGN_CENTER)
		
		nextentry = customwidgets.DateCtrl(self, self.parent.animaldata.localsettings)
		toolssizer2.Add(nextentry, 1, wx.EXPAND)
		
		topsizer.Add(toolssizer2, 0, wx.ALIGN_CENTER)
		
		topspacer2 = wx.StaticText(self, -1, "", size=(-1,10))
		topsizer.Add(topspacer2, 0, wx.EXPAND)
		
		toolssizer3 = wx.BoxSizer(wx.HORIZONTAL)
		
		deletebitmap = wx.Bitmap("icons/delete.png")
		deletebutton = wx.BitmapButton(self, -1, deletebitmap)
		deletebutton.Bind(wx.EVT_BUTTON, self.Delete)
		deletebutton.Disable()
		deletebutton.SetToolTipString(self.t("animaldeletevaccinationtooltip"))
		toolssizer3.Add(deletebutton, 0, wx.EXPAND)
		
		batchlabel = wx.StaticText(self, -1, self.t("animalvaccinationbatchlabel"))
		toolssizer3.Add(batchlabel, 0, wx.ALIGN_CENTER)
		
		batchentry = wx.TextCtrl(self, -1, "", size=(300,-1))
		toolssizer3.Add(batchentry, 1, wx.EXPAND)
		
		submitspacer = wx.StaticText(self, -1, "", size=(5,-1))
		toolssizer3.Add(submitspacer, 0, wx.EXPAND)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		submitbutton = wx.BitmapButton(self, -1, submitbitmap)
		submitbutton.Bind(wx.EVT_BUTTON, self.Submit)
		submitbutton.SetToolTipString(self.t("animalsubmitvaccinationtooltip"))
		
		toolssizer3.Add(submitbutton, 0, wx.EXPAND)
		
		topsizer.Add(toolssizer3, 0, wx.ALIGN_CENTER)
		
		self.SetSizer(topsizer)
		
		self.namechoice = namechoice
		self.givenentry = givenentry
		self.nextentry = nextentry
		self.batchentry = batchentry
		self.deletebutton = deletebutton
		self.localsettings = self.parent.animaldata.localsettings
		self.vaccinationslistbox = parent.vaccinationslistbox
		
	
	def Reset(self, ID=False):
		
		self.namechoice.SetValue("")
		self.givenentry.GetToday()
		self.nextentry.GetToday()
		self.batchentry.Clear()
		self.deletebutton.Disable()
		self.vaccinationslistbox.SetSelection(-1)
	
	def VaccinationSelected(self, ID=False):
		
		self.editvaccinationbutton.Enable()
		self.deletevaccinationbutton.Enable()
		
		#listboxid = self.vaccinationslistbox.GetSelection()
		
		#name = self.vaccinationslistbox.htmllist[listboxid][2]
		#given = self.vaccinationslistbox.htmllist[listboxid][0]
		#given = miscmethods.GetWXDateFromDate(given)
		#next = self.vaccinationslistbox.htmllist[listboxid][4]
		#next = miscmethods.GetWXDateFromDate(next)
		#batch = self.vaccinationslistbox.htmllist[listboxid][3]
		
		#self.namechoice.SetValue(name)
		#self.givenentry.SetValue(given)
		#self.nextentry.SetValue(next)
		#self.batchentry.SetValue(batch)
		#self.deletebutton.Enable()
	
	def Submit(self, ID=False):
		
		name = self.namechoice.GetValue()
		given = self.givenentry.GetValue()
		given = miscmethods.GetSQLDateFromWXDate(given)
		next = self.nextentry.GetValue()
		next = miscmethods.GetSQLDateFromWXDate(next)
		batch = self.batchentry.GetValue()
		
		listboxid = self.vaccinationslistbox.GetSelection()
		
		if listboxid > -1:##editing an existing vaccination
			
			ID = self.vaccinationslistbox.htmllist[listboxid][1]
			vaccinationid = self.vaccinationslistbox.htmllist[listboxid][5]
			
		else:
			
			ID = False
			vaccinationid = False
		
		if vaccinationid != False:
			
			dbmethods.WriteToVaccinationOutTable(self.localsettings.dbconnection, ID, vaccinationid, given, 1, False, False, False, next)
			
		else:
			
			animalid = self.parent.animaldata.ID
			dbmethods.WriteToManualVaccinationTable(self.localsettings.dbconnection, ID, animalid, given, name, batch, next)
		
		
		
		self.vaccinationslistbox.RefreshList()
		self.Reset()
	
	def Delete(self, ID=False):
		
		listboxid = self.vaccinationslistbox.GetSelection()
		
		ID = self.vaccinationslistbox.htmllist[listboxid][1]
		vaccinationid = self.vaccinationslistbox.htmllist[listboxid][5]
		
		if miscmethods.ConfirmMessage(self.t("animalconfirmdeletevaccinationmessage")):
			
			if vaccinationid == 0:
				
				action = "DELETE FROM manualvaccination WHERE ID = " + str(ID)
				
			else:
				
				action = "DELETE FROM vaccinationout WHERE ID = " + str(ID)
			
			db.SendSQL(action, self.localsettings.dbconnection)
			
			self.vaccinationslistbox.RefreshList()
			
			self.Reset()

class WeightPanel(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return  self.animaldata.localsettings.t(field,idx)
	
	def __init__(self, parent, animaldata):
		
		self.animaldata = animaldata
		
		self.animalpanel = parent.GetParent()
		
		wx.Panel.__init__(self, parent)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		unitentry = wx.Choice(self, -1, choices=("kg", "g"))
		unitentry.SetSelection(0)
		topsizer.Add(unitentry, 0, wx.ALIGN_RIGHT)
		
		listbox = WeightListbox(self, self.animaldata.localsettings)
		listbox.Bind(wx.EVT_LISTBOX, self.WeightSelected)
		listbox.Bind(wx.EVT_RIGHT_DOWN, self.WeightPopup)
		listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EditWeight)
		
		topsizer.Add(listbox, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.selectedweight = False
		
		self.listbox = listbox
		
		self.unitentry = unitentry
		
		self.unitentry.Bind(wx.EVT_CHOICE, self.listbox.RefreshList)
		
		self.listbox.RefreshList()
	
	def WeightPopup(self, ID):
		
		popupmenu = wx.Menu()
		
		addweight = wx.MenuItem(popupmenu, ADD_WEIGHT, self.t("addlabel"))
		addweight.SetBitmap(wx.Bitmap("icons/new.png"))
		popupmenu.AppendItem(addweight)
		wx.EVT_MENU(popupmenu, ADD_WEIGHT, self.NewWeight)
		
		if self.selectedweight != False:
			
			editweight = wx.MenuItem(popupmenu, EDIT_WEIGHT, self.t("editlabel"))
			editweight.SetBitmap(wx.Bitmap("icons/edit.png"))
			popupmenu.AppendItem(editweight)
			wx.EVT_MENU(popupmenu, EDIT_WEIGHT, self.EditWeight)
			
			deleteweight = wx.MenuItem(popupmenu, DELETE_WEIGHT, self.t("deletelabel"))
			deleteweight.SetBitmap(wx.Bitmap("icons/delete.png"))
			popupmenu.AppendItem(deleteweight)
			wx.EVT_MENU(popupmenu, DELETE_WEIGHT, self.Delete)
		
		popupmenu.AppendSeparator()
		
		refreshweight = wx.MenuItem(popupmenu, REFRESH_WEIGHTS, self.t("refreshlabel"))
		refreshweight.SetBitmap(wx.Bitmap("icons/refresh.png"))
		popupmenu.AppendItem(refreshweight)
		wx.EVT_MENU(popupmenu, REFRESH_WEIGHTS, self.listbox.RefreshList)
		
		self.PopupMenu(popupmenu)
	
	def NewWeight(self, ID):
		
		self.EditWeightDialog(True)
	
	def EditWeight(self, ID):
		
		self.EditWeightDialog(False)
	
	def EditWeightDialog(self, newweight):
		
		dialog = wx.Dialog(self, -1, self.t("editweightlabel"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		panel.newweight = newweight
		
		topsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		datelabel = wx.StaticText(panel, -1, self.t("datelabel") + ":")
		topsizer.Add(datelabel, 0, wx.ALIGN_CENTER)
		
		dateentry = customwidgets.DateCtrl(panel, self.animaldata.localsettings)
		topsizer.Add(dateentry, 0, wx.EXPAND)
		
		if newweight == False:
			
			date = self.selectedweight[1]
			date = miscmethods.GetWXDateFromSQLDate(date)
			dateentry.SetValue(date)
		
		weightlabel = wx.StaticText(panel, -1, miscmethods.NoWrap(" " + self.t("weightpanelpagetitle") + ":"))
		topsizer.Add(weightlabel, 0, wx.ALIGN_CENTER)
		
		weightentry = wx.TextCtrl(panel, -1, "")
		weightentry.SetFocus()
		topsizer.Add(weightentry, 0, wx.EXPAND)
		
		if newweight == False:
			
			weight = self.selectedweight[3]
			
			unit = self.unitentry.GetSelection()
			
			if unit == 0:
				
				weight = float(weight) / 1000.00
			
			weightentry.SetValue(str(weight))
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		submitbutton = wx.BitmapButton(panel, -1, submitbitmap)
		submitbutton.SetToolTipString(self.t("submitlabel"))
		submitbutton.Bind(wx.EVT_BUTTON, self.SubmitWeight)
		topsizer.Add(submitbutton, 0, wx.EXPAND)
		
		panel.SetSizer(topsizer)
		
		panel.dateentry = dateentry
		panel.weightentry = weightentry
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		dialog.Fit()
		
		dialog.ShowModal()
	
	def WeightSelected(self, ID=False):
		
		#self.deletebutton.Enable()
		#self.editbutton.Enable()
		
		listboxid = self.listbox.GetSelection()
		
		self.selectedweight = self.listbox.htmllist[listboxid]
	
	def Delete(self, ID=False):
		
		if miscmethods.ConfirmMessage(self.t("deleteweightconfirm")):
			
			action = "DELETE FROM weight WHERE ID = " + str(self.selectedweight[0])
			db.SendSQL(action, self.animaldata.localsettings.dbconnection)
			
			self.selectedweight = False
			
			self.listbox.RefreshList()
	
	def SubmitWeight(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		date = panel.dateentry.GetValue()
		date = miscmethods.GetSQLDateFromWXDate(date)
		
		weight = panel.weightentry.GetValue()
		
		unit = self.unitentry.GetSelection()
		
		if unit == 0:
			
			weight = float(weight) * 1000.00
		
		if panel.newweight == False:
			
			changelog = self.selectedweight[4]
			selectedweightid = self.selectedweight[0]
			
		else:
			
			changelog = False
			selectedweightid = False
		
		newweightid = dbmethods.WriteToWeightTable(self.animaldata.localsettings.dbconnection, selectedweightid, self.animaldata.ID, date, weight, self.animaldata.localsettings, changelog)
		
		self.listbox.RefreshList()
		
		if self.selectedweight == 0:
			
			listposition = 0
			
			for a in range(0, len(self.listbox.htmllist)):
				
				if self.listbox.htmllist[a][0] == newweightid:
					
					listposition = a
					
					self.selectedweight = self.listbox.htmllist[a]
			
			self.listbox.SetSelection(listposition)
			self.WeightSelected()
		
		panel.GetParent().Close()

class WeightListbox(wx.HtmlListBox):
	
	def __init__(self, parent, localsettings):
		
		wx.HtmlListBox.__init__(self, parent, -1)
		
		self.htmllist = []
		self.localsettings = localsettings
		self.parent = parent
		self.SetItemCount(0)
		self.SetSelection(-1)
		self.unit = 0
	
	def OnGetItem(self, n):
		
		if len(self.htmllist) > 0:
			
			date = self.htmllist[n][1]
			date = miscmethods.FormatDate(date, self.localsettings)
			
			weight = self.htmllist[n][3]
			
			try:
				difference = int(weight) - int(self.htmllist[n + 1][3])
				
				if difference < 0:
					
					differencecolour = "red"
					
					differenceimage = "<img src=icons/downarrowred.png>"
					
					difference = difference * -1
					
				elif difference == 0:
					
					differencecolour = "blue"
					
					differenceimage = "<img src=icons/rightarrow.png>"
					
				else:
					
					differencecolour = "green"
					
					differenceimage = "<img src=icons/uparrow.png>"
			except:
				difference = ""
				differencecolour = "black"
				differenceimage = ""
			
			
			if self.unit == 0:
				
				weight = float(weight) / 1000.00
				unit = "kg"
				
				if difference != "":
					difference = float(difference) / 1000.00
				
			else:
				
				unit = "g"
			
			if difference == 0:
				
				difference = self.parent.t("samelabel")
				
			elif difference != "":
				
				difference = str(difference) + unit
			
			output = "<table cellpadding=0 cellspacing=0 border=0><tr><td valign=middle align=left nowrap width=200><font color=blue size=12pt>" + date + "</font> - " + str(weight) + unit + "</td><td valign=middle>" + differenceimage + "</td><td valign=middle nowrap width=100%><font color=" + differencecolour + ">" + str(difference) + "</font></td></tr></table>"
			
			return output
	
	def RefreshList(self, ID=False):
		
		self.Hide()
		
		self.SetSelection(-1)
		
		action = "SELECT * FROM weight WHERE AnimalID = " + str(self.parent.animaldata.ID) + " ORDER BY Date desc"
		self.htmllist = db.SendSQL(action, self.localsettings.dbconnection)
		
		self.unit = self.parent.unitentry.GetSelection()
		
		self.SetItemCount(len(self.htmllist))
		
		#if len(self.htmllist) == 0:
			#self.Disable()
		#else:
			#self.Enable()
		
		if self.parent.selectedweight != False:
			
			count = 0
			
			for a in self.htmllist:
				
				if a[0] == self.parent.selectedweight[0]:
					
					self.SetSelection(count)
				
				count = count + 1
		
		self.Show()

def ChooseAnimalForm(parent):
	
	animaldata = parent.animaldata
	
	clientdata = parent.clientdata
	
	dialog = wx.Dialog(parent, -1, "Choose a template")
	
	dialogsizer = wx.BoxSizer(wx.VERTICAL)
	
	panel = wx.Panel(dialog)
	
	panel.animaldata = animaldata
	panel.clientdata = clientdata
	
	topsizer = wx.BoxSizer(wx.VERTICAL)
	
	action = "SELECT Title FROM form WHERE FormType = \"animal\""
	results = db.SendSQL(action, animaldata.localsettings.dbconnection)
	
	
	panel.listbox = wx.ListBox(panel, -1)
	panel.listboxtitles = []
	
	for a in results:
		panel.listbox.Append(a[0])
		panel.listboxtitles.append(a[0])
	
	if len(panel.listboxtitles) > 0:
		
		panel.listbox.SetSelection(0)
	
	topsizer.Add(panel.listbox, 1, wx.EXPAND)
	
	submitbutton = wx.Button(panel, -1, "Submit")
	submitbutton.Bind(wx.EVT_BUTTON, GenerateAnimalForm)
	topsizer.Add(submitbutton, 0, wx.ALIGN_CENTER)
	
	panel.SetSizer(topsizer)
	
	dialogsizer.Add(panel, 1, wx.EXPAND)
	
	dialog.SetSizer(dialogsizer)
	
	dialog.ShowModal()

def GenerateAnimalForm(ID):
	
	panel = ID.GetEventObject().GetParent()
	dialog = panel.GetParent()
	
	listboxid = panel.listbox.GetSelection()
	title = panel.listboxtitles[listboxid]
	
	formmethods.GenerateAnimalForm(title, panel.clientdata, panel.animaldata)
	
	dialog.Close()

def TransferOwnerShip(ID):
	
	animalpanel = ID.GetEventObject().animalpanel
	
	ChooseNewOwnerDialog(animalpanel)
	
	#animaldata.ownerid = 37
	
	#animaldata.Submit()

def ChooseNewOwnerDialog(animalpanel):
	
	animaldata = animalpanel.animaldata
	
	animalpanel.clientdialogid = 0
	
	clientid = clientmethods.FindClientDialog(animalpanel, animaldata.localsettings)
	
	if animalpanel.clientdialogid != 0:
		
		animaldata.ownerid = animalpanel.clientdialogid
		
		animaldata.Submit()
	
		animalpanel.animaldata = animaldata
	
		animalpanel.clientdata = clientmethods.ClientSettings(animaldata.localsettings, animalpanel.clientdialogid)
	
		animalpanel.UpdateOwnerLabel()
	
		#panel.GetParent().Close()

def NewOwnerSelected(ID):
	
	panel = ID.GetEventObject().GetParent()
	
	listboxid = panel.listbox.GetSelection()
	
	ownerid = panel.clientdata[listboxid][0]
	
	panel.animaldata.ownerid = ownerid
	
	panel.animaldata.Submit()
	
	panel.animalpanel.animaldata = panel.animaldata
	
	panel.animalpanel.clientdata = clientmethods.ClientSettings(panel.animaldata.localsettings, ownerid)
	
	panel.animalpanel.UpdateOwnerLabel()
	
	panel.GetParent().Close()

class AnimalAppointmentBrowser(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return  self.animaldata.localsettings.t(field, idx)
	
	def __init__(self, parent, animaldata):
		
		self.parent = parent
		self.animaldata = animaldata
		self.animalpanel = parent.GetParent()
		
		wx.Panel.__init__(self, self.parent)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		listbox = customwidgets.AppointmentsSummaryListbox(self, self.animaldata)
		#listbox.Bind(wx.EVT_LIST_ITEM_SELECTED, self.animalpanel.ShowAppointmentDetails)
		listbox.listctrl.Bind(wx.EVT_RIGHT_DOWN, self.animalpanel.AnimalAppointmentPopup)
		
		if self.animaldata.localsettings.editappointments == 1:
			
			listbox.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.animalpanel.Edit)
		
		topsizer.Add(listbox, 1, wx.EXPAND)
		
		legendsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		legendsizer.Add(wx.StaticBitmap(self, -1, wx.Bitmap("icons/ontime.png")), 0, wx.ALIGN_CENTER)
		legendsizer.Add(wx.StaticText(self, -1, self.t("ontimelabel")), 0, wx.ALIGN_CENTER)
		
		legendsizer.Add(wx.StaticText(self, -1,"", size=(10, 0)), 0, wx.ALIGN_CENTER)
		
		legendsizer.Add(wx.StaticBitmap(self, -1, wx.Bitmap("icons/late.png")), 0, wx.ALIGN_CENTER)
		legendsizer.Add(wx.StaticText(self, -1, self.t("latelabel")), 0, wx.ALIGN_CENTER)
		
		legendsizer.Add(wx.StaticText(self, -1,"", size=(10, 0)), 0, wx.ALIGN_CENTER)
		
		legendsizer.Add(wx.StaticBitmap(self, -1, wx.Bitmap("icons/dna.png")), 0, wx.ALIGN_CENTER)
		legendsizer.Add(wx.StaticText(self, -1, self.t("dnalabel")), 0, wx.ALIGN_CENTER)
		
		topsizer.Add(legendsizer, 0, wx.ALIGN_RIGHT)
		
		self.SetSizer(topsizer)
		
		self.animalpanel.animalappointmentslistbox = listbox
