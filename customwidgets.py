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
import datetime
import clientmethods
import sys
import appointmentmethods
import wx.lib.mixins.listctrl as listmix

red = wx.Colour(255, 163, 163)
green = wx.Colour(144, 255, 172)
yellow = wx.Colour(252, 255, 0)

DETATCH_TAB = 6001

class StaffSummaryListbox(wx.HtmlListBox):
  
  def __init__(self, parent, localsettings):
    
    wx.HtmlListBox.__init__(self, parent, -1)
    
    self.htmllist = []
    self.localsettings = localsettings
    self.parent = parent
    self.SetItemCount(0)
  
  def OnGetItem(self, n):
    
    vet = self.htmllist[n][1]
    timeon = self.htmllist[n][3]
    timeoff = self.htmllist[n][4]
    if self.htmllist[n][5] == 0:
      role = "consulting"
    else:
      role = "operating"
    
    output = "<h2>" + vet + " <font size=2>(" + role + ")</font></h2><p>From " + timeon + " to " + timeoff + "</p>"
    
    return output
  
  def RefreshList(self, ID=False):
    
    self.Hide()
    
    date = self.parent.dateentry.GetValue()
    date = miscmethods.GetSQLDateFromWXDate(date)
    
    action = "SELECT * FROM staff WHERE Date = \"" + date + "\" ORDER BY TimeOn"
    results = db.SendSQL(action, self.localsettings.dbconnection)
    
    self.htmllist = []
    
    for a in results:
      self.htmllist.append(a)
    
    self.SetItemCount(len(self.htmllist))
    self.Refresh()
    self.SetSelection(-1)
    
    self.Show()

class DayPlannerListbox(wx.HtmlListBox):
  
  def __init__(self, parent, localsettings, date, step):
    
    wx.HtmlListBox.__init__(self, parent, -1)
    self.Bind(wx.EVT_RIGHT_DOWN, self.ShowVets)
    
    self.htmllist = []
    self.localsettings = localsettings
    self.parent = parent
    self.SetItemCount(0)
    self.step = step
    
    openfrom = self.localsettings.openfrom
    self.openfromtime = miscmethods.GetMinutesFromTime(openfrom)
    
    opento = self.localsettings.opento
    self.opentotime = miscmethods.GetMinutesFromTime(opento)
    
    timeslots = []
    
    for a in range(self.openfromtime, self.opentotime + step, step):
      
      timeslots.append(a)
    
    self.date = date
    
    self.timeslots = timeslots
  
  def ShowVets(self, ID):
    
    listboxid = self.GetSelection()
    
    if listboxid > -1:
      
      app_type = self.parent.app_type_combo.GetSelection()
      
      if app_type == -1:
        app_type = 0
      
      timeslot = self.timeslots[listboxid]
      
      timefrom = timeslot
      timeto = timeslot + self.step
      
      action = "SELECT Name FROM staff WHERE Date = \"" + self.sqldate + "\" AND TimeOn < \"" + miscmethods.GetTimeFromMinutes(timefrom) + ":00" + "\" AND TimeOff > \"" + miscmethods.GetTimeFromMinutes(timefrom) + ":00" + "\" AND Operating = " + str(app_type) + " ORDER BY Name"
      results = db.SendSQL(action, self.localsettings.dbconnection)
      
      vets = ""
      
      for a in results:
        
        if vets != "":
          
          vets = vets + "<br>"
        
        vets = vets + a[0]
      
      if vets == "":
        
        vets = self.localsettings.t("nonelabel")
      
      dialog = wx.Dialog(self, -1, self.localsettings.t("viewappointmentsvetsonlabel"))
      
      dialogsizer = wx.BoxSizer(wx.VERTICAL)
      
      panel = wx.Panel(dialog)
      
      topsizer = wx.BoxSizer(wx.VERTICAL)
      
      summarywindow = wx.html.HtmlWindow(panel)
      topsizer.Add(summarywindow, 1, wx.EXPAND)
      
      summarywindow.SetPage(vets)
      
      panel.SetSizer(topsizer)
      
      dialogsizer.Add(panel, 1, wx.EXPAND)
      
      dialog.SetSizer(dialogsizer)
      
      dialog.SetSize((200,100))
      
      dialog.ShowModal()
      
    else:
      
      pass
    
    
  
  def OnGetItem(self, n):
    
    timeslot = self.timeslots[n]
    
    output = "<table cellspacing=0 cellpadding=0 border=0><tr><td valign=top nowrap><font size=4><b>" + miscmethods.GetTimeFromMinutes(timeslot) + "</b></font>&nbsp;</td><td valign=top>"
    
    appointmentinfo = ""
    
    for a in self.htmllist:
      
      time = a[0]
      
      time = miscmethods.GetMinutesFromTime(str(time))
      
      if time >= timeslot and time < timeslot + self.step:
        
        animal = a[1] + " " + a[2]
        
        reason = a[3]
        
        appointmentinfo = appointmentinfo + "<table cellspacing=0 cellpadding=0><tr><td valign=top>" + miscmethods.GetTimeFromMinutes(time) + "&nbsp;</td><td valign=top><font color=blue>" + animal + "</font>&nbsp;</td><td valign=top>&nbsp;-&nbsp;<font color=red>" + reason + "</font></td></tr></table>"
    
    if appointmentinfo == "":
      
      output = output + "<font color=green><b>" + self.localsettings.t("nonelabel") + "</b></font>"
      
    else:
      
      output = output + appointmentinfo
    
    output = output + "</td></tr></table>"
    
    return output
  
  def RefreshList(self, ID=False):
    
    busy = wx.BusyCursor()
    
    self.Hide()
    
    app_type = self.parent.app_type_combo.GetSelection()
    
    if app_type == -1:
      app_type = 0
      
    sqldate = self.sqldate
    
    action = "SELECT appointment.Time, animal.Name, client.ClientSurname, appointment.AppointmentReason FROM appointment INNER JOIN animal ON appointment.AnimalID = animal.ID INNER JOIN client ON appointment.OwnerID = client.ID WHERE appointment.Date = \"" + self.sqldate + "\" AND appointment.Operation = " + str(app_type) + " ORDER BY appointment.Time"
    results = db.SendSQL(action, self.localsettings.dbconnection)
    
    self.htmllist = results
    
    self.SetItemCount(len(self.timeslots))
    
    self.Show()
    
    del busy

class AppointmentListbox(wx.Panel, listmix.ColumnSorterMixin):
  
  def t(self, key, idx = 0):
    return self.localsettings.t(key,idx)
  
  def __init__(self, parent, localsettings, index):
    
    wx.Panel.__init__(self, parent)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    self.listctrl = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
    listmix.ColumnSorterMixin.__init__(self, 4)
    topsizer.Add(self.listctrl, 1, wx.EXPAND)
    
    imagelist = wx.ImageList(20, 20)
    asmicon = imagelist.Add(wx.Bitmap("icons/asm.png"))
    asmicon = imagelist.Add(wx.Bitmap("icons/editanimal.png"))
    self.listctrl.AssignImageList(imagelist, wx.IMAGE_LIST_SMALL)
    self.listctrl.Bind(wx.EVT_RIGHT_DOWN, parent.AppointmentMenuPopup)
    #self.listctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, parent.EditAppointment)
    self.listctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, parent.AppointmentSelected)
    
    self.SetSizer(topsizer)
    
    self.htmllist = []
    #self.listctrl.htmllist = self.htmllist
    self.localsettings = localsettings
    self.parent = parent
    self.index = index
    self.time = datetime.datetime.today().time().strftime("%X")[:5]
  
  def GetListCtrl(self):# Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    
          return self.listctrl
  
  def GetSelection(self):
    
    selection = -1
    
    for a in range(0, len(self.htmllist)):
      
      if self.listctrl.IsSelected(a) == True:
        
        selection = a
    
    return selection
  
  def ScrollToLine(self, lineno):
    
    self.listctrl.SetScrollPos(wx.VERTICAL, lineno)
  
  def SetSelection(self, selection):
    
    self.listctrl.Unbind(wx.EVT_LIST_ITEM_SELECTED)
    
    if selection == -1:
      
      for a in range(0, len(self.htmllist)):
        
        self.listctrl.Select(a, 0)
      
    else:
      
      self.listctrl.Select(selection)
    
    self.listctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.parent.AppointmentSelected)
  
  def RefreshList(self, ID=False):
  
    self.itemDataMap = {}
    
    self.listctrl.ClearAll()
    
    if self.index == 3:
      
      self.listctrl.InsertColumn(0, self.t("timelabel"))
      self.listctrl.InsertColumn(1, self.t("animalownerlabel"))
      self.listctrl.InsertColumn(2, self.t("animallabel"))
      self.listctrl.InsertColumn(3, self.t("clientbalancelabel"))
      
    elif self.index == 1:
      
      self.listctrl.InsertColumn(0, self.t("timelabel"))
      self.listctrl.InsertColumn(1, self.t("appointmentwaitinglabel"))
      self.listctrl.InsertColumn(2, self.t("animalownerlabel"))
      self.listctrl.InsertColumn(3, self.t("animallabel"))
      self.listctrl.InsertColumn(4, self.t("vetlabel"))
      
    else:
      
      self.listctrl.InsertColumn(0, self.t("timelabel"))
      self.listctrl.InsertColumn(1, self.t("animalownerlabel"))
      self.listctrl.InsertColumn(2, self.t("animallabel"))
      self.listctrl.InsertColumn(3, self.t("vetlabel"))
    
    count = 0
    
    for a in self.htmllist:
      
      time = str(a[1])
      
      if len(str(time)) == 7:
        
        time = "0" + time[:4]
        
      else:
        
        time = time[:5]
      
      animalname = a[3]
      ownersurname = a[4]
      species = a[7]
      
      animal = animalname + " (" + species + ")"
      
      vet = a[14]
      
      asmref = a[16]
      
      currencyunit = self.t("currency")
      
      if currencyunit == "&pound;":
        
        currencyunit = u"£"
      
      if self.index == 3:
        
        balance = a[-1]
        
        balancestring = currencyunit + balance
        
        self.itemDataMap[a[0]] = ( time, ownersurname, animal, balance )
        self.listctrl.InsertStringItem(count, time)
        self.listctrl.SetStringItem(count, 1, ownersurname)
        self.listctrl.SetStringItem(count, 2, animal)
        self.listctrl.SetStringItem(count, 3, balancestring)
        
        if float(balance) < 0:
          
          self.listctrl.SetItemBackgroundColour(count, red)
          
        else:
          
          self.listctrl.SetItemBackgroundColour(count, green)
        
      elif self.index == 1:
        
        currenttime = datetime.datetime.today().strftime("%H:%M")
        
        hours = str(currenttime).split(":")[0]
        minutes = str(currenttime).split(":")[1]
        
        totalcurrentminutes = ( int(hours) * 60 ) + int(minutes)
        
        arrivaltimedelta = a[17]
        
        if arrivaltimedelta != None:
          
          hours = str(arrivaltimedelta).split(":")[0]
          minutes = str(arrivaltimedelta).split(":")[1]
          
          totalarrivalminutes = ( int(hours) * 60 ) + int(minutes)
          
          waiting = str(totalcurrentminutes - totalarrivalminutes) + " " + self.t("minslabel")
          
          appointmenttime = time
          
          hours = str(appointmenttime).split(":")[0]
          minutes = str(appointmenttime).split(":")[1]
          
          totalappointmentminutes = ( int(hours) * 60 ) + int(minutes)
          
          late = False
          
          if totalarrivalminutes - totalappointmentminutes > 0:
            
            waiting = waiting + " (" + self.t("latelabel").lower() + ")"
            
            late = True
          
        else:
          
          waiting = self.t("errorlabel")
        
        self.itemDataMap[a[0]] = ( time, waiting, ownersurname, animal, vet )
        self.listctrl.InsertStringItem(count, time)
        self.listctrl.SetStringItem(count, 1, waiting)
        self.listctrl.SetStringItem(count, 2, ownersurname)
        self.listctrl.SetStringItem(count, 3, animal)
        self.listctrl.SetStringItem(count, 4, vet)
        
        appointmenttime = time
        
        hours = str(appointmenttime).split(":")[0]
        minutes = str(appointmenttime).split(":")[1]
        
        totalappointmentminutes = ( int(hours) * 60 ) + int(minutes)
        
        overdue = totalcurrentminutes - totalappointmentminutes
        
        if overdue < 0:
          
          self.listctrl.SetItemBackgroundColour(count, green)
          
        elif overdue < 10 or late == True:
          
          self.listctrl.SetItemBackgroundColour(count, yellow)
          
        else:
          
          self.listctrl.SetItemBackgroundColour(count, red)
        
      elif self.index == 0:
        
        currenttime = datetime.datetime.today().strftime("%H:%M")
        
        hours = str(currenttime).split(":")[0]
        minutes = str(currenttime).split(":")[1]
        
        totalcurrentminutes = ( int(hours) * 60 ) + int(minutes)
        
        self.itemDataMap[a[0]] = ( time, ownersurname, animal, vet )
        self.listctrl.InsertStringItem(count, time)
        self.listctrl.SetStringItem(count, 1, ownersurname)
        self.listctrl.SetStringItem(count, 2, animal)
        self.listctrl.SetStringItem(count, 3, vet)
        
        appointmenttime = time
        
        hours = str(appointmenttime).split(":")[0]
        minutes = str(appointmenttime).split(":")[1]
        
        totalappointmentminutes = ( int(hours) * 60 ) + int(minutes)
        
        overdue = totalcurrentminutes - totalappointmentminutes
        
        if overdue < 0:
          
          self.listctrl.SetItemBackgroundColour(count, green)
          
        else:
          
          self.listctrl.SetItemBackgroundColour(count, red)
      else:
        
        self.itemDataMap[a[0]] = ( time, animal, vet )
        self.listctrl.InsertStringItem(count, time)
        self.listctrl.SetStringItem(count, 1, ownersurname)
        self.listctrl.SetStringItem(count, 2, animal)
        self.listctrl.SetStringItem(count, 3, vet)
      
      #self.listctrl.InsertStringItem(count, time)
      
      if asmref == "":
        
        self.listctrl.SetItemImage(count, 1)
        
      else:
      
        self.listctrl.SetItemImage(count, 0)
      
      self.listctrl.SetItemData(count, a[0])
      
      count = count + 1
    
    if len(self.htmllist) == 0:
      
      self.listctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
      self.listctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
      self.listctrl.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
      
      if self.index == 1:
        
        self.listctrl.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
      
    else:
      
      
      
      if self.index == 3:
        
        self.listctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        columnwidth = self.listctrl.GetColumnWidth(0)
        self.listctrl.SetColumnWidth(0, columnwidth + 30)
        self.listctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.listctrl.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        self.listctrl.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)
        
      elif self.index == 1:
        
        self.listctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        columnwidth = self.listctrl.GetColumnWidth(0)
        self.listctrl.SetColumnWidth(0, columnwidth + 30)
        self.listctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.listctrl.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        self.listctrl.SetColumnWidth(3, wx.LIST_AUTOSIZE)
        
      else:
        
        self.listctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        columnwidth = self.listctrl.GetColumnWidth(0)
        self.listctrl.SetColumnWidth(0, columnwidth + 30)
        self.listctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.listctrl.SetColumnWidth(2, wx.LIST_AUTOSIZE)
    
    self.listctrl.htmllist = self.htmllist
    
    #if len(self.htmllist) > 0:
      
      #self.listctrl.Bind(wx.EVT_RIGHT_DOWN, self.parent.AppointmentMenuPopup)
      
    #else:
      
      #self.listctrl.Unbind(wx.EVT_RIGHT_DOWN)

