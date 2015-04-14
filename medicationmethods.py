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
import customwidgets
import db
import dbmethods
import formmethods
import datetime
import wx.lib.mixins.listctrl as listmix

ADD_MEDICATION = 1401
EDIT_MEDICATION = 1402
DELETE_MEDICATION = 1403
REFRESH_MEDICATIONS = 1404
ADD_MEDICATIONMOVEMENT = 1405
EDIT_MEDICATIONMOVEMENT = 1406
DELETE_MEDICATIONMOVEMENT = 1407
REFRESH_MEDICATIONMOVEMENTS = 1408
MEDICATION_CHANGELOG = 1409
MEDICATIONMOVEMENT_CHANGELOG = 1410
PRINT_MEDICATIONS = 1411
BATCH_BREAKDOWN = 1412

class MedicationData:
  
  def __init__(self, medicationid=False):
    
    #fields = (ID, Name, Description, Unit, BatchNo, CurrentPrice, ChangeLog)
    
    self.ID = medicationid
    self.name = u""
    self.description = u""
    self.unit = u""
    self.batchno = u""
    self.price = 0
    self.changelog = ""
    self.reorderno = 0
    self.expirydate = "0000-00-00"
    self.consumabletype = 0
    self.costprice = 0
    
  def GetSettings(self, localsettings):
    
    action = "SELECT * FROM medication WHERE ID = " + str(self.ID)
    results = db.SendSQL(action, localsettings.dbconnection)
    
    
    self.name = unicode(results[0][1], "utf8")
    self.description = unicode(results[0][2], "utf8")
    self.unit = unicode(results[0][3], "utf8")
    self.batchno = unicode(results[0][4], "utf8")
    self.price = results[0][5]
    self.changelog = results[0][6]
    self.reorderno = results[0][7]
    self.expirydate = results[0][8]
    self.consumabletype = results[0][9]
    self.costprice = results[0][10]
  
  def Submit(self, localsettings):
    
    currenttime = datetime.datetime.today().strftime("%x %X")
    userid = localsettings.userid
    
    if self.changelog == "":
      self.changelog = currenttime + "%%%" + str(userid)
    else:
      self.changelog = currenttime + "%%%" + str(userid) + "$$$" + self.changelog
    
    dbmethods.WriteToMedicationTable(localsettings.dbconnection, self)
    

class MedicationInData:
  
  def __init__(self, medicationid, medicationinid=False):
    
    #fields = (ID, MedicationID, Date, Amount, BatchNo, Expires, WhereFrom, ChangeLog)
    
    self.ID = medicationinid
    self.medicationid = medicationid
    date = datetime.date.today()
    self.date = miscmethods.GetSQLDateFromDate(date)
    self.amount = 0
    self.batchno = u""
    self.expires = miscmethods.GetSQLDateFromDate(date)
    self.wherefrom = u""
    self.changelog = u""
    
  def GetSettings(self, localsettings):
    
    action = "SELECT * FROM medicationin WHERE ID = " + str(self.ID)
    results = db.SendSQL(action, localsettings.dbconnection)
    
    
    self.medicationid = results[0][1]
    self.date = results[0][2]
    self.amount = results[0][3]
    self.batchno = unicode(results[0][4], "utf8")
    self.expires = results[0][5]
    self.wherefrom = unicode(results[0][6], "utf8")
    self.changelog = results[0][7]
  
  def Submit(self, localsettings):
    
    currenttime = datetime.datetime.today().strftime("%x %X")
    userid = localsettings.userid
    
    if self.changelog == "":
      self.changelog = currenttime + "%%%" + str(userid)
    else:
      self.changelog = currenttime + "%%%" + str(userid) + "$$$" + self.changelog
    
    dbmethods.WriteToMedicationInTable(localsettings.dbconnection, self)
    

class MedicationOutData:
  
  def __init__(self, medicationid, medicationoutid=False):
    
    #fields = (ID, MedicationID, Date, Amount, BatchNo, WhereTo, AppointmentID, ChangeLog)
    
    self.ID = medicationoutid
    self.medicationid = medicationid
    date = datetime.date.today()
    self.date = miscmethods.GetSQLDateFromDate(date)
    self.amount = 0
    self.batchno = u""
    self.whereto = u""
    self.appointmentid = 0
    self.changelog = ""
    self.nextdue = "0000-00-00"
    
  def GetSettings(self, localsettings):
    
    action = "SELECT * FROM medicationout WHERE ID = " + str(self.ID)
    results = db.SendSQL(action, localsettings.dbconnection)
    
    
    self.medicationid = results[0][1]
    self.date = results[0][2]
    self.amount = results[0][3]
    self.batchno = unicode(results[0][4], "utf8")
    self.whereto = unicode(results[0][5], "utf8")
    self.appointmentid = results[0][6]
    self.changelog = results[0][7]
    self.nextdue = results[0][8]
  
  def Submit(self, localsettings):
    
    currenttime = datetime.datetime.today().strftime("%x %X")
    userid = localsettings.userid
    
    if self.changelog == "":
      self.changelog = currenttime + "%%%" + str(userid)
    else:
      self.changelog = currenttime + "%%%" + str(userid) + "$$$" + self.changelog
    
    dbmethods.WriteToMedicationOutTable(localsettings.dbconnection, self)
    

