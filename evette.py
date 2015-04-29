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
import clientmethods
import staffmethods
import settings
import db
import viewappointments
import sampledata
import miscmethods
import dbmethods
import lookupmethods
import medicationmethods
import proceduremethods
import staymethods
import formmethods
import wx.html
import searchmethods
import adminmethods
import rotamethods
import diarymethods
import fileassociationmethods
import appointmentmethods
import datetime
import customwidgets
import sys
import os
import recursivemethods
import animalmethods
import threading
import random
import lostandfound
import re

sound = False

ID_EXIT = 100
ADD_CLIENT = 101
FIND_CLIENT = 102
RESET_CLIENT_TABLES = 103
RESET_MEDICATION_TABLES = 104
VIEW_APPOINTMENTS = 105
EDIT_MEDICATION = 106
TIMER = 107
CREATE_RANDOM_CLIENTS = 108
VIEW_OPS = 109
EDIT_COLOURS = 110
RESET_COLOUR_TABLES = 111
RESET_BREED_TABLES = 112
EDIT_BREEDS = 113
RESET_SPECIES_TABLES = 114
EDIT_SPECIES = 115
ABOUT = 116
EDIT_ANIMALFORMS = 117
ID_SETTINGS = 118
HELP = 119
EDIT_PROCEDURES = 120
RESET_PROCEDURE_TABLES = 121
RESET_RECEIPT_TABLES = 122
TRACE_BATCH = 123
EDIT_STAFF = 124
EDIT_ROTA = 125
EDIT_SETTINGS = 126
RANDOM_DATA = 127
RESET_ALL = 128
BATCH_SEARCH = 129
APPOINTMENT_SEARCH = 130
MAIL_SHOT = 131
EDIT_DIARY = 132
ADD_TO_DIARY = 133
SHOW_LICENSE = 134
FILE_TYPES = 135
BROWSE_APPOINTMENTS = 136
EDIT_CLIENTFORMS = 137
EDIT_INVOICE = 138
EDIT_MEDICATIONFORMS = 139
EDIT_KENNELS = 140
VIEW_KENNELS = 141
ASM_IMPORT = 142
EDIT_REASONS = 143
CLOSE_EVETTE = 144
CLOSE_ALL_WINDOWS = 145
SOUND_EFFECT = 146
ASM_CLIENT_IMPORT = 147
EDIT_MARKUP = 148
LOST_AND_FOUND = 149
ADD_LOST = 150
ADD_FOUND = 151
VIEW_GROOMING = 152