class MedicationListbox(wx.HtmlListBox):
  
  def __init__(self, parent, localsettings):
    
    wx.HtmlListBox.__init__(self, parent, -1)
    
    self.htmllist = []
    self.localsettings = localsettings
    self.parent = parent
    self.SetItemCount(0)
    self.stocklist = ""
  
  def OnGetItem(self, n):
    
    if len(self.htmllist) > 0:
      medicationid = self.htmllist[n][0]
      name = self.htmllist[n][1]
      description = self.htmllist[n][2]
      
      if description != "":
        
        description = "<br><font color=red size=2>" + str(description) + "</font>"
      
      unit = self.htmllist[n][3]
      batchno = self.htmllist[n][4]
      price = self.htmllist[n][5]
      price = miscmethods.FormatPrice(price)
      balance = self.htmllist[n][11]
      
      #print "balance = " + str(balance)
      
      output = "<table width=100% cellpadding=0 cellspacing=0><tr><td valign=top width=100%><font size=3 color=blue><b>" + str(name) + "</b></font>&nbsp;<font size=2>(" + self.localsettings.t("currency") + str(price) + " x " + str(unit) + ")</font>" + description + "</td><td align=right valign=top nowrap>" + str(balance) + "</font>&nbsp;</td></tr></table>"
      
      return output
  
  def RefreshList(self, ID=False):
    
    self.Hide()
    
    self.SetSelection(-1)
    
    medicationid = self.parent.selectedmedicationid
    
    if medicationid == -1:
      self.parent.medicationmovementspanel.Disable()
    
    name = self.parent.medicationsearchpanel.nameentry.GetValue()
    description = self.parent.medicationsearchpanel.descriptionentry.GetValue()
    
    shop = self.parent.medicationsearchpanel.shopcheckbox.GetValue()
    medication = self.parent.medicationsearchpanel.medicationcheckbox.GetValue()
    vaccination = self.parent.medicationsearchpanel.vaccinationcheckbox.GetValue()
    consumable = self.parent.medicationsearchpanel.consumablecheckbox.GetValue()
    chip = self.parent.medicationsearchpanel.chipcheckbox.GetValue()
    
    runninglow = self.parent.medicationsearchpanel.runninglowentry.GetValue()
    
    if name == "" and description == "":
    
      action = "SELECT * FROM medication"
      
    else:
      action = "SELECT * FROM medication WHERE Name LIKE \"%" + name + "%\" AND Description LIKE \"%" + description + "%\""
    
    if shop == False or medication == False or vaccination == False or consumable == False:
      
      if action == "SELECT * FROM medication":
        
        action = action + " WHERE "
        
      else:
        
        action = action + " AND "
      
      checkboxarguments = ""
      
      if medication == False:
        
        checkboxarguments = "Type != 0"
      
      if vaccination == False:
        
        if checkboxarguments != "":
          
          checkboxarguments = checkboxarguments + " AND "
        
        checkboxarguments = checkboxarguments + "Type != 1"
      
      if consumable == False:
        
        if checkboxarguments != "":
          
          checkboxarguments = checkboxarguments + " AND "
        
        checkboxarguments = checkboxarguments + "Type != 2"
      
      if shop == False:
        
        if checkboxarguments != "":
          
          checkboxarguments = checkboxarguments + " AND "
        
        checkboxarguments = checkboxarguments + "Type != 3"
      
      if chip == False:
        
        if checkboxarguments != "":
          
          checkboxarguments = checkboxarguments + " AND "
        
        checkboxarguments = checkboxarguments + "Type != 4"
    
      action = action + checkboxarguments
    
    action = action + " ORDER BY Name"
    
    results = db.SendSQL(action, self.localsettings.dbconnection)
    
    action = "SELECT medicationin.Date, medicationin.ID, medicationin.MedicationID, medicationin.Amount, medicationin.BatchNo, DATE_FORMAT(medicationin.Expires, \"%Y-%m-%d\"), medicationin.WhereFrom, 0, medication.Unit FROM medicationin INNER JOIN medication ON medicationin.MedicationID = medication.ID"
    medicationin = db.SendSQL(action, self.localsettings.dbconnection)
    
    action = "SELECT medicationout.Date, medicationout.ID, medicationout.MedicationID, medicationout.Amount, medicationout.BatchNo, medicationout.WhereTo, medicationout.AppointmentID, 1, medication.Unit FROM medicationout INNER JOIN medication ON medicationout.MedicationID = medication.ID"
    medicationout = db.SendSQL(action, self.localsettings.dbconnection)
    
    modifiedresults = []
    
    newselection = -1
    
    count = -1
    
    for a in results:
      
      inresults = []
      
      medicationid = a[0]
      
      for b in medicationin:
        
        if b[2] == medicationid:
          
          inresults.append(b)
      
      outresults = []
      
      for b in medicationout:
        
        if b[2] == medicationid:
          
          outresults.append(b)
      
      batches = []
      intotal = 0
      outtotal = 0
      
      for b in inresults:
        
        if batches.__contains__(b[4].upper()) == False:## if list of batch nos contains the batch no of this movement
          
          batches.append(b[4].upper())
        
        intotal = intotal + b[3]
      
      for b in outresults:
        
        if batches.__contains__(b[4].upper()) == False:## if list of batch nos contains the batch no of this movement
          
          batches.append(b[4].upper())
        
        outtotal = outtotal + b[3]
      
      batchestotals = []
      
      for c in batches:
        
        total = 0
        for b in inresults:
          if b[4].upper() == c:
            total = total + b[3]
        for b in outresults:
          if b[4].upper() == c:
            total = total - b[3]
        if total != 0:
          batchestotals.append((total, c))
        
      
      total = intotal - outtotal
      
      if total > 0:
        colour = "green"
      else:
        colour = "red"
      
      balance = "<font color=" + colour + " size=3><b>" + str(total) + "</b></font>&nbsp;"
      
      batcheshtml = ""
      
      for b in batchestotals:
        
        if b[0] != 0:
          
          batcheshtml = batcheshtml + "\n" + self.localsettings.t("animalvaccinationbatchlabel") + unicode(b[1], "utf8") + " x " + str(b[0])
      
      output = list(a)
      output.append(balance)
      output.append(batcheshtml)
      
      if runninglow == True:
        
        if total < a[7]:
          
          count = count + 1
          
          if a[0] == self.parent.selectedmedicationid:
            
            newselection = count
          
          modifiedresults.append(output)
        
      else:
        
        count = count + 1
        
        if a[0] == self.parent.selectedmedicationid:
          
          newselection = count
        
        modifiedresults.append(output)
    
    newlistboxid = -1
    
    self.htmllist = modifiedresults
    
    self.SetItemCount(len(self.htmllist))
    
    if newselection != -1:
      
      self.SetSelection(newselection)
      self.ScrollToLine(newselection)
      
    else:
      
      self.parent.selectedmedicationid = -1
      
      self.parent.medicationmovementspanel.medicationid = -1
      
      self.parent.medicationmovementspanel.medicationmovementlist.RefreshList()
      self.parent.medicationmovementspanel.movementlabel.SetLabel("")
      self.parent.medicationmovementspanel.Disable()
    
    #if len(self.htmllist) == 0:
      #self.Disable()
    #else:
      #self.Enable()
    
    self.Show()

