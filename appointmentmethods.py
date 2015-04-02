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
import datetime
import animalmethods
import clientmethods
import db
import dbmethods
import customwidgets
import diarymethods
import vetmethods
import viewappointments
import formmethods

class AppointmentSettings:
  
  def __init__(self, localsettings, animalid, ID):
    
    #(ID, AnimalID, OwnerID, Date, Time, AppointmentReason, Arrived, WithVet, Problem, Notes, Plan, Done, Operation, Vet)
    
    self.localsettings = localsettings
    
    if ID == False:
      
      self.ID = False
      self.animalid = animalid
      
      self.animaldata = animalmethods.AnimalSettings(self.localsettings, False, self.animalid)
      
      self.clientdata = clientmethods.ClientSettings(self.localsettings, self.animaldata.ownerid)
      
      self.ownerid = self.clientdata.ID
      self.date = datetime.date.today()
      self.date = miscmethods.GetSQLDateFromDate(self.date)
      self.time = "14:00"
      self.reason = u"Chequeo"
      self.arrived = 0
      self.withvet = 0
      self.problem = u""
      self.notes = u""
      self.plan = u""
      self.done = 0
      self.operation = 0
      self.vet = u"None"
      currenttime = datetime.datetime.today().strftime("%x %X")
      self.changelog = str(currenttime) + "%%%" + str(self.localsettings.userid)
      self.staying = 0
      self.arrivaltime = None
    else:
      action = "SELECT * FROM appointment WHERE ID = " + str(ID)
      results = db.SendSQL(action, self.localsettings.dbconnection)
      
      self.ID = ID
      self.animalid = results[0][1]
      self.ownerid = results[0][2]
      self.date = results[0][3]
      self.time = results[0][4]
      self.reason = unicode(results[0][5], "utf8")
      self.arrived = results[0][6]
      self.withvet = results[0][7]
      self.problem = unicode(results[0][8], "utf8")
      self.notes = unicode(results[0][9], "utf8")
      self.plan = unicode(results[0][10], "utf8")
      self.done = results[0][11]
      self.operation = results[0][12]
      self.vet = unicode(results[0][13], "utf8")
      self.changelog = results[0][14]
      self.staying = results[0][15]
      self.arrivaltime = results[0][16]
      
      self.animaldata = animalmethods.AnimalSettings(self.localsettings, False, self.animalid)
      self.clientdata = clientmethods.ClientSettings(self.localsettings, self.animaldata.ownerid)
  
  def Submit(self, force=False):
    
    locked = False
    
    if self.ID != False:
      
      action = "SELECT ChangeLog, Arrived FROM appointment WHERE ID = " + str(self.ID)
      results = db.SendSQL(action, self.localsettings.dbconnection)
      
      changelog = results[0][0]
      arrived = results[0][1]
      
      if arrived == 0 and self.arrived == 1:
        
        self.arrivaltime = datetime.datetime.today().strftime("%X")
      
      if changelog != self.changelog:
        
        
        
        if miscmethods.ConfirmMessage(self.localsettings.dictionary["filealteredchoice"][self.localsettings.language]):
          
          locked = False
          
        else:
          
          locked = True
    
    if locked == False:
      
      currenttime = datetime.datetime.today().strftime("%x %X")
      userid = self.localsettings.userid
      
      if self.changelog == "":
        self.changelog = currenttime + "%%%" + str(userid)
      else:
        self.changelog = currenttime + "%%%" + str(userid) + "$$$" + self.changelog
      
      dbmethods.WriteToAppointmentTable(self.localsettings.dbconnection, self)

