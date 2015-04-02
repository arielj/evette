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
import db
import miscmethods
import dbmethods
import settings
import sys
import threading
import evette
import dbupdates

if str(sys.platform)[:3] == "win":
	
	from wx.lib.stattext import GenStaticText
	
else:
	
	from wx import StaticText as GenStaticText


def LaunchDialog(localsettings, splashimagepath=False):
	
	dialog = wx.Dialog(None, -1, "Evette")
	dialog.Bind(wx.EVT_CLOSE, ExitApp)
	
	iconFile = "icons/evette.ico"
	icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
	dialog.SetIcon(icon1)
	
	dialogsizer = wx.BoxSizer(wx.VERTICAL)
	
	panel = wx.Panel(dialog)
	
	topsizer = wx.BoxSizer(wx.VERTICAL)
	
	bgsizer = wx.BoxSizer(wx.VERTICAL)
	
	if splashimagepath == False:
		
		imagebitmap = wx.Bitmap(miscmethods.GetImagePath())
		
	else:
		
		imagebitmap = wx.Bitmap("icons/images/" + splashimagepath)
	
	randomimage = wx.StaticBitmap(panel, -1, imagebitmap)
	framesize = imagebitmap.GetSize()
	bgsizer.Add(randomimage, 0, wx.ALIGN_CENTER)
	
	spacer = GenStaticText(panel, -1, "")
	topsizer.Add(spacer, 1, wx.EXPAND)
	
	horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
	
	infosizer = wx.BoxSizer(wx.VERTICAL)
	
	infosizer.Add(GenStaticText(panel, 1, ""), 1, wx.EXPAND)
	
	versionnolabel = GenStaticText(panel, -1, localsettings.t("versionlabel"))
	font = versionnolabel.GetFont()
	font.SetPointSize(font.GetPointSize() - 2)
	versionnolabel.SetFont(font)
	infosizer.Add(versionnolabel, 0, wx.ALIGN_CENTER)
	
	versionnoentry = GenStaticText(panel, -1, str(dbupdates.GetCurrentVersion()))
	font = versionnoentry.GetFont()
	font.SetPointSize(font.GetPointSize() + 8)
	font.SetWeight(wx.FONTWEIGHT_BOLD)
	versionnoentry.SetFont(font)
	versionnoentry.SetForegroundColour("blue")
	infosizer.Add(versionnoentry, 0, wx.ALIGN_CENTER)
	
	infosizer.Add(GenStaticText(panel, 1, ""), 1, wx.EXPAND)
	
	horizontalsizer.Add(infosizer, 1, wx.ALIGN_BOTTOM)
	
	horizontalsizer.Add(GenStaticText(panel, -1, ""), 1, wx.EXPAND)
	
	entrysizer = wx.BoxSizer(wx.VERTICAL)
	
	userlabel = GenStaticText(panel, -1, localsettings.t("usernamelabel") + ":")
	font = userlabel.GetFont()
	font.SetPointSize(font.GetPointSize() - 2)
	userlabel.SetFont(font)
	entrysizer.Add(userlabel, 0, wx.ALIGN_LEFT)
	
	userentry = wx.TextCtrl(panel, -1, localsettings.lastuser, size=(150,-1), style=wx.TE_PROCESS_ENTER)
	userentry.description = "username"
	userentry.Bind(wx.EVT_CHAR, ButtonPressed)
	userentry.SetToolTipString(localsettings.t("tabbetweenentriestooltip"))
	userentry.SetFocus()
	entrysizer.Add(userentry, 0, wx.EXPAND)
	
	passwordlabel = GenStaticText(panel, -1, localsettings.t("passwordlabel") + ":")
	passwordlabel.SetFont(font)
	entrysizer.Add(passwordlabel, 0, wx.ALIGN_LEFT)
	
	passwordentry = wx.TextCtrl(panel, -1, "", style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
	passwordentry.description = "password"
	passwordentry.SetFocus()
	passwordentry.Bind(wx.EVT_CHAR, ButtonPressed)
	entrysizer.Add(passwordentry, 0, wx.EXPAND)
	
	horizontalsizer.Add(entrysizer, 0, wx.ALIGN_BOTTOM)
	
	topsizer.Add(horizontalsizer, 1, wx.EXPAND)
	
	panel.SetSizer(topsizer)
	
	panel.userentry = userentry
	panel.passwordentry = passwordentry
	panel.localsettings = localsettings
	
	dialogsizer.Add(panel, 1, wx.EXPAND)
	
	dialog.SetSizer(dialogsizer)
	
	dialog.panel = panel
	
	dialog.SetSize(framesize)
	dialog.CenterOnScreen()
	
	dialog.ShowModal()

def ButtonPressed(ID):
        
	keycode = ID.GetKeyCode()
	#print "keycode = " + str(keycode)

	if keycode == 315 or keycode == 317:
                
                if ID.GetEventObject().description == "username":
                        
                        ID.GetEventObject().GetParent().passwordentry.SetFocus()
                        
                else:
                        
                        ID.GetEventObject().GetParent().userentry.SetFocus()
                
	elif keycode == 13:
		
		LogIn(ID)
	
	ID.Skip()

def LogIn(ID):
	
	panel = ID.GetEventObject().GetParent()
	localsettings = panel.localsettings
	
	username = panel.userentry.GetValue()
	password = panel.passwordentry.GetValue()
	
	action = "SELECT ID FROM user WHERE Name = \"" + username + "\" AND Password = \"" + password + "\""
	results = db.SendSQL(action, localsettings.dbconnection)
	
	if len(results) == 0:
		
		panel.passwordentry.Clear()
		panel.passwordentry.SetFocus()
		
	else:
		
		localsettings.SaveSettings(username)
		panel.GetParent().Hide()
		panel.passwordentry.Clear()
		evetteframe = evette.Evette(panel, results[0][0])
		evetteframe.logindialog = panel.GetParent()

def ExitApp(ID):
	
	sys.exit()

def AdjustSettingsDialog(parent, localsettings):
	
	if miscmethods.ConfirmMessage(localsettings.t("launchnodatabaseservermessage"), parent):
		
		dialog = wx.Dialog(parent, -1, localsettings.t("launchdbiplabel"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		gridsizer = wx.FlexGridSizer(cols=2)
		gridsizer.AddGrowableCol(1)
		
		dbiplabel = wx.StaticText(panel, -1, miscmethods.NoWrap(localsettings.t("launchdbiplabel")))
		gridsizer.Add(dbiplabel, 0, wx.EXPAND)
		dbipentry = wx.TextCtrl(panel, -1, localsettings.dbip, size=(200,-1))
		gridsizer.Add(dbipentry, 1, wx.EXPAND)
		
		dbuserlabel = wx.StaticText(panel, -1, miscmethods.NoWrap(localsettings.t("launchdbuserlabel")))
		gridsizer.Add(dbuserlabel, 0, wx.EXPAND)
		dbuserentry = wx.TextCtrl(panel, -1, localsettings.dbuser)
		gridsizer.Add(dbuserentry, 1, wx.EXPAND)
		
		dbpasslabel = wx.StaticText(panel, -1, miscmethods.NoWrap(localsettings.t("launchdbpasslabel")))
		gridsizer.Add(dbpasslabel, 0, wx.EXPAND)
		dbpassentry = wx.TextCtrl(panel, -1, localsettings.dbpass)
		gridsizer.Add(dbpassentry, 1, wx.EXPAND)
		
		topsizer.Add(gridsizer, 0, wx.EXPAND)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		submitbutton = wx.BitmapButton(panel, -1, submitbitmap)
		submitbutton.SetToolTipString(localsettings.t("submitlabel"))
		submitbutton.Bind(wx.EVT_BUTTON, SubmitSettings)
		topsizer.Add(submitbutton, 0, wx.ALIGN_CENTER)
		
		panel.SetSizer(topsizer)
		
		panel.dbuserentry = dbuserentry
		panel.dbpassentry = dbpassentry
		panel.dbipentry = dbipentry
		
		panel.localsettings = localsettings
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		dialog.Fit()
		
		dialog.ShowModal()
		
	else:
		
		sys.exit()

def SubmitSettings(ID):
	
	panel = ID.GetEventObject().GetParent()
	
	panel.localsettings.dbip = panel.dbipentry.GetValue()
	panel.localsettings.dbuser = panel.dbuserentry.GetValue()
	panel.localsettings.dbpass = panel.dbpassentry.GetValue()
	
	panel.localsettings.SaveSettings()
	
	panel.GetParent().Close()

if len(sys.argv) > 1:
	
	splashimagepath = sys.argv[1]
	
else:
	
	splashimagepath = False

app = wx.App()

if miscmethods.CheckConfFileExists() == False:
	
	settings.CreateConfFile()

if miscmethods.CheckEvetteFolderExists() == False:
	
	miscmethods.CreateEvetteFolder()

serverpresent = False

while serverpresent == False:
	
	localsettings = settings.settings(False)
	localsettings.GetSettings()
	
	if db.CheckServer(localsettings) == False:
		
		AdjustSettingsDialog(None, localsettings)
		
	else:
		
		serverpresent = True

localsettings.dbconnection = db.GetConnection(localsettings)

if localsettings.dbconnection == False:
	
	if db.CreateDatabase(localsettings) == False:
		
		sys.exit()
		
	else:
		
		miscmethods.ShowMessage(localsettings.t("launchdatabasecreatedmessage"), None)
		
		localsettings.dbconnection = db.GetConnection(localsettings)

versioncheck = dbupdates.CheckVersion(localsettings)

if versioncheck == True:
	
	LaunchDialog(localsettings, splashimagepath)
	
else:
	
	sys.exit()

app.MainLoop()