class EditMedicationPanel(wx.Panel):
  
  def t(self, field, idx = 0):
    
    return  self.localsettings.t(field, idx)
  
  def __init__(self, notebook, localsettings):
    
    busy = wx.BusyCursor()
    
    self.localsettings = localsettings
    
    wx.Panel.__init__(self, notebook)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    self.pagetitle = miscmethods.GetPageTitle(notebook, self.t("stocklabel"))
    self.pageimage = "icons/stock.png"
    
    horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    medicationlistsizer = wx.BoxSizer(wx.VERTICAL)
    
    
    medicationsearchpanel = MedicationSearchPanel(self, localsettings)
    
    medicationlistsizer.Add(medicationsearchpanel, 0, wx.EXPAND)
    
    self.medicationlistbox = customwidgets.MedicationListbox(self, localsettings)
    self.medicationlistbox.Bind(wx.EVT_LISTBOX, self.MedicationSelected)
    self.medicationlistbox.Bind(wx.EVT_LISTBOX_DCLICK, self.EditMedication)
    self.medicationlistbox.Bind(wx.EVT_RIGHT_DOWN, self.EditMedicationPopup)
    
    #if localsettings.changelog == 1:
      #self.medicationlistbox.Bind(wx.EVT_RIGHT_DOWN, self.MedicationChangeLog)
    
    medicationlistsizer.Add(self.medicationlistbox, 1, wx.EXPAND)
    
    horizontalsizer.Add(medicationlistsizer, 2, wx.EXPAND)
    
    horizontalspacer = wx.StaticText(self, -1, "", size=(50,-1))
    horizontalsizer.Add(horizontalspacer, 0, wx.EXPAND)
    
    medicationmovementsizer = wx.BoxSizer(wx.VERTICAL)
    
    medicationmovementspanel = MedicationMovementPanel(self, localsettings)
    
    medicationmovementsizer.Add(medicationmovementspanel, 1, wx.EXPAND)
    
    horizontalsizer.Add(medicationmovementsizer, 3, wx.EXPAND)
    
    topsizer.Add(horizontalsizer, 1, wx.EXPAND)
    
    self.SetSizer(topsizer)
    
    self.medicationmovementspanel = medicationmovementspanel
    self.medicationmovementspanel.Disable()
    
    self.medicationsearchpanel = medicationsearchpanel
    
    
    self.selectedmedicationid = -1
    self.RefreshMedicationList()
    
    del busy
  
  def EditMedicationPopup(self, ID):
    
    popupmenu = wx.Menu()
    
    add = wx.MenuItem(popupmenu, ADD_MEDICATION, self.t("addlabel"))
    add.SetBitmap(wx.Bitmap("icons/new.png"))
    popupmenu.AppendItem(add)
    wx.EVT_MENU(popupmenu, ADD_MEDICATION, self.AddMedication)
    
    if self.medicationlistbox.GetSelection() > -1:
      
      edit = wx.MenuItem(popupmenu, EDIT_MEDICATION, self.t("editlabel"))
      edit.SetBitmap(wx.Bitmap("icons/edit.png"))
      popupmenu.AppendItem(edit)
      wx.EVT_MENU(popupmenu, EDIT_MEDICATION, self.EditMedication)
      
      delete = wx.MenuItem(popupmenu, DELETE_MEDICATION, self.t("deletelabel"))
      delete.SetBitmap(wx.Bitmap("icons/delete.png"))
      popupmenu.AppendItem(delete)
      wx.EVT_MENU(popupmenu, DELETE_MEDICATION, self.DeleteMedication)
      
      if self.localsettings.changelog == 1:
        
        changelog = wx.MenuItem(popupmenu, MEDICATION_CHANGELOG, self.t("changelog"))
        changelog.SetBitmap(wx.Bitmap("icons/log.png"))
        popupmenu.AppendItem(changelog)
        wx.EVT_MENU(popupmenu, MEDICATION_CHANGELOG, self.MedicationChangeLog)
      
      batchbreakdown = wx.MenuItem(popupmenu, BATCH_BREAKDOWN, self.t("batchbreakdownlabel"))
      batchbreakdown.SetBitmap(wx.Bitmap("icons/form.png"))
      popupmenu.AppendItem(batchbreakdown)
      wx.EVT_MENU(popupmenu, BATCH_BREAKDOWN, self.BatchBreakdownDialog)
    
    popupmenu.AppendSeparator()
    
    printmedications = wx.MenuItem(popupmenu, PRINT_MEDICATIONS, self.t("printtooltip"))
    printmedications.SetBitmap(wx.Bitmap("icons/printer.png"))
    popupmenu.AppendItem(printmedications)
    wx.EVT_MENU(popupmenu, PRINT_MEDICATIONS, self.PrintStockList)
    
    refresh = wx.MenuItem(popupmenu, REFRESH_MEDICATIONS, self.t("refreshlabel"))
    refresh.SetBitmap(wx.Bitmap("icons/refresh.png"))
    popupmenu.AppendItem(refresh)
    wx.EVT_MENU(popupmenu, REFRESH_MEDICATIONS, self.RefreshMedicationList)
    
    self.PopupMenu(popupmenu)
  
  def BatchBreakdownDialog(self, ID):
    
    listboxid = self.medicationlistbox.GetSelection()
    medicationlistboxdata = self.medicationlistbox.htmllist[listboxid]
    
    batchinfo = medicationlistboxdata[12]
    
    miscmethods.ShowMessage(batchinfo, self)
  
  def AddMedication(self, ID):
    
    medicationdata = {}
    
    medicationdata["medicationid"] = -1
    medicationdata["name"] = ""
    medicationdata["unit"] = ""
    medicationdata["description"] = ""
    medicationdata["minimum"] = "0"
    medicationdata["currentbatch"] = ""
    medicationdata["expires"] = ""
    medicationdata["unitprice"] = "0.00"
    medicationdata["costprice"] = "0.00"
    
    if self.medicationsearchpanel.medicationradio.GetValue() == True:
      
      medicationdata["type"] = 0
      
    elif self.medicationsearchpanel.vaccinationradio.GetValue() == True:
      
      medicationdata["type"] = 1
      
    elif self.medicationsearchpanel.consumableradio.GetValue() == True:
      
      medicationdata["type"] = 2
      
    elif self.medicationsearchpanel.shopradio.GetValue() == True:
      
      medicationdata["type"] = 3
      
    elif self.medicationsearchpanel.chipradio.GetValue() == True:
      
      medicationdata["type"] = 4
    else:
      
      medicationdata["type"] = 0
    
    self.EditMedicationDialog(medicationdata)
  
  def EditMedication(self, ID):
    
    listboxid = self.medicationlistbox.GetSelection()
    medicationlistboxdata = self.medicationlistbox.htmllist[listboxid]
    
    medicationdata = {}
    
    medicationdata["medicationid"] = medicationlistboxdata[0]
    medicationdata["name"] = medicationlistboxdata[1]
    medicationdata["unit"] = medicationlistboxdata[3]
    medicationdata["description"] = medicationlistboxdata[2]
    medicationdata["minimum"] = str(medicationlistboxdata[7])
    medicationdata["currentbatch"] = medicationlistboxdata[4]
    
    expires = medicationlistboxdata[8]
    
    
    if expires == None:
      
      expires = ""
      
    else:
      
      expires = miscmethods.GetWXDateFromSQLDate(expires)
    
    medicationdata["expires"] = expires
    
    medicationdata["unitprice"] = miscmethods.FormatPrice(medicationlistboxdata[5])
    medicationdata["type"] = medicationlistboxdata[9]
    medicationdata["costprice"] = miscmethods.FormatPrice(medicationlistboxdata[10])
    
    self.EditMedicationDialog(medicationdata)
  
  def EditMedicationDialog(self, medicationdata):
    
    dialog = wx.Dialog(self, -1, self.t("medicationeditconsumable"))
    
    dialogsizer = wx.BoxSizer(wx.VERTICAL)
    
    panel = wx.Panel(dialog)
    
    panel.medicationid = medicationdata["medicationid"]
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    medicationentrysizer1 = wx.BoxSizer(wx.HORIZONTAL)
    
    namesizer = wx.BoxSizer(wx.VERTICAL)
    namelabel = wx.StaticText(panel, -1, self.t("namelabel"))
    font = namelabel.GetFont()
    font.SetPointSize(font.GetPointSize() - 2)
    namelabel.SetFont(font)
    namesizer.Add(namelabel, 0, wx.ALIGN_LEFT)
    nameentry = wx.TextCtrl(panel, -1, medicationdata["name"])
    namesizer.Add(nameentry, 1, wx.EXPAND)
    medicationentrysizer1.Add(namesizer, 2, wx.EXPAND)
    
    namespacer = wx.StaticText(panel, -1, "", size=(10,-1))
    medicationentrysizer1.Add(namespacer, 0, wx.EXPAND)
    
    unitsizer = wx.BoxSizer(wx.VERTICAL)
    unitlabel = wx.StaticText(panel, -1, self.t("unitlabel") + ":")
    unitlabel.SetFont(font)
    unitsizer.Add(unitlabel, 0, wx.ALIGN_LEFT)
    unitentry = wx.TextCtrl(panel, -1, medicationdata["unit"])
    unitsizer.Add(unitentry, 1, wx.EXPAND)
    medicationentrysizer1.Add(unitsizer, 1, wx.EXPAND)
    
    medicationentrysizer2 = wx.BoxSizer(wx.HORIZONTAL)
    
    descriptionsizer = wx.BoxSizer(wx.VERTICAL)
    descriptionlabel = wx.StaticText(panel, -1, self.t("descriptionlabel"))
    descriptionlabel.SetFont(font)
    descriptionsizer.Add(descriptionlabel, 0, wx.ALIGN_LEFT)
    descriptionentry = wx.TextCtrl(panel, -1, medicationdata["description"])
    descriptionsizer.Add(descriptionentry, 0, wx.EXPAND)
    
    medicationentrysizer2.Add(descriptionsizer, 1, wx.EXPAND)
    
    medicationentrysizer2.Add(wx.StaticText(panel, -1, "", size=(10,-1)), 0, wx.EXPAND)
    
    reordersizer = wx.BoxSizer(wx.VERTICAL)
    reorderlabel = wx.StaticText(panel, -1, self.t("reorderlabel"))
    reorderlabel.SetFont(font)
    reordersizer.Add(reorderlabel, 0, wx.ALIGN_LEFT)
    reorderentry = wx.TextCtrl(panel, -1, medicationdata["minimum"])
    reordersizer.Add(reorderentry, 0, wx.EXPAND)
    
    medicationentrysizer2.Add(reordersizer, 0, wx.EXPAND)
    
    medicationentrysizer3 = wx.BoxSizer(wx.HORIZONTAL)
    
    batchnosizer = wx.BoxSizer(wx.VERTICAL)
    batchnolabel = wx.StaticText(panel, -1, self.t("medicationcurrentbatchlabel"))
    batchnolabel.SetFont(font)
    batchnosizer.Add(batchnolabel, 0, wx.ALIGN_LEFT)
    batchnoentry = wx.TextCtrl(panel, -1, medicationdata["currentbatch"])
    batchnosizer.Add(batchnoentry, 1, wx.EXPAND)
    medicationentrysizer3.Add(batchnosizer, 1, wx.EXPAND)
    
    medicationentrysizer3.Add(wx.StaticText(panel, -1, "", size=(10,-1)), 0, wx.EXPAND)
    
    expirysizer = wx.BoxSizer(wx.VERTICAL)
    expirylabel = wx.StaticText(panel, -1, self.t("medicationexpireslabel"))
    expirylabel.SetFont(font)
    expirysizer.Add(expirylabel, 0, wx.ALIGN_LEFT)
    expiryentry = customwidgets.DateCtrl(panel, self.localsettings)
    
    if str(medicationdata["expires"]) == "":
      
      expiryentry.Clear()
      
    else:
      
      expiryentry.SetValue(medicationdata["expires"])
    
    expirysizer.Add(expiryentry, 1, wx.EXPAND)
    medicationentrysizer3.Add(expirysizer, 1, wx.EXPAND)
    
    medicationentrysizer3.Add(wx.StaticText(panel, -1, "", size=(10,-1)), 0, wx.EXPAND)
    
    costpricesizer = wx.BoxSizer(wx.VERTICAL)
    costpricelabel = wx.StaticText(panel, -1, self.t("costpricelabel"))
    costpricelabel.SetFont(font)
    costpricesizer.Add(costpricelabel, 0, wx.ALIGN_LEFT)
    costpriceentry = wx.TextCtrl(panel, -1, medicationdata["costprice"])
    costpriceentry.SetToolTipString(self.t("costpricentrytooltip"))
    costpriceentry.Bind(wx.EVT_CHAR, self.CalculateCostPrice)
    costpricesizer.Add(costpriceentry, 1, wx.EXPAND)
    medicationentrysizer3.Add(costpricesizer, 1, wx.EXPAND)
    
    medicationentrysizer3.Add(wx.StaticText(panel, -1, "", size=(10,-1)), 0, wx.EXPAND)
    
    pricesizer = wx.BoxSizer(wx.VERTICAL)
    pricelabel = wx.StaticText(panel, -1, self.t("medicationunitpricelabel"))
    pricelabel.SetFont(font)
    pricesizer.Add(pricelabel, 0, wx.ALIGN_LEFT)
    priceentry = wx.TextCtrl(panel, -1, medicationdata["unitprice"])
    priceentry.SetToolTipString(self.t("unitpricentrytooltip"))
    priceentry.Bind(wx.EVT_CHAR, self.UnitPriceEntryKeyPress)
    pricesizer.Add(priceentry, 1, wx.EXPAND)
    medicationentrysizer3.Add(pricesizer, 1, wx.EXPAND)
    
    submitspacer = wx.StaticText(panel, -1, "", size=(10,-1))
    medicationentrysizer3.Add(submitspacer, 0, wx.EXPAND)
    
    submitbitmap = wx.Bitmap("icons/submit.png")
    submitmedicationbutton = wx.BitmapButton(panel, -1, submitbitmap)
    submitmedicationbutton.Bind(wx.EVT_BUTTON, self.SubmitConsumable)
    submitmedicationbutton.SetToolTipString(self.t("submitlabel"))
    medicationentrysizer3.Add(submitmedicationbutton, 0, wx.ALIGN_BOTTOM)
    
    medicationentrysizer4 = wx.GridSizer(cols=3)
    
    medicationradio = wx.RadioButton(panel, -1, self.t("randomdatamedicationlabel"), style = wx.RB_GROUP)
    medicationradio.SetFont(font)
    medicationentrysizer4.Add(medicationradio, 0, wx.EXPAND)
    
    vaccinationradio = wx.RadioButton(panel, -1, self.t("vaccinationsvaccinelabel"))
    vaccinationradio.SetFont(font)
    medicationentrysizer4.Add(vaccinationradio, 0, wx.EXPAND)
    
    consumableradio = wx.RadioButton(panel, -1, self.t("consumablelabel"))
    consumableradio.SetFont(font)
    medicationentrysizer4.Add(consumableradio, 0, wx.EXPAND)
    
    shopradio = wx.RadioButton(panel, -1, self.t("shoplabel"))
    shopradio.SetFont(font)
    medicationentrysizer4.Add(shopradio, 0, wx.EXPAND)
    
    chipradio = wx.RadioButton(panel, -1, self.t("microchiplabel"))
    chipradio.SetFont(font)
    medicationentrysizer4.Add(chipradio, 0, wx.EXPAND)
    
    if medicationdata["type"] == 0:
      
      medicationradio.SetValue(True)
      
    elif medicationdata["type"] == 1:
      
      vaccinationradio.SetValue(True)
      
    elif medicationdata["type"] == 2:
      
      consumableradio.SetValue(True)
      
    elif medicationdata["type"] == 3:
      
      shopradio.SetValue(True)
      
    else:
      
      chipradio.SetValue(True)
    
    topsizer.Add(medicationentrysizer1, 0, wx.EXPAND)
    topsizer.Add(medicationentrysizer2, 0, wx.EXPAND)
    topsizer.Add(medicationentrysizer3, 0, wx.EXPAND)
    topsizer.Add(wx.StaticText(panel, -1, "", size=(-1,10)), 0, wx.EXPAND)
    topsizer.Add(medicationentrysizer4, 0, wx.ALIGN_CENTER_HORIZONTAL)
    
    medicationlistspacer = wx.StaticText(panel, -1, "", size=(-1,10))
    topsizer.Add(medicationlistspacer, 0, wx.EXPAND)
    
    panel.SetSizer(topsizer)
    
    panel.nameentry = nameentry
    panel.descriptionentry = descriptionentry
    panel.unitentry = unitentry
    panel.priceentry = priceentry
    panel.costpriceentry = costpriceentry
    panel.batchnoentry = batchnoentry
    panel.reorderentry = reorderentry
    panel.expiryentry = expiryentry
    panel.medicationradio = medicationradio
    panel.vaccinationradio = vaccinationradio
    panel.consumableradio = consumableradio
    panel.shopradio = shopradio
    panel.chipradio = chipradio
    
    dialogsizer.Add(panel, 1, wx.EXPAND)
    
    dialog.SetSizer(dialogsizer)
    
    dialog.Fit()
    
    dialog.ShowModal()
  
  def CalculateCostPrice(self, ID):
    
    keycode = ID.GetKeyCode()
    
    parentpanel = ID.GetEventObject().GetParent()
    
    if keycode == 99:
      
      dialog = wx.Dialog(self, -1, self.t("calculatecostpricetitle"))
      
      dialogsizer = wx.BoxSizer(wx.VERTICAL)
      
      panel = wx.Panel(dialog)
      
      topsizer = wx.BoxSizer(wx.VERTICAL)
      
      gridsizer = wx.FlexGridSizer(cols=2)
      gridsizer.AddGrowableCol(1)
      
      packpricelabel = wx.StaticText(panel, -1, self.t("packpricelabel"))
      gridsizer.Add(packpricelabel, 0, wx.ALIGN_RIGHT)
      
      packpriceentry = wx.TextCtrl(panel, -1, "0.00")
      packpriceentry.Bind(wx.EVT_TEXT, self.CalculateCostPriceKeyPress)
      gridsizer.Add(packpriceentry, 1, wx.EXPAND)
      
      unitsperpacklabel = wx.StaticText(panel, -1, self.t("unitsperpacklabel"))
      gridsizer.Add(unitsperpacklabel, 0, wx.ALIGN_RIGHT)
      
      unitsperpackentry = wx.TextCtrl(panel, -1, "0")
      unitsperpackentry.Bind(wx.EVT_TEXT, self.CalculateCostPriceKeyPress)
      gridsizer.Add(unitsperpackentry, 1, wx.EXPAND)
      
      unitpricelabel = wx.StaticText(panel, -1, self.t("medicationunitpricelabel"))
      gridsizer.Add(unitpricelabel, 0, wx.ALIGN_RIGHT)
      
      unitpriceentry = wx.TextCtrl(panel, -1, "0.00", style=wx.TE_READONLY)
      gridsizer.Add(unitpriceentry, 1, wx.EXPAND)
      
      gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
      
      submitbitmap = wx.Bitmap("icons/submit.png")
      submitbutton = wx.BitmapButton(panel, -1, submitbitmap)
      submitbutton.SetToolTipString(self.t("submitlabel"))
      submitbutton.Bind(wx.EVT_BUTTON, self.CalculateCostPriceSubmit)
      gridsizer.Add(submitbutton, 0, wx.ALIGN_LEFT)
      
      topsizer.Add(gridsizer, 1, wx.EXPAND)
      
      panel.SetSizer(topsizer)
      
      dialogsizer.Add(panel, 1, wx.EXPAND)
      
      dialog.SetSizer(dialogsizer)
      
      #dialog.SetSize((300,200))
      dialog.Fit()
      
      panel.packpriceentry = packpriceentry
      panel.unitsperpackentry = unitsperpackentry
      panel.unitpriceentry = unitpriceentry
      panel.submitbutton = submitbutton
      panel.parentpanel = parentpanel
      
      packpriceentry.SetFocus()
      
      dialog.ShowModal()
      
    else:
      
      ID.Skip()
  
  def CalculateCostPriceSubmit(self, ID):
    
    panel = ID.GetEventObject().GetParent()
    
    unitprice = panel.unitpriceentry.GetValue()
    
    panel.parentpanel.costpriceentry.SetValue(unitprice)
    
    panel.GetParent().Close()
  
  def CalculateCostPriceKeyPress(self, ID):
    
    panel = ID.GetEventObject().GetParent()
    
    success = True
    
    try:
      
      packprice = float(panel.packpriceentry.GetValue())
      
    except:
      
      success = False
    
    try:
      
      unitsperpack = int(panel.unitsperpackentry.GetValue())
      
      if unitsperpack == 0:
        
        success = False
      
    except:
      
      success = False
    
    if success == True:
      
      packprice = miscmethods.ConvertPriceToPennies(panel.packpriceentry.GetValue(), True)
      
      unitprice = float(packprice) / float(unitsperpack)
      
      unitprice = miscmethods.FormatPrice(int(unitprice))
      
      panel.unitpriceentry.SetValue(str(unitprice))
      
      panel.submitbutton.Enable()
      
    else:
      
      panel.submitbutton.Disable()
  
  def UnitPriceEntryKeyPress(self, ID):
    
    keycode = ID.GetKeyCode()
    
    panel = ID.GetEventObject().GetParent()
    
    if keycode == 97:
      
      costprice = miscmethods.ConvertPriceToPennies(panel.costpriceentry.GetValue())
      multiplyby = float(self.localsettings.markupmultiplyby)
      roundto = int(self.localsettings.markuproundto)
      
      unitprice = int(costprice * multiplyby)
      
      while unitprice % roundto > 0:
        
        unitprice = unitprice + 1
      
      unitprice = miscmethods.FormatPrice(unitprice)
      
      panel.priceentry.SetValue(unitprice)
      
    else:
      
      ID.Skip()
  
  def MedicationChangeLog(self, ID):
    
    if self.selectedmedicationid > -1:
      
      action = "SELECT ChangeLog, Name FROM medication WHERE ID = " + str(self.selectedmedicationid)
      results = db.SendSQL(action, self.localsettings.dbconnection)
      
      changelog = results[0][0]
      
      medicationname = results[0][1]
      
      miscmethods.ShowChangeLog(medicationname, changelog, self.localsettings.dbconnection)
  
  def MedicationSelected(self, ID=False):
    
    listboxid = self.medicationlistbox.GetSelection()
    
    if listboxid > -1:
      
      medicationdata = self.medicationlistbox.htmllist[listboxid]
      
      medicationid = medicationdata[0]
      name = unicode(medicationdata[1], "utf8")
      description = unicode(medicationdata[2], "utf8")
      unit = unicode(medicationdata[3], "utf8")
      batchno = unicode(medicationdata[4], "utf8")
      price = medicationdata[5]
      price = miscmethods.FormatPrice(price)
      reorderno = str(medicationdata[7])
      expirydate = medicationdata[8]
      
      self.selectedmedicationid = medicationdata[0]
      
      newmovementlabel = miscmethods.NoWrap(self.t("medicationmovementsoflabel") + name)
      
      self.medicationmovementspanel.movementlabel.SetLabel(newmovementlabel)
      self.medicationmovementspanel.ClearMovementEntries()
      #self.medicationmovementspanel.unitlabel.SetLabel(" x " + unit + " ")
      #self.medicationmovementspanel.movementbuttonssizer1.Layout()
      
      self.medicationmovementspanel.medicationid = medicationid
      self.medicationmovementspanel.RefreshList()
      
      #self.deletemedicationbutton.Enable()
      #self.editmedicationbutton.Enable()
      #self.batchinfobutton.Enable()
      self.medicationmovementspanel.Enable()
  
  def DeleteMedication(self, ID):
    
    listboxid = self.medicationlistbox.GetSelection()
    medicationid = self.medicationlistbox.htmllist[listboxid][0]
    medicationname = unicode(self.medicationlistbox.htmllist[listboxid][1], "utf8")
    
    if miscmethods.ConfirmMessage(self.t("medicationconfirmdeletemessage") + medicationname + "?"):
      
      action = "DELETE FROM medication WHERE ID = " + str(medicationid)
      db.SendSQL(action, self.localsettings.dbconnection)
      
      self.ClearMedicationEntries()
      self.selectedmedicationid = -1
      self.RefreshMedicationList()
  
  def SubmitConsumable(self, ID):
    
    parent = ID.GetEventObject().GetParent()
    
    success = True
    
    if parent.medicationid > -1:
      
      medicationdata = MedicationData(self.selectedmedicationid)
      medicationdata.GetSettings(self.localsettings)
      
    else:
      medicationdata = MedicationData()
    
    medicationdata.name = parent.nameentry.GetValue()
    medicationdata.description = parent.descriptionentry.GetValue()
    medicationdata.unit = parent.unitentry.GetValue()
    try:
      val = int(parent.reorderentry.GetValue())
      medicationdata.reorderno = val if val >= 0 else 0
    except:
      medicationdata.reorderno = "0"
    
    expiry = parent.expiryentry.GetValue()
    
    if str(expiry) == "":
      medicationdata.expirydate = ""
    else:
      medicationdata.expirydate = miscmethods.GetSQLDateFromWXDate(expiry)
    
    price = parent.priceentry.GetValue()
    medicationdata.price = miscmethods.ConvertPriceToPennies(price)
    
    costprice = parent.costpriceentry.GetValue()
    medicationdata.costprice = miscmethods.ConvertPriceToPennies(costprice)
    
    medicationdata.batchno = parent.batchnoentry.GetValue()
    
    
    if parent.medicationradio.GetValue() == True:
      
      medicationdata.consumabletype = 0
      
    elif parent.vaccinationradio.GetValue() == True:
      
      medicationdata.consumabletype = 1
      
    elif parent.consumableradio.GetValue() == True:
      
      medicationdata.consumabletype = 2
      
    elif parent.shopradio.GetValue() == True:
      
      medicationdata.consumabletype = 3
    else:
      
      medicationdata.consumabletype = 4
    
    
    if medicationdata.price is not False and medicationdata.price >= 0:
      
      medicationdata.Submit(self.localsettings)
    
    self.selectedmedicationid = medicationdata.ID
    
    self.RefreshMedicationList()
    
    parent.GetParent().Close()
    
    self.MedicationSelected()
  
  def ClearMedicationEntries(self, ID=False):
    
    self.selectedmedicationid = -1
    self.medicationmovementspanel.medicationid = -1
    self.medicationlistbox.SetSelection(-1)
    self.medicationmovementspanel.ClearMovementEntries()
    #self.deletemedicationbutton.Disable()
    self.medicationmovementspanel.Disable()
  
  def RefreshMedicationList(self, ID=False):
    
    self.medicationlistbox.RefreshList()
  
  def PrintStockList(self, ID):
    
    if len(self.medicationlistbox.htmllist) > 0:
      
      output = "<table align=center border=1>"
      
      for n in self.medicationlistbox.htmllist:
        
        medicationid = n[0]
        name = n[1]
        description = n[2]
        unit = n[3]
        batchno = n[4]
        price = n[5]
        price = miscmethods.FormatPrice(price)
        balance = n[11]
        batchdata = n[12]
        
        batchhtml = ""
        
        for p in batchdata.split("\n"):
          
          if p != "":
            
            if int(p.split(" ")[-1]) > 0:
              
              colour = "blue"
              
            else:
              
              colour = "red"
            
            batchhtml = batchhtml + "<br><font color=" + colour + " size=1>" + p + "&nbsp;</font>"
        
        output = output + "<tr><td valign=top><font size=2 color=blue>" + str(name) + "</font>&nbsp;<font size=1>(" + self.t("currency") + str(price) + " x " + str(unit) + ")</font><br><font color=red size=1>" + str(description) + "</font></td><td align=right valign=top nowrap>" + balance + "</font>" + batchhtml + "</td></tr>"
      
      output = output + "</table>"
      
      formmethods.BuildForm(self.localsettings, output)