class AppointmentPanel(wx.Panel):
  
  def t(self, field, idx = 0):
    
    return  self.appointmentdata.localsettings.t(field)
  
  def __init__(self, notebook, appointmentdata):
    
    self.appointmentdata = appointmentdata
    
    self.notebook = notebook
    
    self.kennelid = appointmentdata.staying
    
    wx.Panel.__init__(self, notebook)
    
    self.viewappointmentspanel = False
    self.animalpanel = False
    self.kennelspanel = False
    
    if self.appointmentdata.operation == 0:
      pagetitle = self.t("appointmentappointmentforlabel") + " " + self.appointmentdata.animaldata.name + " " + self.appointmentdata.clientdata.surname
    else:
      pagetitle = self.t("appointmentoperationforlabel") + " " + self.appointmentdata.animaldata.name + " " + self.appointmentdata.clientdata.surname
    
    self.pagetitle = miscmethods.GetPageTitle(notebook, pagetitle)
    self.pageimage = "icons/appointment.png"
    
    datesizer = wx.BoxSizer(wx.HORIZONTAL)
    
    datevertsizer = wx.BoxSizer(wx.VERTICAL)
    
    datelabel = wx.StaticText(self, -1, self.t("datelabel") + ":")
    font = datelabel.GetFont()
    font.SetPointSize(font.GetPointSize() - 2)
    datelabel.SetFont(font)
    datevertsizer.Add(datelabel, 0, wx.ALIGN_LEFT)
    
    self.appointmententry = AppointmentDateCtrl(self, self.appointmentdata.localsettings)
    datevertsizer.Add(self.appointmententry, 1, wx.EXPAND)
    
    appointmentdate = miscmethods.GetWXDateFromSQLDate(self.appointmentdata.date)
    self.appointmententry.SetValue(appointmentdate)
    
    action = "SELECT Name FROM user WHERE Position = \"" + self.t("vetpositiontitle") + "\""
    results = db.SendSQL(action, self.appointmentdata.localsettings.dbconnection)
    
    vets = []
    if len(results) != 0:
      for a in results:
        vets.append(a[0])
    
    vetsizer = wx.BoxSizer(wx.VERTICAL)
    
    vetlabel = wx.StaticText(self, -1, self.t("vetlabel") + ":")
    vetlabel.SetFont(font)
    vetsizer.Add(vetlabel, 0, wx.ALIGN_LEFT)
    
    self.vetcombobox = wx.ComboBox(self, -1, self.t("vetpositiontitle"), choices=vets)
    if self.appointmentdata.vet != "None":
      self.vetcombobox.SetValue(str(self.appointmentdata.vet))
    self.vetcombobox.Bind(wx.EVT_CHAR, self.UseVetComboBox)
    self.vetcombobox.SetToolTipString(self.t("appointmententervettooltip"))
    vetsizer.Add(self.vetcombobox, 1, wx.EXPAND)
    
    datesizer.Add(datevertsizer, 1, wx.EXPAND)
    datesizer.Add(vetsizer, 1, wx.EXPAND)
    
    reasonsizer = wx.BoxSizer(wx.VERTICAL)
    self.reasonlabel = wx.StaticText(self, -1, self.t("appointmentreasonlabel"))
    self.reasonlabel.SetFont(font)
    reasonsizer.Add(self.reasonlabel, 0, wx.EXPAND)
    
    self.reasonentry = wx.TextCtrl(self, -1, self.appointmentdata.reason, style=wx.TE_MULTILINE, size=(-1,100))
    self.reasonentry.Bind(wx.EVT_LEFT_DCLICK, self.ChooseAppointmentReason)
    self.reasonentry.SetToolTipString(self.t("doubleclickforreasonstooltip"))
    self.reasonentry.SetFocus()
    
    reasonsizer.Add(self.reasonentry, 1, wx.EXPAND)
    
    searchsizer = wx.BoxSizer(wx.VERTICAL)
    searchsizer.Add(datesizer, 0, wx.EXPAND)
    searchsizer.Add(reasonsizer, 0, wx.EXPAND)
    
    self.opcheckbox = wx.CheckBox(self, -1, self.t("appointmentisopcheckbox", 0))
    self.opcheckbox.SetFont(font)
    self.opcheckbox.Bind(wx.EVT_CHECKBOX, self.SwitchToOps)
    self.opcheckbox.SetToolTipString(self.t("appointmentisopcheckbox", 1))
    searchsizer.Add(self.opcheckbox, 0, wx.ALIGN_LEFT)
    
    searchspacer2 = wx.StaticText(self, -1, "", size=(-1,10))
    searchsizer.Add(searchspacer2, 0, wx.EXPAND)
    
    #appointmenttimesizer = wx.BoxSizer(wx.HORIZONTAL)
    self.appointmenttimelabel = wx.StaticText(self, -1, self.t("timelabel") + ":")
    self.appointmenttimelabel.SetFont(font)
    
    time = str(self.appointmentdata.time)
    
    if len(str(time)) == 7:
      time = "0" + time[:4]
    else:
      time = time[:5]
    
    self.appointmenttimeentry = wx.TextCtrl(self, -1, time)
    searchsizer.Add(self.appointmenttimelabel, 0, wx.ALIGN_LEFT)
    searchsizer.Add(self.appointmenttimeentry, 0, wx.ALIGN_LEFT)
    
    #searchsizer.Add(appointmenttimesizer, 0, wx.EXPAND)
    
    searchspacer3 = wx.StaticText(self, -1, "", size=(-1,10))
    searchsizer.Add(searchspacer3, 0, wx.EXPAND)
    
    #statussizer = wx.BoxSizer(wx.HORIZONTAL)
    
    statuslabel = wx.StaticText(self, -1, self.t("appointmentstatuslabel") + ":")
    statuslabel.SetFont(font)
    searchsizer.Add(statuslabel, 0, wx.ALIGN_LEFT)
    
    statuschoice = wx.Choice(self, -1, choices=(self.t("appointmentnotarrivedlabel"), self.t("appointmentwaitinglabel"), self.t("appointmentwithvetlabel"), self.t("appointmentdonelabel"), self.t("stayinglabel")))
    statuschoice.Bind(wx.EVT_CHOICE, self.StatusChanged)
    
    if self.appointmentdata.staying > 0:
      
      statuschoice.SetSelection(4)
      
    elif self.appointmentdata.done == 1:
      
      statuschoice.SetSelection(3)
      
    elif self.appointmentdata.withvet == 1:
      
      statuschoice.SetSelection(2)
      
    elif self.appointmentdata.arrived == 1:
      
      statuschoice.SetSelection(1)
    else:
      
      statuschoice.SetSelection(0)
    
    searchsizer.Add(statuschoice, 0, wx.ALIGN_LEFT)
    
    #searchsizer.Add(statussizer, 0, wx.EXPAND)
    
    searchspacer = wx.StaticText(self, -1, "", size=(-1,20))
    searchsizer.Add(searchspacer, 0, wx.EXPAND)
    
    #submitbitmap = wx.Bitmap("icons/submit.png")
    appointmentsubmitbutton = wx.Button(self, -1, self.t("submitlabel"))
    appointmentsubmitbutton.SetBackgroundColour("green")
    appointmentsubmitbutton.Bind(wx.EVT_BUTTON, self.Submit)
    appointmentsubmitbutton.SetToolTipString(self.t("appointmentsubmittooltip"))
    searchsizer.Add(appointmentsubmitbutton, 0, wx.ALIGN_CENTER_HORIZONTAL)
    
    searchspacer1 = wx.StaticText(self, -1, "")
    searchsizer.Add(searchspacer1, 1, wx.EXPAND)
    
    #Right hand pane
    
    date = self.appointmententry.GetValue()
    date = miscmethods.GetDateFromWXDate(date)
    date = miscmethods.FormatDate(date, self.appointmentdata.localsettings)
    
    appointmentslistboxlabeltext = self.t("appointmentappointmentsforlabel") + " "  + str(date)
    
    self.appointmentslistboxlabel = wx.StaticText(self, -1, appointmentslistboxlabeltext)
    self.appointmentslistboxlabel.SetFont(font)
    
    self.appointmentslistbox = customwidgets.DayPlannerListbox(self, appointmentdata.localsettings, date, 10)
    self.appointmentslistbox.SetToolTipString(self.t("appointmentsummarylistboxtooltip"))
    self.appointmentslistbox.Bind(wx.EVT_LISTBOX_DCLICK, self.GetTime)
    
    appointmentslistboxsizer = wx.BoxSizer(wx.VERTICAL)
    
    appointmentslistboxsizer.Add(self.appointmentslistboxlabel, 0, wx.EXPAND)
    appointmentslistboxsizer.Add(self.appointmentslistbox, 1, wx.EXPAND)
    
    self.appointmentlistboxtotal = wx.StaticText(self, -1, self.t("totallabel") + ": 0")
    appointmentslistboxsizer.Add(self.appointmentlistboxtotal, 0, wx.ALIGN_RIGHT)
    
    mainsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    mainsizer.Add(searchsizer, 1, wx.EXPAND)
    
    spacer = wx.StaticText(self, -1, "", size=(50,-1))
    mainsizer.Add(spacer, 0, wx.EXPAND)
    
    mainsizer.Add(appointmentslistboxsizer, 2, wx.EXPAND)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    closebuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    bookbitmap = wx.Bitmap("icons/diary.png")
    creatediarynotebutton = wx.BitmapButton(self, -1, bookbitmap)
    creatediarynotebutton.SetToolTipString(self.t("createassociateddiarynotetooltip"))
    creatediarynotebutton.Bind(wx.EVT_BUTTON, self.CreateDiaryNote)
    
    if self.appointmentdata.ID == False  or self.appointmentdata.localsettings.addtodiary == 0:
      
      creatediarynotebutton.Disable()
    
    closebuttonsizer.Add(creatediarynotebutton, 0, wx.EXPAND)
    
    editownerbitmap = wx.Bitmap("icons/editclient.png")
    editownerbutton = wx.BitmapButton(self, -1, editownerbitmap)
    editownerbutton.SetForegroundColour("blue")
    editownerbutton.SetToolTipString(self.t("appointmenteditownerbutton", 1))
    editownerbutton.Bind(wx.EVT_BUTTON, self.OpenClientRecord)
    closebuttonsizer.Add(editownerbutton, 0, wx.EXPAND)
    
    if self.appointmentdata.localsettings.editclients == 0:
      editownerbutton.Disable()
    
    editownerbitmap = wx.Bitmap("icons/editanimal.png")
    editanimalbutton = wx.BitmapButton(self, -1, editownerbitmap)
    editanimalbutton.SetForegroundColour("blue")
    editanimalbutton.SetToolTipString(self.t("appointmenteditanimalbutton", 1))
    editanimalbutton.Bind(wx.EVT_BUTTON, self.OpenAnimalRecord)
    closebuttonsizer.Add(editanimalbutton, 0, wx.EXPAND)
    
    if self.appointmentdata.localsettings.editanimals == 0:
      editanimalbutton.Disable()
    
    if self.appointmentdata.localsettings.vetform == 1:
      
      vetformbitmap = wx.Bitmap("icons/vetform.png")
      vetformbutton = wx.BitmapButton(self, -1, vetformbitmap)
      vetformbutton.Bind(wx.EVT_BUTTON, self.VetForm)
      #vetformbutton.SetBackgroundColour("green")
      vetformbutton.SetToolTipString(self.t("vetformpagetitle"))
      
      if self.appointmentdata.ID == False:
        
        vetformbutton.Disable()
      
      closebuttonsizer.Add(vetformbutton, 0, wx.EXPAND)
    
    deletebitmap = wx.Bitmap("icons/delete.png")
    deletebutton = wx.BitmapButton(self, -1, deletebitmap)
    deletebutton.SetToolTipString(self.t("appointmentdeletetooltip"))
    deletebutton.Bind(wx.EVT_BUTTON, self.Delete)
    closebuttonsizer.Add(deletebutton, 0, wx.EXPAND)
    
    if self.appointmentdata.localsettings.deleteappointments == 0:
      deletebutton.Disable()
    
    closebuttonsizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
    
    refreshbitmap = wx.Bitmap("icons/refresh.png")
    refreshappointmentsbutton = wx.BitmapButton(self, -1, refreshbitmap)
    refreshappointmentsbutton.Bind(wx.EVT_BUTTON, self.RefreshAppointment)
    refreshappointmentsbutton.SetToolTipString(self.t("appointmentrefreshtooltip"))
    closebuttonsizer.Add(refreshappointmentsbutton, 0, wx.EXPAND)
    
    topsizer.Add(wx.StaticText(self, -1, "", size=(-1,10)), 0, wx.EXPAND)
    
    topsizer.Add(closebuttonsizer, 0, wx.EXPAND)
    topsizer.Add(mainsizer, 1, wx.EXPAND)
    
    self.SetSizer(topsizer)
    
    self.appointmentslistboxsizer = appointmentslistboxsizer
    self.statuschoice = statuschoice
    
    if self.appointmentdata.operation == 1:
      self.opcheckbox.SetValue(True)
      self.SwitchToOps()

    self.RefreshAppointment()
    
    #self.appointmententry.Bind(wx.EVT_CHAR, self.DateChangeEvent)
  
  def DateChangeEvent(self, ID):
    
    self.appointmententry.ButtonPressed(ID)
    
    self.RefreshAppointment()
  
  def ChooseAppointmentReason(self, ID):
    
    dialog = wx.Dialog(self, -1, self.t("lookupsreasonpagetitle"))
    
    dialogsizer = wx.BoxSizer(wx.VERTICAL)
    
    panel = wx.Panel(dialog)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    listbox = wx.ListBox(panel)
    listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.UpdateReason)
    listbox.SetToolTipString(self.t("doubleclicktoselecttooltip"))
    topsizer.Add(listbox, 1, wx.EXPAND)
    
    reasons = []
    
    action = "SELECT ReasonName FROM reason ORDER BY ReasonName"
    results = db.SendSQL(action, self.appointmentdata.localsettings.dbconnection)
    
    for a in results:
      
      if reasons.__contains__(a[0]) == False:
        
        reasons.append(a[0])
        listbox.Append(a[0])
    
    panel.reasons = reasons
    panel.listbox = listbox
    
    panel.SetSizer(topsizer)
    
    dialogsizer.Add(panel, 1, wx.EXPAND)
    
    dialog.SetSizer(dialogsizer)
    
    dialog.SetSize((300,200))
    
    dialog.ShowModal()
  
  def UpdateReason(self, ID):
    
    panel = ID.GetEventObject().GetParent()
    
    listboxid = panel.listbox.GetSelection()
    
    reasonname = panel.reasons[listboxid]
    
    self.reasonentry.SetValue(reasonname)
    
    panel.GetParent().Close()
  
  def VetForm(self, ID):
    
    vetform = vetmethods.VetForm(self.notebook, self.appointmentdata, self.appointmentdata.localsettings, self)
    
    self.notebook.AddPage(vetform)
  
  def CreateDiaryNote(self, ID=False):
    
    title = self.t("appointmentappointmentforlabel") + " " + self.appointmentdata.animaldata.name + " " + self.appointmentdata.clientdata.surname + " (" + self.appointmentdata.animaldata.species + ")"
    
    diarynotepanel = diarymethods.DiaryNotePanel(self.notebook, self.appointmentdata.localsettings, 3, self.appointmentdata.ID, title)
    self.notebook.AddPage(diarynotepanel)
  
  def UseVetComboBox(self, ID=False):
    
    parent = ID.GetEventObject()
    
    if parent.GetValue() == "Vet":
      parent.SetValue("")
    
    ID.Skip()
  
  def RefreshTotal(self, ID=False):
    
    date = self.appointmententry.GetValue()
    sqldate = miscmethods.GetSQLDateFromWXDate(date)
    
    if self.opcheckbox.GetValue() == True:
      operation = 1
    else:
      operation = 0
    
    action = "SELECT ID FROM appointment WHERE appointment.Date = \"" + sqldate + "\" AND appointment.Operation = " + str(operation)
    results = db.SendSQL(action, self.appointmentdata.localsettings.dbconnection)
    
    
    total = len(results)
    
    self.appointmentlistboxtotal.SetLabel(self.t("totallabel") + ": " + str(total))
    
    self.appointmentslistboxsizer.Layout()
  
  def SwitchToOps(self, ID=False):
    
    isop = self.opcheckbox.GetValue()
    date = self.appointmententry.GetValue()
    
    weekday = date.GetWeekDay()
    weekday = miscmethods.GetDayNameFromID(weekday, self.appointmentdata.localsettings)
    sqldate = miscmethods.GetSQLDateFromWXDate(date)
    datestring = miscmethods.GetDateFromWXDate(date)
    datestring = miscmethods.FormatDate(datestring, self.appointmentdata.localsettings)
    
    
    
    if isop == True:
      self.appointmenttimeentry.SetValue("09:00")
      self.appointmenttimeentry.Disable()
      
    else:
      self.appointmenttimeentry.Enable()
    
    self.RefreshAppointment()
    self.RefreshTotal()
  
  def Submit(self, ID):
    
    if self.opcheckbox.GetValue() == True:
      self.SubmitOperation(ID)
    else:
      self.SubmitAppointment(ID)
  
  def SubmitOperation(self, ID):
    
    
    self.appointmentdata.date = miscmethods.GetSQLDateFromWXDate(self.appointmententry.GetValue())
    self.appointmentdata.time = self.appointmentdata.localsettings.operationtime
    self.appointmentdata.vet = self.vetcombobox.GetValue()
    
    self.appointmentdata.reason = self.reasonentry.GetValue()
    self.appointmentdata.operation = 1
    
    choice = self.statuschoice.GetSelection()
    
    if choice == 0:
      self.appointmentdata.arrived = 0
      self.appointmentdata.withvet = 0
      self.appointmentdata.done = 0
      self.appointmentdata.staying = 0
    elif choice == 1:
      self.appointmentdata.arrived = 1
      self.appointmentdata.withvet = 0
      self.appointmentdata.done = 0
      self.appointmentdata.staying = 0
    elif choice == 2:
      self.appointmentdata.arrived = 1
      self.appointmentdata.withvet = 1
      self.appointmentdata.done = 0
      self.appointmentdata.staying = 0
    elif choice == 3:
      self.appointmentdata.arrived = 1
      self.appointmentdata.withvet = 0
      self.appointmentdata.done = 1
      self.appointmentdata.staying = 0
    elif choice == 4:
      self.appointmentdata.arrived = 1
      self.appointmentdata.withvet = 1
      self.appointmentdata.done = 0
      self.appointmentdata.staying = self.kennelid
    
    self.appointmentdata.Submit()
    
    try:
      
      self.kennelspanel.RefreshListboxes()
      
    except:
      
      try:
        
        self.parent.animalappointmentslistbox.RefreshList()
        
      except:
        
        try:
          
          viewappointments.UpdateViewAppointments(self.viewappointmentspanel, True)
          
        except:
          
          pass
    
    self.Close()
  
  def SubmitAppointment(self, ID):
    
    time = self.appointmenttimeentry.GetValue()
    
    success = False
    
    if miscmethods.ValidateTime(time) == True:
      if miscmethods.GetMinutesFromTime(time) < miscmethods.GetMinutesFromTime(self.appointmentdata.localsettings.opento) + 1:
        if miscmethods.GetMinutesFromTime(time) > miscmethods.GetMinutesFromTime(self.appointmentdata.localsettings.openfrom) - 1:
          
          time = time[:2] + ":" + time[3:5]
          success = True
        else:
          failurereason = self.t("appointmenttimetooearlymessage")
      else:
        failurereason = self.t("appointmenttimetoolatemessage")
    else:
      failurereason = self.t("appointmentinvalidtimemessage")
    
    if success == True:
      self.appointmentdata.date = miscmethods.GetSQLDateFromWXDate(self.appointmententry.GetValue())
      self.appointmentdata.time = time
      self.appointmentdata.reason = self.reasonentry.GetValue()
      self.appointmentdata.operation = 0
      if self.vetcombobox.GetValue() == "Vet":
        self.appointmentdata.vet = "None"
      else:
        self.appointmentdata.vet = self.vetcombobox.GetValue()
      
      choice = self.statuschoice.GetSelection()
      
      self.appointmentdata.arrived = 0
      self.appointmentdata.withvet = 0
      self.appointmentdata.done = 0
      self.appointmentdata.staying = 0

      if choice != 0:
        self.appointmentdata.arrived = 1

      if choice == 2:
        self.appointmentdata.withvet = 1
      elif choice == 3:
        self.appointmentdata.done = 1
      elif choice == 4:
        self.appointmentdata.withvet = 1
        self.appointmentdata.staying = self.kennelid
      
      self.appointmentdata.Submit()
      
      try:
        self.kennelspanel.RefreshListboxes()
      except:
        try:
          self.parent.animalappointmentslistbox.RefreshList()
        except:
          try:
            viewappointments.UpdateViewAppointments(self.viewappointmentspanel, True)
          except:
            pass

      self.Close()
      
    else:
      miscmethods.ShowMessage(failurereason)
  
  def RefreshAppointment(self, ID=False):
    
    localsettings = self.appointmentdata.localsettings
    
    try:
      
      date = self.appointmententry.GetValue()
      weekday = date.GetWeekDay()
      weekday = miscmethods.GetDayNameFromID(weekday, self.appointmentdata.localsettings)
      sqldate = miscmethods.GetSQLDateFromWXDate(date)
      datestring = miscmethods.GetDateFromWXDate(date)
      datestring = miscmethods.FormatDate(datestring, self.appointmentdata.localsettings)
      
      isop = self.opcheckbox.GetValue()
      
      if isop == True:
        appointmentslistboxlabeltext = self.t("appointmentoperationsforlabel") + " " + weekday + " " + str(datestring)
      else:
        appointmentslistboxlabeltext = self.t("appointmentappointmentsforlabel") + " " + weekday + " " + str(datestring)
      self.appointmentslistboxlabel.SetLabel(appointmentslistboxlabeltext)
      
      self.appointmentslistbox.sqldate = sqldate
      
      self.appointmentslistbox.RefreshList()
      
      self.RefreshTotal()
    
    except:
      
      pass
  
  def GetTime(self,ID):
    
    listboxid = self.appointmentslistbox.GetSelection()
    
    action = "SELECT * FROM settings"
    results = db.SendSQL(action, self.appointmentdata.localsettings.dbconnection)
    
    
    openfromraw = results[0][2]
    openfromtime = ( int(str(openfromraw)[:2]) * 60 ) + int(str(openfromraw)[3:5])
    
    appointmenttime = openfromtime + (listboxid * 10)
    appointmenttime = miscmethods.GetTimeFromMinutes(appointmenttime)[:5]
    
    self.appointmenttimeentry.SetValue(appointmenttime)
  
  def Delete(self, ID):
    
    if miscmethods.ConfirmMessage("Are you sure that you want to delete this appointment?") == True:
      
      action = "DELETE FROM appointment WHERE ID = " + str(self.appointmentdata.ID)
      db.SendSQL(action, self.appointmentdata.localsettings.dbconnection)
      
      
      self.Close(self)
  
  def OpenAnimalRecord(self, ID):
    
    #notebook = ID.GetEventObject().GetGrandParent().GetParent()
    
    animaldata = self.appointmentdata.animaldata
    
    animalpanel = animalmethods.AnimalPanel(self.notebook, animaldata)
    
    self.notebook.AddPage(animalpanel)
  
  def OpenClientRecord(self, ID):
    
    #notebook = ID.GetEventObject().GetGrandParent().GetParent()
    
    clientdata = self.appointmentdata.clientdata
    
    clientpanel = clientmethods.ClientPanel(self.notebook, clientdata)
    
    self.notebook.AddPage(clientpanel)
  
  def Close(self, ID=False):
    
    if self.viewappointmentspanel != False:
      
      try:
        
        self.viewappointmentspanel.RefreshLists()
        
      except:
        
        pass
    
    self.notebook.ClosePage(self.notebook.activepage)
    #miscmethods.ClosePanel(self)
  
  def StatusChanged(self, ID):
    
    choice = ID.GetEventObject()
    
    selectionid = choice.GetSelection()
    
    if selectionid == 4:
      
      self.ChooseKennelBlockDialog()
  
  def ChooseKennelBlockDialog(self):
    
    dialog = wx.Dialog(self, -1, self.t("kennelblocktitlelabel"))
    
    dialogsizer = wx.BoxSizer(wx.VERTICAL)
    
    panel = wx.Panel(dialog)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    action = "SELECT ID, Name FROM kennelblock ORDER BY Name"
    kennelblockdata = db.SendSQL(action, self.appointmentdata.localsettings.dbconnection)
    
    listbox = wx.ListBox(panel, -1)
    listbox.Bind(wx.EVT_LISTBOX, self.ChooseKennelDialog)
    
    for a in kennelblockdata:
      
      listbox.Append(a[1])
    
    topsizer.Add(listbox, 1, wx.EXPAND)
    
    panel.SetSizer(topsizer)
    
    panel.listbox = listbox
    panel.kennelblockdata = kennelblockdata
    
    dialogsizer.Add(panel, 1, wx.EXPAND)
    
    dialog.SetSizer(dialogsizer)
    
    dialog.Fit()
    
    dialog.ShowModal()
  
  def ChooseKennelDialog(self, ID):
    
    parentpanel = ID.GetEventObject().GetParent()
    
    parentpanel.listbox.Unbind(wx.EVT_LISTBOX)
    
    listboxid = parentpanel.listbox.GetSelection()
    
    kennelblockid = parentpanel.kennelblockdata[listboxid][0]
    
    dialog = wx.Dialog(parentpanel, -1, self.t("kennelstitlelabel"))
    
    dialogsizer = wx.BoxSizer(wx.VERTICAL)
    
    panel = wx.Panel(dialog)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    action = "SELECT ID, Name FROM kennel WHERE KennelBlockID = " + str(kennelblockid) + " ORDER BY Name"
    kenneldata = db.SendSQL(action, self.appointmentdata.localsettings.dbconnection)
    
    action = "SELECT Staying FROM appointment WHERE Staying > 0"
    animaldata = db.SendSQL(action, self.appointmentdata.localsettings.dbconnection)
    
    listbox = wx.ListBox(panel, -1)
    listbox.Bind(wx.EVT_LISTBOX, self.KennelChosen)
    
    for a in kenneldata:
      
      kennelid = a[0]
      
      occupied = False
      
      for b in animaldata:
        
        if b[0] == kennelid:
          
          occupied = True
      
      if occupied == True:
        
        occupied = self.t("occupiedlabel")
        
      else:
        
        occupied = self.t("vacantlabel")
      
      listbox.Append(a[1] + " (" + occupied + ")")
    
    topsizer.Add(listbox, 1, wx.EXPAND)
    
    panel.SetSizer(topsizer)
    
    panel.parentpanel = parentpanel
    panel.kenneldata = kenneldata
    panel.listbox = listbox
    
    dialogsizer.Add(panel, 1, wx.EXPAND)
    
    dialog.SetSizer(dialogsizer)
    
    dialog.Fit()
    
    dialog.ShowModal()
    
    parentpanel.GetParent().Close()
  
  def KennelChosen(self, ID):
    
    parentpanel = ID.GetEventObject().GetParent()
    parentdialog = parentpanel.GetParent()
    
    grandparentpanel = parentpanel.parentpanel
    grandparentdialog = grandparentpanel.GetParent()
    
    listboxid = parentpanel.listbox.GetSelection()
    self.kennelid = parentpanel.kenneldata[listboxid][0]
    
    parentdialog.Close()

