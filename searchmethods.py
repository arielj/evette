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
import wx.media
import miscmethods
import db
import dbmethods
import datetime
import animalmethods
import appointmentmethods
import customwidgets
import clientmethods
import wx.lib.mixins.listctrl as listmix
import sys

EDIT_CLIENT = 900
DELETE_CLIENT = 901
EDIT_ANIMAL = 902
DELETE_ANIMAL = 903
CLIENT_CHANGELOG = 904
ANIMAL_CHANGELOG = 905

class SmallSpacer(wx.StaticText):
	
	def __init__(self, parent):
		
		wx.StaticText.__init__(self, parent, size=(10,-1))
		font = self.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		self.SetFont(font)

class SearchPanel(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, notebook, localsettings):
		
		self.localsettings = localsettings
		self.notebook = notebook
		
		wx.Panel.__init__(self, notebook)
		
		rawpagetitle = self.t("clientsearchpagetitle")
		
		pagetitle = miscmethods.GetPageTitle(notebook, rawpagetitle)
		self.pagetitle = pagetitle
		self.pageimage = "icons/search.png"
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		filterpanel = wx.Panel(self)
		
		filtersizer = wx.FlexGridSizer(cols=5)
		filtersizer.AddGrowableCol(0)
		#filtersizer.AddGrowableCol(1)
		filtersizer.AddGrowableCol(2)
		#filtersizer.AddGrowableCol(3)
		filtersizer.AddGrowableCol(4)
		
		namelabel = wx.StaticText(filterpanel, -1, miscmethods.NoWrap(" " + self.t("animalownerlabel") + ":"))
		font = namelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		namelabel.SetFont(font)
		filtersizer.Add(namelabel, 0, wx.ALIGN_LEFT)
		
		filtersizer.Add(SmallSpacer(filterpanel), 0, wx.EXPAND)
		
		addresslabel = wx.StaticText(filterpanel, -1, miscmethods.NoWrap(" " + self.t("clientsearchaddresslabel") + ":"))
		addresslabel.SetFont(font)
		filtersizer.Add(addresslabel, 0, wx.ALIGN_LEFT)
		
		filtersizer.Add(SmallSpacer(filterpanel), 0, wx.EXPAND)
		
		postcodelabel = wx.StaticText(filterpanel, -1, miscmethods.NoWrap(" " + self.t("clientsearchpostcodelabel") + ":"))
		postcodelabel.SetFont(font)
		filtersizer.Add(postcodelabel, 0, wx.ALIGN_LEFT)
		
		nameentry = wx.TextCtrl(filterpanel, -1, "", style=wx.TE_PROCESS_ENTER)
		nameentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		filtersizer.Add(nameentry, 1, wx.EXPAND)
		
		filtersizer.Add(wx.StaticText(filterpanel, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		addressentry = wx.TextCtrl(filterpanel, -1, "", style=wx.TE_PROCESS_ENTER)
		addressentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		filtersizer.Add(addressentry, 1, wx.EXPAND)
		
		filtersizer.Add(wx.StaticText(filterpanel, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		postcodeentry = wx.TextCtrl(filterpanel, -1, "", style=wx.TE_PROCESS_ENTER)
		postcodeentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		filtersizer.Add(postcodeentry, 1, wx.EXPAND)
		
		telephonelabel = wx.StaticText(filterpanel, -1, miscmethods.NoWrap(" " + self.t("clientsearchphonelabel") + ":"))
		telephonelabel.SetFont(font)
		filtersizer.Add(telephonelabel, 0, wx.ALIGN_LEFT)
		
		filtersizer.Add(SmallSpacer(filterpanel), 0, wx.EXPAND)
		
		emailaddresslabel = wx.StaticText(filterpanel, -1, miscmethods.NoWrap(" " + self.t("clientsearchemaillabel") + ":"))
		emailaddresslabel.SetFont(font)
		filtersizer.Add(emailaddresslabel, 0, wx.ALIGN_LEFT)
		
		filtersizer.Add(SmallSpacer(filterpanel), 0, wx.EXPAND)
		
		clientcommentslabel = wx.StaticText(filterpanel, -1, miscmethods.NoWrap(" " + self.t("clientcommentslabel") + ":"))
		clientcommentslabel.SetFont(font)
		filtersizer.Add(clientcommentslabel, 0, wx.ALIGN_LEFT)
		
		telephoneentry = wx.TextCtrl(filterpanel, -1, "", style=wx.TE_PROCESS_ENTER)
		telephoneentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		filtersizer.Add(telephoneentry, 1, wx.EXPAND)
		
		filtersizer.Add(wx.StaticText(filterpanel, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		emailaddressentry = wx.TextCtrl(filterpanel, -1, "", style=wx.TE_PROCESS_ENTER)
		emailaddressentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		filtersizer.Add(emailaddressentry, 1, wx.EXPAND)
		
		filtersizer.Add(wx.StaticText(filterpanel, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		clientcommentsentry = wx.TextCtrl(filterpanel, -1, "", style=wx.TE_PROCESS_ENTER)
		clientcommentsentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		filtersizer.Add(clientcommentsentry, 1, wx.EXPAND)
		
		animalnamelabel = wx.StaticText(filterpanel, -1, miscmethods.NoWrap(" " + self.t("appointmentsearchanimalnamelabel") + ":"))
		animalnamelabel.SetFont(font)
		filtersizer.Add(animalnamelabel, 0, wx.ALIGN_LEFT)
		
		filtersizer.Add(SmallSpacer(filterpanel), 0, wx.EXPAND)
		
		specieslabel = wx.StaticText(filterpanel, -1, miscmethods.NoWrap(" " + self.t("animalspecieslabel") + ":"))
		specieslabel.SetFont(font)
		filtersizer.Add(specieslabel, 0, wx.ALIGN_LEFT)
		
		filtersizer.Add(SmallSpacer(filterpanel), 0, wx.EXPAND)
		
		sexlabel = wx.StaticText(filterpanel, -1, miscmethods.NoWrap(" " + self.t("animalsexlabel") + ":"))
		sexlabel.SetFont(font)
		filtersizer.Add(sexlabel, 0, wx.ALIGN_LEFT)
		
		animalnameentry = wx.TextCtrl(filterpanel, -1, "", style=wx.TE_PROCESS_ENTER)
		animalnameentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		filtersizer.Add(animalnameentry, 1, wx.EXPAND)
		
		action = "SELECT SpeciesName FROM species ORDER BY SpeciesName"
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		specieslist = []
		
		for a in results:
			
			specieslist.append(a[0])
		
		filtersizer.Add(wx.StaticText(filterpanel, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		speciesentry = wx.ComboBox(filterpanel, -1, choices=specieslist)
		speciesentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		filtersizer.Add(speciesentry, 1, wx.EXPAND)
		
		filtersizer.Add(wx.StaticText(filterpanel, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		sexentry = wx.Choice(filterpanel, -1, choices=(self.t("unknownlabel"), self.t("malelabel"), self.t("femalelabel")))
		sexentry.SetSelection(0)
		#sexentry.Bind(wx.EVT_CHOICE, self.KeyPressed)
		filtersizer.Add(sexentry, 0, wx.EXPAND)
		
		breedlabel = wx.StaticText(filterpanel, -1, miscmethods.NoWrap(" " + self.t("animalbreedlabel") + ":"))
		breedlabel.SetFont(font)
		filtersizer.Add(breedlabel, 1, wx.ALIGN_LEFT)
		
		filtersizer.Add(SmallSpacer(filterpanel), 0, wx.EXPAND)
		
		chipnolabel = wx.StaticText(filterpanel, -1, miscmethods.NoWrap(" " + self.t("animalchipnolabel") + ":"))
		chipnolabel.SetFont(font)
		filtersizer.Add(chipnolabel, 0, wx.ALIGN_LEFT)
		
		filtersizer.Add(SmallSpacer(filterpanel), 0, wx.EXPAND)
		
		asmreflabel = wx.StaticText(filterpanel, -1, miscmethods.NoWrap(" " + self.t("asmreflabel") + ":"))
		asmreflabel.SetFont(font)
		filtersizer.Add(asmreflabel, 0, wx.ALIGN_LEFT)
		
		action = "SELECT BreedName FROM breed ORDER BY BreedName"
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		breedlist = []
		
		for a in results:
			
			breedlist.append(a[0])
		
		breedentry = wx.ComboBox(filterpanel, -1, choices=breedlist)
		breedentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		filtersizer.Add(breedentry, 1, wx.EXPAND)
		
		filtersizer.Add(wx.StaticText(filterpanel, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		chipnoentry = wx.TextCtrl(filterpanel, -1, "", style=wx.TE_PROCESS_ENTER)
		chipnoentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		filtersizer.Add(chipnoentry, 1, wx.EXPAND)
		
		filtersizer.Add(wx.StaticText(filterpanel, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		asmrefentry = wx.TextCtrl(filterpanel, -1, "", style=wx.TE_PROCESS_ENTER)
		asmrefentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		filtersizer.Add(asmrefentry, 1, wx.EXPAND)
		
		animalcommentslabel = wx.StaticText(filterpanel, -1, miscmethods.NoWrap(" " + self.t("clientcommentslabel") + ":"))
		animalcommentslabel.SetFont(font)
		filtersizer.Add(animalcommentslabel, 0, wx.ALIGN_LEFT)
		
		filtersizer.Add(SmallSpacer(filterpanel), 0, wx.EXPAND)
		filtersizer.Add(SmallSpacer(filterpanel), 0, wx.EXPAND)
		filtersizer.Add(SmallSpacer(filterpanel), 0, wx.EXPAND)
		filtersizer.Add(SmallSpacer(filterpanel), 0, wx.EXPAND)
		
		animalcommentsentry = wx.TextCtrl(filterpanel, -1, "", style=wx.TE_PROCESS_ENTER)
		animalcommentsentry.Bind(wx.EVT_CHAR, self.KeyPressed)
		filtersizer.Add(animalcommentsentry, 1, wx.EXPAND)
		
		filtersizer.Add(wx.StaticText(filterpanel, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		buttonssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		resetbutton = wx.Button(filterpanel, -1, self.t("resetlabel"))
		resetbutton.SetBackgroundColour("red")
		resetbutton.SetForegroundColour("white")
		resetbutton.Bind(wx.EVT_BUTTON, self.Reset)
		buttonssizer.Add(resetbutton, 1, wx.EXPAND)
		
		searchbutton = wx.Button(filterpanel, -1, self.t("searchlabel"))
		searchbutton.SetBackgroundColour("green")
		searchbutton.SetForegroundColour("black")
		searchbutton.Bind(wx.EVT_BUTTON, self.Search)
		buttonssizer.Add(searchbutton, 1, wx.EXPAND)
		
		filtersizer.Add(buttonssizer, 1, wx.EXPAND)
		
		filtersizer.Add(wx.StaticText(filterpanel, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		includedeceasedentry = wx.CheckBox(filterpanel, -1, miscmethods.NoWrap(self.t("includedeceasedlabel")))
		includedeceasedentry.SetValue(True)
		filtersizer.Add(includedeceasedentry, 1, wx.ALIGN_LEFT)
		
		filterpanel.SetSizer(filtersizer)
		
		topsizer.Add(filterpanel, 0, wx.EXPAND)
		
		topsizer.Add(wx.StaticText(self,-1, "", size=(-1,10)), 0, wx.EXPAND)
                
                #if str(sys.platform)[:3] != "win":
                
                splitter = wx.SplitterWindow(self, -1)
                splitter.notebook = self.notebook
                clientpanel = ClientSearchPanel(splitter, self.localsettings)
                animalpanel = AnimalSearchPanel(splitter, self.localsettings)
                splitter.SplitVertically(clientpanel, animalpanel)
                topsizer.Add(splitter, 1, wx.EXPAND)
##              
##                else:
##                        
##                        splittersizer = wx.BoxSizer(wx.HORIZONTAL)
##                        clientpanel = ClientSearchPanel(self, self.localsettings)
##                        animalpanel = AnimalSearchPanel(self, self.localsettings)
##                        splittersizer.Add(clientpanel, 1, wx.EXPAND)
##                        splittersizer.Add(animalpanel, 1, wx.EXPAND)
##                        topsizer.Add(splittersizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.nameentry = nameentry
		self.addressentry = addressentry
		self.postcodeentry = postcodeentry
		self.telephoneentry = telephoneentry
		self.emailaddressentry = emailaddressentry
		self.clientcommentsentry = clientcommentsentry
		self.animalnameentry = animalnameentry
		self.sexentry = sexentry
		self.speciesentry = speciesentry
		self.breedentry = breedentry
		self.chipnoentry = chipnoentry
		self.asmrefentry = asmrefentry
		self.animalcommentsentry = animalcommentsentry
		self.includedeceasedentry = includedeceasedentry
		
		self.clientpanel = clientpanel
		self.animalpanel = animalpanel
	
	def KeyPressed(self, ID):
		
		keycode = ID.GetKeyCode()
		
		if keycode == 13:
			
			self.Search()
		
		ID.Skip()
	
	def Reset(self, ID):
		
		self.nameentry.Clear()
		self.addressentry.Clear()
		self.postcodeentry.Clear()
		self.telephoneentry.Clear()
		self.emailaddressentry.Clear()
		self.clientcommentsentry.Clear()
		self.animalnameentry.Clear()
		self.sexentry.SetSelection(0)
		self.speciesentry.SetValue("")
		self.breedentry.SetValue("")
		self.chipnoentry.Clear()
		self.asmrefentry.Clear()
		self.animalcommentsentry.Clear()
		self.includedeceasedentry.SetValue(True)
	
	def Search(self, ID=False):
		
		animalsql = ""
		
		if self.animalnameentry.GetValue() != "":
			
			animalsql = animalsql + "animal.Name LIKE \"%" + self.animalnameentry.GetValue() + "%\""
		
		if self.sexentry.GetSelection() > 0:
			
			if animalsql != "":
				
				animalsql = animalsql + " AND "
			
			animalsql = animalsql + "animal.Sex = " + str(self.sexentry.GetSelection())
		
		if self.speciesentry.GetValue() != "":
			
			if animalsql != "":
				
				animalsql = animalsql + " AND "
			
			animalsql = animalsql + "animal.Species LIKE \"%" + self.speciesentry.GetValue() + "%\""
		
		if self.breedentry.GetValue() != "":
			if animalsql != "":
				animalsql = animalsql + " AND "
			
			animalsql = animalsql + "animal.Breed LIKE \"%" + self.breedentry.GetValue() + "%\""
		
		if self.chipnoentry.GetValue() != "":
			
			if animalsql != "":
				
				animalsql = animalsql + " AND "
			
			animalsql = animalsql + "animal.ChipNo LIKE \"%" + self.chipnoentry.GetValue() + "%\""
		
		if self.asmrefentry.GetValue() != "":
			
			if animalsql != "":
				
				animalsql = animalsql + " AND "
			
			animalsql = animalsql + "animal.ASMRef LIKE \"%" + self.asmrefentry.GetValue() + "%\""
		
		if self.animalcommentsentry.GetValue() != "":
			
			if animalsql != "":
				
				animalsql = animalsql + " AND "
			
			animalsql = animalsql + "animal.Comments LIKE \"%" + self.animalcommentsentry.GetValue() + "%\""
		
		if self.includedeceasedentry.GetValue() == False:
			
			if animalsql != "":
				
				animalsql = animalsql + " AND "
			
			animalsql = animalsql + "animal.IsDeceased = 0"
		
		clientsql = ""
		
		if self.nameentry.GetValue() != "":
			
			clientsql = clientsql + "CONCAT(client.ClientTitle, \" \", client.ClientForenames, \" \", client.ClientSurName) LIKE \"%" + self.nameentry.GetValue() + "%\""
		
		if self.telephoneentry.GetValue() != "":
			
			if clientsql != "":
				
				clientsql = clientsql + " AND "
			
			clientsql = clientsql + "( client.ClientHomeTelephone LIKE \"%" + self.telephoneentry.GetValue() + "%\" OR client.ClientMobileTelephone LIKE \"%" + self.telephoneentry.GetValue() + "%\" OR client.ClientWorkTelephone LIKE \"%" + self.telephoneentry.GetValue() + "%\" )"
		
		if self.addressentry.GetValue() != "":
			
			if clientsql != "":
				
				clientsql = clientsql + " AND "
			
			clientsql = clientsql + "client.ClientAddress LIKE \"%" + self.addressentry.GetValue() + "%\""
		
		if self.postcodeentry.GetValue() != "":
			
			if clientsql != "":
				
				clientsql = clientsql + " AND "
			
			clientsql = clientsql + "client.ClientPostcode LIKE \"%" + self.postcodeentry.GetValue() + "%\""
		
		if self.emailaddressentry.GetValue() != "":
			
			if clientsql != "":
				
				clientsql = clientsql + " AND "
			
			clientsql = clientsql + "client.ClientEmailAddress LIKE \"%" + self.emailaddressentry.GetValue() + "%\""
		
		if self.clientcommentsentry.GetValue() != "":
			
			if clientsql != "":
				
				clientsql = clientsql + " AND "
			
			clientsql = clientsql + "client.ClientComments LIKE \"%" + self.clientcommentsentry.GetValue() + "%\""
		
		if clientsql == "" and animalsql == "":
			
			clientaction = "SELECT * FROM client"
			animalaction = "SELECT * FROM animal"
			
		elif clientsql == "" and animalsql != "":
			
			clientaction = "SELECT * FROM client INNER JOIN animal ON animal.OwnerID = client.ID WHERE " + animalsql
			animalaction = "SELECT * FROM animal WHERE " + animalsql
		
		elif animalsql == "" and clientsql != "":
			
			clientaction = "SELECT * FROM client WHERE " + clientsql
			animalaction = "SELECT * FROM animal INNER JOIN client ON animal.OwnerID = client.ID WHERE " + clientsql
			
		else:
			
			clientaction = "SELECT * FROM client INNER JOIN animal ON animal.OwnerID = client.ID WHERE " + animalsql + " AND " + clientsql
			animalaction = "SELECT * FROM animal INNER JOIN client ON animal.OwnerID = client.ID WHERE " + animalsql + " AND " + clientsql
		
		busy = wx.BusyCursor()
		
		rawclientresults = db.SendSQL(clientaction, self.localsettings.dbconnection)
		
		animalresults = db.SendSQL(animalaction, self.localsettings.dbconnection)
		
		clientresults = []
		
		for a in rawclientresults:
			
			duplicate = False
			
			for b in clientresults:
				
				if b[0] == a[0]:
					
					duplicate = True
			
			if duplicate == False:
				
				clientresults.append(a)
		
		if len(clientresults) > 1000 or len(animalresults) > 1000:
			
			miscmethods.ShowMessage(self.t("toomanyresultsmessage"), self)
		
		self.clientpanel.RefreshList(clientresults)
		
		self.animalpanel.RefreshList(animalresults)
		
		del busy

class ClientSearchPanel(wx.Panel, listmix.ColumnSorterMixin):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, parent, localsettings):
		
		busy = wx.BusyCursor()
		
		self.localsettings = localsettings
		self.parent = parent
		
		wx.Panel.__init__(self, parent)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		topsizer.Add(wx.StaticText(self, -1, self.t("clientmenu")), 0, wx.ALIGN_CENTER)
		
		self.listctrl = ClientListCtrl(self, self.localsettings)
		customwidgets.ListCtrlWrapper.RefreshList(self.listctrl)
		
		self.listctrl.listctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.Edit)
		self.listctrl.listctrl.Bind(wx.EVT_RIGHT_DOWN, self.ClientPopupMenu)
		
		topsizer.Add(self.listctrl, 1, wx.EXPAND)
		
		self.totallabel = wx.StaticText(self, -1, self.t("totallabel") + ": 0")
		topsizer.Add(self.totallabel, 0, wx.ALIGN_LEFT)
		
		self.SetSizer(topsizer)
		
		del busy
	
	def ClientPopupMenu(self, ID):
		
		if self.listctrl.listctrl.GetSelectedItemCount() > 0:
			
			popupmenu = wx.Menu()
			
			if self.localsettings.editclients == 1:
				
				editclient = wx.MenuItem(popupmenu, EDIT_CLIENT, self.t("editlabel"))
				editclient.SetBitmap(wx.Bitmap("icons/edit.png"))
				popupmenu.AppendItem(editclient)
				wx.EVT_MENU(popupmenu, EDIT_CLIENT, self.Edit)
				
			if self.localsettings.deleteclients == 1:
				
				deleteclient = wx.MenuItem(popupmenu, DELETE_CLIENT, self.t("deletelabel"))
				deleteclient.SetBitmap(wx.Bitmap("icons/delete.png"))
				popupmenu.AppendItem(deleteclient)
				wx.EVT_MENU(popupmenu, DELETE_CLIENT, self.Delete)
			
			if self.localsettings.changelog == 1:
				
				changelog = wx.MenuItem(popupmenu, CLIENT_CHANGELOG, self.t("changelog"))
				changelog.SetBitmap(wx.Bitmap("icons/log.png"))
				popupmenu.AppendItem(changelog)
				wx.EVT_MENU(popupmenu, CLIENT_CHANGELOG, self.ChangeLog)
			
			self.PopupMenu(popupmenu)
	
	def ChangeLog(self, ID=False):
		
		listboxid = self.listctrl.GetFocusedItem()
		clientid = self.listctrl.GetItemData(listboxid)
		
		action = "SELECT ClientTitle, ClientForenames, ClientSurname, ChangeLog FROM client WHERE ID = " + str(clientid)
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		title = results[0][0]
		forenames = results[0][1]
		surname = results[0][2]
		changelog = results[0][3]
		
		miscmethods.ShowChangeLog(title + " " + forenames + " " + surname, changelog, self.localsettings.dbconnection)
	
	def Edit(self, ID):
		
		listboxid = self.listctrl.GetFocusedItem()
		clientid = self.listctrl.GetItemData(listboxid)
		
		notebook = self.parent.notebook
		
		clientdata = clientmethods.ClientSettings(self.localsettings, clientid)
		clientpanel = clientmethods.ClientPanel(notebook, clientdata)
		wx.CallAfter(notebook.AddPage, clientpanel)
	
	def Delete(self, ID):
		
		listboxid = self.listctrl.GetFocusedItem()
		clientid = self.listctrl.GetItemData(listboxid)
		
		action = "SELECT * FROM animal WHERE animal.OwnerID = " + str(clientid)
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		if len(results) == 0:
			
			confirm = miscmethods.ConfirmMessage(self.t("medicationconfirmdeletemessage"))
			
			if confirm == True:
				
				action = "DELETE FROM client WHERE client.ID = " + str(clientid)
				db.SendSQL(action, self.localsettings.dbconnection)
				
				self.parent.GetParent().Search()
				
			
		else:
			
			miscmethods.ShowMessage("You must delete this clients animals first!")
	
	def RefreshList(self, results):
		
		self.listctrl.RefreshList(results)

class AnimalSearchPanel(wx.Panel, listmix.ColumnSorterMixin):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, parent, localsettings):
		
		self.localsettings = localsettings
		self.parent = parent
		
		wx.Panel.__init__(self, parent)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		topsizer.Add(wx.StaticText(self, -1, self.t("clientanimalslabel")), 0, wx.ALIGN_CENTER)
		
		self.listctrl = AnimalListCtrl(self, self.localsettings)
		customwidgets.ListCtrlWrapper.RefreshList(self.listctrl)
		topsizer.Add(self.listctrl, 1, wx.EXPAND)
		
		self.listctrl.listctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.Edit)
		self.listctrl.listctrl.Bind(wx.EVT_RIGHT_DOWN, self.AnimalPopupMenu)
		
		self.totallabel = wx.StaticText(self, -1, self.t("totallabel") + ": 0")
		topsizer.Add(self.totallabel, 0, wx.ALIGN_LEFT)
		
		self.SetSizer(topsizer)
	
	def AnimalPopupMenu(self, ID):
		
		if self.listctrl.listctrl.GetSelectedItemCount() > 0:
			
			popupmenu = wx.Menu()
			
			if self.localsettings.editclients == 1:
				
				editanimal = wx.MenuItem(popupmenu, EDIT_ANIMAL, self.t("editlabel"))
				editanimal.SetBitmap(wx.Bitmap("icons/edit.png"))
				popupmenu.AppendItem(editanimal)
				wx.EVT_MENU(popupmenu, EDIT_ANIMAL, self.Edit)
				
			if self.localsettings.deleteanimals == 1:
				
				deleteanimal = wx.MenuItem(popupmenu, DELETE_ANIMAL, self.t("deletelabel"))
				deleteanimal.SetBitmap(wx.Bitmap("icons/delete.png"))
				popupmenu.AppendItem(deleteanimal)
				wx.EVT_MENU(popupmenu, DELETE_ANIMAL, self.Delete)
			
			if self.localsettings.changelog == 1:
				
				changelog = wx.MenuItem(popupmenu, ANIMAL_CHANGELOG, self.t("changelog"))
				changelog.SetBitmap(wx.Bitmap("icons/log.png"))
				popupmenu.AppendItem(changelog)
				wx.EVT_MENU(popupmenu, ANIMAL_CHANGELOG, self.ChangeLog)
			
			self.PopupMenu(popupmenu)
	
	def Edit(self, ID):
		
		listboxid = self.listctrl.GetFocusedItem()
		animalid = self.listctrl.GetItemData(listboxid)
		
		notebook = self.parent.notebook
		
		animaldata = animalmethods.AnimalSettings(self.localsettings, False, animalid)
		animalpanel = animalmethods.AnimalPanel(notebook, animaldata)
		wx.CallAfter(notebook.AddPage, animalpanel)
	
	def Delete(self, ID):
		
		listboxid = self.listctrl.GetFocusedItem()
		animalid = self.listctrl.GetItemData(listboxid)
		
		if miscmethods.ConfirmMessage(self.t("medicationconfirmdeletemessage")) == True:
			
			action = "DELETE FROM animal WHERE ID = " + str(animalid)
			db.SendSQL(action, self.localsettings.dbconnection)
			action = "DELETE FROM appointment WHERE AnimalID = " + str(animalid)
			db.SendSQL(action, self.localsettings.dbconnection)
			
			self.parent.GetParent().Search()
	
	def ChangeLog(self, ID=False):
		
		listboxid = self.listctrl.GetFocusedItem()
		animalid = self.listctrl.GetItemData(listboxid)
		
		action = "SELECT animal.Name, client.ClientSurname, animal.ChangeLog FROM animal INNER JOIN client ON animal.OwnerID = client.ID WHERE animal.ID = " + str(animalid)
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		animalname = results[0][0]
		surname = results[0][1]
		changelog = results[0][2]
		
		miscmethods.ShowChangeLog(animalname + " " + surname, changelog, self.localsettings.dbconnection)
	
	def GetListCtrl(self):# Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
		
        	return self.listctrl
	
	def RefreshList(self, results):
		
		#self.itemDataMap = {}
		
		#self.listctrl.ClearAll()
		
		#if len(results) < 1001:
			
			#self.listctrl.InsertColumn(0,self.t("namelabel"))
			#self.listctrl.InsertColumn(1,self.t("animalsexlabel"))
			#self.listctrl.InsertColumn(2,self.t("animalspecieslabel"))
			#self.listctrl.InsertColumn(3,self.t("animalbreedlabel"))
			#self.listctrl.InsertColumn(4,self.t("agelabel"))
			#self.listctrl.InsertColumn(5,self.t("animalcolourlabel"))
			#self.listctrl.InsertColumn(6,self.t("asmreflabel"))
			
			#count = 0
			
			#for a in results:
				
				#age = miscmethods.GetAgeFromDOB(a[7], self.localsettings)
				
				##ID, OwnerID, Name, Sex, Species, Breed, Colour, DOB, Comments, Neutered, ChipNo
				
				#self.itemDataMap[a[0]] = ( a[2], a[3], a[4], a[5], age, a[6], a[15] )
				
				#self.listctrl.InsertStringItem(count, a[2])
				
				#sex = miscmethods.GetSex(self.localsettings, a[3])
				
				#self.listctrl.SetStringItem(count, 1, sex)
				#self.listctrl.SetStringItem(count, 2, a[4])
				#self.listctrl.SetStringItem(count, 3, a[5])
				#self.listctrl.SetStringItem(count, 4, age)
				#self.listctrl.SetStringItem(count, 5, a[6])
				
				#self.listctrl.SetStringItem(count, 6, a[15])
				
				#if a[12] == 1:
					
					#self.listctrl.SetItemImage(count, 2)
					
				#elif a[15] != "":
					
					#self.listctrl.SetItemImage(count, 0)
					
				#else:
					
					#self.listctrl.SetItemImage(count, 1)
				
				#self.listctrl.SetItemData(count, a[0])
				
				#count = count + 1
				
			#if len(results) == 0:
				
				#self.listctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
				#self.listctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
				#self.listctrl.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
				#self.listctrl.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)
				#self.listctrl.SetColumnWidth(4, wx.LIST_AUTOSIZE_USEHEADER)
				#self.listctrl.SetColumnWidth(5, wx.LIST_AUTOSIZE_USEHEADER)
				#self.listctrl.SetColumnWidth(6, wx.LIST_AUTOSIZE_USEHEADER)
			
			#else:
				
				#self.listctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
				#columnwidth = self.listctrl.GetColumnWidth(0)
				#self.listctrl.SetColumnWidth(0, columnwidth + 30)
				#self.listctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE)
				#self.listctrl.SetColumnWidth(2, wx.LIST_AUTOSIZE)
				#self.listctrl.SetColumnWidth(3, wx.LIST_AUTOSIZE)
				#self.listctrl.SetColumnWidth(4, wx.LIST_AUTOSIZE)
				#self.listctrl.SetColumnWidth(5, wx.LIST_AUTOSIZE)
				#self.listctrl.SetColumnWidth(6, wx.LIST_AUTOSIZE)
		
		self.listctrl.RefreshList(results)
		
		self.totallabel.SetLabel(miscmethods.NoWrap(self.t("totallabel") + ": " + str(len(results))))

#class OldClientSearchPanel(wx.Panel):
	
	#def t(self, field, idx = 0):
		
		#return self.localsettings.t(field,idx)
	
	#def GetButtonLabel(self, field, index):
		
		#return self.localsettings.t(field,idx)[index]
	
	#def __init__(self, notebook, localsettings):
		
		#busy = wx.BusyCursor()
		
		#self.localsettings = localsettings
		#self.notebook = notebook
		
		#wx.Panel.__init__(self, notebook)
		
		#rawpagetitle = self.t("clientsearchpagetitle")
		
		#pagetitle = miscmethods.GetPageTitle(notebook, rawpagetitle)
		#self.pagetitle = pagetitle
		
		#topsizer = wx.BoxSizer(wx.VERTICAL)
		
		#horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		#mainsizer = wx.BoxSizer(wx.VERTICAL)
		
		#titlelabel = wx.StaticText(self, -1, self.t("clientsearchstitlelabel"))
		#font = titlelabel.GetFont()
		#font.SetPointSize(font.GetPointSize() + 2)
		#titlelabel.SetFont(font)
		#mainsizer.Add(titlelabel, 0, wx.ALIGN_CENTER)
		
		#searchtoolssizer = wx.FlexGridSizer(rows=3,cols=4)
		#searchtoolssizer.AddGrowableCol(1)
		
		#namelabel = wx.StaticText(self, -1, self.t("namelabel") + ": ")
		#searchtoolssizer.Add(namelabel, 0, wx.ALIGN_RIGHT)
		
		#self.nameinput = wx.TextCtrl(self, -1)
		#searchtoolssizer.Add(self.nameinput, 1, wx.EXPAND)
		
		#phonelabel = wx.StaticText(self, -1, self.t("clientsearchphonelabel") + ": ")
		#searchtoolssizer.Add(phonelabel, 0, wx.ALIGN_RIGHT)
		
		#self.phoneinput = wx.TextCtrl(self, -1, size=(150,-1))
		#searchtoolssizer.Add(self.phoneinput, 1, wx.EXPAND)
		
		#addresslabel = wx.StaticText(self, -1, self.t("clientsearchaddresslabel") + ": ")
		#searchtoolssizer.Add(addresslabel, 0, wx.ALIGN_RIGHT)
		
		#self.addressinput = wx.TextCtrl(self, -1)
		#searchtoolssizer.Add(self.addressinput, 1, wx.EXPAND)
		
		#postcodelabel = wx.StaticText(self, -1, self.t("clientsearchpostcodelabel") + ": ")
		#searchtoolssizer.Add(postcodelabel, 0, wx.ALIGN_RIGHT)
		
		#self.postcodeinput = wx.TextCtrl(self, -1)
		#searchtoolssizer.Add(self.postcodeinput, 1, wx.EXPAND)
		
		#emaillabel = wx.StaticText(self, -1, self.t("clientsearchemaillabel") + ": ")
		#searchtoolssizer.Add(emaillabel, 0, wx.ALIGN_RIGHT)
		
		#self.emailinput = wx.TextCtrl(self, -1)
		#searchtoolssizer.Add(self.emailinput, 1, wx.EXPAND)
		
		#searchbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		#clearbutton = wx.Button(self, -1, self.GetButtonLabel("clientsearchclearbutton", 0))
		#font = clearbutton.GetFont()
		#font.SetPointSize(font.GetPointSize() + 2)
		#clearbutton.SetFont(font)
		#clearbutton.SetForegroundColour("red")
		
		#clearbutton.SetToolTipString(self.GetButtonLabel("clientsearchclearbutton", 1))
		#clearbutton.Bind(wx.EVT_BUTTON, self.Clear)
		#searchbuttonsizer.Add(clearbutton, 1, wx.EXPAND)
		
		#searchbutton = wx.Button(self, -1, self.GetButtonLabel("clientsearchsearchbutton", 0))
		#font = searchbutton.GetFont()
		#font.SetPointSize(font.GetPointSize() + 3)
		#searchbutton.SetFont(font)
		#searchbutton.SetForegroundColour("#03bc21")
		
		#searchbutton.SetToolTipString(self.GetButtonLabel("clientsearchsearchbutton", 1))
		#searchbutton.Bind(wx.EVT_BUTTON, self.Search)
		#searchbuttonsizer.Add(searchbutton, 1, wx.EXPAND)
		
		#openbitmap = wx.Bitmap("icons/edit.png")
		
		#openbutton = wx.BitmapButton(self, -1, openbitmap)
		#openbutton.SetToolTipString(self.t("clientsearcheditclienttooltip"))
		#openbutton.Disable()
		#openbutton.Bind(wx.EVT_BUTTON, self.Edit)
		
		#deletebitmap = wx.Bitmap("icons/delete.png")
		
		#deletebutton = wx.BitmapButton(self, -1, deletebitmap)
		#deletebutton.SetToolTipString(self.t("clientsearchdeleteclienttooltip"))
		#deletebutton.Bind(wx.EVT_BUTTON, self.Delete)
		#deletebutton.Disable()
		
		#searchlabel = wx.StaticText(self, -1, "")
		#searchtoolssizer.Add(searchlabel, 0, wx.ALIGN_RIGHT)
		#searchtoolssizer.Add(searchbuttonsizer, 1, wx.EXPAND)
		
		#searchbuttonssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		#searchbuttonssizer.Add(openbutton)
		#searchbuttonssizer.Add(deletebutton)
		
		##Creating the listbox
		#self.listbox = FindClientListbox(self, localsettings)
		#self.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.Edit)
		#if localsettings.changelog == 1:
			#self.listbox.Bind(wx.EVT_RIGHT_DOWN, self.ClientChangeLog)
		#self.listbox.Bind(wx.EVT_LISTBOX, self.ClientSelected)
		
		
		##Adding components to the mainsizer
		
		#mainsizer.Add(searchtoolssizer, 0, wx.EXPAND)
		
		#mainspacer = wx.StaticText(self, -1, "", size=(-1,10))
		#mainsizer.Add(mainspacer, 0, wx.EXPAND)
		
		#mainsizer.Add(searchbuttonssizer)
		
		#mainsizer.Add(self.listbox, 1, wx.EXPAND)
		
		#self.totallabel = wx.StaticText(self, -1, self.t("totallabel") + ": 0")
		#mainsizer.Add(self.totallabel, 0, wx.ALIGN_LEFT)
		
		#horizontalsizer.Add(mainsizer, 2, wx.EXPAND)
		
		#animalspanel = AnimalSearchPanel(self, localsettings)
		
		#horizontalspacer = wx.StaticText(self, -1, "", size=(10,-1))
		#horizontalsizer.Add(horizontalspacer, 0, wx.EXPAND)
		
		#horizontalsizer.Add(animalspanel, 1, wx.EXPAND)
		
		#topsizer.Add(horizontalsizer, 1, wx.EXPAND)
		
		#self.SetSizer(topsizer)
		
		#self.deletebutton = deletebutton
		#self.openbutton = openbutton
		#self.animalspanel = animalspanel
		
		#self.ApplyShortcuts()
		
		#del busy
	
	#def ApplyShortcuts(self):
		
		#for a in self.GetChildren():
			
			#a.Bind(wx.EVT_CHAR, self.KeyPressed)
			
			#for b in a.GetChildren():
				
				#b.Bind(wx.EVT_CHAR, self.KeyPressed)
	
	#def KeyPressed(self, ID):
		
		#keycode = ID.GetKeyCode()
		
		##print str(keycode)
		
		#if keycode == 13:
			
			#self.Search()
			
		#elif keycode == 15 and self.listbox.GetSelection() > -1:
			
			#self.Edit()
		
		#ID.Skip()
	
	#def ClientChangeLog(self, ID=False):
		
		#listboxid = self.listbox.GetSelection()
		#if listboxid > -1:
			#title = self.listbox.htmllist[listboxid][1]
			#forenames = self.listbox.htmllist[listboxid][2]
			#surname = self.listbox.htmllist[listboxid][3]
			#changelog = self.listbox.htmllist[listboxid][11]
			
			#miscmethods.ShowChangeLog(title + " " + forenames + " " + surname, changelog, self.localsettings.dbconnection)
			
	
	#def Clear(self, ID):
		
		#self.nameinput.Clear()
		#self.addressinput.Clear()
		#self.phoneinput.Clear()
		#self.postcodeinput.Clear()
		#self.emailinput.Clear()
		
		#self.animalspanel.nameentry.Clear()
		#self.animalspanel.sexentry.Clear()
		#self.animalspanel.speciesentry.Clear()
		#self.animalspanel.breedentry.Clear()
		#self.animalspanel.chipentry.Clear()
		#self.animalspanel.commentsentry.Clear()
	
	#def ClientSelected(self, ID=False):
		
		#if self.localsettings.deleteclients == 1:
			#self.deletebutton.Enable()
		#self.openbutton.Enable()
	
	#def Search(self, ID=False):
		
		#busy = wx.BusyCursor()
		
		#self.listbox.RefreshList()
		#self.animalspanel.animallistbox.RefreshList()
		
		#del busy
	
	#def Delete(self, ID):
		
		#listboxid = self.listbox.GetSelection()
		#clientid =  self.listbox.htmllist[listboxid][0]
		
		#action = "SELECT * FROM animal WHERE animal.OwnerID = " + str(clientid)
		#results = db.SendSQL(action, self.localsettings.dbconnection)
		
		#if len(results) == 0:
			#confirm = miscmethods.ConfirmMessage("Really Delete Client?")
			#if confirm == True:
				#action = "DELETE FROM client WHERE client.ID = " + str(clientid)
				#db.SendSQL(action, self.localsettings.dbconnection)
				#self.Search()
		#else:
			#miscmethods.ShowMessage("You must delete this clients animals first!")
	
	#def Edit(self, ID=False):
		
		#listboxid = self.listbox.GetSelection()
		#clientid =  self.listbox.htmllist[listboxid][0]
		#clientdata = clientmethods.ClientSettings(self.localsettings, clientid)
		#clientpanel = clientmethods.ClientPanel(self.notebook, clientdata)
		#self.notebook.AddPage(clientpanel)

#class AnimalSearchPanel(wx.Panel):
	
	#def t(self, field, idx = 0):
		
		#return self.localsettings.t(field,idx)
	
	#def GetButtonLabel(self, field, index):
		
		#return self.localsettings.t(field,idx)[index]
	
	#def __init__(self, parent, localsettings):
		
		#self.localsettings = localsettings
		
		#wx.Panel.__init__(self, parent)
		
		#topsizer = wx.BoxSizer(wx.VERTICAL)
		
		#titlelabel = wx.StaticText(self, -1, self.t("clientsearchanimallabel"))
		#font = titlelabel.GetFont()
		#font.SetPointSize(font.GetPointSize() + 2)
		#titlelabel.SetFont(font)
		#topsizer.Add(titlelabel, 0, wx.ALIGN_CENTER)
		
		#entrysizer = wx.FlexGridSizer(rows=3, cols=4)
		
		#entrysizer.AddGrowableCol(1)
		#entrysizer.AddGrowableCol(3)
		
		#namelabel = wx.StaticText(self, -1, self.t("clientsearchanimalnamelabel") + ": ")
		#entrysizer.Add(namelabel, 0, wx.ALIGN_RIGHT)
		#nameentry = wx.TextCtrl(self, -1, "")
		#entrysizer.Add(nameentry, 1, wx.EXPAND)
		
		#sexlabel = wx.StaticText(self, -1, self.t("clientsearchanimalsexlabel") + ": ")
		#entrysizer.Add(sexlabel, 0, wx.ALIGN_RIGHT)
		#sexentry = wx.TextCtrl(self, -1, "")
		#entrysizer.Add(sexentry, 1, wx.EXPAND)
		
		#specieslabel = wx.StaticText(self, -1, self.t("clientsearchanimalspecieslabel") + ": ")
		#entrysizer.Add(specieslabel, 0, wx.ALIGN_RIGHT)
		#speciesentry = wx.TextCtrl(self, -1, "")
		#entrysizer.Add(speciesentry, 1, wx.EXPAND)
		
		#breedlabel = wx.StaticText(self, -1, self.t("clientsearchanimalbreedlabel") + ": ")
		#entrysizer.Add(breedlabel, 0, wx.ALIGN_RIGHT)
		#breedentry = wx.TextCtrl(self, -1, "")
		#entrysizer.Add(breedentry, 1, wx.EXPAND)
		
		#chiplabel = wx.StaticText(self, -1, self.t("clientsearchanimalchipnolabel") + ": ")
		#entrysizer.Add(chiplabel, 0, wx.ALIGN_RIGHT)
		#chipentry = wx.TextCtrl(self, -1, "")
		#entrysizer.Add(chipentry, 1, wx.EXPAND)
		
		#commentslabel = wx.StaticText(self, -1, self.t("clientsearchanimalcommentslabel") + ": ")
		#entrysizer.Add(commentslabel, 0, wx.ALIGN_RIGHT)
		#commentsentry = wx.TextCtrl(self, -1, "")
		#entrysizer.Add(commentsentry, 1, wx.EXPAND)
		
		#topsizer.Add(entrysizer, 0, wx.EXPAND)
		
		#entryspacer = wx.StaticText(self, -1, "", size=(-1,10))
		#topsizer.Add(entryspacer, 0, wx.EXPAND)
		
		#buttonssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		#editbitmap = wx.Bitmap("icons/edit.bmp")
		#editbutton = wx.BitmapButton(self, -1, editbitmap)
		#editbutton.Bind(wx.EVT_BUTTON, self.OpenAnimalRecord)
		#editbutton.Disable()
		#editbutton.SetToolTipString(self.t("clientsearcheditanimaltooltip"))
		#buttonssizer.Add(editbutton, 0, wx.EXPAND)
		
		#deletebitmap = wx.Bitmap("icons/delete.bmp")
		#deletebutton = wx.BitmapButton(self, -1, deletebitmap)
		#deletebutton.Bind(wx.EVT_BUTTON, self.DeleteAnimalRecord)
		#deletebutton.Disable()
		#deletebutton.SetToolTipString(self.t("clientsearchdeleteanimaltooltip"))
		#buttonssizer.Add(deletebutton, 0, wx.EXPAND)
		
		#buttonssizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		#includedeceasedtickbox = wx.CheckBox(self, -1, self.t("includedeceasedlabel"))
		#includedeceasedtickbox.SetValue(True)
		#buttonssizer.Add(includedeceasedtickbox, 0, wx.EXPAND)
		
		#topsizer.Add(buttonssizer, 0, wx.EXPAND)
		
		#animallistbox = FindAnimalsListbox(self, localsettings)
		#animallistbox.Bind(wx.EVT_LISTBOX, self.AnimalSelected)
		#if localsettings.editanimals == 1:
			#animallistbox.Bind(wx.EVT_LISTBOX_DCLICK, self.OpenAnimalRecord)
		#if localsettings.changelog == 1:
			#animallistbox.Bind(wx.EVT_RIGHT_DOWN, self.AnimalChangeLog)
		#topsizer.Add(animallistbox, 1, wx.EXPAND)
		
		#totallabel = wx.StaticText(self, -1, self.t("totallabel") + " 0")
		#topsizer.Add(totallabel, 0, wx.ALIGN_LEFT)
		
		#self.SetSizer(topsizer)
		
		#self.parent = parent
		#self.nameentry = nameentry
		#self.sexentry = sexentry
		#self.speciesentry = speciesentry
		#self.breedentry = breedentry
		#self.chipentry = chipentry
		#self.commentsentry = commentsentry
		#self.animallistbox = animallistbox
		#self.totallabel = totallabel
		#self.editbutton = editbutton
		#self.deletebutton = deletebutton
		#self.includedeceasedtickbox = includedeceasedtickbox
	
	#def AnimalChangeLog(self, ID=False):
		
		#listboxid = self.animallistbox.GetSelection()
		#if listboxid > -1:
			#animal = self.animallistbox.htmllist[listboxid]
			
			#name = animal[2]
			#changelog = animal[11]
			
			#miscmethods.ShowChangeLog(name, changelog, self.localsettings.dbconnection)
			
	
	#def AnimalSelected(self, ID):
		
		#if self.localsettings.editanimals == 1:
			#self.editbutton.Enable()
		#if self.localsettings.deleteanimals == 1:
			#self.deletebutton.Enable()
	
	#def OpenAnimalRecord(self, ID):
		
		#listboxid = self.animallistbox.GetSelection()
		#animalid = self.animallistbox.htmllist[listboxid][0]
		#animaldata = animalmethods.AnimalSettings(self.localsettings, False, animalid)
		
		#notebook = self.parent.GetGrandParent()
		
		#animalpanel = animalmethods.AnimalPanel(notebook, animaldata)
		#notebook.AddPage(animalpanel)
	
	#def DeleteAnimalRecord(self, ID):
		
		#listboxid = self.animallistbox.GetSelection()
		#animalid = self.animallistbox.htmllist[listboxid][0]
		
		#confirm = miscmethods.ConfirmMessage("Really delete animal?")
		#if confirm == True:
			
			#action = "DELETE FROM animal WHERE ID = " + str(animalid)
			#db.SendSQL(action, self.localsettings.dbconnection)
			#action = "DELETE FROM appointment WHERE AnimalID = " + str(animalid)
			#db.SendSQL(action, self.localsettings.dbconnection)
			
			#self.parent.Search()

#class FindClientListbox(wx.HtmlListBox):
	
	#def __init__(self, parent, localsettings):
		
		#wx.HtmlListBox.__init__(self, parent)
		
		#self.parent = parent
		#self.localsettings = localsettings
		
		#self.SetSelection(-1)
		#self.htmllist = []
		
		#self.SetItemCount(0)
	
	#def OnGetItem(self, n):
		
		#if len(self.htmllist) != 0:
			
			#title = self.htmllist[n][1]
			#forenames = self.htmllist[n][2]
			#surname = self.htmllist[n][3]
			#address = self.htmllist[n][4].replace("\n", ", ")
			#postcode = self.htmllist[n][5]
			
			#output = "<font color=blue>" + title + " " + forenames + " " + surname + "</font> - <font color=red>" + address + ". " + postcode + "</font>"
			
			#return output
			
	#def RefreshList(self):
		
		#animalpanel = self.parent.animalspanel
		
		#name = animalpanel.nameentry.GetValue()
		#sex = animalpanel.sexentry.GetValue()
		#species = animalpanel.speciesentry.GetValue()
		#breed = animalpanel.breedentry.GetValue()
		#chip = animalpanel.chipentry.GetValue()
		#comments = animalpanel.commentsentry.GetValue()
		
		#animalsql = ""
		
		#if name != "":
			#animalsql = animalsql + "animal.Name LIKE \"%" + name + "%\""
		#if sex != "":
			#if animalsql != "":
				#animalsql = animalsql + " AND "
			
			#animalsql = animalsql + "animal.Sex = \"" + sex + "\""
		#if species != "":
			#if animalsql != "":
				#animalsql = animalsql + " AND "
			
			#animalsql = animalsql + "animal.Species LIKE \"%" + species + "%\""
		#if breed != "":
			#if animalsql != "":
				#animalsql = animalsql + " AND "
			
			#animalsql = animalsql + "animal.Breed LIKE \"%" + breed + "%\""
		#if chip != "":
			#if animalsql != "":
				#animalsql = animalsql + " AND "
			
			#animalsql = animalsql + "animal.ChipNo LIKE \"%" + chip + "%\""
		#if comments != "":
			#if animalsql != "":
				#animalsql = animalsql + " AND "
			
			#animalsql = animalsql + "animal.Comments LIKE \"%" + comments + "%\""
###		if animalpanel.includedeceasedtickbox.GetValue() == False:
###			if animalsql != "":
###				animalsql = animalsql + " AND "
###			
###			animalsql = animalsql + "animal.IsDeceased = 0"
		
		
		#clientpanel = self.parent
		
		#clientname = clientpanel.nameinput.GetValue()
		#clientphone = clientpanel.phoneinput.GetValue()
		#clientaddress = clientpanel.addressinput.GetValue()
		#clientpostcode = clientpanel.postcodeinput.GetValue()
		#clientemail = clientpanel.emailinput.GetValue()
		
		#clientsql = ""
		
		#if clientname != "":
			#clientsql = clientsql + "CONCAT(client.ClientTitle, \" \", client.ClientForenames, \" \", client.ClientSurName) LIKE \"%" + clientname + "%\""
		#if clientphone != "":
			#if clientsql != "":
				#clientsql = clientsql + " AND "
			
			#clientsql = clientsql + "( client.ClientHomeTelephone LIKE \"%" + clientphone + "%\" OR client.ClientMobileTelephone LIKE \"%" + clientphone + "%\" OR client.ClientWorkTelephone LIKE \"%" + clientphone + "%\" )"
		#if clientaddress != "":
			#if clientsql != "":
				#clientsql = clientsql + " AND "
			
			#clientsql = clientsql + "client.ClientAddress LIKE \"%" + clientaddress + "%\""
		#if clientpostcode != "":
			#if clientsql != "":
				#clientsql = clientsql + " AND "
			
			#clientsql = clientsql + "client.ClientPostcode LIKE \"%" + clientpostcode + "%\""
		#if clientemail != "":
			#if clientsql != "":
				#clientsql = clientsql + " AND "
			
			#clientsql = clientsql + "client.ClientEmailAddress LIKE \"%" + clientemail + "%\""
		
		
		#if clientsql == "" and animalsql == "":
			
			#action = "SELECT * FROM client"
			
		#elif animalsql == "":
			
			#action = "SELECT * FROM client WHERE " + clientsql
		
		#elif clientsql == "":
			
			#action = "SELECT * FROM client INNER JOIN animal ON animal.OwnerID = client.ID WHERE " + animalsql
			
		#else:
			
			#action = "SELECT * FROM client INNER JOIN animal ON animal.OwnerID = client.ID WHERE " + animalsql + " AND " + clientsql
		
		#results = db.SendSQL(action, self.localsettings.dbconnection)
		
		
		
		#totallabel = self.parent.GetLabel("totallabel")
		
		#self.parent.totallabel.SetLabel(totallabel + ": " + str(len(results)))
		
		#self.Hide()
		#self.htmllist = results
		#self.SetItemCount(len(self.htmllist))
		
		#animalpanel.editbutton.Disable()
		#animalpanel.deletebutton.Disable()
		
		#if len(self.htmllist) == 0:
			
			#self.SetSelection(-1)
			#self.Disable()
			#clientpanel.openbutton.Disable()
			#clientpanel.deletebutton.Disable()
			
		#else:
			
			#self.SetSelection(0)
			#clientpanel.ClientSelected()
			#self.Enable()
		
		#self.Show()

#class FindAnimalsListbox(wx.HtmlListBox):
	
	#def __init__(self, parent, localsettings):
		
		#wx.HtmlListBox.__init__(self, parent)
		
		#self.parent = parent
		#self.localsettings = localsettings
		
		#self.SetSelection(-1)
		#self.htmllist = []
		
		#self.SetItemCount(0)
	
	#def OnGetItem(self, n):
		
		#if len(self.htmllist) != 0:
			
			#name = self.htmllist[n][2]
			#sex = self.htmllist[n][3]
			#species = self.htmllist[n][4]
			#deceased = self.htmllist[n][12]
			#asmref = self.htmllist[n][15]
			
			#if deceased == 1:
				#sexcolour = "gray"
			#elif sex == "Male":
				#sexcolour = "blue"
			#elif sex == "Female":
				#sexcolour = "red"
			#else:
				#sexcolour = "black"
			
			#breed = self.htmllist[n][5]
			#colour = self.htmllist[n][6]
			
			#if asmref == "":
				
				#output = "<font color=" + sexcolour + ">" + name + " (" + species + ", " + breed + ", " + colour + ")</font>"
				
			#else:
				
				#output = "<img src=icons/asm.png><font color=" + sexcolour + ">&nbsp;" + name + " (" + species + ", " + breed + ", " + colour + ")</font>"
			
			#return output
	
	#def RefreshList(self):
		
		#self.SetSelection(-1)
		
		#animalpanel = self.parent
		
		#name = animalpanel.nameentry.GetValue()
		#sex = animalpanel.sexentry.GetValue()
		#species = animalpanel.speciesentry.GetValue()
		#breed = animalpanel.breedentry.GetValue()
		#chip = animalpanel.chipentry.GetValue()
		#comments = animalpanel.commentsentry.GetValue()
		
		#animalsql = ""
		
		#if name != "":
			#animalsql = animalsql + "animal.Name LIKE \"%" + name + "%\""
		#if sex != "":
			#if animalsql != "":
				#animalsql = animalsql + " AND "
			
			#animalsql = animalsql + "animal.Sex = \"" + sex + "\""
		#if species != "":
			#if animalsql != "":
				#animalsql = animalsql + " AND "
			
			#animalsql = animalsql + "animal.Species LIKE \"%" + species + "%\""
		#if breed != "":
			#if animalsql != "":
				#animalsql = animalsql + " AND "
			
			#animalsql = animalsql + "animal.Breed LIKE \"%" + breed + "%\""
		#if chip != "":
			#if animalsql != "":
				#animalsql = animalsql + " AND "
			
			#animalsql = animalsql + "animal.ChipNo LIKE \"%" + chip + "%\""
		#if comments != "":
			#if animalsql != "":
				#animalsql = animalsql + " AND "
			
			#animalsql = animalsql + "animal.Comments LIKE \"%" + comments + "%\""
		#if animalpanel.includedeceasedtickbox.GetValue() == False:
			#if animalsql != "":
				#animalsql = animalsql + " AND "
			
			#animalsql = animalsql + "animal.IsDeceased = 0"
		
		
		#clientpanel = self.parent.GetParent()
		
		#clientname = clientpanel.nameinput.GetValue()
		#clientphone = clientpanel.phoneinput.GetValue()
		#clientaddress = clientpanel.addressinput.GetValue()
		#clientpostcode = clientpanel.postcodeinput.GetValue()
		#clientemail = clientpanel.emailinput.GetValue()
		
		#clientsql = ""
		
		#if clientname != "":
			#clientsql = clientsql + "CONCAT(client.ClientTitle, \" \", client.ClientForenames, \" \", client.ClientSurName) LIKE \"%" + clientname + "%\""
		#if clientphone != "":
			#if clientsql != "":
				#clientsql = clientsql + " AND "
			
			#clientsql = clientsql + "( client.ClientHomeTelephone LIKE \"%" + clientphone + "%\" OR client.ClientMobileTelephone LIKE \"%" + clientphone + "%\" OR client.ClientWorkTelephone LIKE \"%" + clientphone + "%\" )"
		#if clientaddress != "":
			#if clientsql != "":
				#clientsql = clientsql + " AND "
			
			#clientsql = clientsql + "client.ClientAddress LIKE \"%" + clientaddress + "%\""
		#if clientpostcode != "":
			#if clientsql != "":
				#clientsql = clientsql + " AND "
			
			#clientsql = clientsql + "client.ClientPostcode LIKE \"%" + clientpostcode + "%\""
		#if clientemail != "":
			#if clientsql != "":
				#clientsql = clientsql + " AND "
			
			#clientsql = clientsql + "client.ClientEmailAddress LIKE \"%" + clientemail + "%\""
		
		#if clientsql == "" and animalsql == "":
			
			#action = "SELECT * FROM animal"
			
		#elif clientsql == "":
			
			#action = "SELECT * FROM animal WHERE " + animalsql
		
		#elif animalsql == "":
			
			#action = "SELECT * FROM animal INNER JOIN client ON animal.OwnerID = client.ID WHERE " + clientsql
			
		#else:
			
			#action = "SELECT * FROM animal INNER JOIN client ON animal.OwnerID = client.ID WHERE " + animalsql + " AND " + clientsql
		
		#results = db.SendSQL(action, self.localsettings.dbconnection)
		
		
		
		#totallabel = self.parent.GetLabel("totallabel")
		
		#self.parent.totallabel.SetLabel(totallabel + ": " + str(len(results)))
		
		
		#self.Hide()
		#self.htmllist = results
		#self.SetItemCount(len(self.htmllist))
		##self.Refresh()
		
		
		#if len(self.htmllist) == 0:
			#self.Disable()
		#else:
			#self.Enable()
		
		#self.Show()

class AppointmentSearchPanel(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def GetButtonLabel(self, field, index):
		
		return self.localsettings.t(field,idx)[index]
	
	def __init__(self, notebook, localsettings):
		
		self.localsettings = localsettings
		self.notebook = notebook
		
		wx.Panel.__init__(self, notebook)
		
		rawpagetitle = self.t("appointmentsearchpagetitle")
		
		pagetitle = miscmethods.GetPageTitle(notebook, rawpagetitle)
		self.pagetitle = pagetitle
		self.pageimage = "icons/search.png"
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		searchpanel = wx.Panel(self, size=(200,-1))
		
		searchsizer = wx.BoxSizer(wx.VERTICAL)
		#searchsizer.AddGrowableCol(1)
		
		fromdatelabel = wx.StaticText(searchpanel, -1, self.t("fromlabel") + ": ")
		font = fromdatelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		fromdatelabel.SetFont(font)
		searchsizer.Add(fromdatelabel, 0, wx.ALIGN_LEFT)
		
		fromdateentry = customwidgets.DateCtrl(searchpanel, self.localsettings)
		fromdateentry.SetSize((-1,-1))
		searchsizer.Add(fromdateentry, 0, wx.EXPAND)
		
		todatelabel = wx.StaticText(searchpanel, -1, self.t("tolabel") + ": ")
		todatelabel.SetFont(font)
		searchsizer.Add(todatelabel, 0, wx.ALIGN_LEFT)
		
		todateentry = customwidgets.DateCtrl(searchpanel, self.localsettings)
		todateentry.SetSize((-1,-1))
		searchsizer.Add(todateentry, 0, wx.EXPAND)
		
		clientlabel = wx.StaticText(searchpanel, -1, self.t("clientsurnamelabel") + ": ")
		clientlabel.SetFont(font)
		searchsizer.Add(clientlabel, 0, wx.ALIGN_LEFT)
		
		cliententry = wx.TextCtrl(searchpanel, -1, "")
		searchsizer.Add(cliententry, 0, wx.EXPAND)
		
		animalnamelabel = wx.StaticText(searchpanel, -1, self.t("appointmentsearchanimalnamelabel") + ": ")
		animalnamelabel.SetFont(font)
		searchsizer.Add(animalnamelabel, 0, wx.ALIGN_LEFT)
		
		animalnameentry = wx.TextCtrl(searchpanel, -1, "")
		searchsizer.Add(animalnameentry, 0, wx.EXPAND)
		
		specieslabel = wx.StaticText(searchpanel, -1, self.t("animalspecieslabel") + ": ")
		specieslabel.SetFont(font)
		searchsizer.Add(specieslabel, 0, wx.ALIGN_LEFT)
		
		speciesentry = wx.TextCtrl(searchpanel, -1, "")
		searchsizer.Add(speciesentry, 0, wx.EXPAND)
		
		reasonlabel = wx.StaticText(searchpanel, -1,  self.t("reasonlabel") + ": ")
		reasonlabel.SetFont(font)
		searchsizer.Add(reasonlabel, 0, wx.ALIGN_LEFT)
		
		reasonentry = wx.TextCtrl(searchpanel, -1, "")
		searchsizer.Add(reasonentry, 0, wx.EXPAND)
		
		searchsizer.Add(wx.StaticText(searchpanel, -1, ""), 0, wx.EXPAND)
		
		searchbuttonssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		resetbutton = wx.Button(searchpanel, -1, self.t("resetlabel"))
		resetbutton.SetToolTipString(self.t("movementresetsearchentriestooltip"))
		resetbutton.SetBackgroundColour("red")
		resetbutton.SetForegroundColour("white")
		resetbutton.Bind(wx.EVT_BUTTON, self.Reset)
		searchbuttonssizer.Add(resetbutton, 1, wx.EXPAND)
		
		searchbutton = wx.Button(searchpanel, -1, self.t("searchlabel"))
		searchbutton.SetToolTipString(self.t("searchlabel"))
		searchbutton.SetBackgroundColour("green")
		searchbutton.SetForegroundColour("black")
		searchbuttonssizer.Add(searchbutton, 1, wx.EXPAND)
		
		searchsizer.Add(searchbuttonssizer, 0, wx.EXPAND)
		
		searchpanel.SetSizer(searchsizer)
		
		horizontalsizer.Add(searchpanel, 0, wx.EXPAND)
		
		horizontalspacer = wx.StaticText(self, -1, "", size=(50,-1))
		horizontalsizer.Add(horizontalspacer, 0, wx.EXPAND)
		
		listboxpanel = wx.Panel(self)
		listboxpanel.localsettings = self.localsettings
		
		listboxsizer = wx.BoxSizer(wx.VERTICAL)
		
		listbox = AppointmentSearchListbox(listboxpanel)
		listbox.SetToolTipString(self.t("doubleclicktoselecttooltip"))
		listbox.Bind(wx.EVT_LISTBOX, self.AppointmentSelected)
		listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EditAppointment)
		listboxsizer.Add(listbox, 1, wx.EXPAND)
		
		searchbutton.Bind(wx.EVT_BUTTON, listbox.RefreshList)
		
		totallabel = wx.StaticText(listboxpanel, -1, self.t("totallabel") + ": 0 ")
		listboxsizer.Add(totallabel, 0, wx.ALIGN_RIGHT)
		
		listboxpanel.SetSizer(listboxsizer)
		
		horizontalsizer.Add(listboxpanel, 3, wx.EXPAND)
		
		topsizer.Add(horizontalsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.listbox = listbox
		
		listboxpanel.totallabel = totallabel
		listboxpanel.listboxsizer = listboxsizer
		
		listboxpanel.fromdateentry = fromdateentry
		listboxpanel.todateentry = todateentry
		
		listboxpanel.cliententry = cliententry
		listboxpanel.animalnameentry = animalnameentry
		listboxpanel.speciesentry = speciesentry
		listboxpanel.reasonentry = reasonentry
		
		#self.editbutton = editbutton
		self.notebook = notebook
		
		self.listboxpanel = listboxpanel
	
	def Reset(self, ID):
		
		self.listboxpanel.fromdateentry.Clear()
		self.listboxpanel.todateentry.Clear()
		
		self.listboxpanel.cliententry.Clear()
		self.listboxpanel.animalnameentry.Clear()
		self.listboxpanel.speciesentry.Clear()
		self.listboxpanel.reasonentry.Clear()
	
	def AppointmentSelected(self, ID):
		
		#self.editbutton.Enable()
		pass
	
	def EditAppointment(self, ID):
		
		listboxid = self.listbox.GetSelection()
		appointmentid = self.listbox.htmllist[listboxid][0]
		
		appointmentdata = appointmentmethods.AppointmentSettings(self.localsettings, False, appointmentid)
		
		appointmentpanel = appointmentmethods.AppointmentPanel(self.notebook, appointmentdata)
		appointmentpanel.viewappointmentspanel = False
		self.notebook.AddPage(appointmentpanel)
		
		

class AppointmentSearchListbox(wx.HtmlListBox):
	
	def __init__(self, parent):
		
		wx.HtmlListBox.__init__(self, parent, -1)
		
		self.htmllist = []
		self.localsettings = parent.localsettings
		self.parent = parent
		self.SetItemCount(0)
	
	def OnGetItem(self, n):
		
		date = self.htmllist[n][1]
		date = miscmethods.GetDateFromSQLDate(date)
		date = miscmethods.FormatDate(date, self.localsettings)
		
		reason = self.htmllist[n][2]
		animalname = self.htmllist[n][3]
		species = self.htmllist[n][4]
		clientname = self.htmllist[n][5] + " " + self.htmllist[n][6] + " " + self.htmllist[n][7]
		
		output = "<table width=100% cellpadding=0 cellspacing=5><tr><td valign=top width=10%><font color=blue>" + date + "</font></td><td valign=top width=60%><font color=red>" + reason + "</font></td><td width=30% valign=top>Animal: <font color=blue>" + animalname + " (" + species + ")</font><br>Owner: <font color=red>" + clientname + "</font></td></tr></table>"
		
		return output
	
	def RefreshList(self, ID=False):
		
		busy = wx.BusyCursor()
		
		self.Hide()
		
		fromdate = self.parent.fromdateentry.GetValue()
		
		todate = self.parent.todateentry.GetValue()
		
		surname = self.parent.cliententry.GetValue()
		
		animalname = self.parent.animalnameentry.GetValue()
		species = self.parent.speciesentry.GetValue()
		reason = self.parent.reasonentry.GetValue()
		
		action = "SELECT appointment.ID, appointment.Date, appointment.AppointmentReason, animal.Name, animal.Species, client.ClientTitle, client.ClientForenames, client.ClientSurname FROM appointment INNER JOIN animal ON appointment.AnimalID = animal.ID INNER JOIN client ON appointment.OwnerID = client.ID WHERE "
		
		#print "fromdate = " + str(fromdate) + ", todate = " + str(todate)
		
		if str(fromdate) != "" and str(todate) != "":
			
			fromdate = miscmethods.GetSQLDateFromWXDate(fromdate)
			todate = miscmethods.GetSQLDateFromWXDate(todate)
			
			action = action + "appointment.Date BETWEEN \"" + fromdate + "\" AND \"" + todate + "\" AND "
			
		elif str(fromdate) == "" and str(todate) != "":
			
			todate = miscmethods.GetSQLDateFromWXDate(todate)
			
			action = action + "appointment.Date <= \"" + todate + "\" AND "
			
		elif str(fromdate) != "" and str(todate) == "":
			
			fromdate = miscmethods.GetSQLDateFromWXDate(fromdate)
			
			action = action + "appointment.Date >= \"" + fromdate + "\" AND "
		 
		action = action + "client.ClientSurname LIKE \"%" + surname + "%\" AND animal.Name LIKE \"%" + animalname + "%\" AND animal.Species LIKE \"%" + species + "%\" AND appointment.AppointmentReason LIKE \"%" + reason + "%\" ORDER BY appointment.Date desc"
		
		self.htmllist = db.SendSQL(action, self.localsettings.dbconnection)
		
		
		self.SetItemCount(len(self.htmllist))
		self.Refresh()
		self.SetSelection(-1)
		
		self.Show()
		
		self.parent.totallabel.SetLabel(self.parent.GetParent().t("totallabel") + ": " + str(len(self.htmllist)) + " ")
		self.parent.listboxsizer.Layout()
		
		del busy

class ClientListCtrl(customwidgets.ListCtrlWrapper):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, parent, localsettings):
		
		self.htmllist = []
		self.localsettings = localsettings
		self.parent = parent
		
		columnheadings = (self.t("animalnamelabel"), self.t("clientaddresslabel"), self.t("clientpostcodelabel"), self.t("clienthomephonelabel"), self.t("clientmobilephonelabel"), self.t("clientworkphonelabel"), self.t("clientemailaddresslabel"))
		
		customwidgets.ListCtrlWrapper.__init__(self, self.parent, self.localsettings, columnheadings, ("icons/editclient.png",))
	
	def ProcessRow(self, rowdata):
		
		#print "rowdata = " + str(rowdata)
		
		return ( (rowdata[0], rowdata[1], rowdata[2].replace("\r", "").replace("\n", ", "), rowdata[3], rowdata[4], rowdata[5], rowdata[6], rowdata[7]), 0)
	
	def RefreshList(self, results):
		
		self.htmllist = []
		
		if len(results) < 1001:
			
			count = 0
			
			for a in results:
				
				name = ""
				
				if a[1] != "":
					
					name = name + a[1] + " "
				
				if a[2] != "":
					
					name = name + a[2] + " "
				
				if a[3] != "":
					
					name = name + a[3]
				
				self.htmllist.append((a[0], name, a[4], a[5], a[6], a[7], a[8], a[9], a[10]))
		
		self.parent.totallabel.SetLabel(miscmethods.NoWrap(self.t("totallabel") + ": " + str(len(results))))
		
		customwidgets.ListCtrlWrapper.RefreshList(self)

class AnimalListCtrl(customwidgets.ListCtrlWrapper):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, parent, localsettings):
		
		self.htmllist = []
		self.localsettings = localsettings
		self.parent = parent
		
		columnheadings = (self.t("namelabel"), self.t("animalsexlabel"), self.t("animalspecieslabel"), self.t("animalbreedlabel"), self.t("agelabel"), self.t("animalcolourlabel") ,self.t("asmreflabel"))
		
		customwidgets.ListCtrlWrapper.__init__(self, self.parent, self.localsettings, columnheadings, ("icons/asm.png", "icons/editanimal.png", "icons/ghost.png"))
	
	def ProcessRow(self, rowdata):
		
		return ( (rowdata[0], rowdata[1], rowdata[2], rowdata[3], rowdata[4], rowdata[5], rowdata[6], rowdata[7]), rowdata[8])
	
	def RefreshList(self, results):
		
		self.htmllist = []
		
		if len(results) < 1001:
			
			count = 0
			
			for a in results:
				
				sex = miscmethods.GetSex(self.localsettings, a[3])
				
				age = miscmethods.GetAgeFromDOB(a[7], self.localsettings)
				
				if a[12] == 1:
					
					imageid = 2
					
				elif a[15] != "":
					
					imageid = 0
					
				else:
					
					imageid = 1
				
				self.htmllist.append((a[0], a[2], sex, a[4], a[5], age, a[6], a[15], imageid))
		
		self.parent.totallabel.SetLabel(miscmethods.NoWrap(self.t("totallabel") + ": " + str(len(results))))
		
		customwidgets.ListCtrlWrapper.RefreshList(self)
