#!?usr/bin/python
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
import re

ADD_USER = 1301
EDIT_USER = 1302
DELETE_USER = 1304
REFRESH_USERS = 1305

class GenericSettingsPanel(wx.Panel):
  
  def t(self, field, idx = 0):
    
    return self.localsettings.t(field,idx)
  
  def __init__(self, parent, title):
    
    self.localsettings = parent.GetParent().localsettings
    
    wx.Panel.__init__(self, parent)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    edit = wx.CheckBox(self, -1, self.t("editlabel"))
    edit.Bind(wx.EVT_CHECKBOX, self.EditChecked)
    topsizer.Add(edit, 0, wx.ALIGN_LEFT)
    
    delete = wx.CheckBox(self, -1, self.t("deletelabel"))
    delete.Bind(wx.EVT_CHECKBOX, self.DeleteChecked)
    topsizer.Add(delete, 0, wx.ALIGN_LEFT)
    
    self.SetSizer(topsizer)
    
    self.edit = edit
    self.delete = delete
  
  def DeleteChecked(self, ID):
    
    if self.delete.GetValue() == True:
      self.edit.SetValue(True)
  
  def EditChecked(self, ID):
    
    if self.edit.GetValue() == False:
      self.delete.SetValue(False)

class AppointmentSettingsPanel(wx.Panel):
  
  def t(self, field, idx = 0):
    
    return self.localsettings.t(field,idx)
  
  def __init__(self, parent, title):
    
    self.localsettings = parent.GetParent().localsettings
    
    wx.Panel.__init__(self, parent)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    edit = wx.CheckBox(self, -1, self.t("editlabel"))
    edit.Bind(wx.EVT_CHECKBOX, self.EditChecked)
    topsizer.Add(edit, 0, wx.ALIGN_LEFT)
    
    delete = wx.CheckBox(self, -1, self.t("deletelabel"))
    delete.Bind(wx.EVT_CHECKBOX, self.DeleteChecked)
    topsizer.Add(delete, 0, wx.ALIGN_LEFT)
    
    vetform = wx.CheckBox(self, -1, self.t("editvetformlabel"))
    vetform.Bind(wx.EVT_CHECKBOX, self.EditVetFormChecked)
    topsizer.Add(vetform, 0, wx.ALIGN_LEFT)
    
    self.SetSizer(topsizer)
    
    self.edit = edit
    self.delete = delete
    self.vetform = vetform
  
  def DeleteChecked(self, ID):
    
    if self.delete.GetValue() == True:
      self.edit.SetValue(True)
  
  def EditChecked(self, ID):
    
    if self.edit.GetValue() == False:
      self.delete.SetValue(False)
      self.vetform.SetValue(False)
  
  def EditVetFormChecked(self, ID):
    
    if self.vetform.GetValue() == True:
      self.edit.SetValue(True)

class ClientSettingsPanel(wx.Panel):
  
  def t(self, field, idx = 0):
    
    return self.localsettings.t(field,idx)
  
  def __init__(self, parent, title):
    
    self.localsettings = parent.GetParent().localsettings
    
    wx.Panel.__init__(self, parent)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    edit = wx.CheckBox(self, -1, self.t("editlabel"))
    edit.Bind(wx.EVT_CHECKBOX, self.EditChecked)
    topsizer.Add(edit, 0, wx.ALIGN_LEFT)
    
    delete = wx.CheckBox(self, -1, self.t("deletelabel"))
    delete.Bind(wx.EVT_CHECKBOX, self.DeleteChecked)
    topsizer.Add(delete, 0, wx.ALIGN_LEFT)
    
    editfinances = wx.CheckBox(self, -1, self.t("editfinanceslabel"))
    topsizer.Add(editfinances, 0, wx.ALIGN_LEFT)
    
    self.SetSizer(topsizer)
    
    self.edit = edit
    self.delete = delete
    self.editfinances = editfinances
  
  def DeleteChecked(self, ID):
    
    if self.delete.GetValue() == True:
      self.edit.SetValue(True)
  
  def EditChecked(self, ID):
    
    if self.edit.GetValue() == False:
      self.delete.SetValue(False)

class MiscSettingsPanel(wx.Panel):
  
  def t(self, field, idx = 0):
    
    return self.localsettings.t(field,idx)
  
  def __init__(self, parent, title):
    
    self.localsettings = parent.GetParent().localsettings
    
    wx.Panel.__init__(self, parent)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    toolbar = wx.CheckBox(self, -1, self.t("showtoolbarlabel"))
    topsizer.Add(toolbar, 0, wx.ALIGN_LEFT)
    
    changelog = wx.CheckBox(self, -1, self.t("viewchangeloglabel"))
    topsizer.Add(changelog, 0, wx.ALIGN_LEFT)
    
    editsettings = wx.CheckBox(self, -1, self.t("editsettingslabel"))
    topsizer.Add(editsettings, 0, wx.ALIGN_LEFT)
    
    multiplepanels = wx.CheckBox(self, -1, self.t("multiplepanellabel"))
    topsizer.Add(multiplepanels, 0, wx.ALIGN_LEFT)
    
    asmsync = wx.CheckBox(self, -1, self.t("synctoasmlabel"))
    topsizer.Add(asmsync, 0, wx.ALIGN_LEFT)
    
    self.SetSizer(topsizer)
    
    self.toolbar = toolbar
    self.changelog = changelog
    self.editsettings = editsettings
    self.multiplepanels = multiplepanels
    self.asmsync = asmsync

