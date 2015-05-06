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
import db
import dbmethods
import datetime
import os
import threading
import wx
import wx.html

def CreateHeader(localsettings):
	
	home = miscmethods.GetHome()
	
	username = localsettings.username
	
	vetname = localsettings.practicename
	
	time = datetime.datetime.today()
	
	time = time.strftime("%A %d %B %Y - %H:%M").decode('utf-8')
	
	inp = open(home + "/.evette/html/header.dat", "r")
	filecontents = inp.readlines()
	inp.close()
	
	html = ""
	
	for a in filecontents:
		
		html = html + a
	
	html = html.decode('utf-8').replace("$$user$$", username).replace("$$time$$", time).replace("$$vetname$$", vetname)
	
	return html

class BuildForm(threading.Thread):
	
	def __init__(self, localsettings, body):
		
		threading.Thread.__init__(self)
		self.localsettings = localsettings
		self.body = body
		self.start()
	
	def run(self):
		
		localsettings = self.localsettings
		body = self.body
		
		home = miscmethods.GetHome()
		
		username = localsettings.username
		
		time = datetime.datetime.today()
		
		time = time.strftime("%A %d %B %Y - %H:%M").decode('utf-8')
		
		header = CreateHeader(localsettings)
		
		form = header + body + "<p align=right><font size=1><hr>" + localsettings.t("generatedbylabel") + " $$user$$ " + localsettings.t("onlabel") + " $$time$$</font></p></div></body></html>"
		
		form = form.replace("$$user$$", username).replace("$$time$$", time)
		
		pathtotempfolder = home + "/.evette/temp"
		
		filename = 1
		
		while os.path.isfile(pathtotempfolder + "/" + str(filename) + ".html") == True:
			filename = filename + 1
		
		filename = str(filename) + ".html"
		
		out = open(pathtotempfolder + "/" + filename, "w")
		out.write(form.encode('utf-8'))
		out.close()
		
		miscmethods.OpenMedia(False, filename)

class BuildLabel(threading.Thread):
	
	def __init__(self, localsettings, body):
		
		threading.Thread.__init__(self)
		
		self.localsettings = localsettings
		self.body = body
		
		self.start()
	
	def run(self):
		
		localsettings = self.localsettings
		body = self.body
		
		home = miscmethods.GetHome()
		
		header = CreateHeader(localsettings)
		
		form = header + body + "</body></html>"
		
		pathtotempfolder = home + "/.evette/temp"
		
		filename = 1
		
		while os.path.isfile(pathtotempfolder + "/" + str(filename) + ".html") == True:
			filename = filename + 1
		
		filename = str(filename) + ".html"
		
		out = open(pathtotempfolder + "/" + filename, "w")
		out.write(form.encode('utf-8'))
		out.close()
		
		miscmethods.OpenMedia(False, filename)

