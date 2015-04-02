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
import animalmethods
import appointmentmethods
import customwidgets
import diarymethods
import os
import sys
import formmethods
import wx.lib.mixins.listctrl as listmix
import medicationmethods
import attachedfilemethods


EDIT_ANIMAL = 2001
DELETE_ANIMAL = 2002
MAKE_APPOINTMENT = 2003
ADD_ANIMAL = 2004
REFRESH_ANIMALS = 2005
FILTER_ANIMALS = 2006
ADD_INVOICE = 2007
VIEW_INVOICE = 2008
DELETE_INVOICE = 2009
EDIT_INVOICE = 2010
REFRESH_INVOICES = 2011
ADD_RECEIPT = 2012
EDIT_RECEIPT = 2013
DELETE_RECEIPT = 2014
REFRESH_RECEIPTS = 2015

class ClientSettings:
	
	def __init__(self, localsettings, ID=False):
		
		self.localsettings = localsettings
		
		if ID == False:
			self.ID = False
			self.title = u""
			self.forenames = u""
			self.surname = u""
			self.address = u""
			self.postcode = u""
			self.hometelephone = u""
			self.mobiletelephone = u""
			self.worktelephone = u""
			self.phonepermissions = 0
			self.emailaddress = u""
			self.comments = u""
			currenttime = datetime.datetime.today().strftime("%x %X")
			self.changelog = str(currenttime) + "%%%" + str(self.localsettings.userid)
		else:
			
			action = "SELECT * FROM client WHERE ID = " + str(ID)
			results = db.SendSQL(action, self.localsettings.dbconnection)
			
			self.ID = ID
			self.title = unicode(results[0][1], "utf8")
			self.forenames = unicode(results[0][2], "utf8")
			self.surname = unicode(results[0][3], "utf8")
			self.address = unicode(results[0][4], "utf8")
			self.postcode = unicode(results[0][5], "utf8")
			self.hometelephone = unicode(results[0][6], "utf8")
			self.mobiletelephone = unicode(results[0][7], "utf8")
			self.worktelephone = unicode(results[0][8], "utf8")
			self.emailaddress = unicode(results[0][9], "utf8")
			self.comments = results[0][10]
			self.changelog = results[0][11]
			self.phonepermissions = results[0][12]
	
	def Submit(self):
		
		locked = False
		
		if self.ID != False:
			
			action = "SELECT ChangeLog FROM client WHERE ID = " + str(self.ID)
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
			
			dbmethods.WriteToClientTable(self.localsettings.dbconnection, self)