class Evette:
  
  def t(self, field, index = 0):
    return self.localsettings.t(field,index)
  
  def __init__(self, parent, userid):
    
    busy = wx.BusyCursor()
    
    frame = wx.Frame(None, -1, "")
    frame.Bind(wx.EVT_CLOSE, self.CloseEvette)
    iconFile = "icons/evette.ico"
    icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
    frame.SetIcon(icon1)
    
    self.localsettings = settings.settings(userid)
    self.localsettings.GetSettings()
    
    frame.SetTitle("Evette - " + self.localsettings.username + "@"  + self.localsettings.practicename + " (" + self.localsettings.userposition + ")")
    
    if self.localsettings.startup_size and re.match("^\d{3,5}x\d{3,5}$", self.localsettings.startup_size):
      w, h = self.localsettings.startup_size.split('x')
      frame.SetSize((int(w),int(h)))
      frame.CentreOnScreen()
    else:
      frame.Maximize(True)

    panel = wx.Panel(frame)
    #panel.Bind(wx.EVT_CLOSE, self.CloseEvette)
    
    frame.mainfilemenu = wx.Menu()
    
    closeallwindowsmenuitem = wx.MenuItem(frame.mainfilemenu, CLOSE_ALL_WINDOWS, self.t("fileclosewindowsmenu") + "\tCTRL+W", self.t("fileclosewindowsmenu", 1))
    closeallwindowsmenuitem.SetBitmap(wx.Bitmap("icons/close.png"))
    frame.mainfilemenu.AppendItem(closeallwindowsmenuitem)
    wx.EVT_MENU(frame, CLOSE_ALL_WINDOWS, self.CloseAllWindows)
    
    if self.localsettings.editsettings == 1:
      
      editsettingsmenuitem = wx.MenuItem(frame.mainfilemenu, EDIT_SETTINGS, self.t("editsettingsmenu"), self.t("editsettingsmenu", 1))
      editsettingsmenuitem.SetBitmap(wx.Bitmap("icons/system.png"))
      frame.mainfilemenu.AppendItem(editsettingsmenuitem)
      wx.EVT_MENU(frame, EDIT_SETTINGS, self.EditSettings)
      
      editfiletypesmenuitem = wx.MenuItem(frame.mainfilemenu, FILE_TYPES, self.t("fileaccosiationmenu"), self.t("fileaccosiationmenu", 1))
      editfiletypesmenuitem.SetBitmap(wx.Bitmap("icons/filetypes.png"))
      frame.mainfilemenu.AppendItem(editfiletypesmenuitem)
      wx.EVT_MENU(frame, FILE_TYPES, self.EditFileAssociations)
      
      randomdatamenuitem = wx.MenuItem(frame.mainfilemenu, RANDOM_DATA, self.t("randomdatamenu"), self.t("randomdatamenu", 1))
      randomdatamenuitem.SetBitmap(wx.Bitmap("icons/caution.png"))
      frame.mainfilemenu.AppendItem(randomdatamenuitem)
      wx.EVT_MENU(frame, RANDOM_DATA, self.RandomData)
      
      resetdatabasemenuitem = wx.MenuItem(frame.mainfilemenu, RESET_ALL, self.t("resettablesmenu"), self.t("resettablesmenu", 1))
      resetdatabasemenuitem.SetBitmap(wx.Bitmap("icons/caution.png"))
      frame.mainfilemenu.AppendItem(resetdatabasemenuitem)
      wx.EVT_MENU(frame, RESET_ALL, self.ResetAllTables)
    
    quitmenuitem = wx.MenuItem(frame.mainfilemenu, CLOSE_EVETTE, self.t("fileexitmenu") + "\tCTRL+Q", self.t("fileexitmenu", 1))
    quitmenuitem.SetBitmap(wx.Bitmap("icons/quit.png"))
    frame.mainfilemenu.AppendItem(quitmenuitem)
    wx.EVT_MENU(frame, CLOSE_EVETTE, self.CloseEvette)
    
    #Creating the diary menu
    frame.diarymenu = wx.Menu()
    
    editdiarymenuitem = wx.MenuItem(frame.diarymenu, EDIT_DIARY, self.t("editdiarytoolbar") + "\tCTRL+D", self.t("editdiarytoolbar", 1))
    editdiarymenuitem.SetBitmap(wx.Bitmap("icons/diary.png"))
    frame.diarymenu.AppendItem(editdiarymenuitem)
    wx.EVT_MENU(frame, EDIT_DIARY, self.EditDiary)
    
    if self.localsettings.addtodiary == 1:
      
      addtodiarymenuitem = wx.MenuItem(frame.diarymenu, ADD_TO_DIARY, self.t("adddiarynotes") + "\tSHIFT+CTRL+D", self.t("adddiarynotes"))
      addtodiarymenuitem.SetBitmap(wx.Bitmap("icons/new.png"))
      frame.diarymenu.AppendItem(addtodiarymenuitem)
      wx.EVT_MENU(frame, ADD_TO_DIARY, self.NewDiaryNote)
    
    #Creating the client menu
    frame.clientmenu = wx.Menu()
    
    if self.localsettings.editclients == 1:
      
      
      addclientmenuitem = wx.MenuItem(frame.clientmenu, ADD_CLIENT, self.t("addclientmenu") + "\tCTRL+N", self.t("addclientmenu", 1))
      addclientmenuitem.SetBitmap(wx.Bitmap("icons/new.png"))
      frame.clientmenu.AppendItem(addclientmenuitem)
      wx.EVT_MENU(frame, ADD_CLIENT, self.AddClient)
      
      findclientsmenuitem = wx.MenuItem(frame.clientmenu, FIND_CLIENT, self.t("findclientmenu") + "\tCTRL+F", self.t("findclientmenu", 1))
      findclientsmenuitem.SetBitmap(wx.Bitmap("icons/search.png"))
      frame.clientmenu.AppendItem(findclientsmenuitem)
      wx.EVT_MENU(frame, FIND_CLIENT, self.FindClient)
      
      asmimportmenuitem = wx.MenuItem(frame.clientmenu, ASM_CLIENT_IMPORT, self.t("asmimportmenu") + "\tCTRL+I", self.t("asmimportmenu", 1))
      asmimportmenuitem.SetBitmap(wx.Bitmap("icons/asm.png"))
      frame.clientmenu.AppendItem(asmimportmenuitem)
      wx.EVT_MENU(frame, ASM_CLIENT_IMPORT, self.ASMImport)
      
      asmclientimportmenuitem = wx.MenuItem(frame.clientmenu, ASM_IMPORT, self.t("asmclientimportmenu") + "\tCTRL+SHIFT+I", self.t("asmclientimportmenu", 1))
      asmclientimportmenuitem.SetBitmap(wx.Bitmap("icons/asm.png"))
      frame.clientmenu.AppendItem(asmclientimportmenuitem)
      wx.EVT_MENU(frame, ASM_IMPORT, self.ASMClientImport)
      
      mailshotmenuitem = wx.MenuItem(frame.clientmenu, MAIL_SHOT, self.t("mailshotmenu"), self.t("mailshotmenu", 1))
      mailshotmenuitem.SetBitmap(wx.Bitmap("icons/mail.png"))
      frame.clientmenu.AppendItem(mailshotmenuitem)
      wx.EVT_MENU(frame, MAIL_SHOT, self.MailShot)
    
    #Create the file menu
    frame.filemenu = wx.Menu()
    
    if self.localsettings.editusers == 1:
      
      editstaffmenuitem = wx.MenuItem(frame.filemenu, EDIT_STAFF, self.t("editusersmenu"), self.t("editusersmenu", 1))
      editstaffmenuitem.SetBitmap(wx.Bitmap("icons/users.png"))
      frame.filemenu.AppendItem(editstaffmenuitem)
      wx.EVT_MENU(frame, EDIT_STAFF, self.EditStaff)
    
    if self.localsettings.editrota == 1:
      
      editrotamenuitem = wx.MenuItem(frame.filemenu, EDIT_ROTA, self.t("editrotamenu"), self.t("editrotamenu", 1))
      editrotamenuitem.SetBitmap(wx.Bitmap("icons/diary.png"))
      frame.filemenu.AppendItem(editrotamenuitem)
      wx.EVT_MENU(frame, EDIT_ROTA, self.EditRota)
    
    
    
    #Creating the appointment menu
    frame.appointmentmenu = wx.Menu()
    
    if self.localsettings.editappointments == 1:
      
      viewappointmentsmenuitem = wx.MenuItem(frame.appointmentmenu, VIEW_APPOINTMENTS, self.t("viewappointmentsmenu") + "\tCTRL+T", self.t("viewappointmentsmenu", 1))
      viewappointmentsmenuitem.SetBitmap(wx.Bitmap("icons/appointment.png"))
      frame.appointmentmenu.AppendItem(viewappointmentsmenuitem)
      wx.EVT_MENU(frame, VIEW_APPOINTMENTS, self.ViewAppointments)
      
      viewoperationsmenuitem = wx.MenuItem(frame.appointmentmenu, VIEW_OPS, self.t("viewoperationsmenu") + "\tSHIFT+CTRL+T", self.t("viewoperationsmenu", 1))
      viewoperationsmenuitem.SetBitmap(wx.Bitmap("icons/operation.png"))
      frame.appointmentmenu.AppendItem(viewoperationsmenuitem)
      wx.EVT_MENU(frame, VIEW_OPS, self.ViewOps)

      viewgroomingsmenuitem = wx.MenuItem(frame.appointmentmenu, VIEW_GROOMING, self.t("viewgroomingsmenu"), self.t("viewgroomingsmenu", 1))
      viewgroomingsmenuitem.SetBitmap(wx.Bitmap("icons/grooming.png"))
      frame.appointmentmenu.AppendItem(viewgroomingsmenuitem)
      wx.EVT_MENU(frame, VIEW_GROOMING, self.ViewGrooms)

      appointmentsearchmenuitem = wx.MenuItem(frame.appointmentmenu, APPOINTMENT_SEARCH, self.t("appointmentsearchmenu"), self.t("appointmentsearchmenu", 1))
      appointmentsearchmenuitem.SetBitmap(wx.Bitmap("icons/search.png"))
      frame.appointmentmenu.AppendItem(appointmentsearchmenuitem)
      wx.EVT_MENU(frame, APPOINTMENT_SEARCH, self.AppointmentSearch)
      
      browseappointmentsmenuitem = wx.MenuItem(frame.appointmentmenu, BROWSE_APPOINTMENTS, self.t("browseappointmentsmenu") + "\tCTRL+B", self.t("browseappointmentsmenu", 1))
      browseappointmentsmenuitem.SetBitmap(wx.Bitmap("icons/appointment.png"))
      frame.appointmentmenu.AppendItem(browseappointmentsmenuitem)
      wx.EVT_MENU(frame, BROWSE_APPOINTMENTS, self.BrowseAppointments)
    
    #Creating the kennels menu
    #frame.kennelsmenu = wx.Menu()
    
    
    #editkennelsmenuitem = wx.MenuItem(frame.kennelsmenu, EDIT_KENNELS, self.t("editkennelsmenu"), self.t("editkennelsmenu", 1))
    #editkennelsmenuitem.SetBitmap(wx.Bitmap("icons/edit.png"))
    #frame.kennelsmenu.AppendItem(editkennelsmenuitem)
    #wx.EVT_MENU(frame, EDIT_KENNELS, self.EditKennels)
    
    #browsekennelsmenuitem = wx.MenuItem(frame.kennelsmenu, VIEW_KENNELS, self.t("viewkennelsmenu") + "\tCTRL+K", self.t("viewkennelsmenu"))
    #browsekennelsmenuitem.SetBitmap(wx.Bitmap("icons/kennel.png"))
    #frame.kennelsmenu.AppendItem(browsekennelsmenuitem)
    #wx.EVT_MENU(frame, VIEW_KENNELS, self.ViewKennels)
    
    #Creating the medication database menu
    frame.medicationdatabasemenu = wx.Menu()
    
    if self.localsettings.editmedication == 1:
      
      editstockmenuitem = wx.MenuItem(frame.medicationdatabasemenu, EDIT_MEDICATION, self.t("editstockmenu") + "\tCTRL+S", self.t("editstockmenu", 1))
      editstockmenuitem.SetBitmap(wx.Bitmap("icons/edit.png"))
      frame.medicationdatabasemenu.AppendItem(editstockmenuitem)
      wx.EVT_MENU(frame, EDIT_MEDICATION, self.EditMedication)
      
      batchsearchmenuitem = wx.MenuItem(frame.medicationdatabasemenu, BATCH_SEARCH, self.t("batchsearchmenu"), self.t("batchsearchmenu", 1))
      batchsearchmenuitem.SetBitmap(wx.Bitmap("icons/search.png"))
      frame.medicationdatabasemenu.AppendItem(batchsearchmenuitem)
      wx.EVT_MENU(frame, BATCH_SEARCH, self.GetBatchNo)
      
      editmarkupmenuitem = wx.MenuItem(frame.medicationdatabasemenu, EDIT_MARKUP, self.t("editmarkupmenu"), self.t("editmarkupmenu", 1))
      editmarkupmenuitem.SetBitmap(wx.Bitmap("icons/edit.png"))
      frame.medicationdatabasemenu.AppendItem(editmarkupmenuitem)
      wx.EVT_MENU(frame, EDIT_MARKUP, self.EditMarkUp)
    
    #Creating the procedures  menu
    frame.proceduresmenu = wx.Menu()
    
    #Creating the lookups menu
    frame.lookupsmenu = wx.Menu()
    
    if self.localsettings.editlookups == 1:
      
      #Adding items to lookups menu
      editcoloursmenuitem = wx.MenuItem(frame.lookupsmenu, EDIT_COLOURS, self.t("editcoloursmenu"), self.t("editcoloursmenu", 1))
      editcoloursmenuitem.SetBitmap(wx.Bitmap("icons/edit.png"))
      frame.lookupsmenu.AppendItem(editcoloursmenuitem)
      wx.EVT_MENU(frame, EDIT_COLOURS, self.EditColours)
      
      editbreedsmenuitem = wx.MenuItem(frame.lookupsmenu, EDIT_BREEDS, self.t("editbreedsmenu"), self.t("editbreedsmenu", 1))
      editbreedsmenuitem.SetBitmap(wx.Bitmap("icons/edit.png"))
      frame.lookupsmenu.AppendItem(editbreedsmenuitem)
      wx.EVT_MENU(frame, EDIT_BREEDS, self.EditBreeds)
      
      editspeciesmenuitem = wx.MenuItem(frame.lookupsmenu, EDIT_SPECIES, self.t("editspeciesmenu"), self.t("editspeciesmenu", 1))
      editspeciesmenuitem.SetBitmap(wx.Bitmap("icons/edit.png"))
      frame.lookupsmenu.AppendItem(editspeciesmenuitem)
      wx.EVT_MENU(frame, EDIT_SPECIES, self.EditSpecies)
      
      editreasonsmenuitem = wx.MenuItem(frame.lookupsmenu, EDIT_REASONS, self.t("editreasonsmenu"), self.t("editreasonsmenu", 1))
      editreasonsmenuitem.SetBitmap(wx.Bitmap("icons/edit.png"))
      frame.lookupsmenu.AppendItem(editreasonsmenuitem)
      wx.EVT_MENU(frame, EDIT_REASONS, self.EditReasons)
    
    if self.localsettings.editprocedures == 1:
      
      editproceduresmenuitem = wx.MenuItem(frame.lookupsmenu, EDIT_PROCEDURES, self.t("editproceduresmenu"), self.t("editproceduresmenu", 1))
      editproceduresmenuitem.SetBitmap(wx.Bitmap("icons/edit.png"))
      frame.lookupsmenu.AppendItem(editproceduresmenuitem)
      wx.EVT_MENU(frame, EDIT_PROCEDURES, self.EditProcedures)
    
    #Creating the forms menu
    frame.formsmenu = wx.Menu()
    
    if self.localsettings.editforms == 1:
      
      editanimalformsmenuitem = wx.MenuItem(frame.formsmenu, EDIT_ANIMALFORMS, self.t("animalformsmenu"), self.t("animalformsmenu", 1))
      editanimalformsmenuitem.SetBitmap(wx.Bitmap("icons/form.png"))
      frame.formsmenu.AppendItem(editanimalformsmenuitem)
      wx.EVT_MENU(frame, EDIT_ANIMALFORMS, self.EditAnimalForms)
      
      editclientformsmenuitem = wx.MenuItem(frame.formsmenu, EDIT_CLIENTFORMS, self.t("clientformsmenu"), self.t("clientformsmenu", 1))
      editclientformsmenuitem.SetBitmap(wx.Bitmap("icons/form.png"))
      frame.formsmenu.AppendItem(editclientformsmenuitem)
      wx.EVT_MENU(frame, EDIT_CLIENTFORMS, self.EditClientForms)
      
      editmedicationformsmenuitem = wx.MenuItem(frame.formsmenu, EDIT_MEDICATIONFORMS, self.t("medicationformsmenu"), self.t("medicationformsmenu", 1))
      editmedicationformsmenuitem.SetBitmap(wx.Bitmap("icons/form.png"))
      frame.formsmenu.AppendItem(editmedicationformsmenuitem)
      wx.EVT_MENU(frame, EDIT_MEDICATIONFORMS, self.EditMedicationForms)
      
      editinvoicesmenuitem = wx.MenuItem(frame.formsmenu, EDIT_INVOICE, self.t("invoiceformsmenu"), self.t("invoiceformsmenu", 1))
      editinvoicesmenuitem.SetBitmap(wx.Bitmap("icons/form.png"))
      frame.formsmenu.AppendItem(editinvoicesmenuitem)
      wx.EVT_MENU(frame, EDIT_INVOICE, self.EditInvoice)
    
    #Creating the lost and found menu
    frame.lostandfoundmenu = wx.Menu()
    
    addlostmenuitem = wx.MenuItem(frame.
    lostandfoundmenu, ADD_LOST, self.t("addlostmenu") + "\tCTRL+SHIFT+L", self.t("addlostmenu", 1))
    wx.EVT_MENU(frame, ADD_LOST, self.AddLost)
    addlostmenuitem.SetBitmap(wx.Bitmap("icons/lostandfound.png"))
    frame.lostandfoundmenu.AppendItem(addlostmenuitem)
    
    addfoundmenuitem = wx.MenuItem(frame.
    lostandfoundmenu, ADD_FOUND, self.t("addfoundmenu") + "\tCTRL+SHIFT+F", self.t("addfoundmenu", 1))
    wx.EVT_MENU(frame, ADD_FOUND, self.AddFound)
    addfoundmenuitem.SetBitmap(wx.Bitmap("icons/lostandfound.png"))
    frame.lostandfoundmenu.AppendItem(addfoundmenuitem)
    
    lostandfoundmenuitem = wx.MenuItem(frame.
    lostandfoundmenu, LOST_AND_FOUND, self.t("lostandfoundmenu") + "\tCTRL+L", self.t("lostandfoundmenu", 1))
    wx.EVT_MENU(frame, LOST_AND_FOUND, self.LostAndFound)
    lostandfoundmenuitem.SetBitmap(wx.Bitmap("icons/lostandfound.png"))
    frame.lostandfoundmenu.AppendItem(lostandfoundmenuitem)
    
    #Creating the about menu
    frame.helpmenu = wx.Menu()
    
    helpmenuitem = wx.MenuItem(frame.
    helpmenu, HELP, self.t("gethelpmenu"), self.t("gethelpmenu", 1))
    wx.EVT_MENU(frame, HELP, self.Help)
    helpmenuitem.SetBitmap(wx.Bitmap("icons/help.png"))
    frame.helpmenu.AppendItem(helpmenuitem)
    
    aboutmenuitem = wx.MenuItem(frame.helpmenu, ABOUT, self.t("aboutmenu"), self.t("aboutmenu", 1))
    aboutmenuitem.SetBitmap(wx.Bitmap("icons/help.png"))
    frame.helpmenu.AppendItem(aboutmenuitem)
    wx.EVT_MENU(frame, ABOUT, self.About)
    
    showlicensemenuitem = wx.MenuItem(frame.helpmenu, SHOW_LICENSE, self.t("viewlicensemenu"), self.t("viewlicensemenu", 1))
    showlicensemenuitem.SetBitmap(wx.Bitmap("icons/help.png"))
    frame.helpmenu.AppendItem(showlicensemenuitem)
    wx.EVT_MENU(frame, SHOW_LICENSE, self.ViewLicense)
    
    frame.soundmenu = wx.Menu()
    
    frame.soundmenu.Append(SOUND_EFFECT, "Sound Effect\tF1", "Generate a humourous sound effect")
    wx.EVT_MENU(frame, SOUND_EFFECT, self.SoundEffect)
    
    #Creating the menubar
    frame.menubar = wx.MenuBar()
    
    #Adding the menus to the menubar
    frame.menubar.Append(frame.mainfilemenu, self.t("systemlabel"))
    
    frame.menubar.Append(frame.diarymenu, self.t("diarymenu"))
    
    if self.localsettings.editclients == 1:
      frame.menubar.Append(frame.clientmenu, self.t("clientmenu"))
    if self.localsettings.editappointments == 1:
      frame.menubar.Append(frame.appointmentmenu, self.t("appointmentsmenu"))
    
    #frame.menubar.Append(frame.kennelsmenu, self.t("kennelsmenu"))
    
    if self.localsettings.editmedication == 1:
      frame.menubar.Append(frame.medicationdatabasemenu, self.t("stocklabel"))
    if self.localsettings.editlookups == 1 or self.localsettings.editprocedures == 1:
      frame.menubar.Append(frame.lookupsmenu, self.t("lookupsmenu"))
    if self.localsettings.editforms == 1:
      frame.menubar.Append(frame.formsmenu, self.t("formsmenu"))
    if self.localsettings.editusers == 1 or self.localsettings.editrota:
      frame.menubar.Append(frame.filemenu, self.t("staffmenu"))
    
    frame.menubar.Append(frame.lostandfoundmenu, self.t("lostandfoundmenu"))
    frame.menubar.Append(frame.helpmenu, self.t("helpmenu"))
    
    if sound is True:
      
      frame.menubar.Append(frame.soundmenu, "Sound")
    
    #Creating the main vertical sizer
    mainsizer = wx.BoxSizer(wx.VERTICAL)
        
    #Add a status bar
    frame.CreateStatusBar()
    
    #Adding the MenuBar to the Frame content
    frame.SetMenuBar(frame.menubar)
    
    if self.localsettings.toolbar == 1:
      
      #Creating the toolbar
      toolbarsizer = wx.BoxSizer(wx.HORIZONTAL)
      
      if self.localsettings.editclients == 1:
        
        self.bAddClient = wx.Button(panel, ADD_CLIENT, self.t("addclienttoolbar"))
        #self.bAddClient.SetBackgroundColour("#0000ff")
        self.bAddClient.SetForegroundColour("blue")
        
        font = self.bAddClient.GetFont()
        font.SetPointSize(font.GetPointSize() + 2)
        self.bAddClient.SetFont(font)
        
        self.bAddClient.SetToolTipString(self.t("addclienttoolbar", 1))
        self.bAddClient.Bind(wx.EVT_BUTTON, self.AddClient)
        toolbarsizer.Add(self.bAddClient, 0, wx.EXPAND)
        
        self.bViewClients = wx.Button(panel, FIND_CLIENT, self.t("findclienttoolbar"))
        #self.bViewClients.SetBackgroundColour("red")
        self.bViewClients.SetForegroundColour("red")
        
        font = self.bViewClients.GetFont()
        font.SetPointSize(font.GetPointSize() + 2)
        self.bViewClients.SetFont(font)
        
        self.bViewClients.SetToolTipString(self.t("findclienttoolbar", 1))
        self.bViewClients.Bind(wx.EVT_BUTTON, self.FindClient)
        toolbarsizer.Add(self.bViewClients, 0, wx.EXPAND)
      
      if self.localsettings.editappointments == 1:
        
        self.bViewAppointments = wx.Button(panel, VIEW_APPOINTMENTS, self.t("viewappointmentstoolbar"))
        #self.bViewAppointments.SetBackgroundColour("yellow")
        self.bViewAppointments.SetForegroundColour('#555555')
        
        font = self.bViewAppointments.GetFont()
        font.SetPointSize(font.GetPointSize() + 2)
        self.bViewAppointments.SetFont(font)
        
        self.bViewAppointments.SetToolTipString(self.t("viewappointmentstoolbar", 1))
        self.bViewAppointments.Bind(wx.EVT_BUTTON, self.ViewAppointments)
        toolbarsizer.Add(self.bViewAppointments, 0, wx.EXPAND)
        
        self.bViewOps = wx.Button(panel, VIEW_OPS, self.t("viewoperationstoolbar"))
        #self.bViewOps.SetBackgroundColour("green")
        self.bViewOps.SetForegroundColour("green")
        
        font = self.bViewOps.GetFont()
        font.SetPointSize(font.GetPointSize() + 2)
        self.bViewOps.SetFont(font)
        
        self.bViewOps.SetToolTipString(self.t("viewoperationstoolbar", 1))
        self.bViewOps.Bind(wx.EVT_BUTTON, self.ViewOps)
        toolbarsizer.Add(self.bViewOps, 0, wx.EXPAND)
        
        self.bViewGroom = wx.Button(panel, VIEW_GROOMING, self.t("viewgroomingstoolbar"))
        #self.bViewGroom.SetBackgroundColour("yellow")
        self.bViewGroom.SetForegroundColour('#555555')
        
        font = self.bViewGroom.GetFont()
        font.SetPointSize(font.GetPointSize() + 2)
        self.bViewGroom.SetFont(font)
        
        self.bViewGroom.SetToolTipString(self.t("viewgroomingstoolbar", 1))
        self.bViewGroom.Bind(wx.EVT_BUTTON, self.ViewGrooms)
        toolbarsizer.Add(self.bViewGroom, 0, wx.EXPAND)

      editdiarybutton = wx.Button(panel, -1, self.t("editdiarytoolbar"))
      editdiarybutton.SetToolTipString(self.t("editdiarytoolbar", 1))
      #editdiarybutton.SetBackgroundColour("#ffacfe")
      editdiarybutton.SetForegroundColour("#33acfe")
      font = editdiarybutton.GetFont()
      font.SetPointSize(font.GetPointSize() + 2)
      editdiarybutton.SetFont(font)
      editdiarybutton.Bind(wx.EVT_BUTTON, self.EditDiary)
      toolbarsizer.Add(editdiarybutton, 0, wx.EXPAND)
      
      editstockbutton = wx.Button(panel, -1, self.t("editstockmenu"))
      editstockbutton.SetToolTipString(self.t("editstockmenu", 1))
      #editstockbutton.SetBackgroundColour("blue")
      editstockbutton.SetForegroundColour("black")
      font = editstockbutton.GetFont()
      font.SetPointSize(font.GetPointSize() + 2)
      editstockbutton.SetFont(font)
      editstockbutton.Bind(wx.EVT_BUTTON, self.EditMedication)
      toolbarsizer.Add(editstockbutton, 0, wx.EXPAND)
      
      sizerpanel = wx.Panel(panel)
      toolbarsizer.Add(sizerpanel, 1, wx.EXPAND)
      
      
      mainsizer.Add(toolbarsizer, 0, wx.EXPAND)
    
    #Creating the Notebook
    self.notebook = customwidgets.Notebook(panel, self.localsettings)
    self.frame = frame
    
    mainsizer.Add(self.notebook, 1, wx.EXPAND)
    
    panel.SetSizer(mainsizer)
    
    if str(sys.platform)[:3] == "win":
                        frame.Freeze()
                        framesize = frame.GetSize()
                        frame.SetSize((1,1))
                        frame.SetSize(framesize)
                        frame.Thaw()
    
    del busy
    
    frame.Show()
  
  def AddLost(self, ID):
    
    lostanimaldata = lostandfound.LostAndFoundSettings(self.localsettings)
    lostanimaldata.lostorfound = 0
    
    newlostanimalpanel = lostandfound.EditLostAndFoundPanel(self.notebook, lostanimaldata)
    self.notebook.AddPage(newlostanimalpanel)
    
  def AddFound(self, ID):
    
    foundanimaldata = lostandfound.LostAndFoundSettings(self.localsettings)
    foundanimaldata.lostorfound = 1
    
    newfoundanimalpanel = lostandfound.EditLostAndFoundPanel(self.notebook, foundanimaldata)
    self.notebook.AddPage(newfoundanimalpanel)
  
  def CloseEvette(self, ID):
    
    tempfolder = miscmethods.GetHome() + "/.evette/temp"
    
    recursivemethods.EmptyFolder(tempfolder)
    self.logindialog.Show()
    wx.Frame.Destroy(self.frame)
  
  def ASMImport(self, ID):
    
    #print "Importing from ASM"
    
    busy = wx.BusyCursor()
    
    asmconnection = db.GetASMConnection()
    
    dialog = wx.Dialog(self.notebook, -1, self.GetMenu("chooseananimaltitle"))
    
    iconFile = "icons/asm.ico"
    icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
    dialog.SetIcon(icon1)
    
    dialogsizer = wx.BoxSizer(wx.VERTICAL)
    
    panel = wx.Panel(dialog)
    
    topsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    inputsizer = wx.BoxSizer(wx.VERTICAL)
    
    refnolabel = wx.StaticText(panel, -1, self.t("clientrefnolabel"))
    font = refnolabel.GetFont()
    font.SetPointSize(font.GetPointSize() - 2)
    refnolabel.SetFont(font)
    inputsizer.Add(refnolabel, 0, wx.ALIGN_LEFT)
    
    refnoentry = wx.TextCtrl(panel, -1, "", style=wx.TE_PROCESS_ENTER)
    refnoentry.Bind(wx.EVT_CHAR, self.ASMImportButtonPressed)
    inputsizer.Add(refnoentry, 0, wx.EXPAND)
    
    namelabel = wx.StaticText(panel, -1, self.t("namelabel"))
    namelabel.SetFont(font)
    inputsizer.Add(namelabel, 0, wx.ALIGN_LEFT)
    
    nameentry = wx.TextCtrl(panel, -1, "", size=(100,-1), style=wx.TE_PROCESS_ENTER)
    nameentry.SetFocus()
    nameentry.Bind(wx.EVT_CHAR, self.ASMImportButtonPressed)
    inputsizer.Add(nameentry, 0, wx.EXPAND)
    
    specieslabel = wx.StaticText(panel, -1, self.t("animalspecieslabel"))
    specieslabel.SetFont(font)
    inputsizer.Add(specieslabel, 0, wx.ALIGN_LEFT)
    
    speciesentry = wx.TextCtrl(panel, -1, "", size=(100,-1), style=wx.TE_PROCESS_ENTER)
    speciesentry.Bind(wx.EVT_CHAR, self.ASMImportButtonPressed)
    inputsizer.Add(speciesentry, 0, wx.EXPAND)
    
    locationlabel = wx.StaticText(panel, -1, self.t("locationlabel"))
    locationlabel.SetFont(font)
    inputsizer.Add(locationlabel, 0, wx.ALIGN_LEFT)
    
    locationchoice = wx.Choice(panel, -1, choices=("On Shelter", "Adopted", "On Foster"), size=(100,-1))
    locationchoice.Bind(wx.EVT_CHAR, self.ASMImportButtonPressed)
    locationchoice.SetSelection(0)
    inputsizer.Add(locationchoice, 0, wx.EXPAND)
    
    inputsizer.Add(wx.StaticText(panel, -1, "", size=(-1,10)), 0, wx.EXPAND)
    
    topsizer.Add(inputsizer, 0, wx.EXPAND)
    
    topsizer.Add(wx.StaticText(panel, -1, "", size=(10,-1)), 0, wx.EXPAND)
    
    resultssizer = wx.BoxSizer(wx.VERTICAL)
    
    listbox = customwidgets.ASMAnimalListbox(panel, self.localsettings)
    listbox.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.SubmitASMImport)
    listbox.SetToolTipString(self.t("doubleclicktoselecttooltip"))
    customwidgets.ListCtrlWrapper.RefreshList(listbox)
    resultssizer.Add(listbox, 1, wx.EXPAND)
    
    totallabel = wx.StaticText(panel, -1, self.t("totallabel") + ": 0 ")
    resultssizer.Add(totallabel, 0, wx.ALIGN_RIGHT)
    
    topsizer.Add(resultssizer, 1, wx.EXPAND)
    
    panel.SetSizer(topsizer)
    
    panel.refnoentry = refnoentry
    panel.nameentry = nameentry
    panel.speciesentry = speciesentry
    panel.locationchoice = locationchoice
    
    panel.totallabel = totallabel
    panel.resultssizer = resultssizer
    
    panel.asmconnection = asmconnection
    
    panel.listbox = listbox
    
    dialogsizer.Add(panel, 1, wx.EXPAND)
    
    dialog.SetSizer(dialogsizer)
    
    dialog.SetSize((600,400))
    
    del busy
    
    dialog.ShowModal()
  
  def ASMImportButtonPressed(self, ID):
    
    keycode = ID.GetKeyCode()
    
    if keycode == 13:
      
      self.ASMAnimalSearch(ID)
      
    elif keycode == 15:
      
      self.SubmitASMImport(ID)
    
    ID.Skip()
  
  def ASMAnimalSearch(self, ID):
    
    panel = ID.GetEventObject().GetParent()
    panel.listbox.RefreshList()
  
  def SubmitASMImport(self, ID):
    
    panel = ID.GetEventObject().GetGrandParent()
    
    listboxid = panel.listbox.GetSelection()
    
    if listboxid != -1:
      
      animaldata = panel.animaldata[listboxid]
      
      action = "SELECT ID FROM animal WHERE ASMRef = \"" + animaldata[0] + "\""
      results = db.SendSQL(action, self.localsettings.dbconnection)
      
      if len(results) > 0:
        
        if miscmethods.ConfirmMessage(self.t("alreadyimportedmessage"), self.notebook):
          
          animalsettings = animalmethods.AnimalSettings(self.localsettings, False, results[0][0])
          
          animalpanel = animalmethods.AnimalPanel(self.notebook, animalsettings)
          
          self.notebook.AddPage(animalpanel)
          
          panel.GetParent().Close()
        
      else:
        
        archived = animaldata[10]
        activemovementtype = animaldata[11]
        
        if archived == 0 or activemovementtype == 2:
          
          action = "SELECT ShelterID FROM settings"
          clientid = db.SendSQL(action, self.localsettings.dbconnection)[0][0]
          
          #miscmethods.ShowMessage("Animal is on shelter", panel)
          
        else:
          
          action = "SELECT owner.OwnerSurname, owner.OwnerAddress, owner.OwnerPostcode, owner.HomeTelephone, owner.MobileTelephone, owner.WorkTelephone, owner.EmailAddress, animal.ActiveMovementType, owner.OwnerTitle, owner.OwnerForenames FROM owner INNER JOIN adoption ON adoption.OwnerID = owner.ID INNER JOIN animal ON adoption.ID = animal.ActiveMovementID WHERE animal.ShelterCode = \"" + animaldata[0] + "\" AND ( animal.ActiveMovementType = 1 OR animal.ActiveMovementType = 2 ) AND animal.Archived = 1"
          results = db.SendSQL(action, panel.asmconnection)
          
          if len(results) == 1:
            
            ownersurname = results[0][0]
            
            if ownersurname == None:
              
              ownersurname = ""
            
            owneraddress = results[0][1]
            
            if owneraddress == None:
              
              owneraddress = ""
            
            owneraddress = owneraddress.replace("\r", "")
            
            ownerpostcode = results[0][2]
            
            if ownerpostcode == None:
              
              ownerpostcode = ""
            
            ownerhometelephone = results[0][3]
            
            if ownerhometelephone == None:
              
              ownerhometelephone = ""
            
            ownermobiletelephone = results[0][4]
            
            if ownermobiletelephone == None:
              
              ownermobiletelephone = ""
            
            ownerworktelephone = results[0][5]
            
            if ownerworktelephone == None:
              
              ownerworktelephone = ""
            
            owneremailaddress = results[0][6]
            
            if owneremailaddress == None:
              
              owneremailaddress = ""
            
            movementtype = results[0][7]
            
            ownertitle = results[0][8]
            
            if ownertitle == None:
              
              ownertitle = ""
            
            ownerforenames = results[0][9]
            
            if ownerforenames == None:
              
              ownerforenames = ""
            
            action = "SELECT ID, ClientTitle, ClientForenames, ClientSurname, ClientAddress FROM client WHERE ClientPostCode = \"" + ownerpostcode + "\" OR ClientSurname = \"" + ownersurname + "\""
            evetteowners = db.SendSQL(action, self.localsettings.dbconnection)
            
            possiblematches = []
            
            asmhousenumber = owneraddress.split(" ")[0]
            
            for a in evetteowners:
              
              evettehousenumber = a[4].split(" ")[0]
              
              if asmhousenumber == evettehousenumber:
                
                possiblematches.append(a)
                
              else:
                
                if ownerforenames == "" or a[2] == "" or ownerforenames == a[2]:
                  
                  possiblematches.append(a)
            
            selectedownerid = 0
            
            panel.chosenownerid = 0
            
            if len(possiblematches) > 0:
              
              panel.possiblematches = possiblematches
              
              dialog = wx.Dialog(panel, -1, "Possible Owners")
              
              dialog.panel = panel
              
              topsizer = wx.BoxSizer(wx.VERTICAL)
              
              sheltermanagerownerinfo = wx.StaticText(dialog, -1, ownertitle + " " + ownerforenames + " " + ownersurname + ". " + owneraddress.replace("\n", ", ") + ". " + ownerpostcode)
              
              topsizer.Add(sheltermanagerownerinfo, 0, wx.EXPAND)
              
              topsizer.Add(wx.StaticText(dialog, -1, "", size=(-1,10)))
              
              chooseownerlabel = wx.StaticText(dialog, -1, "Choose an owner")
              topsizer.Add(chooseownerlabel, 0, wx.ALIGN_LEFT)
              
              dialog.listbox = wx.ListBox(dialog)
              dialog.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.SelectOwner)
              
              for v in possiblematches:
                
                listboxoutput = v[1] + " " + v[2] + " " + v[3] + ". " + v[4].replace("\n", ", ").replace("\r", "")
                
                dialog.listbox.Append(listboxoutput)
              
              topsizer.Add(dialog.listbox, 1, wx.EXPAND)
              
              dialog.SetSizer(topsizer)
              
              
              
              dialog.ShowModal()
              
              clientid = panel.chosenownerid
              
            if panel.chosenownerid == 0:
              
              clientsettings = clientmethods.ClientSettings(self.localsettings)
              
              clientsettings.title = ownertitle
              clientsettings.forenames = ownerforenames
              clientsettings.surname = ownersurname
              clientsettings.address = owneraddress
              clientsettings.postcode = ownerpostcode
              clientsettings.hometelephone = ownerhometelephone
              clientsettings.mobiletelephone = ownermobiletelephone
              clientsettings.worktelephone = ownerworktelephone
              clientsettings.emailaddress = owneremailaddress
              clientsettings.comments = "Imported from ASM"
              
              clientsettings.Submit()
              
              clientid = clientsettings.ID
            
          else:
            
            clientid = 0
        
        if clientid > 0:
          
          animalsettings = animalmethods.AnimalSettings(self.localsettings, clientid)
          
          animalsettings.name = animaldata[1]