class BrowseAppointments(wx.Panel):
  
  def t(self, field):
    
    return  self.localsettings.t(field)
  
  def __init__(self, notebook, localsettings, popup=False):
    
    busy = wx.BusyCursor()
    
    self.localsettings = localsettings
    self.popup = popup
    
    if popup == False:
      
      self.pagetitle = self.t("browseappointmentspagetitle")
      self.pagetitle = miscmethods.GetPageTitle(notebook, self.pagetitle)
      self.pageimage = "icons/appointment.png"
    
    self.currentdate = datetime.date.today()
    
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
    
    monthlabel = wx.StaticText(monthpanel, -1, monthname + " " + self.currentdate.strftime("%Y"))
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
    
    self.RefreshCalendar()
    
    del busy
  
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
    
    self.monthlabel.SetLabel(monthname + " " + self.currentdate.strftime("%Y"))
    
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
    
    self.monthlabel.SetLabel(monthname + " " + self.currentdate.strftime("%Y"))
    
    self.monthsizer.Layout()
    
    self.RefreshCalendar()
  
  def OpenDay(self, ID):
    
    self.monthpanel.Hide()
    self.calendarpanel.Hide()
    self.calendarpanel.Destroy()
    self.calendarpanel = AppointmentsList(self, self.localsettings, self.currentdate)
    self.calendarsizer.Add(self.calendarpanel, 1, wx.EXPAND)
    self.calendarsizer.Layout()
  
  def BackToCalendar(self, ID):
    
    self.monthpanel.Show()
    self.calendarpanel.Hide()
    self.calendarpanel.Destroy()
    self.calendarpanel = Calendar(self, self.localsettings, self.currentdate.month, self.currentdate.year)
    self.calendarsizer.Add(self.calendarpanel, 1, wx.EXPAND)
    self.calendarsizer.Layout()

