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

import miscmethods
import wx
import db
import sys
import language
import time
import os
import clientmethods

class settings:
  
  def __init__(self, userid):
    
    self.dbip = ""
    self.dbuser = ""
    self.dbpass = ""
    self.userid = userid
  
  def GetSettings(self):
    
    home = miscmethods.GetHome()
    
    self.dictionary = language.GetDictionary()
    
    conffile = home + "/.evette.conf"
    
    try:
      
      if os.path.isfile(conffile):
        
        inp = open(conffile, "r")
        filecontents = ""
        
        for a in inp.readlines():
          
          filecontents = filecontents + a
        
        inp.close()
        
        settingslist = filecontents.strip().split("\n")
        self.dbip = settingslist[0]
        self.dbuser = settingslist[1]
        self.dbpass = settingslist[2]
        self.lastuser = settingslist[4]
        self.language = int(settingslist[5])
        self.appointmentrefresh = int(settingslist[6])
      else:
        self.dbip = "localhost"
        self.dbuser = "root"
        self.dbpass = ""
        self.lastuser = "user"
        self.language = 0
        self.appointmentrefresh = 30
    except:
      #print sys.exc_info()
      self.dbip = "localhost"
      self.dbuser = "root"
      self.dbpass = ""
      self.lastuser = "user"
      self.language = 0
      self.appointmentrefresh = 30
    
    if self.userid != False:
      
      connection = db.GetConnection(self)
      self.dbconnection = connection
      
      action = "SELECT * FROM settings"
      results = db.SendSQL(action, connection)
      
      self.practicename = unicode(results[0][1], "utf8")
      self.openfrom = results[0][2]
      self.opento = results[0][3]
      self.operationtime = results[0][4]
      self.practiceaddress = unicode(results[0][5], "utf8")
      self.practicepostcode = unicode(results[0][6], "utf8")
      self.practicetelephone = unicode(results[0][7], "utf8")
      self.practiceemail = unicode(results[0][8], "utf8")
      self.practicewebsite = unicode(results[0][9], "utf8")
      self.shelterid = results[0][10]
      self.markupmultiplyby = results[0][11]
      self.markuproundto = results[0][12]
      self.asmvaccinationid = results[0][13]
      self.prescriptionfee = results[0][14]
      self.handle_rota_by_day = results[0][15]
      
      action = "SELECT * FROM user WHERE ID = " + str(self.userid)
      results = db.SendSQL(action, connection)
      
      self.username = unicode(results[0][1], "utf8")
      self.userposition = unicode(results[0][3], "utf8")
      
      changelog = results[0][4].split("$")
      self.editclients = int(changelog[0][0])
      self.deleteclients = int(changelog[0][1])
      self.editfinances = int(changelog[0][2])
      self.editanimals = int(changelog[1][0])
      self.deleteanimals = int(changelog[1][1])
      self.editappointments = int(changelog[2][0])
      self.deleteappointments = int(changelog[2][1])
      self.vetform = int(changelog[2][2])
      self.editmedication = int(changelog[3][0])
      self.deletemedication = int(changelog[3][1])
      self.editprocedures = int(changelog[4][0])
      self.deleteprocedures = int(changelog[4][1])
      self.editlookups = int(changelog[5][0])
      self.deletelookups = int(changelog[5][1])
      self.editforms = int(changelog[6][0])
      self.deleteforms = int(changelog[6][1])
      self.editusers = int(changelog[7][0])
      self.deleteusers = int(changelog[7][1])
      self.editrota = int(changelog[7][2])
      self.toolbar = int(changelog[8][0])
      self.changelog = int(changelog[8][1])
      self.editsettings = int(changelog[8][2])
      self.multiplepanels = int(changelog[8][3])
      self.asmsync = int(changelog[8][4])
      self.addtodiary = int(changelog[9][0])
      self.editdiary = int(changelog[9][1])
      self.deletefromdiary = int(changelog[9][2])
      
      self.last_assigned_vet = None
  
  def SaveSettings(self, username=""):
    
    home = miscmethods.GetHome()
    out = open(home + "/.evette.conf", "w")
    out.write(self.dbip + "\n" + self.dbuser + "\n" + self.dbpass + "\n\n" + username + "\n" + str(self.language) + "\n" + str(self.appointmentrefresh))
    out.close()
    
    self.GetSettings()
  
  def t(self, langkey, idx = 0):
    v = self.dictionary[langkey][self.language]
    return v[idx ]if type(v).__name__ == 'tuple' else v

  def GetVetsNames(self):
    action = "SELECT Name FROM user WHERE Position = \"" + self.t("vetpositiontitle") + "\""
    results = db.SendSQL(action, self.dbconnection)

    return map(lambda a: a[0], results)
  
  def GetVetsByDateAndTime(self, date, time_str, operations):
    if self.handle_rota_by_day:

      action = "SELECT Name FROM staff WHERE Date = \"" + date + "\" AND \"" + time_str + ":00\" BETWEEN TimeOn AND TimeOff AND Operating = " + str(operations) + " AND Position = \"" + self.t("vetpositiontitle") + "\" ORDER BY Name"

    else:
      days = ['mon','tue','wed','thu','fri','sat','sun']
      day = time.strptime(date,"%Y-%m-%d").tm_wday
      day = days[day]
      time_str = time_str.replace(':','')
      
      action = "SELECT Name FROM user WHERE Position = '" + self.t("vetpositiontitle") + "' AND " + day + "_from <= '" + time_str + "' AND " + day + "_to >= '" + time_str + "' ORDER BY Name"

    results = db.SendSQL(action, self.dbconnection)
    
    return map(lambda x: x[0], results)