class MedicationMovementListBox(wx.HtmlListBox):
  
  def __init__(self, parent, localsettings):
    
    wx.HtmlListBox.__init__(self, parent, -1)
    
    self.htmllist = []
    self.localsettings = localsettings
    self.parent = parent
    self.SetItemCount(0)
    self.SetSelection(-1)
    self.total = 0
    self.selectedmovement = -1
  
  def OnGetItem(self, n):
    
    if len(self.htmllist) != 0:
      
      date = self.htmllist[n][0]
      date = miscmethods.GetDateFromSQLDate(date)
      date = miscmethods.FormatDate(date, self.localsettings)
      
      unit = unicode(self.htmllist[n][8], "utf8")
      
      quantity = self.htmllist[n][3]
      
      batchno = unicode(self.htmllist[n][4], "utf8").upper()
      
      header = "<table width=100% cellpadding=0 cellspacing=3><tr>"
      
      if self.htmllist[n][7] == 0:
        
        #print "source = " + str(type(self.htmllist[n][6]))
        
        source = self.htmllist[n][6]
        
        if source == self.localsettings.t("clientbalancelabel"):
          
          body = "<td valign=top nowrap><font color=blue>" + str(date) + "</font></td><td valign=top width=100%><font color=blue>" + source + "</font></td><td align=right valign=top nowrap><font color=blue>" + str(quantity) + " x " + unit + "</font></td>"
          
        else:
          
          body = "<td valign=top nowrap>" + str(date) + "</td><td valign=top width=100%><font color=blue>" + batchno + "</font> " + self.localsettings.t("fromlabel") + " " + source + "</td><td valign=top align=right nowrap><font color=green>+" + str(quantity) + " x " + unit + "</font></td>"
        
      else:
        destination = unicode(self.htmllist[n][5], "utf8")
        #print "destination = " + destination
        body = "<td valign=top nowrap>" + str(date) + "</td><td valign=top width=100%><font color=blue>" + batchno + "</font> " + self.localsettings.t("tolabel") + " " + destination + "</td><td valign=top align=right nowrap><font color=red>-" + str(quantity) + " x " + unit + "</font></td>"
      
      footer = "</tr></table>"
      
      return header + body + footer
  
  def RefreshList(self, ID=False):
    
    self.Hide()
    
    self.SetSelection(-1)
    
    #listboxid = self.GetSelection()
    
    #self.Clear()
    
    fromdate = self.parent.fromdateentry.GetValue()
    
    todate = self.parent.todateentry.GetValue()
    
    #print "fromdate = " + str(fromdate) + ", todate = " + str(todate)
    
    if str(fromdate) == "" and str(todate) == "":
      
      dateargumentsin = ""
      dateargumentsout = ""
      
    elif str(fromdate) == "" and str(todate) != "":
      
      dateargumentsin = " AND medicationin.Date <= \"" + miscmethods.GetSQLDateFromWXDate(todate) + "\""
      dateargumentsout = " AND medicationout.Date <= \"" + miscmethods.GetSQLDateFromWXDate(todate) + "\""
      
    elif str(fromdate) != "" and str(todate) == "":
      
      dateargumentsin = " AND medicationin.Date >= \"" + miscmethods.GetSQLDateFromWXDate(fromdate) + "\""
      dateargumentsout = " AND medicationout.Date >= \"" + miscmethods.GetSQLDateFromWXDate(fromdate) + "\""
      
    else:
      
      dateargumentsin = " AND medicationin.Date BETWEEN \"" + miscmethods.GetSQLDateFromWXDate(fromdate) + "\" AND \"" + miscmethods.GetSQLDateFromWXDate(todate) + "\""
      dateargumentsout = " AND medicationout.Date BETWEEN \"" + miscmethods.GetSQLDateFromWXDate(fromdate) + "\" AND \"" + miscmethods.GetSQLDateFromWXDate(todate) + "\""
    
    balance = 0
    
    if str(fromdate) != "":
      
      if self.parent.medicationid > 0:
        
        action = "SELECT Unit FROM medication WHERE ID = " + str(self.parent.medicationid)
        unit = db.SendSQL(action, self.localsettings.dbconnection)[0][0]
        
      else:
        
        unit = "unit"
      
      action = "SELECT Amount FROM medicationin WHERE Date < \"" + miscmethods.GetSQLDateFromWXDate(fromdate) + "\" AND MedicationID = " + str(self.parent.medicationid)
      inresults = db.SendSQL(action, self.localsettings.dbconnection)
      
      action = "SELECT Amount FROM medicationout WHERE Date < \"" + miscmethods.GetSQLDateFromWXDate(fromdate) + "\" AND MedicationID = " + str(self.parent.medicationid)
      outresults = db.SendSQL(action, self.localsettings.dbconnection)
      
      for a in inresults:
        
        balance = balance + a[0]
      
      for a in outresults:
        
        balance = balance - a[0]
    
    action = "SELECT medicationin.Date, medicationin.ID, medicationin.MedicationID, medicationin.Amount, CONCAT(\"" + self.localsettings.t("medicationbatchnolabel") + "\", medicationin.BatchNo ), DATE_FORMAT(medicationin.Expires, \"%Y-%m-%d\"), medicationin.WhereFrom, 0, medication.Unit FROM medicationin INNER JOIN medication ON medicationin.MedicationID = medication.ID WHERE medicationin.MedicationID = " + str(self.parent.medicationid) + dateargumentsin
    inresults = db.SendSQL(action, self.localsettings.dbconnection)
    
    action = "SELECT medicationout.Date, medicationout.ID, medicationout.MedicationID, medicationout.Amount, CONCAT(\"" + self.localsettings.t("medicationbatchnolabel") + "\", medicationout.BatchNo ), medicationout.WhereTo, medicationout.AppointmentID, 1, medication.Unit FROM medicationout INNER JOIN medication ON medicationout.MedicationID = medication.ID WHERE medicationout.MedicationID = " + str(self.parent.medicationid) + dateargumentsout
    outresults = db.SendSQL(action, self.localsettings.dbconnection)
    
    
    
    intotal = 0
    for a in inresults:
      intotal = intotal + a[3]
    
    outtotal = 0
    for a in outresults:
      outtotal = outtotal + a[3]
    
    self.total = balance + intotal - outtotal
    
    #print "fromdate = " + str(fromdate)
    
    #wxfromdate = miscmethods.GetWXDateFromSQLDate(fromdate)
    
    if str(fromdate) != "":
      
      balancetuple = ( (miscmethods.GetDateFromWXDate(fromdate), -1, self.parent.medicationid, balance, "", None,  self.localsettings.t("clientbalancelabel"), 0, unit), )
      
      results = balancetuple + inresults + outresults
      
    else:
      
      results =  inresults + outresults
    
    #print "results = " + str(results)
    
    resultslist = []
    
    newselection = -1
    
    for a in results:
      
      resultslist.append(a)
    
    results = resultslist
    results.sort(reverse=True)
    
    if self.selectedmovement != -1:
      
      count = -1
      
      for a in results:
        
        count = count + 1
        
        if resultslist[count][7] == self.selectedmovement[0] and results[count][1] == self.selectedmovement[1]:
          
          newselection = count
      
      if newselection != -1:
        
        self.SetSelection(newselection)
        
        self.ScrollToLine(newselection)
    
    self.htmllist = results
    
    self.SetItemCount(len(self.htmllist))
    
    if len(self.htmllist) == 0:
      self.Disable()
    else:
      self.Enable()
    
    self.Show()

class ProceduresListBox(wx.HtmlListBox):
  
  def __init__(self, parent, localsettings):
    
    wx.HtmlListBox.__init__(self, parent, -1)
    
    self.htmllist = []
    self.localsettings = localsettings
    self.parent = parent
    self.SetItemCount(0)
    self.SetSelection(-1)
  
  def OnGetItem(self, n):
    
    if len(self.htmllist) != 0:
      
      name = self.htmllist[n][1]
      description = self.htmllist[n][2]
      price = self.htmllist[n][3]
      price = miscmethods.FormatPrice(price)
      
      if description != "":
        
        description = "<font size=3>(" + description + ")</font>"
      
      output = "<table cellpadding=0 cellspacing=0><tr><td align=left valign=top><font color=blue size=4>" + name + "</font>&nbsp;</td><td align=left valign=top>" + description + "&nbsp;</td><td align=left valign=top><font size=3 color=red><b>" + self.localsettings.t("currency") + price + "</b></font></td></tr></table>"
      
      return output
  
  def RefreshList(self, ID=False):
    
    self.Hide()
    
    action = "SELECT * FROM procedures ORDER BY Name"
    results = db.SendSQL(action, self.localsettings.dbconnection)
    
    self.htmllist = results
    
    self.SetItemCount(len(self.htmllist))
    
    self.SetSelection(-1)
    
    self.Show()

