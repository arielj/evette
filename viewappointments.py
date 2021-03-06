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
import wx.html
import db
import customwidgets
import appointmentmethods
import datetime
import vetmethods
import time
import clientmethods
import animalmethods
import dbmethods
import medicationmethods
import traceback

EDIT_APPOINTMENT = 700
EDIT_ANIMAL = 701
EDIT_CLIENT = 702
VET_FORM = 703
MOVE_TO_NOT_ARRIVED = 704
MOVE_TO_WAITING = 705
MOVE_TO_WITH_VET = 706
MOVE_TO_DONE = 707
DESELECT = 708
VET_NOTES = 709
PAY_BILL = 710
SHOP_SALE = 711
APPOINTMENT_TYPES = ['appointment','operation','grooming']

class ViewAppointments(wx.Panel):
  
  def t(self, field, idx = 0):
    
    return self.localsettings.t(field,idx)
  
  def __del__(self):
    self.refreshtimer.Stop()
  
  def __init__(self, notebook, localsettings, operations=0):
    
    busy = wx.BusyCursor()
    
    self.localsettings = localsettings
    
    self.operations = operations
    
    self.selectedappointmentdata = False
    
    [date, sqldate, time] = self.GetDatesAndTime()
    
    if self.operations == 2:
      self.vetlist = self.localsettings.GetGroomersByDateAndTime(sqldate,time)
      if len(self.vetlist) == 0:
        self.vetlist = self.localsettings.GetGroomersNames()

    else:
      self.vetlist = self.localsettings.GetVetsByDateAndTime(sqldate,time,operations)
      if len(self.vetlist) == 0:
        self.vetlist = self.localsettings.GetVetsNames()

    if len(self.vetlist) == 0:
      self.vetlist.append(self.t("nonelabel"))
    
    wx.Panel.__init__(self, notebook)
    
    app_type = APPOINTMENT_TYPES[self.operations]
    self.pagetitle = miscmethods.GetPageTitle(notebook, self.t("view" + app_type + "spagetitle"))
    self.pageimage = "icons/" + app_type + ".png"
    
    topsizer = wx.BoxSizer(wx.VERTICAL)

    lefttorightsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    leftsizer = wx.BoxSizer(wx.VERTICAL)
    
    datetimesizer = wx.BoxSizer(wx.HORIZONTAL)
    
    datetimewindow = wx.html.HtmlWindow(self)
    datetimesizer.Add(datetimewindow, 1, wx.EXPAND)
    
    leftsizer.Add(datetimesizer, 1, wx.EXPAND)
    
    leftspacer1 = wx.StaticText(self, -1, "", size=(-1,30))
    leftsizer.Add(leftspacer1, 0, wx.EXPAND)
    
    detailslabel = wx.StaticText(self, -1, self.t("animalappointmentdetailslabel") + ":")
    leftsizer.Add(detailslabel, 0, wx.ALIGN_LEFT)
    
    detailswindow = wx.html.HtmlWindow(self)
    leftsizer.Add(detailswindow, 1, wx.EXPAND)
    
    leftspacer2 = wx.StaticText(self, -1, "", size=(-1,30))
    leftsizer.Add(leftspacer2, 0, wx.EXPAND)
    
    next_vaccinations_label = wx.StaticText(self, -1, self.t("vaccinationssoonlabel") + ":")
    leftsizer.Add(next_vaccinations_label, 0, wx.ALIGN_LEFT)
    
    next_vaccinations_window = NextVaccinationsWindow(self)
    leftsizer.Add(next_vaccinations_window, 3, wx.EXPAND)



    lefttorightsizer.Add(leftsizer, 1, wx.EXPAND)
    
    lefttorightspacer = wx.StaticText(self, -1, "", size=(50,-1))
    lefttorightsizer.Add(lefttorightspacer, 0, wx.EXPAND)
    
    rightsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    rightleftsizer = wx.BoxSizer(wx.VERTICAL)
    
    
    waitingsizer = wx.BoxSizer(wx.VERTICAL)
    waitinglabel = wx.StaticText(self, -1, self.t("appointmentwaitinglabel") + ":")
    waitingsizer.Add(waitinglabel, 0, wx.ALIGN_LEFT)
    waitinglistbox = customwidgets.AppointmentListbox(self, localsettings, 1)
    waitinglistbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EditAppointment)
    waitingsizer.Add(waitinglistbox, 1, wx.EXPAND)
    waitingtotal = wx.StaticText(self, -1, self.t("totallabel") + ": 0")
    waitingsizer.Add(waitingtotal, 0, wx.ALIGN_RIGHT)
    rightleftsizer.Add(waitingsizer, 1, wx.EXPAND)
    
    withvetbuttonssizer = wx.BoxSizer(wx.HORIZONTAL)
    
    withvetspacer = wx.StaticText(self, -1, "")
    withvetbuttonssizer.Add(withvetspacer, 1, wx.EXPAND)
    
    downbitmap = wx.Bitmap("icons/downarrow.png")
    withvetbutton = wx.BitmapButton(self, -1, downbitmap)
    withvetbutton.SetToolTipString(self.t("viewappointmentsmarkwithvettooltip"))
    withvetbutton.Bind(wx.EVT_BUTTON, self.MarkWithVet)
    withvetbuttonssizer.Add(withvetbutton, 0, wx.EXPAND)
    
    vetcombobox = wx.ComboBox(self, -1, self.vetlist[0], choices=self.vetlist)
    vetcombobox.SetToolTipString(self.t("viewappointmentschoosevettooltip"))
    
    if localsettings.userposition == self.t("vetpositiontitle"):
      vetcombobox.SetValue(localsettings.username)
    
    
    withvetbuttonssizer.Add(vetcombobox, 2, wx.EXPAND)
    
    withvetspacer2 = wx.StaticText(self, -1, "")
    withvetbuttonssizer.Add(withvetspacer2, 1, wx.EXPAND)
    
    rightleftsizer.Add(withvetbuttonssizer, 0, wx.EXPAND)
    
    
    withvetsizer = wx.BoxSizer(wx.VERTICAL)
    withvetlabel = wx.StaticText(self, -1, self.t("appointmentwithvetlabel") + ":")
    withvetsizer.Add(withvetlabel, 0, wx.ALIGN_LEFT)
    withvetlistbox = customwidgets.AppointmentListbox(self, localsettings, 2)
    withvetlistbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EditAppointment)
    withvetsizer.Add(withvetlistbox, 1, wx.EXPAND)
    withvettotal = wx.StaticText(self, -1, self.t("totallabel") + ": 0")
    withvetsizer.Add(withvettotal, 0, wx.ALIGN_RIGHT)
    
    rightleftsizer.Add(withvetsizer, 1, wx.EXPAND)
    
    rightsizer.Add(rightleftsizer, 1, wx.EXPAND)
    
    rightmiddlesizer = wx.BoxSizer(wx.VERTICAL)
    
    middlespacer1 = wx.StaticText(self, -1, "")
    rightmiddlesizer.Add(middlespacer1, 1, wx.EXPAND)
    
    leftbitmap = wx.Bitmap("icons/leftarrow.png")
    arrivedbutton = wx.BitmapButton(self, -1, leftbitmap)
    arrivedbutton.SetToolTipString(self.t("viewappointmentsmarkarrivedtooltip"))
    arrivedbutton.Bind(wx.EVT_BUTTON, self.MarkArrived)
    rightmiddlesizer.Add(arrivedbutton, 0, wx.ALIGN_CENTER)
    
    middlespacer2 = wx.StaticText(self, -1, "")
    rightmiddlesizer.Add(middlespacer2, 2, wx.EXPAND)
    
    rightbitmap = wx.Bitmap("icons/rightarrow.png")
    donebutton = wx.BitmapButton(self, -1, rightbitmap)
    donebutton.SetToolTipString(self.t("viewappointmentsmarkdonetooltip"))
    donebutton.Bind(wx.EVT_BUTTON, self.MarkDone)
    rightmiddlesizer.Add(donebutton, 0, wx.ALIGN_CENTER)
    
    middlespacer3 = wx.StaticText(self, -1, "")
    rightmiddlesizer.Add(middlespacer3, 1, wx.EXPAND)
    
    rightsizer.Add(rightmiddlesizer, 0, wx.EXPAND)
    
    rightrightsizer = wx.BoxSizer(wx.VERTICAL)
    
    notarrivedsizer = wx.BoxSizer(wx.VERTICAL)
    notarrivedlabel = wx.StaticText(self, -1, self.t("appointmentnotarrivedlabel") + ":")
    notarrivedsizer.Add(notarrivedlabel, 0, wx.ALIGN_LEFT)
    notarrivedlistbox = customwidgets.AppointmentListbox(self, localsettings, 0)
    notarrivedlistbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EditAppointment)
    notarrivedsizer.Add(notarrivedlistbox, 1, wx.EXPAND)
    notarrivedtotal = wx.StaticText(self, -1, self.t("totallabel") + ": 0")
    notarrivedsizer.Add(notarrivedtotal, 0, wx.ALIGN_RIGHT)
    
    rightrightsizer.Add(notarrivedsizer, 1, wx.EXPAND)
    
    donespacer = wx.StaticText(self, -1, "", size=(-1,20))
    rightrightsizer.Add(donespacer, 0, wx.EXPAND)
    
    donesizer = wx.BoxSizer(wx.VERTICAL)
    donelabel = wx.StaticText(self, -1, self.t("appointmentdonelabel") + ":")
    donesizer.Add(donelabel, 0, wx.ALIGN_LEFT)
    donelistbox = customwidgets.AppointmentListbox(self, localsettings, 3)
    donelistbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EditAppointment)
    donesizer.Add(donelistbox, 1, wx.EXPAND)
    donetotal = wx.StaticText(self, -1, self.t("totallabel") + ": 0")
    donesizer.Add(donetotal, 0, wx.ALIGN_RIGHT)
    
    rightrightsizer.Add(donesizer, 1, wx.EXPAND)
    
    rightsizer.Add(rightrightsizer, 1, wx.EXPAND)
    
    lefttorightsizer.Add(rightsizer, 2, wx.EXPAND)
    
    topsizer.Add(lefttorightsizer, 1, wx.EXPAND)
    
    self.SetSizer(topsizer)
    
    self.notarrivedlistbox = notarrivedlistbox
    self.waitinglistbox = waitinglistbox
    self.withvetlistbox = withvetlistbox
    self.donelistbox = donelistbox
    self.detailswindow = detailswindow
    self.next_vaccinations_window = next_vaccinations_window
    self.notebook = notebook
    self.datetimewindow = datetimewindow
    self.vetcombobox = vetcombobox
    self.withvetbutton = withvetbutton
    self.arrivedbutton = arrivedbutton
    self.donebutton = donebutton
    self.notarrivedtotal = notarrivedtotal
    self.waitingtotal = waitingtotal
    self.withvettotal = withvettotal
    self.donetotal = donetotal
    
    self.notarrivedsizer = notarrivedsizer
    self.waitingsizer = waitingsizer
    self.withvetsizer = withvetsizer
    self.donesizer = donesizer
    
    self.UpdateViewAppointments(False)
    
    del busy
    
    timeinterval = self.localsettings.appointmentrefresh * 1000#convert from seconds
    
    self.refreshtimer = wx.Timer(self, -1)
    self.Bind(wx.EVT_TIMER, self.UpdateViewAppointments, self.refreshtimer)
    self.refreshtimer.Start(timeinterval)
      
  def MarkArrived(self, ID):
    
    busy = wx.BusyCursor()
    
    self.selectedappointmentdata.arrived = 1
    self.selectedappointmentdata.withvet = 0
    self.selectedappointmentdata.done = 0
    self.selectedappointmentdata.vet = self.vetcombobox.GetValue()
    self.selectedappointmentdata.arrivaltime = datetime.datetime.today().strftime("%X")
    self.selectedappointmentdata.Submit()
    
    self.UpdateViewAppointments(False)
    
    del busy
  
  def MarkWithVet(self, ID):
    
    busy = wx.BusyCursor()
    
    self.selectedappointmentdata.arrived = 1
    self.selectedappointmentdata.withvet = 1
    self.selectedappointmentdata.done = 0
    self.selectedappointmentdata.vet = self.vetcombobox.GetValue()
    self.selectedappointmentdata.Submit()
    
    self.UpdateViewAppointments(False)
    
    self.EditVetFormFromMenu(False)
    
    del busy
  
  def MarkDone(self, ID):
    
    busy = wx.BusyCursor()
    
    self.selectedappointmentdata.arrived = 1
    self.selectedappointmentdata.withvet = 0
    self.selectedappointmentdata.done = 1
    self.selectedappointmentdata.vet = self.vetcombobox.GetValue()
    self.selectedappointmentdata.Submit()
    
    self.UpdateViewAppointments(False)
    
    del busy
  
  def MarkNotArrived(self, ID):
    
    busy = wx.BusyCursor()
    
    self.selectedappointmentdata.arrived = 0
    self.selectedappointmentdata.withvet = 0
    self.selectedappointmentdata.done = 0
    self.selectedappointmentdata.vet = self.vetcombobox.GetValue()
    self.selectedappointmentdata.Submit()
    
    self.UpdateViewAppointments(False)
    
    del busy
  
  def AppointmentMenuPopup(self, ID):
    
    listbox = ID.GetEventObject()
    
    if listbox.GetFocusedItem() > -1 and self.selectedappointmentdata != False and listbox.GetParent().GetSelection() != -1:
      
      popupmenu = wx.Menu()
      
      popupmenu.parent = ID.GetEventObject()
      
      editappointment = wx.MenuItem(popupmenu, EDIT_APPOINTMENT, self.t("editappointmentlabel"))
      editappointment.SetBitmap(wx.Bitmap("icons/edit.png"))
      popupmenu.AppendItem(editappointment)
      wx.EVT_MENU(popupmenu, EDIT_APPOINTMENT, self.EditAppointmentFromMenu)
      
      
      editanimal = wx.MenuItem(popupmenu, EDIT_ANIMAL, self.t("editanimaltooltip"))
      editanimal.SetBitmap(wx.Bitmap("icons/editanimal.png"))
      popupmenu.AppendItem(editanimal)
      wx.EVT_MENU(popupmenu, EDIT_ANIMAL, self.EditAnimalFromMenu)
      
      
      editclient = wx.MenuItem(popupmenu, EDIT_CLIENT, self.t("viewappointmentseditclientbuttonlabel"))
      editclient.SetBitmap(wx.Bitmap("icons/editclient.png"))
      popupmenu.AppendItem(editclient)
      wx.EVT_MENU(popupmenu, EDIT_CLIENT, self.EditClientFromMenu)
      
      shopsale = wx.MenuItem(popupmenu, SHOP_SALE, self.t("shopsalemenuitem"))
      shopsale.SetBitmap(wx.Bitmap("icons/calculator.png"))
      popupmenu.AppendItem(shopsale)
      wx.EVT_MENU(popupmenu, SHOP_SALE, self.ShopSale)
      
      if self.localsettings.editfinances == 1:
        
        paybill = wx.MenuItem(popupmenu, PAY_BILL, self.t("clientpaymentlabel"))
        paybill.SetBitmap(wx.Bitmap("icons/other.png"))
        popupmenu.AppendItem(paybill)
        wx.EVT_MENU(popupmenu, PAY_BILL, self.PayBillDialog)
      
      if self.localsettings.vetform == 1 and listbox.GetParent().index == 2:
        
        popupmenu.AppendSeparator()
        
        vetform = wx.MenuItem(popupmenu, VET_FORM, self.t("vetformpagetitle"))
        vetform.SetBitmap(wx.Bitmap("icons/vetform.png"))
        popupmenu.AppendItem(vetform)
        wx.EVT_MENU(popupmenu, VET_FORM, self.EditVetFormFromMenu)
        
      elif listbox.GetParent().index == 3:
        
        popupmenu.AppendSeparator()
        
        createappointment = wx.MenuItem(popupmenu, VET_FORM, self.t("createappointmentlabel"))
        createappointment.SetBitmap(wx.Bitmap("icons/in.png"))
        popupmenu.AppendItem(createappointment)
        wx.EVT_MENU(popupmenu, VET_FORM, self.CreateAppointmentFromMenu)
        
        viewvetnotes = wx.MenuItem(popupmenu, VET_NOTES, self.t("viewvetnoteslabel"))
        viewvetnotes.SetBitmap(wx.Bitmap("icons/vetform.png"))
        popupmenu.AppendItem(viewvetnotes)
        wx.EVT_MENU(popupmenu, VET_NOTES, self.ViewVetNotes)
      
      popupmenu.AppendSeparator()
      
      notarrived = wx.MenuItem(popupmenu, MOVE_TO_NOT_ARRIVED, self.t("appointmentnotarrivedlabel"))
      notarrived.SetBitmap(wx.Bitmap("icons/submit.png"))
      popupmenu.AppendItem(notarrived)
      wx.EVT_MENU(popupmenu, MOVE_TO_NOT_ARRIVED, self.MarkNotArrived)
      
      waiting = wx.MenuItem(popupmenu, MOVE_TO_WAITING, self.t("appointmentwaitinglabel"))
      waiting.SetBitmap(wx.Bitmap("icons/submit.png"))
      popupmenu.AppendItem(waiting)
      wx.EVT_MENU(popupmenu, MOVE_TO_WAITING, self.MarkArrived)
      
      withvet = wx.MenuItem(popupmenu, MOVE_TO_WITH_VET, self.t("appointmentwithvetlabel"))
      withvet.SetBitmap(wx.Bitmap("icons/submit.png"))
      popupmenu.AppendItem(withvet)
      wx.EVT_MENU(popupmenu, MOVE_TO_WITH_VET, self.MarkWithVet)
      
      done = wx.MenuItem(popupmenu, MOVE_TO_DONE, self.t("appointmentdonelabel"))
      done.SetBitmap(wx.Bitmap("icons/submit.png"))
      popupmenu.AppendItem(done)
      wx.EVT_MENU(popupmenu, MOVE_TO_DONE, self.MarkDone)
      
      popupmenu.AppendSeparator()
      
      unselect = wx.MenuItem(popupmenu, DESELECT, self.t("deselectlabel"))
      unselect.SetBitmap(wx.Bitmap("icons/reset.png"))
      popupmenu.AppendItem(unselect)
      wx.EVT_MENU(popupmenu, DESELECT, self.DeSelectAppointment)
      
      self.PopupMenu(popupmenu)
  
  def ShopSale(self, ID):
    
    medicationmethods.ShopSale(self, self.selectedappointmentdata.clientdata.ID, self.localsettings)
    
    self.UpdateViewAppointments(False)
  
  def ViewVetNotes(self, ID):
    
    dialog = wx.Dialog(self, -1, self.t("viewvetnoteslabel"))
    
    dialogsizer = wx.BoxSizer(wx.VERTICAL)
    
    panel = wx.Panel(dialog)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    summarywindow = wx.html.HtmlWindow(panel)
    topsizer.Add(summarywindow, 1, wx.EXPAND)
    
    appointmentdetails = miscmethods.GetAppointmentDetailsHtml(self.localsettings, self.selectedappointmentdata.ID)
    
    summarywindow.SetPage(appointmentdetails)
    
    panel.SetSizer(topsizer)
    
    dialogsizer.Add(panel, 1, wx.EXPAND)
    
    dialog.SetSizer(dialogsizer)
    
    dialog.SetSize((400,400))
    
    dialog.ShowModal()
  
  def PayBillDialog(self, ID):
    
    listbox = ID.GetEventObject().parent.GetParent()
    
    listboxid = listbox.GetSelection()
    
    #balance = listbox.htmllist[listboxid][-1].replace("-", "")
    
    balance = miscmethods.GetBalance(self.selectedappointmentdata.clientdata, self.localsettings)
    
    balance = miscmethods.FormatPrice(balance).replace("-", "")
    
    dialog = wx.Dialog(self, -1, self.t("clientpaymentlabel"))
    
    dialogsizer = wx.BoxSizer(wx.VERTICAL)
    
    panel = wx.Panel(dialog)
    
    topsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    panel.paymententry = wx.TextCtrl(panel, -1, balance, size=(100,-1))
    topsizer.Add(panel.paymententry, 1, wx.EXPAND)
    
    submitbitmap = wx.Bitmap("icons/submit.png")
    submitbutton = wx.BitmapButton(panel, -1, submitbitmap)
    submitbutton.Bind(wx.EVT_BUTTON, self.SubmitPayment)
    topsizer.Add(submitbutton, 0, wx.EXPAND)
    
    panel.SetSizer(topsizer)
    
    dialogsizer.Add(panel, 1, wx.EXPAND)
    
    dialog.SetSizer(dialogsizer)
    
    dialog.Fit()
    
    dialog.ShowModal()
  
  def SubmitPayment(self, ID):
    
    panel = ID.GetEventObject().GetParent()
    
    payment = panel.paymententry.GetValue()
    
    price = miscmethods.ConvertPriceToPennies(payment)
    
    date = miscmethods.GetSQLDateFromDate(datetime.date.today())
    
    dbmethods.WriteToReceiptTable(self.localsettings.dbconnection, False, date, self.t("clientpaymentinreceiptlabel"), price, 4, self.selectedappointmentdata.clientdata.ID, 0, self.localsettings.userid)
    
    panel.GetParent().Close()
    
    self.UpdateViewAppointments(False)
    
  
  def CreateAppointmentFromMenu(self, ID):
    
    appointmentsettings = appointmentmethods.AppointmentSettings(self.localsettings, self.selectedappointmentdata.animaldata.ID, False)
    appointmentpanel = appointmentmethods.AppointmentPanel(self.notebook, appointmentsettings)
    appointmentpanel.parent = self
    wx.CallAfter(self.notebook.AddPage, appointmentpanel)
  
  def DeSelectAppointment(self, ID):
    
    self.selectedappointmentdata = False
    self.UpdateViewAppointments(False)
  
  def EditAppointmentFromMenu(self, ID):
    
    appointmentid = self.selectedappointmentdata.ID
    self.EditAppointment(appointmentid)
  
  def EditAnimalFromMenu(self, ID):
    
    
    animalpanel = animalmethods.AnimalPanel(self.notebook, self.selectedappointmentdata.animaldata)
    wx.CallAfter(self.notebook.AddPage, animalpanel)
  
  def EditClientFromMenu(self, ID):
    
    clientpanel = clientmethods.ClientPanel(self.notebook, self.selectedappointmentdata.clientdata)
    wx.CallAfter(self.notebook.AddPage, clientpanel)
  
  def EditVetFormFromMenu(self, ID):
    
    vetpanel = vetmethods.VetForm(self.notebook, self.selectedappointmentdata, self.localsettings, self)
    vetpanel.viewappointmentspanel = self
    wx.CallAfter(self.notebook.AddPage, vetpanel)
    
  def RefreshLists(self, ID=False):
  
    [date, sqldate, time_str] = self.GetDatesAndTime()
    
    label = self.GetVetsGroomersOnLabel(sqldate,time_str)
    
    self.datetimewindow.SetPage("<center><font size=2>" + date + "</font><br><font color=blue size=5><b>" + time_str + "</b></font></center><br><font size=1>" + label + "</font>")
    
    for a in (self.notarrivedlistbox, self.waitinglistbox, self.withvetlistbox, self.donelistbox):
      
      a.RefreshList()
      a.SetSelection(-1)
      
      if self.selectedappointmentdata != False:
        
        for b in range(0, len(a.htmllist)):
          
          if a.htmllist[b][0] == self.selectedappointmentdata.ID:
            
            a.SetSelection(b)
            a.ScrollToLine(b)
            self.selectedappointmentdata = appointmentmethods.AppointmentSettings(self.localsettings, False, self.selectedappointmentdata.ID)
            a.listctrl.SetFocus()
      
      label = self.t("totallabel") + ": " + str(len(a.htmllist))
      if a == self.notarrivedlistbox:
        self.notarrivedtotal.SetLabel(label)
        self.notarrivedsizer.Layout()
      elif a == self.waitinglistbox:
        self.waitingtotal.SetLabel(label)
        self.waitingsizer.Layout()
      elif a == self.withvetlistbox:
        self.withvettotal.SetLabel(label)
        self.withvetsizer.Layout()
      elif a == self.donelistbox:
        self.donetotal.SetLabel(label)
        self.donesizer.Layout()
    
    if self.notarrivedlistbox.GetSelection() > -1:
      self.withvetbutton.Disable()
      self.arrivedbutton.Enable()
      self.donebutton.Disable()
    elif self.waitinglistbox.GetSelection() > -1:
      self.withvetbutton.Enable()
      self.arrivedbutton.Disable()
      self.donebutton.Disable()
    elif self.withvetlistbox.GetSelection() > -1:
      self.withvetbutton.Disable()
      self.arrivedbutton.Disable()
      self.donebutton.Enable()
    elif self.donelistbox.GetSelection() > -1:
      self.withvetbutton.Disable()
      self.arrivedbutton.Disable()
      self.donebutton.Disable()
    else:
      self.withvetbutton.Disable()
      self.arrivedbutton.Disable()
      self.donebutton.Disable()
      self.detailswindow.SetPage("")
  
  def AppointmentSelected(self, ID=False):
    
    #print "Appointment Selected!"
    
    busy = wx.BusyCursor
    
    parent = ID.GetEventObject()
    
    listboxid = parent.GetParent().GetSelection()
    appointmentid = parent.GetParent().htmllist[listboxid][0]
    
    selectedappointmentdata = appointmentmethods.AppointmentSettings(self.localsettings, False, appointmentid)
    
    self.notarrivedlistbox.SetSelection(-1)
    self.waitinglistbox.SetSelection(-1)
    self.withvetlistbox.SetSelection(-1)
    self.donelistbox.SetSelection(-1)
    
    parent.GetParent().SetSelection(listboxid)
    
    if self.notarrivedlistbox.GetSelection() > -1:
      self.withvetbutton.Disable()
      self.arrivedbutton.Enable()
      self.donebutton.Disable()
    elif self.waitinglistbox.GetSelection() > -1:
      self.withvetbutton.Enable()
      self.arrivedbutton.Disable()
      self.donebutton.Disable()
    elif self.withvetlistbox.GetSelection() > -1:
      self.withvetbutton.Disable()
      self.arrivedbutton.Disable()
      self.donebutton.Enable()
    else:
      self.withvetbutton.Disable()
      self.arrivedbutton.Disable()
      self.donebutton.Disable()
    
    appointmenthtml = miscmethods.GetAppointmentHtml(selectedappointmentdata)
    
    self.detailswindow.SetPage(appointmenthtml)
    
    self.selectedappointmentdata = selectedappointmentdata
    
    del busy
    
    parent.GetParent().SetFocus()
  
  def EditAppointment(self, ID):
    
    try:
      
      listboxid = ID.GetEventObject().GetParent().GetSelection()
      appointmentid = ID.GetEventObject().GetParent().htmllist[listboxid][0]
      
    except:
      
      appointmentid = ID
    
    
    appointmentdata = appointmentmethods.AppointmentSettings(self.localsettings, False, appointmentid)
    appointmentpanel = appointmentmethods.AppointmentPanel(self.notebook, appointmentdata)
    appointmentpanel.viewappointmentspanel = self
    wx.CallAfter(self.notebook.AddPage, appointmentpanel)
  
  def DeleteAppointment(self, ID):
    
    appointmentid = self.selectedappointmentdata[0]
    if miscmethods.ConfirmMessage("Really delete appointment?"):
      
      action = "DELETE FROM appointment WHERE ID = " + str(appointmentid)
      db.SendSQL(action, self.localsettings.dbconnection)
      
      self.detailswindow.SetPage("")
      self.RefreshLists()
      self.editbutton.Disable()
      self.deletebutton.Disable()
    
  def VetVisit(self, ID):
    
    appointmentid = self.selectedappointmentdata.ID
    appointmentdata = appointmentmethods.AppointmentSettings(self.localsettings, False, appointmentid)
    
    self.RefreshLists()
    
    vetpanel = vetmethods.VetForm(self.notebook, appointmentdata, self.localsettings, self)
    vetpanel.viewappointmentspanel = self
    self.notebook.AddPage(vetpanel)
  
  def OpenClientRecord(self, ID):
    
    clientdata = self.selectedappointmentdata.clientdata
    
    clientpanel = clientmethods.ClientPanel(self.notebook, clientdata)
    
    clientpanel.viewappointmentspanel = self
    
    self.notebook.AddPage(clientpanel)
    
  def UpdateViewAppointments(self, event, force=False):
    [date,sqldate,timestring] = self.GetDatesAndTime()
    
    label = self.GetVetsGroomersOnLabel(sqldate,timestring)
    
    self.datetimewindow.SetPage("<center><font size=2>" + date + "</font><br><font color=blue size=5><b>" + timestring + "</b></font></center><br><font size=1>" + label + "</font>")
    
    for a in range(0, 4):
      
      index = a
    
      action = "SELECT appointment.ID, appointment.Time, animal.ID, animal.Name, client.ClientSurname, animal.Sex, animal.Neutered, animal.Species, animal.Breed, animal.Comments, client.ClientComments, appointment.AppointmentReason, animal.DOB, client.ClientTitle, appointment.Vet, client.ID, animal.ASMRef, appointment.ArrivalTime FROM appointment INNER JOIN animal ON appointment.AnimalID = animal.ID INNER JOIN client ON animal.OwnerID = client.ID WHERE appointment.Operation = " + str(self.operations) + " AND appointment.Date = \"" + sqldate + "\""
      
      if index == 0:
        
        action = action + " AND appointment.Arrived = 0"
        
      elif index == 1:
        
        action = action + " AND appointment.Arrived = 1 AND appointment.WithVet = 0 AND appointment.done = 0"
        
      elif index == 2:
        
        action = action + " AND appointment.WithVet = 1"
        
      else:
        
        action = action + " AND appointment.Done = 1"
      
      action = action + " AND appointment.Staying = 0 ORDER BY appointment.Time"

      if index == 0:
        self.notarrivedlistbox.htmllist = db.SendSQL(action, self.localsettings.dbconnection)
        
      elif index == 1:
        self.waitinglistbox.htmllist = db.SendSQL(action, self.localsettings.dbconnection)

      elif index == 2:
        self.withvetlistbox.htmllist = db.SendSQL(action, self.localsettings.dbconnection)
      else:
        results = db.SendSQL(action, self.localsettings.dbconnection)
        
        htmllist = []
        
        for b in results:
          
          clientid = b[15]
          
          clientdata = clientmethods.ClientSettings(self.localsettings, clientid)
          
          balance = miscmethods.GetBalance(clientdata, self.localsettings)
          
          #if balance < 0:
            
            #colour = "red"
            
          #else:
            
            #colour = "green"
          
          balance = miscmethods.FormatPrice(balance)
          
          #balance = "<font size=2 color=" + colour + ">&nbsp;" + self.t("currency") + balance + "</font>"
          
          listitem = list(b)
          
          listitem.append(balance)
          
          htmllist.append(listitem)
        
        self.donelistbox.htmllist = htmllist
    
    busy = wx.BusyCursor()
    
    self.RefreshLists()
    
    del busy

  def GetDatesAndTime(self):
    date = datetime.datetime.today().strftime("%A %d %B %Y").decode('utf-8')
    sqldate = datetime.datetime.today().strftime("%Y-%m-%d")
    time = datetime.datetime.today().strftime("%X")[:5]
    return [date,sqldate,time]
  
  def GetVetsGroomersOnLabel(self,sqldate,time_str):
    label = "<u>"
    if self.operations == 2:
      groomerslist = self.localsettings.GetGroomersByDateAndTime(sqldate,time_str)
      groomers = ', '.join(groomerslist)
      label += self.t("viewappointmentsgroomersonlabel") + "</u>: " + groomers.decode('utf-8')
    else:
      vetlist = self.localsettings.GetVetsByDateAndTime(sqldate,time_str,self.operations)
      vets = ', '.join(vetlist)
      label += self.t("viewappointmentsvetsonlabel") + "</u>: " + vets.decode('utf-8')
    
    return label

