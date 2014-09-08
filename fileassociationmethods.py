#!/usr/bin/python

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
import os
import customwidgets

REFRESH_ASSOCIATIONS = 900
ADD_ASSOCIATION = 901
EDIT_ASSOCIATION = 902
DELETE_ASSOCIATION = 903

class FileTypePanel(wx.Panel):
	
	def GetLabel(self, field):
		
		return  self.localsettings.dictionary[field][self.localsettings.language]
	
	def __init__(self, notebook, localsettings):
		
		self.localsettings = localsettings
		
		self.pagetitle = self.GetLabel("fileassociationspagetitle")
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, self.pagetitle)
		
		self.pageimage = "icons/filetypes.png"
		
		wx.Panel.__init__(self, notebook)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		listbox = FileTypesListbox(self, self.localsettings)
		listbox.listctrl.Bind(wx.EVT_RIGHT_DOWN, self.Popup)
		listbox.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.Edit)
		topsizer.Add(listbox, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.listbox = listbox
		
		self.listbox.RefreshList()
	
	def Popup(self, ID):
		
		popupmenu = wx.Menu()
		
		addassociation = wx.MenuItem(popupmenu, ADD_ASSOCIATION, self.GetLabel("addlabel"))
		addassociation.SetBitmap(wx.Bitmap("icons/new.png"))
		wx.EVT_MENU(popupmenu, ADD_ASSOCIATION, self.Add)
		popupmenu.AppendItem(addassociation)
		
		if self.listbox.listctrl.GetSelectedItemCount() > 0:
			
			editassociation = wx.MenuItem(popupmenu, EDIT_ASSOCIATION, self.GetLabel("editlabel"))
			editassociation.SetBitmap(wx.Bitmap("icons/edit.png"))
			wx.EVT_MENU(popupmenu, EDIT_ASSOCIATION, self.Edit)
			popupmenu.AppendItem(editassociation)
			
			deleteassociation = wx.MenuItem(popupmenu, DELETE_ASSOCIATION, self.GetLabel("deletelabel"))
			deleteassociation.SetBitmap(wx.Bitmap("icons/delete.png"))
			wx.EVT_MENU(popupmenu, DELETE_ASSOCIATION, self.Delete)
			popupmenu.AppendItem(deleteassociation)
		
		popupmenu.AppendSeparator()
		
		refreshassociation = wx.MenuItem(popupmenu, REFRESH_ASSOCIATIONS, self.GetLabel("refreshlabel"))
		refreshassociation.SetBitmap(wx.Bitmap("icons/refresh.png"))
		wx.EVT_MENU(popupmenu, REFRESH_ASSOCIATIONS, self.listbox.RefreshList)
		popupmenu.AppendItem(refreshassociation)
		
		self.PopupMenu(popupmenu)
	
	def Add(self, ID):
		
		self.EditFileTypeDialog()
	
	def Edit(self, ID):
		
		listboxid = self.listbox.GetSelection()
		
		countid = self.listbox.htmllist[listboxid][0]
		
		self.EditFileTypeDialog(countid)
	
	def EditFileTypeDialog(self, countid=-1):
		
		dialog = wx.Dialog(self, -1, self.GetLabel("fileassociationspagetitle"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		extensionlabel = wx.StaticText(panel, -1, self.GetLabel("extensionlabel") + ":")
		font = extensionlabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		extensionlabel.SetFont(font)
		topsizer.Add(extensionlabel, 0, wx.ALIGN_LEFT)
		
		extensionentry = wx.TextCtrl(panel, -1, "")
		extensionentry.SetFocus()
		topsizer.Add(extensionentry, 0, wx.ALIGN_LEFT)
		
		programlabel = wx.StaticText(panel, -1, self.GetLabel("programlabel") + ":")
		programlabel.SetFont(font)
		topsizer.Add(programlabel, 0, wx.ALIGN_LEFT)
		
		programsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		programentry = wx.TextCtrl(panel, -1, "", size=(250,-1))
		programsizer.Add(programentry, 1, wx.EXPAND)
		
		editbitmap = wx.Bitmap("icons/edit.png")
		findprogrambutton = wx.BitmapButton(panel, -1, editbitmap)
		findprogrambutton.SetToolTipString(self.GetLabel("programbrowsertooltip"))
		findprogrambutton.Bind(wx.EVT_BUTTON, self.GetProgramPath)
		programsizer.Add(findprogrambutton, 0, wx.EXPAND)
		
		topsizer.Add(programsizer, 0, wx.EXPAND)
		
		topsizer.Add(wx.StaticText(panel, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		submitbutton = wx.Button(panel, -1, self.GetLabel("submitlabel"))
		submitbutton.SetToolTipString(self.GetLabel("submitlabel"))
		submitbutton.SetBackgroundColour("green")
		submitbutton.Bind(wx.EVT_BUTTON, self.Submit)
		topsizer.Add(submitbutton, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		panel.SetSizer(topsizer)
		
		if countid != -1:
			
			extvalue = self.listbox.htmllist[countid][1][0]
			programvalue = self.listbox.htmllist[countid][1][1]
			
			extensionentry.SetValue(extvalue)
			programentry.SetValue(programvalue)
		
		panel.extensionentry = extensionentry
		panel.programentry = programentry
		panel.countid = countid
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		dialog.Fit()
		
		dialog.ShowModal()
	
	def Submit(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		extension = panel.extensionentry.GetValue()
		
		program = panel.programentry.GetValue()
		
		output = ""
		
		success = True
		
		if panel.countid == -1:
			
			existingextensions = []
			
			for a in range(0, len(self.listbox.htmllist)):
				
				existingextensions.append(self.listbox.htmllist[a][1][0].strip())
				
				output = output + self.listbox.htmllist[a][1][0].strip() + "$$$" + self.listbox.htmllist[a][1][1].strip() + "\n"
			
			output = output + extension.strip() + "$$$" + program.strip()
			
			if existingextensions.__contains__(extension):
				
				success = False
				
				miscmethods.ShowMessage(self.GetLabel("fileassociationexistsmessage"))
			
		else:
			
			for a in range(0, len(self.listbox.htmllist)):
				
				if a == panel.countid:
					
					output = output + self.listbox.htmllist[a][1][0].strip() + "$$$" + program + "\n"
					
				else:
					
					output = output + self.listbox.htmllist[a][1][0].strip() + "$$$" + self.listbox.htmllist[a][1][1].strip() + "\n"
			
			output = output.strip()
		
		if success == True:
			
			pathtofiletypesfile = miscmethods.GetHome() + "/.evette/filetypes.conf"
			
			out = open(pathtofiletypesfile, "w")
			out.write(output)
			out.close()
			
			self.listbox.RefreshList()
			
			panel.GetParent().Close()
	
	def Delete(self, ID):
		
		if miscmethods.ConfirmMessage(self.GetLabel("deleteassociationconfirm")):
			
			listboxid = self.listbox.GetSelection()
			
			output = ""
			
			for a in range(0, len(self.listbox.htmllist)):
				
				if a != listboxid:
					
					output = output + self.listbox.htmllist[a][1][0] + "$$$" + self.listbox.htmllist[a][1][1] + "\n"
			
			output = output.strip()
			
			pathtofiletypesfile = miscmethods.GetHome() + "/.evette/filetypes.conf"
			
			out = open(pathtofiletypesfile, "w")
			out.write(output)
			out.close()
			
			self.listbox.RefreshList()
	
	def GetProgramPath(self, ID):
		
		programpath = wx.FileSelector()
		
		panel = ID.GetEventObject().GetParent()
		
		panel.programentry.SetValue(programpath)

class FileTypesListbox(customwidgets.ListCtrlWrapper):
	
	def GetLabel(self, field):
		
		return  self.localsettings.dictionary[field][self.localsettings.language]
	
	def __init__(self, parent, localsettings):
		
		self.htmllist = []
		self.localsettings = localsettings
		self.parent = parent
		
		columnheadings = (self.GetLabel("extensionlabel"), self.GetLabel("programlabel"))
		
		customwidgets.ListCtrlWrapper.__init__(self, parent, self.localsettings, columnheadings)
	
	def ProcessRow(self, rowdata):
		
		output = ((rowdata[0], rowdata[1][0], rowdata[1][1]), -1)
		
		return output
			
	def RefreshList(self, ID=False):
		
		pathtofiletypesfile = miscmethods.GetHome() + "/.evette/filetypes.conf"
		
		if os.path.isfile(pathtofiletypesfile) == False:
			
			out = open(pathtofiletypesfile, "w")
			out.write("")
			out.close()
		
		inp = open(pathtofiletypesfile, "r")
		
		self.htmllist = []
		
		count = 0
		
		for a in inp.readlines():
			
			self.htmllist.append( (count, a.strip().split("$$$")) )
			
			count = count + 1
		
		inp.close()
		
		customwidgets.ListCtrlWrapper.RefreshList(self)