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
import clientmethods
import animalmethods
import diarymethods
import customwidgets
import wx.lib.mixins.listctrl as listmix
import sys

NEW_LOST = 2001
EDIT_LOST = 2002
DELETE_LOST = 2003
NEW_FOUND = 2004
EDIT_FOUND = 2005
DELETE_FOUND = 2006
ADD_CLIENT = 2007
EDIT_CLIENT = 2008
FIND_CLIENT = 2009
CONTACT_CLIENT = 2010
EDIT_ANIMAL = 2011

class LostAndFoundSettings:
	
	#ID, LostOrFound, ContactID, Species, Date, Sex, Neutered, FurLength, Colour1, Colour2, Colour3, Collar, CollarDescription, Size, Age, IsChipped, ChipNo, Temperament, Comment, DateComplete, ChangeLog)
	
	def __init__(self, localsettings, ID=False):
		
		self.localsettings = localsettings
		
		if ID == False:
			
			self.ID = False
			self.lostorfound = 0
			self.contactid = 0
			self.species = u""
			self.date = "0000-00-00"
			self.sex = 0
			self.neutered = 0
			self.furlength = 0
			self.colour1 = u""
			self.colour2 = u""
			self.colour3 = u""
			self.collar = 0
			self.collardescription = u""
			self.size = 0
			self.age = 0
			self.ischipped = 0
			self.chipno = ""
			self.temperament = 0
			self.comments = u""
			self.datecomplete = "0000-00-00"
			self.area = u""
			self.animalid = 0
			
			currenttime = datetime.datetime.today().strftime("%x %X")
			self.changelog = str(currenttime) + "%%%" + str(self.localsettings.userid)
		else:
			
			action = "SELECT * FROM lostandfound WHERE ID = " + str(ID)
			results = db.SendSQL(action, self.localsettings.dbconnection)
			
			self.ID = ID
			self.lostorfound = results[0][1]
			self.contactid = results[0][2]
			self.species = unicode(results[0][3], "utf8")
			self.date = results[0][4]
			self.sex = results[0][5]
			self.neutered = results[0][6]
			self.furlength = results[0][7]
			self.colour1 = unicode(results[0][8], "utf8")
			self.colour2 = unicode(results[0][9], "utf8")
			self.colour3 = unicode(results[0][10], "utf8")
			self.collar = results[0][11]
			self.collardescription = unicode(results[0][12], "utf8")
			self.size = results[0][13]
			self.age = results[0][14]
			self.ischipped = results[0][15]
			self.chipno = unicode(results[0][16], "utf8")
			self.temperament = results[0][17]
			self.comments = unicode(results[0][18], "utf8")
			self.datecomplete = results[0][19]
			self.changelog = results[0][20]
			self.area = unicode(results[0][21], "utf8")
			self.animalid = results[0][22]
	
	def Submit(self):
		
		locked = False
		
		if self.ID != False:
			
			action = "SELECT ChangeLog FROM lostandfoud WHERE ID = " + str(self.ID)
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
			
			dbmethods.WriteToLostAndFoundTable(self.localsettings.dbconnection, self)

