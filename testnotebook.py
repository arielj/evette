#!/usr/bin/python

import wx
import customwidgets
import random
import settings

pagetitles = (
	"Apple",
	"Balls",
	"Carrot",
	"Dog",
	"Ears",
	"Fun bags"
	)

def AddPanel(ID):
	
	notebook = ID.GetEventObject().GetParent().notebook
	
	panel = wx.Panel(notebook)
	
	topsizer = wx.BoxSizer(wx.VERTICAL)
	
	panel.pagetitle = pagetitles[int(random.random() * len(pagetitles))]
	
	label = wx.StaticText(panel, -1,  panel.pagetitle)
	topsizer.Add(label, 0, wx.EXPAND)
	
	textarea = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE)
	topsizer.Add(textarea, 1, wx.EXPAND)
	
	panel.SetSizer(topsizer)
	
	notebook.AddPage(panel)

localsettings = settings.settings(3)
localsettings.GetSettings()

app = wx.App()
frame = wx.Frame(None, -1, "Adams Frame")
panel = wx.Panel(frame)
topsizer = wx.BoxSizer(wx.VERTICAL)
addpanelbutton = wx.Button(panel, -1, "Add Panel")
addpanelbutton.Bind(wx.EVT_BUTTON, AddPanel)
topsizer.Add(addpanelbutton, 0, wx.ALIGN_LEFT)
notebook = customwidgets.Notebook(panel, localsettings)
topsizer.Add(notebook, 1, wx.EXPAND)
panel.SetSizer(topsizer)
panel.notebook = notebook

frame.Show()
app.MainLoop()
