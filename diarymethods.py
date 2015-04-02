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
import customwidgets
import datetime
import clientmethods
import animalmethods
import appointmentmethods

REFRESH = 1100
ADD = 1101
EDIT = 1102
DELETE = 1103
OPEN_LINK = 1104

def GetLinkType(linktypeid):
	
	linktypes = ("client", "animal", "appointment")
	
	if linktypeid == 0:
		
		return "None"
		
	else:
		
		return linktypes[linktypeid - 1]

class DiarySettings:
	
	def __init__(self, localsettings, ID):
		
		self.localsettings = localsettings
		
		if ID == False:
			
			today = datetime.date.today()
			self.ID = False
			self.date = miscmethods.GetSQLDateFromDate(today)
			self.name = ""
			self.position = ""
			self.subject = ""
			self.note = ""
			self.removed = ""
			self.linktype = 0
			self.linkid = 0
			self.changelog = ""
			
		else:
			
			action = "SELECT Date, Name, Position, Subject, Note, Removed, LinkType, LinkID, ChangeLog FROM diary WHERE ID = " + str(ID)
			results = db.SendSQL(action, self.localsettings.dbconnection)
			
			
			self.ID = ID
			self.date = results[0][0]
			self.name = results[0][1]
			self.position = results[0][2]
			self.subject = results[0][3]
			self.note = results[0][4]
			self.removed = results[0][5]
			if str(self.removed) == "None":
				self.removed = ""
			self.linktype = results[0][6]
			self.linkid = results[0][7]
			self.changelog = results[0][8]
	
	def Submit(self):
		
		currenttime = datetime.datetime.today().strftime("%x %X")
		userid = self.localsettings.userid
		
		if self.changelog == "":
			self.changelog = currenttime + "%%%" + str(userid)
		else:
			self.changelog = currenttime + "%%%" + str(userid) + "$$$" + self.changelog
		
		dbmethods.WriteToDiaryTable(self.localsettings.dbconnection, self)
		

