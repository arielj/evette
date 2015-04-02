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
import customwidgets
import appointmentmethods

class EditRotaPanel(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, notebook, localsettings):
		
		busy = wx.BusyCursor()
		
		self.localsettings = localsettings
		
		self.pagetitle = self.t("editrotalabel")
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, self.pagetitle)
		
		self.currentdate = datetime.date.today()
		
		action = "SELECT Name, Position FROM user ORDER BY Name"
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		
		self.staffnames = []
		self.staffpositions = []
		
		for a in results:
			
			self.staffnames.append(a[0])
			self.staffpositions.append(a[1])
		
		wx.Panel.__init__(self, notebook)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		monthsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		monthpanel = wx.Panel(self)
		
		monthsizer.Add(wx.StaticText(monthpanel, -1, ""), 1, wx.EXPAND)
		
		previousbitmap = wx.Bitmap("icons/leftarrow.png")
		previousbutton = wx.BitmapButton(monthpanel, -1, previousbitmap)
		previousbutton.SetToolTipString(self.t("previousmonthtooltip"))
		previousbutton.Bind(wx.EVT_BUTTON, self.PreviousMonth)
		monthsizer.Add(previousbutton, 0, wx.EXPAND)
		
		monthsizer.Add(wx.StaticText(monthpanel, -1, ""), 1, wx.EXPAND)
		
		monthname = miscmethods.GetMonth(int(self.currentdate.strftime("%m")), self.localsettings)
		
		monthlabel = wx.StaticText(monthpanel, -1, monthname + u"\xa0" + self.currentdate.strftime("%Y"))
		monthlabel.SetForegroundColour("red")
		
		font = monthlabel.GetFont()
		font.SetPointSize(font.GetPointSize() + 6)
		monthlabel.SetFont(font)
		monthsizer.Add(monthlabel, 0, wx.EXPAND)
		
		monthsizer.Add(wx.StaticText(monthpanel, -1, ""), 1, wx.EXPAND)
		
		nextbitmap = wx.Bitmap("icons/rightarrow.png")
		nextbutton = wx.BitmapButton(monthpanel, -1, nextbitmap)
		nextbutton.SetToolTipString(self.t("nextmonthtooltip"))
		nextbutton.Bind(wx.EVT_BUTTON, self.NextMonth)
		monthsizer.Add(nextbutton, 0, wx.EXPAND)
		
		monthsizer.Add(wx.StaticText(monthpanel, -1, ""), 1, wx.EXPAND)
		
		addstaffcheckbox = wx.CheckBox(monthpanel, -1, self.t("addstafflabel"))
		addstaffcheckbox.Bind(wx.EVT_CHECKBOX, self.EnableQuickRota)
		monthsizer.Add(addstaffcheckbox, 0, wx.ALIGN_BOTTOM)
		
		quickrotapanel = wx.Panel(monthpanel)
		
		quickrotasizer = wx.BoxSizer(wx.HORIZONTAL)
		
		quickrotasizer.Add(wx.StaticText(self, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		namesizer = wx.BoxSizer(wx.VERTICAL)
		
		namelabel = wx.StaticText(quickrotapanel, -1, self.t("namelabel") + ":")
		font = namelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		namelabel.SetFont(font)
		namesizer.Add(namelabel, 0, wx.EXPAND)
		
		nameentry = wx.ComboBox(quickrotapanel, -1, choices=self.staffnames)
		nameentry.Bind(wx.EVT_COMBOBOX, self.GetStaffPosition)
		namesizer.Add(nameentry, 1, wx.EXPAND)
		
		quickrotasizer.Add(namesizer, 2, wx.EXPAND)
		
		positionsizer = wx.BoxSizer(wx.VERTICAL)
		
		positionlabel = wx.StaticText(quickrotapanel, -1, self.t("positionlabel") + ":")
		font = positionlabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		positionlabel.SetFont(font)
		positionsizer.Add(positionlabel, 0, wx.EXPAND)
		
		positionentry = wx.TextCtrl(quickrotapanel, -1, "")
		positionsizer.Add(positionentry, 1, wx.EXPAND)
		
		quickrotasizer.Add(positionsizer, 2, wx.EXPAND)
		
		timeonsizer = wx.BoxSizer(wx.VERTICAL)
		
		timeonlabel = wx.StaticText(quickrotapanel, -1, self.t("timeonlabel") + ":")
		font = timeonlabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		timeonlabel.SetFont(font)
		timeonsizer.Add(timeonlabel, 0, wx.EXPAND)
		
		timeonentry = wx.TextCtrl(quickrotapanel, -1, str(self.localsettings.openfrom))
		timeonsizer.Add(timeonentry, 1, wx.EXPAND)
		
		quickrotasizer.Add(timeonsizer, 1, wx.EXPAND)
		
		timeoffsizer = wx.BoxSizer(wx.VERTICAL)
		
		timeofflabel = wx.StaticText(quickrotapanel, -1, self.t("timeofflabel") + ":")
		font = timeofflabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		timeofflabel.SetFont(font)
		timeoffsizer.Add(timeofflabel, 0, wx.EXPAND)
		
		timeoffentry = wx.TextCtrl(quickrotapanel, -1, str(self.localsettings.opento))
		timeoffsizer.Add(timeoffentry, 1, wx.EXPAND)
		
		quickrotasizer.Add(timeoffsizer, 1, wx.EXPAND)
		
		operatingsizer = wx.BoxSizer(wx.VERTICAL)
		
		operatinglabel = wx.StaticText(quickrotapanel, -1, self.t("operatinglabel") + ":")
		font = operatinglabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		operatinglabel.SetFont(font)
		operatingsizer.Add(operatinglabel, 0, wx.EXPAND)
		
		operatingentry = wx.CheckBox(quickrotapanel, -1)
		operatingsizer.Add(operatingentry, 1, wx.EXPAND)
		
		quickrotasizer.Add(operatingsizer, 1, wx.EXPAND)
		
		quickrotapanel.SetSizer(quickrotasizer)
		
		quickrotapanel.Hide()
		
		monthsizer.Add(quickrotapanel, 4, wx.EXPAND)
		
		
		monthpanel.SetSizer(monthsizer)
		
		topsizer.Add(monthpanel, 0, wx.EXPAND)
		
		topsizer.Add(wx.StaticText(self, -1, "", size=(-1,20)), 0, wx.EXPAND)
		
		
		calendarsizer = wx.BoxSizer(wx.VERTICAL)
		calendarpanel = wx.Panel(self)
		calendarsizer.Add(calendarpanel, 1, wx.EXPAND)
		topsizer.Add(calendarsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.topsizer = topsizer
		
		self.monthlabel = monthlabel
		self.monthsizer = monthsizer
		self.monthpanel = monthpanel
		self.calendarsizer = calendarsizer
		self.calendarpanel = calendarpanel
		
		self.quickrotapanel = quickrotapanel
		
		self.addstaffcheckbox = addstaffcheckbox
		
		self.nameentry = nameentry
		self.positionentry = positionentry
		self.timeonentry = timeonentry
		self.timeoffentry = timeoffentry
		self.operatingentry = operatingentry
		
		self.RefreshCalendar()
		
		del busy
	
	def GetStaffPosition(self, ID):
		
		staffname = ID.GetEventObject().GetValue()
		
		positionid = -1
		
		for a in range(0, len(self.staffnames)):
			
			if self.staffnames[a] == staffname:
				
				positionid = a
		
		if positionid != -1:
			
			self.positionentry.SetValue(self.staffpositions[positionid])
	
	def EnableQuickRota(self, ID=False):
		
		if ID.GetEventObject().GetValue() == True:
			self.quickrotapanel.Show()
		else:
			self.quickrotapanel.Hide()
		
		self.topsizer.Layout()
	
	def RefreshCalendar(self, ID=False):
		
		self.calendarpanel.Hide()
		self.calendarpanel.Destroy()
		self.calendarpanel = Calendar(self, self.localsettings, self.currentdate.month, self.currentdate.year)
		self.calendarsizer.Add(self.calendarpanel, 1, wx.EXPAND)
		self.calendarsizer.Layout()
	
	def NextMonth(self, ID=False):
		
		
		month = self.currentdate.month
		year = self.currentdate.year
		
		if month == 12:
			
			month = 1
			year = year + 1
			
		else:
			
			month = month + 1
		
		self.currentdate = datetime.date(year, month, 1)
		
		monthname = miscmethods.GetMonth(int(self.currentdate.strftime("%m")), self.localsettings)
		
		self.monthlabel.SetLabel(monthname + u"\xa0" + self.currentdate.strftime("%Y"))
		
		self.monthsizer.Layout()
		
		self.RefreshCalendar()
		
	def PreviousMonth(self, ID=False):
		
		
		month = self.currentdate.month
		year = self.currentdate.year
		
		if month == 1:
			
			month = 12
			year = year - 1
			
		else:
			
			month = month - 1
		
		self.currentdate = datetime.date(year, month, 1)
		
		monthname = miscmethods.GetMonth(int(self.currentdate.strftime("%m")), self.localsettings)
		
		self.monthlabel.SetLabel(monthname + u"\xa0" + self.currentdate.strftime("%Y"))
		
		self.monthsizer.Layout()
		
		self.RefreshCalendar()
	
	def OpenDay(self, ID=False):
		
		if self.addstaffcheckbox.GetValue() == False:
			
			self.monthpanel.Hide()
			self.calendarpanel.Hide()
			self.calendarpanel.Destroy()
			self.calendarpanel = DailyRota(self, self.localsettings, self.currentdate)
			self.calendarsizer.Add(self.calendarpanel, 1, wx.EXPAND)
			self.calendarsizer.Layout()
			
		else:
			
			date = miscmethods.GetSQLDateFromDate(self.currentdate)
			
			name = self.nameentry.GetValue()
			position = self.positionentry.GetValue()
			timeon = self.timeonentry.GetValue()
			timeoff = self.timeoffentry.GetValue()
			
			operating = self.operatingentry.GetValue()
			
			if operating == True:
				operating = 1
			else:
				operating = 0
			
			success = dbmethods.WriteToStaffTable(self.localsettings.dbconnection, date, name, position, timeon, timeoff, operating, False, self.localsettings)
			
			
			
			if success == True:
				self.selectedcell.RefreshCell()
				#self.RefreshCalendar()
		
	def BackToCalendar(self, ID):
		
		self.monthpanel.Show()
		self.calendarpanel.Hide()
		self.calendarpanel.Destroy()
		self.calendarpanel = Calendar(self, self.localsettings, self.currentdate.month, self.currentdate.year)
		self.calendarsizer.Add(self.calendarpanel, 1, wx.EXPAND)
		self.calendarsizer.Layout()
		
class Calendar(wx.ScrolledWindow):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, parent, localsettings, month, year):
		
		self.localsettings = localsettings
		
		self.parent = parent
		
		wx.ScrolledWindow.__init__(self, parent, style=wx.VSCROLL)
		
		self.Hide()
		
		self.SetScrollbars(1,1,1,1)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		self.topsizer = topsizer
		
		gridsizer = wx.FlexGridSizer(cols=7)
		
		for a in range(0, 7):
			
			gridsizer.AddGrowableCol(a)
		
		noofdays = GetDaysInMonth(month, year)
		
		date = datetime.date(year, month, 1)
		
		dayofweek = date.strftime("%w")
		
		if dayofweek == "1":
			
			extradays = 0
			
		elif dayofweek == "2":
			
			extradays = 1
			
		elif dayofweek == "3":
			
			extradays = 2
			
		elif dayofweek == "4":
			
			extradays = 3
			
		elif dayofweek == "5":
			
			extradays = 4
			
		elif dayofweek == "6":
			
			extradays = 5
			
		else:
			
			extradays = 6
		
		for a in (self.t("monday"), self.t("tuesday"), self.t("wednesday"), self.t("thursday"), self.t("friday"), self.t("saturday"), self.t("sunday")):
			
			gridsizer.Add(wx.StaticText(self, -1, a), 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		rowcount = 1
		
		count = 1
		
		if extradays > 0:
			
			for a in range(0, extradays):
				
				count = count + 1
				
				gridsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
				
			gridsizer.AddGrowableRow(rowcount)
			
			rowcount = 2
		
		for a in range(0, noofdays):
			
			gridsizer.Add(DayCell(self, self.localsettings, date), 1, wx.EXPAND)
			
			date = date + datetime.timedelta(days=1)
			
			if count == 1:
				
				gridsizer.AddGrowableRow(rowcount)
				
				rowcount = rowcount + 1
				
			elif count == 7:
				
				count = 0
				
			count = count + 1
		
		topsizer.Add(gridsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.Show()

class DayCell(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, parent, localsettings, date):
		
		self.localsettings = localsettings
		
		self.date = date
		
		self.parent = parent
		
		wx.Panel.__init__(self, parent, style=wx.SIMPLE_BORDER)
		
		self.topsizer = wx.BoxSizer(wx.VERTICAL)
		
		self.SetSizer(self.topsizer)
		
		self.RefreshCell()
	
	def RefreshCell(self):
		
		self.Hide()
		
		stafflist = self.GetStaffList()
		
		try:
			self.topsizer.Remove(self.daycellpanel)
			self.daycellpanel.Destroy()
		except:
			pass
		
		daycellpanel = wx.Panel(self, -1)
		
		if self.date == datetime.date.today():
			
			daycellpanel.SetBackgroundColour("#CBFFD5")
			
		elif self.date.strftime("%w") == "0" or self.date.strftime("%w") == "6":
			
			daycellpanel.SetBackgroundColour("#E8E8E8")
			
		else:
			
			daycellpanel.SetBackgroundColour("white")
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		label = wx.StaticText(daycellpanel, -1, str(self.date.day))
		label.SetForegroundColour("blue")
		font = label.GetFont()
		font.SetPointSize(font.GetPointSize() + 2)
		label.SetFont(font)
		topsizer.Add(label, 0, wx.ALIGN_CENTER)
		
		horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		leftsizer = wx.BoxSizer(wx.VERTICAL)
		
		vetslabel = wx.StaticText(daycellpanel, -1, self.t("vetslabel") + u"\xa0")
		vetslabel.SetForegroundColour("red")
		font = vetslabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		vetslabel.SetFont(font)
		
		leftsizer.Add(vetslabel, 0, wx.ALIGN_LEFT)
		
		vetentries = []
		
		for a in range(0, len(stafflist[0])):
			
			vetentries.append(wx.StaticText(daycellpanel, -1, stafflist[0][a]))
			
			font = vetentries[a].GetFont()
			font.SetPointSize(font.GetPointSize() - 2)
			vetentries[a].SetFont(font)
			
			leftsizer.Add(vetentries[a], 0, wx.ALIGN_LEFT)
		
		horizontalsizer.Add(leftsizer, 1, wx.EXPAND)
		
		centersizer = wx.BoxSizer(wx.VERTICAL)
		
		nurseslabel = wx.StaticText(daycellpanel, -1, self.t("nurseslabel") + u"\xa0")
		nurseslabel.SetForegroundColour("red")
		font = nurseslabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		nurseslabel.SetFont(font)
		centersizer.Add(nurseslabel, 0, wx.ALIGN_LEFT)
		
		nurseentries = []
		
		for a in range(0, len(stafflist[1])):
			
			nurseentries.append(wx.StaticText(daycellpanel, -1, stafflist[1][a]))
			
			font = nurseentries[a].GetFont()
			font.SetPointSize(font.GetPointSize() - 2)
			nurseentries[a].SetFont(font)
			
			centersizer.Add(nurseentries[a], 0, wx.ALIGN_LEFT)
		
		horizontalsizer.Add(centersizer, 1, wx.EXPAND)
		
		rightsizer = wx.BoxSizer(wx.VERTICAL)
		
		otherslabel = wx.StaticText(daycellpanel, -1, self.t("otherslabel"))
		otherslabel.SetForegroundColour("red")
		font = otherslabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		otherslabel.SetFont(font)
		rightsizer.Add(otherslabel, 0, wx.ALIGN_LEFT)
		
		othersentries = []
		
		for a in range(0, len(stafflist[2])):
			
			othersentries.append(wx.StaticText(daycellpanel, -1, stafflist[2][a]))
			
			font = othersentries[a].GetFont()
			font.SetPointSize(font.GetPointSize() - 2)
			othersentries[a].SetFont(font)
			
			rightsizer.Add(othersentries[a], 0, wx.ALIGN_LEFT)
		
		horizontalsizer.Add(rightsizer, 1, wx.EXPAND)
		
		topsizer.Add(horizontalsizer, 1, wx.EXPAND)
		
		daycellpanel.Bind(wx.EVT_LEFT_DOWN, self.DayCellSelected)
		daycellpanel.Bind(wx.EVT_LEFT_DCLICK, self.parent.GetParent().OpenDay)
		
		for a in daycellpanel.GetChildren():
			
			a.Bind(wx.EVT_LEFT_DOWN, self.DayCellSelected)
			a.Bind(wx.EVT_LEFT_DCLICK, self.parent.GetParent().OpenDay)
		
		daycellpanel.SetSizer(topsizer)
		
		self.topsizer.Add(daycellpanel, 1, wx.EXPAND)
		
		self.topsizer.Layout()
		
		self.parent.topsizer.Layout()
		
		self.daycellpanel = daycellpanel
		
		self.Show()
		
	
	def GetStaffList(self):
		
		date = miscmethods.GetSQLDateFromDate(self.date)
		
		action = "SELECT Name, Position FROM staff WHERE Date = \"" + str(date) + "\" ORDER BY Name"
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		
		vets = []
		nurses = []
		others = []
		
		for a in results:
			
			if a[1] == self.t("vetpositiontitle"):
				
				vets.append(a[0])
				
			elif a[1] == self.t("vetnursepositiontitle"):
				
				nurses.append(a[0])
				
			else:
				
				others.append(a[0])
		
		return (vets, nurses, others)
	
	def DayCellSelected(self, ID):
		
		self.parent.GetParent().currentdate = self.date
		self.parent.GetParent().selectedcell = self

class DailyRota(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, parent, localsettings, date):
		
		self.parent = parent
		self.localsettings = localsettings
		self.date = date
		
		wx.Panel.__init__(self, parent)
		#self.SetBackgroundColour("yellow")
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		titlesizer = wx.BoxSizer(wx.HORIZONTAL)
		
		upbitmap = wx.Bitmap("icons/uparrow.png")
		calendarbutton = wx.BitmapButton(self, -1, upbitmap)
		calendarbutton.SetToolTipString(self.parent.t("backtocalendartooltip"))
		calendarbutton.Bind(wx.EVT_BUTTON, self.parent.BackToCalendar)
		titlesizer.Add(calendarbutton, 0, wx.EXPAND)
		
		topsizer.Add(titlesizer, 0, wx.EXPAND)
		
		action = "SELECT Name, Position FROM user ORDER BY Name"
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		stafflist = []
		positionlist = []
		for a in results:
			stafflist.append(a[0])
			positionlist.append(a[1])
		
		horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		horizontalsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		self.stafflist = stafflist
		self.positionlist = positionlist
		
		stafftablesizer = wx.BoxSizer(wx.VERTICAL)
		
		weekday = miscmethods.GetWeekday(int(self.date.strftime("%w")), self.localsettings)
		
		datestring = weekday + u"\xa0" + miscmethods.FormatDate(self.date, self.localsettings)
		
		datelabel = wx.StaticText(self, -1, datestring)
		
		datelabel.SetForegroundColour("red")
		
		font = datelabel.GetFont()
		font.SetPointSize(font.GetPointSize() + 6)
		datelabel.SetFont(font)
		stafftablesizer.Add(datelabel, 0, wx.ALIGN_CENTER)
		
		stafftablewidget = StaffTable(self, self.localsettings, self.date)
		
		stafftablesizer.Add(stafftablewidget, 1, wx.EXPAND)
		
		horizontalsizer.Add(stafftablesizer, 5, wx.EXPAND)
		
		horizontalsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		topsizer.Add(horizontalsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)

def GetDaysInMonth(month, year):
	
	leapyearslist = []
	
	for a in range(1980, 2080, 4):
		
		leapyearslist.append(a)
	
	daysinmonthlist = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]
	
	if leapyearslist.__contains__(year):
		
		if month == 2:
			
			result = 29
			
		else:
			
			result = daysinmonthlist[month - 1]
		
	else:
		
		result = daysinmonthlist[month - 1]
		
	return result

class StaffTable(wx.Panel):
	
	def __init__(self, parent, localsettings, date):
		
		self.parent = parent
		self.localsettings = localsettings
		self.date = date
		self.selectedstaffid = 0
		
		sqldate = miscmethods.GetSQLDateFromDate(self.date)
		
		wx.Panel.__init__(self, self.parent)
		
		#self.SetBackgroundColour("white")
		
		horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		resetsizer = wx.BoxSizer(wx.VERTICAL)
		
		resetsizer.Add(wx.Panel(self), 1, wx.EXPAND)
		
		newbitmap = wx.Bitmap("icons/new.png")
		newbutton = wx.BitmapButton(self, -1, newbitmap)
		newbutton.SetToolTipString(self.parent.t("addstafftodailyrotatooltip"))
		newbutton.Bind(wx.EVT_BUTTON, self.NewRotaEntry)
		
		resetsizer.Add(newbutton, 0, wx.EXPAND)
		
		horizontalsizer.Add(resetsizer, 0, wx.EXPAND)
		
		horizontalsizer.Add(wx.Panel(self, size=(10,-1)), 0, wx.EXPAND)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		action = "SELECT ID, Name, Position, TimeOn, TimeOff, Operating FROM staff WHERE Date = \"" + sqldate + "\" ORDER BY TimeOn, Name"
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		labelslist = (self.parent.t("namelabel"), self.parent.t("positionlabel"), self.parent.t("timeonlabel"), self.parent.t("timeofflabel"), self.parent.t("operatinglabel"))
		
		labelssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		labels = []
		
		for a in range(0, len(labelslist)):
			
			labels.append(wx.StaticText(self, -1, labelslist[a]))
			labels[a].SetForegroundColour("blue")
			
			font = labels[a].GetFont()
			font.SetPointSize(font.GetPointSize() + 4)
			labels[a].SetFont(font)
			
			labelssizer.Add(labels[a], 1, wx.EXPAND)
		
		topsizer.Add(labelssizer, 0, wx.EXPAND)
		
		listitems = []
		panels = []
		
		for a in range(0, len(results)):
			
			staffid = results[a][0]
			
			panels.append(wx.Panel(self))
			
			panels[a].staffdata = results[a]
			
			panels[a].SetBackgroundColour("white")
			
			panels[a].staffid = staffid
			
			panels[a].topsizer = wx.BoxSizer(wx.HORIZONTAL)
			
			for b in range(0, 4):
				
				listitems.append(wx.StaticText(panels[a], -1, str(results[a][b + 1])))
				
				increment = (a * 5) + b
				
				listitems[increment].SetForegroundColour("red")
				
				panels[a].topsizer.Add(listitems[increment], 1, wx.EXPAND)
				
			if results[a][5] == 1:
				
				operating = self.parent.t("yeslabel")
				
			else:
				
				operating = self.parent.t("nolabel")
			
			
			listitems.append(wx.StaticText(panels[a], -1, operating))
			
			increment = (a * 5) + 4
			
			listitems[increment].SetForegroundColour("red")
			
			panels[a].topsizer.Add(listitems[increment], 1, wx.EXPAND)
			
			panels[a].SetSizer(panels[a].topsizer)
			
			panels[a].Bind(wx.EVT_LEFT_DOWN, self.StaffSelected)
			
			for c in panels[a].GetChildren():
				
				c.Bind(wx.EVT_LEFT_DOWN, self.StaffSelected)
			
			topsizer.Add(panels[a], 0, wx.EXPAND)
		
		topsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
		
		editpanel = wx.Panel(self)
		
		editpanel.topsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		namesizer = wx.BoxSizer(wx.VERTICAL)
		
		namelabel = wx.StaticText(editpanel, -1, self.parent.t("namelabel") + ":")
		namesizer.Add(namelabel, 0, wx.EXPAND)
		
		nameentry = wx.ComboBox(editpanel, -1, choices=self.parent.stafflist)
		nameentry.Bind(wx.EVT_COMBOBOX, self.GetStaffPosition)
		namesizer.Add(nameentry, 0, wx.EXPAND)
		
		editpanel.topsizer.Add(namesizer, 1, wx.EXPAND)
		
		positionsizer = wx.BoxSizer(wx.VERTICAL)
		
		positionlabel = wx.StaticText(editpanel, -1, self.parent.t("positionlabel") + ":")
		positionsizer.Add(positionlabel, 0, wx.EXPAND)
		
		positionentry = wx.TextCtrl(editpanel, -1, "")
		positionsizer.Add(positionentry, 0, wx.EXPAND)
		
		editpanel.topsizer.Add(positionsizer, 1, wx.EXPAND)
		
		insizer = wx.BoxSizer(wx.VERTICAL)
		
		inlabel = wx.StaticText(editpanel, -1, self.parent.t("timeonlabel") + ":")
		insizer.Add(inlabel, 0, wx.EXPAND)
		
		inentry = wx.TextCtrl(editpanel, -1, "")
		insizer.Add(inentry, 0, wx.EXPAND)
		
		editpanel.topsizer.Add(insizer, 1, wx.EXPAND)
		
		outsizer = wx.BoxSizer(wx.VERTICAL)
		
		outlabel = wx.StaticText(editpanel, -1, self.parent.t("timeofflabel") + ":")
		outsizer.Add(outlabel, 0, wx.EXPAND)
		
		outentry = wx.TextCtrl(editpanel, -1, "")
		outsizer.Add(outentry, 0, wx.EXPAND)
		
		editpanel.topsizer.Add(outsizer, 1, wx.EXPAND)
		
		operatingsizer = wx.BoxSizer(wx.VERTICAL)
		
		operatinglabel = wx.StaticText(editpanel, -1, self.parent.t("operatinglabel") + ":")
		operatingsizer.Add(operatinglabel, 0, wx.EXPAND)
		
		operatingentry = wx.CheckBox(editpanel, -1)
		operatingsizer.Add(operatingentry, 0, wx.EXPAND)
		
		editpanel.topsizer.Add(operatingsizer, 1, wx.EXPAND)
		
		editpanel.SetSizer(editpanel.topsizer)
		
		editpanel.Disable()
		
		topsizer.Add(editpanel, 0, wx.EXPAND)
		
		self.panels = panels
		
		horizontalsizer.Add(topsizer, 1, wx.EXPAND)
		
		horizontalsizer.Add(wx.Panel(self, size=(10,-1)), 0, wx.EXPAND)
		
		submitsizer = wx.BoxSizer(wx.VERTICAL)
		
		deletebitmap = wx.Bitmap("icons/delete.png")
		deletebutton = wx.BitmapButton(self, -1, deletebitmap)
		deletebutton.SetToolTipString(self.parent.t("deleterotaitemtooltip"))
		deletebutton.Bind(wx.EVT_BUTTON, self.Delete)
		deletebutton.Disable()
		submitsizer.Add(deletebutton, 0, wx.EXPAND)
		
		submitsizer.Add(wx.Panel(self), 1, wx.EXPAND)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		submitbutton = wx.BitmapButton(self, -1, submitbitmap)
		submitbutton.SetToolTipString(self.parent.t("submitrotaitemtooltip"))
		submitbutton.Bind(wx.EVT_BUTTON, self.Submit)
		submitbutton.Disable()
		
		submitsizer.Add(submitbutton, 0, wx.EXPAND)
		
		horizontalsizer.Add(submitsizer, 0, wx.EXPAND)
		
		
		
		self.SetSizer(horizontalsizer)
		
		self.nameentry = nameentry
		self.positionentry = positionentry
		self.inentry = inentry
		self.outentry = outentry
		self.operatingentry = operatingentry
		self.submitbutton = submitbutton
		self.newbutton = newbutton
		self.deletebutton = deletebutton
		
		self.editpanel = editpanel
	
	def GetStaffPosition(self, ID=False):
		
		staffname = ID.GetEventObject().GetValue()
		
		position = ""
		
		for a in range(0, len(self.parent.stafflist)):
			
			if self.parent.stafflist[a] == staffname:
				
				position = self.parent.positionlist[a]
		
		self.positionentry.SetValue(position)
	
	def ClearEditPanel(self, ID=False):
		
		self.nameentry.SetValue("")
		self.positionentry.Clear()
		self.inentry.Clear()
		self.outentry.Clear()
		self.operatingentry.SetValue(False)
	
	def NewRotaEntry(self, ID):
		
		for a in self.panels:
			
			a.SetBackgroundColour("white")
		
		self.ClearEditPanel()
		self.editpanel.Enable()
		self.submitbutton.Enable()
		self.deletebutton.Disable()
		
		self.selectedstaffid = 0
	
	def StaffSelected(self, ID=False):
		
		try:	##This block should run fine on Windows
			selectedpanel = ID.GetEventObject().GetParent()
			staffid = selectedpanel.staffid
			staffdata = selectedpanel.staffdata
		except:
			##This block should run fine on Linux
			selectedpanel = ID.GetEventObject()
			staffid = selectedpanel.staffid
			staffdata = selectedpanel.staffdata
		
		staffid = staffdata[0]
		name = staffdata[1]
		position = staffdata[2]
		timeon = staffdata[3]
		timeoff = staffdata[4]
		operating = staffdata[5]
		
		self.nameentry.SetValue(name)
		self.positionentry.SetValue(position)
		self.inentry.SetValue(timeon)
		self.outentry.SetValue(timeoff)
		
		if operating == 1:
			
			self.operatingentry.SetValue(True)
			
		else:
			
			self.operatingentry.SetValue(False)
		
		
		for a in self.panels:
			
			if a != selectedpanel:
				
				a.SetBackgroundColour("white")
		
			else:
				
				selectedpanel.SetBackgroundColour("yellow")
		
		self.selectedstaffid = staffid
		
		self.editpanel.Enable()
		self.submitbutton.Enable()
		self.deletebutton.Enable()
		self.Refresh()
	
	def Submit(self, ID):
		
		success = True
		
		if self.selectedstaffid == 0:
			
			staffid = False
			
		else:
			
			staffid = self.selectedstaffid
		
		date = miscmethods.GetSQLDateFromDate(self.date)
		
		name = self.nameentry.GetValue()
		
		if name == "":
			miscmethods.ShowMessage("No name")
			success = False
		
		position = self.positionentry.GetValue()
		timeon = self.inentry.GetValue()
		timeoff = self.outentry.GetValue()
		
		operating = self.operatingentry.GetValue()
		
		if operating == True:
			
			operating = 1
			
		else:
			
			operating = 0
		
		if success == True:
			
			if dbmethods.WriteToStaffTable(self.localsettings.dbconnection, date, name, position, timeon, timeoff, operating, staffid, self.localsettings) == True:
				
				self.parent.GetParent().OpenDay()
	
	def Delete(self, ID):
		
		staffid = self.selectedstaffid
		
		if miscmethods.ConfirmMessage("Are you sure that you want to remove this rota item?"):
			
			action = "DELETE FROM staff WHERE ID = " + str(staffid)
			db.SendSQL(action, self.localsettings.dbconnection)
			
			
			self.parent.GetParent().OpenDay()