class DiarySettingsPanel(wx.Panel):
  
  def t(self, field, idx = 0):
    
    return self.localsettings.t(field,idx)
  
  def __init__(self, parent, title):
    
    self.localsettings = parent.GetParent().localsettings
    
    wx.Panel.__init__(self, parent)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    adddiarynotes = wx.CheckBox(self, -1, self.t("adddiarynotes"))
    topsizer.Add(adddiarynotes, 0, wx.ALIGN_LEFT)
    
    editdiarynotes = wx.CheckBox(self, -1, self.t("editdiarynotes"))
    topsizer.Add(editdiarynotes, 0, wx.ALIGN_LEFT)
    
    deletediarynotes = wx.CheckBox(self, -1, self.t("deletediarynotes"))
    topsizer.Add(deletediarynotes, 0, wx.ALIGN_LEFT)
    
    self.SetSizer(topsizer)
    
    self.adddiarynotes = adddiarynotes
    self.editdiarynotes = editdiarynotes
    self.deletediarynotes = deletediarynotes

class UserSettingsPanel(wx.Panel):
  
  def t(self, field, idx = 0):
    
    return self.localsettings.t(field,idx)
  
  def __init__(self, parent, title):
    
    self.localsettings = parent.GetParent().localsettings
    
    wx.Panel.__init__(self, parent)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    edit = wx.CheckBox(self, -1, self.t("editlabel"))
    edit.Bind(wx.EVT_CHECKBOX, self.EditChecked)
    topsizer.Add(edit, 0, wx.ALIGN_LEFT)
    
    delete = wx.CheckBox(self, -1, self.t("deletelabel"))
    delete.Bind(wx.EVT_CHECKBOX, self.DeleteChecked)
    topsizer.Add(delete, 0, wx.ALIGN_LEFT)
    
    editrota = wx.CheckBox(self, -1, self.t("editrotalabel"))
    topsizer.Add(editrota, 0, wx.ALIGN_LEFT)
    
    self.SetSizer(topsizer)
    
    self.edit = edit
    self.delete = delete
    self.editrota = editrota
  
  def DeleteChecked(self, ID):
    
    if self.delete.GetValue() == True:
      self.edit.SetValue(True)
  
  def EditChecked(self, ID):
    
    if self.edit.GetValue() == False:
      self.delete.SetValue(False)

class SchedulesTab(wx.Panel):

  def t(self, field, idx = 0):
    
    return self.localsettings.t(field,idx)
  
  def __init__(self, parent, title):
    
    self.localsettings = parent.GetParent().localsettings
    
    wx.Panel.__init__(self, parent)
    
    mon_sizer, mon_from_entry, mon_to_entry = self.Fields('monday')
    tue_sizer, tue_from_entry, tue_to_entry = self.Fields('tuesday')
    wed_sizer, wed_from_entry, wed_to_entry = self.Fields('wednesday')
    thu_sizer, thu_from_entry, thu_to_entry = self.Fields('thursday')
    fri_sizer, fri_from_entry, fri_to_entry = self.Fields('friday')
    sat_sizer, sat_from_entry, sat_to_entry = self.Fields('saturday')
    sun_sizer, sun_from_entry, sun_to_entry = self.Fields('sunday')

    week_sizer = wx.BoxSizer(wx.HORIZONTAL)
    week_sizer.Add(mon_sizer,0,wx.ALIGN_LEFT)
    week_sizer.Add(tue_sizer,0,wx.ALIGN_LEFT)
    week_sizer.Add(wed_sizer,0,wx.ALIGN_LEFT)
    week_sizer.Add(thu_sizer,0,wx.ALIGN_LEFT)
    week_sizer.Add(fri_sizer,0,wx.ALIGN_LEFT)
    week_sizer.Add(sat_sizer,0,wx.ALIGN_LEFT)
    week_sizer.Add(sun_sizer,0,wx.ALIGN_LEFT)
    self.SetSizer(week_sizer)
    
    self.mon_from_entry = mon_from_entry
    self.mon_to_entry = mon_to_entry
    self.tue_from_entry = tue_from_entry
    self.tue_to_entry = tue_to_entry
    self.wed_from_entry = wed_from_entry
    self.wed_to_entry = wed_to_entry
    self.thu_from_entry = thu_from_entry
    self.thu_to_entry = thu_to_entry
    self.fri_from_entry = fri_from_entry
    self.fri_to_entry = fri_to_entry
    self.sat_from_entry = sat_from_entry
    self.sat_to_entry = sat_to_entry
    self.sun_from_entry = sun_from_entry
    self.sun_to_entry = sun_to_entry
    
  def Field(self, from_or_to):
    
    field_label = wx.StaticText(self, -1, self.t(from_or_to) + ":")
    font = field_label.GetFont()
    font.SetPointSize(font.GetPointSize() - 2)
    field_label.SetFont(font)
    field_entry = wx.TextCtrl(self, -1, "", size=(100,-1))
    
    return [field_label,field_entry]
  
  def Fields(self, attr_name):
    field_sizer = wx.BoxSizer(wx.VERTICAL)
    
    field_label = wx.StaticText(self, -1, self.t(attr_name) + ":")
    
    field_from_label, field_from_entry = self.Field("from")
    field_to_label, field_to_entry = self.Field("to")
    
    field_sizer.Add(field_label, 0, wx.ALIGN_LEFT)
    field_sizer.Add(field_from_label, 0, wx.ALIGN_LEFT)
    field_sizer.Add(field_from_entry, 1, wx.EXPAND)
    field_sizer.Add(field_to_label, 0, wx.ALIGN_LEFT)
    field_sizer.Add(field_to_entry, 1, wx.EXPAND)

    return [field_sizer,field_from_entry,field_to_entry]
  
  def GetValues(self):
    schedules = {}
    
    if self.GetTimeValues('mon',schedules) is False:
      return 'mon'

    if self.GetTimeValues('tue',schedules) is False:
      return 'tue'

    if self.GetTimeValues('wed',schedules) is False:
      return 'wed'

    if self.GetTimeValues('thu',schedules) is False:
      return 'thu'

    if self.GetTimeValues('fri',schedules) is False:
      return 'fri'

    if self.GetTimeValues('sat',schedules) is False:
      return 'sat'
      
    if self.GetTimeValues('sun',schedules) is False:
      return 'sun'
    
    return schedules
  
  def GetTimeValues(self, day, schedules):
  
    from_val = getattr(self, day + "_from_entry").GetValue()
    to_val = getattr(self, day + "_to_entry").GetValue()
    
    from_val = re.sub('\D','',from_val).zfill(4) #format as HHMM
    if from_val[0:2] > '24' or from_val[2:4] > '60':
      return False

    to_val = re.sub('\D','',to_val).zfill(4)
    if to_val[0:2] > '24' or to_val[2:4] > '60':
      return False
    
    if from_val > to_val:
      return False
    
    schedules[day] = {'from': from_val, 'to': to_val}
    return True

