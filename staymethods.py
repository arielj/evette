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
import db
import dbmethods
import miscmethods
import customwidgets
import appointmentmethods
import vetmethods
import datetime
import animalmethods
import clientmethods

EDIT_VETFORM = 7001
EDIT_APPOINTMENT = 7002
DISCHARGE = 7003
EDIT_ANIMAL = 7004
EDIT_CLIENT = 7005
ADD_BLOCK = 7006
EDIT_BLOCK = 7007
DELETE_BLOCK = 7008
REFRESH_BLOCKS = 7009
EDIT_KENNEL = 7010
DELETE_KENNEL = 7011
REFRESH_KENNELS = 7012
ADD_KENNEL = 7013

class EditKennelsPanel(wx.Panel):
	
	def GetLabel(self, field):
		
		return  self.localsettings.dictionary[field][self.localsettings.language]
	
	def __init__(self, notebook, localsettings):
		
		self.localsettings = localsettings
		
		wx.Panel.__init__(self, notebook)
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, self.GetLabel("editkennelsmenu")[0])
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.kennelblockpanel = KennelBlockPanel(self, localsettings)
		horizontalsizer.Add(self.kennelblockpanel, 2, wx.EXPAND)
		
		horizontalsizer.Add(wx.StaticText(self, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		self.kennelspanel = KennelsPanel(self, localsettings)
		horizontalsizer.Add(self.kennelspanel, 3, wx.EXPAND)
		
		topsizer.Add(horizontalsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.kennelblockpanel.listbox.RefreshList()

class KennelBlockPanel(wx.Panel):
	
	
	def GetLabel(self, field):
		
		return  self.localsettings.dictionary[field][self.localsettings.language]
	
	def __init__(self, parent, localsettings):
		
		self.localsettings = localsettings
		
		wx.Panel.__init__(self, parent)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		titlelabel = wx.StaticText(self, -1, miscmethods.NoWrap(self.GetLabel("kennelblocktitlelabel")))
		font = titlelabel.GetFont()
		font.SetPointSize(font.GetPointSize() + 4)
		titlelabel.SetFont(font)
		topsizer.Add(titlelabel, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		#buttonssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		#newbitmap = wx.Bitmap("icons/new.png")
		#newbutton = wx.BitmapButton(self, -1, newbitmap)
		#newbutton.SetToolTipString(self.GetLabel("addkennelblocktooltip"))
		#newbutton.Bind(wx.EVT_BUTTON, self.AddKennelBlock)
		#buttonssizer.Add(newbutton, 0, wx.EXPAND)
		
		#editbitmap = wx.Bitmap("icons/edit.png")
		#editbutton = wx.BitmapButton(self, -1, editbitmap)
		#editbutton.SetToolTipString(self.GetLabel("editkennelblocktitle"))
		#editbutton.Bind(wx.EVT_BUTTON, self.EditKennelBlock)
		#buttonssizer.Add(editbutton, 0, wx.EXPAND)
		
		#deletebitmap = wx.Bitmap("icons/delete.png")
		#deletebutton = wx.BitmapButton(self, -1, deletebitmap)
		#deletebutton.SetToolTipString(self.GetLabel("deletelabel"))
		#deletebutton.Bind(wx.EVT_BUTTON, self.DeleteKennelBlock)
		#buttonssizer.Add(deletebutton, 0, wx.EXPAND)
		
		#buttonssizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		#refreshbitmap = wx.Bitmap("icons/refresh.png")
		#refreshbutton = wx.BitmapButton(self, -1, refreshbitmap)
		#refreshbutton.SetToolTipString(self.GetLabel("lookupsrefreshtooltip"))
		#refreshbutton.Bind(wx.EVT_BUTTON, self.RefreshList)
		#buttonssizer.Add(refreshbutton, 0, wx.EXPAND)
		
		#topsizer.Add(buttonssizer, 0, wx.EXPAND)
		
		listbox = KennelBlockListbox(self, localsettings)
		listbox.Bind(wx.EVT_LISTBOX, self.ItemSelected)
		listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EditKennelBlock)
		listbox.Bind(wx.EVT_RIGHT_DOWN, self.BlocksPopup)
		
		topsizer.Add(listbox, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.parent = parent
		
		self.listbox = listbox
		#self.editbutton = editbutton
		#self.deletebutton = deletebutton
	
	def BlocksPopup(self, ID):
		
		popupmenu = wx.Menu()
		
		addblock = wx.MenuItem(popupmenu, ADD_BLOCK, self.GetLabel("addlabel"))
		addblock.SetBitmap(wx.Bitmap("icons/new.png"))
		popupmenu.AppendItem(addblock)
		wx.EVT_MENU(popupmenu, ADD_BLOCK, self.AddKennelBlock)
		
		if self.listbox.GetSelection() > -1:
			
			editblock = wx.MenuItem(popupmenu, EDIT_BLOCK, self.GetLabel("editlabel"))
			editblock.SetBitmap(wx.Bitmap("icons/new.png"))
			popupmenu.AppendItem(editblock)
			wx.EVT_MENU(popupmenu, EDIT_BLOCK, self.EditKennelBlock)
			
			deleteblock = wx.MenuItem(popupmenu, DELETE_BLOCK, self.GetLabel("deletelabel"))
			deleteblock.SetBitmap(wx.Bitmap("icons/new.png"))
			popupmenu.AppendItem(deleteblock)
			wx.EVT_MENU(popupmenu, DELETE_BLOCK, self.DeleteKennelBlock)
		
		popupmenu.AppendSeparator()
		
		refresh = wx.MenuItem(popupmenu, REFRESH_BLOCKS, self.GetLabel("refreshlabel"))
		refresh.SetBitmap(wx.Bitmap("icons/refresh.png"))
		popupmenu.AppendItem(refresh)
		wx.EVT_MENU(popupmenu, REFRESH_BLOCKS, self.RefreshList)
		
		self.PopupMenu(popupmenu)
	
	def RefreshList(self, ID):
		
		self.listbox.RefreshList()
	
	def ItemSelected(self, ID):
		
		#self.editbutton.Enable()
		#self.deletebutton.Enable()
		listboxid = self.listbox.GetSelection()
		self.listbox.selectedid = self.listbox.htmllist[listboxid][0]
		
		self.parent.kennelspanel.kennelblockid = self.listbox.htmllist[listboxid][0]
		self.parent.kennelspanel.listbox.SetSelection(-1)
		self.parent.kennelspanel.listbox.RefreshList()
		self.parent.kennelspanel.Enable()
	
	def AddKennelBlock(self, ID):
		
		self.listbox.selectedid = 0
		self.EditKennelBlockDialog()
	
	def EditKennelBlock(self, ID):
		
		listboxid = self.listbox.GetSelection()
		
		kennelblockid = self.listbox.htmllist[listboxid][0]
		name = self.listbox.htmllist[listboxid][1]
		description = self.listbox.htmllist[listboxid][2]
		
		kennelblockdata = (kennelblockid, name, description)
		
		self.EditKennelBlockDialog(kennelblockdata)
	
	def DeleteKennelBlock(self, ID):
		
		if miscmethods.ConfirmMessage(self.GetLabel("deletekennelblockconfirmation"), self):
			
			self.listbox.selectedid = 0
			
			listboxid = self.listbox.GetSelection()
			kennelblockid = self.listbox.htmllist[listboxid][0]
			
			action = "DELETE FROM kennelblock WHERE ID = " + str(kennelblockid)
			db.SendSQL(action, self.localsettings.dbconnection)
			
			self.listbox.RefreshList()
	
	def EditKennelBlockDialog(self, kennelblockdata=False):
		
		if kennelblockdata == False:
			
			kennelblockid = 0
			name = ""
			description = ""
			titlelabel = self.GetLabel("addkennelblocktooltip")
			
		else:
			
			kennelblockid = kennelblockdata[0]
			name = kennelblockdata[1]
			description = kennelblockdata[2]
			titlelabel = self.GetLabel("editkennelblocktitle")
		
		dialog = wx.Dialog(self, -1, titlelabel)
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		panel.kennelblockid = kennelblockid
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		namelabel = wx.StaticText(panel, -1, self.GetLabel("namelabel"))
		font = namelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		namelabel.SetFont(font)
		topsizer.Add(namelabel, 0, wx.ALIGN_LEFT)
		
		nameentry = wx.TextCtrl(panel, -1, name)
		topsizer.Add(nameentry, 0, wx.EXPAND)
		
		descriptionlabel = wx.StaticText(panel, -1, self.GetLabel("descriptionlabel"))
		descriptionlabel.SetFont(font)
		topsizer.Add(descriptionlabel, 0, wx.ALIGN_LEFT)
		
		descriptionentry = wx.TextCtrl(panel, -1, description, style=wx.TE_MULTILINE)
		topsizer.Add(descriptionentry, 1, wx.EXPAND)
		
		submitbutton = wx.Button(panel, -1, self.GetLabel("submitlabel"))
		submitbutton.SetBackgroundColour("green")
		submitbutton.Bind(wx.EVT_BUTTON, self.SubmitKennelBlock)
		submitbutton.SetToolTipString(self.GetLabel("submitlabel"))
		topsizer.Add(submitbutton, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		panel.SetSizer(topsizer)
		
		panel.nameentry = nameentry
		panel.descriptionentry = descriptionentry
		panel.kennelblockdata = kennelblockdata
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		#dialog.Fit()
		dialog.SetSize((300,200))
		
		dialog.ShowModal()
	
	def SubmitKennelBlock(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		name = panel.nameentry.GetValue()
		description = panel.descriptionentry.GetValue()
		
		if panel.kennelblockid == 0:
			
			action = "INSERT INTO kennelblock (Name, Description) VALUES (\"" + name + "\", \"" + description + "\")"
			db.SendSQL(action, self.localsettings.dbconnection)
			
			action = "SELECT LAST_INSERT_ID() FROM kennelblock"
			self.listbox.selectedid = db.SendSQL(action, self.localsettings.dbconnection)[0][0]
			
			self.parent.kennelspanel.kennelblockid = self.listbox.selectedid
			
		else:
			
			action = "REPLACE INTO kennelblock (ID, Name, Description) VALUES (" + str(panel.kennelblockid) + ", \"" + name + "\", \"" + description + "\")"
			db.SendSQL(action, self.localsettings.dbconnection)
		
		dialog = panel.GetParent()
		dialog.Close()
		
		self.listbox.RefreshList()

class KennelBlockListbox(wx.HtmlListBox):
	
	def __init__(self, parent, localsettings):
		
		wx.HtmlListBox.__init__(self, parent, -1)
		
		self.htmllist = []
		self.localsettings = localsettings
		self.parent = parent
		self.selectedid = 0
		self.SetItemCount(0)
	
	def OnGetItem(self, n):
		
		if len(self.htmllist) > 0:
			
			name = self.htmllist[n][1]
			description = self.htmllist[n][2]
			
			if description != "":
				
				description = "<br><font size=2 color=red>" + description + "</font>"
			
			output = "<font color=blue><b>" + name + "</b></font>" + description
			
			return output
	
	def RefreshList(self, ID=False):
		
		action = "SELECT * FROM kennelblock ORDER BY Name"
		self.htmllist = db.SendSQL(action, self.localsettings.dbconnection)
		
		newselection = -1
		
		for a in range(0, len(self.htmllist)):
			
			if self.htmllist[a][0] == self.selectedid:
				
				newselection = a
				break
		
		self.Hide()
		
		if len(self.htmllist) > 0:
			
			self.Enable()
			
		else:
			
			self.Disable()
		
		if newselection > -1:
			
			self.parent.parent.kennelspanel.Enable()
			
		else:
			
			self.parent.parent.kennelspanel.Disable()
		
		self.parent.parent.kennelspanel.listbox.RefreshList()
		
		self.SetItemCount(len(self.htmllist))
		self.SetSelection(newselection)
		
		if newselection > -1:
			self.ScrollToLine(newselection)
		
		self.Refresh()
		
		self.Show()

class KennelsPanel(wx.Panel):
	
	
	def GetLabel(self, field):
		
		return  self.localsettings.dictionary[field][self.localsettings.language]
	
	def __init__(self, parent, localsettings):
		
		self.localsettings = localsettings
		
		wx.Panel.__init__(self, parent)
		
		self.kennelblockid = -1
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		titlelabel = wx.StaticText(self, -1, self.GetLabel("kennelstitlelabel"))
		font = titlelabel.GetFont()
		font.SetPointSize(font.GetPointSize() + 4)
		titlelabel.SetFont(font)
		topsizer.Add(titlelabel, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		#buttonssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		#newbitmap = wx.Bitmap("icons/new.png")
		#newbutton = wx.BitmapButton(self, -1, newbitmap)
		#newbutton.SetToolTipString(self.GetLabel("addkenneltooltip"))
		#newbutton.Bind(wx.EVT_BUTTON, self.AddKennel)
		#buttonssizer.Add(newbutton, 0, wx.EXPAND)
		
		#editbitmap = wx.Bitmap("icons/edit.png")
		#editbutton = wx.BitmapButton(self, -1, editbitmap)
		#editbutton.SetToolTipString(self.GetLabel("editkenneltitle"))
		#editbutton.Bind(wx.EVT_BUTTON, self.EditKennel)
		#buttonssizer.Add(editbutton, 0, wx.EXPAND)
		
		#deletebitmap = wx.Bitmap("icons/delete.png")
		#deletebutton = wx.BitmapButton(self, -1, deletebitmap)
		#deletebutton.SetToolTipString(self.GetLabel("deletelabel"))
		#deletebutton.Bind(wx.EVT_BUTTON, self.DeleteKennel)
		#buttonssizer.Add(deletebutton, 0, wx.EXPAND)
		
		#buttonssizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		#refreshbitmap = wx.Bitmap("icons/refresh.png")
		#refreshbutton = wx.BitmapButton(self, -1, refreshbitmap)
		#refreshbutton.SetToolTipString(self.GetLabel("lookupsrefreshtooltip"))
		#refreshbutton.Bind(wx.EVT_BUTTON, self.RefreshList)
		#buttonssizer.Add(refreshbutton, 0, wx.EXPAND)
		
		#topsizer.Add(buttonssizer, 0, wx.EXPAND)
		
		listbox = KennelListbox(self, self.localsettings)
		listbox.Bind(wx.EVT_LISTBOX, self.ItemSelected)
		listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EditKennel)
		listbox.Bind(wx.EVT_RIGHT_DOWN, self.KennelsPopup)
		topsizer.Add(listbox, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.listbox = listbox
		#self.editbutton = editbutton
		#self.deletebutton = deletebutton
		
		self.listbox.RefreshList()
	
	def KennelsPopup(self, ID):
		
		popupmenu = wx.Menu()
		
		addblock = wx.MenuItem(popupmenu, ADD_KENNEL, self.GetLabel("addlabel"))
		addblock.SetBitmap(wx.Bitmap("icons/new.png"))
		popupmenu.AppendItem(addblock)
		wx.EVT_MENU(popupmenu, ADD_KENNEL, self.AddKennel)
		
		if self.listbox.GetSelection() > -1:
			
			editblock = wx.MenuItem(popupmenu, EDIT_KENNEL, self.GetLabel("editlabel"))
			editblock.SetBitmap(wx.Bitmap("icons/new.png"))
			popupmenu.AppendItem(editblock)
			wx.EVT_MENU(popupmenu, EDIT_KENNEL, self.EditKennel)
			
			deleteblock = wx.MenuItem(popupmenu, DELETE_KENNEL, self.GetLabel("deletelabel"))
			deleteblock.SetBitmap(wx.Bitmap("icons/new.png"))
			popupmenu.AppendItem(deleteblock)
			wx.EVT_MENU(popupmenu, DELETE_KENNEL, self.DeleteKennel)
		
		popupmenu.AppendSeparator()
		
		refresh = wx.MenuItem(popupmenu, REFRESH_KENNELS, self.GetLabel("refreshlabel"))
		refresh.SetBitmap(wx.Bitmap("icons/refresh.png"))
		popupmenu.AppendItem(refresh)
		wx.EVT_MENU(popupmenu, REFRESH_KENNELS, self.RefreshList)
		
		self.PopupMenu(popupmenu)
	
	def RefreshList(self, ID):
		
		self.listbox.RefreshList()
	
	def ItemSelected(self, ID):
		
		#self.editbutton.Enable()
		#self.deletebutton.Enable()
		listboxid = self.listbox.GetSelection()
		self.listbox.selectedid = self.listbox.htmllist[listboxid][0]
	
	def AddKennel(self, ID):
		
		self.listbox.selectedid = 0
		self.EditKennelDialog()
	
	def EditKennel(self, ID):
		
		listboxid = self.listbox.GetSelection()
		
		kennelid = self.listbox.htmllist[listboxid][0]
		name = self.listbox.htmllist[listboxid][2]
		description = self.listbox.htmllist[listboxid][3]
		
		kenneldata = (kennelid, name, description)
		
		self.EditKennelDialog(kenneldata)
	
	def DeleteKennel(self, ID):
		
		if miscmethods.ConfirmMessage(self.GetLabel("deletekennelconfirmation"), self):
			
			self.listbox.selectedid = 0
			
			listboxid = self.listbox.GetSelection()
			kennelid = self.listbox.htmllist[listboxid][0]
			
			action = "DELETE FROM kennel WHERE ID = " + str(kennelid)
			db.SendSQL(action, self.localsettings.dbconnection)
			
			self.listbox.RefreshList()
	
	def EditKennelDialog(self, kenneldata=False):
		
		if kenneldata == False:
			
			kennelid = 0
			name = ""
			description = ""
			titlelabel = self.GetLabel("addkenneltooltip")
			
		else:
			
			kennelid = kenneldata[0]
			name = kenneldata[1]
			description = kenneldata[2]
			titlelabel = self.GetLabel("editkenneltitle")
		
		dialog = wx.Dialog(self, -1, titlelabel)
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		panel.kennelid = kennelid
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		namelabel = wx.StaticText(panel, -1, self.GetLabel("namelabel"))
		font = namelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		namelabel.SetFont(font)
		topsizer.Add(namelabel, 0, wx.ALIGN_LEFT)
		
		nameentry = wx.TextCtrl(panel, -1, name)
		topsizer.Add(nameentry, 0, wx.EXPAND)
		
		descriptionlabel = wx.StaticText(panel, -1, self.GetLabel("descriptionlabel"))
		descriptionlabel.SetFont(font)
		topsizer.Add(descriptionlabel, 0, wx.ALIGN_LEFT)
		
		descriptionentry = wx.TextCtrl(panel, -1, description, style=wx.TE_MULTILINE)
		topsizer.Add(descriptionentry, 1, wx.EXPAND)
		
		submitbutton = wx.Button(panel, -1, self.GetLabel("submitlabel"))
		submitbutton.SetBackgroundColour("green")
		submitbutton.Bind(wx.EVT_BUTTON, self.SubmitKennel)
		submitbutton.SetToolTipString(self.GetLabel("submitlabel"))
		topsizer.Add(submitbutton, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		panel.SetSizer(topsizer)
		
		panel.nameentry = nameentry
		panel.descriptionentry = descriptionentry
		panel.kenneldata = kenneldata
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		#dialog.Fit()
		dialog.SetSize((300,200))
		
		dialog.ShowModal()
	
	def SubmitKennel(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		name = panel.nameentry.GetValue()
		description = panel.descriptionentry.GetValue()
		
		if panel.kennelid == 0:
			
			action = "INSERT INTO kennel (KennelBlockID, Name, Description) VALUES (" + str(self.kennelblockid) + ", \"" + name + "\", \"" + description + "\")"
			db.SendSQL(action, self.localsettings.dbconnection)
			
			action = "SELECT LAST_INSERT_ID() FROM kennel"
			self.listbox.selectedid = db.SendSQL(action, self.localsettings.dbconnection)[0][0]
			
		else:
			
			action = "REPLACE INTO kennel (ID, KennelBlockID, Name, Description) VALUES (" + str(panel.kennelid) + ", " + str(self.kennelblockid) + ", \"" + name + "\", \"" + description + "\")"
			db.SendSQL(action, self.localsettings.dbconnection)
		
		dialog = panel.GetParent()
		dialog.Close()
		
		self.listbox.RefreshList()

class KennelListbox(wx.HtmlListBox):
	
	def __init__(self, parent, localsettings):
		
		wx.HtmlListBox.__init__(self, parent, -1)
		
		self.htmllist = []
		self.localsettings = localsettings
		self.parent = parent
		self.selectedid = 0
		self.SetItemCount(0)
	
	def OnGetItem(self, n):
		
		if len(self.htmllist) > 0:
			
			#print "self.htmllist[" + str(n) + "] = " + str(self.htmllist[n])
			
			name = self.htmllist[n][2]
			description = self.htmllist[n][3]
			
			if description != "":
				
				description = "<br><font size=2 color=red>" + description + "</font>"
			
			output = "<font color=blue><b>" + name + "</b></font>" + description
			
			return output
	
	def RefreshList(self, ID=False):
		
		action = "SELECT * FROM kennel WHERE KennelBlockID = " + str(self.parent.kennelblockid) + " ORDER BY Name"
		self.htmllist = db.SendSQL(action, self.localsettings.dbconnection)
		
		newselection = -1
		
		for a in range(0, len(self.htmllist)):
			
			if self.htmllist[a][0] == self.selectedid:
				
				newselection = a
				break
		
		self.Hide()
		
		if len(self.htmllist) > 0:
			
			self.Enable()
			
		else:
			
			self.Disable()
		
		#print "newselection = " + str(newselection)
                
                self.SetItemCount(len(self.htmllist))
		
		self.SetSelection(newselection)
		
		if newselection > -1:
			
			self.ScrollToLine(newselection)
		
		self.Refresh()
		
		self.Show()

class ViewKennelsPanel(wx.Panel):
	
	def GetLabel(self, field):
		
		return  self.localsettings.dictionary[field][self.localsettings.language]
	
	def __init__(self, parent, localsettings):
		
		wx.Panel.__init__(self, parent)
		
		self.listboxes = []
		
		self.localsettings = localsettings
		
		self.pagetitle = miscmethods.GetPageTitle(parent, self.GetLabel("viewkennelsmenu")[0])
		
		self.pageimage = "icons/kennel.png"
		
		action = "SELECT * FROM kennelblock ORDER BY Name"
		kennelblockdata = db.SendSQL(action, self.localsettings.dbconnection)
		
		action = "SELECT * FROM kennel ORDER BY Name"
		kenneldata = db.SendSQL(action, self.localsettings.dbconnection)
		
		topsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		toolspanel = KennelToolsPanel(self, self.localsettings)
		topsizer.Add(toolspanel, 0, wx.EXPAND)
		
		notebook = wx.Notebook(self)
		
		for a in kennelblockdata:
			
			panel = KennelCellPanel(notebook, self.localsettings, a[0])
			
			notebook.AddPage(panel, a[1])
		
		topsizer.Add(notebook, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		toolspanel.refreshbutton.Bind(wx.EVT_BUTTON, self.RefreshListboxes)
		
		self.toolspanel = toolspanel
		self.kennelblockdata = kennelblockdata
		self.kenneldata = kenneldata
		
		self.RefreshListboxes()
	
	def RefreshListboxes(self, ID=False):
		
		for a in self.listboxes:
			
			a.RefreshList()
		
		action = "SELECT animal.Species, kennelblock.ID, kennel.ID FROM appointment INNER JOIN animal ON appointment.AnimalID = animal.ID INNER JOIN kennel ON appointment.Staying = kennel.ID INNER JOIN kennelblock ON kennel.KennelBlockID = kennelblock.ID WHERE appointment.Staying > 0"
		animaldata = db.SendSQL(action, self.localsettings.dbconnection)
		
		html = ""
		
		for a in self.kennelblockdata:
			
			html = html + "<font color=blue size=3><b><u>" + a[1] + "</u></b></font><br>"
			
			kennelblockid = a[0]
			
			specieslist = []
			
			for b in animaldata:
				
				if specieslist.__contains__(b[0]) == False:
					
					specieslist.append(b[0])
			
			for b in specieslist:
				
				count = 0
				
				for c in animaldata:
					
					if c[0] == b and c[1] == a[0]:
						
						count = count + 1
				
				if count > 0:
					
					html = html + "&nbsp;<font size=1>" + str(count) + " x " + b + "</font><br>"
			
			noofkennels = 0
			nooccupied = 0
			
			for b in self.kenneldata:
				
				if b[1] == a[0]:
					
					noofkennels = noofkennels + 1
					
					occupied = False
					
					for c in animaldata:
						
						if c[2] == b[0]:
							
							occupied = True
					
					if occupied == True:
						
						nooccupied = nooccupied + 1
			
			vacancies = noofkennels - nooccupied
			
			html = html + "&nbsp;<font size=1 color=red>" + self.GetLabel("vacantlabel") + " x " + str(vacancies) + "</font><br>"
		
		self.toolspanel.htmlwindow.SetPage(html)

class KennelToolsPanel(wx.Panel):
	
	def GetLabel(self, field):
		
		return  self.localsettings.dictionary[field][self.localsettings.language]
	
	def __init__(self, parent, localsettings):
		
		wx.Panel.__init__(self, parent)
		
		self.localsettings = localsettings
		self.parent = parent
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		refreshbitmap = wx.Bitmap("icons/refresh.png")
		refreshbutton = wx.BitmapButton(self, -1, refreshbitmap)
		refreshbutton.SetToolTipString(self.GetLabel("lookupsrefreshtooltip"))
		topsizer.Add(refreshbutton, 0, wx.ALIGN_LEFT)
		
		htmlwindow = wx.html.HtmlWindow(self, size=(200,-1))
		topsizer.Add(htmlwindow, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.refreshbutton = refreshbutton
		self.htmlwindow = htmlwindow

class KennelCellPanel(wx.Panel):
	
	def GetLabel(self, field):
		
		return  self.localsettings.dictionary[field][self.localsettings.language]
	
	def __init__(self, parent, localsettings, kennelblockid):
		
		kennelspanel = parent.GetParent()
		
		wx.Panel.__init__(self, parent)
		
		#self.SetBackgroundColour("white")
		
		self.localsettings = localsettings
		
		action = "SELECT * FROM kennel WHERE KennelBlockID = " + str(kennelblockid) + " ORDER BY Name"
		kenneldata = db.SendSQL(action, self.localsettings.dbconnection)
		
		action = "SELECT animal.Name, animal.Species, appointment.Staying, appointment.ID FROM animal INNER JOIN appointment ON appointment.AnimalID = animal.ID WHERE appointment.Staying > 0 ORDER BY animal.Name"
		animaldata = db.SendSQL(action, self.localsettings.dbconnection)
		
		topsizer = wx.FlexGridSizer(cols=5)
		
		for a in range(0, 5):
			
			topsizer.AddGrowableCol(a)
		
		count = 0
		row = 0
		
		for a in range(0, len(kenneldata)):
			
			if count == 0:
				
				topsizer.AddGrowableRow(row)
			
			count = count + 1
			
			if count == 5:
				
				count = 0
				row = row + 1
		
		for a in kenneldata:
			
			name = a[2]
			description = a[3]
			
			panel = wx.Panel(self, style=wx.SIMPLE_BORDER)
			
			panelsizer = wx.BoxSizer(wx.VERTICAL)
			
			kennelnamelabel = wx.StaticText(panel, -1, name)
			
			font = kennelnamelabel.GetFont()
			font.SetPointSize(font.GetPointSize() + 2)
			kennelnamelabel.SetFont(font)
			
			panelsizer.Add(kennelnamelabel, 0, wx.ALIGN_CENTER_HORIZONTAL)
			
			if description != "":
				
				kenneldescriptionlabel = wx.StaticText(panel, -1, description)
				panelsizer.Add(kenneldescriptionlabel, 0, wx.ALIGN_LEFT)
			
			panel.listbox = KennelResidentListbox(panel, self.localsettings, a[0])
			panel.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EditAppointment)
			panel.listbox.Bind(wx.EVT_RIGHT_DOWN, self.AnimalPopupMenu)
			#panel.listbox.RefreshList()
			
			panelsizer.Add(panel.listbox, 1, wx.EXPAND)
			
			panel.SetSizer(panelsizer)
			
			panel.animaldata = animaldata
			
			topsizer.Add(panel, 1, wx.EXPAND)
			
			kennelspanel.listboxes.append(panel.listbox)
		
		self.SetSizer(topsizer)
	
	def EditAppointment(self, ID):
		
		kennelcell = ID.GetEventObject().GetParent()
		
		listboxid = kennelcell.listbox.GetSelection()
		
		appointmentid = kennelcell.animaldata[listboxid][3]
		
		notebook = kennelcell.GetGrandParent().GetGrandParent()
		
		appointmentdata = appointmentmethods.AppointmentSettings(self.localsettings, False, appointmentid)
		
		appointmentpanel = appointmentmethods.AppointmentPanel(notebook, appointmentdata)
		appointmentpanel.kennelspanel = kennelcell.GetGrandParent().GetParent()
		
		#print "kennelspanel = " + str(kennelspanel)
		
		notebook.AddPage(appointmentpanel)
	
	def AnimalPopupMenu(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		if panel.listbox.GetSelection() > -1:
			
			popupmenu = wx.Menu()
			popupmenu.panel = panel
			
			vetform = wx.MenuItem(popupmenu, EDIT_VETFORM, self.GetLabel("editvetformlabel"))
			vetform.SetBitmap(wx.Bitmap("icons/vetform.png"))
			popupmenu.AppendItem(vetform)
			wx.EVT_MENU(popupmenu, EDIT_VETFORM, self.EditVetForm)
			
			editanimal = wx.MenuItem(popupmenu, EDIT_ANIMAL, self.GetLabel("editanimaltooltip"))
			editanimal.SetBitmap(wx.Bitmap("icons/editanimal.png"))
			popupmenu.AppendItem(editanimal)
			wx.EVT_MENU(popupmenu, EDIT_ANIMAL, self.EditAnimal)
			
			editclient = wx.MenuItem(popupmenu, EDIT_CLIENT, self.GetLabel("viewappointmentseditclientbuttonlabel"))
			editclient.SetBitmap(wx.Bitmap("icons/editclient.png"))
			popupmenu.AppendItem(editclient)
			wx.EVT_MENU(popupmenu, EDIT_CLIENT, self.EditClient)
			
			discharge = wx.MenuItem(popupmenu, DISCHARGE, self.GetLabel("dischargelabel"))
			discharge.SetBitmap(wx.Bitmap("icons/reset.png"))
			popupmenu.AppendItem(discharge)
			wx.EVT_MENU(popupmenu, DISCHARGE, self.Discharge)
			
			self.PopupMenu(popupmenu)
	
	def EditVetForm(self, ID):
		
		panel = ID.GetEventObject().panel
		
		listbox = panel.listbox
		
		notebook = self.GetGrandParent().GetParent()
		
		appointmentid = listbox.htmllist[listbox.GetSelection()][3]
		
		appointmentdata = appointmentmethods.AppointmentSettings(self.localsettings, False, appointmentid)
		stayingid = appointmentdata.staying
		animalid = appointmentdata.animalid
		
		today = datetime.date.today()
		
		appointmentdate = miscmethods.GetDateFromSQLDate(appointmentdata.date)
		
		if appointmentdate != today:
			
			appointmentdata.staying = 0
			appointmentdata.done = 1
			appointmentdata.withvet = 0
			
			appointmentdata.Submit(True)
			
			miscmethods.ShowMessage(self.GetLabel("animalstayedmessage"), self)
			
			appointmentdata = appointmentmethods.AppointmentSettings(self.localsettings, animalid, False)
			appointmentdata.reason = self.GetLabel("overnightstaylabel")
			appointmentdata.time =  str(datetime.datetime.today().time())[:5]
			appointmentdata.arrived = 1
			appointmentdata.withvet = 1
			appointmentdata.staying = stayingid
			
			appointmentdata.Submit()
		
		vetform = vetmethods.VetForm(notebook, appointmentdata, self.localsettings, self)
		
		notebook.AddPage(vetform)
	
	def EditAnimal(self, ID):
		
		panel = ID.GetEventObject().panel
		
		listbox = panel.listbox
		
		notebook = self.GetGrandParent().GetParent()
		
		appointmentid = listbox.htmllist[listbox.GetSelection()][3]
		
		appointmentdata = appointmentmethods.AppointmentSettings(self.localsettings, False, appointmentid)
		animalid = appointmentdata.animalid
		
		animaldata = animalmethods.AnimalSettings(self.localsettings, False, animalid)
		
		animalpanel = animalmethods.AnimalPanel(notebook, animaldata)
		
		notebook.AddPage(animalpanel)
	
	def EditClient(self, ID):
		
		panel = ID.GetEventObject().panel
		
		listbox = panel.listbox
		
		notebook = self.GetGrandParent().GetParent()
		
		appointmentid = listbox.htmllist[listbox.GetSelection()][3]
		
		appointmentdata = appointmentmethods.AppointmentSettings(self.localsettings, False, appointmentid)
		clientid = appointmentdata.ownerid
		
		clientdata = clientmethods.ClientSettings(self.localsettings, clientid)
		
		clientpanel = clientmethods.ClientPanel(notebook, clientdata)
		
		notebook.AddPage(clientpanel)
	
	def Discharge(self, ID):
		
		panel = ID.GetEventObject().panel
		
		listbox = panel.listbox
		
		notebook = self.GetGrandParent().GetParent()
		
		appointmentid = listbox.htmllist[listbox.GetSelection()][3]
		
		appointmentdata = appointmentmethods.AppointmentSettings(self.localsettings, False, appointmentid)
		
		appointmentdata.staying = 0
		
		appointmentdata.Submit()
		
		listbox.RefreshList()

class KennelResidentListbox(wx.HtmlListBox):
	
	def __init__(self, parent, localsettings, kennelid):
		
		wx.HtmlListBox.__init__(self, parent, -1)
		
		self.kennelid = kennelid
		self.htmllist = []
		self.localsettings = localsettings
		self.parent = parent
		self.SetItemCount(0)
	
	def OnGetItem(self, n):
		
		if len(self.htmllist) > 0:
			
			return "<font color=red>" + self.htmllist[n][0] + " (" + self.htmllist[n][1] + ")</font>"
	
	def RefreshList(self, ID=False):
		
		self.Hide()
		
		action = "SELECT animal.Name, animal.Species, appointment.Staying, appointment.ID FROM animal INNER JOIN appointment ON appointment.AnimalID = animal.ID WHERE appointment.Staying = " + str(self.kennelid) + " ORDER BY animal.Name"
		self.htmllist = db.SendSQL(action, self.localsettings.dbconnection)
		
		self.SetItemCount(len(self.htmllist))
		self.SetSelection(-1)
		self.Refresh()
		
		if len(self.htmllist) == 0:
			
			self.Disable()
			
		else:
			
			self.Enable()
		
		self.Show()