class AnimalFormEditor(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, notebook, localsettings):
		
		self.localsettings = localsettings
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, self.t("animalformspagetitle"))
		
		wx.Panel.__init__(self, notebook)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		mainsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		browserpanel = FormBrowserPanel(self, localsettings, "animal")
		mainsizer.Add(browserpanel, 1, wx.EXPAND)
		
		spacer = wx.StaticText(self, -1, "", size=(10,-1))
		mainsizer.Add(spacer, 0, wx.EXPAND)
		
		editorpanel = FormEditingPanel(self, localsettings, "animal")
		mainsizer.Add(editorpanel, 4, wx.EXPAND)
		
		topsizer.Add(mainsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.editorpanel = editorpanel
		self.browserpanel = browserpanel

class ClientFormEditor(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, notebook, localsettings):
		
		self.localsettings = localsettings
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, self.t("clientformspagetitle"))
		
		wx.Panel.__init__(self, notebook)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		mainsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		browserpanel = FormBrowserPanel(self, localsettings, "client")
		mainsizer.Add(browserpanel, 1, wx.EXPAND)
		
		spacer = wx.StaticText(self, -1, "", size=(10,-1))
		mainsizer.Add(spacer, 0, wx.EXPAND)
		
		editorpanel = FormEditingPanel(self, localsettings, "client")
		mainsizer.Add(editorpanel, 4, wx.EXPAND)
		
		topsizer.Add(mainsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.editorpanel = editorpanel
		self.browserpanel = browserpanel

class MedicationFormEditor(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, notebook, localsettings):
		
		self.localsettings = localsettings
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, self.t("editmedicationtformspagetitle"))
		
		wx.Panel.__init__(self, notebook)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		mainsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		browserpanel = FormBrowserPanel(self, localsettings, "medication")
		mainsizer.Add(browserpanel, 1, wx.EXPAND)
		
		spacer = wx.StaticText(self, -1, "", size=(10,-1))
		mainsizer.Add(spacer, 0, wx.EXPAND)
		
		editorpanel = FormEditingPanel(self, localsettings, "medication")
		mainsizer.Add(editorpanel, 4, wx.EXPAND)
		
		topsizer.Add(mainsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.editorpanel = editorpanel
		self.browserpanel = browserpanel

class InvoiceEditor(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, notebook, localsettings):
		
		self.localsettings = localsettings
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, self.t("editinvoicepagetitle"))
		
		wx.Panel.__init__(self, notebook)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		mainsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		browserpanel = FormBrowserPanel(self, localsettings, "invoice")
		mainsizer.Add(browserpanel, 1, wx.EXPAND)
		
		spacer = wx.StaticText(self, -1, "", size=(10,-1))
		mainsizer.Add(spacer, 0, wx.EXPAND)
		
		editorpanel = FormEditingPanel(self, localsettings, "invoice")
		mainsizer.Add(editorpanel, 4, wx.EXPAND)
		
		topsizer.Add(mainsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.editorpanel = editorpanel
		self.browserpanel = browserpanel

class FormEditingPanel(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, parent, localsettings, formtype):
		
		self.localsettings = localsettings
		
		self.formtype = formtype
		
		wx.Panel.__init__(self, parent)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		buttonssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		deletebitmap = wx.Bitmap("icons/delete.png")
		deletebutton = wx.BitmapButton(self, -1, deletebitmap)
		deletebutton.Bind(wx.EVT_BUTTON, self.Delete)
		deletebutton.Disable()
		buttonssizer.Add(deletebutton, 0, wx.EXPAND)
		
		self.deletebutton = deletebutton
		
		namelabel = wx.StaticText(self, -1, " Title: ")
		buttonssizer.Add(namelabel, 0, wx.ALIGN_CENTER)
		
		nameentry = wx.TextCtrl(self, -1, "")
		buttonssizer.Add(nameentry, 1, wx.EXPAND)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		submitbutton = wx.BitmapButton(self, -1, submitbitmap)
		submitbutton.Bind(wx.EVT_BUTTON, self.Submit)
		buttonssizer.Add(submitbutton, 0, wx.EXPAND)
		
		topsizer.Add(buttonssizer, 0, wx.EXPAND)
		
		spacer = wx.StaticText(self, -1, "", size=(-1,10))
		topsizer.Add(spacer, 0, wx.EXPAND)
		
		mainsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		formnotebook = wx.Notebook(self)
		formnotebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.GeneratePreview)
		
		entrypanel = wx.Panel(formnotebook)
		
		entrypanelsizer = wx.BoxSizer(wx.VERTICAL)
		
		self.entry = wx.TextCtrl(entrypanel, -1, "", style=wx.TE_MULTILINE)
		entrypanelsizer.Add(self.entry, 1, wx.EXPAND)
		
		entrypanel.SetSizer(entrypanelsizer)
		
		previewpanel = wx.Panel(formnotebook)
		
		previewsizer = wx.BoxSizer(wx.VERTICAL)
		
		self.previewwindow = wx.html.HtmlWindow(previewpanel)
		
		previewsizer.Add(self.previewwindow, 1, wx.EXPAND)
		
		previewpanel.SetSizer(previewsizer)
		
		formnotebook.AddPage(entrypanel, "HTML", select=True)
		
		formnotebook.AddPage(previewpanel, self.t("previewlabel"), select=False)
		
		mainsizer.Add(formnotebook, 3, wx.EXPAND)
		
		spacer2 = wx.StaticText(self, -1, "", size=(10,-1))
		mainsizer.Add(spacer2, 0, wx.EXPAND)
		
		wordkeysizer = wx.BoxSizer(wx.VERTICAL)
		
		wordkeylabel = wx.StaticText(self, -1, self.t("wordkeyslabel") + ":")
		wordkeysizer.Add(wordkeylabel, 0, wx.ALIGN_LEFT)
		
		wordkeys = WordKeys(self, localsettings, formtype)
		wordkeys.Bind(wx.EVT_LISTBOX_DCLICK, self.InsertWordkey)
		wordkeysizer.Add(wordkeys, 1, wx.EXPAND)
		
		mainsizer.Add(wordkeysizer, 1, wx.EXPAND)
		
		topsizer.Add(mainsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.parent = parent
		self.nameentry = nameentry
		self.wordkeys = wordkeys
	
	def GeneratePreview(self, ID):
		
		html = self.entry.GetValue().replace(">>", "&gt;&gt;").replace("<<", "&lt;&lt;")
		
		self.previewwindow.SetPage(html)
		
		ID.Skip()
	
	def InsertWordkey(self, ID):
		
		listboxid = self.wordkeys.GetSelection()
		
		wordkey = self.wordkeys.htmllist[listboxid][0]
		
		self.entry.WriteText(wordkey)
		self.entry.SetFocus()
	
	def Submit(self, ID):
		
		title = self.nameentry.GetValue()
		
		body = self.entry.GetValue()
		
		action = "SELECT ID FROM form WHERE Title = \"" + title + "\""
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		
		if len(results) > 0:
			if miscmethods.ConfirmMessage("A template called " + title + " already exists, would you like to overwrite it?") == True:
				formid = results[0][0]
				action = "REPLACE INTO form (ID, Title, Body, FormType) VALUES ( " + str(formid) + ", \"" + title + "\", \"" + body + "\", \"" + self.formtype + "\" )"
				db.SendSQL(action, self.localsettings.dbconnection)
		else:
			action = "INSERT INTO form (Title, Body, FormType) VALUES ( \"" + title + "\", \"" + body + "\", \"" + self.formtype + "\" )"
			db.SendSQL(action, self.localsettings.dbconnection)
			
		
		
		listbox = self.parent.browserpanel.listbox
		listbox.RefreshList()
	
	def Delete(self, ID):
		
		listboxid = self.parent.browserpanel.listbox.GetSelection()
		formid = self.parent.browserpanel.listbox.htmllist[listboxid][0]
		
		if miscmethods.ConfirmMessage("Are you sure that you want to delete this template?") == True:
			
			action = "DELETE FROM form WHERE ID = " + str(formid)
			db.SendSQL(action, self.localsettings.dbconnection)
			
			self.deletebutton.Disable()
			self.entry.Clear()
			self.nameentry.Clear()
			self.parent.browserpanel.listbox.RefreshList()

class FormBrowserPanel(wx.Panel):
	
	def __init__(self, parent, localsettings, formtype):
		
		wx.Panel.__init__(self, parent)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		listbox = FormListbox(self, localsettings, formtype)
		listbox.Bind(wx.EVT_LISTBOX, self.FormSelected)
		topsizer.Add(listbox, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.listbox = listbox
		self.parent = parent
		
		listbox.RefreshList()
	
	def FormSelected(self, ID):
		
		home = miscmethods.GetHome()
		
		listboxid = self.listbox.GetSelection()
		
		body = self.listbox.htmllist[listboxid][2]
		title = self.listbox.htmllist[listboxid][1]
		
		self.parent.editorpanel.entry.SetValue(body)
		self.parent.editorpanel.nameentry.SetValue(title)
		self.parent.editorpanel.deletebutton.Enable()

class FormListbox(wx.HtmlListBox):
	
	def __init__(self, parent, localsettings, formtype):
		
		wx.HtmlListBox.__init__(self, parent, -1)
		
		self.formtype = formtype
		self.htmllist = []
		self.localsettings = localsettings
		self.parent = parent
		self.SetItemCount(0)
	
	def OnGetItem(self, n):
		
		output = self.htmllist[n][1]
		
		return "<font size=2 color=blue>" + output + "</font>"
	
	def RefreshList(self, ID=False):
		
		self.Hide()
		
		listboxid = self.GetSelection()
		
		if listboxid != -1:
			templatename = self.htmllist[listboxid]
		else:
			templatename = "None"
		
		action = "SELECT * FROM form WHERE FormType = \"" + self.formtype + "\" ORDER BY Title"
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		
		self.htmllist = results
		
		self.SetItemCount(len(self.htmllist))
		
		self.SetSelection(-1)
		
		for a in range(0, len(self.htmllist)):
			
			if self.htmllist[a][1] == templatename:
				
				self.SetSelection(a)
		
		self.Refresh()
		
		self.Show()

class WordKeys(wx.HtmlListBox):
	
	def __init__(self, parent, localsettings, wordtype):
		
		wx.HtmlListBox.__init__(self, parent, -1)
		
		if wordtype == "animal":
			
			self.htmllist = ( ("<<PracticeName>>", 3), ("<<PracticeAddress>>", 3), ("<<PracticePostcode>>", 3), ("<<PracticeTelephone>>", 3), ("<<AnimalName>>", 0), ("<<AnimalSpecies>>", 0), ("<<AnimalColour>>", 0), ("<<AnimalBreed>>", 0), ("<<AnimalSex>>", 0), ("<<AnimalNeutered>>", 0), ("<<AnimalDOB>>", 0), ("<<AnimalComments>>", 0), ("<<AnimalChipNo>>", 0), ("<<ClientName>>", 1), ("<<ClientTitle>>", 1), ("<<ClientForenames>>", 1), ("<<ClientSurname>>", 1), ("<<ClientAddress>>", 1), ("<<ClientPostcode>>", 1), ("<<ClientHomeTelephone>>", 1), ("<<ClientMobileTelephone>>", 1), ("<<ClientWorkTelephone>>", 1), ("<<ClientEmailAddress>>", 1), ("<<ClientComments>>", 1), ("<<Today>>", 2 ) )
			
		elif wordtype == "client":
			
			self.htmllist = ( ("<<PracticeName>>", 0), ("<<PracticeAddress>>", 0), ("<<PracticePostcode>>", 0), ("<<PracticeTelephone>>", 0), ("<<ClientName>>", 1), ("<<ClientAddress>>", 1), ("<<ClientPostcode>>", 1), ("<<ClientHomeTelephone>>", 1), ("<<ClientMobileTelephone>>", 1), ("<<ClientWorkTelephone>>", 1), ("<<ClientEmailAddress>>", 1), ("<<ClientComments>>", 1), ("<<Today>>", 2 ) )
			
		elif wordtype == "invoice":
			
			self.htmllist = ( ("<<PracticeName>>", 0), ("<<PracticeAddress>>", 0), ("<<PracticePostcode>>", 0), ("<<PracticeTelephone>>", 0), ("<<ClientName>>", 1), ("<<ClientAddress>>", 1), ("<<ClientPostcode>>", 1), ("<<ClientHomeTelephone>>", 1), ("<<ClientMobileTelephone>>", 1), ("<<ClientWorkTelephone>>", 1), ("<<ClientEmailAddress>>", 1), ("<<Today>>", 2 ), ("<<InvoiceNumber>>", 3), ("<<InvoiceBreakdown>>", 3), ("<<InvoiceTotal>>", 3), ("<<FromDate>>", 3), ("<<ToDate>>", 3) )
			
		elif wordtype == "medication":
			
			self.htmllist = ( ("<<AnimalName>>", 0), ("<<AnimalSpecies>>", 0), ("<<AnimalColour>>", 0), ("<<AnimalBreed>>", 0), ("<<AnimalSex>>", 0), ("<<AnimalDOB>>", 0), ("<<AnimalComments>>", 0), ("<<AnimalChipNo>>", 0), ("<<ClientName>>", 1), ("<<ClientAddress>>", 1), ("<<ClientPostcode>>", 1), ("<<ClientHomeTelephone>>", 1), ("<<ClientMobileTelephone>>", 1), ("<<ClientWorkTelephone>>", 1), ("<<ClientEmailAddress>>", 1), ("<<ClientComments>>", 1), ("<<Today>>", 2 ), ("<<MedicationName>>", 3), ("<<Unit>>", 3), ("<<Quantity>>", 3), ("<<Instructions>>", 3), ("<<BatchNo>>", 3), ("<<Expires>>", 3), ("<<PracticeName>>", 4), ("<<PracticeAddress>>", 4), ("<<PracticePostcode>>", 4), ("<<PracticeTelephone>>", 4) )
			
		else:
			
			self.htmllist = []
		
		self.localsettings = localsettings
		self.parent = parent
		self.SetItemCount(len(self.htmllist))
	
	def OnGetItem(self, n):
		
		wordkey = self.htmllist[n][0].replace("<", "&lt;").replace(">", "&gt;")
		if self.htmllist[n][1] == 0:
			colour = "blue"
		elif self.htmllist[n][1] == 1:
			colour = "red"
		elif self.htmllist[n][1] == 2:
			colour = "green"
		elif self.htmllist[n][1] == 3:
			colour = "brown"
		elif self.htmllist[n][1] == 4:
			colour = "purple"
		else:
			colour = "black"
		
		return "<font size=2 color=" + colour + ">" + wordkey + "</font>"

def GenerateAnimalForm(formname, clientdata, animaldata):
	
	action = "SELECT Body FROM form WHERE Title = \"" + formname + "\" AND FormType = \"animal\""
	results = db.SendSQL(action, animaldata.localsettings.dbconnection)
	
	
	body = unicode(results[0][0], "utf-8")
	
	clientname = clientdata.title + " " + clientdata.forenames + " " + clientdata.surname
	clientaddress = miscmethods.RemoveLineBreaks(clientdata.address)
	
	animalneutered = animaldata.neutered
	
	if animalneutered == 0:
		
		animalneutered = animaldata.localsettings.t("nolabel")
		
	else:
		
		animalneutered = animaldata.localsettings.t("yeslabel")
	
	time = datetime.datetime.today()
	
	todaysdate = time.strftime("%A %d %B %Y")
	
	body = body.replace("<<AnimalName>>", animaldata.name).replace("<<AnimalSpecies>>", animaldata.species).replace("<<AnimalColour>>", animaldata.colour).replace("<<AnimalBreed>>", animaldata.breed).replace("<<AnimalNeutered>>", animalneutered).replace("<<AnimalDOB>>", animaldata.dob).replace("<<AnimalComments>>", animaldata.comments).replace("<<AnimalChipNo>>", animaldata.chipno).replace("<<ClientName>>", clientname).replace("<<ClientTitle>>", clientdata.title).replace("<<ClientForenames>>", clientdata.forenames).replace("<<ClientSurname>>", clientdata.surname).replace("<<ClientAddress>>", clientaddress).replace("<<ClientPostcode>>", clientdata.postcode).replace("<<ClientHomeTelephone>>", clientdata.hometelephone).replace("<<ClientMobileTelephone>>", clientdata.mobiletelephone).replace("<<ClientWorkTelephone>>", clientdata.worktelephone).replace("<<ClientEmailAddress>>", clientdata.emailaddress).replace("<<ClientComments>>", unicode(clientdata.comments, "utf-8")).replace("<<Today>>", todaysdate).replace("<<PracticeName>>", clientdata.localsettings.practicename).replace("<<PracticeAddress>>", clientdata.localsettings.practiceaddress.replace("\n", "<br>")).replace("<<PracticePostcode>>", clientdata.localsettings.practicepostcode).replace("<<PracticeTelephone>>", clientdata.localsettings.practicetelephone)
	
	if animaldata.sex == 0:
		
		body = body.replace("<<AnimalSex>>", animaldata.localsettings.t("unknownlabel"))
		
	elif animaldata.sex == 1:
		
		body = body.replace("<<AnimalSex>>", animaldata.localsettings.t("malelabel"))
		
	else:
		
		body = body.replace("<<AnimalSex>>", animaldata.localsettings.t("femalelabel"))
	
	BuildForm(clientdata.localsettings, body)

def GenerateClientForm(formname, clientdata):
	
	action = "SELECT Body FROM form WHERE Title = \"" + formname + "\" AND FormType = \"client\""
	results = db.SendSQL(action, clientdata.localsettings.dbconnection)
	
	
	body = unicode(results[0][0], "utf-8")
	
	clientname = clientdata.title + " " + clientdata.forenames + " " + clientdata.surname
	clientaddress = miscmethods.RemoveLineBreaks(clientdata.address)
	
	time = datetime.datetime.today()
	
	todaysdate = time.strftime("%A %d %B %Y")
	
	body = body.replace("<<ClientName>>", clientname).replace("<<ClientAddress>>", clientaddress).replace("<<ClientPostcode>>", clientdata.postcode).replace("<<ClientHomeTelephone>>", clientdata.hometelephone).replace("<<ClientMobileTelephone>>", clientdata.mobiletelephone).replace("<<ClientWorkTelephone>>", clientdata.worktelephone).replace("<<ClientEmailAddress>>", clientdata.emailaddress).replace("<<ClientComments>>", unicode(clientdata.comments, "utf-8")).replace("<<Today>>", todaysdate).replace("<<PracticeName>>", clientdata.localsettings.practicename).replace("<<PracticeAddress>>", clientdata.localsettings.practiceaddress.replace("\n", "<br>")).replace("<<PracticePostcode>>", clientdata.localsettings.practicepostcode).replace("<<PracticeTelephone>>", clientdata.localsettings.practicetelephone)
	
	BuildForm(clientdata.localsettings, body)

def GenerateMedicationDocument(formname, appointmentdata, medicationname, unit, quantity, instructions, batchno, expires):
	
	if str(expires) == None or str(expires) == "":
		expires = ""
	else:
		expires = miscmethods.GetDateFromWXDate(expires)
		expires = miscmethods.FormatDate(expires, appointmentdata.localsettings)
	
	action = "SELECT Body FROM form WHERE Title = \"" + formname + "\" AND FormType = \"medication\""
	results = db.SendSQL(action, appointmentdata.localsettings.dbconnection)
	
	
	body = unicode(results[0][0], "utf-8")
	
	clientname = appointmentdata.clientdata.title + " " + appointmentdata.clientdata.forenames + " " + appointmentdata.clientdata.surname
	clientaddress = miscmethods.RemoveLineBreaks(appointmentdata.clientdata.address)
	
	time = datetime.datetime.today()
	
	todaysdate = time.strftime("%A %d %B %Y")
	
	body = body.replace("<<ClientName>>", clientname).replace("<<ClientAddress>>", clientaddress).replace("<<ClientPostcode>>", appointmentdata.clientdata.postcode).replace("<<ClientHomeTelephone>>", appointmentdata.clientdata.hometelephone).replace("<<ClientMobileTelephone>>", appointmentdata.clientdata.mobiletelephone).replace("<<ClientWorkTelephone>>", appointmentdata.clientdata.worktelephone).replace("<<ClientEmailAddress>>", appointmentdata.clientdata.emailaddress).replace("<<ClientComments>>", unicode(appointmentdata.clientdata.comments, "utf-8")).replace("<<Today>>", todaysdate).replace("<<MedicationName>>", medicationname).replace("<<Unit>>", unit).replace("<<Quantity>>", quantity).replace("<<Instructions>>", instructions).replace("<<BatchNo>>", batchno).replace("<<Expires>>", expires).replace("<<PracticeName>>", appointmentdata.clientdata.localsettings.practicename).replace("<<PracticeAddress>>", appointmentdata.clientdata.localsettings.practiceaddress.replace("\n", "<br>")).replace("<<PracticePostcode>>", appointmentdata.clientdata.localsettings.practicepostcode).replace("<<PracticeTelephone>>", appointmentdata.clientdata.localsettings.practicetelephone).replace("<<AnimalName>>", appointmentdata.animaldata.name).replace("<<AnimalSpecies>>", appointmentdata.animaldata.species).replace("<<AnimalColour>>", appointmentdata.animaldata.colour).replace("<<AnimalBreed>>", appointmentdata.animaldata.breed).replace("<<AnimalDOB>>", appointmentdata.animaldata.dob).replace("<<AnimalComments>>", appointmentdata.animaldata.comments).replace("<<AnimalChipNo>>", appointmentdata.animaldata.chipno)
	
	if appointmentdata.animaldata.sex == 0:
		
		body = body.replace("<<AnimalSex>>", appointmentdata.localsettings.t("unknownlabel"))
		
	elif appointmentdata.animaldata.sex == 1:
		
		body = body.replace("<<AnimalSex>>", appointmentdata.localsettings.t("malelabel"))
		
	else:
		
		body = body.replace("<<AnimalSex>>", appointmentdata.localsettings.t("femalelabel"))
	
	BuildLabel(appointmentdata.localsettings, body)

def GetFormList(localsettings, formtype):
	
	action = "SELECT * FROM form WHERE FormType = \"" + formtype + "\" ORDER BY Title"
	results = db.SendSQL(action, localsettings.dbconnection)
	
	
	templates = []
	
	for a in results:
		templates.append(a[1])
	
	return templates