class VaccinationListbox(wx.HtmlListBox):
  
  def __init__(self, parent, localsettings):
    
    wx.HtmlListBox.__init__(self, parent, -1)
    
    self.htmllist = []
    self.localsettings = localsettings
    self.parent = parent
    self.SetItemCount(0)
    self.SetSelection(-1)
  
  def OnGetItem(self, n):
    
    #print "self.htmllist = " + str(self.htmllist)
    
    if len(self.htmllist) > 0:
      
      vaccinationid = self.htmllist[n][0]
      name = self.htmllist[n][1]
      description = self.htmllist[n][2]
      #unit = self.htmllist[n][3]
      batchno = self.htmllist[n][3]
      price = self.htmllist[n][4]
      price = miscmethods.FormatPrice(price)
      balance = self.htmllist[n][6]
      
      #print "balance = " + str(balance)
      
      vaccine_t = self.localsettings.t('animalvaccinelabel').lower()
      
      output = "<table width=100% cellpadding=0 cellspacing=0><tr><td valign=top width=100%><font size=2 color=blue>" + str(name) + "</font>&nbsp;<font size=1>(" + self.localsettings.t("currency") + str(price) + " x " + vaccine_t +")</font><br><font color=red size=1>" + str(description) + "</font></td><td align=right valign=top nowrap>" + balance + "</font></td></tr></table>"
      
      return output
  
  def RefreshList(self, ID=False):
    
    self.Hide()
    
    self.SetSelection(-1)
    
    action = "SELECT * FROM vaccinationtype ORDER BY Name"
    results = db.SendSQL(action, self.localsettings.dbconnection)
    
    action = "SELECT vaccinationin.Date, vaccinationin.ID, vaccinationin.VaccinationID, vaccinationin.Amount, vaccinationin.BatchNo, DATE_FORMAT(vaccinationin.Expires, \"%Y-%m-%d\"), vaccinationin.WhereFrom, 0 FROM vaccinationin INNER JOIN vaccinationtype ON vaccinationin.VaccinationID = vaccinationtype.ID"
    vaccinationin = db.SendSQL(action, self.localsettings.dbconnection)
    
    action = "SELECT vaccinationout.Date, vaccinationout.ID, vaccinationout.VaccinationID, vaccinationout.Amount, vaccinationout.BatchNo, vaccinationout.WhereTo, vaccinationout.AppointmentID, 1 FROM vaccinationout INNER JOIN vaccinationtype ON vaccinationout.VaccinationID = vaccinationtype.ID"
    vaccinationout = db.SendSQL(action, self.localsettings.dbconnection)
    
    modifiedresults = []
    
    newselection = -1
    
    count = -1
    
    for a in results:
      
      count = count + 1
      
      if a[0] == self.parent.selectedvaccinationid:
        
        newselection = count
      
      inresults = []
      
      vaccinationid = a[0]
      
      for b in vaccinationin:
        
        if b[2] == vaccinationid:
          
          inresults.append(b)
      
      outresults = []
      
      for b in vaccinationout:
        
        if b[2] == vaccinationid:
          
          outresults.append(b)
      
      batches = []
      intotal = 0
      outtotal = 0
      
      for b in inresults:
        if batches.__contains__(b[4].upper()) == False:
          batches.append(b[4].upper())
        intotal = intotal + b[3]
      
      for b in outresults:
        outtotal = outtotal + b[3]
      
      batchestotals = []
      for c in batches:
        total = 0
        for b in inresults:
          if b[4].upper() == c:
            total = total + b[3]
        for b in outresults:
          if b[4].upper() == c:
            total = total - b[3]
        if total != 0:
          batchestotals.append((total, c))
        
      
      total = intotal - outtotal
      
      if total > 0:
        colour = "green"
      else:
        colour = "red"
      
      balance = "<font color=" + colour + " size=2>" + str(total) + "</font>&nbsp;<font color=blue size=1>"
      
      for b in batchestotals:
        
        balance = balance + "<br>Batch: " + b[1] + " x " + str(b[0]) + "&nbsp;"
      
      
      output = list(a)
      output.append(balance)
      
      modifiedresults.append(output)
    
    self.htmllist = modifiedresults
    
    self.SetItemCount(len(self.htmllist))
    
    if newselection != -1:
      self.SetSelection(newselection)
      self.ScrollToLine(newselection)
      self.parent.VaccinationSelected()
    else:
      self.parent.editvaccinationbutton.Disable()
      self.parent.deletevaccinationbutton.Disable()
      self.parent.selectedvaccinationid = -1
      self.parent.ClearVaccinationEntries()
      self.parent.vaccinationmovementspanel.Disable()
      self.parent.vaccinationmovementspanel.vaccinationmovementlist.RefreshList()
    
    if len(self.htmllist) == 0:
      self.Disable()
    else:
      self.Enable()
    
    self.Show()

class VaccinationMovementListBox(wx.HtmlListBox):
  
  def __init__(self, parent, localsettings):
    
    wx.HtmlListBox.__init__(self, parent, -1)
    
    self.htmllist = []
    self.localsettings = localsettings
    self.parent = parent
    self.SetItemCount(0)
    self.SetSelection(-1)
    self.total = 0
    self.selectedmovement = -1
  
  def OnGetItem(self, n):
    
    if len(self.htmllist) != 0:
      
      date = self.htmllist[n][0]
      date = miscmethods.GetDateFromSQLDate(date)
      date = miscmethods.FormatDate(date, self.localsettings)
      
      quantity = self.htmllist[n][3]
      
      vaccine_t = self.localsettings.t('animalvaccinelabel').lower()
      
      if self.htmllist[n][7] == 0:
        source = self.htmllist[n][6]
        output = "<table width=100%><tr><td nowrap>" + str(date) + "</td><td width=100%>From " + source + "</td><td align=right nowrap><font color=green>+" + str(quantity) + " x " + vaccine_t +"</font></td></tr></table>"
      else:
        destination = self.htmllist[n][5]
        output = "<table width=100%><tr><td nowrap>" + str(date) + "</td><td width=100%>To " + destination + "</td><td align=right nowrap><font color=red>-" + str(quantity) + " x " + vaccine_t +"</font></td></tr></table>"
      
      return output
  
  def RefreshList(self, ID=False):
    
    self.Hide()
    
    self.SetSelection(-1)
    
    action = "SELECT vaccinationin.Date, vaccinationin.ID, vaccinationin.VaccinationID, vaccinationin.Amount, vaccinationin.BatchNo, DATE_FORMAT(vaccinationin.Expires, \"%Y-%m-%d\"), vaccinationin.WhereFrom, 0 FROM vaccinationin WHERE vaccinationin.VaccinationID = " + str(self.parent.vaccinationid)
    inresults = db.SendSQL(action, self.localsettings.dbconnection)
    
    action = "SELECT vaccinationout.Date, vaccinationout.ID, vaccinationout.VaccinationID, vaccinationout.Amount, vaccinationout.BatchNo, vaccinationout.WhereTo, vaccinationout.AppointmentID, 1 FROM vaccinationout WHERE vaccinationout.VaccinationID = " + str(self.parent.vaccinationid)
    outresults = db.SendSQL(action, self.localsettings.dbconnection)
    
    intotal = 0
    
    for a in inresults:
      
      intotal = intotal + a[3]
    
    outtotal = 0
    
    for a in outresults:
      
      outtotal = outtotal + a[3]
    
    self.total = intotal - outtotal
    
    results = inresults + outresults
    
    resultslist = []
    
    for a in results:
      
      resultslist.append(a)
    
    results = resultslist
    results.sort(reverse=True)
    
    if self.selectedmovement != -1:
      
      count = -1
      
      for a in results:
        
        count = count + 1
        
        if resultslist[count][7] == self.selectedmovement[0] and results[count][1] == self.selectedmovement[1]:
          
          newselection = count
      
      if newselection != -1:
        
        self.SetSelection(newselection)
        
        self.ScrollToLine(newselection)
    
    self.htmllist = results
    
    self.SetItemCount(len(self.htmllist))
    
    if len(self.htmllist) == 0:
      self.Disable()
    else:
      self.Enable()
    
    self.Show()

class ReceiptListbox(wx.HtmlListBox):
  
  def __init__(self, parent, localsettings):
    
    wx.HtmlListBox.__init__(self, parent, -1)
    
    self.htmllist = []
    self.localsettings = localsettings
    self.parent = parent
    self.SetItemCount(0)
    self.SetSelection(-1)
    self.total = 0.00
  
  def OnGetItem(self, n):
    
    if len(self.htmllist) > 0:
      
      name = self.htmllist[n][2]
      price = self.htmllist[n][3]
      price = miscmethods.FormatPrice(price * -1)
      
      #if n == 0:
        #output = "<table width=100% cellpadding=0 cellspacing=0><tr><td align=left><b>Total:</b></td><td align=right><b>" + self.localsettings.t("currency") + self.htmllist[-1] + "</b>&nbsp;</td></tr></table><table width=100% cellpadding=0 cellspacing=0><tr><td align=left valign=top>" + name + "</td><td align=right valign=top>" + self.localsettings.t("currency") + price + "&nbsp;</td></tr></table>"
        #return output
      #else:
      output = "<table width=100% cellpadding=0 cellspacing=0><tr><td align=left valign=top><font size=2>" + name + "</font></td><td align=right valign=top><font size=2>" + self.localsettings.t("currency") + price + "&nbsp;</font></td></tr></table>"
      
      return output
  
  def RefreshList(self, ID=False):
    
    self.Hide()
    
    action = "SELECT * FROM receipt WHERE AppointmentID = " + str(self.parent.appointmentdata.ID) + " ORDER BY Description"
    results = db.SendSQL(action, self.localsettings.dbconnection)
    
    
    totalprice = 0
    
    for a in results:
      
      totalprice = totalprice + a[3]
    
    totalprice = miscmethods.FormatPrice(totalprice * -1)
    
    #results = results + (totalprice,)
    
    self.htmllist = results
    
    self.SetItemCount(len(self.htmllist))
    
    self.SetSelection(-1)
    
    currencysymbol = self.localsettings.t("currency")
    
    if currencysymbol == "&pound;":
      
      currencysymbol = u"\xa3"
    
    newtotal = self.localsettings.t("totallabel") + ": " + currencysymbol + totalprice + " "
    
    self.parent.receipttotallabel.SetLabel(miscmethods.NoWrap(newtotal))
    self.parent.prescribedbuttonssizer.Layout()
    
    self.parent.deletemedicationbutton.Disable()
    
    self.Refresh()
    
    self.Show()

#class AppointmentsSummaryListbox(wx.HtmlListBox):
  
  #def __init__(self, parent, animaldata, excludetoday=False):
    
    #wx.HtmlListBox.__init__(self, parent, -1)
    
    #self.htmllist = []
    #self.localsettings = animaldata.localsettings
    #self.parent = parent
    #self.animaldata = animaldata
    #self.excludetoday = excludetoday
    #self.SetItemCount(0)
    #self.SetSelection(-1)
  
  #def OnGetItem(self, n):
    
    #if len(self.htmllist) != 0:
      
      #date = self.htmllist[n][3]
      #date = miscmethods.FormatSQLDate(date, self.animaldata.localsettings)
      
      #time = self.htmllist[n][4]
      
      #time = miscmethods.FormatTime(time)
      
      #reason = self.htmllist[n][5]
      
      #return "<font color=blue>" + str(date) + "</font>&nbsp;" + time + "<br><font color=red>" + reason + "</font>"
  
  #def RefreshList(self, ID=False):
    
    #self.Hide()
    
    #if self.excludetoday == False:
      #action = "SELECT * FROM appointment WHERE AnimalID = " + str(self.animaldata.ID) + " ORDER BY Date, Time"
    #else:
      #today = datetime.date.today()
      #today = miscmethods.GetSQLDateFromDate(today)
      #action = "SELECT * FROM appointment WHERE AnimalID = " + str(self.animaldata.ID) + " AND Date != \"" + today + "\" ORDER BY Date, Time"
    
    #results = db.SendSQL(action, self.localsettings.dbconnection)
    
    
    #self.htmllist = results
    
    #self.SetItemCount(len(self.htmllist))
    
    #self.SetSelection(-1)
    
    #self.Show()