class MedicationMovementPanel(wx.Panel):
  
  def t(self, field, idx = 0):
    
    return  self.localsettings.t(field,idx)
  
  def __init__(self, parent, localsettings):
    
    self.localsettings = localsettings
    
    wx.Panel.__init__(self, parent)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    topsizer.Add(wx.Panel(self, size=(-1,10)), 0, wx.EXPAND)
    
    movementlabel = wx.StaticText(self, -1, self.t("medicationmovementsoflabel"))
    topsizer.Add(movementlabel, 0, wx.ALIGN_LEFT)
    
    topsizer.Add(wx.Panel(self, size=(-1,10)), 0, wx.EXPAND)
    
    buttonssizer = wx.BoxSizer(wx.HORIZONTAL)
    
    #addbitmap = wx.Bitmap("icons/new.png")
    #addbutton = wx.BitmapButton(self, -1, addbitmap)
    #addbutton.Bind(wx.EVT_BUTTON, self.CreateMovement)
    #addbutton.SetToolTipString(self.t("createmovementlabel"))
    #buttonssizer.Add(addbutton, 0, wx.EXPAND)
    
    #editbitmap = wx.Bitmap("icons/edit.png")
    #editbutton = wx.BitmapButton(self, -1, editbitmap)
    #editbutton.Disable()
    #editbutton.Bind(wx.EVT_BUTTON, self.EditMovement)
    #editbutton.SetToolTipString(self.t("editmovementlabel"))
    #buttonssizer.Add(editbutton, 0, wx.EXPAND)
    
    #deletebitmap = wx.Bitmap("icons/delete.png")
    #deletebutton = wx.BitmapButton(self, -1, deletebitmap)
    #deletebutton.Disable()
    #deletebutton.Bind(wx.EVT_BUTTON, self.DeleteMovement)
    #deletebutton.SetToolTipString(self.t("medicationdeletemovementtooltip"))
    #buttonssizer.Add(deletebutton, 0, wx.EXPAND)
    
    buttonssizer.Add(wx.Panel(self), 1, wx.EXPAND)
    
    datesizer = wx.BoxSizer(wx.HORIZONTAL)
    
    fromlabel = wx.StaticText(self, -1, self.t("fromlabel") + u"\xa0")
    datesizer.Add(fromlabel, 0, wx.ALIGN_CENTER)
    
    fromdateentry = customwidgets.DateCtrl(self, self.localsettings)
    
    for a in range(0, 6):
      
      fromdateentry.SubtractMonth()
    
    datesizer.Add(fromdateentry, 0, wx.EXPAND)
    
    tolabel = wx.StaticText(self, -1, u"\xa0" + self.t("tolabel").lower() + u"\xa0")
    datesizer.Add(tolabel, 0, wx.ALIGN_CENTER)
    
    todateentry = customwidgets.DateCtrl(self, self.localsettings)
    datesizer.Add(todateentry, 0, wx.EXPAND)
    
    buttonssizer.Add(datesizer, 0, wx.EXPAND)
    
    buttonssizer.Add(wx.Panel(self), 1, wx.EXPAND)
    
    refreshbitmap = wx.Bitmap("icons/refresh.png")
    refreshbutton = wx.BitmapButton(self, -1, refreshbitmap)
    refreshbutton.Bind(wx.EVT_BUTTON, self.RefreshList)
    refreshbutton.SetToolTipString(self.t("movementrefreshmovementsmessage"))
    buttonssizer.Add(refreshbutton, 0, wx.EXPAND)
    
    topsizer.Add(buttonssizer, 0, wx.EXPAND)
    
    topsizer.Add(wx.Panel(self, size=(-1,10)), 0, wx.EXPAND)
    
    medicationmovementlist = customwidgets.MedicationMovementListBox(self, localsettings)
    medicationmovementlist.Bind(wx.EVT_LISTBOX, self.MovementSelected)
    medicationmovementlist.Bind(wx.EVT_LISTBOX_DCLICK, self.EditMovement)
    medicationmovementlist.Bind(wx.EVT_RIGHT_DOWN, self.MedicationMovementPopup)
    
    #if localsettings.changelog == 1:
      #medicationmovementlist.Bind(wx.EVT_RIGHT_DOWN, self.MovementChangeLog)
    
    topsizer.Add(medicationmovementlist, 1, wx.EXPAND)
    
    totallabel = wx.StaticText(self, -1, self.t("totallabel") + ": 0")
    topsizer.Add(totallabel, 0, wx.ALIGN_RIGHT)
    
    self.SetSizer(topsizer)
    
    self.medicationmovementlist = medicationmovementlist
    
    self.movementlabel = movementlabel
    
    self.topsizer = topsizer
    self.totallabel = totallabel
    self.parent = parent
    
    #self.addbutton = addbutton
    #self.editbutton = editbutton
    #self.deletebutton = deletebutton
    
    self.fromdateentry = fromdateentry
    self.todateentry = todateentry
    
    self.medicationid = -1
  
  def MedicationMovementPopup(self, ID):
    
    popupmenu = wx.Menu()
    
    add = wx.MenuItem(popupmenu, ADD_MEDICATIONMOVEMENT, self.t("addlabel"))
    add.SetBitmap(wx.Bitmap("icons/new.png"))
    popupmenu.AppendItem(add)
    wx.EVT_MENU(popupmenu, ADD_MEDICATIONMOVEMENT, self.CreateMovement)
    
    listboxid = self.medicationmovementlist.GetSelection()
    movementdetails = self.medicationmovementlist.htmllist[listboxid]
    
    if movementdetails[6] != self.t("clientbalancelabel"):
      
      edit = wx.MenuItem(popupmenu, EDIT_MEDICATIONMOVEMENT, self.t("editlabel"))
      edit.SetBitmap(wx.Bitmap("icons/edit.png"))
      popupmenu.AppendItem(edit)
      wx.EVT_MENU(popupmenu, EDIT_MEDICATIONMOVEMENT, self.EditMovement)
      
      delete = wx.MenuItem(popupmenu, DELETE_MEDICATIONMOVEMENT, self.t("deletelabel"))
      delete.SetBitmap(wx.Bitmap("icons/delete.png"))
      popupmenu.AppendItem(delete)
      wx.EVT_MENU(popupmenu, DELETE_MEDICATIONMOVEMENT, self.DeleteMovement)
      
      if self.localsettings.changelog == 1:
        
        changelog = wx.MenuItem(popupmenu, MEDICATIONMOVEMENT_CHANGELOG, self.t("changelog"))
        changelog.SetBitmap(wx.Bitmap("icons/log.png"))
        popupmenu.AppendItem(changelog)
        wx.EVT_MENU(popupmenu, MEDICATIONMOVEMENT_CHANGELOG, self.MovementChangeLog)
    
    popupmenu.AppendSeparator()
    
    refresh = wx.MenuItem(popupmenu, REFRESH_MEDICATIONMOVEMENTS, self.t("refreshlabel"))
    refresh.SetBitmap(wx.Bitmap("icons/refresh.png"))
    popupmenu.AppendItem(refresh)
    wx.EVT_MENU(popupmenu, REFRESH_MEDICATIONMOVEMENTS, self.RefreshList)
    
    self.PopupMenu(popupmenu)
  
  def CreateMovement(self, ID):
    
    listboxid = self.medicationmovementlist.GetSelection()
    
    medicationid = self.parent.selectedmedicationid
    
    action = "SELECT BatchNo FROM medication WHERE ID = " + str(medicationid)
    batchno = db.SendSQL(action, self.localsettings.dbconnection)[0][0]
    
    movementdetails = ( batchno, )
    
    self.EditMovementDialog(movementdetails)
    
  def EditMovement(self, ID):
    
    listboxid = self.medicationmovementlist.GetSelection()
    
    movementdetails = self.medicationmovementlist.htmllist[listboxid]
    
    if movementdetails[6] != self.t("clientbalancelabel"):
      
      self.EditMovementDialog(movementdetails)
  
  def EditMovementDialog(self, movementdetails=False):
    
    #print "movementdetails = " + str(movementdetails)
    
    if len(movementdetails) > 1:
      
      movementid = movementdetails[1]
      
      quantity = movementdetails[3]
      
      date = movementdetails[0]
      date = miscmethods.GetWXDateFromSQLDate(date)
      
      unit = unicode(movementdetails[8], "utf8")
      
      batchno = unicode(movementdetails[4], "utf8").replace(self.t("medicationbatchnolabel"), "")
      
      if movementdetails[7] == 0:
        
        expires = movementdetails[5]
        
        if str(expires) == "0000-00-00" or str(expires) == "None":
          
          expires = None
          
        else:
          
          expires = miscmethods.GetWXDateFromSQLDate(expires)
        
        destination = unicode(movementdetails[6], "utf8")
        fromtovalue = 0
      else:
        destination = unicode(movementdetails[5], "utf8")
        expires = None
        fromtovalue = 1
      
    else:
      
      movementid = -1
      date = datetime.date.today()
      date = miscmethods.GetWXDateFromDate(date)
      quantity = 0
      
      action = "SELECT Unit FROM medication WHERE ID = " + str(self.medicationid)
      
      unit = unicode(db.SendSQL(action, self.localsettings.dbconnection)[0][0], "utf8")
      
      
      batchno = unicode(movementdetails[0], "utf8")
      expires = None
      destination = ""
      fromtovalue = 1
    
    dialog = wx.Dialog(self, -1, self.t("editmovementlabel"))
    
    dialogsizer = wx.BoxSizer(wx.VERTICAL)
    
    panel = wx.Panel(dialog)
    
    panel.medicationid = self.medicationid
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    movementbuttonssizer1 = wx.BoxSizer(wx.HORIZONTAL)
    
    movementbuttonssizer1.Add(wx.StaticText(panel, -1, "", size=(10,-1)), 0, wx.EXPAND)
    
    quantitylabel = wx.StaticText(panel, -1, " " + self.t("movelabel") + " ")
    movementbuttonssizer1.Add(quantitylabel, 0, wx.ALIGN_CENTER)
    
    quantityentry = wx.TextCtrl(panel, -1, str(quantity))
    quantityentry.Bind(wx.EVT_CHAR, miscmethods.NumbersOnly)
    movementbuttonssizer1.Add(quantityentry, 1, wx.EXPAND)
    
    unitlabel = wx.StaticText(panel, -1, unit + "s ")
    movementbuttonssizer1.Add(unitlabel, 0, wx.ALIGN_CENTER)
    
    fromto = wx.Choice(panel, -1, choices=(self.t("fromlabel"), self.t("tolabel")))
    fromto.Bind(wx.EVT_CHOICE, self.FromToChange)
    fromto.SetSelection(fromtovalue)
    
    if len(movementdetails) > 1:
      
      fromto.Disable()
    
    movementbuttonssizer1.Add(fromto, 0, wx.EXPAND)
    
    destinationentry = wx.TextCtrl(panel, -1, destination)
    movementbuttonssizer1.Add(destinationentry, 3, wx.EXPAND)
    
    movementbuttonssizer1.Add(wx.StaticText(panel, -1, "", size=(10,-1)), 0, wx.EXPAND)
    
    movementbuttonssizer2 = wx.BoxSizer(wx.HORIZONTAL)
    
    movementbuttonssizer2.Add(wx.StaticText(panel, -1, "", size=(10,-1)), 0, wx.EXPAND)
    
    onlabel = wx.StaticText(panel, -1, self.t("onlabel") + " ")
    movementbuttonssizer2.Add(onlabel, 0, wx.ALIGN_CENTER)
    
    movementdate = customwidgets.DateCtrl(panel, self.localsettings)
    movementdate.SetValue(date)
    movementbuttonssizer2.Add(movementdate, 1, wx.EXPAND)
    
    batchlabel = wx.StaticText(panel, -1, " " + self.t("medicationbatchnolabel") + " ")
    movementbuttonssizer2.Add(batchlabel, 0, wx.ALIGN_CENTER)
    
    batchentry = wx.TextCtrl(panel, -1, batchno)
    movementbuttonssizer2.Add(batchentry, 1, wx.EXPAND)
    
    
    expireslabel = wx.StaticText(panel, -1, " " + self.t("medicationexpireslabel") + " ")
    movementbuttonssizer2.Add(expireslabel, 0, wx.ALIGN_CENTER)
    
    expirydate = customwidgets.DateCtrl(panel, self.localsettings)
    
    if expires != None:
      
      expirydate.SetValue(expires)
      
    else:
      
      expirydate.Clear()
    
    if fromtovalue == 1:
      
      expireslabel.Disable()
      expirydate.Disable()
    
    movementbuttonssizer2.Add(expirydate, 1, wx.EXPAND)
    
    submitspacer = wx.StaticText(panel, -1, "", size=(10,-1))
    movementbuttonssizer2.Add(submitspacer, 0, wx.EXPAND)
    
    submitbitmap = wx.Bitmap("icons/submit.png")
    submitbutton = wx.BitmapButton(panel, -1, submitbitmap)
    submitbutton.Bind(wx.EVT_BUTTON, self.SubmitMovement)
    submitbutton.SetToolTipString(self.t("submitlabel"))
    movementbuttonssizer2.Add(submitbutton, 0, wx.ALIGN_BOTTOM)
    
    movementbuttonssizer2.Add(wx.StaticText(panel, -1, "", size=(10,-1)), 0, wx.EXPAND)
    
    topsizer.Add(wx.Panel(panel, size=(-1,10)), 0, wx.EXPAND)
    topsizer.Add(movementbuttonssizer1, 0, wx.EXPAND)
    topsizer.Add(wx.Panel(panel, size=(-1,10)), 0, wx.EXPAND)
    topsizer.Add(movementbuttonssizer2, 0, wx.EXPAND)
    topsizer.Add(wx.Panel(panel, size=(-1,10)), 0, wx.EXPAND)
    
    panel.SetSizer(topsizer)
    
    panel.movementid = movementid
    
    panel.quantityentry = quantityentry
    panel.fromto = fromto
    panel.destinationentry = destinationentry
    panel.movementdate = movementdate
    panel.batchentry = batchentry
    panel.expirydate = expirydate
    panel.expireslabel = expireslabel
    
    dialogsizer.Add(panel, 1, wx.EXPAND)
    
    dialog.SetSizer(dialogsizer)
    
    dialog.Fit()
    
    dialog.ShowModal()
  
  def MovementChangeLog(self, ID):
    
    listboxid = self.medicationmovementlist.GetSelection()
    
    if listboxid > -1:
      movementdetails = self.medicationmovementlist.htmllist[listboxid]
      fromorto = movementdetails[7]
      
      if fromorto == 0:
        action = "SELECT medicationin.ChangeLog, medication.Name FROM medicationin INNER JOIN medication ON medicationin.MedicationID = medication.ID WHERE medicationin.ID = " + str(movementdetails[1])
      else:
        action = "SELECT medicationout.ChangeLog, medication.Name FROM medicationout INNER JOIN medication ON medicationout.MedicationID = medication.ID WHERE medicationout.ID = " + str(movementdetails[1])
      
      results = db.SendSQL(action, self.localsettings.dbconnection)
      
      changelog = unicode(results[0][0], "utf8")
      
      medicationname = unicode(results[0][1], "utf8")
      
      miscmethods.ShowChangeLog(medicationname + " " + self.t("movementmovementlabel").lower(), changelog, self.localsettings.dbconnection)
      
      
  
  def SubmitMovement(self, ID):
    
    parent = ID.GetEventObject().GetParent()
    
    quantity = int(parent.quantityentry.GetValue())

    if quantity > 0:
      batchno = parent.batchentry.GetValue()
    
      expires = parent.expirydate.GetValue()
    
      if str(expires) == "None" or str(expires) == "":
      
        expires = "0000-00-00"
      else:
      
        expires = miscmethods.GetSQLDateFromWXDate(expires)
    
      date = parent.movementdate.GetValue()
      date = miscmethods.GetSQLDateFromWXDate(date)
      destination = parent.destinationentry.GetValue()
    
      if parent.movementid < 1:#Editing an existing movement
      
        if parent.fromto.GetSelection() == 0:
        
          medicationindata = MedicationInData(self.medicationid)
        
          medicationindata.date = date
          medicationindata.amount = quantity
          medicationindata.batchno = batchno
          medicationindata.expires = expires
          medicationindata.wherefrom = destination
        
          medicationindata.Submit(self.localsettings)
        
          self.medicationmovementlist.selectedmovement = (0, medicationindata.ID)
        
        else:
        
          medicationoutdata = MedicationOutData(self.medicationid)
        
          medicationoutdata.date = date
          medicationoutdata.amount = quantity
          medicationoutdata.batchno = batchno
          medicationoutdata.expires = expires
          medicationoutdata.whereto = destination
        
          medicationoutdata.Submit(self.localsettings)
        
          self.medicationmovementlist.selectedmovement = (1, medicationoutdata.ID)
      
      else:
      
        listboxid = self.medicationmovementlist.GetSelection()
        movementid = self.medicationmovementlist.htmllist[listboxid][1]
      
        if parent.fromto.GetSelection() == 0:
        
          medicationindata = MedicationInData(self.medicationid, movementid)
          medicationindata.GetSettings(self.localsettings)
        
          medicationindata.date = date
          medicationindata.amount = quantity
          medicationindata.batchno = batchno
          medicationindata.expires = expires
          medicationindata.wherefrom = destination
        
          medicationindata.Submit(self.localsettings)
        
        else:
        
          medicationoutdata = MedicationOutData(self.medicationid, movementid)
          medicationoutdata.GetSettings(self.localsettings)
        
          medicationoutdata.date = date
          medicationoutdata.amount = quantity
          medicationoutdata.batchno = batchno
          medicationoutdata.whereto = destination
        
          medicationoutdata.Submit(self.localsettings)
    
      emptylist = len(self.medicationmovementlist.htmllist) == 0

      self.RefreshList()
      self.parent.medicationlistbox.RefreshList()

      if emptylist:
        self.medicationmovementlist.SetSelection(0)
    
      self.MovementSelected()
    
      parent.GetParent().Close()

    else:
      
      miscmethods.ShowMessage(self.t("movementcantbezero"), parent)
    
  def RefreshList(self, ID=False):
    
    self.medicationmovementlist.RefreshList()
    self.totallabel.SetLabel(self.t("totallabel") + ": " + str(self.medicationmovementlist.total))
    self.topsizer.Layout()
    
  
  def MovementSelected(self, ID=False):
    
    listboxid = self.medicationmovementlist.GetSelection()
    
    movementdetails = self.medicationmovementlist.htmllist[listboxid]
    
    if movementdetails[6] != self.t("clientbalancelabel"):
      
      #self.deletebutton.Enable()
      #self.editbutton.Enable()
      self.medicationmovementlist.selectedmovement = (movementdetails[7], movementdetails[1])
      
    else:
      
      #self.deletebutton.Disable()
      #self.editbutton.Disable()
      self.medicationmovementlist.selectedmovement = -1
  
  def ClearMovementEntries(self, ID=False):
    
    today = miscmethods.GetTodaysWXDate()
    
    #self.quantityentry.Clear()
    #self.fromto.SetSelection(0)
    #self.destinationentry.Clear()
    #self.movementdate.SetValue(today)
    #self.batchentry.Clear()
    #self.expirydate.SetValue(today)
    #self.expirydate.Enable()
    self.medicationmovementlist.selectedmovement = -1
    self.medicationmovementlist.RefreshList()
    #self.deletebutton.Disable()
    #self.editbutton.Disable()
    #self.fromto.Enable()
    
  def FromToChange(self, ID):
    
    panel = ID.GetEventObject().GetParent()
    
    if panel.fromto.GetSelection() == 0:
      panel.expirydate.Enable()
      panel.expireslabel.Enable()
      panel.batchentry.Clear()
    else:
      panel.expirydate.Clear()
      panel.expireslabel.Disable()
      panel.expirydate.Disable()
  
  def DeleteMovement(self, ID):
    
    if miscmethods.ConfirmMessage(self.t("movementconfirmdeletemovementmessage")) == True:
      
      listboxid = self.medicationmovementlist.GetSelection()
      movementdetails = self.medicationmovementlist.htmllist[listboxid]
      
      if movementdetails[7] == 0:
        
        action = "DELETE FROM medicationin WHERE ID = " + str(movementdetails[1])
        
      else:
        
        action = "DELETE FROM medicationout WHERE ID = " + str(movementdetails[1])
      
      db.SendSQL(action, self.localsettings.dbconnection)
      
      self.ClearMovementEntries()
      self.medicationmovementlist.selectedmovement = -1
      self.RefreshList()
      self.parent.medicationlistbox.RefreshList()

