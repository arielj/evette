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
import threading
import db
import base64
import os
import datetime
import miscmethods
import language
import dbmethods
import customwidgets

ADD_MEDIA = 8000
EDIT_MEDIA = 8001
REFRESH_MEDIA = 8002
DELETE_MEDIA = 8004
VIEW_MEDIA = 8005
SAVE_MEDIA = 8006

class AttachedFilesPanel(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return  self.localsettings.t(field)
	
	def __init__(self, parent, localsettings, linktype, linkid):
		
		self.localsettings = localsettings
		self.linktype = linktype
		self.linkid = linkid
		
		wx.Panel.__init__(self, parent)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		buttonssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		listbox = AttachedFilesListbox(self, self.localsettings, linktype, linkid)
		listbox.listctrl.Bind(wx.EVT_RIGHT_DOWN, self.Popup)
		topsizer.Add(listbox, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.listbox = listbox
		
		self.listbox.RefreshList()
	
	def Popup(self, ID):
		
		popupmenu = wx.Menu()
		
		addmedia = wx.MenuItem(popupmenu, ADD_MEDIA, self.t("addlabel"))
		addmedia.SetBitmap(wx.Bitmap("icons/new.png"))
		popupmenu.AppendItem(addmedia)
		wx.EVT_MENU(popupmenu, ADD_MEDIA, self.AddMedia)
		
		if self.listbox.listctrl.GetSelectedItemCount() > 0:
			
			viewmedia = wx.MenuItem(popupmenu, VIEW_MEDIA, self.t("viewlabel"))
			viewmedia.SetBitmap(wx.Bitmap("icons/view.png"))
			popupmenu.AppendItem(viewmedia)
			wx.EVT_MENU(popupmenu, VIEW_MEDIA, self.OpenMedia)
			
			savemedia = wx.MenuItem(popupmenu, SAVE_MEDIA, self.t("savetooltip"))
			savemedia.SetBitmap(wx.Bitmap("icons/save.png"))
			popupmenu.AppendItem(savemedia)
			wx.EVT_MENU(popupmenu, SAVE_MEDIA, self.SaveMedia)
			
			editmedia = wx.MenuItem(popupmenu, EDIT_MEDIA, self.t("renamelabel"))
			editmedia.SetBitmap(wx.Bitmap("icons/edit.png"))
			popupmenu.AppendItem(editmedia)
			wx.EVT_MENU(popupmenu, EDIT_MEDIA, self.RenameMedia)
			
			deletemedia = wx.MenuItem(popupmenu, DELETE_MEDIA, self.t("deletelabel"))
			deletemedia.SetBitmap(wx.Bitmap("icons/delete.png"))
			popupmenu.AppendItem(deletemedia)
			wx.EVT_MENU(popupmenu, DELETE_MEDIA, self.DeleteMedia)
		
		refreshmedia = wx.MenuItem(popupmenu, REFRESH_MEDIA, self.t("refreshlabel"))
		refreshmedia.SetBitmap(wx.Bitmap("icons/refresh.png"))
		popupmenu.AppendItem(refreshmedia)
		wx.EVT_MENU(popupmenu, REFRESH_MEDIA, self.listbox.RefreshList)
		
		self.PopupMenu(popupmenu)
	
	def SaveMedia(self, ID=False):
		
		busy = wx.BusyCursor()
		
		listboxid = self.listbox.GetSelection()
		
		mediaid = self.listbox.htmllist[listboxid][0]
		filename = self.listbox.htmllist[listboxid][3]
		
		action = "SELECT Content FROM media WHERE ID = " + str(mediaid)
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		output = base64.decodestring(str(results[0][0]))
		
		if filename.__contains__("."):
			
			fileextension = filename.split(".")[-1]
			
		else:
			
			fileextension = ""
		
		targetfile = wx.SaveFileSelector(fileextension.upper(), fileextension, filename)
		
		out = open(targetfile, "wb")
		out.write(output)
		out.close()
		
		del busy
	
	def MediaSelected(self, ID=False):
		
		listboxid = self.listbox.GetSelection()
		description = self.listbox.htmllist[listboxid][4]
		
		self.descriptionentry.SetValue(description)
		self.deletebutton.Enable()
		self.savebutton.Enable()
		self.replacemediabutton.Enable()
	
	def AddMedia(self, ID):
		
		busy = wx.BusyCursor()
		
		filename = wx.FileSelector()
		
		if filename == "":
			
			pass
			
		else:
			
			inp = open(filename, "rb")
			
			size = os.path.getsize(filename)
			size = size / 1024.00
			
			if size > 20480:
				
				miscmethods.ShowMessage(self.t("mediatoolargemessage"))
				
			else:
				
				content = inp.read()
				content = base64.encodestring(content)
				inp.close()
				
				todaysdate = datetime.date.today()
				todayssqldate = miscmethods.GetSQLDateFromDate(todaysdate)
				
				uploadedby = todayssqldate + "$$$" + self.localsettings.username
				
				if filename.__contains__("\\"):
					
					filename = filename.replace("\\", "/")
				
				dbmethods.WriteToMediaTable(self.localsettings.dbconnection, False, self.linktype, self.linkid, filename.split("/")[-1], "", size, content, uploadedby)
				
				self.listbox.RefreshList()
		
		del busy
	
	def RenameMedia(self, ID):
		
		listboxid = self.listbox.GetSelection()
		description = self.listbox.htmllist[listboxid][4]
		
		dialog = wx.Dialog(self, -1, self.t("renamelabel"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		descriptionlabel = wx.StaticText(panel, -1, self.t("descriptionlabel"))
		font = descriptionlabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		descriptionlabel.SetFont(font)
		topsizer.Add(descriptionlabel, 0, wx.ALIGN_LEFT)
		
		nameinput = wx.TextCtrl(panel, -1, description, size=(150,-1))
		nameinput.Bind(wx.EVT_CHAR, self.KeyStroke)
		topsizer.Add(nameinput, 0, wx.EXPAND)
		
		panel.SetSizer(topsizer)
		
		panel.nameinput = nameinput
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		dialog.Fit()
		
		nameinput.SetFocus()
		
		dialog.ShowModal()
	
	def KeyStroke(self, ID):
		
		keycode = ID.GetKeyCode()
		
		if keycode == 13:
			
			self.SubmitRename(ID)
		
		ID.Skip()
	
	def SubmitRename(self, ID):
		
		panel = ID.GetEventObject().GetParent()
		
		description = panel.nameinput.GetValue()
		
		listboxid = self.listbox.GetSelection()
		mediaid = self.listbox.htmllist[listboxid][0]
		
		todaysdate = datetime.date.today()
		todayssqldate = miscmethods.GetSQLDateFromDate(todaysdate)
		
		uploadedby = todayssqldate + "$$$" + self.localsettings.username
		
		action = "UPDATE media SET Description = \"" + description + "\" WHERE ID = " + str(mediaid)
		db.SendSQL(action, self.localsettings.dbconnection)
		
		action = "UPDATE media SET uploadedby = \"" + uploadedby + "\" WHERE ID = " + str(mediaid)
		db.SendSQL(action, self.localsettings.dbconnection)
		
		panel.GetParent().Close()
		
		self.listbox.RefreshList()
	
	def DeleteMedia(self, ID):
		
		if miscmethods.ConfirmMessage(self.t("deleteattachedfileconfirm")):
			
			listboxid = self.listbox.GetSelection()
			
			mediaid = self.listbox.htmllist[listboxid][0]
			
			action = "DELETE FROM media WHERE ID = " + str(mediaid)
			db.SendSQL(action, self.localsettings.dbconnection)
			
			self.listbox.RefreshList()
	
	def OpenMedia(self, ID=False):
		
		OpenFileThread(self)

class AttachedFilesListbox(customwidgets.ListCtrlWrapper):
	
	
	
	def __init__(self, parent, localsettings, linktype, linkid):
		
		date_t = localsettings.t("attachmentdatelabel")
		title_t = localsettings.t("attachmenttitlelabel")
		size_t =  localsettings.t("attachmentsizelabel")
		
		columnheadings = (date_t, title_t, size_t)
		
		customwidgets.ListCtrlWrapper.__init__(self, parent, localsettings, columnheadings)
		
		self.htmllist = []
		self.localsettings = localsettings
		self.parent = parent
		self.linktype = linktype
		self.linkid = linkid
	
	def RefreshList(self, ID=False):
		
		action = "SELECT ID, LinkType, LinkID, FileName, Description, FileSize, UploadedBy FROM media WHERE LinkType = " + str(self.linktype) + " AND LinkID = " + str(self.linkid) + " ORDER BY UploadedBy desc"
		
		self.htmllist = db.SendSQL(action, self.localsettings.dbconnection)
		
		customwidgets.ListCtrlWrapper.RefreshList(self)
	
	def ProcessRow(self, rowdata):
		
		filename = rowdata[3]
		description = rowdata[4]
		
		uploaddate = rowdata[6].split("$$$")[0]
		uploaddate = miscmethods.GetDateFromSQLDate(uploaddate)
		uploaddate = miscmethods.FormatDate(uploaddate, self.localsettings)
		
		filesize = str(rowdata[5]) + " KB"
		
		if description == "":
			
			filetext = filename
			
		else:
			
			if filename.__contains__("."):
				
				fileextension = filename.split(".")[-1]
				
			else:
				
				fileextension = ""
			
			
			filetext = description + " (" + fileextension + ")"
		
		output = ((rowdata[0], uploaddate, filetext, filesize), -1)
		
		return output

class OpenFileThread(threading.Thread):
	
	def __init__(self, attachedfilespanel):
		
		threading.Thread.__init__(self)
		self.parent = attachedfilespanel
		self.start()
	
	def run(self):
		
		listboxid = self.parent.listbox.GetSelection()
		
		mediaid = self.parent.listbox.htmllist[listboxid][0]
		
		miscmethods.OpenMedia(mediaid)
