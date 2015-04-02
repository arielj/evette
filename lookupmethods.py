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
import wx
import miscmethods

ADD_LOOKUP = 1101
EDIT_LOOKUP = 1102
DELETE_LOOKUP = 1103
REFRESH_LOOKUPS = 1104

class EditLookup(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return  self.localsettings.t(field,idx)
	
	def __init__(self, notebook, lookup, localsettings):
		
		self.localsettings = localsettings
		
		wx.Panel.__init__(self, notebook)
		
		if lookup == "colour":
			
			self.pagetitle = miscmethods.GetPageTitle(notebook, self.t("lookupscolourpagetitle"))
			
		elif lookup == "breed":
			
			self.pagetitle = miscmethods.GetPageTitle(notebook, self.t("lookupsbreedpagetitle"))
			
		elif lookup == "species":
			
			self.pagetitle = miscmethods.GetPageTitle(notebook, self.t("lookupsspeciespagetitle"))
			
		elif lookup == "reason":
			
			self.pagetitle = miscmethods.GetPageTitle(notebook, self.t("lookupsreasonpagetitle"))
		
		self.lookup = lookup
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		self.listbox = wx.ListBox(self)
		self.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EditLookup)
		self.listbox.Bind(wx.EVT_RIGHT_DOWN, self.Popup)
		
		topsizer.Add(self.listbox, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.RefreshLookups()
	
	def Popup(self, ID):
		
		popupmenu = wx.Menu()
		
		add = wx.MenuItem(popupmenu, ADD_LOOKUP, self.t("addlabel"))
		add.SetBitmap(wx.Bitmap("icons/new.png"))
		popupmenu.AppendItem(add)
		wx.EVT_MENU(popupmenu, ADD_LOOKUP, self.AddLookup)
		
		if self.listbox.GetSelection() > -1:
			
			edit = wx.MenuItem(popupmenu, EDIT_LOOKUP, self.t("editlabel"))
			edit.SetBitmap(wx.Bitmap("icons/edit.png"))
			popupmenu.AppendItem(edit)
			wx.EVT_MENU(popupmenu, EDIT_LOOKUP, self.EditLookup)
			
			delete = wx.MenuItem(popupmenu, DELETE_LOOKUP, self.t("deletelabel"))
			delete.SetBitmap(wx.Bitmap("icons/delete.png"))
			popupmenu.AppendItem(delete)
			wx.EVT_MENU(popupmenu, DELETE_LOOKUP, self.DeleteLookup)
		
		popupmenu.AppendSeparator()
		
		refresh = wx.MenuItem(popupmenu, REFRESH_LOOKUPS, self.t("refreshlabel"))
		refresh.SetBitmap(wx.Bitmap("icons/refresh.png"))
		popupmenu.AppendItem(refresh)
		wx.EVT_MENU(popupmenu, REFRESH_LOOKUPS, self.RefreshLookups)
		
		self.PopupMenu(popupmenu)
	
	def AddLookup(self, ID):
		
		self.EditLookupDialog()
	
	def EditLookup(self, ID):
		
		listboxid = self.listbox.GetSelection()
		
		lookupid = self.lookupsdata[listboxid][0]
		
		self.EditLookupDialog(lookupid)
	
	def EditLookupDialog(self, lookupid=False):
		
		dialog = wx.Dialog(self, -1, self.t("lookupslabel"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		panel.lookupid = lookupid
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		namelabel = wx.StaticText(panel, -1, self.t("namelabel") + ":")
		font = namelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		namelabel.SetFont(font)
		topsizer.Add(namelabel, 0, wx.ALIGN_LEFT)
		
		nameentry = wx.TextCtrl(panel, -1, "", size=(150,-1))
		topsizer.Add(nameentry, 0, wx.EXPAND)
		
		if lookupid != False:
			
			listboxid = self.listbox.GetSelection()
			
			lookupname = self.lookupsdata[listboxid][1]
			
			nameentry.SetValue(lookupname)
		
		submitbutton = wx.Button(panel, -1, self.t("submitlabel"))
		submitbutton.SetBackgroundColour("green")
		submitbutton.SetToolTipString(self.t("submitlabel"))
		submitbutton.Bind(wx.EVT_BUTTON, self.SubmitLookup)
		topsizer.Add(submitbutton, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		panel.SetSizer(topsizer)
		
		panel.nameentry = nameentry
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		dialog.Fit()
		
		dialog.ShowModal()
	
	def SubmitLookup(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		name = panel.nameentry.GetValue()
		
		lookup = self.lookup
		columnname = lookup[0].upper() + lookup[1:] + "Name"
			
		if name == "":
			
			miscmethods.ShowMessage(self.t("lookupsnonamemessage"))
			
		else:
			
			if panel.lookupid == False:
				
				action = "INSERT INTO " + lookup + " (" + columnname + ") VALUES (\"" + name + "\")"
				
			else:
				
				action = "UPDATE " + lookup + " SET " + columnname + " = \"" + name + "\" WHERE ID = " + str(panel.lookupid)
			
			db.SendSQL(action, self.localsettings.dbconnection)
			self.RefreshLookups()
			
			panel.GetParent().Close()
	
	def DeleteLookup(self, ID):
		
		lookup = self.lookup
		listboxid = self.listbox.GetSelection()
		lookupid = self.lookupsdata[listboxid][0]
		
		query = miscmethods.ConfirmMessage(self.t("lookupsdeletemessage"))
		
		if query == True:
			
			action = "DELETE FROM " + lookup + " WHERE ID = " + str(lookupid) + ";"
			db.SendSQL(action, self.localsettings.dbconnection)
			
			self.RefreshLookups()
	
	def RefreshLookups(self, ID=False):
		
		lookup = self.lookup
		
		columnname = lookup[0].upper() + lookup[1:] + "Name"
		
		action = "SELECT * FROM " + lookup + " ORDER BY " + columnname + ";"
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		
		self.listbox.Clear()
		
		self.lookupsdata = []
		
		for a in range(0, len(results)):
			
			output = str(results[a][1])
			self.listbox.Append(output)
			self.lookupsdata.append(results[a])