class NextVaccinationsWindow(customwidgets.ListCtrlWrapper):
  def t(self, field, idx = 0):
    return  self.localsettings.t(field, idx)
  
  def __init__(self, parent):
    self.htmllist = []
    self.localsettings = parent.localsettings
    self.parent = parent
    
    columnheadings = (self.t("clientlabel"), self.t("animallabel"), self.t("nextduelabel"), self.t("clientmobilephonelabel"))
    
    customwidgets.ListCtrlWrapper.__init__(self, parent, self.localsettings, columnheadings)
    
    self.RefreshList()
    
    self.listctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_activated)
  
  def RefreshList(self, ID=False):
  
    self.htmllist = dbmethods.GetNextVaccinations(self.localsettings)
  
    customwidgets.ListCtrlWrapper.RefreshList(self)
  
  def ProcessRow(self, rowdata):
    return [map(lambda x: str(x), rowdata), -1]

  def on_item_activated(self, event):
		listboxid = self.GetFocusedItem()
		clientid = self.GetItemData(listboxid)
		
		notebook = self.parent.notebook
		
		clientdata = clientmethods.ClientSettings(self.localsettings, clientid)
		clientpanel = clientmethods.ClientPanel(notebook, clientdata)
		wx.CallAfter(notebook.AddPage, clientpanel)

def UpdateMessage(ID):
  
  appointmentpanel = ID.GetEventObject().appointmentpanel
  
  #print "appointmentpanel = " + str(appointmentpanel)