#class ReceiptSummaryListbox(wx.HtmlListBox):
  
  #def __init__(self, parent, clientdata):
    
    #wx.HtmlListBox.__init__(self, parent, -1)
    
    #self.htmllist = []
    #self.localsettings = clientdata.localsettings
    #self.parent = parent
    #self.clientdata = clientdata
    #self.totalprice = 0.00
    #self.SetItemCount(0)
    #self.SetSelection(-1)
  
  #def OnGetItem(self, n):
    
    #if len(self.htmllist) != 0:
      
      #date = self.htmllist[n][0]
      #date = miscmethods.FormatSQLDate(date, self.localsettings)
      
      #description = self.htmllist[n][2]
      
      #price = self.htmllist[n][1]
      
      #if price < 0:
        #colour = "red"
      #else:
        #colour = "green"
      
      #price = miscmethods.FormatPrice(price)
      
      #if description == "Balance":
        #output = "<table width=100% cellpadding=5 cellspacing=0><tr><td valign=top align=left nowrap><font size=3 color=green>" + date + "</font></td><td valign=middle align=left width=100%><font size=2 color=green>" + description + "</font></td><td valign=top align=right nowrap><font color=" + colour + " size=3>" + self.localsettings.t("currency" + price + "</font></td></tr></table>"
      #else:
        #output = "<table width=100% cellpadding=5 cellspacing=0><tr><td valign=top align=left nowrap><font size=3>" + date + "</font></td><td valign=middle align=left width=100%><font size=2>" + description + "</font></td><td valign=top align=right nowrap><font color=" + colour + " size=3>" + self.localsettings.t("currency") + price + "</font></td></tr></table>"
      
      #return output
  
  #def RefreshList(self, ID=False):
    
    #self.Hide()
    
    #if self.clientdata.ID != False:
      
      #action = "SELECT receipt.Price, receipt.Date, receipt.Description FROM receipt WHERE receipt.Type = 4 AND receipt.TypeID = " + str(self.clientdata.ID) + " AND receipt.Date < \"" + self.fromdate + "\""
      
      #balanceresults1 = db.SendSQL(action, self.localsettings.dbconnection)
      
      #action = "SELECT receipt.Price, receipt.Date, receipt.Description FROM appointment LEFT JOIN receipt ON appointment.ID = receipt.AppointmentID WHERE appointment.OwnerID = " + str(self.clientdata.ID) + " AND receipt.Date < \"" + self.fromdate + "\""
      
      #balanceresults2 = db.SendSQL(action, self.localsettings.dbconnection)
      
      #balanceresults = balanceresults1 + balanceresults2
      
      #balance = 0
      
      #for a in balanceresults:
        
        #balance = balance + a[0]
      
      #action = "SELECT receipt.Date, receipt.Price, receipt.Description, receipt.ID FROM receipt WHERE receipt.Type = 4 AND receipt.TypeID = " + str(self.clientdata.ID) + " AND receipt.Date BETWEEN \"" + self.fromdate + "\" AND \"" + self.todate + "\""
      
      #results1 = db.SendSQL(action, self.localsettings.dbconnection)
      
      #action = "SELECT receipt.Date, receipt.Price, receipt.Description, receipt.ID FROM appointment LEFT JOIN receipt ON appointment.ID = receipt.AppointmentID WHERE appointment.OwnerID = " + str(self.clientdata.ID) + " AND receipt.Date BETWEEN \"" + self.fromdate + "\" AND \"" + self.todate + "\""
      
      #results2 = db.SendSQL(action, self.localsettings.dbconnection)
      
    
    #else:
      
      #balance = 0
      #results1 = ()
      #results2 = ()
    
    #results = results1 + results2
    
    #results = list(results)
    
    #results.sort()
    
    #newresults = [(self.fromdate, balance, "Balance", 0),]
    
    #for a in results:
      
      #newresults.append(a)
    
    #results = newresults
    
    #totalprice = 0
    
    #for a in results:
      #totalprice = totalprice + a[1]
    
    #self.totalprice = totalprice
    
    #self.htmllist = results
    
    #self.SetItemCount(len(self.htmllist))
    
    #self.Show()
    
    #self.parent.clientpanel.billsummarypanel.GenerateBalance()

class VaccinationSummaryListbox(wx.HtmlListBox):
  
  def __init__(self, parent, animaldata):
    
    wx.HtmlListBox.__init__(self, parent, -1)
    
    self.htmllist = []
    self.localsettings = animaldata.localsettings
    self.parent = parent
    self.animaldata = animaldata
    self.SetItemCount(0)
    self.SetSelection(-1)
  
  def OnGetItem(self, n):
    
    #(ID, VaccinationID, Date, Amount, BatchNo, WhereTo, AppointmentID)
    
    if len(self.htmllist) != 0:
      
      date = self.htmllist[n][0]
      date = miscmethods.FormatSQLDate(date, self.localsettings)
      
      name = self.htmllist[n][2]
      
      batchno = self.htmllist[n][3]
      
      if str(self.htmllist[n][4]) != "None":
        
        nextdue = self.htmllist[n][4]
        nextdue = miscmethods.FormatSQLDate(nextdue, self.localsettings)
        
        #print "date = " + str(self.htmllist[n][4])      
        rawdate = miscmethods.GetDateFromSQLDate(self.htmllist[n][4])
        
        daypivot = rawdate - datetime.date.today()
        
        daypivot = daypivot.days
        
        if daypivot == 0:
          
          today_t = self.localsettings.t("today").upper()
          
          daypivot = "<font size=2 color=green><b> " + today_t +"</b></font>"
          
        elif daypivot > 0:
          
          in_t = self.localsettings.t("in").lower()
          day_t = self.localsettings.t("day").lower()
          days_t = self.localsettings.t("days").lower()
          
          daypivot_s = "<font size=2 color=green> "+ in_t +" " + str(daypivot) + " "
          
          if daypivot == 1:
             daypivot_s += day_t
          else:
             daypivot_s += days_t
          
          daypivot_s += "</font>"
          
        else:
          
          daypivot = daypivot * -1
          
          day_ago_t = self.localsettings.t("day_ago").lower()
          days_ago_t = self.localsettings.t("days_ago").lower()
          
          daypivot_s = "<font size=2 color=red> " + str(daypivot) + " "
          if daypivot == 1:
            daypivot_s += day_ago_t
          else:
            daypivot_s += days_ago_t
            
          daypivot += "</font>"
        
      else:
        
        daypivot = ""
        nextdue = ""
      
      #print str(daypivot)
      
      given_t = self.localsettings.t("animalgivenlabel")
      batch_t = self.localsettings.t("animalvaccinationbatchlabel")
      next_t = self.localsettings.t("animalnextlabel")
      
      return "<table width=100% cellpadding=0 cellspacing=5><tr><td valign=top><font size=2>" + given_t + "<br></font><font color=red>" + date + "</font></td><td valign=top width=100%><font color=blue>" + name + "<br></font><font size=2>"+ batch_t + " " + batchno + "</font></td><td valign=top><font size=2>" + next_t + "<br></font>" + nextdue + "<br>" + daypivot_s + "</td></tr></table>"
  
  def RefreshList(self, ID=False):
    
    self.Hide()
    
    if self.animaldata.ID != False:
      
      action = "SELECT medicationout.Date, medicationout.ID, medication.Name, medicationout.BatchNo, medicationout.NextDue, medicationout.MedicationID FROM medicationout INNER JOIN medication ON medicationout.MedicationID = medication.ID INNER JOIN appointment ON medicationout.AppointmentID = appointment.ID WHERE appointment.AnimalID = " + str(self.animaldata.ID)
      results1 = db.SendSQL(action, self.localsettings.dbconnection)
      
      action = "SELECT Date, ID, Name, Batch, Next, 0 FROM manualvaccination WHERE AnimalID = " + str(self.animaldata.ID)
      results2 = db.SendSQL(action, self.localsettings.dbconnection)
      
      
      
      self.htmllist = []
      
      if len(results1) > 0:
        self.htmllist = self.htmllist + list(results1)
      
      if len(results2) > 0:
        self.htmllist = self.htmllist + list(results2)
      
      if len(self.htmllist) > 1:
        
        self.htmllist.sort()
      
    else:
      
      self.htmllist = []
    
    self.SetItemCount(len(self.htmllist))
    
    self.SetSelection(-1)
    
    #self.parent.GetGrandParent().editvaccinationbutton.Disable()
    #self.parent.GetGrandParent().deletevaccinationbutton.Disable()
    
    self.Show()
    
    self.Refresh()