##          print "animaldata[2] = " + str(animaldata[2])
##          if animaldata[2] == 0:
##                                                animalsettings.sex = 2
##                                        elif animaldata[2] == 1:
##                                                animalsettings.sex = 1
##                                        else:
##                                                animalsettings.sex = 0
##                                        
##                                        print "sex = " + str(animalsettings.sex)
                                        
          if animaldata[2] == self.t("malelabel"):

            animalsettings.sex = 1

          elif animaldata[2] == self.t("femalelabel"):

            animalsettings.sex = 2

          else:

            animalsettings.sex = 0
          
          animalsettings.species = animaldata[4]
          animalsettings.breed = animaldata[5]
          animalsettings.colour = animaldata[6]
          
          dob = animaldata[7]
          
          animalsettings.dob = miscmethods.FormatDate(dob, self.localsettings)
          
          animalsettings.comments = ""
          
          animalsettings.neutered = animaldata[3]
          animalsettings.chipno = animaldata[8]
          
          if animalsettings.chipno == None:
            
            animalsettings.chipno = ""
          
          if animalsettings.comments == None:
            
            animalsettings.comments = ""
          
          animalsettings.asmref = animaldata[0]
          
          animalsettings.Submit()
          
          animalpanel = animalmethods.AnimalPanel(self.notebook, animalsettings)
          
          self.notebook.AddPage(animalpanel)
          
          panel.GetParent().Close()
          
        else:
          
          miscmethods.ShowMessage(self.t("errorobtainingownermessage"), panel)
  
  def SelectOwner(self, ID):
    
    dialog = ID.GetEventObject().GetParent()
    
    listboxid = dialog.listbox.GetSelection()
    
    panel = dialog.panel
    
    panel.chosenownerid = panel.possiblematches[listboxid][0]
    
    dialog.Close()
  
  def ASMClientImport(self, ID):
    
    clientmethods.ASMClientImport(self.notebook, self.localsettings)
  
  def HotKey(self, ID):
    
    print "Hotkey: " + str(ID)
  
  def AddClient(self, ID):
    
    clientsettings = clientmethods.ClientSettings(self.localsettings)
    
    addclientpanel = clientmethods.ClientPanel(self.notebook, clientsettings)
    
    self.notebook.AddPage(addclientpanel)
    
    wx.CallAfter(addclientpanel.titleentry.SetFocus)
  
  def FindClient(self, ID=False):
    
    findclientpanel = searchmethods.SearchPanel(self.notebook, self.localsettings)
    
    self.notebook.AddPage(findclientpanel)
    
    wx.CallAfter(findclientpanel.nameentry.SetFocus)
  
  def EditStaff(self, ID):
    
    editstaffpanel = staffmethods.EditStaffPanel(self.notebook, self.localsettings)
    
    self.notebook.AddPage(editstaffpanel)
  
  def EditRota(self, ID):
    
    editrotapanel = rotamethods.EditRotaPanel(self.notebook, self.localsettings)
    
    self.notebook.AddPage(editrotapanel)
  
  def EditSettings(self, ID=False):
    
    settingspanel = settings.SettingsPanel(self.notebook, self.localsettings)
    
    self.notebook.AddPage(settingspanel)
  
  def ViewAppointments(self, ID=False):
    self.ViewAppPage("appointment", 0)
  
  def ViewAppPage(self, app_type, app_type_idx):
    
    pageno = -1
    
    for a in self.notebook.tabs:
      if a.pagetitle == self.t("view" + app_type + "spagetitle").replace(" ", u"\xa0"):
        pageno = a.image.ID
    
    if pageno == -1:
      appointmentpanel = viewappointments.ViewAppointments(self.notebook, self.localsettings, app_type_idx)
      self.notebook.AddPage(appointmentpanel)
      
    else:
      if self.notebook.activepage != pageno:
        self.notebook.tabsdropdown.SetSelection(pageno)
        self.notebook.PageSelected(-1, pageno)
  
  def ViewOps(self, ID=False):
    self.ViewAppPage('operation',1)
    
  def ViewGrooms(self, ev=False):
    self.ViewAppPage('grooming',2)
  
  def RandomData(self, ID=False):
    
    randomdatapanel = sampledata.RandomDataPanel(self.notebook, self.localsettings)
    
    self.notebook.AddPage(randomdatapanel)
  
  def ResetAllTables(self, ID=False):
    
    if miscmethods.ConfirmMessage(self.t("resetdatabasequestion")) == True:
      connection = db.GetConnection(self.localsettings)
      action = "DROP DATABASE evette"
      db.SendSQL(action, connection)
      connection.close()
      
      db.CreateDatabase(self.localsettings)
      
      miscmethods.ShowMessage(self.t("alltablesresetmessage"))
  
  def EditColours(self, ID):
    editcolourpanel = lookupmethods.EditLookup(self.notebook, "colour", self.localsettings)
    self.notebook.AddPage(editcolourpanel)
  
  def EditBreeds(self, ID):
    editbreedpanel = lookupmethods.EditLookup(self.notebook, "breed", self.localsettings)
    self.notebook.AddPage(editbreedpanel)
  
  def EditSpecies(self, ID):
    editspeciespanel = lookupmethods.EditLookup(self.notebook, "species", self.localsettings)
    self.notebook.AddPage(editspeciespanel)
  
  def EditReasons(self, ID):
    editreasonspanel = lookupmethods.EditLookup(self.notebook, "reason", self.localsettings)
    self.notebook.AddPage(editreasonspanel)
  
  def EditMedication(self, ID):
    editmedicationpanel = medicationmethods.EditMedicationPanel(self.notebook, self.localsettings)
    self.notebook.AddPage(editmedicationpanel)
  
  def EditProcedures(self, ID):
    editprocedurespanel = proceduremethods.EditProceduresPanel(self.notebook, self.localsettings)
    self.notebook.AddPage(editprocedurespanel)
  
  def EditVaccinations(self, ID):
    editvaccinationspanel = vaccinationmethods.EditVaccinationsPanel(self.notebook, self.localsettings)
    self.notebook.AddPage(editvaccinationspanel)
  
  def EditAnimalForms(self, ID):
    editformspanel = formmethods.AnimalFormEditor(self.notebook, self.localsettings)
    self.notebook.AddPage(editformspanel)
  
  def EditClientForms(self, ID):
    editformspanel = formmethods.ClientFormEditor(self.notebook, self.localsettings)
    self.notebook.AddPage(editformspanel)
  
  def EditMedicationForms(self, ID):
    editformspanel = formmethods.MedicationFormEditor(self.notebook, self.localsettings)
    self.notebook.AddPage(editformspanel)
  
  def EditInvoice(self, ID):
    editformspanel = formmethods.InvoiceEditor(self.notebook, self.localsettings)
    self.notebook.AddPage(editformspanel)
  
  def EditMarkUp(self, ID):
    
    editmarkuppanel = medicationmethods.EditMarkUp(self.notebook, self.localsettings)
  
  def Help(self, ID):
    
    helppanel = wx.Panel(self.notebook)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    helpwindow = wx.html.HtmlWindow(helppanel)
    topsizer.Add(helpwindow, 1, wx.EXPAND)
    
    helppanel.SetSizer(topsizer)
    
    helppanel.pagetitle = miscmethods.GetPageTitle(self.notebook, self.t("helpmenu"))
    helppanel.pageimage = "icons/help.png"
    
    self.notebook.AddPage(helppanel)
    
    helpwindow.LoadPage("html/index.html")
  
  def About(self, ID):
    
    aboutpanel = wx.Panel(self.notebook)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    aboutwindow = wx.html.HtmlWindow(aboutpanel)
    topsizer.Add(aboutwindow, 1, wx.EXPAND)
    
    aboutpanel.SetSizer(topsizer)
    
    aboutpanel.pagetitle = miscmethods.GetPageTitle(self.notebook, self.t("aboutlabel"))
    aboutpanel.pageimage = "icons/help.png"
    
    self.notebook.AddPage(aboutpanel)
    
    aboutwindow.LoadPage("html/about.html")
  
  def AppointmentSearch(self, ID):
    
    appointmentsearchpanel = searchmethods.AppointmentSearchPanel(self.notebook, self.localsettings)
    self.notebook.AddPage(appointmentsearchpanel)
  
  def MailShot(self, ID=False):
    
    mailshotpanel = adminmethods.MailShotPanel(self.notebook, self.localsettings)
    self.notebook.AddPage(mailshotpanel)
  
  def EditDiary(self, ID=False):
    
    diarypanel = diarymethods.EditDiaryPanel(self.notebook, self.localsettings)
    self.notebook.AddPage(diarypanel)
  
  def NewDiaryNote(self, ID=False):
    
    title = self.t("nolinklabel")
    diarynotepanel = diarymethods.DiaryNotePanel(self.notebook, self.localsettings, 0, 0, title, False, self)
    self.notebook.AddPage(diarynotepanel)
  
  def ViewLicense(self, ID=False):
    
    licensepanel = wx.Panel(self.notebook)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    licensewindow = wx.html.HtmlWindow(licensepanel)
    topsizer.Add(licensewindow, 1, wx.EXPAND)
    
    licensepanel.SetSizer(topsizer)
    
    licensepanel.pagetitle = miscmethods.GetPageTitle(self.notebook, self.t("licenselabel"))
    licensepanel.pageimage = "icons/help.png"
    
    self.notebook.AddPage(licensepanel)
    
    licensewindow.LoadPage("html/gpl.html")
  
  def EditFileAssociations(self, ID):
    
    filetypespanel = fileassociationmethods.FileTypePanel(self.notebook, self.localsettings)
    self.notebook.AddPage(filetypespanel)
  
  def EditKennels(self, ID):
    
    editkennelspanel = staymethods.EditKennelsPanel(self.notebook, self.localsettings)
    self.notebook.AddPage(editkennelspanel)
  
  def ViewKennels(self, ID):
    
    viewkennelspanel = staymethods.ViewKennelsPanel(self.notebook, self.localsettings)
    self.notebook.AddPage(viewkennelspanel)
  
  def LostAndFound(self, ID):
    
    lostandfoundpanel = lostandfound.LostAndFoundPanel(self.notebook, self.localsettings)
    self.notebook.AddPage(lostandfoundpanel)
    
  def BrowseAppointments(self, ID):
    
    today = datetime.date.today()
    
    month = today.month
    year = today.year
    
    browseappointmentspanel = appointmentmethods.BrowseAppointments(self.notebook, self.localsettings)
    self.notebook.AddPage(browseappointmentspanel)
  
  def GetBatchNo(self, ID):
    
    dialog = wx.Dialog(self.frame, -1, self.t("medicationbatchnolabel"))
    
    dialogsizer = wx.BoxSizer(wx.VERTICAL)
    
    panel = wx.Panel(dialog)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    topsizer.Add(wx.StaticText(panel, -1, self.t("medicationbatchnolabel")), 0, wx.ALIGN_LEFT)
    
    batchinput = wx.TextCtrl(panel, -1, "", size=(200,-1))
    topsizer.Add(batchinput, 0, wx.EXPAND)
    
    submitsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    containscheckbox = wx.CheckBox(panel, -1, self.t("containslabel").lower())
    submitsizer.Add(containscheckbox, 0, wx.ALIGN_CENTER)
    
    submitsizer.Add(wx.Panel(panel), 1, wx.EXPAND)
    
    submitbitmap = wx.Bitmap("icons/submit.png")
    submitbutton = wx.BitmapButton(panel, -1, submitbitmap)
    submitbutton.SetToolTipString(self.t("submitlabel"))
    submitbutton.Bind(wx.EVT_BUTTON, self.GenerateBatchMovementReport)
    submitsizer.Add(submitbutton, 0, wx.EXPAND)
    
    topsizer.Add(submitsizer, 0, wx.EXPAND)
    
    panel.SetSizer(topsizer)
    
    panel.batchinput = batchinput
    panel.containscheckbox = containscheckbox
    
    dialogsizer.Add(panel, 1, wx.EXPAND)
    
    dialog.SetSizer(dialogsizer)
    
    dialog.Fit()
    
    dialog.ShowModal()
  
  def GenerateBatchMovementReport(self, ID):
    
    busy = wx.BusyCursor()
    
    parent = ID.GetEventObject().GetParent()
    
    batchno = parent.batchinput.GetValue()
    
    if parent.containscheckbox.GetValue() == True:
      
      action = "SELECT medicationin.Date, medication.Name, medicationin.MedicationID, medicationin.Amount, medicationin.BatchNo, DATE_FORMAT(medicationin.Expires, \"%Y-%m-%d\"), medicationin.WhereFrom, 0, medication.Unit FROM medicationin INNER JOIN medication ON medicationin.MedicationID = medication.ID WHERE medicationin.BatchNo LIKE \"%" + str(batchno) + "%\""
      resultsin = db.SendSQL(action, self.localsettings.dbconnection)
      
      action = "SELECT medicationout.Date, medication.Name, medicationout.MedicationID, medicationout.Amount, medicationout.BatchNo, 0, medicationout.WhereTo, 1, medication.Unit FROM medicationout INNER JOIN medication ON medicationout.MedicationID = medication.ID WHERE medicationout.BatchNo LIKE \"%" + str(batchno) + "%\""
      resultsout = db.SendSQL(action, self.localsettings.dbconnection)
      
    else:
      
      action = "SELECT medicationin.Date, medication.Name, medicationin.MedicationID, medicationin.Amount, medicationin.BatchNo, DATE_FORMAT(medicationin.Expires, \"%Y-%m-%d\"), medicationin.WhereFrom, 0, medication.Unit FROM medicationin INNER JOIN medication ON medicationin.MedicationID = medication.ID WHERE medicationin.BatchNo = \"" + str(batchno) + "\""
      resultsin = db.SendSQL(action, self.localsettings.dbconnection)
      
      action = "SELECT medicationout.Date, medication.Name, medicationout.MedicationID, medicationout.Amount, medicationout.BatchNo, 0, medicationout.WhereTo, 1, medication.Unit FROM medicationout INNER JOIN medication ON medicationout.MedicationID = medication.ID WHERE medicationout.BatchNo = \"" + str(batchno) + "\""
      resultsout = db.SendSQL(action, self.localsettings.dbconnection)
    
    header = "<h1 align=center><u>" + self.t("medicationmovementsofbatchnumberlabel") + str(batchno) + "</u></h1><table align=center>"
    
    results = []
    
    for a in resultsin:
      results.append(a)
    for a in resultsout:
      results.append(a)
    
    results.sort()
    
    body = ""
    
    for a in results:
      
      date = miscmethods.GetDateFromSQLDate(a[0])
      date = miscmethods.FormatDate(date, self.localsettings)
      
      name = a[1]
      
      if a[7] == 0:
        fromorto = self.t("fromlabel").lower()
      else:
        fromorto = self.t("tolabel").lower()
      
      quantity = a[3]
      
      destination = a[6]
      
      body = body + "<tr><td valign=top>" + date + "</td><td valign=top>" + name + " x " + str(quantity) + " " + fromorto + " " + destination + "</td></tr>"
    
    footer = "</table>"
    
    formmethods.BuildForm(self.localsettings, header + body + footer)
    
    del busy
    
    parent.GetParent().Close()
  
  def CloseAllWindows(self, ID):
    
    if miscmethods.ConfirmMessage(self.t("confirmcloseallwindowsmessage"), self.frame):
      
      while len(self.notebook.pages) > 0:
        
        self.notebook.ClosePage(self.notebook.activepage, True)
  
  def SoundEffect(self, ID):
    
    SoundEffectThread()

class SoundEffectThread(threading.Thread):
  
  def __init__(self):
    
    threading.Thread.__init__(self)
    
    self.start()
  
  def run(self):
    
    tracks = os.listdir("audio")
    
    #tracks = []
    
    #for a in os.listdir("audio"):
      
      #if a.split(".")[-1].lower() == "mp3":
        
        #tracks.append(a)
    
    track = tracks[int(random.random() * len(tracks))]
    
    os.system("mplayer audio/" + track)