def CreateConfFile():
  
  home = miscmethods.GetHome()
  conffile = home + "/.evette.conf"
  output = "localhost\nroot\nFalse\n\nuser\n0"
  out = open(conffile, "w")
  out.write(output)
  out.close()

class SettingsPanel(wx.Panel):
  
  def t(self, field, idx = 0):
    
    return self.localsettings.t(field,idx)
  
  def UpdateShelterName(self, ID=False):
    
    action = "SELECT client.ClientTitle, client.ClientForenames, client.ClientSurname FROM client INNER JOIN settings ON settings.ShelterID = client.ID"
    shelteridresults = db.SendSQL(action, self.localsettings.dbconnection)
    
    if len(shelteridresults) > 0:
      
      sheltername = ""
      
      if shelteridresults[0][0] != "":
        
        sheltername = sheltername + shelteridresults[0][0] + " "
      
      if shelteridresults[0][1] != "":
        
        sheltername = sheltername + shelteridresults[0][1] + " "
      
      if shelteridresults[0][2] != "":
        
        sheltername = sheltername + shelteridresults[0][2]
      
    else:
      
      sheltername = self.t("nonelabel")
    
    self.asmshelterentry.SetValue(sheltername)
  
  def UpdateShelterVaccination(self, ID=False):
    
    try:
      asmconnection = db.GetASMConnection()
      action = "SELECT ID, VaccinationType FROM vaccinationtype WHERE ID = " + str(self.localsettings.asmvaccinationid)
      asmvaccinationresults = db.SendSQL(action, asmconnection)
      asmconnection.close()
      
      if len(asmvaccinationresults) > 0:
        
        self.localsettings.asmvaccinationid = asmvaccinationresults[0][0]
        asmvaccinationtype = asmvaccinationresults[0][1]
        
      else:
        
        self.localsettings.asmvaccinationid = 0
        asmvaccinationtype = self.t("nonelabel")
        
      self.asmvaccinationentry.SetValue(asmvaccinationtype)
      
    except:
      
      self.asmvaccinationentry.SetValue(self.t("errorlabel"))
      self.asmvaccinationbutton.Disable()
  
  def __init__(self, notebook, localsettings):
    
    self.localsettings = localsettings
    
    pagetitle = self.t("editsettingslabel")
    
    action = "SELECT * FROM settings"
    results = db.SendSQL(action, localsettings.dbconnection)
    
    practicename = results[0][1]
    openfrom = results[0][2]
    opento = results[0][3]
    operationtime = results[0][4]
    handle_rota_by_day = results[0][15]
    practiceaddress = results[0][5]
    practicepostcode = results[0][6]
    practicetelephone = results[0][7]
    practiceemail = results[0][8]
    practicewebsite = results[0][9]
    language = localsettings.language
    
    self.pagetitle = miscmethods.GetPageTitle(notebook, pagetitle)
    
    wx.Panel.__init__(self, notebook)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    leftsizer = wx.BoxSizer(wx.VERTICAL)
    
    namelabel = wx.StaticText(self, -1, self.t("settingspracticenamelabel") + ": ")
    font = namelabel.GetFont()
    font.SetPointSize(font.GetPointSize() - 2)
    namelabel.SetFont(font)
    leftsizer.Add(namelabel, 0, wx.ALIGN_LEFT)
    
    nameentry = wx.TextCtrl(self, -1, practicename)
    leftsizer.Add(nameentry, 0, wx.EXPAND)
    
    addresslabel = wx.StaticText(self, -1, self.t("clientaddresslabel") + ": ")
    addresslabel.SetFont(font)
    leftsizer.Add(addresslabel, 0, wx.ALIGN_LEFT)
    
    addressentry = wx.TextCtrl(self, -1, practiceaddress, style=wx.TE_MULTILINE)
    leftsizer.Add(addressentry, 0, wx.EXPAND)
    
    postcodelabel = wx.StaticText(self, -1, self.t("clientpostcodelabel") + ": ")
    postcodelabel.SetFont(font)
    leftsizer.Add(postcodelabel, 0, wx.ALIGN_LEFT)
    
    postcodeentry = wx.TextCtrl(self, -1, practicepostcode)
    leftsizer.Add(postcodeentry, 0, wx.EXPAND)
    
    telephonelabel = wx.StaticText(self, -1, self.t("clientsearchphonelabel") + ": ")
    telephonelabel.SetFont(font)
    leftsizer.Add(telephonelabel, 0, wx.ALIGN_LEFT)
    
    telephoneentry = wx.TextCtrl(self, -1, practicetelephone)
    leftsizer.Add(telephoneentry, 0, wx.EXPAND)
    
    emaillabel = wx.StaticText(self, -1, self.t("clientemailaddresslabel") + ": ")
    emaillabel.SetFont(font)
    leftsizer.Add(emaillabel, 0, wx.ALIGN_LEFT)
    
    emailentry = wx.TextCtrl(self, -1, practiceemail)
    leftsizer.Add(emailentry, 0, wx.EXPAND)
    
    websitelabel = wx.StaticText(self, -1, self.t("websitelabel") + ": ")
    websitelabel.SetFont(font)
    leftsizer.Add(websitelabel, 0, wx.ALIGN_LEFT)
    
    websiteentry = wx.TextCtrl(self, -1, practicewebsite)
    leftsizer.Add(websiteentry, 0, wx.EXPAND)
    
    horizontalsizer.Add(leftsizer, 1, wx.EXPAND)
    
    horizontalsizer.Add(wx.StaticText(self, -1, "", size=(20,-1)), 0, wx.EXPAND)
    
    middlesizer = wx.BoxSizer(wx.VERTICAL)
    
    openfromlabel = wx.StaticText(self, -1, self.t("settingsopenfromlabel") + ": ")
    openfromlabel.SetFont(font)
    middlesizer.Add(openfromlabel, 0, wx.ALIGN_LEFT)
    
    openfromentry = wx.TextCtrl(self, -1, openfrom)
    middlesizer.Add(openfromentry, 0, wx.EXPAND)
    
    opentolabel = wx.StaticText(self, -1, self.t("settingsopentolabel") + ": ")
    opentolabel.SetFont(font)
    middlesizer.Add(opentolabel, 0, wx.ALIGN_LEFT)
    
    opentoentry = wx.TextCtrl(self, -1, opento)
    middlesizer.Add(opentoentry, 0, wx.EXPAND)
    
    operationtimelabel = wx.StaticText(self, -1, self.t("settingsoperatingtimelabel") + ": ")
    operationtimelabel.SetFont(font)
    middlesizer.Add(operationtimelabel, 0, wx.ALIGN_LEFT)
    
    operationtimeentry = wx.TextCtrl(self, -1, operationtime)
    middlesizer.Add(operationtimeentry, 0, wx.EXPAND)
    
    handle_rota_by_day_check = wx.CheckBox(self, -1, self.t("settingshandlerotabydaylabel") + ": ", style = wx.ALIGN_RIGHT)
    handle_rota_by_day_check.SetToolTipString(self.t("settingshandlerotabydaytooltip"))
    handle_rota_by_day_check.SetValue(handle_rota_by_day == 1)
    middlesizer.Add(handle_rota_by_day_check, 0, wx.EXPAND)
    
    prescriptionfeelabel = wx.StaticText(self, -1, self.t("prescriptionfeelabel") + ": ")
    prescriptionfeelabel.SetFont(font)
    middlesizer.Add(prescriptionfeelabel, 0, wx.ALIGN_LEFT)
    
    prescriptionfeeentry = wx.TextCtrl(self, -1, miscmethods.FormatPrice(self.localsettings.prescriptionfee))
    middlesizer.Add(prescriptionfeeentry, 0, wx.EXPAND)
    
    middlesizer.Add(wx.StaticText(self, -1, "", size=(-1,20)), 0, wx.EXPAND)
    
    asmshelterlabel = wx.StaticText(self, -1, self.t("asmshelterlabel") + ": ")
    asmshelterlabel.SetFont(font)
    middlesizer.Add(asmshelterlabel, 0, wx.ALIGN_LEFT)
    
    asmsheltersizer = wx.BoxSizer(wx.HORIZONTAL)
    
    asmbitmap = wx.Bitmap("icons/asm.png")
    asmstaticbitmap = wx.StaticBitmap(self, -1, asmbitmap)
    asmsheltersizer.Add(asmstaticbitmap, 0, wx.ALIGN_CENTER)
    
    asmshelterentry = wx.TextCtrl(self, -1, self.t("nonelabel"), style=wx.TE_READONLY)
    asmshelterentry.SetToolTipString(self.t("asmsheltertooltip"))
    asmsheltersizer.Add(asmshelterentry, 1, wx.EXPAND)
    
    searchbitmap = wx.Bitmap("icons/search.png")
    asmshelterbutton = wx.BitmapButton(self, -1, searchbitmap)
    asmshelterbutton.Bind(wx.EVT_BUTTON, self.FindShelter)
    asmshelterbutton.SetToolTipString(self.t("searchlabel"))
    asmsheltersizer.Add(asmshelterbutton, 0, wx.EXPAND)
    
    middlesizer.Add(asmsheltersizer, 0, wx.EXPAND)
    
    asmvaccinationlabel = wx.StaticText(self, -1, self.t("asmvaccinationlabel") + ": ")
    asmvaccinationlabel.SetFont(font)
    middlesizer.Add(asmvaccinationlabel, 0, wx.ALIGN_LEFT)
    
    asmvaccinationsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    #asmbitmap = wx.Bitmap("icons/asm.png")
    asmstaticbitmap = wx.StaticBitmap(self, -1, asmbitmap)
    asmvaccinationsizer.Add(asmstaticbitmap, 0, wx.ALIGN_CENTER)
    
    asmvaccinationentry = wx.TextCtrl(self, -1, self.t("nonelabel"), style=wx.TE_READONLY)
    asmvaccinationentry.SetToolTipString(self.t("asmvaccinationtooltip"))
    asmvaccinationsizer.Add(asmvaccinationentry, 1, wx.EXPAND)
    
    searchbitmap = wx.Bitmap("icons/search.png")
    asmvaccinationbutton = wx.BitmapButton(self, -1, searchbitmap)
    asmvaccinationbutton.Bind(wx.EVT_BUTTON, self.FindVaccination)
    asmvaccinationbutton.SetToolTipString(self.t("searchlabel"))
    asmvaccinationsizer.Add(asmvaccinationbutton, 0, wx.EXPAND)
    
    middlesizer.Add(asmvaccinationsizer, 0, wx.EXPAND)
    
    horizontalsizer.Add(middlesizer, 1, wx.EXPAND)
    
    horizontalsizer.Add(wx.StaticText(self, -1, "", size=(20,-1)), 0, wx.EXPAND)
    
    rightsizer = wx.BoxSizer(wx.VERTICAL)
    
    languagelabel = wx.StaticText(self, -1, self.t("settingslanguagelabel") + ": ")
    languagelabel.SetFont(font)
    rightsizer.Add(languagelabel, 0, wx.ALIGN_LEFT)
    
    inp = open("language.py")
    filecontents = ""
    for a in inp.readlines():
      filecontents = filecontents + a
    inp.close()
    
    alternativelanguage = filecontents.split("####")[1]
    
    languageentry = wx.Choice(self, -1, choices=("British English", alternativelanguage))
    languageentry.SetSelection(language)
    rightsizer.Add(languageentry, 0, wx.EXPAND)
    
    appointmentrefreshlabel = wx.StaticText(self, -1, self.t("appointmentrefreshlabel") + ":")
    appointmentrefreshlabel.SetFont(font)
    rightsizer.Add(appointmentrefreshlabel, 0, wx.ALIGN_LEFT)
    
    appointmentrefreshentry = wx.TextCtrl(self, -1, str(self.localsettings.appointmentrefresh))
    rightsizer.Add(appointmentrefreshentry, 0, wx.EXPAND)
    
    rightsizer.Add(wx.StaticText(self, -1, "", size=(-1,20)), 0, wx.EXPAND)
    
    submitbutton = wx.Button(self, -1, self.t("submitlabel"))
    submitbutton.SetBackgroundColour("green")
    submitbutton.SetToolTipString(self.t("submitlabel"))
    submitbutton.Bind(wx.EVT_BUTTON, self.Submit)
    rightsizer.Add(submitbutton, 0, wx.ALIGN_CENTER_HORIZONTAL)
    
    horizontalsizer.Add(rightsizer, 1, wx.EXPAND)
    
    topsizer.Add(horizontalsizer, 1, wx.EXPAND)
    
    self.SetSizer(topsizer)
    
    self.nameentry = nameentry
    self.addressentry = addressentry
    self.postcodeentry = postcodeentry
    self.telephoneentry = telephoneentry
    self.emailentry = emailentry
    self.websiteentry = websiteentry
    self.openfromentry = openfromentry
    self.opentoentry = opentoentry
    self.operationtimeentry = operationtimeentry
    self.handle_rota_by_day_check = handle_rota_by_day_check
    self.asmshelterentry = asmshelterentry
    self.asmvaccinationentry = asmvaccinationentry
    self.asmvaccinationbutton = asmvaccinationbutton
    self.languageentry = languageentry
    self.appointmentrefreshentry = appointmentrefreshentry
    self.prescriptionfeeentry = prescriptionfeeentry
    self.notebook = notebook
    
    self.UpdateShelterName()
    self.UpdateShelterVaccination()
  
  def FindShelter(self, ID):
    
    self.clientdialogid = 0
    
    clientid = clientmethods.FindClientDialog(self, self.localsettings)
    
    if self.clientdialogid > 0:
      
      self.localsettings.shelterid = self.clientdialogid
      
      action = "UPDATE settings SET ShelterID = " + str(self.clientdialogid)
      db.SendSQL(action, self.localsettings.dbconnection)
      
      self.UpdateShelterName()
  
  def FindVaccination(self, ID):
    
    dialog = wx.Dialog(self, -1, self.t("asmvaccinationlabel"))
    
    dialogsizer = wx.BoxSizer(wx.VERTICAL)
    
    panel = wx.Panel(dialog)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    listbox = wx.ListBox(panel, size=(300,200))
    listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.VaccinationSelected)
    listbox.SetToolTipString(self.t("doubleclicktoselecttooltip"))
    topsizer.Add(listbox, 1, wx.EXPAND)
    
    panel.SetSizer(topsizer)
    
    dialogsizer.Add(panel, 1, wx.EXPAND)
    
    dialog.SetSizer(dialogsizer)
    
    dialog.Fit()
    
    asmconnection = db.GetASMConnection()
    action = "SELECT ID, VaccinationType FROM vaccinationtype ORDER BY VaccinationType"
    results = db.SendSQL(action, asmconnection)
    asmconnection.close()
    
    for a in results:
      
      listbox.Append(a[1])
    
    panel.listbox = listbox
    panel.results = results
    
    dialog.ShowModal()
  
  def VaccinationSelected(self, ID):
    
    panel = ID.GetEventObject().GetParent()
    
    listboxid = panel.listbox.GetSelection()
    vaccinationid = panel.results[listboxid][0]
    
    self.asmvaccinationentry.SetValue(panel.results[listboxid][1])
    
    action = "UPDATE settings SET ASMVaccinationID = " + str(vaccinationid)
    db.SendSQL(action, self.localsettings.dbconnection)
    
    self.localsettings.asmvaccinationid = vaccinationid
    
    panel.GetParent().Close()
  
  def Submit(self, ID):
    
    name = self.nameentry.GetValue()
    address = self.addressentry.GetValue()
    postcode = self.postcodeentry.GetValue()
    telephone = self.telephoneentry.GetValue()
    email = self.emailentry.GetValue()
    website = self.websiteentry.GetValue()
    handle_rota_by_day = str(int(self.handle_rota_by_day_check.GetValue()))
    
    prescriptionfee = miscmethods.ConvertPriceToPennies(self.prescriptionfeeentry.GetValue())
    
    if prescriptionfee == -1:
      
      prescriptionfee = 0
    
    self.localsettings.prescriptionfee = prescriptionfee
    
    openfrom = self.openfromentry.GetValue()
    opento = self.opentoentry.GetValue()
    operationtime = self.operationtimeentry.GetValue()
    self.localsettings.language = self.languageentry.GetSelection()
    self.localsettings.appointmentrefresh = self.appointmentrefreshentry.GetValue()
    
    try:
      
      self.localsettings.appointmentrefresh = int(self.localsettings.appointmentrefresh)
      
    except:
      
      self.localsettings.appointmentrefresh = "30"
    
    if language != self.localsettings.language:
      
      home = miscmethods.GetHome()
      
      self.localsettings.SaveSettings(self.localsettings.username)
      #out = open(home + "/.evette.conf", "w")
      #out.write(self.localsettings.dbip + "\n" + self.localsettings.dbuser + "\n" + self.localsettings.dbpass + "\n\n" + self.localsettings.lastuser + "\n" + str(language))
      #out.close()
    
    action = "UPDATE settings SET PracticeName = \"" + name + "\", PracticeAddress = \"" + address + "\", PracticePostcode = \"" + postcode + "\", PracticeTelephone = \"" + telephone + "\", PracticeEmail = \"" + email + "\", PracticeWebsite = \"" + website + "\", OpenFrom = \"" + openfrom + "\", OpenTo = \"" + opento + "\", OperationTime = \"" + operationtime + "\", PrescriptionFee = " + str(prescriptionfee) + ", handle_rota_by_day = " + handle_rota_by_day
    
    db.SendSQL(action, self.localsettings.dbconnection)
    
    self.localsettings.SaveSettings(self.localsettings.username)
    
    self.notebook.ClosePage(self.notebook.activepage)