class MedicationSearchPanel(wx.Panel):
  
  def t(self, field, idx = 0):
    
    return  self.localsettings.t(field,idx)
  
  def __init__(self, parent, localsettings):
    
    self.parent = parent
    self.localsettings = localsettings
    
    wx.Panel.__init__(self, parent)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    entrysizer = wx.BoxSizer(wx.VERTICAL)
    
    namelabel = wx.StaticText(self, -1, self.t("namelabel"))
    font = namelabel.GetFont()
    font.SetPointSize(font.GetPointSize() - 2)
    namelabel.SetFont(font)
    entrysizer.Add(namelabel, 0, wx.ALIGN_LEFT)
    
    nameentry = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER)
    nameentry.Bind(wx.EVT_CHAR, self.KeyStroke)
    entrysizer.Add(nameentry, 1, wx.EXPAND)
    
    descriptionlabel = wx.StaticText(self, -1, self.t("descriptionlabel"))
    descriptionlabel.SetFont(font)
    entrysizer.Add(descriptionlabel, 0, wx.ALIGN_LEFT)
    
    descriptionentry = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER)
    descriptionentry.Bind(wx.EVT_CHAR, self.KeyStroke)
    entrysizer.Add(descriptionentry, 1, wx.EXPAND)
    
    horizontalsizer.Add(entrysizer, 1, wx.EXPAND)
    
    horizontalsizer.Add(wx.Panel(self, size=(10,-1)), 0, wx.EXPAND)
    
    checkboxsizer = wx.FlexGridSizer(cols=2)
    checkboxsizer.AddGrowableCol(0)
    checkboxsizer.AddGrowableCol(1)
    
    checkboxspacer1 = wx.StaticText(self, -1, "")
    checkboxspacer1.SetFont(font)
    
    checkboxspacer2 = wx.StaticText(self, -1, "")
    font = checkboxspacer2.GetFont()
    font.SetPointSize(font.GetPointSize() - 2)
    checkboxspacer2.SetFont(font)
    
    checkboxsizer.Add(checkboxspacer1, 0, wx.EXPAND)
    checkboxsizer.Add(checkboxspacer2, 0, wx.EXPAND)
    
    medicationradio = wx.CheckBox(self, -1, self.t("randomdatamedicationlabel"))
    medicationradio.Bind(wx.EVT_CHECKBOX, self.parent.RefreshMedicationList)
    medicationradio.SetFont(font)
    medicationradio.SetValue(True)
    checkboxsizer.Add(medicationradio, 0, wx.EXPAND)
    
    vaccinationradio = wx.CheckBox(self, -1, self.t("vaccinationsvaccinelabel"))
    vaccinationradio.Bind(wx.EVT_CHECKBOX, self.parent.RefreshMedicationList)
    vaccinationradio.SetFont(font)
    vaccinationradio.SetValue(True)
    checkboxsizer.Add(vaccinationradio, 0, wx.EXPAND)
    
    consumableradio = wx.CheckBox(self, -1, self.t("consumablelabel"))
    consumableradio.Bind(wx.EVT_CHECKBOX, self.parent.RefreshMedicationList)
    consumableradio.SetFont(font)
    consumableradio.SetValue(True)
    checkboxsizer.Add(consumableradio, 0, wx.EXPAND)
    
    shopradio = wx.CheckBox(self, -1, self.t("shoplabel"))
    shopradio.Bind(wx.EVT_CHECKBOX, self.parent.RefreshMedicationList)
    shopradio.SetFont(font)
    shopradio.SetValue(True)
    checkboxsizer.Add(shopradio, 0, wx.EXPAND)
    
    chipradio = wx.CheckBox(self, -1, self.t("microchiplabel"))
    chipradio.Bind(wx.EVT_CHECKBOX, self.parent.RefreshMedicationList)
    chipradio.SetFont(font)
    chipradio.SetValue(True)
    checkboxsizer.Add(chipradio, 0, wx.EXPAND)
    
    runninglowentry = wx.CheckBox(self, -1, self.t("runninglowlabel"))
    runninglowentry.Bind(wx.EVT_CHECKBOX, self.parent.RefreshMedicationList)
    runninglowentry.SetFont(font)
    checkboxsizer.Add(runninglowentry, 0, wx.EXPAND)
    
    horizontalsizer.Add(checkboxsizer, 0, wx.EXPAND)
    
    horizontalsizer.Add(wx.Panel(self, size=(10,-1)), 0, wx.EXPAND)
    
    topsizer.Add(horizontalsizer, 0, wx.EXPAND)
    
    topsizer.Add(wx.Panel(self, size=(-1,10)), 0, wx.EXPAND)
    
    self.SetSizer(topsizer)
    
    self.nameentry = nameentry
    self.descriptionentry = descriptionentry
    self.runninglowentry = runninglowentry
    self.shopradio = shopradio
    self.medicationradio = medicationradio
    self.vaccinationradio = vaccinationradio
    self.consumableradio = consumableradio
    self.chipradio = chipradio
  
  def KeyStroke(self, ID):
    
    keycode = ID.GetKeyCode()
    
    if keycode == 13:
      
      self.parent.RefreshMedicationList()
    
    ID.Skip()
  
  def Reset(self, ID=False):
    
    self.nameentry.Clear()
    self.descriptionentry.Clear()
    self.runninglowentry.SetValue(False)
    self.shopradio.SetValue(True)
    self.medicationradio.SetValue(True)
    self.vaccinationradio.SetValue(True)
    self.consumableradio.SetValue(True)
    self.chipradio.SetValue(True)