class EditDiaryPanel(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return  self.localsettings.t(field,idx)
	
	def __init__(self, notebook, localsettings):
		
		busy = wx.BusyCursor()
		
		self.notebook = notebook
		
		self.localsettings = localsettings
		
		self.pagetitle = self.t("editdiarypagetitle")
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, self.pagetitle)
		self.pageimage = "icons/diary.png"
		
		users = []
		positions = []
		
		action = "SELECT Name, Position FROM user"
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		
		for a in results:
			users.append(a[0])
			if positions.__contains__(a[1]) == False:
				positions.append(a[1])
			
		users.sort()
		positions.sort()
		
		wx.Panel.__init__(self, notebook)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		topsizer.Add(wx.StaticText(self, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		filtersizer1 = wx.BoxSizer(wx.HORIZONTAL)
		
		fromcheckbox = wx.CheckBox(self, -1, "")
		fromcheckbox.Bind(wx.EVT_CHECKBOX, self.FromDateChecked)
		filtersizer1.Add(fromcheckbox, 0, wx.ALIGN_BOTTOM)
		
		fromsizer = wx.BoxSizer(wx.VERTICAL)
		
		fromlabel = wx.StaticText(self, -1, self.t("fromlabel") + ":")
		font = fromlabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		fromlabel.SetFont(font)
		fromsizer.Add(fromlabel, 0, wx.ALIGN_LEFT)
		
		fromdateentry = customwidgets.DateCtrl(self, self.localsettings)
		fromdateentry.SetSize((-1,-1))
		fromdateentry.Disable()
		fromsizer.Add(fromdateentry, 0, wx.EXPAND)
		
		filtersizer1.Add(fromsizer, 1, wx.EXPAND)
		
		filtersizer1.Add(wx.StaticText(self, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		tosizer = wx.BoxSizer(wx.VERTICAL)
		
		todatelabel = wx.StaticText(self, -1, self.t("tolabel") + ":")
		todatelabel.SetFont(font)
		tosizer.Add(todatelabel, 0, wx.ALIGN_LEFT)
		
		todateentry = customwidgets.DateCtrl(self, self.localsettings)
		todateentry.SetSize((-1,-1))
		tosizer.Add(todateentry, 0, wx.EXPAND)
		
		filtersizer1.Add(tosizer, 1, wx.EXPAND)
		
		filtersizer1.Add(wx.StaticText(self, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		usersizer = wx.BoxSizer(wx.VERTICAL)
		userlabel = wx.StaticText(self, -1, self.t("usernamelabel") + ":")
		userlabel.SetFont(font)
		usersizer.Add(userlabel, 0, wx.ALIGN_LEFT)
		
		userentry = wx.ComboBox(self, -1, self.localsettings.username, choices=users)
		usersizer.Add(userentry, 0, wx.EXPAND)
		
		filtersizer1.Add(usersizer, 2, wx.EXPAND)
		
		filtersizer1.Add(wx.StaticText(self, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		positionsizer = wx.BoxSizer(wx.VERTICAL)
		
		positionlabel = wx.StaticText(self, -1, self.t("positionlabel") + ":")
		positionlabel.SetFont(font)
		positionsizer.Add(positionlabel, 0, wx.ALIGN_LEFT)
		
		positionentry = wx.ComboBox(self, -1, self.localsettings.userposition, choices=positions)
		positionsizer.Add(positionentry, 0, wx.EXPAND)
		
		filtersizer1.Add(positionsizer, 2, wx.EXPAND)
		
		topsizer.Add(filtersizer1, 0, wx.EXPAND)
		
		topsizer.Add(wx.StaticText(self, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		filtersizer2 = wx.BoxSizer(wx.HORIZONTAL)
		
		clearbitmap = wx.Bitmap("icons/reset.png")
		clearbutton = wx.BitmapButton(self, -1, clearbitmap)
		clearbutton.SetToolTipString(self.t("cleardiarytooltip"))
		clearbutton.Bind(wx.EVT_BUTTON, self.ClearEntries)
		filtersizer2.Add(clearbutton, 0, wx.ALIGN_BOTTOM)
		
		filtersizer2.Add(wx.StaticText(self, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		subjectsizer = wx.BoxSizer(wx.VERTICAL)
		
		subjectlabel = wx.StaticText(self, -1, self.t("subjectcontainslabel") + ":")
		subjectlabel.SetFont(font)
		subjectsizer.Add(subjectlabel, 0, wx.ALIGN_LEFT)
		
		subjectentry = wx.TextCtrl(self, -1, "")
		subjectsizer.Add(subjectentry, 0, wx.EXPAND)
		
		filtersizer2.Add(subjectsizer, 1, wx.EXPAND)
		
		filtersizer2.Add(wx.StaticText(self, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		notesizer = wx.BoxSizer(wx.VERTICAL)
		
		notelabel = wx.StaticText(self, -1, self.t("notecontainslabel") + ":")
		notelabel.SetFont(font)
		notesizer.Add(notelabel, 0, wx.ALIGN_LEFT)
		
		noteentry = wx.TextCtrl(self, -1, "")
		notesizer.Add(noteentry, 0, wx.EXPAND)
		
		filtersizer2.Add(notesizer, 1, wx.EXPAND)
		
		filtersizer2.Add(wx.StaticText(self, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		removedcheckbox = wx.CheckBox(self, -1, self.t("showremovedlabel"))
		removedcheckbox.SetFont(font)
		filtersizer2.Add(removedcheckbox, 0, wx.ALIGN_BOTTOM)
		
		filtersizer2.Add(wx.StaticText(self, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		refreshbitmap = wx.Bitmap("icons/refresh.png")
		refreshbutton = wx.BitmapButton(self, -1, refreshbitmap)
		refreshbutton.SetToolTipString(self.t("refreshdiarytooltip"))
		filtersizer2.Add(refreshbutton, 0, wx.ALIGN_BOTTOM)
		
		topsizer.Add(filtersizer2, 0, wx.EXPAND)
		
		topsizer.Add(wx.StaticText(self, -1, "", size=(-1,10)), 0, wx.EXPAND)
		
		diarylistbox = DiaryNotesListbox(self)
		diarylistbox.listctrl.Bind(wx.EVT_RIGHT_DOWN, self.DiaryPopup)
		
		if self.localsettings.editdiary == 1:
			
			diarylistbox.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.EditNote)
		
		topsizer.Add(diarylistbox, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.fromdateentry = fromdateentry
		self.todateentry = todateentry
		self.userentry = userentry
		self.positionentry = positionentry
		self.subjectentry = subjectentry
		self.noteentry = noteentry
		self.removedcheckbox = removedcheckbox
		
		self.fromcheckbox = fromcheckbox
		self.diarylistbox = diarylistbox
		
		refreshbutton.Bind(wx.EVT_BUTTON, self.diarylistbox.RefreshList)
		self.diarylistbox.RefreshList()
		
		del busy
	
	def DiaryPopup(self, ID):
		
		popupmenu = wx.Menu()
		
		add = wx.MenuItem(popupmenu, ADD, self.t("addlabel"))
		add.SetBitmap(wx.Bitmap("icons/new.png"))
		popupmenu.AppendItem(add)
		wx.EVT_MENU(popupmenu, ADD, self.NewNote)
		
		if self.diarylistbox.listctrl.GetSelectedItemCount() > 0:
			
			edit = wx.MenuItem(popupmenu, EDIT, self.t("editlabel"))
			edit.SetBitmap(wx.Bitmap("icons/edit.png"))
			popupmenu.AppendItem(edit)
			wx.EVT_MENU(popupmenu, EDIT, self.EditNote)
			
			delete = wx.MenuItem(popupmenu, DELETE, self.t("deletelabel"))
			delete.SetBitmap(wx.Bitmap("icons/delete.png"))
			popupmenu.AppendItem(delete)
			wx.EVT_MENU(popupmenu, DELETE, self.DeleteNote)
			
			popupmenu.AppendSeparator()
			
			listboxid = self.diarylistbox.GetSelection()
			linktype = GetLinkType(self.diarylistbox.htmllist[listboxid][8])
			linkid = self.diarylistbox.htmllist[listboxid][9]
			
			if linktype != "None":
				
				link = wx.MenuItem(popupmenu, OPEN_LINK, self.t("opentargetrecordtooltip"))
				link.SetBitmap(wx.Bitmap("icons/uparrow.png"))
				popupmenu.AppendItem(link)
				wx.EVT_MENU(popupmenu, OPEN_LINK, self.OpenLink)
				
				popupmenu.AppendSeparator()
		
		refresh = wx.MenuItem(popupmenu, REFRESH, self.t("refreshlabel"))
		refresh.SetBitmap(wx.Bitmap("icons/refresh.png"))
		popupmenu.AppendItem(refresh)
		wx.EVT_MENU(popupmenu, REFRESH, self.diarylistbox.RefreshList)
		
		self.PopupMenu(popupmenu)
	
	def NewNote(self, ID):
		
		title = self.t("nolinklabel")
		diarynotepanel = DiaryNotePanel(self.notebook, self.localsettings, 0, 0, title, False, self)
		self.notebook.AddPage(diarynotepanel)
	
	def ClearEntries(self, ID):
		
		self.fromcheckbox.SetValue(False)
		self.FromDateChecked()
		
		todayswxdate = miscmethods.GetTodaysWXDate()
		
		self.todateentry.SetValue(todayswxdate)
		self.userentry.SetValue("")
		self.positionentry.SetValue("")
		self.subjectentry.Clear()
		self.noteentry.Clear()
		self.removedcheckbox.SetValue(False)
	
	def FromDateChecked(self, ID=False):
		
		if self.fromcheckbox.GetValue() == True:
			
			self.fromdateentry.Enable()
			
		else:
			
			self.fromdateentry.Disable()
	
	def OpenLink(self, ID):
		
		listboxid = self.diarylistbox.GetSelection()
		
		linktype = GetLinkType(self.diarylistbox.htmllist[listboxid][8])
		
		linkid = self.diarylistbox.htmllist[listboxid][9]
		
		if linktype == "client":
			
			clientsettings = clientmethods.ClientSettings(self.localsettings, linkid)
			clientpanel = clientmethods.ClientPanel(self.notebook, clientsettings)
			self.notebook.AddPage(clientpanel)
			
		elif linktype == "animal":
			
			animalsettings = animalmethods.AnimalSettings(self.localsettings, False, linkid)
			animalpanel = animalmethods.AnimalPanel(self.notebook, animalsettings)
			self.notebook.AddPage(animalpanel)
			
		elif linktype == "appointment":
			
			appointmentsettings = appointmentmethods.AppointmentSettings(self.localsettings, False, linkid)
			appointmentpanel = appointmentmethods.AppointmentPanel(self.notebook, appointmentsettings)
			self.notebook.AddPage(appointmentpanel)
	
	def DeleteNote(self, ID):
		
		listboxid = self.diarylistbox.GetSelection()
		
		noteid = self.diarylistbox.htmllist[listboxid][0]
		
		if miscmethods.ConfirmMessage(self.t("confirmdeletediarynotemessage")):
			
			action = "DELETE FROM diary WHERE ID = " + str(noteid)
			results = db.SendSQL(action, self.localsettings.dbconnection)
			
			
			self.diarylistbox.RefreshList()
	
	def EditNote(self, ID):
		
		title = ""
		
		listboxid = self.diarylistbox.GetSelection()
		
		noteid = self.diarylistbox.htmllist[listboxid][0]
		
		linktype = self.diarylistbox.htmllist[listboxid][8]
		linkid = self.diarylistbox.htmllist[listboxid][9]
		
		if linktype == 1:
			
			action = "SELECT ClientTitle, ClientSurname FROM client WHERE ID = " + str(linkid)
			results = db.SendSQL(action, self.localsettings.dbconnection)
			
			
			title = results[0][0] + " " + results[0][1]
			
		elif linktype == 2:
			
			action = "SELECT animal.Name, client.ClientSurname, animal.Species FROM animal INNER JOIN client ON animal.OwnerID = client.ID WHERE animal.ID = " + str(linkid)
			results = db.SendSQL(action, self.localsettings.dbconnection)
			
			
			title = results[0][0] + " " + results[0][1] + " (" + results[0][2] + ")"
		
		diarynotepanel = DiaryNotePanel(self.notebook, self.localsettings, linktype, linkid, title, noteid, self)
		self.notebook.AddPage(diarynotepanel)

class DiaryNotesListbox(customwidgets.ListCtrlWrapper):
	
	def t(self, field, idx = 0):
		
		return  self.localsettings.t(field,idx)
	
	def __init__(self, parent):
		
		self.htmllist = []
		self.localsettings = parent.localsettings
		self.parent = parent
		
		columnheadings = ( self.t("datelabel"), self.t("namelabel"), self.t("positionlabel"), self.t("linklabel"), self.t("subjectlabel"), self.t("removedlabel") )
		
		#print "columnheadings = " + str(columnheadings)
		
		customwidgets.ListCtrlWrapper.__init__(self, parent, self.localsettings, columnheadings)
	
	def ProcessRow(self, rowdata):
		
		#(ID, VaccinationID, Date, Amount, BatchNo, WhereTo, AppointmentID)
		
		date = miscmethods.GetDateFromSQLDate(rowdata[1])
		date = miscmethods.FormatDate(date, self.localsettings)
		
		name = rowdata[2]
		position = rowdata[3]
			
		subject = rowdata[4]
		note = rowdata[5]
		
		linkinfo = rowdata[10]
		
		if str(rowdata[6]) != "None":
			
			removed = miscmethods.GetDateFromSQLDate(rowdata[6])
			removed = miscmethods.FormatDate(removed, self.localsettings)
			#isremoved = "<font color=red size=3><b>" + self.parent.t("removedlabel") + "</b></font>"
			
		else:
			
			removed = ""
		
		output = ( (rowdata[0], date, name, position, linkinfo, subject, removed ), -1 )
		
		return output
	
	def RefreshList(self, ID=False):
		
		fromdate = self.parent.fromdateentry.GetValue()
		fromdate = miscmethods.GetSQLDateFromWXDate(fromdate)
		
		todate = self.parent.todateentry.GetValue()
		todate = miscmethods.GetSQLDateFromWXDate(todate)
		
		name = self.parent.userentry.GetValue()
		position = self.parent.positionentry.GetValue()
		subject = self.parent.subjectentry.GetValue()
		note = self.parent.noteentry.GetValue()
		removed = self.parent.removedcheckbox.GetValue()
		
		action = "SELECT diary.ID, diary.Date, diary.Name, diary.Position, diary.Subject, diary.Note, diary.Removed, diary.ChangeLog, diary.LinkType, diary.LinkID, CASE WHEN diary.LinkType = 1 THEN CONCAT(\"" + self.parent.t("clientlabel") + ": \", client.ClientTitle, \" \", client.ClientSurname) WHEN diary.LinkType = 2 THEN CONCAT(\"" + self.parent.t("animallabel") + ": \", animal.Name, \" \", client.ClientSurname, \" (\", animal.Species, \")\") WHEN diary.LinkType = 3 THEN CONCAT(\"" + self.parent.t("appointmentappointmentforlabel") + ": \", animal.Name, \" \", client.ClientSurname, \" (\", animal.Species, \")\") ELSE \"\" END AS LinkInfo FROM diary LEFT JOIN appointment ON diary.LinkType = 3 AND diary.LinkID = appointment.ID LEFT JOIN animal ON ( diary.LinkType = 2 AND diary.LinkID = animal.ID ) OR ( diary.LinkType = 3 AND appointment.AnimalID = animal.ID ) LEFT JOIN client ON ( diary.LinkType = 1 AND diary.LinkID = client.ID ) OR ( diary.LinkType = 2 AND animal.OwnerID = client.ID ) OR ( diary.LinkType = 3 AND appointment.OwnerID = client.ID ) WHERE "
		
		sqlconditions = ""
		
		if self.parent.fromcheckbox.GetValue() == True:
			
			sqlconditions = sqlconditions + "diary.Date BETWEEN \"" + fromdate + "\" AND \"" + todate + "\" "
			
		else:
			
			sqlconditions = sqlconditions + "diary.Date <= \"" + todate + "\" "
		
		if name != "":
			
			if sqlconditions != "":
				
				sqlconditions = sqlconditions + "AND ( "
			
			sqlconditions = sqlconditions + "diary.Name = \"" + name + "\" "
		
		if position != "":
			
			if name != "":
				
				sqlconditions = sqlconditions + "OR "
				
			else:
				
				if sqlconditions != "":
					
					sqlconditions = sqlconditions + "AND "
			
			sqlconditions = sqlconditions + "diary.Position = \"" + position + "\" "
		
		if name != "":
			
			sqlconditions = sqlconditions + " OR ( diary.Name = \"\" AND diary.Position = \"\" ) ) "
		
		if subject != "":
			
			if sqlconditions != "":
				
				sqlconditions = sqlconditions + "AND "
			
			sqlconditions = sqlconditions + "diary.Subject LIKE \"%" + subject + "%\" "
		
		if note != "":
			
			if sqlconditions != "":
				
				sqlconditions = sqlconditions + "AND "
			
			sqlconditions = sqlconditions + "diary.Note LIKE \"%" + note + "%\" "
			
		if removed == False:
			
			if sqlconditions != "":
				
				sqlconditions = sqlconditions + "AND "
			
			sqlconditions = sqlconditions + "diary.Removed = \"0000-00-00\" "
		
		
		action = action + sqlconditions + "ORDER BY diary.Date, diary.Position, diary.Name"
		self.htmllist = db.SendSQL(action, self.localsettings.dbconnection)
		
		customwidgets.ListCtrlWrapper.RefreshList(self)
		
class DiaryNotePanel(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return  self.localsettings.t(field,idx)
	
	def __init__(self, notebook, localsettings, linktype, linkid, title, ID=False, parent=False):
		
		self.localsettings = localsettings
		
		self.parent = parent
		
		self.diarydata = DiarySettings(self.localsettings, ID)
		
		self.diarydata.linktype = linktype
		self.diarydata.linkid = linkid
		
		self.pagetitle = self.t("diarynotelabel") + " - " + title
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, self.pagetitle)
		
		self.pageimage = "icons/diary.png"
		
		users = []
		positions = []
		
		action = "SELECT Name, Position FROM user"
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		
		for a in results:
			users.append(a[0])
			if positions.__contains__(a[1]) == False:
				positions.append(a[1])
			
		users.sort()
		positions.sort()
		
		wx.Panel.__init__(self, notebook)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		horizontalsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		gridsizer = wx.FlexGridSizer(cols=2)
		
		
		gridsizer.AddGrowableCol(1)
		gridsizer.AddGrowableRow(4)
		gridsizer.AddGrowableRow(6)
		
		datelabel = wx.StaticText(self, -1, self.t("datelabel") + ":")
		gridsizer.Add(datelabel, 0, wx.ALIGN_RIGHT)
		
		dateentry = customwidgets.DateCtrl(self, self.localsettings)
		gridsizer.Add(dateentry, 0, wx.ALIGN_LEFT)
		
		namelabel = wx.StaticText(self, -1, self.t("usernamelabel") + ":")
		gridsizer.Add(namelabel, 0, wx.ALIGN_RIGHT)
		
		nameentry = wx.ComboBox(self, -1, self.diarydata.name, choices=users, size=(300,-1))
		gridsizer.Add(nameentry, 0, wx.ALIGN_LEFT)
		
		positionlabel = wx.StaticText(self, -1, self.t("positionlabel") + ":")
		gridsizer.Add(positionlabel, 0, wx.ALIGN_RIGHT)
		
		positionentry = wx.ComboBox(self, -1, self.diarydata.position, choices=positions, size=(300,-1))
		gridsizer.Add(positionentry, 0, wx.ALIGN_LEFT)
		
		subjectlabel = wx.StaticText(self, -1, self.t("subjectlabel") + ":")
		gridsizer.Add(subjectlabel, 0, wx.ALIGN_RIGHT)
		
		subjectentry = wx.TextCtrl(self, -1, self.diarydata.subject)
		gridsizer.Add(subjectentry, 1, wx.EXPAND)
		
		notelabel = wx.StaticText(self, -1, self.t("notelabel") + ":")
		gridsizer.Add(notelabel, 0, wx.ALIGN_RIGHT)
		
		noteentry = wx.TextCtrl(self, -1, self.diarydata.note, style=wx.TE_MULTILINE)
		gridsizer.Add(noteentry, 1, wx.EXPAND)
		
		removedlabel = wx.StaticText(self, -1, self.t("removedlabel") + ":")
		gridsizer.Add(removedlabel, 0, wx.ALIGN_RIGHT)
		
		removedentry = customwidgets.DateCtrl(self, self.localsettings)
		if str(self.diarydata.removed) == "":
			removedentry.Clear()
		else:
			removeddate = miscmethods.GetWXDateFromSQLDate(self.diarydata.removed)
			removedentry.SetValue(removeddate)
		gridsizer.Add(removedentry, 1, wx.EXPAND)
		
		changeloglabel = wx.StaticText(self, -1, self.t("changelog") + ":")
		gridsizer.Add(changeloglabel, 0, wx.ALIGN_RIGHT)
		
		if self.diarydata.ID == False:
			
			changelog = ""
			
		else:
			
			changelog = miscmethods.FormatChangeLog(self.diarydata.changelog, self.t("diarynotelabel"), self.localsettings.dbconnection)
			
		
		changelogentry = wx.TextCtrl(self, -1, changelog, style=wx.TE_MULTILINE)
		changelogentry.Disable()
		gridsizer.Add(changelogentry, 1, wx.EXPAND)
		
		gridsizer.Add(wx.StaticText(self, -1, ""), 0, wx.EXPAND)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		submitbutton = wx.BitmapButton(self, -1, submitbitmap)
		submitbutton.SetToolTipString(self.t("submitlabel"))
		submitbutton.Bind(wx.EVT_BUTTON, self.Submit)
		gridsizer.Add(submitbutton, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		horizontalsizer.Add(gridsizer, 4, wx.EXPAND)
		
		horizontalsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		topsizer.Add(horizontalsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.dateentry = dateentry
		self.nameentry = nameentry
		self.positionentry = positionentry
		self.subjectentry = subjectentry
		self.noteentry = noteentry
		self.removedentry = removedentry
		self.notebook = notebook
	
	def Submit(self, ID=False):
		
		date = self.dateentry.GetValue()
		self.diarydata.date = miscmethods.GetSQLDateFromWXDate(date)
		self.diarydata.name = self.nameentry.GetValue()
		self.diarydata.position = self.positionentry.GetValue()
		self.diarydata.subject = self.subjectentry.GetValue()
		self.diarydata.note = self.noteentry.GetValue()
		removed = self.removedentry.GetValue()
		if str(removed) != "":
			self.diarydata.removed = miscmethods.GetSQLDateFromWXDate(removed)
		else:
			self.diarydata.removed = "0000-00-00"
		
		self.diarydata.Submit()
		
		if self.parent != False:
			try:
				self.parent.diarylistbox.RefreshList()
			except:
				pass
		
		self.notebook.ClosePage(self.notebook.activepage)