class LostAndFoundPanel(wx.Panel):
	
	def GetLabel(self, field):
		
		return  self.localsettings.dictionary[field][self.localsettings.language]
	
	def __init__(self, notebook, localsettings):
		
		self.localsettings = localsettings
		self.notebook = notebook
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, self.GetLabel("lostandfoundmenu")[0])
		self.pageimage = "icons/lostandfound.png"
		
		wx.Panel.__init__(self, notebook)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		mainfiltersizer = wx.BoxSizer(wx.HORIZONTAL)
		
		idsizer = wx.BoxSizer(wx.VERTICAL)
		
		idlabel = wx.StaticText(self, -1, self.GetLabel("idlabel"))
		font = idlabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		idlabel.SetFont(font)
		idsizer.Add(idlabel, 0, wx.ALIGN_LEFT)
		
		identry = wx.TextCtrl(self, -1, "")
		#identry.Bind(wx.EVT_CHAR, self.KeyPressed)
		idsizer.Add(identry, 0, wx.EXPAND)
		
		idsizer.Add(wx.StaticText(self, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		mainfiltersizer.Add(idsizer, 1, wx.ALIGN_TOP)
		
		mainfiltersizer.Add(wx.StaticText(self, -1, "", size=(20,-1)), 0, wx.EXPAND)
		
		datefiltersizer = wx.BoxSizer(wx.VERTICAL)
		
		fromsizer = wx.BoxSizer(wx.VERTICAL)
		
		fromlabel = wx.StaticText(self, -1, " " + self.GetLabel("fromlabel") + " ", style=wx.EXPAND)
		fromlabel.SetFont(font)
		fromsizer.Add(fromlabel, 0, wx.ALIGN_LEFT)
		
		fromentry = customwidgets.DateCtrl(self, self.localsettings)
		
		for a in range(0, 6):
			
			fromentry.SubtractMonth()
		
		fromsizer.Add(fromentry, 0, wx.EXPAND)
		
		datefiltersizer.Add(fromsizer, 0, wx.EXPAND)
		
		tosizer = wx.BoxSizer(wx.VERTICAL)
		
		tolabel = wx.StaticText(self, -1, " " + self.GetLabel("tolabel") + " ", style=wx.EXPAND)
		tolabel.SetFont(font)
		tosizer.Add(tolabel, 0, wx.ALIGN_LEFT)
		
		toentry = customwidgets.DateCtrl(self, self.localsettings)
		tosizer.Add(toentry, 0, wx.EXPAND)
		
		datefiltersizer.Add(tosizer, 0, wx.EXPAND)
		
		includecompletecheckbox = wx.CheckBox(self, -1, self.GetLabel("includecompletelabel"))
		includecompletecheckbox.SetFont(font)
		datefiltersizer.Add(includecompletecheckbox, 0, wx.ALIGN_LEFT)
		
		mainfiltersizer.Add(datefiltersizer, 2, wx.ALIGN_TOP)
		
		mainfiltersizer.Add(wx.StaticText(self, -1, "", size=(20,-1)), 0, wx.EXPAND)
		
		areasizer = wx.BoxSizer(wx.VERTICAL)
		
		arealabel = wx.StaticText(self, -1, self.GetLabel("arealabel"))
		arealabel.SetFont(font)
		areasizer.Add(arealabel, 0, wx.ALIGN_LEFT)
		
		areaentry = wx.TextCtrl(self, -1, "")
		#areaentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		areasizer.Add(areaentry, 0, wx.EXPAND)
		
		areasizer.Add(wx.StaticText(self, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		buttonssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		reset = wx.Button(self, -1, self.GetLabel("resetlabel"))
		reset.SetBackgroundColour("red")
		reset.SetForegroundColour("white")
		reset.SetToolTipString(self.GetLabel("resetlabel"))
		reset.Bind(wx.EVT_BUTTON, self.Reset)
		buttonssizer.Add(reset, 1, wx.EXPAND)
		
		refreshbutton = wx.Button(self, -1, self.GetLabel("searchlabel"))
		refreshbutton.SetBackgroundColour("green")
		refreshbutton.SetForegroundColour("black")
		refreshbutton.SetToolTipString(self.GetLabel("searchlabel"))
		refreshbutton.Bind(wx.EVT_BUTTON, self.RefreshLists)
		buttonssizer.Add(refreshbutton, 1, wx.EXPAND)
		
		areasizer.Add(buttonssizer, 1, wx.EXPAND)
		
		mainfiltersizer.Add(areasizer, 3, wx.ALIGN_TOP)
		
		mainfiltersizer.Add(wx.StaticText(self, -1, "", size=(20,-1)), 0, wx.EXPAND)
		
		descriptionfiltersizer = wx.FlexGridSizer(cols=2)
		descriptionfiltersizer.AddGrowableCol(0)
		descriptionfiltersizer.AddGrowableCol(1)
		
		speciessizer = wx.BoxSizer(wx.VERTICAL)
		
		specieslabel = wx.StaticText(self, -1, self.GetLabel("animalspecieslabel"))
		specieslabel.SetFont(font)
		speciessizer.Add(specieslabel, 0, wx.ALIGN_LEFT)
		
		speciesentry = wx.TextCtrl(self, -1, "")
		#speciesentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		speciessizer.Add(speciesentry, 0, wx.EXPAND)
		
		descriptionfiltersizer.Add(speciessizer, 1, wx.EXPAND)
		
		coloursizer = wx.BoxSizer(wx.VERTICAL)
		
		colourlabel = wx.StaticText(self, -1, self.GetLabel("animalcolourlabel"))
		colourlabel.SetFont(font)
		coloursizer.Add(colourlabel, 0, wx.ALIGN_LEFT)
		
		colourentry = wx.TextCtrl(self, -1, "")
		#colourentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		coloursizer.Add(colourentry, 0, wx.EXPAND)
		
		descriptionfiltersizer.Add(coloursizer, 1, wx.EXPAND)
		
		sexsizer = wx.BoxSizer(wx.VERTICAL)
		
		sexlabel = wx.StaticText(self, -1, self.GetLabel("animalsexlabel"))
		sexlabel.SetFont(font)
		sexsizer.Add(sexlabel, 0, wx.ALIGN_LEFT)
		
		sexentry = wx.Choice(self, -1, choices=(self.GetLabel("unknownlabel"), self.GetLabel("malelabel"), self.GetLabel("femalelabel")))
		sexentry.SetSelection(0)
		#sexentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		sexsizer.Add(sexentry, 0, wx.EXPAND)
		
		descriptionfiltersizer.Add(sexsizer, 1, wx.EXPAND)
		
		neuteredsizer = wx.BoxSizer(wx.VERTICAL)
		
		neuteredlabel = wx.StaticText(self, -1, self.GetLabel("neuteredlabel"))
		neuteredlabel.SetFont(font)
		neuteredsizer.Add(neuteredlabel, 0, wx.ALIGN_LEFT)
		
		neuteredentry = wx.Choice(self, -1, choices=(self.GetLabel("unknownlabel"), self.GetLabel("yeslabel"), self.GetLabel("nolabel")))
		neuteredentry.SetSelection(0)
		#neuteredentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		neuteredsizer.Add(neuteredentry, 0, wx.EXPAND)
		
		descriptionfiltersizer.Add(neuteredsizer, 1, wx.EXPAND)
		
		agesizer = wx.BoxSizer(wx.VERTICAL)
		
		agelabel = wx.StaticText(self, -1, self.GetLabel("agelabel"))
		agelabel.SetFont(font)
		agesizer.Add(agelabel, 0, wx.ALIGN_LEFT)
		
		ageentry = wx.Choice(self, -1, choices=(self.GetLabel("unknownlabel"), self.GetLabel("juvenilelabel"), self.GetLabel("adultlabel"), self.GetLabel("elderlylabel")))
		#ageentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		agesizer.Add(ageentry, 0, wx.EXPAND)
		
		descriptionfiltersizer.Add(agesizer, 1, wx.EXPAND)
		
		mainfiltersizer.Add(descriptionfiltersizer, 6, wx.ALIGN_TOP)
		
		topsizer.Add(mainfiltersizer, 0, wx.EXPAND)
		
		#topsizer.Add(wx.StaticText(self, -1, "", size=(-1,20)), 0, wx.EXPAND)
		
		leftpanel = wx.Panel(self)
		
		leftsizer = wx.BoxSizer(wx.VERTICAL)
		
		lostlabel = wx.StaticText(leftpanel, -1, self.GetLabel("lostlabel"))
		font = lostlabel.GetFont()
		font.SetPointSize(font.GetPointSize() + 4)
		lostlabel.SetFont(font)
		lostlabel.SetForegroundColour("red")
		leftsizer.Add(lostlabel, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		lostlistbox = LostAndFoundListCtrl(leftpanel, 0)
		lostlistbox.listctrl.Bind(wx.EVT_RIGHT_DOWN, self.LostPopUp)
		lostlistbox.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.Edit)
		leftsizer.Add(lostlistbox, 1, wx.EXPAND)
		
		lostlistbox.totallabel = wx.StaticText(leftpanel, -1, self.GetLabel("totallabel") + ": 0")
		leftsizer.Add(lostlistbox.totallabel, 0, wx.ALIGN_LEFT)
		
		leftpanel.SetSizer(leftsizer)
		
		#horizontalsizer.Add(leftsizer, 1, wx.EXPAND)
		
		#horizontalsizer.Add(wx.StaticText(self, -1, "", size=(20,-1)), 0, wx.EXPAND)
		
		rightpanel = wx.Panel(self)
		
		rightsizer = wx.BoxSizer(wx.VERTICAL)
		
		foundlabel = wx.StaticText(rightpanel, -1, self.GetLabel("foundlabel"))
		font = foundlabel.GetFont()
		font.SetPointSize(font.GetPointSize() + 4)
		foundlabel.SetFont(font)
		foundlabel.SetForegroundColour("blue")
		rightsizer.Add(foundlabel, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		foundlistbox = LostAndFoundListCtrl(rightpanel, 1)
		foundlistbox.listctrl.Bind(wx.EVT_RIGHT_DOWN, self.FoundPopUp)
		foundlistbox.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.Edit)
		rightsizer.Add(foundlistbox, 1, wx.EXPAND)
		
		foundlistbox.totallabel = wx.StaticText(rightpanel, -1, self.GetLabel("totallabel") + ": 0")
		rightsizer.Add(foundlistbox.totallabel, 0, wx.ALIGN_LEFT)
		
		rightpanel.SetSizer(rightsizer)
		
		#horizontalsizer.Add(rightsizer, 1, wx.EXPAND)
		
		#if str(sys.platform)[:3] != "win":
                
                horizontalsizer = wx.SplitterWindow(self, -1)
                
                leftpanel.Reparent(horizontalsizer)
                rightpanel.Reparent(horizontalsizer)
                
                horizontalsizer.SplitVertically(leftpanel, rightpanel)
##			
##                else:
##			
##			horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
##			
##			horizontalsizer.Add(leftpanel, 1, wx.EXPAND)
##			horizontalsizer.Add(wx.StaticText(self, -1, "", size=(20,-1)), 0, wx.EXPAND)
##			horizontalsizer.Add(rightpanel, 1, wx.EXPAND)
		
		topsizer.Add(horizontalsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.fromentry = fromentry
		self.toentry = toentry
		
		self.identry = identry
		self.speciesentry = speciesentry
		self.colourentry = colourentry
		self.areaentry = areaentry
		self.sexentry = sexentry
		self.neuteredentry = neuteredentry
		self.ageentry = ageentry
		self.includecompletecheckbox = includecompletecheckbox
		
		self.lostlistbox = lostlistbox
		customwidgets.ListCtrlWrapper.RefreshList(self.lostlistbox)
		self.foundlistbox = foundlistbox
		customwidgets.ListCtrlWrapper.RefreshList(self.foundlistbox)
	
	def Reset(self, ID):
		
		today = miscmethods.GetWXDateFromDate(datetime.date.today())
		
		self.fromentry.SetValue(today)
		self.toentry.SetValue(today)
		
		for a in range(0, 6):
			
			self.fromentry.SubtractMonth()
		
		self.identry.Clear()
		self.speciesentry.Clear()
		self.colourentry.Clear()
		self.areaentry.Clear()
		self.sexentry.SetSelection(0)
		self.neuteredentry.SetSelection(0)
		self.ageentry.SetSelection(0)
		self.includecompletecheckbox.SetValue(False)
	
	def RefreshLists(self, ID=False):
		
		self.lostlistbox.RefreshList()
		self.foundlistbox.RefreshList()
	
	def Edit(self, ID):
		
		listctrl = ID.GetEventObject()
		
		listboxid = listctrl.GetFocusedItem()
		lostandfoundid = listctrl.GetItemData(listboxid)
		
		lostanimaldata = LostAndFoundSettings(self.localsettings, lostandfoundid)
		
		lostanimalpanel = EditLostAndFoundPanel(self.notebook, lostanimaldata)
		self.notebook.AddPage(lostanimalpanel)
	
	def LostPopUp(self, ID):
		
		listctrl = ID.GetEventObject()
		
		listboxid = listctrl.GetFocusedItem()
                
                popupmenu = wx.Menu()
                
                addlost = wx.MenuItem(popupmenu, NEW_LOST, self.GetLabel("addlabel"))
                addlost.SetBitmap(wx.Bitmap("icons/new.png"))
                popupmenu.AppendItem(addlost)
                
                wx.EVT_MENU(popupmenu, NEW_LOST, self.NewLost)

                if listboxid > -1:
                        
                        lostandfoundid = listctrl.GetItemData(listboxid)
                        
                        popupmenu.lostandfoundid = lostandfoundid
                        
                        editlost = wx.MenuItem(popupmenu, EDIT_LOST, self.GetLabel("editlabel"))
                        editlost.SetBitmap(wx.Bitmap("icons/edit.png"))
                        popupmenu.AppendItem(editlost)
                        wx.EVT_MENU(popupmenu, EDIT_LOST, self.EditLost)
                        
                        deletelost = wx.MenuItem(popupmenu, DELETE_LOST, self.GetLabel("deletelabel"))
                        deletelost.SetBitmap(wx.Bitmap("icons/delete.png"))
                        popupmenu.AppendItem(deletelost)
                        wx.EVT_MENU(popupmenu, DELETE_LOST, self.DeleteLost)
                        
                self.PopupMenu(popupmenu)
	
	def NewLost(self, ID):
		
		lostanimaldata = LostAndFoundSettings(self.localsettings)
		lostanimaldata.lostorfound = 0
		
		newlostanimalpanel = EditLostAndFoundPanel(self.notebook, lostanimaldata)
		self.notebook.AddPage(newlostanimalpanel)
	
	def EditLost(self, ID):
		
		menuitem = ID.GetEventObject()
		
		lostandfoundid = menuitem.lostandfoundid
		
		lostanimaldata = LostAndFoundSettings(self.localsettings, lostandfoundid)
		
		lostanimalpanel = EditLostAndFoundPanel(self.notebook, lostanimaldata)
		self.notebook.AddPage(lostanimalpanel)
	
	def DeleteLost(self, ID):
		
		if miscmethods.ConfirmMessage(self.GetLabel("medicationconfirmdeletemessage")):
			
			menuitem = ID.GetEventObject()
			
			lostandfoundid = menuitem.lostandfoundid
			
			action = "DELETE FROM lostandfound WHERE ID = " + str(lostandfoundid)
			db.SendSQL(action, self.localsettings.dbconnection)
			
			self.RefreshLists()
	
	def FoundPopUp(self, ID):
		
		listctrl = ID.GetEventObject()
		
		listboxid = listctrl.GetFocusedItem()
		
		popupmenu = wx.Menu()
		
		addfound = wx.MenuItem(popupmenu, NEW_LOST, self.GetLabel("addlabel"))
		addfound.SetBitmap(wx.Bitmap("icons/new.png"))
		popupmenu.AppendItem(addfound)
		wx.EVT_MENU(popupmenu, NEW_LOST, self.NewFound)
		
		if listboxid > -1:
                        
                        lostandfoundid = listctrl.GetItemData(listboxid)
                        
                        popupmenu.lostandfoundid = lostandfoundid
			
			editfound = wx.MenuItem(popupmenu, EDIT_LOST, self.GetLabel("editlabel"))
			editfound.SetBitmap(wx.Bitmap("icons/edit.png"))
			popupmenu.AppendItem(editfound)
			wx.EVT_MENU(popupmenu, EDIT_LOST, self.EditFound)
			
			deletefound = wx.MenuItem(popupmenu, DELETE_LOST, self.GetLabel("deletelabel"))
			deletefound.SetBitmap(wx.Bitmap("icons/delete.png"))
			popupmenu.AppendItem(deletefound)
			wx.EVT_MENU(popupmenu, DELETE_LOST, self.DeleteFound)
		
		self.PopupMenu(popupmenu)
	
	def NewFound(self, ID):
		
		foundanimaldata = LostAndFoundSettings(self.localsettings)
		foundanimaldata.lostorfound = 1
		
		newfoundanimalpanel = EditLostAndFoundPanel(self.notebook, foundanimaldata)
		self.notebook.AddPage(newfoundanimalpanel)
	
	def EditFound(self, ID):
		
		menuitem = ID.GetEventObject()
		
		lostandfoundid = menuitem.lostandfoundid
		
		foundanimaldata = LostAndFoundSettings(self.localsettings, lostandfoundid)
		
		foundanimalpanel = EditLostAndFoundPanel(self.notebook, foundanimaldata)
		self.notebook.AddPage(foundanimalpanel)
	
	def DeleteFound(self, ID):
		
		if miscmethods.ConfirmMessage(self.GetLabel("medicationconfirmdeletemessage")):
			
			menuitem = ID.GetEventObject()
			
			lostandfoundid = menuitem.lostandfoundid
			
			action = "DELETE FROM lostandfound WHERE ID = " + str(lostandfoundid)
			db.SendSQL(action, self.localsettings.dbconnection)
			
			self.RefreshLists()

class EditLostAndFoundPanel(wx.Panel):
	
	def GetLabel(self, field):
		
		return  self.localsettings.dictionary[field][self.localsettings.language]
	
	def __init__(self, notebook, lostorfounddata):
		
		self.lostorfounddata = lostorfounddata
		self.localsettings = lostorfounddata.localsettings
		self.notebook = notebook
		
		if self.lostorfounddata.lostorfound == 0:
			
			pagetitle = self.GetLabel("lostanimallabel")
			datelabel = self.GetLabel("datelostlabel")
			
		else:
			
			pagetitle = self.GetLabel("foundanimallabel")
			datelabel = self.GetLabel("datefoundlabel")
		
		if lostorfounddata.ID != False:
			
			pagetitle = pagetitle + " " + str(lostorfounddata.ID)
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, pagetitle)
		self.pageimage = "icons/lostandfound.png"
		
		wx.Panel.__init__(self, notebook)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		topsizer.Add(wx.StaticText(self, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		#ID, LostOrFound, ContactID, Species, Date, Sex, Neutered, FurLength, Colour1, Colour2, Colour3, Collar, CollarDescription, Size, Age, IsChipped, ChipNo, Temperament, Comment, DateComplete, ChangeLog)
		
		contactsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		savebitmap = wx.Bitmap("icons/save.png")
		savebutton = wx.BitmapButton(self, -1, savebitmap)
		savebutton.SetToolTipString(self.GetLabel("savetooltip"))
		savebutton.Bind(wx.EVT_BUTTON, self.Save)
		contactsizer.Add(savebutton, 0, wx.ALIGN_TOP)
		
		self.savebutton = savebutton
		
		matchbitmap = wx.Bitmap("icons/search.png")
		matchbutton = wx.BitmapButton(self, -1, matchbitmap)
		matchbutton.SetToolTipString(self.GetLabel("lostandfoundsearchtooltip"))
		matchbutton.Bind(wx.EVT_BUTTON, self.Match)
		contactsizer.Add(matchbutton, 0, wx.ALIGN_TOP)
		
		self.matchbutton = matchbutton
		
		if self.lostorfounddata.ID == False:
			
			idnumber = ""
			self.matchbutton.Disable()
			
		else:
			
			idnumber = miscmethods.NoWrap(" " + self.GetLabel("idlabel") + ": " + str(self.lostorfounddata.ID))
		
		contactsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		idlabel = wx.StaticText(self, -1, idnumber)
		idlabel.SetForegroundColour("red")
		font = idlabel.GetFont()
		font.SetPointSize(font.GetPointSize() + 4)
		idlabel.SetFont(font)
		contactsizer.Add(idlabel, 0, wx.ALIGN_CENTER)
		
		contactsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		datesizer = wx.BoxSizer(wx.VERTICAL)
		
		datelabel = wx.StaticText(self, -1, datelabel)
		font = datelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		datelabel.SetFont(font)
		datesizer.Add(datelabel, 0, wx.ALIGN_LEFT)
		
		dateentry = customwidgets.DateCtrl(self, self.localsettings)
		dateentry.Bind(wx.EVT_CHAR, self.EnableSave)
		#dateentry.Bind(wx.EVT_TEXT, self.EnableSave)
		datesizer.Add(dateentry, 0, wx.EXPAND)
		
		try:
			
			date = miscmethods.GetWXDateFromSQLDate(self.lostorfounddata.date)
			dateentry.SetValue(date)
			
		except:
			
			dateentry.GetToday()
		
		contactsizer.Add(datesizer, 0, wx.EXPAND)
		
		contactsizer.Add(wx.StaticText(self, -1, "", size=(20,-1)), 0, wx.EXPAND)
		
		clientsizer = wx.BoxSizer(wx.VERTICAL)
		
		clientlabel = wx.StaticText(self, -1, self.GetLabel("contacttooltip"))
		clientlabel.SetFont(font)
		clientsizer.Add(clientlabel, 0, wx.ALIGN_LEFT)
		
		cliententrysizer = wx.BoxSizer(wx.HORIZONTAL)
		
		cliententry = wx.StaticText(self, -1, self.GetLabel("nonelabel"))
		
		cliententry.SetForegroundColour("blue")
		font = cliententry.GetFont()
		font.SetPointSize(font.GetPointSize() + 2)
		cliententry.SetFont(font)
		cliententry.SetToolTipString(self.GetLabel("rightclickformenutooltip"))
		cliententry.Bind(wx.EVT_RIGHT_DOWN, self.ClientPopup)
		
		cliententrysizer.Add(cliententry, 0, wx.ALIGN_CENTER)
		
		clientsizer.Add(cliententrysizer, 0, wx.EXPAND)
		
		contactsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		contactsizer.Add(clientsizer, 0, wx.EXPAND)
		
		contactsizer.Add(wx.StaticText(self, -1, "", size=(20,-1)), 0, wx.EXPAND)
		
		if self.lostorfounddata.animalid > 0:
			
			action = "SELECT Name FROM animal WHERE ID = " + str(self.lostorfounddata.animalid)
			results = db.SendSQL(action, self.localsettings.dbconnection)
			
			if len(results) == 1:
				
				animalsizer = wx.BoxSizer(wx.VERTICAL)
				
				animallabel = wx.StaticText(self, -1, self.GetLabel("animallabel"))
				font = animallabel.GetFont()
				font.SetPointSize(font.GetPointSize() - 2)
				animallabel.SetFont(font)
				animalsizer.Add(animallabel, 0, wx.ALIGN_LEFT)
				
				animalentry = wx.StaticText(self, -1, results[0][0])
				
				animalentry.SetForegroundColour("blue")
				font = animalentry.GetFont()
				font.SetPointSize(font.GetPointSize() + 2)
				animalentry.SetFont(font)
				animalentry.SetToolTipString(self.GetLabel("rightclickformenutooltip"))
				animalentry.Bind(wx.EVT_RIGHT_DOWN, self.AnimalPopup)
				
				animalsizer.Add(animalentry, 0, wx.ALIGN_LEFT)
				
				contactsizer.Add(animalsizer, 0, wx.EXPAND)
		
		contactsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		topsizer.Add(contactsizer, 0, wx.EXPAND)
		
		topsizer.Add(wx.StaticText(self, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		animaldescriptionsizer = wx.BoxSizer(wx.VERTICAL)
		
		speciessizer = wx.BoxSizer(wx.VERTICAL)
		
		specieslabel = wx.StaticText(self, -1, self.GetLabel("animalspecieslabel"))
		font = specieslabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		specieslabel.SetFont(font)
		speciessizer.Add(specieslabel, 0, wx.ALIGN_LEFT)
		
		action = "SELECT SpeciesName FROM species ORDER BY SpeciesName"
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		specieslist = []
		
		for a in results:
			
			specieslist.append(a[0])
		
		speciesentry = wx.ComboBox(self, -1, self.lostorfounddata.species, choices=specieslist)
		speciesentry.Bind(wx.EVT_TEXT, self.EnableSave)
		#speciesentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		speciessizer.Add(speciesentry, 0, wx.EXPAND)
		
		animaldescriptionsizer.Add(speciessizer, 0, wx.EXPAND)
		
		sexandneuteredsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		sexsizer = wx.BoxSizer(wx.VERTICAL)
		
		sexlabel = wx.StaticText(self, -1, self.GetLabel("animalsexlabel"))
		sexlabel.SetFont(font)
		sexsizer.Add(sexlabel, 0, wx.ALIGN_LEFT)
		
		sexentry = wx.Choice(self, -1, choices=(self.GetLabel("unknownlabel"), self.GetLabel("malelabel"), self.GetLabel("femalelabel")))
		sexentry.SetSelection(self.lostorfounddata.sex)
		sexentry.Bind(wx.EVT_CHOICE, self.EnableSave)
		#sexentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		sexsizer.Add(sexentry, 0, wx.EXPAND)
		
		sexandneuteredsizer.Add(sexsizer, 1, wx.EXPAND)
		
		sexandneuteredsizer.Add(wx.StaticText(self, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		neuteredsizer = wx.BoxSizer(wx.VERTICAL)
		
		neuteredlabel = wx.StaticText(self, -1, self.GetLabel("neuteredlabel"))
		neuteredlabel.SetFont(font)
		neuteredsizer.Add(neuteredlabel, 0, wx.ALIGN_LEFT)
		
		neuteredentry = wx.Choice(self, -1, choices=(self.GetLabel("unknownlabel"), self.GetLabel("yeslabel"), self.GetLabel("nolabel")))
		neuteredentry.SetSelection(self.lostorfounddata.neutered)
		neuteredentry.Bind(wx.EVT_CHOICE, self.EnableSave)
		#neuteredentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		neuteredsizer.Add(neuteredentry, 0, wx.EXPAND)
		
		sexandneuteredsizer.Add(neuteredsizer, 1, wx.EXPAND)
		
		animaldescriptionsizer.Add(sexandneuteredsizer, 0, wx.EXPAND)
		
		agesizer = wx.BoxSizer(wx.VERTICAL)
		
		agelabel = wx.StaticText(self, -1, self.GetLabel("agelabel"))
		agelabel.SetFont(font)
		agesizer.Add(agelabel, 0, wx.ALIGN_LEFT)
		
		ageentry = wx.Choice(self, -1, choices=(self.GetLabel("unknownlabel"), self.GetLabel("juvenilelabel"), self.GetLabel("adultlabel"), self.GetLabel("elderlylabel")))
		ageentry.SetSelection(self.lostorfounddata.age)
		ageentry.Bind(wx.EVT_CHOICE, self.EnableSave)
		#ageentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		agesizer.Add(ageentry, 0, wx.EXPAND)
		
		animaldescriptionsizer.Add(agesizer, 0, wx.EXPAND)
		
		colour1sizer = wx.BoxSizer(wx.VERTICAL)
		
		colour1label = wx.StaticText(self, -1, self.GetLabel("animalcolourlabel") + " 1")
		colour1label.SetFont(font)
		colour1sizer.Add(colour1label, 0, wx.ALIGN_LEFT)
		
		colour1entry = wx.TextCtrl(self, -1, self.lostorfounddata.colour1)
		colour1entry.Bind(wx.EVT_TEXT, self.EnableSave)
		#colour1entry.Bind(wx.EVT_CHAR, self.KeyPressed)
		colour1sizer.Add(colour1entry, 0, wx.EXPAND)
		
		animaldescriptionsizer.Add(colour1sizer, 0, wx.EXPAND)
		
		colour2sizer = wx.BoxSizer(wx.VERTICAL)
		
		colour2label = wx.StaticText(self, -1, self.GetLabel("animalcolourlabel") + " 2")
		colour2label.SetFont(font)
		colour2sizer.Add(colour2label, 0, wx.ALIGN_LEFT)
		
		colour2entry = wx.TextCtrl(self, -1, self.lostorfounddata.colour2)
		colour2entry.Bind(wx.EVT_TEXT, self.EnableSave)
		#colour2entry.Bind(wx.EVT_CHAR, self.KeyPressed)
		colour2sizer.Add(colour2entry, 0, wx.EXPAND)
		
		animaldescriptionsizer.Add(colour2sizer, 0, wx.EXPAND)
		
		colour3sizer = wx.BoxSizer(wx.VERTICAL)
		
		colour3label = wx.StaticText(self, -1, self.GetLabel("animalcolourlabel") + " 3")
		colour3label.SetFont(font)
		colour3sizer.Add(colour3label, 0, wx.ALIGN_LEFT)
		
		colour3entry = wx.TextCtrl(self, -1, self.lostorfounddata.colour3)
		colour3entry.Bind(wx.EVT_TEXT, self.EnableSave)
		#colour3entry.Bind(wx.EVT_CHAR, self.KeyPressed)
		colour3sizer.Add(colour3entry, 0, wx.EXPAND)
		
		animaldescriptionsizer.Add(colour3sizer, 0, wx.EXPAND)
		
		furlengthsizer = wx.BoxSizer(wx.VERTICAL)
		
		furlengthlabel = wx.StaticText(self, -1, self.GetLabel("furlengthlabel"))
		furlengthlabel.SetFont(font)
		furlengthsizer.Add(furlengthlabel, 0, wx.ALIGN_LEFT)
		
		furlengthentry = wx.Choice(self, -1, choices=(self.GetLabel("unknownlabel"), self.GetLabel("shortlabel"), self.GetLabel("fluffylabel"), self.GetLabel("longlabel"), self.GetLabel("hairlesslabel")))
		furlengthentry.SetSelection(self.lostorfounddata.furlength)
		furlengthentry.Bind(wx.EVT_CHOICE, self.EnableSave)
		#furlengthentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		furlengthsizer.Add(furlengthentry, 0, wx.EXPAND)
		
		animaldescriptionsizer.Add(furlengthsizer, 0, wx.EXPAND)
		
		bodysizesizer = wx.BoxSizer(wx.VERTICAL)
		
		bodysizelabel = wx.StaticText(self, -1, self.GetLabel("sizelabel"))
		bodysizelabel.SetFont(font)
		bodysizesizer.Add(bodysizelabel, 0, wx.ALIGN_LEFT)
		
		bodysizeentry = wx.Choice(self, -1, choices=(self.GetLabel("unknownlabel"), self.GetLabel("smalllabel"), self.GetLabel("mediumlabel"), self.GetLabel("largelabel")))
		bodysizeentry.SetSelection(self.lostorfounddata.size)
		bodysizeentry.Bind(wx.EVT_CHOICE, self.EnableSave)
		#bodysizeentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		bodysizesizer.Add(bodysizeentry, 0, wx.EXPAND)
		
		animaldescriptionsizer.Add(bodysizesizer, 0, wx.EXPAND)
		
		horizontalsizer.Add(animaldescriptionsizer, 1, wx.EXPAND)
		
		horizontalsizer.Add(wx.StaticText(self, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		secondarydescriptionsizer = wx.BoxSizer(wx.VERTICAL)
		
		chippedsizer = wx.BoxSizer(wx.VERTICAL)
		
		chippedlabel = wx.StaticText(self, -1, self.GetLabel("microchiplabel"))
		chippedlabel.SetFont(font)
		chippedsizer.Add(chippedlabel, 0, wx.ALIGN_LEFT)
		
		chippedentry = wx.Choice(self, -1, choices=(self.GetLabel("unknownlabel"), self.GetLabel("yeslabel"), self.GetLabel("nolabel")))
		chippedentry.SetSelection(self.lostorfounddata.ischipped)
		chippedentry.Bind(wx.EVT_CHOICE, self.EnableSave)
		#chippedentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		chippedsizer.Add(chippedentry, 0, wx.EXPAND)
		
		secondarydescriptionsizer.Add(chippedsizer, 0, wx.EXPAND)
		
		temperamentsizer = wx.BoxSizer(wx.VERTICAL)
		
		temperamentlabel = wx.StaticText(self, -1, self.GetLabel("temperamentlabel"))
		temperamentlabel.SetFont(font)
		temperamentsizer.Add(temperamentlabel, 0, wx.ALIGN_LEFT)
		
		temperamententry = wx.Choice(self, -1, choices=(self.GetLabel("unknownlabel"), self.GetLabel("friendlylabel"), self.GetLabel("timidlabel"), self.GetLabel("aggressivelabel")))
		temperamententry.SetSelection(self.lostorfounddata.temperament)
		temperamententry.Bind(wx.EVT_CHOICE, self.EnableSave)
		#temperamententry.Bind(wx.EVT_CHAR, self.KeyPressed)
		temperamentsizer.Add(temperamententry, 0, wx.EXPAND)
		
		secondarydescriptionsizer.Add(temperamentsizer, 0, wx.EXPAND)
		
		collarsizer = wx.BoxSizer(wx.VERTICAL)
		
		collarlabel = wx.StaticText(self, -1, self.GetLabel("collarlabel"))
		collarlabel.SetFont(font)
		collarsizer.Add(collarlabel, 0, wx.ALIGN_LEFT)
		
		collardescriptionsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		collarchoice = wx.Choice(self, -1, choices=(self.GetLabel("unknownlabel"), self.GetLabel("yeslabel"), self.GetLabel("nolabel")))
		collarchoice.SetSelection(self.lostorfounddata.collar)
		collarchoice.Bind(wx.EVT_CHOICE, self.EnableSave)
		#collarentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		collardescriptionsizer.Add(collarchoice, 0, wx.EXPAND)
		
		collarentry = wx.TextCtrl(self, -1, self.lostorfounddata.collardescription)
		collarentry.Bind(wx.EVT_TEXT, self.EnableSave)
		collarentry.SetToolTipString(self.GetLabel("collardescriptiontooltip"))
		#collarentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		collardescriptionsizer.Add(collarentry, 1, wx.EXPAND)
		
		collarsizer.Add(collardescriptionsizer, 0, wx.EXPAND)
		
		secondarydescriptionsizer.Add(collarsizer, 0, wx.EXPAND)
		
		areasizer = wx.BoxSizer(wx.VERTICAL)
		
		arealabel = wx.StaticText(self, -1, self.GetLabel("arealabel"))
		arealabel.SetFont(font)
		areasizer.Add(arealabel, 0, wx.ALIGN_LEFT)
		
		areaentry = wx.TextCtrl(self, -1, self.lostorfounddata.area)
		areaentry.Bind(wx.EVT_TEXT, self.EnableSave)
		areaentry.SetToolTipString(self.GetLabel("areatooltip"))
		#areaentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		areasizer.Add(areaentry, 0, wx.EXPAND)
		
		secondarydescriptionsizer.Add(areasizer, 0, wx.EXPAND)
		
		horizontalsizer.Add(secondarydescriptionsizer, 1, wx.EXPAND)
		
		horizontalsizer.Add(wx.StaticText(self, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		tertiarydescriptionsizer = wx.BoxSizer(wx.VERTICAL)
		
		datecompletedsizer = wx.BoxSizer(wx.VERTICAL)
		
		datecompletedlabel = wx.StaticText(self, -1, self.GetLabel("datecompletelabel"))
		datecompletedlabel.SetFont(font)
		datecompletedsizer.Add(datecompletedlabel, 0, wx.ALIGN_LEFT)
		
		datecompletedentry = customwidgets.DateCtrl(self, self.localsettings)
		
		try:
			
			datecomplete = miscmethods.GetWXDateFromSQLDate(self.lostorfounddata.datecomplete)
			datecompletedentry.SetValue(datecomplete)
			
		except:
			
			datecompletedentry.Clear()
		
		
		datecompletedentry.Bind(wx.EVT_TEXT, self.EnableSave)
		#datecompletedentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		datecompletedsizer.Add(datecompletedentry, 0, wx.EXPAND)
		
		tertiarydescriptionsizer.Add(datecompletedsizer, 0, wx.EXPAND)
		
		commentssizer = wx.BoxSizer(wx.VERTICAL)
		
		commentslabel = wx.StaticText(self, -1, self.GetLabel("clientcommentslabel"))
		commentslabel.SetFont(font)
		commentssizer.Add(commentslabel, 0, wx.ALIGN_LEFT)
		
		commentsentry = wx.TextCtrl(self, -1, self.lostorfounddata.comments, style=wx.TE_MULTILINE)
		commentsentry.Bind(wx.EVT_TEXT, self.EnableSave)
		#commentsentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		commentssizer.Add(commentsentry, 1, wx.EXPAND)
		
		tertiarydescriptionsizer.Add(commentssizer, 1, wx.EXPAND)
		
		horizontalsizer.Add(tertiarydescriptionsizer, 1, wx.EXPAND)
		
		topsizer.Add(horizontalsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.dateentry = dateentry
		self.cliententry = cliententry
		self.speciesentry = speciesentry
		self.sexentry = sexentry
		self.neuteredentry = neuteredentry
		self.ageentry = ageentry
		self.colour1entry = colour1entry
		self.colour2entry = colour2entry
		self.colour3entry = colour3entry
		self.furlengthentry = furlengthentry
		self.bodysizeentry = bodysizeentry
		#self.breedentry = breedentry
		self.chippedentry = chippedentry
		self.temperamententry = temperamententry
		self.collarchoice = collarchoice
		self.collarentry = collarentry
		self.areaentry = areaentry
		self.datecompletedentry = datecompletedentry
		self.commentsentry = commentsentry
		
		#self.contactclientbutton = contactclientbutton
		#self.editclientbutton = editclientbutton
		
		self.contactsizer = contactsizer
		
		self.idlabel = idlabel
		
		if self.lostorfounddata.contactid > 0:
			
			self.UpdateContactInfo(self.lostorfounddata.contactid)
		
		self.savebutton.Disable()
	
	def EnableSave(self, ID=False):
		
		if self.lostorfounddata.contactid > 0:
			
			self.savebutton.Enable()
		
		if ID != False:
			
			ID.Skip()
	
	def Match(self, ID):
		
		dialog = wx.Dialog(self, -1, self.GetLabel("datelabel"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		if self.lostorfounddata.lostorfound == 0:
			
			instructions = self.GetLabel("searchuptolabel")
			
		else:
			
			instructions = self.GetLabel("searchfromlabel")
		
		instructionslabel = wx.StaticText(panel, -1, instructions)
		topsizer.Add(instructionslabel, 1, wx.EXPAND)
		
		datesizer = wx.BoxSizer(wx.HORIZONTAL)
		
		dateentry = customwidgets.DateCtrl(panel, self.localsettings)
		dateentry.Clear()
		datesizer.Add(dateentry, 0, wx.EXPAND)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		submitbutton = wx.BitmapButton(panel, -1, submitbitmap)
		submitbutton.Bind(wx.EVT_BUTTON, self.MatchLostAndFound)
		submitbutton.SetToolTipString(self.GetLabel("submitlabel"))
		datesizer.Add(submitbutton, 0, wx.EXPAND)
		
		topsizer.Add(datesizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		panel.SetSizer(topsizer)
		
		panel.dateentry = dateentry
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		dialog.Fit()
		
		dialog.ShowModal()
	
	def MatchLostAndFound(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		date = panel.dateentry.GetValue()
		
		if str(date) != "":
			
			date = miscmethods.GetSQLDateFromWXDate(date)
		
		lostorfound = self.lostorfounddata.lostorfound
		
		if lostorfound == 0:
			
			lostorfoundinverse = 1
			
		else:
			
			lostorfoundinverse = 0
		
		action = "SELECT lostandfound.*, client.ClientTitle, client.ClientForenames, client.ClientSurname FROM lostandfound INNER JOIN client ON lostandfound.ContactID = client.ID WHERE lostandfound.DateComplete = \"0000-00-00\" AND lostandfound.LostOrFound = " + str(lostorfoundinverse)
		
		if lostorfound == 0 and date == "":
			
			action = action + " AND lostandfound.Date >= \"" + str(self.lostorfounddata.date) + "\""
			
		elif lostorfound == 0:
			
			action = action + " AND lostandfound.Date BETWEEN \"" + str(self.lostorfounddata.date) + "\" AND \"" + str(date) + "\""
			
		elif lostorfound == 1 and date == "":
			
			action = action + " AND lostandfound.Date <= \"" + str(self.lostorfounddata.date) + "\""
			
		elif lostorfound == 1:
			
			action = action + " AND lostandfound.Date BETWEEN \"" + str(date) + "\" AND \"" + str(self.lostorfounddata.date) + "\""
		
		#print "\naction = " + str(action)
		#print action
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		possiblematches = []
		
		for a in results:
			
			score = 0
			
			foundID = a[0]
			#foundlostorfound = a[1]
			#foundcontactid = a[2]
			foundspecies = unicode(a[3], "utf8")
			founddate = a[4]
			foundsex = a[5]
			foundneutered = a[6]
			foundfurlength = a[7]
			foundcolour1 = unicode(a[8], "utf8")
			foundcolour2 = unicode(a[9], "utf8")
			foundcolour3 = unicode(a[10], "utf8")
			foundcollar = a[11]
			foundcollardescription = unicode(a[12], "utf8")
			foundsize = a[13]
			foundage = a[14]
			foundischipped = a[15]
			foundchipno = unicode(a[16], "utf8")
			foundtemperament = a[17]
			foundcomments = unicode(a[18], "utf8")
			founddatecomplete = a[19]
			foundchangelog = a[20]
			foundarea = unicode(a[21], "utf8")
			
			datepivot = miscmethods.GetDateFromSQLDate(founddate) - miscmethods.GetDateFromSQLDate(self.lostorfounddata.date)
			
			datepivot = datepivot.days
			
			if datepivot < 0:
				
				datepivot = datepivot * -1
			
			datescore = 10
			
			while datepivot > 7 and datescore > 0:
				
				datepivot = datepivot - 7
				datescore = datescore - 1
				
			score = score + datescore
			
			pass1 = True
			
			if foundspecies != self.lostorfounddata.species:
				
				pass1 = False
			
			if foundsex == self.lostorfounddata.sex:
				
				score = score + 1
				
			elif foundsex == 0 or self.lostorfounddata.sex == 0:
				
				pass
				
			else:
				
				pass1 = False
			
			if foundneutered == self.lostorfounddata.neutered:
				
				score = score + 1
				
			elif foundneutered == 0 or self.lostorfounddata.neutered == 0:
				
				pass
				
			else:
				
				pass1 = False
			
			if foundfurlength == self.lostorfounddata.furlength:
				
				score = score + 1
				
			#elif foundfurlength == 0 or self.lostorfounddata.furlength == 0:
				
				#pass
				
			#else:
				
				#pass1 = False
			
			if foundsize == self.lostorfounddata.size:
				
				score = score + 1
				
			#elif foundsize == 0 or self.lostorfounddata.size == 0:
				
				#pass
				
			#else:
				
				#pass1 = False
			
			if foundage == self.lostorfounddata.age:
				
				score = score + 2
				
			#elif foundage == 0 or self.lostorfounddata.age == 0:
				
				#pass
				
			#else:
				
				#pass1 = False
			
			if foundischipped == self.lostorfounddata.ischipped:
				
				score = score + 1
				
			elif foundischipped == 0 or self.lostorfounddata.ischipped == 0:
				
				pass
				
			else:
				
				pass1 = False
			
			
			if lostorfound == 0:
				
				if foundcollar == self.lostorfounddata.collar:
					
					score = score + 1
					
				elif foundcollar == 0 or self.lostorfounddata.collar == 0 or foundcollar == 2:
					
					pass
					
				else:
					
					pass1 = False
				
			else:
				
				if foundcollar == self.lostorfounddata.collar:
					
					score = score + 1
					
				elif foundcollar == 0 or self.lostorfounddata.collar == 0 or foundcollar == 1:
					
					pass
					
				else:
					
					pass1 = False
			
			if pass1 == True:
				
				colourmatch = 0
				
				for b in (foundcolour1, foundcolour2, foundcolour3):
					
					if ( b.lower() == self.lostorfounddata.colour1.lower() or b.lower() == self.lostorfounddata.colour2.lower() or b.lower() == self.lostorfounddata.colour3.lower() ) and b != "":
						
						colourmatch = colourmatch + 1
				
				areamatch = 0
				
				for b in foundarea.split(" "):
					
					for c in self.lostorfounddata.area.split(" "):
						
						if c.lower() == b.lower():
							
							areamatch = areamatch + 1
				
				if colourmatch > 0 and areamatch > 0:
					
					possiblematches.append((score + ( colourmatch * 2) + ( areamatch * 3 ), a))
		
		possiblematches.sort(reverse=True)
		
		panel.GetParent().Close()
		
		self.MatchResultsDialog(possiblematches)
	
	def MatchResultsDialog(self, possiblematches):
		
		title = self.GetLabel("lostandfoundsearchresultspagetitle") + " #" + str(self.lostorfounddata.ID)
		
		panel = wx.Panel(self.notebook)
		panel.pagetitle = title
		panel.pageimage = "icons/lostandfound.png"
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		listbox = LostAndFoundMatchListCtrl(panel, possiblematches, self.localsettings)
		listbox.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.EditMatch)
		listbox.Bind(wx.EVT_RIGHT_DOWN, self.MatchPopUp)
		topsizer.Add(listbox, 1, wx.EXPAND)
		
		panel.SetSizer(topsizer)
		
		self.notebook.AddPage(panel)
		
		listbox.RefreshList()
	
	def MatchPopUp(self, ID):
		
		listctrl = ID.GetEventObject()
		
		listboxid = listctrl.GetFocusedItem()
		lostandfoundid = listctrl.GetItemData(listboxid)
		
		popupmenu = wx.Menu()
		popupmenu.listctrl = listctrl
		
		popupmenu.lostandfoundid = lostandfoundid
		
		if listctrl.GetSelectedItemCount() > 0:
			
			editlost = wx.MenuItem(popupmenu, EDIT_LOST, self.GetLabel("editlabel"))
			editlost.SetBitmap(wx.Bitmap("icons/edit.png"))
			popupmenu.AppendItem(editlost)
			wx.EVT_MENU(popupmenu, EDIT_LOST, self.EditMatchFromMenu)
		
		self.PopupMenu(popupmenu)
	
	def EditMatchFromMenu(self, ID):
		
		listctrl = ID.GetEventObject().listctrl
		
		listboxid = listctrl.GetFocusedItem()
		lostandfoundid = listctrl.GetItemData(listboxid)
		
		lostandfounddata = LostAndFoundSettings(self.localsettings, lostandfoundid)
		
		panel = EditLostAndFoundPanel(self.notebook, lostandfounddata)
		self.notebook.AddPage(panel)
	
	def EditMatch(self, ID):
		
		listctrl = ID.GetEventObject()
		
		listboxid = listctrl.GetFocusedItem()
		lostandfoundid = listctrl.GetItemData(listboxid)
		
		lostandfounddata = LostAndFoundSettings(self.localsettings, lostandfoundid)
		
		panel = EditLostAndFoundPanel(self.notebook, lostandfounddata)
		self.notebook.AddPage(panel)
	
	def ClientPopup(self, ID):
		
		#print "Client Popup"
		
		popupmenu = wx.Menu()
		
		addclient = wx.MenuItem(popupmenu, ADD_CLIENT, self.GetLabel("addlabel"))
		addclient.SetBitmap(wx.Bitmap("icons/new.png"))
		popupmenu.AppendItem(addclient)
		wx.EVT_MENU(popupmenu, ADD_CLIENT, self.AddClient)
		
		findclient = wx.MenuItem(popupmenu, FIND_CLIENT, self.GetLabel("searchlabel"))
		findclient.SetBitmap(wx.Bitmap("icons/search.png"))
		popupmenu.AppendItem(findclient)
		wx.EVT_MENU(popupmenu, FIND_CLIENT, self.FindClient)
		
		if self.lostorfounddata.contactid > 0:
			
			editclient = wx.MenuItem(popupmenu, EDIT_CLIENT, self.GetLabel("editlabel"))
			editclient.SetBitmap(wx.Bitmap("icons/edit.png"))
			popupmenu.AppendItem(editclient)
			wx.EVT_MENU(popupmenu, EDIT_CLIENT, self.EditClient)
			
			contactclient = wx.MenuItem(popupmenu, CONTACT_CLIENT, self.GetLabel("contacttooltip"))
			contactclient.SetBitmap(wx.Bitmap("icons/contact.png"))
			popupmenu.AppendItem(contactclient)
			wx.EVT_MENU(popupmenu, CONTACT_CLIENT, self.ContactClient)
		
		self.PopupMenu(popupmenu)
	
	def AnimalPopup(self, ID):
		
		#print "Client Popup"
		
		popupmenu = wx.Menu()
		
		editanimal = wx.MenuItem(popupmenu, EDIT_ANIMAL, self.GetLabel("editlabel"))
		editanimal.SetBitmap(wx.Bitmap("icons/edit.png"))
		popupmenu.AppendItem(editanimal)
		wx.EVT_MENU(popupmenu, EDIT_ANIMAL, self.EditAnimal)
		
		self.PopupMenu(popupmenu)
	
	def EditAnimal(self, ID):
		
		animalsettings = animalmethods.AnimalSettings(self.localsettings, False, self.lostorfounddata.animalid)
		
		animalpanel = animalmethods.AnimalPanel(self.notebook, animalsettings, False)
		
		self.notebook.AddPage(animalpanel)
	
	def Save(self, ID):
		
		#self.lostorfounddata.ID = False
		#self.lostorfounddata.lostorfound = 0
		#self.lostorfounddata.contactid = 0
		self.lostorfounddata.species = self.speciesentry.GetValue()
		date = self.dateentry.GetValue()
		self.lostorfounddata.date = miscmethods.GetSQLDateFromWXDate(date)
		self.lostorfounddata.sex = self.sexentry.GetSelection()
		self.lostorfounddata.neutered = self.neuteredentry.GetSelection()
		self.lostorfounddata.furlength = self.furlengthentry.GetSelection()
		self.lostorfounddata.colour1 = self.colour1entry.GetValue()
		self.lostorfounddata.colour2 = self.colour2entry.GetValue()
		self.lostorfounddata.colour3 = self.colour3entry.GetValue()
		self.lostorfounddata.collar = self.collarchoice.GetSelection()
		self.lostorfounddata.collardescription = self.collarentry.GetValue()
		self.lostorfounddata.size = self.bodysizeentry.GetSelection()
		self.lostorfounddata.age = self.ageentry.GetSelection()
		self.lostorfounddata.ischipped = self.chippedentry.GetSelection()
		#self.lostorfounddata.chipno = ""
		self.lostorfounddata.temperament = self.temperamententry.GetSelection()
		self.lostorfounddata.comments = self.commentsentry.GetValue()
		datecomplete = self.datecompletedentry.GetValue()
		self.lostorfounddata.datecomplete = miscmethods.GetSQLDateFromWXDate(datecomplete)
		self.lostorfounddata.area = self.areaentry.GetValue()
		
		dbmethods.WriteToLostAndFoundTable(self.localsettings.dbconnection, self.lostorfounddata)
		
		self.savebutton.Disable()
		self.matchbutton.Enable()
		
		if self.idlabel.GetLabel() == "":
			
			self.idlabel.SetLabel(miscmethods.NoWrap(" " + self.GetLabel("idlabel") + ": " + str(self.lostorfounddata.ID)))
			self.contactsizer.Layout()
	
	def ContactClient(self, ID):
		
		action = "SELECT ClientTitle, ClientForenames, ClientSurname, ClientAddress, ClientPostcode, ClientEmailAddress, ClientHomeTelephone, ClientMobileTelephone, ClientWorkTelephone, ClientComments, PhonePermissions FROM client WHERE ID = " + str(self.lostorfounddata.contactid)
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		name = ""
		
		if results[0][0] != "":
			
			name = name + results[0][0] + " "
		
		if results[0][1] != "":
			
			name = name + results[0][1] + " "
		
		if results[0][2] != "":
			
			name = name + results[0][2]
		
		dialog = wx.Frame(self, -1, self.GetLabel("contacttooltip") + ": " + name)
		iconFile = "icons/evette.ico"
		icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
		dialog.SetIcon(icon1)
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		namelabel = wx.StaticText(panel, -1, self.GetLabel("animalnamelabel"))
		topsizer.Add(namelabel, 0, wx.ALIGN_LEFT)
		
		namevalue = wx.StaticText(panel, -1, name)
		font = namevalue.GetFont()
		font.SetPointSize(font.GetPointSize() + 6)
		namevalue.SetFont(font)
		namevalue.SetForegroundColour("blue")
		
		topsizer.Add(namevalue, 0, wx.ALIGN_LEFT)
		
		hometelephonelabel = wx.StaticText(panel, -1, self.GetLabel("clienthomephonelabel"))
		topsizer.Add(hometelephonelabel, 0, wx.ALIGN_LEFT)
		
		hometelephonevalue = wx.StaticText(panel, -1, results[0][6])
		font = hometelephonevalue.GetFont()
		font.SetPointSize(font.GetPointSize() + 4)
		hometelephonevalue.SetFont(font)
		
		if str(results[0][10]).__contains__("1"):
			
			hometelephonevalue.SetForegroundColour("green")
			
		else:
			
			hometelephonevalue.SetForegroundColour("red")
		
		topsizer.Add(hometelephonevalue, 0, wx.ALIGN_LEFT)
		
		mobiletelephonelabel = wx.StaticText(panel, -1, self.GetLabel("clientmobilephonelabel"))
		topsizer.Add(mobiletelephonelabel, 0, wx.ALIGN_LEFT)
		
		mobiletelephonevalue = wx.StaticText(panel, -1, results[0][7])
		font = mobiletelephonevalue.GetFont()
		font.SetPointSize(font.GetPointSize() + 4)
		mobiletelephonevalue.SetFont(font)
		
		if str(results[0][10]).__contains__("2"):
			
			mobiletelephonevalue.SetForegroundColour("green")
			
		else:
			
			mobiletelephonevalue.SetForegroundColour("red")
		
		topsizer.Add(mobiletelephonevalue, 0, wx.ALIGN_LEFT)
		
		worktelephonelabel = wx.StaticText(panel, -1, self.GetLabel("clientworkphonelabel"))
		topsizer.Add(worktelephonelabel, 0, wx.ALIGN_LEFT)
		
		worktelephonevalue = wx.StaticText(panel, -1, results[0][8])
		font = worktelephonevalue.GetFont()
		font.SetPointSize(font.GetPointSize() + 4)
		worktelephonevalue.SetFont(font)
		
		if str(results[0][10]).__contains__("3"):
			
			worktelephonevalue.SetForegroundColour("green")
			
		else:
			
			worktelephonevalue.SetForegroundColour("red")
		
		topsizer.Add(worktelephonevalue, 0, wx.ALIGN_LEFT)
		
		emailaddresslabel = wx.StaticText(panel, -1, self.GetLabel("clientemailaddresslabel"))
		topsizer.Add(emailaddresslabel, 0, wx.ALIGN_LEFT)
		
		emailaddressvalue = wx.StaticText(panel, -1, results[0][5])
		font = emailaddressvalue.GetFont()
		font.SetPointSize(font.GetPointSize() + 4)
		emailaddressvalue.SetFont(font)
		
		topsizer.Add(emailaddressvalue, 0, wx.ALIGN_LEFT)
		
		addresslabel = wx.StaticText(panel, -1, self.GetLabel("clientaddresslabel"))
		topsizer.Add(addresslabel, 0, wx.ALIGN_LEFT)
		
		addressvalue = wx.StaticText(panel, -1, results[0][3])
		font = addressvalue.GetFont()
		font.SetPointSize(font.GetPointSize() + 3)
		addressvalue.SetFont(font)
		
		topsizer.Add(addressvalue, 0, wx.ALIGN_LEFT)
		
		postcodevalue = wx.StaticText(panel, -1, results[0][4])
		font = postcodevalue.GetFont()
		font.SetPointSize(font.GetPointSize() + 3)
		postcodevalue.SetFont(font)
		
		topsizer.Add(postcodevalue, 0, wx.ALIGN_LEFT)
		
		panel.SetSizer(topsizer)
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		#dialog.SetSize((300,200))
		dialog.Fit()
		
		dialog.CenterOnScreen()
		
		dialog.Show()
	
	def FindClient(self, ID):
		
		clientmethods.FindClientDialog(self, self.localsettings)
		
		try:
			
			clientid = self.clientdialogid
			
		except:
			
			clientid = 0
		
		if clientid > 0:
			
			self.lostorfounddata.contactid = clientid
			
			self.UpdateContactInfo(self.lostorfounddata.contactid)
	
	def UpdateContactInfo(self, contactid):
		
		#print "Updating contact info!"
		
		self.lostorfounddata.contactid = contactid
		
		if self.lostorfounddata.contactid > 0:
			
			action = "SELECT ClientTitle, ClientForenames, ClientSurname, ClientAddress, ClientPostcode, ClientEmailAddress, ClientHomeTelephone, ClientMobileTelephone, ClientWorkTelephone, ClientComments FROM client WHERE ID = " + str(self.lostorfounddata.contactid)
			results = db.SendSQL(action, self.localsettings.dbconnection)
			
			name = ""
			
			if results[0][0] != "":
				
				name = name + results[0][0] + " "
			
			if results[0][1] != "":
				
				name = name + results[0][1] + " "
			
			if results[0][2] != "":
				
				name = name + results[0][2]
			
			self.cliententry.SetLabel(miscmethods.NoWrap(name))
			
			#self.contactclientbutton.Enable()
			#self.editclientbutton.Enable()
			
			self.contactsizer.Layout()
			
			self.EnableSave()
		
	def AddClient(self, ID):
		
		addclientpanel = AddClientPanel(self)
		
		self.notebook.AddPage(addclientpanel)
	
	def EditClient(self, ID):
		
		clientdata = clientmethods.ClientSettings(self.localsettings, self.lostorfounddata.contactid)
		
		editclientpanel = clientmethods.ClientPanel(self.notebook, clientdata)
		
		self.notebook.AddPage(editclientpanel)

class AddClientPanel:
	
	def __init__(self, editlostandfoundpanel):
		
		self.editlostandfoundpanel = editlostandfoundpanel
		
		self.clientdata = clientmethods.ClientSettings(editlostandfoundpanel.localsettings)
		
		self.clientpanel = clientmethods.ClientPanel(editlostandfoundpanel.notebook, self.clientdata)
	
	def SaveClient(self, ID):
		
		self.clientpanel.SaveClient(self, ID)
		
		self.editlostandfoundpanel.UpdateContactInfo(self.clientdata.ID)

class LostAndFoundListCtrl(customwidgets.ListCtrlWrapper):
	
	def GetLabel(self, field):
		
		return  self.localsettings.dictionary[field][self.localsettings.language]
	
	def __init__(self, parent, lostorfound):
		
		self.lostorfound = lostorfound
		self.localsettings = parent.GetParent().localsettings
		self.parent = parent
		
		columnheadings = (self.GetLabel("idlabel"), self.GetLabel("datelabel"), self.GetLabel("animalspecieslabel"), self.GetLabel("animalsexlabel"), self.GetLabel("neuteredlabel"), self.GetLabel("arealabel"), self.GetLabel("animalcolourlabel"), self.GetLabel("contacttooltip"), self.GetLabel("completelabel"))
		
		customwidgets.ListCtrlWrapper.__init__(self, parent, self.localsettings, columnheadings, ("icons/editanimal.png", "icons/evettelogo.png", "icons/asm.png"))
	
	def ProcessRow(self, rowdata):
		
		#print "rowdata[8] = " + str(rowdata[8])
		
		if rowdata[9] > 0:
			
			imageid = 1
			
		else:
			
			imageid = 0
		
		return ( (rowdata[0], str(rowdata[0]), rowdata[1], rowdata[2], rowdata[3], rowdata[4], rowdata[5], rowdata[6], rowdata[7], rowdata[8] ), imageid )
	
	def RefreshList(self):
		
		self.htmllist = []
		
		parent = self.parent.GetGrandParent()
		
		fromdate = parent.fromentry.GetValue()
		fromdate = miscmethods.GetSQLDateFromWXDate(fromdate)
		
		todate = parent.toentry.GetValue()
		todate = miscmethods.GetSQLDateFromWXDate(todate)
		
		lostandfoundid = parent.identry.GetValue()
		species = parent.speciesentry.GetValue()
		colour = parent.colourentry.GetValue()
		sex = parent.sexentry.GetSelection()
		neutered = parent.neuteredentry.GetSelection()
		age = parent.ageentry.GetSelection()
		area = parent.areaentry.GetValue()
		
		includecomplete = parent.includecompletecheckbox.GetValue()
		
		if str(fromdate) == "0000-00-00" and str(todate) == "0000-00-00":
			
			datearguments = ""
			
		elif str(fromdate) == "0000-00-00":
			
			datearguments = " AND lostandfound.Date <= \"" + str(todate) + "\""
			
		elif str(todate) == "0000-00-00":
			
			datearguments = " AND lostandfound.Date >= \"" + str(fromdate) + "\""
			
		else:
			
			datearguments = " AND lostandfound.Date BETWEEN \"" + str(fromdate) + "\" AND \"" + str(todate) + "\""
		
		
		
		filterarguments = ""
		
		if lostandfoundid != "":
			
			filterarguments = " AND lostandfound.ID = " + str(lostandfoundid)
		
		if species != "":
			
			filterarguments = filterarguments + " AND lostandfound.Species LIKE \"%" + species + "%\""
		
		if colour != "":
			
			filterarguments = filterarguments + " AND ( "
			
			colourarguments = ""
			
			for a in colour.split(" "):
				
				if colourarguments != "":
					
					colourarguments = colourarguments + " OR "
				
				colourarguments = colourarguments + "Colour1 LIKE \"%" + a + "%\" OR Colour2 LIKE \"%" + a + "%\" OR Colour3 LIKE \"%" + a + "%\""
			
			filterarguments = filterarguments + colourarguments + " )"
		
		if sex > 0:
			
			filterarguments = filterarguments + " AND lostandfound.Sex = " + str(sex)
		
		if age > 0:
			
			filterarguments = filterarguments + " AND lostandfound.Age = " + str(age)
		
		if neutered > 0:
			
			filterarguments = filterarguments + " AND lostandfound.Neutered = " + str(neutered)
		
		if area != "":
			
			filterarguments = filterarguments + " AND lostandfound.Area LIKE \"%" + str(area) + "%\""
		
		if includecomplete == False:
			
			filterarguments = filterarguments + " AND lostandfound.DateComplete = \"0000-00-00\""
		
		action = "SELECT lostandfound.ID, lostandfound.Date, lostandfound.Species, lostandfound.Sex, lostandfound.Neutered, lostandfound.Colour1, lostandfound.Colour2, lostandfound.Colour3, client.ClientTitle, client.ClientForenames, client.ClientSurname, lostandfound.DateComplete, lostandfound.Area, lostandfound.AnimalID FROM lostandfound INNER JOIN client ON lostandfound.ContactID = client.ID WHERE lostandfound.LostOrFound = " + str(self.lostorfound) + datearguments + filterarguments
		
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		if len(results) < 1001:
			
			count = 0
			
			for a in results:
				
				name = ""
				
				if a[8] != "":
					
					name = name + a[8] + " "
				
				if a[9] != "":
					
					name = name + a[9] + " "
				
				if a[10] != "":
					
					name = name + a[10]
				
				colour = ""
				
				if a[5] != "":
					
					colour = colour + a[5] + " "
				
				if a[6] != "":
					
					colour = colour + a[6] + " "
				
				if a[7] != "":
					
					colour = colour + a[7]
				
				if a[3] == 0:
					
					sex = "???"
					
				elif a[3] == 1:
					
					sex = self.GetLabel("malelabel")
					
				else:
					
					sex = self.GetLabel("femalelabel")
				
				if a[4] == 0:
					
					neutered = "???"
					
				elif a[4] == 1:
					
					neutered = self.GetLabel("yeslabel")
					
				else:
					
					neutered = self.GetLabel("nolabel")
				
				date = miscmethods.FormatSQLDate(a[1], self.localsettings)
				
				complete = a[11]
				
				if complete != None:
					
					complete = self.GetLabel("yeslabel")
					
				else:
					
					complete = self.GetLabel("nolabel")
				
				area = a[12]
				
				animalid = a[13]
				
				self.htmllist.append( (a[0], date, a[2], sex, neutered, area, colour, name, complete, animalid) )
		
		customwidgets.ListCtrlWrapper.RefreshList(self)
		
		self.totallabel.SetLabel(miscmethods.NoWrap(self.GetLabel("totallabel") + ": " + str(len(results))))

class LostAndFoundMatchListCtrl(wx.ListCtrl, listmix.ColumnSorterMixin):
	
	def GetLabel(self, field):
		
		return  self.localsettings.dictionary[field][self.localsettings.language]
	
	def __init__(self, parent, possiblematches, localsettings):
		
		self.localsettings = localsettings
		self.parent = parent
		self.possiblematches = possiblematches
		
		wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
		listmix.ColumnSorterMixin.__init__(self, 7)
		
		#imagelist = wx.ImageList(20, 20)
		#asmicon = imagelist.Add(wx.Bitmap("icons/editclient.png"))
		#self.listctrl.AssignImageList(imagelist, wx.IMAGE_LIST_SMALL)
		
		#self.listctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.Edit)
		#self.listctrl.Bind(wx.wx.EVT_RIGHT_DOWN, self.ClientPopupMenu)
		
		self.InsertColumn(0,self.GetLabel("idlabel"))
		self.InsertColumn(1,self.GetLabel("scorelabel"))
		self.InsertColumn(2,self.GetLabel("datelabel"))
		self.InsertColumn(3,self.GetLabel("animalspecieslabel"))
		self.InsertColumn(4,self.GetLabel("animalsexlabel"))
		self.InsertColumn(5,self.GetLabel("neuteredlabel"))
		self.InsertColumn(6,self.GetLabel("arealabel"))
		self.InsertColumn(7,self.GetLabel("animalcolourlabel"))
		self.InsertColumn(8,self.GetLabel("contacttooltip"))
		
		self.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
		self.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
		self.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
		self.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)
		self.SetColumnWidth(4, wx.LIST_AUTOSIZE_USEHEADER)
		self.SetColumnWidth(5, wx.LIST_AUTOSIZE_USEHEADER)
		self.SetColumnWidth(6, wx.LIST_AUTOSIZE_USEHEADER)
		self.SetColumnWidth(7, wx.LIST_AUTOSIZE_USEHEADER)
		self.SetColumnWidth(8, wx.LIST_AUTOSIZE_USEHEADER)
	
	def GetListCtrl(self):# Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
		
        	return self
	
	def RefreshList(self):
		
		scores = []
		results = []
		
		for a in self.possiblematches:
			
			scores.append(a[0])
			results.append(a[1])
		
		#print "scores = " + str(scores)
		
		self.itemDataMap = {}
		
		self.ClearAll()
		
		if len(results) < 1001:
			
			self.InsertColumn(0,self.GetLabel("idlabel"))
			self.InsertColumn(1,self.GetLabel("scorelabel"))
			self.InsertColumn(2,self.GetLabel("datelabel"))
			self.InsertColumn(3,self.GetLabel("animalspecieslabel"))
			self.InsertColumn(4,self.GetLabel("animalsexlabel"))
			self.InsertColumn(5,self.GetLabel("neuteredlabel"))
			self.InsertColumn(6,self.GetLabel("arealabel"))
			self.InsertColumn(7,self.GetLabel("animalcolourlabel"))
			self.InsertColumn(8,self.GetLabel("contacttooltip"))
			
			#foundID = a[0]
			##foundlostorfound = a[1]
			##foundcontactid = a[2]
			#foundspecies = unicode(a[3], "utf8")
			##founddate = a[4]
			#foundsex = a[5]
			#foundneutered = a[6]
			#foundfurlength = a[7]
			#foundcolour1 = unicode(a[8], "utf8")
			#foundcolour2 = unicode(a[9], "utf8")
			#foundcolour3 = unicode(a[10], "utf8")
			#foundcollar = a[11]
			#foundcollardescription = unicode(a[12], "utf8")
			#foundsize = a[13]
			#foundage = a[14]
			#foundischipped = a[15]
			#foundchipno = unicode(a[16], "utf8")
			#foundtemperament = a[17]
			#foundcomments = unicode(a[18], "utf8")
			#founddatecomplete = a[19]
			#foundchangelog = a[20]
			#foundarea = unicode(a[21], "utf8")
			#animalid
			
			count = 0
			
			for a in results:
				
				name = ""
				
				if a[23] != "":
					
					name = name + a[23] + " "
				
				if a[24] != "":
					
					name = name + a[24] + " "
				
				if a[25] != "":
					
					name = name + a[25]
				
				colour = ""
				
				if a[8] != "":
					
					colour = colour + a[8] + " "
				
				if a[9] != "":
					
					colour = colour + a[9] + " "
				
				if a[10] != "":
					
					colour = colour + a[10]
				
				if a[5] == 0:
					
					sex = "???"
					
				elif a[5] == 1:
					
					sex = self.GetLabel("malelabel")
					
				else:
					
					sex = self.GetLabel("femalelabel")
				
				if a[6] == 0:
					
					neutered = "???"
					
				elif a[6] == 1:
					
					neutered = self.GetLabel("yeslabel")
					
				else:
					
					neutered = self.GetLabel("nolabel")
				
				date = miscmethods.FormatSQLDate(a[4], self.localsettings)
				
				complete = a[19]
				
				if complete != None:
					
					complete = self.GetLabel("yeslabel")
					
				else:
					
					complete = self.GetLabel("nolabel")
				
				area = a[21]
				
				species = a[3]
				
				lostandfoundid = str(a[0])
				
				score = str(scores[count])
				
				self.itemDataMap[a[0]] = ( lostandfoundid, score, date, species, sex, neutered, area, colour, name )
				
				self.InsertStringItem(count, lostandfoundid)
				self.SetStringItem(count, 1, score)
				self.SetStringItem(count, 2, date)
				self.SetStringItem(count, 3, species)
				self.SetStringItem(count, 4, sex)
				self.SetStringItem(count, 5, neutered)
				self.SetStringItem(count, 6, area)
				self.SetStringItem(count, 7, colour)
				self.SetStringItem(count, 8, name)
				
				self.SetItemImage(count, 0)
				
				self.SetItemData(count, a[0])
				
				count = count + 1
				
			if len(results) == 0:
				
				self.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
				self.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
				self.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
				self.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)
				self.SetColumnWidth(4, wx.LIST_AUTOSIZE_USEHEADER)
				self.SetColumnWidth(5, wx.LIST_AUTOSIZE_USEHEADER)
				self.SetColumnWidth(6, wx.LIST_AUTOSIZE_USEHEADER)
				self.SetColumnWidth(7, wx.LIST_AUTOSIZE_USEHEADER)
				self.SetColumnWidth(8, wx.LIST_AUTOSIZE_USEHEADER)
				
			else:
				
				for a in range(0,9):
					
					self.SetColumnWidth(a, wx.LIST_AUTOSIZE_USEHEADER)
					headerwidth = self.GetColumnWidth(a)
					
					self.SetColumnWidth(a, wx.LIST_AUTOSIZE)
					autowidth = self.GetColumnWidth(a)
					
					if autowidth < headerwidth:
						
						self.SetColumnWidth(a, wx.LIST_AUTOSIZE_USEHEADER)
						
					else:
						
						self.SetColumnWidth(a, wx.LIST_AUTOSIZE)
					
					if a == 2:
						
						columnwidth = self.GetColumnWidth(a)
						self.SetColumnWidth(a, columnwidth + 10)
		
		#self.totallabel.SetLabel(miscmethods.NoWrap(self.GetLabel("totallabel") + ": " + str(len(results))))