class ShopSale(wx.Dialog):
  
  def t(self, field, idx = 0):
    
    return  self.localsettings.t(field,idx)
  
  def __init__(self, parent, clientid, localsettings):
    
    self.localsettings = localsettings
    self.clientid = clientid
    self.parent = parent
    self.basket = []
    
    action = "SELECT ClientTitle, ClientForenames, ClientSurname FROM client WHERE ID = " + str(self.clientid)
    results = db.SendSQL(action, self.localsettings.dbconnection)
    
    title = results[0][0] 
    forenames = results[0][1]
    surname = results[0][2]
    
    name = ""
    
    if surname == "":
      
      name = forenames
      
    else:
      
      if title != "":
        
        name = title + " "
      
      if forenames != "":
        
        name = name + forenames + " "
      
      name = name + surname
    
    self.clientname = name
    
    wx.Dialog.__init__(self, parent, -1, self.t("shopitemstitle") + " - " + name)
    
    dialogsizer = wx.BoxSizer(wx.VERTICAL)
    
    panel = wx.Panel(self)
    
    topsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    stocksizer = wx.BoxSizer(wx.VERTICAL)
    
    medicationnamelabel = wx.StaticText(panel, -1, self.t("searchlabel"))
    stocksizer.Add(medicationnamelabel, 0, wx.ALIGN_LEFT)
    
    nameentry = wx.TextCtrl(panel, -1, "")
    nameentry.Bind(wx.wx.EVT_TEXT, self.KeyPress)
    stocksizer.Add(nameentry, 0, wx.EXPAND)
    
    medicationlabel = wx.StaticText(panel, -1, self.t("shopitemstitle"))
    stocksizer.Add(medicationlabel, 0, wx.ALIGN_LEFT)
    
    listbox = wx.ListBox(panel, -1, size=(-1,150))
    listbox.Bind(wx.EVT_LISTBOX, self.ChoiceSelected)
    #listbox.Bind(wx.EVT_RIGHT_DOWN, self.ShowDescription)
    stocksizer.Add(listbox, 1, wx.EXPAND)
    
    stocksizer.Add(wx.Panel(panel, size=(10,10)), 0, wx.EXPAND)
    
    horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    quantitysizer = wx.BoxSizer(wx.VERTICAL)
    
    quantitylabel = wx.StaticText(panel, -1, self.t("quantitylabel"))
    quantitysizer.Add(quantitylabel, 0, wx.ALIGN_LEFT)
    
    quantityentrysizer = wx.BoxSizer(wx.HORIZONTAL)
    
    removebitmap = wx.Bitmap("icons/out.png")
    subtractbutton = wx.BitmapButton(panel, -1, removebitmap)
    subtractbutton.Bind(wx.EVT_BUTTON, self.DecreaseQuantity)
    subtractbutton.SetToolTipString(self.t("subtractlabel"))
    quantityentrysizer.Add(subtractbutton, 0, wx.EXPAND)
    
    quantityentry = wx.TextCtrl(panel, -1, "1", size=(100,-1))
    quantityentrysizer.Add(quantityentry, 0, wx.EXPAND)
    
    addbitmap = wx.Bitmap("icons/in.png")
    plusbutton = wx.BitmapButton(panel, -1, addbitmap)
    plusbutton.Bind(wx.EVT_BUTTON, self.IncreaseQuantity)
    plusbutton.SetToolTipString(self.t("addlabel"))
    quantityentrysizer.Add(plusbutton, 0, wx.EXPAND)
    
    unittext = self.t("unitlabel").lower()
    
    unitlabel = wx.StaticText(panel, -1, miscmethods.NoWrap(" x " + unittext + " "))
    quantityentrysizer.Add(unitlabel, 0, wx.ALIGN_CENTER)
    
    quantitysizer.Add(quantityentrysizer, 0, wx.EXPAND)
    
    horizontalsizer.Add(quantitysizer, 0, wx.EXPAND)
    
    stocksizer.Add(horizontalsizer, 0, wx.EXPAND)
    
    topsizer.Add(stocksizer, 1, wx.EXPAND)
    
    topsizer.Add(wx.Panel(panel, size=(10,10)), 0, wx.EXPAND)
    
    submitsizer = wx.BoxSizer(wx.VERTICAL)
    
    submitbitmap = wx.Bitmap("icons/rightarrow.png")
    submitbutton = wx.BitmapButton(panel, -1, submitbitmap)
    submitbutton.Disable()
    submitbutton.SetToolTipString(self.t("addtobaskettooltip"))
    submitbutton.Bind(wx.EVT_BUTTON, self.AddToBasket)
    submitsizer.Add(submitbutton, 0, wx.ALIGN_BOTTOM)
    
    submitsizer.Add(wx.StaticText(panel, -1, "", size=(10,-1)), 0, wx.EXPAND)
    
    putbackbitmap = wx.Bitmap("icons/leftarrow.png")
    putbackbutton = wx.BitmapButton(panel, -1, putbackbitmap)
    putbackbutton.Disable()
    putbackbutton.SetToolTipString(self.t("putbacktooltip"))
    putbackbutton.Bind(wx.EVT_BUTTON, self.RemoveFromBasket)
    submitsizer.Add(putbackbutton, 0, wx.ALIGN_BOTTOM)
    
    topsizer.Add(submitsizer, 0, wx.ALIGN_CENTER)
    
    topsizer.Add(wx.Panel(panel, size=(10,10)), 0, wx.EXPAND)
    
    basketsizer = wx.BoxSizer(wx.VERTICAL)
    
    basketlabel = wx.StaticText(panel, -1, self.t("basketlabel"))
    basketsizer.Add(basketlabel, 0, wx.ALIGN_LEFT)
    
    self.basketlistbox = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
    #listmix.ColumnSorterMixin.__init__(self, 4)
    
    self.basketlistbox.Bind(wx.EVT_LIST_ITEM_SELECTED, self.BasketItemSelected)
    
    basketsizer.Add(self.basketlistbox, 1, wx.EXPAND)
    
    totalsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    totallabel = wx.StaticText(panel, -1, self.t("totallabel") + ": 0")
    totalsizer.Add(totallabel, 0, wx.ALIGN_CENTER)
    
    totalsizer.Add(wx.StaticText(panel, -1, ""), 1, wx.EXPAND)
    
    markaspaidcheckbox = wx.CheckBox(panel, -1, self.t("markaspaidlabel"))
    totalsizer.Add(markaspaidcheckbox, 0, wx.ALIGN_CENTER)
    
    basketsizer.Add(totalsizer, 0, wx.EXPAND)
    
    topsizer.Add(basketsizer, 1, wx.EXPAND)
    
    topsizer.Add(wx.Panel(panel, size=(10,10)), 0, wx.EXPAND)
    
    confirmbitmap = wx.Bitmap("icons/submit.png")
    confirmbutton = wx.BitmapButton(panel, -1, confirmbitmap)
    confirmbutton.Disable()
    confirmbutton.SetToolTipString(self.t("submitlabel"))
    confirmbutton.Bind(wx.EVT_BUTTON, self.SubmitBasket)
    topsizer.Add(confirmbutton, 0, wx.ALIGN_CENTER)
    
    panel.SetSizer(topsizer)
    
    panel.nameentry = nameentry
    panel.quantityentry = quantityentry
    panel.listbox = listbox
    panel.submitbutton = submitbutton
    panel.unitlabel = unitlabel
    panel.horizontalsizer = horizontalsizer
    panel.basketlistbox = self.basketlistbox
    panel.totallabel = totallabel
    panel.putbackbutton = putbackbutton
    panel.confirmbutton = confirmbutton
    panel.markaspaidcheckbox = markaspaidcheckbox
    self.totalprice = 0
    
    dialogsizer.Add(panel, 1, wx.EXPAND)
    
    self.SetSizer(dialogsizer)
    
    busy = wx.BusyCursor()
    action = "SELECT * FROM medication ORDER BY Name"
    panel.rawmedicationdata = db.SendSQL(action, self.localsettings.dbconnection)
    panel.medicationdata = panel.rawmedicationdata
    del busy
    
    self.UpdateList(panel)
    
    self.RefreshBasket(panel)
    
    self.Fit()
    
    panel.nameentry.SetFocus()
    
    self.ShowModal()
  
  def GetListCtrl(self):# Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    
          return self.basketlistbox
  
  def IncreaseQuantity(self, ID):
    
    panel = ID.GetEventObject().GetParent()
    
    quantity = panel.quantityentry.GetValue()
    
    try:
      
      quantity = int(quantity)
      quantitycheck = True
      quantity = quantity + 1
      panel.quantityentry.SetValue(str(quantity))
      
    except:
      
      miscmethods.ShowMessage(self.t("quantityerrormessage"), self)
  
  def DecreaseQuantity(self, ID):
    
    panel = ID.GetEventObject().GetParent()
    
    quantity = panel.quantityentry.GetValue()
    
    try:
      
      quantity = int(quantity)
      quantitycheck = True
      quantity = quantity - 1
      panel.quantityentry.SetValue(str(quantity))
      
    except:
      
      miscmethods.ShowMessage(self.t("quantityerrormessage"), self)
  
  def BasketItemSelected(self, ID):
    
    panel = ID.GetEventObject().GetParent()
    
    panel.putbackbutton.Enable()
  
  def AddToBasket(self, ID):
    
    panel = ID.GetEventObject().GetParent()
    
    quantity = panel.quantityentry.GetValue()
    
    quantitycheck = False
    
    try:
      
      quantity = int(quantity)
      quantitycheck = True
      
    except:
      
      miscmethods.ShowMessage(self.t("quantityerrormessage"), self)
    
    if quantitycheck == True:
      
      choiceid = panel.listbox.GetSelection()
      
      stockid = panel.medicationdata[choiceid][0]
      name = panel.medicationdata[choiceid][1]
      unit = panel.medicationdata[choiceid][3]
      unitprice = panel.medicationdata[choiceid][5]
      
      todaysdate = datetime.date.today()
      todaysdate = miscmethods.GetSQLDateFromDate(todaysdate)
      
      #medicationout (ID, MedicationID, Date, Amount, BatchNo, WhereTo, AppointmentID, ChangeLog, NextDue)
      
      self.basket.append((stockid, name, todaysdate, quantity, unit, unitprice, ))
      
      self.RefreshBasket(panel)
  
  def RemoveFromBasket(self, ID):
    
    panel = ID.GetEventObject().GetParent()
    
    listboxid = self.basketlistbox.GetFocusedItem()
    
    count = 0
    
    basket = []
    
    for a in self.basket:
      
      if count != listboxid:
        
        basket.append(a)
      
      count = count + 1
    
    self.basket = basket
    
    self.RefreshBasket(panel)
  
  def RefreshBasket(self, panel):
    
    self.itemDataMap = {}
    
    self.basketlistbox.ClearAll()
    
    self.basketlistbox.InsertColumn(0, self.t("namelabel"))
    self.basketlistbox.InsertColumn(1, self.t("quantitylabel"))
    self.basketlistbox.InsertColumn(2, self.t("pricelabel"))
    
    totalprice = 0
    
    count = 0
    
    for a in self.basket:
      
      price = int(a[3]) * int(a[5])
      
      totalprice = totalprice + price
      
      price = miscmethods.FormatPrice(price)
      
      if self.t("currency") == "&pound;":
        
        price = u"£" + price
        
      else:
        
        price = self.t("currency") + price
      
      self.itemDataMap[a[0]] = ( a[1], str(a[3]) + " x " + a[4], price )
      
      self.basketlistbox.InsertStringItem(count, a[1])
      self.basketlistbox.SetStringItem(count, 1, str(a[3]) + " x " + a[4])
      self.basketlistbox.SetStringItem(count, 2, price)
      
      count = count + 1
    
    if len(self.basket) == 0:
      
      self.basketlistbox.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
      self.basketlistbox.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
      self.basketlistbox.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
      
    else:
      
      self.basketlistbox.SetColumnWidth(0, wx.LIST_AUTOSIZE)
      self.basketlistbox.SetColumnWidth(1, wx.LIST_AUTOSIZE)
      self.basketlistbox.SetColumnWidth(2, wx.LIST_AUTOSIZE)
    
    self.totalprice = totalprice
    
    totalprice = miscmethods.FormatPrice(totalprice)
    
    if self.t("currency") == "&pound;":
      
      totalprice = u"£" + totalprice
      
    else:
      
      totalprice = self.t("currency") + totalprice
    
    panel.totallabel.SetLabel(self.t("totallabel") + ": " + totalprice)
    
    panel.putbackbutton.Disable()
    
    if len(self.basket) > 0:
      
      panel.confirmbutton.Enable()
      
    else:
      
      panel.confirmbutton.Disable()
  
  def ChoiceSelected(self, ID):
    
    try:
      
      panel = ID.GetEventObject().GetParent()
      
    except:
      
      panel = ID
    
    choiceid = panel.listbox.GetSelection()
    
    currentbatch = panel.medicationdata[choiceid][4]
    unit = panel.medicationdata[choiceid][3]
    
    panel.unitlabel.SetLabel(miscmethods.NoWrap(" x " + unit + " "))
    panel.horizontalsizer.Layout()
  
  def KeyPress(self, ID):
    
    nameentry = ID.GetEventObject()
    
    ID.Skip()
    
    panel = nameentry.GetParent()
    
    self.UpdateList(panel)
  
  def UpdateList(self, ID):
    
    try:
      
      panel = ID.GetEventObject().GetParent()
      
    except:
      
      panel = ID
    
    namecontains = panel.nameentry.GetValue()
    
    filteredmedicationdata = []
    
    for a in panel.rawmedicationdata:
      
      if namecontains == "":
        
        filteredmedicationdata.append(a)
        
      else:
        
        if a[1].lower().__contains__(namecontains.lower()) == True or a[2].lower().__contains__(namecontains.lower()):
          
          filteredmedicationdata.append(a)
    
    panel.listbox.Clear()
    
    if len(filteredmedicationdata) > 0:
      
      for a in filteredmedicationdata:
        
        if self.t("currency") == "&pound;":
          
          currencysymbol = u"£"
          
        else:
          
          currencysymbol = self.t("currency")
        
        panel.listbox.Append(a[1] + "  (" + currencysymbol + miscmethods.FormatPrice(a[5]) + "/" + a[3] + ")")
    
    panel.medicationdata = filteredmedicationdata
    
    if len(filteredmedicationdata) == 0:
      
      panel.listbox.SetSelection(-1)
      panel.submitbutton.Disable()
      panel.unitlabel.SetLabel(miscmethods.NoWrap(" x " + self.t("unitlabel").lower() + " "))
      panel.horizontalsizer.Layout()
      
    else:
      
      panel.listbox.SetSelection(0)
      self.ChoiceSelected(panel)
      panel.submitbutton.Enable()
  
  def SubmitBasket(self, ID):
    
    for a in self.basket:
      
      medicationoutdata = MedicationOutData(a[0])
      
      #self.basket.append((stockid, name, todaysdate, quantity, unit, unitprice))
      
      date = datetime.date.today()
      medicationoutdata.date = miscmethods.GetSQLDateFromDate(date)
      
      medicationoutdata.amount = int(a[3])
      medicationoutdata.batchno = u""
      medicationoutdata.whereto = self.t("shopsalemenuitem") + " - " + self.clientname
      medicationoutdata.appointmentid = 0
      
      medicationoutdata.Submit(self.localsettings)
      
      #WriteToReceiptTable(connection, ID, Date, Description, Price, Type, TypeID, AppointmentID, userid)
      
      description = a[1] + " x " + str(a[3])
      
      price = int(a[3]) * int(a[5]) * -1
      
      dbmethods.WriteToReceiptTable(self.localsettings.dbconnection, False, medicationoutdata.date, description, price, 4, self.clientid, 0, self.localsettings.userid)
    
    #Types are: 0 = medication, 1 = procedure, 2 = vaccination, 3 = manual, 4 = payment
    
    #WriteToReceiptTable(connection, ID, Date, Description, Price, Type, TypeID, AppointmentID, userid)
    
    panel = ID.GetEventObject().GetParent()
    
    if panel.markaspaidcheckbox.GetValue():
      
      dbmethods.WriteToReceiptTable(self.localsettings.dbconnection, False, miscmethods.GetSQLDateFromDate(date), self.t("clientpaymentinreceiptlabel"), self.totalprice, 4, self.clientid, 0, self.localsettings.userid)
    
    self.Close()