class ClientPanel(wx.Panel, listmix.ColumnSorterMixin):
	
	def t(self, field):
		
		return  self.clientdata.localsettings.t(field)
	
	def GetButtonLabel(self, field, index):
		
		return  self.clientdata.localsettings.dictionary[field][self.clientdata.localsettings.language][index]
	
	def __init__(self, notebook, clientdata):
		
		busy = wx.BusyCursor()
		
		self.clientdata = clientdata
		
		if clientdata.ID == False:
			pagetitle = self.t("newclientpagetitle")
		else:
			pagetitle = clientdata.title + " " + clientdata.surname
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, pagetitle)
		
		self.pageimage = "icons/editclient.png"
		
		wx.Panel.__init__(self, notebook)
		
		self.viewappointmentspanel = False
		
		fields = ( (clientdata.title, self.t("clienttitlelabel"), "title"), (clientdata.forenames, self.t("clientforenameslabel"), "small"), (clientdata.surname, self.t("clientsurnamelabel"), "small"), (clientdata.address, self.t("clientaddresslabel"), "large"), (clientdata.postcode, self.t("clientpostcodelabel"), "small"), (clientdata.hometelephone, self.t("clienthomephonelabel"), "telephone", 1),  (clientdata.mobiletelephone, self.t("clientmobilephonelabel"), "telephone", 2), (clientdata.worktelephone, self.t("clientworkphonelabel"), "telephone", 3), (clientdata.emailaddress, self.t("clientemailaddresslabel"), "small"), (clientdata.comments, self.t("clientcommentslabel"), "large") )
		
		noofrows = len(fields)
		
		flexisizer = wx.BoxSizer(wx.VERTICAL)
		
		labels = []
		inputfields = []
		
		for a in range(0, len(fields)):
			
			label = wx.StaticText(self, -1, miscmethods.NoWrap(fields[a][1]) + ": ", style=wx.ALIGN_BOTTOM)
			font = label.GetFont()
			font.SetPointSize(font.GetPointSize() - 2)
			label.SetFont(font)
			labels.append(label)
			
			if fields[a][2] == "small":
				
				inputfield = wx.TextCtrl(self, -1, fields[a][0])
				inputfield.phoneid = 0
				inputfield.flexvalue = 0
				inputfield.Bind(wx.EVT_CHAR, self.EnableSave)
				inputfields.append(inputfield)
				
			elif fields[a][2] == "large":
				
				inputfield = wx.TextCtrl(self, -1, fields[a][0], style=wx.TE_MULTILINE)
				inputfield.phoneid = 0
				inputfield.flexvalue = 1
				inputfield.Bind(wx.EVT_CHAR, self.EnableSave)
				inputfields.append(inputfield)
				
			elif fields[a][2] == "title":
				
				inputfield = wx.ComboBox(self, -1, fields[a][0], choices=("Mr", "Ms", "Mrs", "Miss", "Dr"))
				inputfield.phoneid = 0
				inputfield.flexvalue = 0
				inputfield.Bind(wx.EVT_CHAR, self.EnableSave)
				inputfield.Bind(wx.EVT_COMBOBOX, self.EnableSave)
				inputfields.append(inputfield)
				
			elif fields[a][2] == "telephone":
				
				inputfield = wx.TextCtrl(self, -1, fields[a][0])
				inputfield.SetToolTipString(self.t("phonenumbertooltip"))
				inputfield.phoneid = 0
				inputfield.slotid = fields[a][3]
				inputfield.flexvalue = 0
				inputfield.Bind(wx.EVT_TEXT, self.EnableSave)
				inputfield.Bind(wx.EVT_CHAR, self.LookForPublicChar)
				
				if fields[a][3] == 1:
					
					if str(clientdata.phonepermissions).__contains__("1"):
						
						inputfield.SetBackgroundColour("green")
						
						inputfield.phoneid = 1
					
				elif fields[a][3] == 2:
					
					if str(clientdata.phonepermissions).__contains__("2"):
						
						inputfield.SetBackgroundColour("green")
						
						inputfield.phoneid = 1
					
				elif fields[a][3] == 3:
					
					if str(clientdata.phonepermissions).__contains__("3"):
						
						inputfield.SetBackgroundColour("green")
						
						inputfield.phoneid = 1
				
				inputfields.append(inputfield)
			
			flexisizer.Add(labels[a], 0, wx.ALIGN_LEFT)
			flexisizer.Add(inputfields[a], inputfields[a].flexvalue, wx.EXPAND)
		
		mainclientsizer = wx.BoxSizer(wx.VERTICAL)
		
		mainclientsizer.Add(flexisizer, 1, wx.EXPAND)
		
		########Animal Details were here#########################
		
		mainsizer = wx.BoxSizer(wx.HORIZONTAL)
		mainsizer.Add(mainclientsizer, 2, wx.EXPAND)
		
		spacer = wx.StaticText(self, -1, "", size=(20,-1))
		mainsizer.Add(spacer, 0, wx.EXPAND)
		
		#mainsizer.Add(animallistsizer, 3, wx.EXPAND)
		
		#spacer2 = wx.StaticText(self, -1, "", size=(20,-1))
		#mainsizer.Add(spacer2, 0, wx.EXPAND)
		
		billnotebooksizer = wx.BoxSizer(wx.VERTICAL)
		
		billsummarycontainer = wx.Panel(self)
		
		billsummarycontainersizer = wx.BoxSizer(wx.HORIZONTAL)
		
		billsummarypanel = BillSummaryPanel(billsummarycontainer, clientdata)
		billsummarycontainersizer.Add(billsummarypanel, 1, wx.EXPAND)
		
		billsummarycontainer.SetSizer(billsummarycontainersizer)
		
		billnotebooksizer.Add(billsummarycontainer, 0, wx.ALIGN_CENTER)
		
		billnotebooksizer.Add(wx.StaticText(self, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		billnotebook = wx.Notebook(self)
		
		if self.clientdata.ID == False:
			billnotebook.Disable()
		
		if clientdata.localsettings.editfinances == 0:
			billnotebook.Disable()
		
		animalpanel = wx.Panel(billnotebook)
		
		animalsizer = wx.BoxSizer(wx.VERTICAL)
		
		self.animallistbox = customwidgets.AnimalListCtrl(animalpanel, clientdata)
		
		self.animallistbox.listctrl.Bind(wx.EVT_RIGHT_DOWN, self.AnimalMenuPopup)
		self.animallistbox.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.EditAnimal)
		
		if self.clientdata.ID == False:
			
			self.animallistbox.Disable()
		
		animaltotallabel = wx.StaticText(animalpanel, -1, self.t("totallabel") + ": 0 ")
		
		animalsizer.Add(self.animallistbox, 1, wx.EXPAND)
		animalsizer.Add(animaltotallabel, 0, wx.ALIGN_RIGHT)
		
		animalpanel.SetSizer(animalsizer)
		
		billnotebook.AddPage(animalpanel, self.t("clientanimalslabel"), select=True)
		
		#billsummarypanel = BillSummaryPanel(billnotebook, clientdata)
		#billnotebook.AddPage(billsummarypanel, self.t("clientbalancelabel"), select=False)
		
		receiptpanel = ClientReceiptPanel(billnotebook, clientdata)
		billnotebook.AddPage(receiptpanel, self.t("clientdetailedbilllabel"), select=False)
		
		invoicepanel = ClientInvoicePanel(billnotebook, clientdata)
		billnotebook.AddPage(invoicepanel, self.t("invoicespagetitle"), select=False)
		
		attachedfilespanel = attachedfilemethods.AttachedFilesPanel(billnotebook, clientdata.localsettings, 0, clientdata.ID)
		billnotebook.AddPage(attachedfilespanel, self.t("attachedfileslabel"), select=False)
		
		billnotebooksizer.Add(billnotebook, 1, wx.EXPAND)
		
		mainsizer.Add(billnotebooksizer, 4, wx.EXPAND)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		closebuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		savebuttonbitmap = wx.Bitmap("icons/save.png")
		
		savebutton = wx.BitmapButton(self, -1, savebuttonbitmap)
		savebutton.SetToolTipString(self.t("clientsavetooltip"))
		savebutton.Bind(wx.EVT_BUTTON, self.SaveClient)
		savebutton.Disable()
		
		closebuttonsizer.Add(savebutton, 0, wx.EXPAND)
		
		mergebuttonbitmap = wx.Bitmap("icons/users.png")
		
		mergebutton = wx.BitmapButton(self, -1, mergebuttonbitmap)
		mergebutton.SetToolTipString(self.t("clientmergetooltip"))
		mergebutton.Bind(wx.EVT_BUTTON, self.MergeClient)
		closebuttonsizer.Add(mergebutton, 0, wx.EXPAND)
		
		if self.clientdata.ID == False or self.clientdata.localsettings.deleteclients == 0:
			
			mergebutton.Disable()
		
		bookbitmap = wx.Bitmap("icons/diary.png")
		creatediarynotebutton = wx.BitmapButton(self, -1, bookbitmap)
		creatediarynotebutton.SetToolTipString(self.t("createassociateddiarynotetooltip"))
		creatediarynotebutton.Bind(wx.EVT_BUTTON, self.CreateDiaryNote)
		
		if self.clientdata.ID == False or self.clientdata.localsettings.addtodiary == 0:
			
			creatediarynotebutton.Disable()
		
		closebuttonsizer.Add(creatediarynotebutton, 0, wx.EXPAND)
		
		formbitmap = wx.Bitmap("icons/form.png")
		formbutton = wx.BitmapButton(self, -1, formbitmap)
		formbutton.SetToolTipString(self.t("clientgenerateformtooltip"))
		formbutton.Bind(wx.EVT_BUTTON, self.GenerateForm)
		closebuttonsizer.Add(formbutton, 0, wx.EXPAND)
		
		if self.clientdata.ID == False:
			
			formbutton.Disable()
		
		shopsalebitmap = wx.Bitmap("icons/calculator.png")
		shopsalebutton = wx.BitmapButton(self, -1, shopsalebitmap)
		shopsalebutton.SetToolTipString(self.t("shopsalemenuitem"))
		shopsalebutton.Bind(wx.EVT_BUTTON, self.ShopSale)
		closebuttonsizer.Add(shopsalebutton, 0, wx.EXPAND)
		
		if self.clientdata.ID == False:
			
			shopsalebutton.Disable()
		
		closebuttonsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		topsizer.Add(closebuttonsizer, 0, wx.EXPAND)
		
		topsizer.Add(wx.StaticText(self, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		topsizer.Add(mainsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.billnotebook = billnotebook
		
		self.notebook = notebook
		#self.addanimalbutton = addanimalbutton
		self.mergebutton = mergebutton
		self.creatediarynotebutton = creatediarynotebutton
		self.formbutton = formbutton
		self.shopsalebutton = shopsalebutton
		self.billnotebook = billnotebook
		#self.animalsearchinput = animalsearchinput
		self.animalnamefilter = ""
		self.invoicepanel = invoicepanel
		self.animaltotallabel = animaltotallabel
		self.animallistsizer = animalsizer
		#self.animallistboxlabel = animallistboxlabel
		
		self.savebutton = savebutton
		self.flexisizer = flexisizer
		
		if self.clientdata.ID != False:
			
			self.RefreshAnimals()
		
		self.receiptlistbox = receiptpanel.receiptlistbox
		
		billsummarypanel.GenerateBalance()
		
		self.billsummarypanel = billsummarypanel
		receiptpanel.RefreshList()
		self.receiptpanel = receiptpanel
		self.attachedfilespanel = attachedfilespanel
		
		self.titleentry = inputfields[0]
		
		del busy
	
	def GetListCtrl(self):# Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
		
        	return self.animallistbox
	
	def LookForPublicChar(self, ID):
		
		inputfield = ID.GetEventObject()
		
		keycode = ID.GetKeyCode()
		
		if keycode == 16:
			
			if inputfield.phoneid == 1:
				inputfield.Hide()
				backgroundcolour = self.titleentry.GetBackgroundColour()
				inputfield.SetBackgroundColour(backgroundcolour)
				inputfield.phoneid = 0
				
				self.clientdata.phonepermissions = str(self.clientdata.phonepermissions).replace(str(inputfield.slotid), "")
				inputfield.Show()
				
			else:
				inputfield.Hide()
				inputfield.SetBackgroundColour("green")
				inputfield.phoneid = 1
				
				self.clientdata.phonepermissions = str(self.clientdata.phonepermissions) + str(inputfield.slotid)
				inputfield.Show()
			
			if self.clientdata.phonepermissions == "":
				
				self.clientdata.phonepermissions = 0
				
			else:
				
				self.clientdata.phonepermissions = int(self.clientdata.phonepermissions)
			
			self.EnableSave(ID)
			
			inputfield.SetFocus()
			
		else:
			
			ID.Skip()
	
	def MergeClient(self, ID):
		
		FindClientDialog(self, self.clientdata.localsettings)
		
		try:
			
			clientid = self.clientdialogid
			
		except:
			
			clientid = 0
		
		if clientid > 0:
			
			action = "UPDATE animal SET OwnerID = " + str(self.clientdata.ID) + " WHERE OwnerID = " + str(clientid)
			db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			action = "UPDATE appointment SET OwnerID = " + str(self.clientdata.ID) + " WHERE OwnerID = " + str(clientid)
			db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			action = "UPDATE receipt SET TypeID = " + str(self.clientdata.ID) + " WHERE TypeID = " + str(clientid) + " AND Type = 4"
			db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			action = "UPDATE diary SET LinkID = " + str(self.clientdata.ID) + " WHERE LinkID = " + str(clientid) + " AND LinkType = 1"
			db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			action = "UPDATE media SET LinkID = " + str(self.clientdata.ID) + " WHERE LinkID = " + str(clientid) + " AND LinkType = 1"
			db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			action = "UPDATE invoice SET ClientID = " + str(self.clientdata.ID) + " WHERE ClientID = " + str(clientid)
			db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			action = "DELETE FROM client WHERE ID = " + str(clientid)
			db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			miscmethods.ShowMessage(self.t("clientsmergedmessage"), self)
	
	def AnimalMenuPopup(self, ID):
		
		popupmenu = wx.Menu()
		
		if self.clientdata.localsettings.editanimals == 1:
			
			addanimal = wx.MenuItem(popupmenu, ADD_ANIMAL, self.t("addlabel"))
			addanimal.SetBitmap(wx.Bitmap("icons/new.png"))
			popupmenu.AppendItem(addanimal)
			wx.EVT_MENU(popupmenu, ADD_ANIMAL, self.AddAnimal)
		
		#listboxid = -1
		
		#for a in range(0, len(self.animallistbox.htmllist)):
			
			#if self.animallistbox.IsSelected(a) == True:
				
				#listboxid = a
		
		#if listboxid > -1:
		if self.animallistbox.listctrl.GetSelectedItemCount() > 0:
			
			if self.clientdata.localsettings.editanimals == 1:
				
				editanimal = wx.MenuItem(popupmenu, EDIT_ANIMAL, self.t("editlabel"))
				editanimal.SetBitmap(wx.Bitmap("icons/edit.png"))
				popupmenu.AppendItem(editanimal)
				wx.EVT_MENU(popupmenu, EDIT_ANIMAL, self.EditAnimal)
			
			if self.clientdata.localsettings.deleteanimals == 1:
				
				deleteanimal = wx.MenuItem(popupmenu, DELETE_ANIMAL, self.t("deletelabel"))
				deleteanimal.SetBitmap(wx.Bitmap("icons/delete.png"))
				popupmenu.AppendItem(deleteanimal)
				wx.EVT_MENU(popupmenu, DELETE_ANIMAL, self.DeleteAnimal)
			
			if self.clientdata.localsettings.editappointments == 1:
				
				createappointment = wx.MenuItem(popupmenu, MAKE_APPOINTMENT, self.t("createappointmentlabel"))
				createappointment.SetBitmap(wx.Bitmap("icons/new.png"))
				popupmenu.AppendItem(createappointment)
				wx.EVT_MENU(popupmenu, MAKE_APPOINTMENT, self.CreateAppointment)
		
		filteranimals = wx.MenuItem(popupmenu, FILTER_ANIMALS, self.t("filteranimalslabel"))
		filteranimals.SetBitmap(wx.Bitmap("icons/search.png"))
		popupmenu.AppendItem(filteranimals)
		wx.EVT_MENU(popupmenu, FILTER_ANIMALS, self.FilterAnimals)
		
		refreshanimals = wx.MenuItem(popupmenu, REFRESH_ANIMALS, self.t("refreshlabel"))
		refreshanimals.SetBitmap(wx.Bitmap("icons/refresh.png"))
		popupmenu.AppendItem(refreshanimals)
		wx.EVT_MENU(popupmenu, REFRESH_ANIMALS, self.RefreshAnimals)
		
		self.PopupMenu(popupmenu)
	
	def FilterAnimals(self, ID):
		
		dialog = wx.Dialog(self.notebook, -1, self.t("chooseananimaltitle"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		namelabel = wx.StaticText(panel, -1, self.t("appointmentsearchanimalnamelabel"))
		font = namelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		namelabel.SetFont(font)
		topsizer.Add(namelabel, 0, wx.ALIGN_LEFT)
		
		nameentry = wx.TextCtrl(panel, -1, "", style=wx.TE_PROCESS_ENTER)
		nameentry.Bind(wx.EVT_CHAR, self.AnimalNameFilterKeyPress)
		topsizer.Add(nameentry, 1, wx.EXPAND)
		
		nameentry.SetFocus()
		
		panel.SetSizer(topsizer)
		
		panel.nameentry = nameentry
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		dialog.Fit()
		
		dialog.ShowModal()
	
	def AnimalNameFilterKeyPress(self, ID):
		
		keycode = ID.GetKeyCode()
		
		panel = ID.GetEventObject().GetParent()
		
		name = panel.nameentry.GetValue()
		
		if keycode == 13:
			
			self.animalnamefilter = name
			
			panel.GetParent().Close()
			
			if name == "":
				
				name = self.t("alllabel")
			
			self.RefreshAnimals()
			
			#self.animaltotallabel.SetLabel(miscmethods.NoWrap(self.t("filterlabel") + " (" + name + ")" + " " + self.animaltotallabel.GetLabel()))
			
			#self.animallistsizer.Layout()
			
		else:
			
			ID.Skip()
	
	def EnableSave(self, ID):
		
		self.savebutton.Enable()
		
		ID.Skip()
	
	def GenerateForm(self, ID):
		
		ChooseClientForm(self)
	
	def CreateDiaryNote(self, ID=False):
		
		title = self.clientdata.title + " " + self.clientdata.surname
		
		diarynotepanel = diarymethods.DiaryNotePanel(self.notebook, self.clientdata.localsettings, 1, self.clientdata.ID, title)
		self.notebook.AddPage(diarynotepanel)
	
	def ChangeLog(self, ID):
		
		action = "SELECT ChangeLog FROM client WHERE ID = " + str(self.clientdata.ID)
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		
		changelog = results[0][0]
		
		miscmethods.ShowChangeLog(self.clientdata.title + " " + self.clientdata.forenames + " " + self.clientdata.surname, changelog, self.localsettings.dbconnection)
		
	
	def SaveClient(self, ID):
		
		children = self.GetChildren()
		
		self.clientdata.title = children[1].GetValue()
		self.clientdata.forenames = children[3].GetValue()
		self.clientdata.surname = children[5].GetValue()
		self.clientdata.address = children[7].GetValue()
		self.clientdata.postcode = children[9].GetValue()
		self.clientdata.hometelephone = children[11].GetValue()
		self.clientdata.mobiletelephone = children[13].GetValue()
		self.clientdata.worktelephone = children[15].GetValue()
		self.clientdata.emailaddress = children[17].GetValue()
		self.clientdata.comments = children[19].GetValue()
		
		self.clientdata.title = miscmethods.FormatText(self.clientdata.title)
		self.clientdata.forenames = miscmethods.FormatText(self.clientdata.forenames)
		self.clientdata.surname = miscmethods.FormatText(self.clientdata.surname)
		self.clientdata.address = miscmethods.FormatText(self.clientdata.address)
		self.clientdata.postcode = self.clientdata.postcode.upper()
		#self.clientdata.comments = miscmethods.ValidateEntryString(self.clientdata.comments)
		
		children[1].SetValue(self.clientdata.title)
		children[3].SetValue(self.clientdata.forenames)
		children[5].SetValue(self.clientdata.surname)
		children[7].SetValue(self.clientdata.address)
		children[9].SetValue(self.clientdata.postcode)
		children[19].SetValue(self.clientdata.comments)
		
		if self.clientdata.localsettings.addtodiary == 1:
			
			self.creatediarynotebutton.Enable()
		
		self.formbutton.Enable()
		self.shopsalebutton.Enable()
		self.animallistbox.Enable()
		
		if self.clientdata.localsettings.deleteclients == 1:
			
			self.mergebutton.Enable()
		
		if self.clientdata.ID == False:
			
			notebook = self.GetParent()
			
			self.clientdata = CheckForExistingClient(self, self.clientdata, notebook).clientdata
			
			if self.clientdata.ID == False:
				
				self.clientdata.Submit()
				self.savebutton.Disable()
				self.RefreshAnimals()
			
			else:
				
				self.clientdata = ClientSettings(self.clientdata.localsettings)
			
		else:
			
			self.clientdata.Submit()
			self.savebutton.Disable()
		
		self.attachedfilespanel.listbox.linkid = self.clientdata.ID
		self.billnotebook.Enable()
	
	def ShopSale(self, ID):
		
		medicationmethods.ShopSale(self, self.clientdata.ID, self.clientdata.localsettings)
		
		self.receiptpanel.RefreshList()
	
	def EditClientFromSaveDialog(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		listboxid = panel.listbox.GetSelection()
		
		clientid = panel.possiblematches[listboxid][0]
		
		notebook = self.GetParent()
		
		clientsettings = ClientSettings(self.clientdata.localsettings, clientid)
		
		clientpanel = ClientPanel(notebook, clientsettings)
		
		notebook.AddPage(clientpanel)
		
		panel.GetParent().Close()
	
	def ClosePage(self, ID=False):
		
		if self.savebutton.IsEnabled() == True:
			
			return miscmethods.ConfirmMessage(self.t("clientunsavedchangesmessage"))
			
		else:
			
			return True
	
	def RefreshAnimals(self, ID=False):
		
		if self.animalnamefilter == "":
			
			name = self.t("alllabel")
			
		else:
			
			name = self.animalnamefilter
		
		self.animallistbox.RefreshList()
		
		self.animaltotallabel.SetLabel(miscmethods.NoWrap(self.t("filterlabel") + " (" + name + ")" + " " + self.clientdata.localsettings.dictionary["totallabel"][self.clientdata.localsettings.language] + ": " + str(len(self.animallistbox.htmllist))))
		
		self.animallistsizer.Layout()
		
	def AddAnimal(self, ID):
		
		animalsettings = animalmethods.AnimalSettings(self.clientdata.localsettings, self.clientdata.ID, False)
		animalpanel = animalmethods.AnimalPanel(self.notebook, animalsettings, self)
		self.notebook.AddPage(animalpanel)
		wx.CallAfter(animalpanel.nameentry.SetFocus)
	
	def DeleteAnimal(self, ID):
		
		listboxid = self.animallistbox.GetSelection()
		animalid = self.animallistbox.htmllist[listboxid][0]
		
		confirm = miscmethods.ConfirmMessage(self.t("clientdeleteanimalmessage"))
		
		if confirm == True:
			
			action = "DELETE FROM animal WHERE ID = " + str(animalid)
			db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			action = "DELETE FROM appointment WHERE AnimalID = " + str(animalid)
			db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			self.RefreshAnimals()
	
	def EditAnimal(self, ID):
		
		listboxid = self.animallistbox.GetSelection()
		animalid = self.animallistbox.htmllist[listboxid][0]
		
		animalsettings = animalmethods.AnimalSettings(self.clientdata.localsettings, False, animalid)
		animalpanel = animalmethods.AnimalPanel(self.notebook, animalsettings, self)
		wx.CallAfter(self.notebook.AddPage, animalpanel)
		
		animalpanel.nameentry.SetFocus()
	
	def CreateAppointment(self, ID):
		
		listboxid = self.animallistbox.GetSelection()
		animalid = self.animallistbox.htmllist[listboxid][0]
		
		animaldata = animalmethods.AnimalSettings(self.clientdata.localsettings, self.clientdata.ID, animalid)
		
		appointmentsettings = appointmentmethods.AppointmentSettings(animaldata.localsettings, animaldata.ID, False)
		appointmentpanel = appointmentmethods.AppointmentPanel(self.notebook, appointmentsettings)
		wx.CallAfter(self.notebook.AddPage, appointmentpanel)

class ClientReceiptPanel(wx.Panel):
	
	def t(self, field):
		
		return  self.clientdata.localsettings.t(field)
	
	def GetButtonLabel(self, field, index):
		
		return  self.clientdata.localsettings.dictionary[field][self.clientdata.localsettings.language][index]
	
	def __init__(self, parent, clientdata):
		
		self.clientdata = clientdata
		
		clientpanel = parent.GetParent()
		
		wx.Panel.__init__(self, parent)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		summarytoolssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		latestcheckbox = wx.CheckBox(self, -1, self.GetButtonLabel("clientrecentbillitems", 0))
		font = latestcheckbox.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		latestcheckbox.SetFont(font)
		latestcheckbox.SetToolTipString(self.GetButtonLabel("clientrecentbillitems", 1))
		latestcheckbox.Bind(wx.EVT_CHECKBOX, self.RecentBoxTicked)
		summarytoolssizer.Add(latestcheckbox, 0, wx.ALIGN_CENTER)
		
		summarytoolssizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		fromsizer = wx.BoxSizer(wx.VERTICAL)
		
		fromlabel = wx.StaticText(self, -1, " " + self.t("fromlabel") + " ", style=wx.EXPAND)
		font = fromlabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		fromlabel.SetFont(font)
		fromsizer.Add(fromlabel, 0, wx.ALIGN_LEFT)
		
		fromentry = customwidgets.DateCtrl(self, self.clientdata.localsettings)
		fromsizer.Add(fromentry, 1, wx.EXPAND)
		
		summarytoolssizer.Add(fromsizer, 0, wx.EXPAND)
		
		tosizer = wx.BoxSizer(wx.VERTICAL)
		
		tolabel = wx.StaticText(self, -1, " " + self.t("tolabel") + " ", style=wx.EXPAND)
		tolabel.SetFont(font)
		tosizer.Add(tolabel, 0, wx.ALIGN_LEFT)
		
		toentry = customwidgets.DateCtrl(self, self.clientdata.localsettings)
		tosizer.Add(toentry, 1, wx.EXPAND)
		
		summarytoolssizer.Add(tosizer, 0, wx.EXPAND)
		
		summarytoolssizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		refreshbitmap = wx.Bitmap("icons/refresh.png")
		refreshbutton = wx.BitmapButton(self, -1, refreshbitmap)
		refreshbutton.SetToolTipString(self.t("clientrefreshbilltooltip"))
		refreshbutton.Bind(wx.EVT_BUTTON, self.RefreshList)
		summarytoolssizer.Add(refreshbutton, 0, wx.ALIGN_BOTTOM)
		
		topsizer.Add(summarytoolssizer, 0, wx.EXPAND)
		
		receiptlistbox = customwidgets.ReceiptSummaryListbox(self, clientdata)
		receiptlistbox.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.EditReceiptItem)
		receiptlistbox.listctrl.Bind(wx.EVT_RIGHT_DOWN, self.ReceiptPopup)
		
		#if clientdata.localsettings.changelog == 1:
			
			#receiptlistbox.Bind(wx.EVT_RIGHT_DOWN, self.ReceiptChangeLog)
		
		topsizer.Add(receiptlistbox, 4, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.receiptlistbox = receiptlistbox
		self.latestcheckbox = latestcheckbox
		self.fromentry = fromentry
		self.toentry = toentry
		self.clientpanel = clientpanel
		#self.newbutton = newbutton
		#self.editbutton = editbutton
		#self.deletebutton = deletebutton
		
		self.latestcheckbox.SetValue(True)
		
		today = datetime.date.today()
		
		timedelta = datetime.timedelta(30)
		
		fromdate = today - timedelta
		
		todate = miscmethods.GetWXDateFromDate(today)
		fromdate = miscmethods.GetWXDateFromDate(fromdate)
		
		self.fromentry.SetValue(fromdate)
		self.fromentry.Disable()
		self.toentry.SetValue(todate)
		self.toentry.Disable()
	
	def ReceiptPopup(self, ID):
		
		popupmenu = wx.Menu()
		
		if self.clientdata.localsettings.editfinances == 1:
			
			add = wx.MenuItem(popupmenu, ADD_RECEIPT, self.t("addlabel"))
			add.SetBitmap(wx.Bitmap("icons/new.png"))
			popupmenu.AppendItem(add)
			wx.EVT_MENU(popupmenu, ADD_RECEIPT, self.CreateReceiptItem)
			
			if self.receiptlistbox.GetSelection() > 0:
				
				edit = wx.MenuItem(popupmenu, EDIT_RECEIPT, self.t("editlabel"))
				edit.SetBitmap(wx.Bitmap("icons/edit.png"))
				popupmenu.AppendItem(edit)
				wx.EVT_MENU(popupmenu, EDIT_RECEIPT, self.EditReceiptItem)
				
				delete = wx.MenuItem(popupmenu, DELETE_RECEIPT, self.t("deletelabel"))
				delete.SetBitmap(wx.Bitmap("icons/delete.png"))
				popupmenu.AppendItem(delete)
				wx.EVT_MENU(popupmenu, DELETE_RECEIPT, self.Delete)
			
			popupmenu.AppendSeparator()
		
		refresh = wx.MenuItem(popupmenu, REFRESH_RECEIPTS, self.t("refreshlabel"))
		refresh.SetBitmap(wx.Bitmap("icons/refresh.png"))
		popupmenu.AppendItem(refresh)
		wx.EVT_MENU(popupmenu, REFRESH_RECEIPTS, self.RefreshList)
		
		self.PopupMenu(popupmenu)
	
	def CreateReceiptItem(self, ID):
		
		self.EditReceiptItemDialog()
		
	def EditReceiptItem(self, ID):
		
		listboxid = self.receiptlistbox.GetSelection()
		
		if listboxid > 0:
			
			self.EditReceiptItemDialog(listboxid)
	
	def EditReceiptItemDialog(self, listboxid=-1):
		
		if listboxid > 0:
			
			receiptid = self.receiptlistbox.htmllist[listboxid][3]
			
			date = self.receiptlistbox.htmllist[listboxid][0]
			
			description = self.receiptlistbox.htmllist[listboxid][2]
			
			price = self.receiptlistbox.htmllist[listboxid][1]
			price = miscmethods.FormatPrice(price)
			
		else:
			
			self.receiptlistbox.SetSelection(-1)
			
			receiptid = -1
			
			date = datetime.date.today()
			date = miscmethods.GetSQLDateFromDate(date)
			
			description = ""
			price = "0.00"
		
		dialog = wx.Dialog(self, -1, self.t("vetformreceiptitemlabel"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		descriptionlabel = wx.StaticText(panel, -1, self.t("descriptionlabel"))
		font = descriptionlabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		descriptionlabel.SetFont(font)
		topsizer.Add(descriptionlabel, 0, wx.ALIGN_LEFT)
		
		descriptionentry = wx.TextCtrl(panel, -1, description, style=wx.TE_MULTILINE, size=(200,-1))
		topsizer.Add(descriptionentry, 1, wx.EXPAND)
		
		pricelabel = wx.StaticText(panel, -1, self.t("pricelabel"))
		pricelabel.SetFont(font)
		topsizer.Add(pricelabel, 0, wx.ALIGN_LEFT)
		
		pricesizer = wx.BoxSizer(wx.HORIZONTAL)
		
		priceentry = wx.TextCtrl(panel, -1, price)
		pricesizer.Add(priceentry, 0, wx.EXPAND)
		
		pricesizer.Add(wx.StaticText(panel, -1, ""), 1, wx.EXPAND)
		
		#submitbitmap = wx.Bitmap("icons/submit.png")
		submitbutton = wx.Button(panel, -1, self.t("submitlabel"))
		submitbutton.SetBackgroundColour("green")
		submitbutton.SetToolTipString(self.t("submitlabel"))
		submitbutton.Bind(wx.EVT_BUTTON, self.Submit)
		pricesizer.Add(submitbutton, 0, wx.EXPAND)
		
		topsizer.Add(pricesizer, 0, wx.EXPAND)
		
		panel.SetSizer(topsizer)
		
		panel.descriptionentry = descriptionentry
		panel.priceentry = priceentry
		
		panel.Date = date
		panel.receiptid = receiptid
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		dialog.Fit()
		
		dialog.ShowModal()
	
	def ReceiptChangeLog(self, ID):
		
		listboxid = self.receiptlistbox.GetSelection()
		if listboxid > 0:
			
			receiptid = self.receiptlistbox.htmllist[listboxid][3]
			
			action = "SELECT ChangeLog, Description FROM receipt WHERE ID = " + str(receiptid)
			results = db.SendSQL(action, self.localsettings.dbconnection)
			
			changelog = results[0][0]
			description = results[0][1]
			
			
			miscmethods.ShowChangeLog(self.t("clientreceiptchangeloglabel") + description, changelog, self.localsettings.dbconnection)
			
	
	def Submit(self, ID):
		
		parent = ID.GetEventObject().GetParent()
		
		description = parent.descriptionentry.GetValue()
		
		price = parent.priceentry.GetValue()
		price = miscmethods.ConvertPriceToPennies(price)
		
		if price != -1:
			
			listboxid = self.receiptlistbox.GetSelection()
			
			if listboxid > 0:
				
				receiptid = parent.receiptid
				
				action = "SELECT * FROM receipt WHERE ID = " + str(receiptid)
				results = db.SendSQL(action, self.clientdata.localsettings.dbconnection)
				
				date = results[0][1]
				receipttype = results[0][4]
				receipttypeid = results[0][5]
				appointmentid = results[0][6]
				
			else:
				
				receiptid = False
				date = datetime.date.today()
				date = miscmethods.GetSQLDateFromDate(date)
				receipttype = 4
				receipttypeid = self.clientdata.ID
				appointmentid = 0
			
			dbmethods.WriteToReceiptTable(self.clientdata.localsettings.dbconnection, receiptid, date, description, price, receipttype, receipttypeid, appointmentid, self.clientdata.localsettings.userid)
			
			
			
			self.RefreshList()
			
			parent.GetParent().Close()
	
	def Delete(self, ID=False):
		
		if miscmethods.ConfirmMessage(self.t("clientreceiptdeletemessage")) == True:
			listboxid = self.receiptlistbox.GetSelection()
			receiptid = self.receiptlistbox.htmllist[listboxid][3]
			
			action = "DELETE FROM receipt WHERE ID = " + str(receiptid)
			db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			
			self.RefreshList()
	
	def ItemSelected(self, ID):
		
		listboxid = self.receiptlistbox.GetSelection()
		
		if listboxid != 0:
			
			self.editbutton.Enable()
			self.deletebutton.Enable()
			
		else:
			self.deletebutton.Disable()
			self.editbutton.Disable()
			
	
	def RecentBoxTicked(self, ID=False):
		
		if self.latestcheckbox.GetValue() == True:
			
			today = datetime.date.today()
			
			timedelta = datetime.timedelta(30)
			
			fromdate = today - timedelta
			
			todate = miscmethods.GetWXDateFromDate(today)
			fromdate = miscmethods.GetWXDateFromDate(fromdate)
			
			self.fromentry.SetValue(fromdate)
			self.fromentry.Disable()
			self.toentry.SetValue(todate)
			self.toentry.Disable()
		else:
			self.fromentry.Enable()
			self.toentry.Enable()
		
		self.RefreshList()
	
	def RefreshList(self, ID=False):
		
		fromdate = self.fromentry.GetValue()
		fromdate = miscmethods.GetSQLDateFromWXDate(fromdate)
		
		todate = self.toentry.GetValue()
		todate = miscmethods.GetSQLDateFromWXDate(todate)
		
		self.receiptlistbox.fromdate = fromdate
		self.receiptlistbox.todate = todate
		
		self.receiptlistbox.RefreshList()

class BillSummaryPanel(wx.Panel):
	
	def t(self, field):
		
		return  self.clientdata.localsettings.t(field)
	
	def __init__(self, parent, clientdata):
		
		self.clientdata = clientdata
		
		wx.Panel.__init__(self, parent)
		
		topsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		balancesizer = wx.BoxSizer(wx.VERTICAL)
		
		balancelabel = wx.StaticText(self, -1, self.t("clientbalancelabel"))
		font = balancelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		balancelabel.SetFont(font)
		balancesizer.Add(balancelabel, 0, wx.ALIGN_LEFT)
		
		balanceentry = wx.StaticText(self, -1, "")
		font = balanceentry.GetFont()
		font.SetPointSize(font.GetPointSize() + 4)
		balanceentry.SetFont(font)
		balancesizer.Add(balanceentry, 0, wx.ALIGN_CENTER)
		
		topsizer.Add(balancesizer, 0, wx.EXPAND)
		
		topsizer.Add(wx.StaticText(self, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		paymentsizer = wx.BoxSizer(wx.VERTICAL)
		
		paymentlabel = wx.StaticText(self, -1,self.t("clientpaymentlabel") + ":")
		font = paymentlabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		paymentlabel.SetFont(font)
		paymentsizer.Add(paymentlabel, 0, wx.ALIGN_LEFT)
		
		self.paymententry = wx.TextCtrl(self, -1, "")
		self.paymententry.Bind(wx.EVT_CHAR, self.KeyStroke)
		paymentsizer.Add(self.paymententry, 0, wx.EXPAND)
		
		topsizer.Add(paymentsizer, 0, wx.EXPAND)
		
		topsizer.Add(wx.StaticText(self, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		self.GetInvoiceIDs()
		
		self.invoicenumberselectsizer = wx.BoxSizer(wx.VERTICAL)
		
		invoicelabel = wx.StaticText(self, -1, self.t("invoiceidlabel"))
		invoicelabel.SetFont(font)
		self.invoicenumberselectsizer.Add(invoicelabel, 0, wx.ALIGN_LEFT)
		
		self.invoicenumberselect = wx.Choice(self, -1, choices=self.invoiceids)
		self.invoicenumberselect.SetSelection(0)
		self.invoicenumberselect.SetToolTipString(self.t("invoiceidchoicetooltip"))
		self.invoicenumberselectsizer.Add(self.invoicenumberselect, 0, wx.EXPAND)
		topsizer.Add(self.invoicenumberselectsizer, 0, wx.EXPAND)
		
		#submitbitmap = wx.Bitmap("icons/submit.png")
		#submitbutton = wx.BitmapButton(self, -1, submitbitmap)
		#submitbutton.SetToolTipString(self.t("clientsubmitpaymenttooltip"))
		#submitbutton.Bind(wx.EVT_BUTTON, self.Submit)
		#topsizer.Add(submitbutton, 0, wx.EXPAND)
		
		#spacer2 = wx.StaticText(self, -1, "", size=(-1,10))
		#topsizer.Add(spacer2, 0, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.topsizer = topsizer
		
		self.balanceentry = balanceentry
		
		self.clientpanel = parent.GetParent()
	
	def KeyStroke(self, ID):
		
		keycode = ID.GetKeyCode()
		
		if keycode == 13:
			
			self.Submit(ID)
		
		ID.Skip()
	
	def GetInvoiceIDs(self):
		
		action = "SELECT ID FROM invoice WHERE ClientID = " + str(self.clientdata.ID) + " AND Paid != Total"
		results = db.SendSQL(action, self.clientdata.localsettings.dbconnection)
		
		
		self.invoiceids = [self.t("invoiceidlabel"),]
		
		for a in results:
			
			self.invoiceids.append(str(a[0]))
	
	def ClearPaymentEntry(self, ID=False):
		
		self.paymententry.Clear()
	
	def GenerateBalance(self, ID=False):
		
		if self.clientpanel.receiptlistbox.totalprice < 0:
			colour = "red"
		else:
			colour = "green"
		
		balance = miscmethods.FormatPrice(self.clientpanel.receiptlistbox.totalprice)
		
		#output = "<center><u>" + self.t("clientbalancelabel") + "</u><br><font color=" + colour + " size=5><large>" + self.t("currency") + balance + "</large></font></center>"
		
		currencyunit = self.t("currency")
		
		if currencyunit == "&pound;":
			
			currencyunit = u"£"
		
		self.balanceentry.SetLabel(currencyunit + balance)
		self.balanceentry.SetForegroundColour(colour)
		#self.summarywindow.Refresh()
		
		if balance[0] == "-":
			
			balance = balance[1:]
			
			self.paymententry.SetValue(balance)
			
		else:
			
			self.paymententry.SetValue("0.00")
		
		self.GetInvoiceIDs()
		
		self.invoicenumberselect.Destroy()
		
		self.invoicenumberselect = wx.Choice(self, -1, choices=self.invoiceids)
		self.invoicenumberselect.SetToolTipString(self.t("invoiceidchoicetooltip"))
		self.invoicenumberselectsizer.Add(self.invoicenumberselect, 0, wx.EXPAND)
		self.invoicenumberselectsizer.Layout()
		
		self.clientpanel.invoicepanel.invoiceslistbox.RefreshList()
		
		self.topsizer.Layout()
	
	def Submit(self, ID):
		
		date = datetime.date.today()
		date = miscmethods.GetSQLDateFromDate(date)
		
		price = self.paymententry.GetValue()
		
		price = miscmethods.ConvertPriceToPennies(price)
		
		clientid = self.clientpanel.clientdata.ID
		
		if price != -1:
			
			invoiceselectionid = self.invoicenumberselect.GetSelection()
			
			if invoiceselectionid > 0:
				
				invoiceid = self.invoiceids[invoiceselectionid]
				
				action = "SELECT Paid FROM invoice WHERE ID = " + str(invoiceid)
				results = db.SendSQL(action, self.clientdata.localsettings.dbconnection)
				
				paid = results[0][0] + price
				
				action = "UPDATE invoice SET Paid = " + str(paid) + " WHERE ID = " + str(invoiceid)
				db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			dbmethods.WriteToReceiptTable(self.clientdata.localsettings.dbconnection, False, date, self.t("clientpaymentinreceiptlabel"), price, 4, clientid, 0, self.clientdata.localsettings.userid)
			
			
			
			self.clientpanel.receiptlistbox.RefreshList()
			
			self.GenerateBalance()

class AnimalsListbox(wx.HtmlListBox):
	
	def __init__(self, parent, clientdata):
		
		wx.HtmlListBox.__init__(self, parent)
		
		self.parent = parent
		self.clientdata = clientdata
		
		self.SetSelection(-1)
		self.htmllist = []
		
		self.SetItemCount(0)
	
	def OnGetItem(self, n):
		
		if len(self.htmllist) != 0:
			
			name = self.htmllist[n][1]
			sex = self.htmllist[n][2]
			species = self.htmllist[n][3]
			deceased = self.htmllist[n][5]
			asmref = self.htmllist[n][6]
			
			if deceased == 1:
				colour = "gray"
			elif sex == "Male":
				colour = "blue"
			elif sex == "Female":
				colour = "red"
			else:
				colour = "blank"
			
			if asmref == "":
				
				output = "<font color=" + colour + ">" + name + " (" + species + ")</font>"
				
			else:
				
				output = "<img src=icons/asm.png><font color=" + colour + ">&nbsp;" + name + " (" + species + ")</font>"
			
			
			#output = "<font color=" + colour + " size=4>" + name + " (" + species + ")</font>"
			
			return output
			
	def RefreshList(self):
		
		self.Hide()
		
		listboxid = self.GetSelection()
		
		if listboxid != -1:
			animalid = self.htmllist[listboxid][0]
		else:
			animalid = 0
		
		listboxid = -1
		
		self.htmllist = []
		
		action = "SELECT ID, Name, Sex, Species, Colour, IsDeceased, ASMRef FROM animal WHERE animal.OwnerID = " + str(self.clientdata.ID)
		
		if self.parent.animalsearchinput.GetValue() != "":
			
			action = action + " AND Name LIKE \'%" + self.parent.animalsearchinput.GetValue() + "%\'"
		
		action = action + " ORDER BY IsDeceased, Name"
		results = db.SendSQL(action, self.clientdata.localsettings.dbconnection)
		
		
		for a in range(0, len(results)):
			
			self.htmllist.append(results[a])
			
			if results[a][0] == animalid:
				
				listboxid = a
		
		self.parent.animaltotallabel.SetLabel(self.clientdata.localsettings.dictionary["totallabel"][self.clientdata.localsettings.language] + ": " + str(len(self.htmllist)))
		
		if len(self.htmllist) > 50:
			
			self.htmllist = []
		
		self.SetItemCount(len(self.htmllist))
		
		if len(self.htmllist) == 0:
			
                        self.Disable()
			
                else:
			
                        self.Enable()
		
		if listboxid == -1:
			
			self.parent.openanimalbutton.Disable()
			self.parent.deleteanimalbutton.Disable()
			self.parent.addappointmentbutton.Disable()
		
                self.SetSelection(listboxid)
                self.Refresh()
		self.Show()
		
		self.parent.animallistsizer.Layout()

class ClientInvoicePanel(wx.Panel):
	
	def t(self, field):
		
		return  self.clientdata.localsettings.t(field)
	
	def __init__(self, parent, clientdata):
		
		self.clientdata = clientdata
		
		self.clientpanel = parent.GetParent()
		
		wx.Panel.__init__(self, parent)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		invoiceslistbox = InvoicesListbox(self, self.clientdata)
		invoiceslistbox.listctrl.Bind(wx.EVT_RIGHT_DOWN, self.InvoicePopup)
		
		topsizer.Add(invoiceslistbox, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.invoiceslistbox = invoiceslistbox
		self.invoiceslistbox.RefreshList()
	
	def InvoicePopup(self, ID):
		
		popupmenu = wx.Menu()
		
		addinvoice = wx.MenuItem(popupmenu, ADD_INVOICE, self.t("addlabel"))
		addinvoice.SetBitmap(wx.Bitmap("icons/new.png"))
		popupmenu.AppendItem(addinvoice)
		wx.EVT_MENU(popupmenu, ADD_INVOICE, self.GenerateInvoice)
		
		if self.invoiceslistbox.GetSelection() > -1:
			
			viewinvoice = wx.MenuItem(popupmenu, VIEW_INVOICE, self.t("viewlabel"))
			viewinvoice.SetBitmap(wx.Bitmap("icons/view.png"))
			popupmenu.AppendItem(viewinvoice)
			wx.EVT_MENU(popupmenu, VIEW_INVOICE, self.ViewInvoice)
			
			editinvoice = wx.MenuItem(popupmenu, EDIT_INVOICE, self.t("editlabel"))
			editinvoice.SetBitmap(wx.Bitmap("icons/edit.png"))
			popupmenu.AppendItem(editinvoice)
			wx.EVT_MENU(popupmenu, EDIT_INVOICE, self.EditInvoicePayment)
			
			deleteinvoice = wx.MenuItem(popupmenu, DELETE_INVOICE, self.t("deletelabel"))
			deleteinvoice.SetBitmap(wx.Bitmap("icons/delete.png"))
			popupmenu.AppendItem(deleteinvoice)
			wx.EVT_MENU(popupmenu, DELETE_INVOICE, self.DeleteInvoice)
		
		popupmenu.AppendSeparator()
		
		refreshinvoice = wx.MenuItem(popupmenu, REFRESH_INVOICES, self.t("refreshlabel"))
		refreshinvoice.SetBitmap(wx.Bitmap("icons/refresh.png"))
		popupmenu.AppendItem(refreshinvoice)
		wx.EVT_MENU(popupmenu, REFRESH_INVOICES, self.invoiceslistbox.RefreshList)
		
		self.PopupMenu(popupmenu)
	
	def EditInvoicePayment(self, ID):
		
		listboxid = self.invoiceslistbox.GetSelection()
		invoiceid = self.invoiceslistbox.htmllist[listboxid][0]
		
		action = "SELECT Paid FROM invoice WHERE ID = " + str(invoiceid)
		results = db.SendSQL(action, self.clientdata.localsettings.dbconnection)
		
		paid = results[0][0]
		
		paid = miscmethods.FormatPrice(paid)
		
		dialog = wx.Dialog(self, -1, self.t("editinvoicepaymenttitle"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		panel.invoiceid = invoiceid
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		pricelabel = wx.StaticText(panel, -1, self.t("pricelabel"))
		font = pricelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		pricelabel.SetFont(font)
		
		topsizer.Add(pricelabel, 0, wx.ALIGN_LEFT)
		
		panel.paymentinput = wx.TextCtrl(panel, -1, paid, size=(100,-1))
		panel.paymentinput.Bind(wx.EVT_CHAR, self.PaymentKeyStroke)
		topsizer.Add(panel.paymentinput, 0, wx.ALIGN_CENTER)
		
		panel.SetSizer(topsizer)
		
		panel.paymentinput.SetFocus()
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		dialog.Fit()
		
		dialog.ShowModal()
	
	def PaymentKeyStroke(self, ID):
		
		keycode = ID.GetKeyCode()
		
		if keycode == 13:
			
			parent = ID.GetEventObject().GetParent()
			
			payment = parent.paymentinput.GetValue()
			
			payment = miscmethods.ConvertPriceToPennies(payment)
			
			self.UpdatePayment(payment, parent.invoiceid)
			
			parent.GetParent().Close()
		
		ID.Skip()
	
	def UpdatePayment(self, payment, invoiceid):
		
		action = "UPDATE invoice SET Paid = " + str(payment) + " WHERE ID = " + str(invoiceid)
		db.SendSQL(action, self.clientdata.localsettings.dbconnection)
		
		self.invoiceslistbox.RefreshList()
	
	def GenerateInvoice(self, ID):
		
		clientdata = self.clientdata
	
		dialog = wx.Dialog(self, -1, self.t("newinvoicetooltip"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		leftsizer = wx.BoxSizer(wx.VERTICAL)
		
		action = "SELECT Title FROM form WHERE FormType = \"invoice\""
		results = db.SendSQL(action, self.clientdata.localsettings.dbconnection)
		
		
		panel.listbox = wx.ListBox(panel, -1, size=(200,-1))
		panel.listboxtitles = []
		
		for a in results:
			panel.listbox.Append(a[0])
			panel.listboxtitles.append(a[0])
		
		if len(panel.listboxtitles) > 0:
			
			panel.listbox.SetSelection(0)
		
		leftsizer.Add(panel.listbox, 1, wx.EXPAND)
		
		horizontalsizer.Add(leftsizer, 0, wx.EXPAND)
		
		rightsizer = wx.BoxSizer(wx.VERTICAL)
		
		rightsizer.Add(wx.Panel(panel), 1, wx.EXPAND)
		
		#gridsizer = wx.FlexGridSizer(cols=2)
		
		fromlabel = wx.StaticText(panel, -1, self.t("fromlabel") + ":")
		font = fromlabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		fromlabel.SetFont(font)
		rightsizer.Add(fromlabel, 0, wx.EXPAND)
		
		fromentry = customwidgets.DateCtrl(panel, self.clientdata.localsettings)
		rightsizer.Add(fromentry, 0, wx.EXPAND)
		
		tolabel = wx.StaticText(panel, -1, self.t("tolabel") + ":")
		tolabel.SetFont(font)
		rightsizer.Add(tolabel, 0, wx.EXPAND)
		
		toentry = customwidgets.DateCtrl(panel, self.clientdata.localsettings)
		rightsizer.Add(toentry, 0, wx.EXPAND)
		
		rightsizer.Add(wx.Panel(panel), 1, wx.EXPAND)
		
		#submitbitmap = wx.Bitmap("icons/submit.png")
		submitbutton = wx.Button(panel, -1, self.t("submitlabel"))
		submitbutton.SetBackgroundColour("green")
		submitbutton.SetToolTipString(self.t("submitlabel"))
		submitbutton.Bind(wx.EVT_BUTTON, self.CreateInvoice)
		rightsizer.Add(submitbutton, 0, wx.ALIGN_CENTER)
		
		rightsizer.Add(wx.Panel(panel), 1, wx.EXPAND)
		
		horizontalsizer.Add(wx.StaticText(panel, -1, ""), 1, wx.EXPAND)
		
		horizontalsizer.Add(rightsizer, 2, wx.EXPAND)
		
		horizontalsizer.Add(wx.StaticText(panel, -1, ""), 1, wx.EXPAND)
		
		topsizer.Add(horizontalsizer, 1, wx.EXPAND)
		
		panel.SetSizer(topsizer)
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		panel.fromentry = fromentry
		panel.toentry = toentry
		
		dialog.ShowModal()
		
		self.clientpanel.receiptpanel.RefreshList()
	
	def CreateInvoice(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		listboxid = panel.listbox.GetSelection()
		formname = panel.listboxtitles[listboxid]
		
		dialog = panel.GetParent()
		
		clientpanel = dialog.GetParent().clientpanel
		
		fromdate = panel.fromentry.GetValue()
		fromdate = miscmethods.GetSQLDateFromWXDate(fromdate)
		
		todate = panel.toentry.GetValue()
		todate = miscmethods.GetSQLDateFromWXDate(todate)
		
		action = "SELECT ID FROM invoice WHERE ClientID = " + str(self.clientdata.ID) + " AND ( \"" + fromdate + "\" BETWEEN FromDate AND ToDate OR \"" + todate + "\" BETWEEN FromDate AND ToDate OR FromDate BETWEEN \"" + fromdate + "\" AND \"" + todate + "\" OR ToDate BETWEEN \"" + fromdate + "\" AND \"" + todate + "\" )"
		results = db.SendSQL(action, self.clientdata.localsettings.dbconnection)
		
		if len(results) > 0:
			
			
			miscmethods.ShowMessage(self.t("invoiceoverlapmessage"))
			
		else:
			
			action = "SELECT receipt.Date, receipt.Price, receipt.Description, receipt.ID FROM receipt WHERE receipt.Type = 4 AND receipt.TypeID = " + str(self.clientdata.ID) + " AND receipt.Date BETWEEN \"" + fromdate + "\" AND \"" + todate + "\""
			
			results1 = db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			action = "SELECT receipt.Date, receipt.Price, receipt.Description, receipt.ID FROM appointment LEFT JOIN receipt ON appointment.ID = receipt.AppointmentID WHERE appointment.OwnerID = " + str(self.clientdata.ID) + " AND receipt.Date BETWEEN \"" + fromdate + "\" AND \"" + todate + "\""
			
			results2 = db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			
			results = results1 + results2
			
			results = list(results)
			
			results.sort()
			
			totalprice = 0
			
			for a in results:
				totalprice = totalprice + a[1]
			
			htmllist = results
			
			listboxid = panel.listbox.GetSelection()
			title = panel.listboxtitles[listboxid]
			
			totalprice = totalprice * -1
			
			invoicebreakdown = "<table cellpadding=5><tr><td><u>" + self.clientdata.localsettings.dictionary["datelabel"][self.clientdata.localsettings.language] + "</u></td><td></td><td align=right><u>" + self.clientdata.localsettings.dictionary["pricelabel"][self.clientdata.localsettings.language] + "</u></td></tr>"
			
			for a in htmllist:
				
				if a[1] < 0:
					colour = "red"
					price = a[1] * -1
				else:
					colour = "green"
					price = a[1]
				
				price = "<font color=" + colour + ">" + str(miscmethods.FormatPrice(price)) + "</font>"
				
				invoicebreakdown = invoicebreakdown + "<tr><td>" + miscmethods.FormatSQLDate(str(a[0]), self.clientdata.localsettings) + "</td><td>" + unicode(a[2], "utf8") + "</td><td align=right>" + price + "</td></tr>"
			
			invoicebreakdown = invoicebreakdown + "</table>"
			
			action = "SELECT Body FROM form WHERE Title = \"" + formname + "\" AND FormType = \"invoice\""
			results = db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			
			body = unicode(results[0][0], "utf-8")
			
			clientname = self.clientdata.title + " " + self.clientdata.forenames + " " + self.clientdata.surname
			clientaddress = self.clientdata.address.replace("\n", "<br>")
			
			time = datetime.datetime.today()
			
			todaysdate = time.strftime("%A %d %B %Y")
			
			invoiceid = dbmethods.WriteToInvoiceTable(self.clientdata.localsettings.dbconnection, False, self.clientdata.ID, fromdate, todate, totalprice, "")
			
			body = body.replace("<<ClientName>>", clientname).replace("<<ClientAddress>>", clientaddress).replace("<<ClientPostcode>>", self.clientdata.postcode).replace("<<ClientHomeTelephone>>", self.clientdata.hometelephone).replace("<<ClientMobileTelephone>>", self.clientdata.mobiletelephone).replace("<<ClientWorkTelephone>>", self.clientdata.worktelephone).replace("<<ClientEmailAddress>>", self.clientdata.emailaddress).replace("<<ClientComments>>", unicode(self.clientdata.comments, "utf-8")).replace("<<Today>>", todaysdate).replace("<<PracticeName>>", self.clientdata.localsettings.practicename).replace("<<PracticeAddress>>", self.clientdata.localsettings.practiceaddress.replace("\n", "<br>")).replace("<<PracticePostcode>>", self.clientdata.localsettings.practicepostcode).replace("<<PracticeTelephone>>", self.clientdata.localsettings.practicetelephone).replace("<<InvoiceBreakdown>>", invoicebreakdown).replace("<<InvoiceTotal>>", miscmethods.FormatPrice(totalprice)).replace("<<FromDate>>", miscmethods.FormatSQLDate(fromdate, self.clientdata.localsettings)).replace("<<ToDate>>", miscmethods.FormatSQLDate(todate, self.clientdata.localsettings)).replace("<<InvoiceNumber>>", str(invoiceid))
			
			invoiceid = dbmethods.WriteToInvoiceTable(self.clientdata.localsettings.dbconnection, invoiceid, self.clientdata.ID, fromdate, todate, totalprice, body)
			
			self.invoiceslistbox.RefreshList()
			
			formmethods.BuildForm(self.clientdata.localsettings, body)
			
			dialog.Close()
			
			self.clientpanel.receiptpanel.RefreshList()
	
	def DeleteInvoice(self, ID=False):
		
		if miscmethods.ConfirmMessage("Are you sure that you want to delete this invoice?"):
			
			listboxid = self.invoiceslistbox.GetSelection()
			invoiceid = self.invoiceslistbox.htmllist[listboxid][0]
			
			action = "DELETE FROM invoice WHERE ID = " + str(invoiceid)
			db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			self.invoiceslistbox.RefreshList()
			
			self.clientpanel.receiptpanel.RefreshList()
	
	def ViewInvoice(self, ID=False):
		
		listboxid = self.invoiceslistbox.GetSelection()
		body = self.invoiceslistbox.htmllist[listboxid][5]
		
		formmethods.BuildForm(self.clientdata.localsettings, body)

def ChooseClientForm(parent):
	
	clientdata = parent.clientdata
	
	dialog = wx.Dialog(parent, -1, "Choose a template")
	
	dialogsizer = wx.BoxSizer(wx.VERTICAL)
	
	panel = wx.Panel(dialog)
	
	panel.clientdata = clientdata
	
	topsizer = wx.BoxSizer(wx.VERTICAL)
	
	action = "SELECT Title FROM form WHERE FormType = \"client\""
	results = db.SendSQL(action, clientdata.localsettings.dbconnection)
	
	
	panel.listbox = wx.ListBox(panel, -1)
	panel.listboxtitles = []
	
	for a in results:
		panel.listbox.Append(a[0])
		panel.listboxtitles.append(a[0])
	
	if len(panel.listboxtitles) > 0:
		
		panel.listbox.SetSelection(0)
	
	topsizer.Add(panel.listbox, 1, wx.EXPAND)
	
	submitbutton = wx.Button(panel, -1, "Submit")
	submitbutton.Bind(wx.EVT_BUTTON, GenerateClientForm)
	topsizer.Add(submitbutton, 0, wx.ALIGN_CENTER)
	
	panel.SetSizer(topsizer)
	
	dialogsizer.Add(panel, 1, wx.EXPAND)
	
	dialog.SetSizer(dialogsizer)
	
	dialog.ShowModal()

def GenerateClientForm(ID):
	
	panel = ID.GetEventObject().GetParent()
	dialog = panel.GetParent()
	
	#clientpanel = dialog.GetParent().clientpanel
	
	listboxid = panel.listbox.GetSelection()
	title = panel.listboxtitles[listboxid]
	
	formmethods.GenerateClientForm(title, panel.clientdata)
	
	dialog.Close()

class InvoicesListbox(customwidgets.ListCtrlWrapper):
	
	def t(self, field):
		
		return  self.localsettings.t(field)
	
	def __init__(self, parent, clientdata):
		
		self.htmllist = []
		self.localsettings = clientdata.localsettings
		self.parent = parent
		self.clientdata = clientdata
		
		columnheadings = (self.t("invoiceidlabel"), self.t("fromlabel"), self.t("tolabel"), self.t("totallabel"), self.t("paidlabel"))
		
		imageslist = ("icons/ontime.png", "icons/dna.png")
		
		customwidgets.ListCtrlWrapper.__init__(self, parent, clientdata.localsettings, columnheadings, imageslist)
	
	def ProcessRow(self, rowdata):
		
		invoiceid = rowdata[0]
		fromdate = miscmethods.FormatSQLDate(rowdata[2], self.localsettings)
		todate = miscmethods.FormatSQLDate(rowdata[3], self.localsettings)
		
		currency = self.t("currency")
		
		if currency == "&pound;":
			
			currency = u"£"
		
		total = currency + miscmethods.FormatPrice(rowdata[4])
		paid = currency + miscmethods.FormatPrice(rowdata[6])
		
		if rowdata[6] < rowdata[4]:
			
			imageid = 1
			
		else:
			
			imageid = 0
		
		output = ((invoiceid, str(invoiceid), fromdate, todate, total, paid), imageid)
		
		return output
			
	def RefreshList(self, ID=False):
		
		action = "SELECT * FROM invoice WHERE ClientID = " + str(self.clientdata.ID) + " ORDER BY FromDate"
		self.htmllist = db.SendSQL(action, self.localsettings.dbconnection)
		
		customwidgets.ListCtrlWrapper.RefreshList(self)

#class InvoicesListbox(wx.HtmlListBox):
	
	#def t(self, field):
		
		#return  self.clientdata.localsettings.t(field)
	
	#def __init__(self, parent, clientdata):
		
		#self.clientdata = clientdata
		
		#wx.HtmlListBox.__init__(self, parent)
		
		#self.parent = parent
		
		#self.SetSelection(-1)
		#self.htmllist = []
		
		#self.SetItemCount(0)
	
	#def OnGetItem(self, n):
		
		#if len(self.htmllist) != 0:
			
			#if self.htmllist[n][6] != self.htmllist[n][4]:
				
				#invoicepaid = "<font size=2 color=red>" + self.t("paidlabel") + " " + self.t("currency") + miscmethods.FormatPrice(self.htmllist[n][6]) + "</font>"
				
			#else:
				
				#invoicepaid = "<font size=2 color=green>" + self.t("paidlabel") + " " + self.t("currency") + miscmethods.FormatPrice(self.htmllist[n][6]) + "</font>"
			
			#output = "<table cellpadding=0 cellspacing=5><tr><td><font size=2 color=red>#" + str(self.htmllist[n][0]) + "</font></td><td><font size=2 color=blue> " + self.t("fromlabel").lower() + " " + miscmethods.FormatSQLDate(self.htmllist[n][2], self.clientdata.localsettings) + " " + self.t("tolabel").lower() + " " + miscmethods.FormatSQLDate(self.htmllist[n][3], self.clientdata.localsettings) + "</font></td><td><font size=2 color=red>" + self.t("totallabel") + ": " + self.t("currency") + miscmethods.FormatPrice(self.htmllist[n][4]) + "</font></td><td>" + invoicepaid + "</td>"
			
			#output = output + "</tr></table>"
			
			#return output
			
	#def RefreshList(self, ID=False):
		
		#self.Hide()
		
		#action = "SELECT * FROM invoice WHERE ClientID = " + str(self.clientdata.ID) + " ORDER BY FromDate"
		#self.htmllist = db.SendSQL(action, self.clientdata.localsettings.dbconnection)
		
		
		#self.SetItemCount(len(self.htmllist))
		#self.Refresh()
		#self.SetSelection(-1)
		#self.Show()

class FindClientDialog(wx.Dialog, listmix.ColumnSorterMixin):
	
	def t(self, field):
		
		return  self.localsettings.t(field)
	
	def __init__(self, parent, localsettings):
		
		self.parent = parent
		self.localsettings = localsettings
		
		wx.Dialog.__init__(self, parent, -1, self.t("clientsearchpagetitle"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(self)
		
		topsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		inputsizer = wx.BoxSizer(wx.VERTICAL)
		
		namelabel = wx.StaticText(panel, -1, self.t("namelabel"))
		font = namelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		namelabel.SetFont(font)
		inputsizer.Add(namelabel, 0, wx.ALIGN_LEFT)
		
		nameentry = wx.TextCtrl(panel, -1, "", size=(100,-1), style=wx.TE_PROCESS_ENTER)
		nameentry.Bind(wx.EVT_CHAR, self.ButtonPressed)
		nameentry.SetFocus()
		inputsizer.Add(nameentry, 0, wx.EXPAND)
		
		addresslabel = wx.StaticText(panel, -1, self.t("clientaddresslabel"))
		addresslabel.SetFont(font)
		inputsizer.Add(addresslabel, 0, wx.ALIGN_LEFT)
		
		addressentry = wx.TextCtrl(panel, -1, "", style=wx.TE_PROCESS_ENTER)
		addressentry.Bind(wx.EVT_CHAR, self.ButtonPressed)
		inputsizer.Add(addressentry, 0, wx.EXPAND)
		
		postcodelabel = wx.StaticText(panel, -1, self.t("clientpostcodelabel"))
		postcodelabel.SetFont(font)
		inputsizer.Add(postcodelabel, 0, wx.ALIGN_LEFT)
		
		postcodeentry = wx.TextCtrl(panel, -1, "", style=wx.TE_PROCESS_ENTER)
		postcodeentry.Bind(wx.EVT_CHAR, self.ButtonPressed)
		inputsizer.Add(postcodeentry, 0, wx.EXPAND)
		
		inputsizer.Add(wx.StaticText(panel, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		topsizer.Add(inputsizer, 0, wx.EXPAND)
		
		topsizer.Add(wx.StaticText(panel, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		#listbox = wx.ListBox(panel, size=(300,200))
		self.listctrl = wx.ListCtrl(panel, -1, size=(500, 300), style=wx.LC_REPORT)
		listmix.ColumnSorterMixin.__init__(self, 4)
		
		self.listctrl.InsertColumn(0,self.t("namelabel"))
		self.listctrl.InsertColumn(1,self.t("clientaddresslabel"))
		self.listctrl.InsertColumn(2,self.t("clientpostcodelabel"))
		
		self.listctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
		self.listctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
		self.listctrl.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
		
		self.listctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.ClientSelected)
		self.listctrl.SetToolTipString(self.t("doubleclicktoselecttooltip"))
		topsizer.Add(self.listctrl, 1, wx.EXPAND)
		
		panel.SetSizer(topsizer)
		
		panel.nameentry = nameentry
		panel.addressentry = addressentry
		panel.postcodeentry = postcodeentry
		
		panel.listctrl = self.listctrl
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		self.SetSizer(dialogsizer)
		
		self.Fit()
		
		self.ShowModal()
	
	def GetListCtrl(self):# Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
		
        	return self.listctrl
	
	def ButtonPressed(self, ID):
		
		keycode = ID.GetKeyCode()
		
		if keycode == 13:
			
			self.Search(ID)
		
		ID.Skip()
	
	def Search(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		name = panel.nameentry.GetValue()
		address = panel.addressentry.GetValue()
		postcode = panel.postcodeentry.GetValue()
		
		action = "SELECT ID, ClientTitle, ClientForenames, ClientSurname, ClientAddress, ClientPostcode  FROM client WHERE CONCAT(ClientTitle, \" \", ClientForenames, \" \", ClientSurname) LIKE \"%" + name + "%\" AND ClientAddress LIKE \"%" + address + "%\" AND ClientPostcode LIKE \"%" + postcode + "%\""
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		self.itemDataMap = {}
		
		self.listctrl.ClearAll()
		
		self.listctrl.InsertColumn(0,self.t("namelabel"))
		self.listctrl.InsertColumn(1,self.t("clientaddresslabel"))
		self.listctrl.InsertColumn(2,self.t("clientpostcodelabel"))
		
		count = 0
		
		for a in results:
			
			name = ""
			
			if a[1] != "":
				
				name = name + a[1] + " "
			
			if a[2] != "":
				
				name = name + a[2] + " "
			
			if a[3] != "":
				
				name = name + a[3]
			
			self.itemDataMap[a[0]] = ( name, a[4], a[5] )
			
			self.listctrl.InsertStringItem(count, name)
			self.listctrl.SetStringItem(count, 1, a[4].replace("\r", "").replace("\n", ", "))
			self.listctrl.SetStringItem(count, 2, a[5])
			
			self.listctrl.SetItemData(count, a[0])
			
			#panel.listbox.Append(a[1] + " " + a[2] + " " + a[3] + ". " + a[4].replace("\r", "").replace("\n", ", ") + ". " + a[5])
			
			count = count + 1
		
		if len(results) == 0:
			
			self.listctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
			self.listctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
			self.listctrl.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
			
		else:
			
			self.listctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
			self.listctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE)
			self.listctrl.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
		
		self.clientsdata = results
	
	def ClientSelected(self, ID):
		
		listboxid = self.listctrl.GetFocusedItem()
		clientid = self.listctrl.GetItemData(listboxid)
		
		self.parent.clientdialogid = clientid
		
		self.Close()

class ASMClientImport:
	
	def t(self, field):
		
		return  self.localsettings.t(field)
	
	def __init__(self, notebook, localsettings, opennewclient=True):
		
		self.notebook = notebook
		self.localsettings = localsettings
		self.outputvar = 0
		self.opennewclient = opennewclient
		
		busy = wx.BusyCursor()
		
		asmconnection = db.GetASMConnection()
		
		dialog = wx.Dialog(self.notebook, -1, self.t("chooseclientlabel"))
		
		iconFile = "icons/asm.ico"
		icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
		dialog.SetIcon(icon1)
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		topsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		inputsizer = wx.BoxSizer(wx.VERTICAL)
		
		namelabel = wx.StaticText(panel, -1, self.t("namelabel"))
		font = namelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		namelabel.SetFont(font)
		inputsizer.Add(namelabel, 0, wx.ALIGN_LEFT)
		
		nameentry = wx.TextCtrl(panel, -1, "", size=(100,-1), style=wx.TE_PROCESS_ENTER)
		nameentry.SetFocus()
		nameentry.Bind(wx.EVT_CHAR, self.ASMClientImportButtonPressed)
		inputsizer.Add(nameentry, 0, wx.EXPAND)
		
		addresslabel = wx.StaticText(panel, -1, self.t("clientaddresslabel"))
		addresslabel.SetFont(font)
		inputsizer.Add(addresslabel, 0, wx.ALIGN_LEFT)
		
		addressentry = wx.TextCtrl(panel, -1, "", size=(100,-1), style=wx.TE_PROCESS_ENTER)
		addressentry.Bind(wx.EVT_CHAR, self.ASMClientImportButtonPressed)
		inputsizer.Add(addressentry, 0, wx.EXPAND)
		
		postcodelabel = wx.StaticText(panel, -1, self.t("clientpostcodelabel"))
		postcodelabel.SetFont(font)
		inputsizer.Add(postcodelabel, 0, wx.ALIGN_LEFT)
		
		postcodeentry = wx.TextCtrl(panel, -1, "", style=wx.TE_PROCESS_ENTER)
		postcodeentry.Bind(wx.EVT_CHAR, self.ASMClientImportButtonPressed)
		inputsizer.Add(postcodeentry, 0, wx.EXPAND)
		
		inputsizer.Add(wx.StaticText(panel, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		topsizer.Add(inputsizer, 0, wx.EXPAND)
		
		resultssizer = wx.BoxSizer(wx.VERTICAL)
		
		listbox = customwidgets.ClientImportListCtrl(panel, self.localsettings)
		listbox.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.SubmitASMClientImport)
		listbox.SetToolTipString(self.t("doubleclicktoselecttooltip"))
		customwidgets.ListCtrlWrapper.RefreshList(listbox)
		resultssizer.Add(listbox, 1, wx.EXPAND)
		
		totallabel = wx.StaticText(panel, -1, self.t("totallabel") + ": 0 ")
		resultssizer.Add(totallabel, 0, wx.ALIGN_RIGHT)
		
		topsizer.Add(wx.StaticText(panel, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		topsizer.Add(resultssizer, 1, wx.EXPAND)
		
		panel.SetSizer(topsizer)
		
		panel.nameentry = nameentry
		panel.addressentry = addressentry
		panel.postcodeentry = postcodeentry
		
		panel.totallabel = totallabel
		panel.resultssizer = resultssizer
		
		panel.asmconnection = asmconnection
		
		panel.listbox = listbox
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		dialog.SetSize((400,300))
		
		del busy
		
		dialog.ShowModal()
	
	def ASMClientImportButtonPressed(self, ID):
		
		keycode = ID.GetKeyCode()
		
		if keycode == 13:
			
			self.ASMClientSearch(ID)
		
		ID.Skip()
	
	def ASMClientSearch(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		panel.listbox.RefreshList()
	
	def SubmitASMClientImport(self, ID):
		
		#print "Submiting ASM Client Import"
		
		panel = ID.GetEventObject().GetParent().parent
		
		listboxid = panel.listbox.GetSelection()
		
		if listboxid != -1:
			
			#ID, OwnerName, OwnerAddress, OwnerPostcode, OwnerTitle, OwnerForenames, OwnerSurname, HomeTelephone, MobileTelephone, WorkTelephone, EmailAddress, Comments
			
			clientdata = panel.clientdata[listboxid]
			
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
			
			action = "SELECT ID, ClientTitle, ClientForenames, ClientSurname, ClientAddress FROM client WHERE ClientPostCode = \"" + postcode + "\" OR ClientSurname = \"" + surname + "\""
			evetteowners = db.SendSQL(action, self.localsettings.dbconnection)
			
			possiblematches = []
			
			asmhousenumber = address.split(" ")[0]
			
			for a in evetteowners:
				
				evettehousenumber = a[4].split(" ")[0]
				
				if asmhousenumber == evettehousenumber:
					
					possiblematches.append(a)
					
				else:
					
					if forenames == "" or a[2] == "" or forenames == a[2]:
						
						possiblematches.append(a)
			
			selectedownerid = 0
			
			panel.chosenownerid = 0
			
			if len(possiblematches) > 0:
				
				panel.possiblematches = possiblematches
				
				dialog = wx.Dialog(panel, -1, "Possible Owners")
				
				dialog.panel = panel
				
				topsizer = wx.BoxSizer(wx.VERTICAL)
				
				sheltermanagerownerinfo = wx.StaticText(dialog, -1, title + " " + forenames + " " + surname + ". " + address.replace("\n", ", ").replace("\r", "") + ". " + postcode)
				
				topsizer.Add(sheltermanagerownerinfo, 0, wx.EXPAND)
				
				topsizer.Add(wx.StaticText(dialog, -1, "", size=(-1,10)))
				
				chooseownerlabel = wx.StaticText(dialog, -1, "Choose an owner")
				topsizer.Add(chooseownerlabel, 0, wx.ALIGN_LEFT)
				
				dialog.listbox = wx.ListBox(dialog)
				dialog.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.SelectExistingOwner)
				
				for v in possiblematches:
					
					listboxoutput = v[1] + " " + v[2] + " " + v[3] + ". " + v[4].replace("\n", ", ").replace("\r", "")
					
					dialog.listbox.Append(listboxoutput)
				
				topsizer.Add(dialog.listbox, 1, wx.EXPAND)
				
				dialog.SetSizer(topsizer)
				
				dialog.ShowModal()
				
				clientid = panel.chosenownerid
				
			if panel.chosenownerid == 0:
				
				clientsettings = ClientSettings(self.localsettings)
				
				clientsettings.title = str(title)
				clientsettings.forenames = str(forenames)
				clientsettings.surname = str(surname)
				clientsettings.address = str(address)
				clientsettings.postcode = str(postcode)
				clientsettings.hometelephone = str(hometelephone)
				clientsettings.mobiletelephone = str(mobiletelephone)
				clientsettings.worktelephone = str(worktelephone)
				clientsettings.emailaddress = str(emailaddress)
				clientsettings.comments = "Imported from ASM:\n" + str(comments)
				
				clientsettings.Submit()
				
				clientid = clientsettings.ID
				
				panel.GetParent().Close()
				
				self.outputvar = clientid
				
				if self.opennewclient == True:
					
					clientpanel = ClientPanel(self.notebook, clientsettings)
					
					self.notebook.AddPage(clientpanel)
				
			else:
				
				clientid = 0
	
	def SelectExistingOwner(self, ID):
		
		dialog = ID.GetEventObject().GetParent()
		
		listboxid = dialog.listbox.GetSelection()
		
		panel = dialog.panel
		
		panel.chosenownerid = panel.possiblematches[listboxid][0]
		
		self.outputvar = panel.chosenownerid
		
		if self.opennewclient == True:
			
			clientsettings = ClientSettings(self.localsettings, panel.chosenownerid)
			
			clientpanel = ClientPanel(self.notebook, clientsettings)
			
			self.notebook.AddPage(clientpanel)
		
		dialog.GetGrandParent().Close()
		
		dialog.Close()
	
	def SelectOwner(self, ID):
		
		dialog = ID.GetEventObject().GetParent()
		
		listboxid = dialog.listbox.GetSelection()
		
		panel = dialog.panel
		
		panel.chosenownerid = panel.possiblematches[listboxid][0]
		
		dialog.Close()

class CheckForExistingClient:
	
	def t(self, label):
		
		return miscmethods.t(label, self.localsettings)
	
	def __init__(self, parent, clientdata, notebook=False):
		
		self.parent = parent
		self.clientdata = clientdata
		self.localsettings = self.clientdata.localsettings
		self.notebook = notebook
		
		addresslist = self.clientdata.address.split("\n")
		
		possiblematches = []
		
		if len(addresslist) > 0:
			
			firstline = addresslist[0]
			
			action = "SELECT ID, ClientTitle, ClientForenames, ClientSurname, ClientAddress, ClientPostcode FROM client WHERE ClientAddress LIKE \"" + firstline + "%\""
			results = db.SendSQL(action, self.clientdata.localsettings.dbconnection)
			
			for a in results:
				
				possiblematches.append(a)
			
			if len(possiblematches) > 0:
				
				if miscmethods.ConfirmMessage(self.t("possibleduplicateownermessage"), self.parent):
					
					dialog = wx.Dialog(self.parent, -1, self.t("animalownerlabel"))
					
					dialogsizer = wx.BoxSizer(wx.VERTICAL)
					
					panel = wx.Panel(dialog)
					
					topsizer = wx.BoxSizer(wx.VERTICAL)
					
					listbox = wx.ListBox(panel, size=(300,200))
					listbox.SetToolTipString(self.t("doubleclicktoselecttooltip"))
					listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.SelectClient)
					topsizer.Add(listbox, 1, wx.EXPAND)
					
					for a in possiblematches:
						
						name = ""
						
						if a[1] != "":
							
							name = name + a[1] + " "
						
						if a[2] != "":
							
							name = name + a[2] + " "
						
						if a[3] != "":
							
							name = name + a[3]
						
						
						listbox.Append(name + ". " + a[4].replace("\r", "").replace("\n", ", ") + ". " + a[5].upper() )
					
					panel.SetSizer(topsizer)
					
					panel.listbox = listbox
					panel.possiblematches = possiblematches
					
					dialogsizer.Add(panel, 1, wx.EXPAND)
					
					dialog.SetSizer(dialogsizer)
					
					dialog.Fit()
					
					dialog.ShowModal()
		
	def SelectClient(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		listboxid = panel.listbox.GetSelection()
		
		clientid = panel.possiblematches[listboxid][0]
		
		self.clientdata = ClientSettings(self.localsettings, clientid)
		
		if self.notebook != False:
			
			clientpanel = ClientPanel(self.notebook, self.clientdata)
			
			self.notebook.AddPage(clientpanel)
		
		panel.GetParent().Close()
