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
import db
import dbmethods
import miscmethods
import customwidgets

ADD_PROCEDURE = 1201
EDIT_PROCEDURE = 1202
DELETE_PROCEDURE = 1203
REFRESH_PROCEDURES = 1204

class EditProceduresPanel(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, notebook, localsettings):
		
		self.localsettings = localsettings
		
		wx.Panel.__init__(self, notebook)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, self.t("editprocedurespagetitle"))
		
		self.procedureslistbox = customwidgets.ProceduresListBox(self, localsettings)
		self.procedureslistbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EditProcedure)
		self.procedureslistbox.Bind(wx.EVT_RIGHT_DOWN, self.Popup)
		
		topsizer.Add(self.procedureslistbox, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.procedureslistbox.RefreshList()
	
	def Popup(self, ID):
		
		popupmenu = wx.Menu()
		
		add = wx.MenuItem(popupmenu, ADD_PROCEDURE, self.t("addlabel"))
		add.SetBitmap(wx.Bitmap("icons/new.png"))
		popupmenu.AppendItem(add)
		wx.EVT_MENU(popupmenu, ADD_PROCEDURE, self.AddProcedure)
		
		if self.procedureslistbox.GetSelection() > -1:
			
			edit = wx.MenuItem(popupmenu, EDIT_PROCEDURE, self.t("editlabel"))
			edit.SetBitmap(wx.Bitmap("icons/edit.png"))
			popupmenu.AppendItem(edit)
			wx.EVT_MENU(popupmenu, EDIT_PROCEDURE, self.EditProcedure)
			
			delete = wx.MenuItem(popupmenu, DELETE_PROCEDURE, self.t("deletelabel"))
			delete.SetBitmap(wx.Bitmap("icons/delete.png"))
			popupmenu.AppendItem(delete)
			wx.EVT_MENU(popupmenu, DELETE_PROCEDURE, self.DeleteProcedure)
		
		popupmenu.AppendSeparator()
		
		refresh = wx.MenuItem(popupmenu, REFRESH_PROCEDURES, self.t("refreshlabel"))
		refresh.SetBitmap(wx.Bitmap("icons/refresh.png"))
		popupmenu.AppendItem(refresh)
		wx.EVT_MENU(popupmenu, REFRESH_PROCEDURES, self.RefreshList)
		
		self.PopupMenu(popupmenu)
	
	def AddProcedure(self, ID):
		
		self.EditProcedureDialog()
	
	def EditProcedure(self, ID):
		
		listboxid = self.procedureslistbox.GetSelection()
		
		proceduredata = self.procedureslistbox.htmllist[listboxid]
		
		self.EditProcedureDialog(proceduredata)
	
	def EditProcedureDialog(self, proceduredata=False):
		
		dialog = wx.Dialog(self, -1, self.t("editprocedurelabel"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		topsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		namesizer = wx.BoxSizer(wx.VERTICAL)
		
		lname = wx.StaticText(panel, -1, self.t("namelabel") + ":")
		font = lname.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		lname.SetFont(font)
		namesizer.Add(lname, 1, wx.ALIGN_LEFT)
		
		nameentry = wx.TextCtrl(panel, -1, "")
		nameentry.SetFocus()
		namesizer.Add(nameentry, 0, wx.EXPAND)
		
		descriptionsizer = wx.BoxSizer(wx.VERTICAL)
		
		ldescription = wx.StaticText(panel, -1, self.t("descriptionlabel") + ":")
		ldescription.SetFont(font)
		descriptionsizer.Add(ldescription, 0, wx.ALIGN_LEFT)
		
		descriptionentry = wx.TextCtrl(panel, -1, "")
		descriptionsizer.Add(descriptionentry, 1, wx.EXPAND)
		
		pricesizer = wx.BoxSizer(wx.VERTICAL)
		
		lprice = wx.StaticText(panel, -1, self.t("pricelabel") + ":")
		lprice.SetFont(font)
		pricesizer.Add(lprice, 0, wx.ALIGN_LEFT)
		
		priceentry = wx.TextCtrl(panel, -1, "")
		pricesizer.Add(priceentry, 1, wx.EXPAND)
		
		entrysizer = wx.BoxSizer(wx.HORIZONTAL)
		
		entrysizer.Add(namesizer, 2, wx.EXPAND)
		
		entrysizer.Add(descriptionsizer, 5, wx.EXPAND)
		
		entrysizer.Add(pricesizer, 1, wx.EXPAND)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		bsubmit = wx.BitmapButton(panel, -1, submitbitmap)
		bsubmit.Bind(wx.EVT_BUTTON, self.SubmitProcedure)
		entrysizer.Add(bsubmit, 0, wx.ALIGN_BOTTOM)
		
		topsizer.Add(entrysizer, 0, wx.EXPAND)
		
		panel.SetSizer(topsizer)
		
		panel.nameentry = nameentry
		panel.descriptionentry = descriptionentry
		panel.priceentry = priceentry
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		if proceduredata != False:
			
			nameentry.SetValue(proceduredata[1])
			descriptionentry.SetValue(proceduredata[2])
			price = miscmethods.FormatPrice(proceduredata[3])
			priceentry.SetValue(price)
			
			panel.procedureid = proceduredata[0]
			
		else:
			
			panel.procedureid = -1
		
		dialog.Fit()
		
		dialog.ShowModal()
	
	def RefreshList(self, ID=False):
		
		self.procedureslistbox.RefreshList()
	
	def SubmitProcedure(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		name = panel.nameentry.GetValue()
		
		if name == "":
			
			miscmethods.ShowMessage(self.t("proceduresunnamedproceduremessage"))
			
		else:
			
			description = panel.descriptionentry.GetValue()
			price = panel.priceentry.GetValue()
			price = str(miscmethods.ConvertPriceToPennies(price))
			
			if panel.procedureid > -1:
				
				procedureid = panel.procedureid
				
				action = "REPLACE INTO procedures (ID, Name, Description, Price) VALUES (" + str(procedureid) + ", \"" + name + "\", \"" + description + "\", \"" + price + "\")"
				db.SendSQL(action, self.localsettings.dbconnection)
				
			else:
				
				action = "INSERT INTO procedures (Name, Description, Price) VALUES (\"" + name + "\", \"" + description + "\", \"" + price + "\")"
				db.SendSQL(action, self.localsettings.dbconnection)
			
			self.RefreshList()
			
			panel.GetParent().Close()
	
	def DeleteProcedure(self, ID):
		
		if miscmethods.ConfirmMessage(self.t("proceduresdeletemessage")) == True:
			
			listboxid = self.procedureslistbox.GetSelection()
			procedureid = self.procedureslistbox.htmllist[listboxid][0]
			
			action = "DELETE FROM procedures WHERE ID = " + str(procedureid)
			db.SendSQL(action, self.localsettings.dbconnection)
			
			self.RefreshList()