class DateCtrl(wx.TextCtrl):
  
  def __init__(self, parent, localsettings, silent=False):
    
    self.localsettings = localsettings
    self.silent = silent
    
    self.date = datetime.date.today()
    date = miscmethods.FormatDate(self.date, localsettings)
    
    wx.TextCtrl.__init__(self, parent, -1, date, size=(100,-1))
    self.SetToolTipString(self.localsettings.t("datectrltooltip"))
    self.Bind(wx.EVT_CHAR, self.ButtonPressed)
    self.Bind(wx.EVT_LEFT_DCLICK, self.PopupCalendar)
  
  def PopupCalendar(self, ID):
    
    dialog = wx.Dialog(self, -1, self.localsettings.t("choosedatetitle"))
    
    dialogsizer = wx.BoxSizer(wx.VERTICAL)
    
    browseappointmentspanel = appointmentmethods.BrowseAppointments(dialog, self.localsettings, True)
    
    dialogsizer.Add(browseappointmentspanel, 1, wx.EXPAND)
    
    dialog.SetSizer(dialogsizer)
    
    dialog.SetSize((800,600))
    
    dialog.ShowModal()
    
  
  def ButtonPressed(self, ID):
    
    keycode = ID.GetKeyCode()
    
    if keycode == 9 or keycode == 8 or keycode == 127 or keycode == 47 or keycode == 316 or keycode == 314 or keycode == 318 or keycode == 319 or (keycode > 47 and keycode < 58):
      
      if keycode == 9:
        
        date = wx.TextCtrl.GetValue(self)
        wx.TextCtrl.SetValue(self, date)
      
      ID.Skip()
    else:
      
      try:
        
        if keycode == 116 or keycode == 84:
          self.GetToday()
        
        value = wx.TextCtrl.GetValue(self)
        
        if self.localsettings.t("dateformat") == "DDMMYYYY":
          day = value[0:2]
          month = value[3:5]
          year = value[6:10]
        elif self.localsettings.t("dateformat") == "MMDDYYYY":
          day = value[3:5]
          month = value[0:2]
          year = value[6:10]
        else:
          day = value[-2:]
          month = value[5:7]
          year = value[:4]
        
        self.date = datetime.date(int(year), int(month), int(day))
        
        if keycode == 100:
          self.AddDay()
        elif keycode == 68:
          self.SubtractDay()
        elif keycode == 119:
          self.AddWeek()
        elif keycode == 87:
          self.SubtractWeek()
        elif keycode == 121:
          self.AddYear()
        elif keycode == 89:
          self.SubtractYear()
        elif keycode == 109:
          self.AddMonth()
        elif keycode == 77:
          self.SubtractMonth()
        
      except:
          
        pass
  
  def GetToday(self):
    
    self.date = datetime.date.today()
    
    wxdate = miscmethods.GetWXDateFromDate(self.date)
    self.SetValue(wxdate)
  
  def AddDay(self):
    
    timedelta = datetime.date(2006, 1, 2) - datetime.date(2006, 1, 1)
    
    self.date = self.date + timedelta
    
    wxdate = miscmethods.GetWXDateFromDate(self.date)
    self.SetValue(wxdate)
    
  def SubtractDay(self):
    
    timedelta = datetime.date(2006, 1, 2) - datetime.date(2006, 1, 1)
    
    self.date = self.date - timedelta
    
    wxdate = miscmethods.GetWXDateFromDate(self.date)
    self.SetValue(wxdate)
  
  def AddWeek(self):
    
    timedelta = datetime.date(2006, 1, 8) - datetime.date(2006, 1, 1)
    
    self.date = self.date + timedelta
    
    wxdate = miscmethods.GetWXDateFromDate(self.date)
    self.SetValue(wxdate)
  
  def SubtractWeek(self):
    
    timedelta = datetime.date(2006, 1, 8) - datetime.date(2006, 1, 1)
    
    self.date = self.date - timedelta
    
    wxdate = miscmethods.GetWXDateFromDate(self.date)
    self.SetValue(wxdate)
  
  def AddYear(self):
    
    currentday = self.date.day
    currentmonth = self.date.month
    currentyear = self.date.year
    
    newmonth = currentmonth
    newyear = currentyear + 1
    
    newday = currentday
    
    success = False
    
    while success == False:
      
      try:
        
        newdate = datetime.date(newyear, newmonth, newday)
        success = True
        
      except:
        
        newday = newday - 1
    
    self.date = newdate
    
    wxdate = miscmethods.GetWXDateFromDate(self.date)
    self.SetValue(wxdate)
  
  def SubtractYear(self):
    
    currentday = self.date.day
    currentmonth = self.date.month
    currentyear = self.date.year
    
    newmonth = currentmonth
    newyear = currentyear - 1
    
    newday = currentday
    
    success = False
    
    while success == False:
      
      try:
        
        newdate = datetime.date(newyear, newmonth, newday)
        success = True
        
      except:
        
        newday = newday - 1
    
    self.date = newdate
    
    wxdate = miscmethods.GetWXDateFromDate(self.date)
    self.SetValue(wxdate)
  
  def AddMonth(self):
    
    currentday = self.date.day
    currentmonth = self.date.month
    currentyear = self.date.year
    
    if currentmonth == 12:
      
      newmonth = 1
      newyear = currentyear + 1
      
    else:
      
      newmonth = currentmonth + 1
      newyear = currentyear
    
    newday = currentday
    
    success = False
    
    while success == False:
      
      try:
        
        newdate = datetime.date(newyear, newmonth, newday)
        success = True
        
      except:
        
        newday = newday - 1
    
    self.date = newdate
    
    wxdate = miscmethods.GetWXDateFromDate(self.date)
    self.SetValue(wxdate)
  
  def SubtractMonth(self):
    
    currentday = self.date.day
    currentmonth = self.date.month
    currentyear = self.date.year
    
    if currentmonth == 1:
      
      newmonth = 12
      newyear = currentyear - 1
      
    else:
      
      newmonth = currentmonth - 1
      newyear = currentyear
    
    newday = currentday
    
    success = False
    
    while success == False:
      
      try:
        
        newdate = datetime.date(newyear, newmonth, newday)
        success = True
        
      except:
        
        newday = newday - 1
    
    self.date = newdate
    
    wxdate = miscmethods.GetWXDateFromDate(self.date)
    self.SetValue(wxdate)
  
  def GetValue(self):
    
    success = False
    
    try:
      value = wx.TextCtrl.GetValue(self)
      
      if value == "":
        
        output = ""
        
      else:
        
        if self.localsettings.t("dateformat") == "DDMMYYYY":
          
          if len(value) == 4:
            
            day = "01"
            month = "01"
            year = value
            
          elif len(value) == 7:
            
            day = "01"
            month = value[:2]
            year = value[-4:]
            
          else:
            
            day = value[0:2]
            month = value[3:5]
            year = value[6:10]
          
        elif self.localsettings.t("dateformat") == "MMDDYYYY":
          
          if len(value) == 4:
            
            day = "01"
            month = "01"
            year = value
            
          elif len(value) == 7:
            
            day = "01"
            month = value[:2]
            year = value[-4:]
            
          else:
            
            day = value[3:5]
            month = value[0:2]
            year = value[6:10]
          
        else:
          
          if len(value) == 4:
            
            day = "01"
            month = "01"
            year = value
            
          elif len(value) == 7:
            
            day = "01"
            month = value[:2]
            year = value[-4:]
            
          else:
            
            day = value[-2:]
            month = value[5:7]
            year = value[:4]
          
          
        output = wx.DateTime()
        output.Set(int(day), int(month) - 1, int(year))
        
        #self.SetValue(output)
      
      success = True
    except:
      pass
    
    if success == False:
      
      if self.silent == False:
        
        miscmethods.ShowMessage(str(output) + " is an invalid date!", self)
        #self.Clear()
        #self.Bind(wx.EVT_CHAR, self.ButtonPressed)
        self.SetFocus()
      
      output = False
    
    return output
  
  def SetValue(self, wxdate):
    
    if str(wxdate) != "None":
      
      self.date = miscmethods.GetDateFromWXDate(wxdate)
      output = miscmethods.FormatDate(self.date, self.localsettings)
      
    else:
      output = ""
    
    wx.TextCtrl.SetValue(self, output)

class Notebook(wx.Panel):
  
  def __init__(self, parent, localsettings):
    
    self.localsettings = localsettings
    
    self.frame = parent.GetParent()
    
    wx.Panel.__init__(self, parent)
    
    self.activecolour = "#b0ffdb"
    
    topsizer = wx.BoxSizer(wx.VERTICAL)

    tabsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    tabsdropdown = wx.Choice(self, -1)
    tabsdropdown.Hide()
    tabsdropdown.Bind(wx.EVT_CHOICE, self.PageSelected)
    tabsizer.Add(tabsdropdown, 1, wx.ALIGN_RIGHT)
    
    topsizer.Add(tabsizer, 0, wx.EXPAND)
    
    self.SetSizer(topsizer)
    
    self.tabsizer = tabsizer
    self.topsizer = topsizer
    self.tabsdropdown = tabsdropdown
    
    self.tabs = []
    self.pages = []
    self.tabchoices = []
    self.currentid = 0
    self.activepage = -1
    
    if self.localsettings.multiplepanels == 0:
      
      tabsdropdown.Hide()
  
  def AddPage(self, panel):
    
    pagetitle = panel.pagetitle
    pagetitle = pagetitle.replace(" ", u"\xa0")
    
    if self.localsettings.multiplepanels == 0:
      
      while len(self.pages) > 0:
        
        self.ClosePage(0, True)
    
    ##Hide previous active page
    if self.activepage != -1:
      count = 0
      for a in self.tabs:
        if a.image.ID == self.activepage:
          self.pages[count].Hide()
          self.DisableTab(self.tabs[count])
        count = count + 1
    
    ##Add to list of pages
    self.pages.append(panel)
    
    ##Add a new tab
    
    tabpanel = wx.Panel(self)
    self.tabs.append(tabpanel)
    self.tabchoices.append(pagetitle)
    tabpanel.Bind(wx.EVT_RIGHT_DOWN, self.RightClick)
    tabpanel.pagetitle = pagetitle
    tabpanel.ID = self.currentid
    
    spacersizer = wx.BoxSizer(wx.VERTICAL)
    
    spacer1 = wx.StaticText(tabpanel, -1, "", size=(-1,5))
    spacer1.ID = self.currentid
    spacer1.Bind(wx.EVT_LEFT_DOWN, self.PageSelected)
    spacer1.Bind(wx.EVT_RIGHT_DOWN, self.RightClick)
    spacersizer.Add(spacer1, 0, wx.EXPAND)
    
    
    tabsizer = wx.BoxSizer(wx.HORIZONTAL)
    tabsizer.Add(wx.StaticText(tabpanel, -1, "", size=(5,-1)), 0, wx.EXPAND)
    
    try:
      
      imagepath = panel.pageimage
      
    except:
      
      imagepath = "icons/system.png"
    
    bitmap = wx.Bitmap(imagepath)
    image = wx.StaticBitmap(tabpanel, -1, bitmap)
    image.SetToolTipString(pagetitle)
    image.ID = self.currentid
    image.Bind(wx.EVT_LEFT_DOWN, self.PageSelected)
    image.Bind(wx.EVT_RIGHT_DOWN, self.RightClick)
    tabsizer.Add(image, 0, wx.ALIGN_CENTER)
    
    tabspacer = wx.StaticText(tabpanel, -1, "", size=(5,-1))
    tabspacer.ID = self.currentid
    tabspacer.Bind(wx.EVT_LEFT_DOWN, self.PageSelected)
    tabspacer.Bind(wx.EVT_RIGHT_DOWN, self.RightClick)
    tabsizer.Add(tabspacer, 0, wx.EXPAND)
    
    tablabel = wx.StaticText(tabpanel, -1, pagetitle)
    #tablabel.SetToolTipString(pagetitle)
    tablabel.ID = self.currentid
    tablabel.Bind(wx.EVT_LEFT_DOWN, self.PageSelected)
    tablabel.Bind(wx.EVT_RIGHT_DOWN, self.RightClick)
    tabsizer.Add(tablabel, 1, wx.ALIGN_CENTER)
    tabsizer.Add(wx.StaticText(tabpanel, -1, "", size=(5,-1)), 0, wx.EXPAND)
    
    if self.localsettings.multiplepanels == 1:
      
      closesizer = wx.BoxSizer(wx.VERTICAL)
      closebitmap = wx.Bitmap("icons/close.png")
      tabpanel.closebutton = wx.StaticBitmap(tabpanel, -1, closebitmap)
      tabpanel.closebutton.ID = self.currentid
      tabpanel.closebutton.SetToolTipString(self.localsettings.t("closelabel"))
      tabpanel.closebutton.Bind(wx.EVT_LEFT_DOWN, self.ClosePage)
      closesizer.Add(tabpanel.closebutton, 0, wx.EXPAND)
      tabsizer.Add(closesizer, 0, wx.EXPAND)
      
      spacer2 = wx.StaticText(tabpanel, -1, "", size=(5,-1))
      spacer2.ID = self.currentid
      spacer2.Bind(wx.EVT_LEFT_DOWN, self.PageSelected)
      spacer2.Bind(wx.EVT_RIGHT_DOWN, self.RightClick)
      tabsizer.Add(spacer2, 0, wx.EXPAND)
    
    spacersizer.Add(tabsizer, 0, wx.EXPAND)
    
    spacer3 = wx.StaticText(tabpanel, -1, "", size=(-1,5))
    spacer3.ID = self.currentid
    spacer3.Bind(wx.EVT_LEFT_DOWN, self.PageSelected)
    spacer3.Bind(wx.EVT_RIGHT_DOWN, self.RightClick)
    spacersizer.Add(spacer3, 0, wx.EXPAND)
    
    tabpanel.SetSizer(spacersizer)
    self.tabsizer.Add(tabpanel, 1, wx.EXPAND)
    self.topsizer.Add(panel, 1, wx.EXPAND)

    tabpanel.image = image
    tabpanel.tablabel = tablabel
    tabpanel.tabspacer = tabspacer
    tabpanel.tablabel = tablabel
    tabpanel.tabsizer = tabsizer
    
    
    ##Declare new active page
    self.activepage = self.currentid
                
    self.EnableTab(self.tabs[-1])
    
    tabpanel.Bind(wx.EVT_LEFT_DOWN, self.PageSelected)

    tabpanel.image = image
    self.currentid = self.currentid + 1
    self.topsizer.Layout()
    
  def ClosePage(self, ID, forceclose=False):
    
    try:
      
      eventobject = ID.GetEventObject()
      pageid = eventobject.ID
      
    except:
      pageid = ID
    
    if forceclose == False:
      
      try:
        success = self.pages[pageid].ClosePage()
      except:
        success = True
      
    else:
      
      success = True
    
    if success == True:
      
      count = 0
      
      for a in self.tabs:
              
        if a.ID == pageid:
                
          self.pages[count].Destroy()
          self.pages.remove(self.pages[count])
          
          self.tabs[count].Destroy()
          self.tabs.remove(self.tabs[count])
        
        count = count + 1
      
      if len(self.pages) == 0:
              
        self.activepage = -1
                                
      elif self.activepage == pageid:
                                
        self.activepage = -1
                                
        if len(self.pages) > 0:
                                        
          self.activepage = self.tabs[-1].image.ID
          self.EnableTab(self.tabs[-1])
          self.pages[-1].Show()
      
      self.topsizer.Layout()
      
      #print "after closing, activepage = " + str(self.activepage)
  
  def DisableTab(self, tab):
    
    font = tab.tablabel.GetFont()
    font.SetPointSize(7)
    font.SetWeight(wx.FONTWEIGHT_NORMAL)
    tab.tablabel.SetFont(font)
    
    defaultcolour = self.GetBackgroundColour().Get()
    
    newcolour = []
    
    for a in range(0, 3):
      
      colour = defaultcolour[a]
      
      if colour > 20:
        
        colour = colour - 20
      
      newcolour.append(colour)
    
    tab.SetBackgroundColour(newcolour)
    
    #for a in (tab.image, tab.tablabel, tab.tabspacer, tab.tablabel):
    #  
    #  a.SetBackgroundColour(newcolour)
    tab.Hide()
    tab.tabsizer.Layout()
    tab.Show()
  
  def EnableTab(self, tab):
    
    font = tab.tablabel.GetFont()
    font.SetPointSize(8)
    font.SetWeight(wx.FONTWEIGHT_BOLD)
    tab.tablabel.SetFont(font)
    
    defaultcolour = self.GetBackgroundColour().Get()
    
    tab.SetBackgroundColour(defaultcolour)
    
    #for a in (tab.image, tab.tablabel, tab.tabspacer, tab.tablabel):
    #  
    #  a.SetBackgroundColour(defaultcolour)
    tab.Hide()
    tab.tabsizer.Layout()
    tab.Show()
  
  def PageSelected(self, ID, pageid=-1):
    
    if pageid == -1:
      
      pageid = ID.GetEventObject().ID
    
    if pageid != self.activepage:
                        
      count = 0
      
      for a in self.tabs:
              
        if a.image.ID == self.activepage:
                
          self.pages[count].Hide()
          
          self.DisableTab(self.tabs[count])
        
        count = count + 1
      
      count = 0
      
      for a in self.tabs:
              
        if a.image.ID == pageid:
                
          self.activepage = a.image.ID
          
          self.EnableTab(self.tabs[count])
          
          self.pages[count].Show()
        
        count = count + 1
      
      self.topsizer.Layout()
  
  def RightClick(self, ID):
    
    popupmenu = wx.Menu()
    
    popupmenu.parent = ID.GetEventObject()
    
    detatchmenu = wx.MenuItem(popupmenu, DETATCH_TAB, self.localsettings.t("closelabel"))
    detatchmenu.SetBitmap(wx.Bitmap("icons/close.png"))
    popupmenu.AppendItem(detatchmenu)
    wx.EVT_MENU(popupmenu, DETATCH_TAB, self.ClosePageFromMenu)
    
    self.PopupMenu(popupmenu)
  
  def ClosePageFromMenu(self, ID):
    
    pageno = ID.GetEventObject().parent.ID
    
    self.ClosePage(pageno)