class EditStaffPanel(wx.Panel):
  
  def t(self, field, idx = 0):
    
    return self.localsettings.t(field,idx)
  
  def __init__(self, notebook, localsettings):
    
    self.localsettings = localsettings
    
    self.pagetitle = miscmethods.GetPageTitle(notebook, self.t("editstaffpagetitle"))
    
    wx.Panel.__init__(self, notebook)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    userlist = wx.ListBox(self, -1)
    userlist.Bind(wx.EVT_RIGHT_DOWN, self.Popup)
    userlist.Bind(wx.EVT_LISTBOX_DCLICK, self.EditUser)
    topsizer.Add(userlist, 1, wx.EXPAND)
    
    self.SetSizer(topsizer)
    
    self.localsettings = self.localsettings
    self.userlist = userlist
    
    self.RefreshUsers()
  
  def Popup(self, ID):
    
    popupmenu = wx.Menu()
    
    add = wx.MenuItem(popupmenu, ADD_USER, self.t("addlabel"))
    add.SetBitmap(wx.Bitmap("icons/new.png"))
    popupmenu.AppendItem(add)
    wx.EVT_MENU(popupmenu, ADD_USER, self.AddUser)
    
    if self.userlist.GetSelection() > -1:
      
      edit = wx.MenuItem(popupmenu, EDIT_USER, self.t("editlabel"))
      edit.SetBitmap(wx.Bitmap("icons/edit.png"))
      popupmenu.AppendItem(edit)
      wx.EVT_MENU(popupmenu, EDIT_USER, self.EditUser)
      
      delete = wx.MenuItem(popupmenu, DELETE_USER, self.t("deletelabel"))
      delete.SetBitmap(wx.Bitmap("icons/delete.png"))
      popupmenu.AppendItem(delete)
      wx.EVT_MENU(popupmenu, DELETE_USER, self.DeleteUser)
    
    popupmenu.AppendSeparator()
    
    refresh = wx.MenuItem(popupmenu, REFRESH_USERS, self.t("refreshlabel"))
    refresh.SetBitmap(wx.Bitmap("icons/refresh.png"))
    popupmenu.AppendItem(refresh)
    wx.EVT_MENU(popupmenu, REFRESH_USERS, self.RefreshUsers)
    
    self.PopupMenu(popupmenu)
  
  def AddUser(self, ID):
    
    self.EditUserDialog()
  
  def EditUser(self, ID):
    
    listboxid = self.userlist.GetSelection()
    
    userid = self.users[listboxid]
    
    action = "SELECT * FROM user WHERE ID = " + str(userid)
    results = db.SendSQL(action, self.localsettings.dbconnection)
    
    self.EditUserDialog(results[0])
  
  def EditUserDialog(self, userdata=False):
    
    busy = wx.BusyCursor()
    
    action = "SELECT DISTINCT(Position) FROM user ORDER BY Position"
    results = db.SendSQL(action, self.localsettings.dbconnection)
    
    positions = [self.t('vetpositiontitle'), self.t('groomerpositiontitle'), self.t('managerpositiontitle'), self.t('vetnursepositiontitle')]
    
    for a in results:
      
      if positions.__contains__(a[0]) == False:
        
        positions.append(a[0])
    
    dialog = wx.Dialog(self, -1, self.t("edituserlabel"))
    
    dialogsizer = wx.BoxSizer(wx.VERTICAL)
    
    panel = wx.Panel(dialog)
    
    panel.userdata = userdata
    
    panel.localsettings = self.localsettings
    
    permissionssizer = wx.BoxSizer(wx.VERTICAL)
    
    permissionssizer.Add(wx.StaticText(panel, -1, "", size=(-1,10)), 0, wx.EXPAND)
    
    inputsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    namesizer = wx.BoxSizer(wx.VERTICAL)
    
    namelabel = wx.StaticText(panel, -1, self.t("namelabel") + ":")
    font = namelabel.GetFont()
    font.SetPointSize(font.GetPointSize() - 2)
    namelabel.SetFont(font)
    namesizer.Add(namelabel, 0, wx.ALIGN_LEFT)
    
    nameentry = wx.TextCtrl(panel, -1, "", size=(150,-1))
    namesizer.Add(nameentry, 1, wx.EXPAND)
    
    inputsizer.Add(namesizer, 0, wx.EXPAND)
    
    passwordsizer = wx.BoxSizer(wx.VERTICAL)
    
    passwordlabel = wx.StaticText(panel, -1, miscmethods.NoWrap(" " + self.t("passwordlabel") + ":"))
    passwordlabel.SetFont(font)
    passwordsizer.Add(passwordlabel, 0, wx.ALIGN_LEFT)
    
    passwordentry = wx.TextCtrl(panel, -1, "", size=(150,-1))
    passwordsizer.Add(passwordentry, 1, wx.EXPAND)
    
    inputsizer.Add(passwordsizer, 0, wx.EXPAND)
    
    positionsizer = wx.BoxSizer(wx.VERTICAL)
    
    positionlabel = wx.StaticText(panel, -1, miscmethods.NoWrap(" " + self.t("positionlabel") + ":"))
    positionlabel.SetFont(font)
    positionsizer.Add(positionlabel, 0, wx.ALIGN_LEFT)
    
    positionentry = wx.ComboBox(panel, -1, "", choices=positions)
    positionsizer.Add(positionentry, 1, wx.EXPAND)
    
    inputsizer.Add(positionsizer, 0, wx.EXPAND)
    
    permissionssizer.Add(inputsizer, 0, wx.EXPAND)
    
    permissionssizer.Add(wx.StaticText(panel, -1, "", size=(-1,10)), 0, wx.EXPAND)
    
    permissionsnotebook = wx.Notebook(panel)
    
    clientpermissions = ClientSettingsPanel(permissionsnotebook, self.t("clientslabel"))
    permissionsnotebook.AddPage(clientpermissions, self.t("clientslabel"), select=True)
    
    animalpermissions = GenericSettingsPanel(permissionsnotebook, self.t("animalslabel"))
    permissionsnotebook.AddPage(animalpermissions, self.t("animalslabel"), select=False)
    
    appointmentpermissions = AppointmentSettingsPanel(permissionsnotebook, self.t("appointmentslabel"))
    permissionsnotebook.AddPage(appointmentpermissions, self.t("appointmentslabel"), select=False)
    
    medicationpermissions = GenericSettingsPanel(permissionsnotebook, self.t("medicationlabel"))
    permissionsnotebook.AddPage(medicationpermissions, self.t("medicationlabel"), select=False)
    
    procedurepermissions = GenericSettingsPanel(permissionsnotebook, self.t("procedureslabel"))
    permissionsnotebook.AddPage(procedurepermissions, self.t("procedureslabel"), select=False)
    
    lookuppermissions = GenericSettingsPanel(permissionsnotebook, self.t("lookupslabel"))
    permissionsnotebook.AddPage(lookuppermissions, self.t("lookupslabel"), select=False)
    
    formpermissions = GenericSettingsPanel(permissionsnotebook, self.t("formslabel"))
    permissionsnotebook.AddPage(formpermissions, self.t("formslabel"), select=False)
    
    userpermissions = UserSettingsPanel(permissionsnotebook, self.t("userslabel"))
    permissionsnotebook.AddPage(userpermissions, self.t("userslabel"), select=False)
    
    diarypermissions = DiarySettingsPanel(permissionsnotebook, self.t("diarylabel"))
    permissionsnotebook.AddPage(diarypermissions, self.t("diarylabel"), select=False)
    
    miscpermissions = MiscSettingsPanel(permissionsnotebook, self.t("misclabel"))
    permissionsnotebook.AddPage(miscpermissions, self.t("misclabel"), select=False)
    
    schedulestab = SchedulesTab(permissionsnotebook, self.t("scheduleslabel"))
    permissionsnotebook.AddPage(schedulestab, self.t("scheduleslabel"), select=False)
    
    permissionssizer.Add(permissionsnotebook, 1, wx.EXPAND)
    
    tickallsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    untickallbitmap = wx.Bitmap("icons/reset.png")
    untickallbutton = wx.BitmapButton(panel, -1, untickallbitmap)
    untickallbutton.SetToolTipString(self.t("resetlabel"))
    untickallbutton.Bind(wx.EVT_BUTTON, self.UnTickAll)
    tickallsizer.Add(untickallbutton, 0, wx.EXPAND)
    
    tickallbitmap = wx.Bitmap("icons/tickall.png")
    tickallbutton = wx.BitmapButton(panel, -1, tickallbitmap)
    tickallbutton.SetToolTipString(self.t("tickalltooltip"))
    tickallbutton.Bind(wx.EVT_BUTTON, self.TickAll)
    tickallsizer.Add(tickallbutton, 0, wx.EXPAND)
    
    tickallsizer.Add(wx.StaticText(panel, -1, ""), 1, wx.EXPAND)
    
    submitbitmap = wx.Bitmap("icons/submit.png")
    submitbutton = wx.BitmapButton(panel, -1, submitbitmap)
    submitbutton.SetToolTipString(self.t("submitlabel"))
    submitbutton.Bind(wx.EVT_BUTTON, self.SubmitUser)
    tickallsizer.Add(submitbutton, 0, wx.EXPAND)
    
    permissionssizer.Add(tickallsizer, 0, wx.EXPAND)
    
    panel.SetSizer(permissionssizer)
    
    panel.clientpermissions = clientpermissions
    panel.animalpermissions = animalpermissions
    panel.appointmentpermissions = appointmentpermissions
    panel.medicationpermissions = medicationpermissions
    panel.procedurepermissions = procedurepermissions
    panel.lookuppermissions = lookuppermissions
    panel.formpermissions = formpermissions
    panel.userpermissions = userpermissions
    panel.diarypermissions = diarypermissions
    panel.miscpermissions = miscpermissions
    panel.schedulestab = schedulestab
    
    panel.nameentry = nameentry
    panel.passwordentry = passwordentry
    panel.positionentry = positionentry
    
    dialogsizer.Add(panel, 1, wx.EXPAND)
    
    dialog.SetSizer(dialogsizer)
    
    if userdata != False:
      
      panel.nameentry.SetValue(userdata[1])
      panel.passwordentry.SetValue(userdata[2])
      panel.positionentry.SetValue(userdata[3])
      
      changelog = userdata[4].split("$")
      
      panel.clientpermissions.edit.SetValue(bool(int(changelog[0][0])))
      panel.clientpermissions.delete.SetValue(bool(int(changelog[0][1])))
      panel.clientpermissions.editfinances.SetValue(bool(int(changelog[0][2])))
      panel.animalpermissions.edit.SetValue(bool(int(changelog[1][0])))
      panel.animalpermissions.delete.SetValue(bool(int(changelog[1][1])))
      panel.appointmentpermissions.edit.SetValue(bool(int(changelog[2][0])))
      panel.appointmentpermissions.delete.SetValue(bool(int(changelog[2][1])))
      panel.appointmentpermissions.vetform.SetValue(bool(int(changelog[2][2])))
      panel.medicationpermissions.edit.SetValue(bool(int(changelog[3][0])))
      panel.medicationpermissions.delete.SetValue(bool(int(changelog[3][1])))
      panel.procedurepermissions.edit.SetValue(bool(int(changelog[4][0])))
      panel.procedurepermissions.delete.SetValue(bool(int(changelog[4][1])))
      panel.lookuppermissions.edit.SetValue(bool(int(changelog[5][0])))
      panel.lookuppermissions.delete.SetValue(bool(int(changelog[5][1])))
      panel.formpermissions.edit.SetValue(bool(int(changelog[6][0])))
      panel.formpermissions.delete.SetValue(bool(int(changelog[6][1])))
      panel.userpermissions.edit.SetValue(bool(int(changelog[7][0])))
      panel.userpermissions.delete.SetValue(bool(int(changelog[7][1])))
      panel.userpermissions.editrota.SetValue(bool(int(changelog[7][2])))
      panel.miscpermissions.toolbar.SetValue(bool(int(changelog[8][0])))
      panel.miscpermissions.changelog.SetValue(bool(int(changelog[8][1])))
      panel.miscpermissions.editsettings.SetValue(bool(int(changelog[8][2])))
      panel.miscpermissions.multiplepanels.SetValue(bool(int(changelog[8][3])))
      panel.miscpermissions.asmsync.SetValue(bool(int(changelog[8][4])))
      panel.diarypermissions.adddiarynotes.SetValue(bool(int(changelog[9][0])))
      panel.diarypermissions.editdiarynotes.SetValue(bool(int(changelog[9][1])))
      panel.diarypermissions.deletediarynotes.SetValue(bool(int(changelog[9][2])))
      
      panel.schedulestab.mon_from_entry.SetValue(userdata[5] or '')
      panel.schedulestab.mon_to_entry.SetValue(userdata[6] or '')
      panel.schedulestab.tue_from_entry.SetValue(userdata[7] or '')
      panel.schedulestab.tue_to_entry.SetValue(userdata[8] or '')
      panel.schedulestab.wed_from_entry.SetValue(userdata[9] or '')
      panel.schedulestab.wed_to_entry.SetValue(userdata[10] or '')
      panel.schedulestab.thu_from_entry.SetValue(userdata[11] or '')
      panel.schedulestab.thu_to_entry.SetValue(userdata[12] or '')
      panel.schedulestab.fri_from_entry.SetValue(userdata[13] or '')
      panel.schedulestab.fri_to_entry.SetValue(userdata[14] or '')
      panel.schedulestab.sat_from_entry.SetValue(userdata[15] or '')
      panel.schedulestab.sat_to_entry.SetValue(userdata[16] or '')
      panel.schedulestab.sun_from_entry.SetValue(userdata[17] or '')
      panel.schedulestab.sun_to_entry.SetValue(userdata[18] or '')
      
    
    dialog.SetSize((900,400))
    
    del busy
    
    dialog.ShowModal()
  
  def TickAll(self, ID):
    
    panel = ID.GetEventObject().GetParent()
    
    panel.clientpermissions.edit.SetValue(True)
    panel.clientpermissions.delete.SetValue(True)
    panel.clientpermissions.editfinances.SetValue(True)
    
    panel.animalpermissions.edit.SetValue(True)
    panel.animalpermissions.delete.SetValue(True)
    
    panel.appointmentpermissions.edit.SetValue(True)
    panel.appointmentpermissions.delete.SetValue(True)
    panel.appointmentpermissions.vetform.SetValue(True)
    
    panel.medicationpermissions.edit.SetValue(True)
    panel.medicationpermissions.delete.SetValue(True)
    
    panel.procedurepermissions.edit.SetValue(True)
    panel.procedurepermissions.delete.SetValue(True)
    
    panel.lookuppermissions.edit.SetValue(True)
    panel.lookuppermissions.delete.SetValue(True)
    
    panel.formpermissions.edit.SetValue(True)
    panel.formpermissions.delete.SetValue(True)
    
    panel.userpermissions.edit.SetValue(True)
    panel.userpermissions.delete.SetValue(True)
    panel.userpermissions.editrota.SetValue(True)
    
    panel.miscpermissions.toolbar.SetValue(True)
    panel.miscpermissions.changelog.SetValue(True)
    panel.miscpermissions.editsettings.SetValue(True)
    panel.miscpermissions.multiplepanels.SetValue(True)
    panel.miscpermissions.asmsync.SetValue(True)
    
    panel.diarypermissions.adddiarynotes.SetValue(True)
    panel.diarypermissions.editdiarynotes.SetValue(True)
    panel.diarypermissions.deletediarynotes.SetValue(True)
  
  def UnTickAll(self, ID):
    
    panel = ID.GetEventObject().GetParent()
    
    panel.clientpermissions.edit.SetValue(False)
    panel.clientpermissions.delete.SetValue(False)
    panel.clientpermissions.editfinances.SetValue(False)
    
    panel.animalpermissions.edit.SetValue(False)
    panel.animalpermissions.delete.SetValue(False)
    
    panel.appointmentpermissions.edit.SetValue(False)
    panel.appointmentpermissions.delete.SetValue(False)
    panel.appointmentpermissions.vetform.SetValue(False)
    
    panel.medicationpermissions.edit.SetValue(False)
    panel.medicationpermissions.delete.SetValue(False)
    
    panel.procedurepermissions.edit.SetValue(False)
    panel.procedurepermissions.delete.SetValue(False)
    
    panel.lookuppermissions.edit.SetValue(False)
    panel.lookuppermissions.delete.SetValue(False)
    
    panel.formpermissions.edit.SetValue(False)
    panel.formpermissions.delete.SetValue(False)
    
    panel.userpermissions.edit.SetValue(False)
    panel.userpermissions.delete.SetValue(False)
    panel.userpermissions.editrota.SetValue(False)
    
    panel.miscpermissions.toolbar.SetValue(False)
    panel.miscpermissions.changelog.SetValue(False)
    panel.miscpermissions.editsettings.SetValue(False)
    panel.miscpermissions.multiplepanels.SetValue(False)
    panel.miscpermissions.asmsync.SetValue(False)
    
    panel.diarypermissions.adddiarynotes.SetValue(False)
    panel.diarypermissions.editdiarynotes.SetValue(False)
    panel.diarypermissions.deletediarynotes.SetValue(False)
  
  def RefreshUsers(self, ID=False):
    
    self.userlist.Clear()
    self.users = []
    
    action = "SELECT * FROM user ORDER BY Name;"
    results = db.SendSQL(action, self.localsettings.dbconnection)
    
    for a in results:
      
      self.users.append(a[0])
      self.userlist.Append(a[1] + " - " + a[3])
    
    self.userlist.SetSelection(-1)
  
  def SubmitUser(self, ID):
    
    panel = ID.GetEventObject().GetParent()
    
    username = panel.nameentry.GetValue()
    userpassword = panel.passwordentry.GetValue()
    position = panel.positionentry.GetValue()
    
    permissions = str(int(panel.clientpermissions.edit.GetValue()))
    permissions += str(int(panel.clientpermissions.delete.GetValue()))
    permissions += str(int(panel.clientpermissions.editfinances.GetValue()))+"$"
    permissions += str(int(panel.animalpermissions.edit.GetValue()))
    permissions += str(int(panel.animalpermissions.delete.GetValue()))+"$"
    permissions += str(int(panel.appointmentpermissions.edit.GetValue()))
    permissions += str(int(panel.appointmentpermissions.delete.GetValue()))
    permissions += str(int(panel.appointmentpermissions.vetform.GetValue()))+"$"
    permissions += str(int(panel.medicationpermissions.edit.GetValue()))
    permissions += str(int(panel.medicationpermissions.delete.GetValue()))+"$"
    permissions += str(int(panel.procedurepermissions.edit.GetValue()))
    permissions += str(int(panel.procedurepermissions.delete.GetValue()))+"$"
    permissions += str(int(panel.lookuppermissions.edit.GetValue()))
    permissions += str(int(panel.lookuppermissions.delete.GetValue()))+"$"
    permissions += str(int(panel.formpermissions.edit.GetValue()))
    permissions += str(int(panel.formpermissions.delete.GetValue()))+"$"
    permissions += str(int(panel.userpermissions.edit.GetValue()))
    permissions += str(int(panel.userpermissions.delete.GetValue()))
    permissions += str(int(panel.userpermissions.editrota.GetValue()))+"$"
    permissions += str(int(panel.miscpermissions.toolbar.GetValue()))
    permissions += str(int(panel.miscpermissions.changelog.GetValue()))
    permissions += str(int(panel.miscpermissions.editsettings.GetValue()))
    permissions += str(int(panel.miscpermissions.multiplepanels.GetValue()))
    permissions += str(int(panel.miscpermissions.asmsync.GetValue()))+"$"
    permissions += str(int(panel.diarypermissions.adddiarynotes.GetValue()))
    permissions += str(int(panel.diarypermissions.editdiarynotes.GetValue()))
    permissions += str(int(panel.diarypermissions.deletediarynotes.GetValue()))+"$"
    
    schedules = panel.schedulestab.GetValues()

    if type(schedules) == str:
      miscmethods.ShowMessage(self.t('invalidscheduletime')[schedules])
      return False
    else:
      userid = panel.userdata[0] if panel.userdata else False
      
      dbmethods.WriteToUserTable(self.localsettings.dbconnection, userid, username, userpassword, position, permissions, schedules)
      
      self.RefreshUsers()
      
      panel.GetParent().Close()
  
  def DeleteUser(self, ID):
    
    listboxid = self.userlist.GetSelection()
    
    userid = self.users[listboxid]
    
    action = "SELECT * FROM user WHERE ID = " + str(userid) + ";"
    results = db.SendSQL(action, self.localsettings.dbconnection)
    
    self.selecteduserid = userid
    
    if miscmethods.ConfirmMessage(self.t("userdeletemessage")) == True:
      
      action = "DELETE FROM user WHERE ID = " + str(self.selecteduserid) + ";"
      results = db.SendSQL(action, self.localsettings.dbconnection)
      
      self.RefreshUsers()