class AppointmentsList(wx.Panel):
  
  def t(self, field):
    
    return  self.localsettings.t(field)
  
  def __init__(self, parent, localsettings, date):
    
    self.parent = parent
    self.localsettings = localsettings
    self.date = date
    
    wx.Panel.__init__(self, parent)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    buttonssizer = wx.BoxSizer(wx.HORIZONTAL)
    
    upbitmap = wx.Bitmap("icons/uparrow.png")
    calendarbutton = wx.BitmapButton(self, -1, upbitmap)
    calendarbutton.SetToolTipString(self.t("backtocalendartooltip"))
    calendarbutton.Bind(wx.EVT_BUTTON, self.parent.BackToCalendar)
    buttonssizer.Add(calendarbutton, 0, wx.EXPAND)
    
    editanimalbitmap = wx.Bitmap("icons/editanimal.png")
    editanimalbutton = wx.BitmapButton(self, -1, editanimalbitmap)
    editanimalbutton.SetToolTipString(self.t("editanimaltooltip"))
    editanimalbutton.Bind(wx.EVT_BUTTON, self.EditAnimal)
    editanimalbutton.Disable()
    buttonssizer.Add(editanimalbutton, 0, wx.EXPAND)
    
    editclientbitmap = wx.Bitmap("icons/editclient.png")
    editclientbutton = wx.BitmapButton(self, -1, editclientbitmap)
    editclientbutton.SetToolTipString(self.t("viewappointmentseditclientbuttonlabel"))
    editclientbutton.Bind(wx.EVT_BUTTON, self.EditClient)
    editclientbutton.Disable()
    buttonssizer.Add(editclientbutton, 0, wx.EXPAND)
    
    refreshbitmap = wx.Bitmap("icons/refresh.png")
    refreshbutton = wx.BitmapButton(self, -1, refreshbitmap)
    refreshbutton.SetToolTipString(self.t("lookupsrefreshtooltip"))
    refreshbutton.Bind(wx.EVT_BUTTON, self.RefreshList)
    buttonssizer.Add(refreshbutton, 0, wx.EXPAND)
    
    buttonssizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
    
    weekday = miscmethods.GetWeekday(int(self.date.strftime("%w")), self.localsettings)
    
    datestring = weekday + u"\xa0" + miscmethods.FormatDate(self.date, self.localsettings)
    
    datelabel = wx.StaticText(self, -1, datestring)
    
    datelabel.SetForegroundColour("red")
    
    font = datelabel.GetFont()
    font.SetPointSize(font.GetPointSize() + 6)
    datelabel.SetFont(font)
    
    buttonssizer.Add(datelabel, 0, wx.EXPAND)
    
    buttonssizer.Add(wx.StaticText(self, -1, ""), 1, wx.EXPAND)
    
    
    printbuttonbitmap = wx.Bitmap("icons/printer.png")
    printbutton = wx.BitmapButton(self, -1, printbuttonbitmap)
    printbutton.Bind(wx.EVT_BUTTON, self.PrintAppointmentList)
    printbutton.SetToolTipString(self.t("printtooltip"))
    buttonssizer.Add(printbutton, 0, wx.EXPAND)
    
    topsizer.Add(buttonssizer, 0, wx.EXPAND)
    
    appointmentslist = AppointmentsListbox(self, self.localsettings, self.date, 10)
    appointmentslist.Bind(wx.EVT_LISTBOX_DCLICK, self.EditAppointment)
    appointmentslist.Bind(wx.EVT_LISTBOX, self.ItemSelected)
    appointmentslist.RefreshList()
    
    topsizer.Add(appointmentslist, 1, wx.EXPAND)
    
    self.appointmentslist = appointmentslist
    
    self.SetSizer(topsizer)
    
    self.appointmentslist = appointmentslist
    self.editanimalbutton = editanimalbutton
    self.editclientbutton = editclientbutton
  
  def PrintAppointmentList(self, ID):
    
    output = "<h1 align=center><u>" + self.t("appointmentsmenu") + " " + miscmethods.FormatDate(self.date, self.localsettings) + "</h1>"
    
    for a in self.appointmentslist.htmllist:
      
      time = str(a[1])[:-3]
      if len(time) == 4:
        time = "0" + time
      animalname = a[2] + " " + a[3]
      species = a[7]
      reason = a[4]
      asmref = a[8]
      
      output = output + "<table cellpadding=0 cellspacing=5 width=100%><tr><td valign=top nowrap><b>" + str(time) + "</b></td>"
      
      if asmref != "":
        
        output = output + "<td><font color=red><b>" + asmref + "</b></font></td>"
      
      output = output + "<td valign=top nowrap><font color=blue>" + animalname + "</font> (" + species + ")</td><td valign=top width=100%><font color=red>" + reason + "</font></td></tr></table>"
    
    formmethods.BuildForm(self.localsettings, output)
  
  def ItemSelected(self, ID):
    
    self.editclientbutton.Enable()
    self.editanimalbutton.Enable()
  
  def RefreshList(self, ID):
    
    self.appointmentslist.RefreshList()
    self.editclientbutton.Disable()
    self.editanimalbutton.Disable()
  
  def EditAppointment(self, ID):
    
    listboxid = self.appointmentslist.GetSelection()
    appointmentid = self.appointmentslist.htmllist[listboxid][0]
    
    appointmentdata = AppointmentSettings(self.localsettings, False, appointmentid)
    
    notebook = self.GetGrandParent()#.GetParent()
    
    appointmentpanel = AppointmentPanel(notebook, appointmentdata)
    notebook.AddPage(appointmentpanel)
  
  def EditAnimal(self, ID):
    
    listboxid = self.appointmentslist.GetSelection()
    animalid = self.appointmentslist.htmllist[listboxid][5]
    
    animaldata = animalmethods.AnimalSettings(self.localsettings, False, animalid)
    
    notebook = self.GetGrandParent()#.GetParent()
    
    animalpanel = animalmethods.AnimalPanel(notebook, animaldata)
    notebook.AddPage(animalpanel)
  
  def EditClient(self, ID):
    
    listboxid = self.appointmentslist.GetSelection()
    clientid = self.appointmentslist.htmllist[listboxid][6]
    
    clientdata = clientmethods.ClientSettings(self.localsettings, clientid)
    
    notebook = self.GetGrandParent()#.GetParent()
    
    clientpanel = clientmethods.ClientPanel(notebook, clientdata)
    notebook.AddPage(clientpanel)