class EditMarkUp(wx.Dialog):
  
  def t(self, field, idx = 0):
    
    return  self.localsettings.t(field,idx)
  
  def __init__(self, parent, localsettings):
    
    self.localsettings = localsettings
    
    wx.Dialog.__init__(self, parent, -1, self.t("editmarkupmenu"))
    
    dialogsizer = wx.BoxSizer(wx.VERTICAL)
    
    panel = wx.Panel(self)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    gridsizer = wx.FlexGridSizer(cols=2)
    gridsizer.AddGrowableCol(1)
    
    costpricelabel = wx.StaticText(panel, -1, self.t("costpricelabel"))
    gridsizer.Add(costpricelabel, 0, wx.ALIGN_RIGHT)
    
    costpriceentry = wx.TextCtrl(panel, -1, "10.00")
    costpriceentry.Bind(wx.EVT_TEXT, self.KeyPressed)
    costpriceentry.SetToolTipString(self.t("costpriceentrytooltip"))
    gridsizer.Add(costpriceentry, 1, wx.EXPAND)
    
    gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
    gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
    
    multiplybylabel = wx.StaticText(panel, -1, self.t("multiplybylabel"))
    gridsizer.Add(multiplybylabel, 0, wx.ALIGN_RIGHT)
    
    multiplybyentry = wx.TextCtrl(panel, -1, str(self.localsettings.markupmultiplyby))
    multiplybyentry.Bind(wx.EVT_TEXT, self.KeyPressed)
    gridsizer.Add(multiplybyentry, 1, wx.EXPAND)
    
    roundtolabel = wx.StaticText(panel, -1, self.t("roundtolabel"))
    gridsizer.Add(roundtolabel, 0, wx.ALIGN_RIGHT)
    
    roundtoentry = wx.TextCtrl(panel, -1, str(self.localsettings.markuproundto))
    roundtoentry.Bind(wx.EVT_TEXT, self.KeyPressed)
    roundtoentry.SetToolTipString(self.t("priceinpenniestooltip"))
    gridsizer.Add(roundtoentry, 1, wx.EXPAND)
    
    gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
    gridsizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
    
    unitpricelabel = wx.StaticText(panel, -1, self.t("customerpricelabel"))
    gridsizer.Add(unitpricelabel, 0, wx.ALIGN_RIGHT)
    
    unitpriceentry = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
    gridsizer.Add(unitpriceentry, 1, wx.EXPAND)
    
    topsizer.Add(gridsizer, 0, wx.EXPAND)
    
    topsizer.Add(wx.StaticText(panel, -1 , ""), 1, wx.EXPAND)
    
    buttonssizer = wx.BoxSizer(wx.HORIZONTAL)
    
    submitbitmap = wx.Bitmap("icons/submit.png")
    submitbutton = wx.BitmapButton(panel, -1, submitbitmap)
    submitbutton.SetToolTipString(self.t("submitsettingstooltip"))
    submitbutton.Bind(wx.EVT_BUTTON, self.Submit)
    buttonssizer.Add(submitbutton, 0, wx.EXPAND)
    
    applybitmap = wx.Bitmap("icons/refresh.png")
    applybutton = wx.BitmapButton(panel, -1, applybitmap)
    applybutton.SetToolTipString(self.t("applymarkuptostocktooltip"))
    applybutton.Bind(wx.EVT_BUTTON, self.Apply)
    buttonssizer.Add(applybutton, 0, wx.EXPAND)
    
    topsizer.Add(buttonssizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
    
    topsizer.Add(wx.StaticText(panel, -1 , ""), 1, wx.EXPAND)
    
    panel.SetSizer(topsizer)
    
    dialogsizer.Add(panel, 1, wx.EXPAND)
    
    self.SetSizer(dialogsizer)
    
    self.SetSize((300,200))
    #self.Fit()
    
    self.costpriceentry = costpriceentry
    self.multiplybyentry = multiplybyentry
    self.roundtoentry = roundtoentry
    self.unitpriceentry = unitpriceentry
    
    self.submitbutton = submitbutton
    self.applybutton = applybutton
    
    self.CalculateUnitPrice()
    
    self.ShowModal()
  
  def CheckValues(self):
    
    success = True
    
    try:
      
      costprice = float(self.costpriceentry.GetValue())
      
    except:
      
      success = False
      #miscmethods.ShowMessage(self.t("invalidpricemessage"), self)
    
    try:
      
      multiplyby = float(self.multiplybyentry.GetValue())
      
    except:
      
      success = False
      #miscmethods.ShowMessage(self.t("quantityerrormessage"), self)
    
    try:
      
      roundto = int(self.roundtoentry.GetValue())
      
    except:
      
      success = False
      #miscmethods.ShowMessage(self.t("invalidpricemessage"), self)
    
    if success == True:
      
      self.submitbutton.Enable()
      self.applybutton.Enable()
      
    else:
      
      self.submitbutton.Disable()
      self.applybutton.Disable()
    
    return success
  
  def Submit(self, ID):
    
    if self.CheckValues() == True:
      
      self.localsettings.markupmultiplyby = self.multiplybyentry.GetValue()
      self.localsettings.markuproundto = int(self.roundtoentry.GetValue())
      
      action = "UPDATE settings SET MarkupMultiplyBy = \"" + self.multiplybyentry.GetValue() + "\", MarkupRoundTo = " + self.multiplybyentry.GetValue()
      db.SendSQL(action, self.localsettings.dbconnection)
      
      self.Close()
  
  def KeyPressed(self, ID):
    
    parentobject = ID.GetEventObject()
    
    self.CalculateUnitPrice()
  
  def CalculateUnitPrice(self):
    
    if self.CheckValues() == True:
      
      #print "Calculating.."
      
      costprice = self.costpriceentry.GetValue()
      multiplyby = float(self.multiplybyentry.GetValue())
      roundto = int(self.roundtoentry.GetValue())
      
      #print "costprice = " + costprice
      
      if costprice[-1] == ".":
        
        costprice = costprice[:-1]
      
      unitprice = int(miscmethods.ConvertPriceToPennies(costprice) * multiplyby)
      
      while unitprice % roundto > 0:
        
        unitprice = unitprice + 1
      
      unitprice = miscmethods.FormatPrice(unitprice)
      
      self.unitpriceentry.SetValue(str(unitprice))
      
    else:
      
      self.unitpriceentry.SetValue(self.t("errorlabel"))
  
  def Apply(self, ID):
    
    if self.CheckValues() == True:
      
      if miscmethods.ConfirmMessage(self.t("automarkupconfirmmessage"), self):
        
        multiplyby = float(self.multiplybyentry.GetValue())
        roundto = int(self.roundtoentry.GetValue())
        
        action = "SELECT ID, CostPrice FROM medication"
        results = db.SendSQL(action, self.localsettings.dbconnection)
        
        for a in results:
          
          costprice = a[1]
          
          unitprice = int(costprice * multiplyby)
          
          while unitprice % roundto > 0:
            
            unitprice = unitprice + 1
          
          action = "UPDATE medication SET CurrentPrice = " + str(unitprice) + " WHERE ID = " + str(a[0])
          db.SendSQL(action, self.localsettings.dbconnection)
          
        miscmethods.ShowMessage(self.t("markupappliedtoallmessage"), self)