class EditStaffRota(wx.Panel):
  
  def t(self, field, idx = 0):
    
    return self.localsettings.t(field,idx)
  
  def __init__(self, notebook, localsettings):
    
    self.localsettings = localsettings
    
    self.pagetitle = miscmethods.GetPageTitle(notebook, self.t("editrotapagetitle"))
    
    wx.Panel.__init__(self, notebook)
    
    topsizer = wx.BoxSizer(wx.VERTICAL)
    
    action = "SELECT Name FROM user WHERE Position LIKE \"%Vet%\" ORDER BY Name"
    results = db.SendSQL(action, localsettings.dbconnection)
    
    
    vets = []
    for a in results:
      vets.append(a[0])
    
    toolssizer = wx.FlexGridSizer(rows=1)
    
    vetlabel = wx.StaticText(self, -1, self.t("vetlabel") + ": ")
    toolssizer.Add(vetlabel, 0, wx.ALIGN_CENTER)
    
    vetentry = wx.ComboBox(self, -1, "", choices=vets)
    toolssizer.Add(vetentry, 1, wx.EXPAND)
    
    timeonlabel = wx.StaticText(self, -1, " " + self.t("timeonlabel") + ": ")
    toolssizer.Add(timeonlabel, 0, wx.ALIGN_CENTER)
    
    timeonentry = wx.TextCtrl(self, -1, "")
    toolssizer.Add(timeonentry, 1, wx.EXPAND)
    
    timeofflabel = wx.StaticText(self, -1, " " + self.t("timeofflabel") + ": ")
    toolssizer.Add(timeofflabel, 0, wx.ALIGN_CENTER)
    
    timeoffentry = wx.TextCtrl(self, -1, "")
    toolssizer.Add(timeoffentry, 1, wx.EXPAND)
    
    operatingcheckbox = wx.CheckBox(self, -1, " " + self.t("operatinglabel") + ": ")
    toolssizer.Add(operatingcheckbox, 0, wx.ALIGN_CENTER)
    
    #spacer2 = wx.StaticText(self, -1, "")
    #toolssizer.Add(spacer2, 2, wx.EXPAND)
    
    for a in (1, 3, 5):
      toolssizer.AddGrowableCol(a)
    
    submitbitmap = wx.Bitmap("icons/submit.png")
    submitbutton = wx.BitmapButton(self, -1, submitbitmap)
    submitbutton.Bind(wx.EVT_BUTTON, self.Submit)
    toolssizer.Add(submitbutton, 0, wx.ALIGN_CENTER)
    
    topsizer.Add(toolssizer, 0, wx.EXPAND)
    
    spacer = wx.StaticText(self, -1, "")
    topsizer.Add(spacer, 0, wx.EXPAND)
    
    listssizer = wx.BoxSizer(wx.HORIZONTAL)
    
    datesizer = wx.BoxSizer(wx.VERTICAL)
    
    datelabel = wx.StaticText(self, -1, self.t("datelabel") + ":")
    datesizer.Add(datelabel, 0, wx.ALIGN_LEFT)
    
    datepickersizer = wx.BoxSizer(wx.HORIZONTAL)
    #self.dateentry = wx.DatePickerCtrl(self, -1, size=(200,-1))
    self.dateentry = customwidgets.DateCtrl(self, self.localsettings)
    #self.dateentry.Bind(wx.EVT_DATE_CHANGED, self.RefreshRota)
    datepickersizer.Add(self.dateentry, 1, wx.EXPAND)
    
    refreshbitmap = wx.Bitmap("icons/refresh.png")
    refreshbutton = wx.BitmapButton(self, -1, refreshbitmap)
    refreshbutton.Bind(wx.EVT_BUTTON, self.RefreshRota)
    datepickersizer.Add(refreshbutton, 0, wx.wx.EXPAND)
    
    datesizer.Add(datepickersizer, 0, wx.EXPAND)
    
    listssizer.Add(datesizer, 1, wx.EXPAND)
    
    spacer1 = wx.StaticText(self, -1, "", size=(20,-1))
    listssizer.Add(spacer1, 0, wx.EXPAND)
    
    summarysizer = wx.BoxSizer(wx.VERTICAL)
    
    staffsummarylabel = wx.StaticText(self, -1, self.t("staffsummarylabel") + ":")
    summarysizer.Add(staffsummarylabel, 0, wx.ALIGN_LEFT)
    
    staffsummarylistbox = customwidgets.StaffSummaryListbox(self, self.localsettings)
    staffsummarylistbox.Bind(wx.EVT_LISTBOX, self.SlotSelected)
    summarysizer.Add(staffsummarylistbox, 1, wx.EXPAND)
    
    summarybuttonssizer = wx.BoxSizer(wx.HORIZONTAL)
    
    editbitmap = wx.Bitmap("icons/edit.png")
    editbutton = wx.BitmapButton(self, -1, editbitmap)
    editbutton.Bind(wx.EVT_BUTTON, self.Edit)
    summarybuttonssizer.Add(editbutton, 0, wx.ALIGN_LEFT)
    
    deletebitmap = wx.Bitmap("icons/delete.png")
    deletebutton = wx.BitmapButton(self, -1, deletebitmap)
    deletebutton.Bind(wx.EVT_BUTTON, self.Delete)
    summarybuttonssizer.Add(deletebutton, 0, wx.ALIGN_LEFT)
    
    summarysizer.Add(summarybuttonssizer, 0, wx.ALIGN_LEFT)
    
    listssizer.Add(summarysizer, 2, wx.EXPAND)
    
    spacer3 = wx.StaticText(self, -1, "", size=(20,-1))
    listssizer.Add(spacer3, 0, wx.EXPAND)
    
    dayplansizer = wx.BoxSizer(wx.VERTICAL)
    
    dayplanlabel = wx.StaticText(self, -1,  self.t("dayplanlabel") + ":")
    dayplansizer.Add(dayplanlabel, 0, wx.ALIGN_LEFT)
    
    dayplan = wx.html.HtmlWindow(self)
    dayplansizer.Add(dayplan, 1, wx.EXPAND)
    
    listssizer.Add(dayplansizer, 3, wx.EXPAND)
    
    topsizer.Add(listssizer, 1, wx.EXPAND)
    
    self.SetSizer(topsizer)
    
    self.vetentry = vetentry
    self.timeonentry = timeonentry
    self.timeoffentry = timeoffentry
    self.staffsummarylistbox = staffsummarylistbox
    self.dayplan = dayplan
    self.operatingcheckbox = operatingcheckbox
    self.staffsummarylistbox.RefreshList()
    self.GenerateDayPlan()
  
  def Submit(self, ID):
    
    success = False
    date = self.dateentry.GetValue()
    date = miscmethods.GetSQLDateFromWXDate(date)
    vet = self.vetentry.GetValue()
    timeon = self.timeonentry.GetValue()
    timeoff = self.timeoffentry.GetValue()
    if self.operatingcheckbox.GetValue() == True:
      operating = 1
    else:
      operating = 0
    
    if vet == "":
      
      miscmethods.ShowMessage(self.t("novetnamemessage"))
      
    else:
    
      if miscmethods.ValidateTime(timeon) == True and miscmethods.ValidateTime(timeoff) == True:
        timeonint = int(timeon[:2] + timeon[3:5])
        timeoffint = int(timeoff[:2] + timeoff[3:5])
        if timeonint < timeoffint:
          success = True
        else:
          miscmethods.ShowMessage(self.t("vetfinishedbeforestartingmessage"))
      
      if success == True:
        
        starttimesql = timeon[:2] + ":" + timeon[3:5] + ":00"
        offtimesql = timeoff[:2] + ":" + timeoff[3:5] + ":00"
        
        action = "SELECT ID FROM staff WHERE DATE = \"" + date + "\" AND Vet = \"" + vet + "\" AND ( \"" + starttimesql + "\" BETWEEN TimeOn AND TimeOff OR \"" + offtimesql + "\" BETWEEN TimeOn AND TimeOff OR TimeOn BETWEEN \"" + starttimesql + "\" AND \"" + offtimesql + "\" OR TimeOff BETWEEN \"" + starttimesql + "\" AND \"" + offtimesql + "\" )"
        results = db.SendSQL(action, self.localsettings.dbconnection)
        
        if len(results) > 0:
          miscmethods.ShowMessage(self.t("vettwoplacesatoncemessage"))
        else:
          dbmethods.WriteToStaffTable(self.localsettings.dbconnection, date, vet, timeon, timeoff, operating)
          
          self.RefreshRota()
      else:
        miscmethods.ShowMessage(self.t("invalidtimemessage"))
  
  def Delete(self, ID):
    
    listboxid = self.staffsummarylistbox.GetSelection()
    staffid = self.staffsummarylistbox.htmllist[listboxid][0]
    
    action = "DELETE FROM staff WHERE ID = " + str(staffid)
    db.SendSQL(action, self.localsettings.dbconnection)
    
    self.RefreshRota()
  
  def GenerateDayPlan(self, ID=False):
    
    date = self.dateentry.GetValue()
    sqldate = miscmethods.GetSQLDateFromWXDate(date)
    
    output = miscmethods.GenerateDayPlan(self.localsettings, sqldate, 30)
    self.dayplan.SetPage(output)
  
  def RefreshRota(self, ID=False):
    
    self.staffsummarylistbox.RefreshList()
    self.GenerateDayPlan()
  
  def Edit(self, ID):
    
    listboxid = self.staffsummarylistbox.GetSelection()
    staffid = self.staffsummarylistbox.htmllist[listboxid][0]
    
    success = False
    date = self.dateentry.GetValue()
    date = miscmethods.GetSQLDateFromWXDate(date)
    vet = self.vetentry.GetValue()
    timeon = self.timeonentry.GetValue()
    timeoff = self.timeoffentry.GetValue()
    if self.operatingcheckbox.GetValue() == True:
      operating = 1
    else:
      operating = 0
    
    if miscmethods.ValidateTime(timeon) == True and miscmethods.ValidateTime(timeoff) == True:
      timeonint = int(timeon[:2] + timeon[3:5])
      timeoffint = int(timeoff[:2] + timeoff[3:5])
      if timeonint < timeoffint:
        success = True
      else:
        miscmethods.ShowMessage(self.t("vetfinishedbeforestartingmessage"))
    
    if success == True:
      
      dbmethods.WriteToStaffTable(self.localsettings.dbconnection, date, vet, timeon, timeoff, operating, staffid)
      
      self.RefreshRota()
    else:
      miscmethods.ShowMessage(self.t("invalidtimemessage"))
  
  def SlotSelected(self, ID):
    
    listboxid = self.staffsummarylistbox.GetSelection()
    staffdata = self.staffsummarylistbox.htmllist[listboxid]
    self.vetentry.SetValue(staffdata[1])
    self.timeonentry.SetValue(staffdata[3])
    self.timeoffentry.SetValue(staffdata[4])
    if staffdata[5] == 0:
      self.operatingcheckbox.SetValue(False)
    else:
      self.operatingcheckbox.SetValue(True)