class ListCtrlWrapper(wx.Panel, listmix.ColumnSorterMixin):
  
  def __init__(self, parent, localsettings, columnheadings, images=False):
    
    wx.Panel.__init__(self, parent)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    self.listctrl = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
    listmix.ColumnSorterMixin.__init__(self, len(columnheadings))
    topsizer.Add(self.listctrl, 1, wx.EXPAND)
    
    if images != False:
      
      imagelist = wx.ImageList(20, 20)
      
      for a in images:
        
        imagelist.Add(wx.Bitmap(a))
      
      self.listctrl.AssignImageList(imagelist, wx.IMAGE_LIST_SMALL)
    
    self.SetSizer(topsizer)
    
    self.htmllist = []
    self.localsettings = localsettings
    self.parent = parent
    self.columnheadings = columnheadings
  
  def GetListCtrl(self):# Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    
          return self.listctrl
  
  def GetSelection(self):
    
    listboxid = self.listctrl.GetFocusedItem()
    itemid = self.listctrl.GetItemData(listboxid)
    
    selection = -1
    
    count = 0
    
    for a in self.htmllist:
      
      if a[0] == itemid:
        
        selection = count
      
      count = count + 1
    
    return selection
  
  def ScrollToLine(self, lineno):
    
    self.listctrl.SetScrollPos(wx.VERTICAL, lineno)
  
  def SetSelection(self, selection):
    
    self.listctrl.Unbind(wx.EVT_LIST_ITEM_SELECTED)
    
    if selection == -1:
      
      for a in range(0, len(self.htmllist)):
        
        self.listctrl.Select(a, 0)
      
    else:
      
      self.listctrl.Select(selection)
  
  def RefreshList(self, ID=False):
    
    self.itemDataMap = {}
    
    self.listctrl.ClearAll()
    
    count = 0
    
    for a in self.columnheadings:
      
      self.listctrl.InsertColumn(count, a)
      
      count = count + 1
    
    count = 0
    
    for a in self.htmllist:
      
      processedrow = self.ProcessRow(a)
      
      output = processedrow[0]
      
      self.itemDataMap[output[0]] = tuple(output[1:])
      self.listctrl.InsertStringItem(count, output[1])
      
      bcount = 1
      
      for b in output[2:]:
        
        self.listctrl.SetStringItem(count, bcount, b.replace("\r", "").replace("\n", " "))
        
        bcount = bcount + 1
      
      if processedrow[1] != -1:
        
        self.listctrl.SetItemImage(count, processedrow[1])
      
      self.listctrl.SetItemData(count, output[0])
      
      count = count + 1
    
    #for a in range(0, len(self.columnheadings)):
      
      #self.listctrl.SetColumnWidth(a, wx.LIST_AUTOSIZE_USEHEADER)
    
    if len(self.htmllist) > 0:
      
      if processedrow[1] == -1:
        
        self.listctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        
      else:
        
        if str(sys.platform)[:3] != "win":
          
          self.listctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
          columnwidth = self.listctrl.GetColumnWidth(0)
          self.listctrl.SetColumnWidth(0, columnwidth + 25)
          
        else:
          
          self.listctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
    
    for a in range(1, len(self.columnheadings)):
      
      self.listctrl.SetColumnWidth(a, wx.LIST_AUTOSIZE)
    
    for a in range(0, len(self.columnheadings)):
      
      headerwidth = self.listctrl.GetColumnWidth(a)
      
      self.listctrl.SetColumnWidth(a, wx.LIST_AUTOSIZE_USEHEADER)
      
      if self.listctrl.GetColumnWidth(a) < headerwidth:
        
        self.listctrl.SetColumnWidth(a, headerwidth)
  
  def GetFocusedItem(self):
    
    return wx.ListCtrl.GetFocusedItem(self.listctrl)
  
  def GetItemData(self, dataid):
    
    return wx.ListCtrl.GetItemData(self.listctrl, dataid)

class AppointmentsSummaryListbox(ListCtrlWrapper):
  
  def t(self, field, idx = 0):
    
    return  self.animaldata.localsettings.t(field, idx)
  
  def __init__(self, parent, animaldata, excludetoday=False):
    
    self.htmllist = []
    self.localsettings = animaldata.localsettings
    self.parent = parent
    self.animaldata = animaldata
    self.excludetoday = excludetoday
    
    columnheadings = (self.t("datelabel"), self.t("timelabel"), self.t("reasonlabel"))
    
    ListCtrlWrapper.__init__(self, parent, animaldata.localsettings, columnheadings, ("icons/clock.png", "icons/ontime.png", "icons/late.png", "icons/dna.png"))
  
  def RefreshList(self, ID=False):
    
    if self.excludetoday == False:
      
      action = "SELECT * FROM appointment WHERE AnimalID = " + str(self.animaldata.ID) + " ORDER BY Date desc, Time"
      
    else:
      
      today = datetime.date.today()
      today = miscmethods.GetSQLDateFromDate(today)
      action = "SELECT * FROM appointment WHERE AnimalID = " + str(self.animaldata.ID) + " AND Date != \"" + today + "\" ORDER BY Date desc, Time"
    
    self.htmllist = db.SendSQL(action, self.localsettings.dbconnection)
    
    ListCtrlWrapper.RefreshList(self)
  
  def ProcessRow(self, rowdata):
    
    appointmentid = rowdata[0]
    
    date = rowdata[3]
    date = miscmethods.FormatSQLDate(date, self.localsettings)
    
    time = rowdata[4]
    
    arrivaltime = rowdata[16]
    
    imageid = 0
    
    if miscmethods.GetDateFromSQLDate(rowdata[3]) < datetime.date.today():
      
      imageid = 1
      
      if rowdata[6] == 0 and rowdata[7] == 0  and rowdata[11] == 0:
        
        imageid = 3
        
      elif arrivaltime != None:
        
        if arrivaltime > time:
          
          imageid = 2
    
    time = miscmethods.FormatTime(time)
    
    reason = rowdata[5]
    
    output = ((appointmentid, date, time, reason), imageid)
    
    return output