class Calendar(wx.ScrolledWindow):
  
  def t(self, field):
    
    return  self.localsettings.t(field)
  
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
      
      gridsizer.Add(DayCell(self, self.localsettings, date, self.localsettings.dbconnection), 1, wx.EXPAND)
      
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
  
  def t(self, field):
    
    return  self.localsettings.t(field)
  
  def __init__(self, parent, localsettings, date, connection):
    
    self.localsettings = localsettings
    
    self.date = date
    
    self.parent = parent
    
    wx.Panel.__init__(self, parent, style=wx.SIMPLE_BORDER)
    
    if self.parent.parent.popup == True:
      
      self.Bind(wx.EVT_LEFT_DOWN, self.DateSelected)
      
    else:
      
      self.Bind(wx.EVT_LEFT_DOWN, self.DayCellSelected)
      self.Bind(wx.EVT_LEFT_DCLICK, self.parent.GetParent().OpenDay)
    
    self.topsizer = wx.BoxSizer(wx.VERTICAL)
    
    self.SetSizer(self.topsizer)
    
    self.RefreshCell(connection)
  
  def RefreshCell(self, connection):
    
    self.Hide()
    
    try:
      self.topsizer.Remove(self.daycellpanel)
      self.daycellpanel.Destroy()
    except:
      pass
    
    #daycellpanel = self
    
    if self.date == datetime.date.today():
      
      self.SetBackgroundColour("#CBFFD5")
      
    elif self.date.strftime("%w") == "0" or self.date.strftime("%w") == "6":
      
      self.SetBackgroundColour("#E8E8E8")
      
    else:
      
      self.SetBackgroundColour("white")
    
    label = wx.StaticText(self, -1, str(self.date.day))
    
    if self.parent.parent.popup == True:
      
      label.Bind(wx.EVT_LEFT_DOWN, self.DateSelected)
      
    else:
      
      label.Bind(wx.EVT_LEFT_DOWN, self.DayCellSelected)
      label.Bind(wx.EVT_LEFT_DCLICK, self.parent.GetParent().OpenDay)
    
    label.SetForegroundColour("blue")
    font = label.GetFont()
    font.SetPointSize(font.GetPointSize() + 2)
    label.SetFont(font)
    self.topsizer.Add(label, 1, wx.ALIGN_CENTER_HORIZONTAL)
    
    
    action = "SELECT Operation FROM appointment WHERE Date = \"" + miscmethods.GetSQLDateFromDate(self.date) + "\""
    results = db.SendSQL(action, self.localsettings.dbconnection)
    
    appointments = 0
    operations = 0
    
    for a in results:
      
      if a[0] == 0:
        
        appointments = appointments + 1
        
      else:
        
        operations = operations + 1
    
    appointmentslabel = wx.StaticText(self, -1, str(appointments) + " " + self.t("appointmentsmenu").lower().replace("&", "") + "\n" + str(operations) + " " + self.t("operationslabel").lower())
    
    if self.parent.parent.popup == True:
      
      appointmentslabel.Bind(wx.EVT_LEFT_DOWN, self.DateSelected)
      
    else:
      
      appointmentslabel.Bind(wx.EVT_LEFT_DOWN, self.DayCellSelected)
      appointmentslabel.Bind(wx.EVT_LEFT_DCLICK, self.parent.GetParent().OpenDay)
    
    self.topsizer.Add(appointmentslabel, 1, wx.ALIGN_CENTER)
    
    self.Show()
  
  def DayCellSelected(self, ID):
    
    self.parent.GetParent().currentdate = self.date
    self.parent.GetParent().selectedcell = self
  
  def DateSelected(self, ID):
    
    date = self.date
    
    date = miscmethods.GetWXDateFromDate(date)
    
    self.parent.parent.GetGrandParent().SetValue(date)
    
    self.parent.parent.GetParent().Close()

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

class AppointmentsListbox(wx.HtmlListBox):
  
  def __init__(self, parent, localsettings, date, step=10):
    wx.HtmlListBox.__init__(self, parent, -1)
    
    self.htmllist = []
    self.localsettings = localsettings
    self.date = date
    self.parent = parent
    self.step = step
    self.SetItemCount(0)
  
  def OnGetItem(self, n):
    
    if len(self.htmllist) > 0:
      
      time = str(self.htmllist[n][1])[:-3]
      if len(time) == 4:
        time = "0" + time
      animalname = self.htmllist[n][2] + " " + self.htmllist[n][3]
      species = self.htmllist[n][7]
      reason = self.htmllist[n][4]
      asmref = self.htmllist[n][8]
      
      output = "<table cellpadding=0 cellspacing=5 width=100% border=0><tr><td valign=middle nowrap><b>" + str(time) + "</b></td>"
      
      if asmref != "":
        
        output = output + "<td valign=middle><img src=icons/asm.png></td>"
      
      output = output + "<td valign=middle nowrap><font color=blue>" + animalname + "</font> (" + species + ")</td><td valign=middle width=100%><font color=red>" + reason + "</font></td></tr></table>"
    
    return output
  
  def RefreshList(self, ID=False):
    
    self.Hide()
    
    action = "SELECT appointment.ID, appointment.Time, animal.Name, client.ClientSurname, appointment.AppointmentReason, appointment.AnimalID, animal.OwnerID, animal.Species, animal.ASMRef FROM appointment INNER JOIN animal ON appointment.AnimalID = animal.ID INNER JOIN client ON animal.OwnerID = client.ID WHERE appointment.Date = \"" + str(self.date) + "\" ORDER BY appointment.Time"
    
    results = db.SendSQL(action, self.localsettings.dbconnection)
    
    self.htmllist = []
    
    for a in results:
      self.htmllist.append(a)
    
    self.SetItemCount(len(self.htmllist))
    self.Refresh()
    self.SetSelection(-1)
    
    self.Show()

class AppointmentDateCtrl(customwidgets.DateCtrl):
  
  def __init__(self, parent, localsettings):
    
    self.parent = parent
    customwidgets.DateCtrl.__init__(self, parent, localsettings, True)
  
  def ButtonPressed(self, ID):
    
    customwidgets.DateCtrl.ButtonPressed(self, ID)
    
    wx.CallAfter(self.parent.RefreshAppointment)
  
  def PopupCalendar(self, ID):
    
    customwidgets.DateCtrl.PopupCalendar(self, ID)
    
    self.parent.RefreshAppointment()