class ReceiptSummaryListbox(ListCtrlWrapper):
  
  def t(self, field, idx = 0):
    
    return  self.localsettings.t(field, idx)
  
  def __init__(self, parent, clientdata):
    
    self.htmllist = []
    self.localsettings = clientdata.localsettings
    self.parent = parent
    self.clientdata = clientdata
    self.totalprice = 0.00
    
    columnheadings = (self.t("datelabel"), self.t("descriptionlabel"), self.t("pricelabel"))
    
    ListCtrlWrapper.__init__(self, parent, self.localsettings, columnheadings, ("icons/downarrowred.png", "icons/uparrow.png", "icons/rightarrow.png"))
    
  def ProcessRow(self, rowdata):
    
    date = rowdata[0]
    date = miscmethods.FormatSQLDate(date, self.localsettings)
    
    description = rowdata[2]
    
    price = rowdata[1]
    
    if price < 0:
      
      imageid = 0
      
    elif price > 0:
      
      imageid = 1
      
    else:
      
      imageid = 2
    
    receiptid = rowdata[3]
    
    if price < 0:
      
      colour = "red"
      
    else:
      
      colour = "green"
    
    currencyunit = self.t("currency")
    
    if currencyunit == "&pound;":
      
      currencyunit = u"£"
    
    price = currencyunit + miscmethods.FormatPrice(price)
    
    return ((receiptid, date, description, price), imageid)
  
  def RefreshList(self, ID=False):
    
    if self.clientdata.ID != False:
      
      action = "SELECT receipt.Price, receipt.Date, receipt.Description FROM receipt WHERE receipt.Type = 4 AND receipt.TypeID = " + str(self.clientdata.ID) + " AND receipt.Date < \"" + self.fromdate + "\""
      
      balanceresults1 = db.SendSQL(action, self.localsettings.dbconnection)
      
      action = "SELECT receipt.Price, receipt.Date, receipt.Description FROM appointment LEFT JOIN receipt ON appointment.ID = receipt.AppointmentID WHERE appointment.OwnerID = " + str(self.clientdata.ID) + " AND receipt.Date < \"" + self.fromdate + "\""
      
      balanceresults2 = db.SendSQL(action, self.localsettings.dbconnection)
      
      balanceresults = balanceresults1 + balanceresults2
      
      balance = 0
      
      for a in balanceresults:
        
        balance = balance + a[0]
      
      action = "SELECT receipt.Date, receipt.Price, receipt.Description, receipt.ID FROM receipt WHERE receipt.Type = 4 AND receipt.TypeID = " + str(self.clientdata.ID) + " AND receipt.Date BETWEEN \"" + self.fromdate + "\" AND \"" + self.todate + "\""
      
      results1 = db.SendSQL(action, self.localsettings.dbconnection)
      
      action = "SELECT receipt.Date, receipt.Price, receipt.Description, receipt.ID FROM appointment LEFT JOIN receipt ON appointment.ID = receipt.AppointmentID WHERE appointment.OwnerID = " + str(self.clientdata.ID) + " AND receipt.Date BETWEEN \"" + self.fromdate + "\" AND \"" + self.todate + "\""
      
      results2 = db.SendSQL(action, self.localsettings.dbconnection)
      
    
    else:
      
      balance = 0
      results1 = ()
      results2 = ()
    
    results = results1 + results2
    
    results = list(results)
    
    results.sort()
    
    newresults = [(self.fromdate, balance, "Balance", 0),]
    
    for a in results:
      
      newresults.append(a)
    
    results = newresults
    
    totalprice = 0
    
    for a in results:
      totalprice = totalprice + a[1]
    
    self.totalprice = totalprice
    
    self.htmllist = results
    
    self.parent.clientpanel.billsummarypanel.GenerateBalance()
    
    ListCtrlWrapper.RefreshList(self)
  
  def GetSelection(self):
    
    listboxid = self.listctrl.GetFocusedItem()
    itemid = self.listctrl.GetItemData(listboxid)
    
    selection = -1
    
    count = 0
    
    for a in self.htmllist:
      
      if a[3] == itemid:
        
        selection = count
      
      count = count + 1
    
    return selection

class AnimalListCtrl(ListCtrlWrapper):
  
  def t(self, field, idx = 0):
    
    return  self.localsettings.t(field, idx)
  
  def __init__(self, animalpanel, clientdata):
    
    self.htmllist = []
    self.clientdata = clientdata
    self.localsettings = clientdata.localsettings
    self.parent = animalpanel
    self.clientpanel = animalpanel.GetGrandParent()
    
    columnheadings = (self.t("namelabel"), self.t("animalsexlabel"), self.t("animalspecieslabel"), self.t("agelabel"))
    
    ListCtrlWrapper.__init__(self, self.parent, self.localsettings, columnheadings, ("icons/asm.png", "icons/editanimal.png", "icons/ghost.png"))
  
  def ProcessRow(self, rowdata):
    
    name = rowdata[1]
    sex = miscmethods.GetSex(self.localsettings, rowdata[2])
    species = rowdata[3]
    age = miscmethods.GetAgeFromDOB(rowdata[7], self.localsettings)
    asmref = rowdata[6]
    
    if rowdata[8] == 1:
      
      imageid = 2
      
    elif asmref == "":
      
      imageid = 1
      
    else:
    
      imageid = 0
    
    return ((rowdata[0], name, sex, species, age), imageid)
  
  def RefreshList(self, ID=False):
    
    action = "SELECT ID, Name, Sex, Species, Colour, IsDeceased, ASMRef, DOB, IsDeceased FROM animal WHERE animal.OwnerID = " + str(self.clientdata.ID)
    
    if self.clientpanel.animalnamefilter != "":
      
      action = action + " AND Name LIKE \'%" + self.clientpanel.animalnamefilter + "%\'"
    
    action = action + " ORDER BY IsDeceased, Name"
    self.htmllist = db.SendSQL(action, self.clientdata.localsettings.dbconnection)
    
    ListCtrlWrapper.RefreshList(self)

class ASMAnimalListbox(ListCtrlWrapper):
  
  def t(self, field, idx = 0):
    
    return  self.localsettings.t(field, idx)
  
  def __init__(self, parent, localsettings):
    
    self.htmllist = []
    self.localsettings = localsettings
    self.parent = parent
    
    columnheadings = (self.t("asmreflabel"), self.t("animalnamelabel"), self.t("animalsexlabel"), self.t("animalspecieslabel"), self.t("agelabel"), self.t("animalcolourlabel"))
    
    ListCtrlWrapper.__init__(self, self.parent, self.localsettings, columnheadings, ("icons/asm.png",))
  
  def ProcessRow(self, rowdata):
    
    #count, refno, name, sex, species, dob, colour
    name = rowdata[2]
    sex = rowdata[3]
    species = rowdata[4]
    age = miscmethods.GetAgeFromDOB(miscmethods.FormatSQLDate(rowdata[5], self.localsettings), self.localsettings)
    asmref = rowdata[1]
    colour = rowdata[6]
    
    return ((rowdata[0], asmref, name, sex, species, age, colour), 0)
  
  def RefreshList(self, ID=False):
    
    busy = wx.BusyCursor()
    
    asmconnection = self.parent.asmconnection
    
    refno = self.parent.refnoentry.GetValue()
    name = self.parent.nameentry.GetValue()
    species = self.parent.speciesentry.GetValue()
    location = self.parent.locationchoice.GetSelection()
    
    action = "SELECT animal.ShelterCode, animal.AnimalName, lksex.Sex, animal.Neutered, species.SpeciesName, breed.BreedName, basecolour.BaseColour, animal.DateOfBirth, animal.IdentichipNumber, animal.HiddenAnimalDetails, animal.Archived, animal.ActiveMovementType FROM animal INNER JOIN species ON animal.SpeciesID = species.ID INNER JOIN breed ON animal.BreedID = breed.ID INNER JOIN lksex ON animal.Sex = lksex.ID INNER JOIN basecolour ON animal.BaseColourID = basecolour.ID "
    
    if location == 0:
      
      action = action + "WHERE animal.Archived = 0"
      
    else:
      
      action = action + "WHERE animal.ActiveMovementType = " + str(location)
    
    
    action = action + " AND animal.ShelterCode LIKE \"%" + refno + "%\" AND animal.AnimalName LIKE \"%" + name + "%\" AND species.SpeciesName LIKE \"%" + species + "%\" AND animal.DeceasedDate IS NULL AND animal.NonShelterAnimal = 0 ORDER BY animal.ShelterCode desc"
    results = db.SendSQL(action, asmconnection)
    
    self.parent.totallabel.SetLabel(self.t("totallabel") + ": " + str(len(results)) + " ")
    self.parent.resultssizer.Layout()
    
    self.parent.animaldata = results
    
    if len(results) > 1000:
      
      miscmethods.ShowMessage(self.t("toomanyresultsmessage"), self.notebook)
      
    else:
      count = 0
      
      self.htmllist = []
      
      for a in results:
        
        refno = a[0]
        name = a[1]
        sex = a[2]
        
        species = a[4]
        
        colour = a[6]
        dob = a[7]
        
        self.htmllist.append((count, refno, name, sex, species, dob, colour))
        
        count = count + 1
    
    del busy
    
    ListCtrlWrapper.RefreshList(self)

class ClientImportListCtrl(ListCtrlWrapper):
  
  def t(self, field, idx = 0):
    
    return  self.localsettings.t(field, idx)
  
  def __init__(self, parent, localsettings):
    
    self.htmllist = []
    self.localsettings = localsettings
    self.parent = parent
    
    columnheadings = (self.t("animalnamelabel"), self.t("clientaddresslabel"), self.t("clientpostcodelabel"))
    
    ListCtrlWrapper.__init__(self, self.parent, self.localsettings, columnheadings, ("icons/editclient.png",))
  
  def ProcessRow(self, rowdata):
    
    #count, refno, name, sex, species, dob, colour
    name = rowdata[1]
    address = rowdata[2].replace("\r", "").replace("\n", ", ")
    postcode = rowdata[3]
    
    return ((rowdata[0], name, address, postcode), 0)
  
  def RefreshList(self, ID=False):
    
    busy = wx.BusyCursor()
    
    panel = self.parent
    
    asmconnection = panel.asmconnection
    
    name = panel.nameentry.GetValue()
    address = panel.addressentry.GetValue()
    postcode = panel.postcodeentry.GetValue()
    
    action = "SELECT ID, OwnerName, OwnerAddress, OwnerPostcode, OwnerTitle, OwnerForenames, OwnerSurname, HomeTelephone, MobileTelephone, WorkTelephone, EmailAddress, Comments FROM owner WHERE OwnerName LIKE \"%" + name + "%\" AND OwnerAddress LIKE \"%" + address + "%\" AND OwnerPostcode LIKE \"%" + postcode + "%\""
    results = db.SendSQL(action, asmconnection)
    
    panel.totallabel.SetLabel(self.t("totallabel") + ": " + str(len(results)) + " ")
    panel.resultssizer.Layout()
    
    panel.clientdata = results
    
    if len(results) > 1000:
      
      miscmethods.ShowMessage(self.t("toomanyresultsmessage"), panel)
      
    else:
      
      self.htmllist = []
      
      for a in results:
        
        name = a[1]
        address = a[2]
        postcode = a[3]
        
        self.htmllist.append( (a[0], unicode(a[1], "utf8"), unicode(a[2], "utf8"), unicode(a[3], "utf8")) )
    
    del busy
    
    ListCtrlWrapper.RefreshList(self)
