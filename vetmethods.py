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
import db
import dbmethods
import datetime
import customwidgets
import formmethods
import medicationmethods
import viewappointments
import animalmethods

class VetForm(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return  self.localsettings.t(field,idx)

	def __init__(self, notebook, appointmentdata, localsettings, parent):
		
		self.parent = parent
		
		self.appointmentdata = appointmentdata
		
		self.localsettings = localsettings
		
		wx.Panel.__init__(self, notebook)
		
		self.pagetitle = miscmethods.GetPageTitle(notebook, self.t("vetformpagetitle"))
		self.pageimage = "icons/vetform.png"
		
		mainsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		leftsizer = wx.BoxSizer(wx.VERTICAL)
		
		previousappointmentssizer = wx.BoxSizer(wx.VERTICAL)
		
		previousappointmentlabel = wx.StaticText(self, -1, self.t("vetformotherappointmentslabel"))
		font = previousappointmentlabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		previousappointmentlabel.SetFont(font)
		previousappointmentssizer.Add(previousappointmentlabel, 0, wx.ALIGN_LEFT)
		
		self.previousappointmentslistbox = customwidgets.AppointmentsSummaryListbox(self, self.appointmentdata.animaldata, True)
		self.previousappointmentslistbox.Bind(wx.EVT_LIST_ITEM_SELECTED, self.AppointmentSelected)
		
		previousappointmentssizer.Add(self.previousappointmentslistbox, 1, wx.EXPAND)
		
		previousappointmentdetailslabel = wx.StaticText(self, -1, self.t("vetformappointmentdetailslabel"))
		previousappointmentdetailslabel.SetFont(font)
		previousappointmentssizer.Add(previousappointmentdetailslabel, 0, wx.ALIGN_LEFT)
		
		self.previousappointmentdetails = wx.html.HtmlWindow(self)
		previousappointmentssizer.Add(self.previousappointmentdetails, 2, wx.EXPAND)
		
		leftsizer.Add(previousappointmentssizer, 1, wx.EXPAND)
		
		middlesizer = wx.BoxSizer(wx.VERTICAL)
		
		reasonsizer = wx.BoxSizer(wx.VERTICAL)
		#reasonlabel = wx.StaticText(self, -1, self.t("appointmentreasonlabel").replace(" ", u"\xa0") + ":")
		
		
		
		self.animaldetailswindow = wx.html.HtmlWindow(self)
		
		appointmenthtml = miscmethods.GetAppointmentHtml(appointmentdata)
		
		self.animaldetailswindow.SetPage(appointmenthtml)
		
		reasonsizer.Add(self.animaldetailswindow, 1, wx.EXPAND)
		
		
		
		#reasonsizer.Add(reasonlabel, 0, wx.ALIGN_LEFT)
		#reasonbox = wx.TextCtrl(self, -1, self.appointmentdata.reason, style=wx.TE_MULTILINE)
		#reasonsizer.Add(reasonbox, 1, wx.EXPAND)
		
		problemsizer = wx.BoxSizer(wx.VERTICAL)
		
		problemlabel = wx.StaticText(self, -1, self.t("problemlabel").replace(" ", u"\xa0") + ":")
		problemlabel.SetFont(font)
		problemsizer.Add(problemlabel, 0, wx.ALIGN_LEFT)
		
		middlesizer.Add(reasonsizer, 1, wx.EXPAND)
		middlesizer.Add(problemsizer, 1, wx.EXPAND)
		
		rightsizer = wx.BoxSizer(wx.VERTICAL)
		
		rightsizer.Add(wx.Panel(self, size=(-1,10)), 0, wx.EXPAND)
		
		buttongridsizer = wx.FlexGridSizer(cols=4)
		
		buttongridsizer.AddGrowableCol(1)
		buttongridsizer.AddGrowableCol(3)
		
		buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
		medicationbutton = wx.Button(self, -1, self.t("randomdatamedicationlabel"))
		
		font = medicationbutton.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		medicationbutton.SetFont(font)
		
		medicationbutton.Bind(wx.EVT_BUTTON, self.AddMedication)
		buttongridsizer.Add(medicationbutton, 0, wx.EXPAND)
		
		buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
		procedurebutton = wx.Button(self, -1, self.t("procedurelabel"))
		procedurebutton.SetFont(font)
		procedurebutton.Bind(wx.EVT_BUTTON, self.AddProcedure)
		buttongridsizer.Add(procedurebutton, 0, wx.EXPAND)
		
		buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
		buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
		buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
		buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
		
		buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
		vaccinationbutton = wx.Button(self, -1, self.t("vaccinationsvaccinelabel"))
		vaccinationbutton.SetFont(font)
		vaccinationbutton.Bind(wx.EVT_BUTTON, self.AddVaccination)
		buttongridsizer.Add(vaccinationbutton, 0, wx.EXPAND)
		
		buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
		consumablebutton = wx.Button(self, -1, self.t("consumablelabel"))
		consumablebutton.SetFont(font)
		consumablebutton.Bind(wx.EVT_BUTTON, self.AddConsumable)
		buttongridsizer.Add(consumablebutton, 0, wx.EXPAND)
		
		buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
		buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
		buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
		buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
		
		buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
		shopbutton = wx.Button(self, -1, self.t("shoplabel"))
		shopbutton.SetFont(font)
		shopbutton.Bind(wx.EVT_BUTTON, self.AddShopItem)
		buttongridsizer.Add(shopbutton, 0, wx.EXPAND)
		
		buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
		manualbutton = wx.Button(self, -1, self.t("manuallabel"))
		manualbutton.SetFont(font)
		manualbutton.Bind(wx.EVT_BUTTON, self.AddManual)
		buttongridsizer.Add(manualbutton, 0, wx.EXPAND)
		
		if self.appointmentdata.animaldata.chipno == "":
			
			buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
			buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
			buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
			buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
			
			buttongridsizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
			chipbutton = wx.Button(self, -1, self.t("microchiplabel"))
			chipbutton.SetFont(font)
			chipbutton.Bind(wx.EVT_BUTTON, self.Microchip)
			buttongridsizer.Add(chipbutton, 0, wx.EXPAND)
			
			self.chipbutton = chipbutton
		
		rightsizer.Add(buttongridsizer, 0, wx.ALIGN_LEFT)
		
		rightsizer.Add(wx.Panel(self, size=(-1,10)), 0, wx.EXPAND)
		
		self.problementry = wx.TextCtrl(self, -1, self.appointmentdata.problem, style=wx.TE_MULTILINE)
		problemsizer.Add(self.problementry, 1, wx.EXPAND)
		
		notessizer = wx.BoxSizer(wx.VERTICAL)
		
		noteslabel = wx.StaticText(self, -1, self.t("noteslabel") + ":")
		noteslabel.SetFont(font)
		notessizer.Add(noteslabel, 0, wx.ALIGN_LEFT)
		
		self.notesentry = wx.TextCtrl(self, -1, self.appointmentdata.notes, style=wx.TE_MULTILINE)
		notessizer.Add(self.notesentry, 1, wx.EXPAND)
		
		middlesizer.Add(notessizer, 2, wx.EXPAND)
		
		plansizer = wx.BoxSizer(wx.VERTICAL)
		
		planlabel = wx.StaticText(self, -1, self.t("planlabel") + ":")
		planlabel.SetFont(font)
		plansizer.Add(planlabel, 0, wx.ALIGN_LEFT)
		
		self.planentry = wx.TextCtrl(self, -1, self.appointmentdata.plan, style=wx.TE_MULTILINE)
		plansizer.Add(self.planentry, 1, wx.EXPAND)
		
		middlesizer.Add(plansizer, 1, wx.EXPAND)
		
		prescribedmedicationsizer = wx.BoxSizer(wx.VERTICAL)
		
		lprescribed = wx.StaticText(self, -1, self.t("receiptlabel") + ":")
		lprescribed.SetFont(font)
		prescribedmedicationsizer.Add(lprescribed, 0, wx.ALIGN_LEFT)
		
		self.receiptlistbox = customwidgets.ReceiptListbox(self, localsettings)
		self.receiptlistbox.Bind(wx.EVT_LISTBOX, self.ReceiptItemSelected)
		
		if localsettings.changelog == 1:
			
			self.receiptlistbox.Bind(wx.EVT_RIGHT_DOWN, self.ReceiptChangeLog)
		
		
		
		prescribedmedicationsizer.Add(self.receiptlistbox, 1, wx.EXPAND)
		
		prescribedbuttonssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		deletebitmap = wx.Bitmap("icons/delete.png")
		deletemedicationbutton = wx.BitmapButton(self, -1, deletebitmap)
		deletemedicationbutton.Disable()
		deletemedicationbutton.SetToolTipString(self.t("vetformdeletereceipttooltip"))
		deletemedicationbutton.Bind(wx.EVT_BUTTON, self.DeleteReceiptEntry)
		prescribedbuttonssizer.Add(deletemedicationbutton, 0, wx.ALIGN_LEFT)
		
		prescribedbuttonssizer.Add(wx.Panel(self, size=(10,10)), 0, wx.EXPAND)
		
		prescribedbuttonssizer.Add(wx.Panel(self), 1, wx.EXPAND)
		
		receipttotallabel = wx.StaticText(self, -1, "")
		prescribedbuttonssizer.Add(receipttotallabel, 0, wx.ALIGN_CENTER)
		
		prescribedmedicationsizer.Add(prescribedbuttonssizer, 0, wx.EXPAND)
		
		rightsizer.Add(prescribedmedicationsizer, 2, wx.EXPAND)
		
		#donebitmap = wx.Bitmap("icons/submit.png")
		donebutton = wx.Button(self, -1, self.t("appointmentdonelabel"))
		donebutton.SetBackgroundColour("green")
		donebutton.Bind(wx.EVT_BUTTON, self.Done)
		donebutton.SetToolTipString(self.t("vetformdonetooltip"))
		
		middlesizer.Add(donebutton, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		mainsizer.Add(leftsizer, 1, wx.EXPAND)
		mainspacer = wx.StaticText(self, -1, "", size=(20,-1))
		mainspacer2 = wx.StaticText(self, -1, "", size=(20,-1))
		mainsizer.Add(mainspacer, 0, wx.EXPAND)
		mainsizer.Add(middlesizer, 2, wx.EXPAND)
		mainsizer.Add(mainspacer2, 0, wx.EXPAND)
		mainsizer.Add(rightsizer, 1, wx.EXPAND)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		topsizer.Add(mainsizer, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.rightsizer = rightsizer
		
		self.prescribedmedicationsizer = prescribedmedicationsizer
		self.prescribedbuttonssizer = prescribedbuttonssizer
		self.receipttotallabel = receipttotallabel
		
		self.deletemedicationbutton = deletemedicationbutton
		
		self.previousappointmentslistbox.RefreshList()
		
		self.receiptlistbox.RefreshList()
		
		self.notebook = notebook
	
	def Microchip(self, ID):
		
		self.AddMedicationDialog(4)
	
	def SubmitMicrochip(self, chipno):
		
		animaldata = animalmethods.AnimalSettings(self.appointmentdata.localsettings, False, self.appointmentdata.animaldata.ID)
		
		animaldata.chipno = chipno
		
		animaldata.Submit()
		
		self.chipbutton.Disable()
		
		self.appointmentdata.animaldata = animaldata
		
		self.notesentry.AppendText("\n" + self.t("microchippedlabel") + " # " + chipno)
	
	def AddMedication(self, ID):
		
		self.AddMedicationDialog(0)
	
	def AddVaccination(self, ID):
		
		self.AddMedicationDialog(1)
	
	def AddConsumable(self, ID):
		
		self.AddMedicationDialog(2)
	
	def AddShopItem(self, ID):
		
		self.AddMedicationDialog(3)
	
	def AddMedicationDialog(self, Type):
		
		if Type == 0:
			
			title = self.t("prescribemedicationlabel")
			
		elif Type == 1:
			
			title = self.t("animalvaccinelabel")
			
		elif Type == 2:
			
			title = self.t("consumablelabel")
			
		elif Type == 3:
			
			title = self.t("shoplabel")
			
		else:
			
			title = self.t("microchiplabel")
		
		dialog = wx.Dialog(self, -1, title)
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		medicationnamelabel = wx.StaticText(panel, -1, self.t("searchlabel"))
		font = medicationnamelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2 )
		medicationnamelabel.SetFont(font)
		topsizer.Add(medicationnamelabel, 0, wx.ALIGN_LEFT)
		
		medicationnameentry = wx.TextCtrl(panel, -1, "")
		medicationnameentry.Bind(wx.wx.EVT_TEXT, self.MedicationNameEntryKeyPress)
		topsizer.Add(medicationnameentry, 0, wx.EXPAND)
		
		medicationlabel = wx.StaticText(panel, -1, self.t("randomdatamedicationlabel"))
		medicationlabel.SetFont(font)
		topsizer.Add(medicationlabel, 0, wx.ALIGN_LEFT)
		
		medicationlistbox = wx.ListBox(panel, -1, size=(-1,200))
		medicationlistbox.Bind(wx.EVT_LISTBOX, self.MedicationChoiceSelected)
		medicationlistbox.Bind(wx.EVT_RIGHT_DOWN, self.ShowDescription)
		topsizer.Add(medicationlistbox, 1, wx.EXPAND)
		
		topsizer.Add(wx.Panel(panel, size=(10,10)), 0, wx.EXPAND)
		
		horizontalsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		quantitysizer = wx.BoxSizer(wx.VERTICAL)
		
		quantitylabel = wx.StaticText(panel, -1, self.t("quantitylabel"))
		quantitylabel.SetFont(font)
		quantitysizer.Add(quantitylabel, 0, wx.ALIGN_LEFT)
		
		quantityentry = wx.TextCtrl(panel, -1, "1", size=(100,-1))
		quantitysizer.Add(quantityentry, 0, wx.EXPAND)
		
		if Type == 1 or Type == 4:
			
			quantityentry.SetValue("1")
			quantityentry.Disable()
		
		horizontalsizer.Add(quantitysizer, 0, wx.EXPAND)
		
		unitssizer = wx.BoxSizer(wx.VERTICAL)
		
		unitssizer.Add(wx.StaticText(panel, -1, ""), 0, wx.EXPAND)
		
		unittext = self.t("unitlabel").lower()
		
		unitlabel = wx.StaticText(panel, -1, miscmethods.NoWrap(" x " + unittext + " "))
		unitssizer.Add(unitlabel, 0, wx.ALIGN_CENTER)
		
		horizontalsizer.Add(unitssizer, 0, wx.EXPAND)
		
		batchsizer = wx.BoxSizer(wx.VERTICAL)
		
		batchlabel = wx.StaticText(panel, -1, self.t("medicationbatchnolabel"))
		batchlabel.SetFont(font)
		batchsizer.Add(batchlabel, 0, wx.ALIGN_LEFT)
		
		batchentry = wx.TextCtrl(panel, -1, "", size=(100,-1))
		batchsizer.Add(batchentry, 1, wx.EXPAND)
		
		horizontalsizer.Add(batchsizer, 0, wx.EXPAND)
		
		expiressizer = wx.BoxSizer(wx.VERTICAL)
		
		expireslabel = wx.StaticText(panel, -1, self.t("medicationexpireslabel"))
		expireslabel.SetFont(font)
		expiressizer.Add(expireslabel, 0, wx.ALIGN_LEFT)
		
		expiresentry = customwidgets.DateCtrl(panel, self.localsettings)
		
		expiresentry.Clear()
		
		expiressizer.Add(expiresentry, 1, wx.EXPAND)
		
		chipnolabel = wx.StaticText(panel, -1, self.t("animalchipnolabel"))
		chipnolabel.SetFont(font)
		expiressizer.Add(chipnolabel, 0, wx.ALIGN_LEFT)
		panel.chipnoentry = wx.TextCtrl(panel, -1, "", size=(200,-1))
		expiressizer.Add(panel.chipnoentry, 1, wx.EXPAND)
		
		if Type == 4:
			
			expireslabel.Hide()
			expiresentry.Hide()
			
		else:
			
			chipnolabel.Hide()
			panel.chipnoentry.Hide()
		
		horizontalsizer.Add(expiressizer, 1, wx.EXPAND)
		
		topsizer.Add(horizontalsizer, 0, wx.EXPAND)
		
		topsizer.Add(wx.Panel(panel, size=(10,10)), 0, wx.EXPAND)
		
		instructionslabel = wx.StaticText(panel, -1, self.t("vetforminstructionslabel"))
		instructionslabel.SetFont(font)
		topsizer.Add(instructionslabel, 0, wx.ALIGN_LEFT)
		
		instructionsentry = wx.TextCtrl(panel, -1, "", style=wx.TE_MULTILINE)
		topsizer.Add(instructionsentry, 0, wx.EXPAND)
		
		if Type != 0:
			
			instructionslabel.Hide()
			instructionsentry.Hide()
		
		topsizer.Add(wx.Panel(panel, size=(10,10)), 0, wx.EXPAND)
		
		submitsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		nextduesizer = wx.BoxSizer(wx.VERTICAL)
		
		nextduelabel = wx.StaticText(panel, -1, self.t("nextduelabel"))
		nextduelabel.SetFont(font)
		nextduesizer.Add(nextduelabel, 0, wx.ALIGN_LEFT)
		
		nextdueentry = customwidgets.DateCtrl(panel, self.localsettings)
		nextdueentry.Clear()
		nextduesizer.Add(nextdueentry, 1, wx.EXPAND)
		
		submitsizer.Add(nextduesizer, 0, wx.EXPAND)
		
		if Type != 1:
			
			nextduelabel.Hide()
			nextdueentry.Hide()
		
		if Type == 0:
			
			printbuttonbitmap = wx.Bitmap("icons/printer.png")
			printbutton = wx.BitmapButton(panel, -1, printbuttonbitmap)
			printbutton.Bind(wx.EVT_BUTTON, ChooseMedicationDocument)
			printbutton.SetToolTipString(self.t("vetformprintlabeltooltip"))
			submitsizer.Add(printbutton, 0, wx.EXPAND)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		submitbutton = wx.BitmapButton(panel, -1, submitbitmap)
		submitbutton.Disable()
		submitbutton.SetToolTipString(self.t("submitlabel"))
		submitbutton.Bind(wx.EVT_BUTTON, self.SubmitMedication)
		submitsizer.Add(submitbutton, 0, wx.ALIGN_BOTTOM)
		
		topsizer.Add(submitsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		topsizer.Add(wx.Panel(panel, size=(10,10)), 0, wx.EXPAND)
		
		panel.SetSizer(topsizer)
		
		panel.medicationnameentry = medicationnameentry
		panel.batchentry = batchentry
		panel.expiresentry = expiresentry
		panel.medicationlistbox = medicationlistbox
		panel.instructionsentry = instructionsentry
		panel.quantityentry = quantityentry
		panel.nextduelabel = nextduelabel
		panel.nextdueentry = nextdueentry
		panel.submitbutton = submitbutton
		
		panel.unitlabel = unitlabel
		panel.horizontalsizer = horizontalsizer
		
		panel.Type = Type
		panel.localsettings = self.localsettings
		
		busy = wx.BusyCursor()
		action = "SELECT * FROM medication WHERE Type = " + str(panel.Type) + " ORDER BY Name"
		panel.rawmedicationdata = db.SendSQL(action, self.localsettings.dbconnection)
		panel.medicationdata = panel.rawmedicationdata
		del busy
		
		self.UpdateMedicationList(panel)
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		dialog.Fit()
		
		medicationnameentry.SetFocus()
		
		dialog.ShowModal()
	
	def MedicationNameEntryKeyPress(self, ID):
		
		medicationnameentry = ID.GetEventObject()
		
		ID.Skip()
		
		panel = medicationnameentry.GetParent()
		
		self.UpdateMedicationList(panel)
	
	def UpdateMedicationList(self, ID):
		
		try:
			
			panel = ID.GetEventObject().GetParent()
			
		except:
			
			panel = ID
		
		namecontains = panel.medicationnameentry.GetValue()
		
		filteredmedicationdata = []
		
		for a in panel.rawmedicationdata:
			
			if namecontains == "":
				
				filteredmedicationdata.append(a)
				
			else:
				
				if a[1].lower().__contains__(namecontains.lower()) == True or a[2].lower().__contains__(namecontains.lower()):
					
					filteredmedicationdata.append(a)
		
		panel.medicationlistbox.Clear()
		
		if len(filteredmedicationdata) > 0:
			
			for a in filteredmedicationdata:
				
				if self.t("currency") == "&pound;":
					
					currencysymbol = u"£"
					
				else:
					
					currencysymbol = self.t("currency")
				
				panel.medicationlistbox.Append(unicode(a[1], "utf8") + "  (" + currencysymbol + miscmethods.FormatPrice(a[5]) + "/" + unicode(a[3], "utf8") + ")")
		
		panel.medicationdata = filteredmedicationdata
		
		if len(filteredmedicationdata) == 0:
			
			panel.medicationlistbox.SetSelection(-1)
			panel.submitbutton.Disable()
			panel.batchentry.Clear()
			panel.expiresentry.Clear()
			panel.unitlabel.SetLabel(miscmethods.NoWrap(" x " + self.t("unitlabel").lower() + " "))
			panel.horizontalsizer.Layout()
			
		else:
			
			panel.medicationlistbox.SetSelection(0)
			self.MedicationChoiceSelected(panel)
			panel.submitbutton.Enable()
		
	
	def PrintLabel(self, ID):
		
		parent = ID.GetEventObject().GetParent()
		
		vetform = parent.GetGrandParent()
		
		choiceid = parent.medicationlistbox.GetSelection()
		#description = parent.medicationdata[choiceid][2]
	
	def ShowDescription(self, ID):
		
		parent = ID.GetEventObject().GetParent()
		
		vetform = parent.GetGrandParent()
		
		choiceid = parent.medicationlistbox.GetSelection()
		description = parent.medicationdata[choiceid][2]
		
		miscmethods.ShowMessage(description, parent)
	
	def SubmitMedication(self, ID):
		
		parent = ID.GetEventObject().GetParent()
		
		vetform = parent.GetGrandParent()
		
		choiceid = parent.medicationlistbox.GetSelection()
		medicationid = parent.medicationdata[choiceid][0]
		
		medicationoutdata = medicationmethods.MedicationOutData(medicationid)
		
		medicationoutdata.amount = parent.quantityentry.GetValue()
		
		if medicationoutdata.amount != "":
			
			medicationoutdata.batchno = parent.batchentry.GetValue()
			
			date = datetime.date.today()
			medicationoutdata.date = miscmethods.GetSQLDateFromDate(date)
			
			nextdue = parent.nextdueentry.GetValue()
			
			if str(nextdue) != "":
				
				nextdue = miscmethods.GetSQLDateFromWXDate(nextdue)
				
				formattedduedate = miscmethods.GetDateFromSQLDate(nextdue)
				
				formattedduedate = miscmethods.FormatDate(formattedduedate, self.localsettings)
				
				vetform.planentry.AppendText("\n" + parent.medicationdata[choiceid][1] + " " + self.t("nextduelabel") + " " + str(formattedduedate))
				
			else:
				
				nextdue = "0000-00-00"
			
			medicationoutdata.nextdue = nextdue
			
			name = parent.medicationdata[choiceid][1]
			unit = parent.medicationdata[choiceid][3]
			unitprice = parent.medicationdata[choiceid][5]
			
			instructions = parent.instructionsentry.GetValue()
			
			if instructions != "":
				
				instructions = " - " + instructions
			
			medicationoutdata.appointmentid = vetform.appointmentdata.ID
			
			description = name + ", " + str(medicationoutdata.amount) + " x " + unit
			
			price = unitprice * float(medicationoutdata.amount) * -1
			
			medicationoutdata.whereto = vetform.appointmentdata.animaldata.name + " " + vetform.appointmentdata.clientdata.surname + " (" + vetform.appointmentdata.animaldata.species + ")"
			
			medicationoutdata.Submit(self.localsettings)
			
			dbmethods.WriteToReceiptTable(self.localsettings.dbconnection, False, medicationoutdata.date, description, price, 0, medicationoutdata.ID, vetform.appointmentdata.ID, self.localsettings.userid)
			
			
			vetform.receiptlistbox.RefreshList()
			
			#print "parent.Type = " + str(parent.Type)
			
			if parent.Type == 4:
				
				chipno = parent.chipnoentry.GetValue()
				
				self.SubmitMicrochip(chipno)
				
			elif parent.Type != 3:
				
				vetform.notesentry.AppendText("\n" + medicationoutdata.amount + " x " + unit + " " + name + " (" + medicationoutdata.batchno + ")" + instructions)
			
			if parent.Type == 1:
				
				if vetform.appointmentdata.animaldata.asmref != "" and self.localsettings.asmvaccinationid > 0:
					
					try:
						
						asmconnection = db.GetASMConnection()
						
						action = "SELECT ID FROM animal WHERE ShelterCode = \"" + str(vetform.appointmentdata.animaldata.asmref) + "\""
						animalid = db.SendSQL(action, asmconnection)[0][0]
						
						action = "UPDATE animalvaccination SET DateOfVaccination = \"" + str(datetime.date.today()) + "\", Comments = CASE WHEN Comments LIKE \"%#%\" THEN CONCAT(Comments, \"" + name + " #" + medicationoutdata.batchno + ". \") ELSE \"" + name + " #" + medicationoutdata.batchno + ". \" END WHERE AnimalID = " + str(animalid) + " AND DateRequired = \"" + str(datetime.date.today()) + "\""
						db.SendSQL(action, asmconnection)
						
						action = "SELECT ID FROM animalvaccination WHERE DateRequired = \"" + str(datetime.date.today()) + "\" AND AnimalID = " + str(animalid)
						results = db.SendSQL(action, asmconnection)
						
						if len(results) == 0:
							
							action = "SELECT NextID FROM primarykey WHERE TableName = \"animalvaccination\""
							nextid = db.SendSQL(action, asmconnection)[0][0]
							
							action = "INSERT INTO animalvaccination (ID, AnimalID, VaccinationID, DateOfVaccination, DateRequired, Comments, CreatedBy, CreatedDate, LastChangedBy, LastChangedDate, RecordVersion) VALUES (" + str(nextid) + ", " + str(animalid) + ", " + str(self.localsettings.asmvaccinationid) + ", \"" + str(datetime.date.today()) + "\", \"" + str(datetime.date.today()) + "\", \"" + name + " #" + medicationoutdata.batchno + "\", \"Evette\", \"" + str(datetime.date.today()) + "\", \"Evette\", \"" + str(datetime.date.today()) + "\", 0)"
							db.SendSQL(action, asmconnection)
							
							action = "UPDATE primarykey SET NextID = NextID + 1 WHERE TableName = \"animalvaccination\""
							db.SendSQL(action, asmconnection)
						
						action = "SELECT ID FROM animalvaccination WHERE DateRequired = \"" + str(nextdue) + "\" AND AnimalID = " + str(animalid)
						results = db.SendSQL(action, asmconnection)
						
						if len(results) == 0:
							
							action = "SELECT NextID FROM primarykey WHERE TableName = \"animalvaccination\""
							nextid = db.SendSQL(action, asmconnection)[0][0]
							
							action = "INSERT INTO animalvaccination (ID, AnimalID, VaccinationID, DateRequired, Comments, CreatedBy, CreatedDate, LastChangedBy, LastChangedDate, RecordVersion) VALUES (" + str(nextid) + ", " + str(animalid) + ", " + str(self.localsettings.asmvaccinationid) + ", \"" + str(nextdue) + "\", \"" + name + "\", \"Evette\", \"" + str(datetime.date.today()) + "\", \"Evette\", \"" + str(datetime.date.today()) + "\", 0)"
							db.SendSQL(action, asmconnection)
							
							action = "UPDATE primarykey SET NextID = NextID + 1 WHERE TableName = \"animalvaccination\""
							db.SendSQL(action, asmconnection)
							
						else:
							
							action = "UPDATE animalvaccination SET Comments = CASE WHEN Comments LIKE \"%_%\" THEN CONCAT(Comments, \", " + name + ". \") ELSE \"" + name + "\" END WHERE AnimalID = " + str(animalid) + " AND DateRequired = \"" + str(nextdue) + "\""
							db.SendSQL(action, asmconnection)
					
					except:
						
						miscmethods.ShowMessage(self.t("asmerrormessage"), parent)
			
			dialog = parent.GetParent()
			
			dialog.Close()
			
		else:
			
			miscmethods.ShowMessage(self.t("quantityerrormessage"), parent)
	
	def MedicationChoiceSelected(self, ID):
		
		try:
			
			panel = ID.GetEventObject().GetParent()
			
		except:
			
			panel = ID
		
		choiceid = panel.medicationlistbox.GetSelection()
		
		currentbatch = panel.medicationdata[choiceid][4]
		expirydate = panel.medicationdata[choiceid][8]
		unit = panel.medicationdata[choiceid][3]
		
		panel.batchentry.SetValue(currentbatch)
		
		panel.unitlabel.SetLabel(miscmethods.NoWrap(" x " + unit + " "))
		panel.horizontalsizer.Layout()
		
		if expirydate == None:
			
			panel.expiresentry.Clear()
			
		else:
			
			expirydate = miscmethods.GetWXDateFromSQLDate(expirydate)
			panel.expiresentry.SetValue(expirydate)
	
	def AddProcedure(self, ID):
		
		self.AddProcedureDialog()
	
	def AddProcedureDialog(self):
		
		action = "SELECT * FROM procedures ORDER BY Name"
		proceduresdata = db.SendSQL(action, self.localsettings.dbconnection)
		
		procedures = []
		
		for a in proceduresdata:
			
			if self.t("currency") == "&pound;":
				
				currencysymbol = u"£"
				
			else:
				
				currencysymbol = self.t("currency")
			
			procedures.append(a[1] + "  (" + currencysymbol + miscmethods.FormatPrice(a[3]) + ")")
		
		dialog = wx.Dialog(self, -1, self.t("procedurelabel"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		procedurenamelabel = wx.StaticText(panel, -1, self.t("searchlabel"))
		font = procedurenamelabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		procedurenamelabel.SetFont(font)
		topsizer.Add(procedurenamelabel, 0, wx.ALIGN_LEFT)
		
		procedurenameentry = wx.TextCtrl(panel, -1, "")
		procedurenameentry.Bind(wx.wx.EVT_TEXT, self.ProcedureNameEntryKeyPress)
		topsizer.Add(procedurenameentry, 0, wx.EXPAND)
		
		procedurelabel = wx.StaticText(panel, -1, self.t("proceduresmenu"))
		procedurelabel.SetFont(font)
		topsizer.Add(procedurelabel, 0, wx.ALIGN_LEFT)
		
		procedurelistbox = wx.ListBox(panel, -1, size=(400,200))
		topsizer.Add(procedurelistbox, 0, wx.EXPAND)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		submitbutton = wx.BitmapButton(panel, -1, submitbitmap)
		submitbutton.Disable()
		submitbutton.SetToolTipString(self.t("submitlabel"))
		submitbutton.Bind(wx.EVT_BUTTON, self.SubmitProcedure)
		topsizer.Add(submitbutton, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		panel.SetSizer(topsizer)
		
		panel.procedurenameentry = procedurenameentry
		panel.proceduresdata = proceduresdata
		panel.procedurelistbox = procedurelistbox
		panel.submitbutton = submitbutton
		
		self.UpdateProcedureList(panel)
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		dialog.Fit()
		
		dialog.ShowModal()
	
	def ProcedureNameEntryKeyPress(self, ID):
		
		procedurenameentry = ID.GetEventObject()
		
		ID.Skip()
		
		panel = procedurenameentry.GetParent()
		
		self.UpdateProcedureList(panel)
	
	def UpdateProcedureList(self, ID):
		
		try:
			
			panel = ID.GetEventObject().GetParent()
			
		except:
			
			panel = ID
		
		namecontains = panel.procedurenameentry.GetValue()
		
		filteredproceduredata = []
		
		for a in panel.proceduresdata:
			
			if namecontains == "":
				
				filteredproceduredata.append(a)
				
			else:
				
				if a[1].lower().__contains__(namecontains.lower()) == True:
					
					filteredproceduredata.append(a)
		
		panel.procedurelistbox.Clear()
		
		if len(filteredproceduredata) > 0:
			
			for a in filteredproceduredata:
				
				if self.t("currency") == "&pound;":
					
					currencysymbol = u"£"
					
				else:
					
					currencysymbol = self.t("currency")
				
				panel.procedurelistbox.Append(a[1] + "  (" + currencysymbol + miscmethods.FormatPrice(a[3]) + ")")
		
		panel.filteredproceduresdata = filteredproceduredata
		
		if len(filteredproceduredata) == 0:
			
			panel.procedurelistbox.SetSelection(-1)
			panel.submitbutton.Disable()
			
		else:
			
			panel.procedurelistbox.SetSelection(0)
			#self.ProcedureChoiceSelected(panel)
			panel.submitbutton.Enable()
	
	def SubmitProcedure(self, ID):
		
		parent = ID.GetEventObject().GetParent()
		
		vetform = parent.GetGrandParent()
		
		choiceid = parent.procedurelistbox.GetSelection()
		proceduredata = parent.filteredproceduresdata[choiceid]
		
		today = datetime.date.today()
		date = miscmethods.GetSQLDateFromDate(today)
		
		procedureid = proceduredata[0]
		name = proceduredata[1]
		description = proceduredata[2]
		price = proceduredata[3] * -1
		appointmentid = self.appointmentdata.ID
		
		
		dbmethods.WriteToReceiptTable(self.localsettings.dbconnection, False, date, name, price, 1, procedureid, appointmentid, self.localsettings.userid)
		
		
		
		vetform.receiptlistbox.RefreshList()
		
		vetform.notesentry.AppendText("\n" + description)
		
		dialog = parent.GetParent()
		
		dialog.Close()
	
	def AddManual(self, ID):
		
		self.AddManualDialog()
	
	def AddManualDialog(self):
		
		dialog = wx.Dialog(self, -1, self.t("manuallabel"))
		
		dialogsizer = wx.BoxSizer(wx.VERTICAL)
		
		panel = wx.Panel(dialog)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		descriptionlabel = wx.StaticText(panel, -1, self.t("descriptionlabel"))
		font = descriptionlabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		descriptionlabel.SetFont(font)
		topsizer.Add(descriptionlabel, 0, wx.ALIGN_LEFT)
		
		descriptionentry = wx.TextCtrl(panel, -1, "", style=wx.TE_MULTILINE, size=(200,-1))
		topsizer.Add(descriptionentry, 1, wx.EXPAND)
		
		#topsizer.Add(wx.StaticText(panel, -1, "", size=(10,10)), 0, wx.EXPAND)
		
		pricelabel = wx.StaticText(panel, -1, self.t("pricelabel"))
		pricelabel.SetFont(font)
		topsizer.Add(pricelabel, 0, wx.ALIGN_LEFT)
		
		pricesizer = wx.BoxSizer(wx.HORIZONTAL)
		
		priceentry = wx.TextCtrl(panel, -1, "0.00")
		pricesizer.Add(priceentry, 0, wx.EXPAND)
		
		#topsizer.Add(wx.Panel(panel, size=(10,10)), 0, wx.EXPAND)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		submitbutton = wx.BitmapButton(panel, -1, submitbitmap)
		submitbutton.SetToolTipString(self.t("submitlabel"))
		submitbutton.Bind(wx.EVT_BUTTON, self.SubmitManual)
		pricesizer.Add(submitbutton, 0, wx.ALIGN_BOTTOM)
		
		topsizer.Add(pricesizer, 0, wx.ALIGN_LEFT)
		
		topsizer.Add(wx.Panel(panel, size=(10,10)), 0, wx.EXPAND)
		
		panel.SetSizer(topsizer)
		
		panel.descriptionentry = descriptionentry
		panel.priceentry = priceentry
		
		dialogsizer.Add(panel, 1, wx.EXPAND)
		
		dialog.SetSizer(dialogsizer)
		
		dialog.Fit()
		
		dialog.ShowModal()
	
	def SubmitManual(self, ID):
		
		parent = ID.GetEventObject().GetParent()
		vetform = parent.GetGrandParent()
		
		date = datetime.date.today()
		date = miscmethods.GetSQLDateFromDate(date)
		
		appointmentid = vetform.appointmentdata.ID
		
		price = parent.priceentry.GetValue()
		
		price = miscmethods.ConvertPriceToPennies(price) * -1
		
		description = parent.descriptionentry.GetValue()
		
		if description == "":
			
			miscmethods.ShowMessage(self.t("vetformnodescriptionmessage"), parent)
			
		else:
			
			dbmethods.WriteToReceiptTable(self.localsettings.dbconnection, False, date, description, price, 3, 0, appointmentid, self.localsettings.userid)
			
			
			
			vetform.receiptlistbox.RefreshList()
			
			parent.GetParent().Close()
	
	def ReceiptChangeLog(self, ID=False):
		
		listboxid = self.receiptlistbox.GetSelection()
		
		if listboxid > -1:
			
			changelog = self.receiptlistbox.htmllist[listboxid][7]
			
			miscmethods.ShowChangeLog(self.t("vetformreceiptitemlabel"), changelog, self.localsettings.dbconnection)
	
	def AppointmentSelected(self, ID):
		
		listboxid = self.previousappointmentslistbox.GetFocusedItem()
		appointmentid = self.previousappointmentslistbox.GetItemData(listboxid)
		
		#listboxid = self.previousappointmentslistbox.GetSelection()
		
		#appointmentid = self.previousappointmentslistbox.htmllist[listboxid][0]
		
		appointmenthtml = miscmethods.GetAppointmentDetailsHtml(self.localsettings, appointmentid, True)
		
		self.previousappointmentdetails.SetPage(appointmenthtml)
	
	def ReceiptItemSelected(self, ID):
		
		self.deletemedicationbutton.Enable()
	
	def DeleteReceiptEntry(self, ID):
		
		listboxid = self.receiptlistbox.GetSelection()
		
		receiptdata = self.receiptlistbox.htmllist[listboxid]
		
		receiptid = receiptdata[0]
		
		receipttype = receiptdata[4]
		receipttypeid = receiptdata[5]
		
		if receipttype == 0:
			
			if miscmethods.ConfirmMessage(self.t("vetformdeletereceiptmessage")) == True:
				
				action = "DELETE FROM receipt WHERE ID = " + str(receiptid)
				db.SendSQL(action, self.localsettings.dbconnection)
				
				action = "DELETE FROM medicationout WHERE ID = " + str(receipttypeid)
				db.SendSQL(action, self.localsettings.dbconnection)
				
				self.receiptlistbox.RefreshList()
		
		if receipttype == 1:
			
			if miscmethods.ConfirmMessage(self.t("vetformdeletereceiptmessage")) == True:
				
				action = "DELETE FROM receipt WHERE ID = " + str(receiptid)
				db.SendSQL(action, self.localsettings.dbconnection)
				
				self.receiptlistbox.RefreshList()
		
		if receipttype == 2:
			
			if miscmethods.ConfirmMessage(self.t("vetformdeletereceiptmessage")) == True:
				
				action = "DELETE FROM receipt WHERE ID = " + str(receiptid)
				db.SendSQL(action, self.localsettings.dbconnection)
				
				action = "DELETE FROM vaccinationout WHERE ID = " + str(receipttypeid)
				db.SendSQL(action, self.localsettings.dbconnection)
				
				self.receiptlistbox.RefreshList()
				self.vaccinationslistbox.RefreshList()
		
		if receipttype == 3:
			
			if miscmethods.ConfirmMessage(self.t("vetformdeletereceiptmessage")) == True:
				
				action = "DELETE FROM receipt WHERE ID = " + str(receiptid)
				db.SendSQL(action, self.localsettings.dbconnection)
				
				self.receiptlistbox.RefreshList()
	
	def Save(self, ID):
		
		self.appointmentdata.problem = self.problementry.GetValue()
		self.appointmentdata.notes = self.notesentry.GetValue()
		self.appointmentdata.plan = self.planentry.GetValue()
		
		self.appointmentdata.Submit()
	
	def Done(self, ID):
		
		if self.appointmentdata.staying == 0:
			
			self.appointmentdata.done = 1
			self.appointmentdata.withvet = 0
			self.appointmentdata.arrived = 1
		
		self.appointmentdata.problem = self.problementry.GetValue()
		self.appointmentdata.notes = self.notesentry.GetValue()
		self.appointmentdata.plan = self.planentry.GetValue()
		
		self.appointmentdata.Submit()
		
		try:
			
			self.viewappointmentspanel.UpdateViewAppointments(False)
			
		except:
			
			miscmethods.LogException()
		
		self.notebook.ClosePage(self.notebook.activepage)

class MedicationPanel(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return  self.localsettings.t(field,idx)
	
	def __init__(self, parent, localsettings):
		
		self.localsettings = localsettings
		
		wx.Panel.__init__(self, parent)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		entrysizer = wx.BoxSizer(wx.HORIZONTAL)
		
		resetbitmap = wx.Bitmap("icons/reset.png")
		resetbutton = wx.BitmapButton(self, -1, resetbitmap)
		resetbutton.SetToolTipString(self.t("vetformmedicationclearcontainstooltip"))
		entrysizer.Add(resetbutton, 0, wx.EXPAND)
		
		entrylabel = wx.StaticText(self, -1, " " + self.t("containslabel") + ": ")
		entrysizer.Add(entrylabel, 0, wx.ALIGN_CENTER)
		
		entry = wx.TextCtrl(self, -1, "")
		resetbutton.Bind(wx.EVT_BUTTON, self.ClearEntry)
		entrysizer.Add(entry, 1, wx.EXPAND)
		
		refreshbitmap = wx.Bitmap("icons/refresh.png")
		refreshbutton = wx.BitmapButton(self, -1, refreshbitmap)
		refreshbutton.SetToolTipString(self.t("vetformrefreshmedicationtooltip"))
		
		entrysizer.Add(refreshbutton, 0, wx.EXPAND)
		
		entryspacer = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(entryspacer, 0, wx.EXPAND)
		
		topsizer.Add(entrysizer, 0, wx.EXPAND)
		
		entryspacer1 = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(entryspacer1, 0, wx.EXPAND)
		
		listbox = MedicationListbox(self, localsettings)
		listbox.Bind(wx.EVT_LISTBOX, self.MedicationSelected)
		refreshbutton.Bind(wx.EVT_BUTTON, self.RefreshList)
		topsizer.Add(listbox, 1, wx.EXPAND)
		
		entryspacer2 = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(entryspacer2, 0, wx.EXPAND)
		
		submitsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		resetbitmap = wx.Bitmap("icons/reset.png")
		resetsubmissionbutton = wx.BitmapButton(self, -1, resetbitmap)
		resetsubmissionbutton.SetToolTipString(self.t("resetlabel"))
		resetsubmissionbutton.Bind(wx.EVT_BUTTON, self.UnSelectMedication)
		resetsubmissionbutton.Disable()
		submitsizer.Add(resetsubmissionbutton, 0, wx.EXPAND)
		
		quantityentry = wx.TextCtrl(self, -1, "")
		quantityentry.Disable()
		quantityentry.SetToolTipString(self.t("vetformnoofunitstooltip"))
		submitsizer.Add(quantityentry, 1, wx.EXPAND)
		
		unitlabel = wx.StaticText(self, -1, " x " + self.t("unitlabel") + " ")
		submitsizer.Add(unitlabel, 0, wx.ALIGN_CENTER)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		submitsubmissionbutton = wx.BitmapButton(self, -1, submitbitmap)
		submitsubmissionbutton.SetToolTipString(self.t("submitlabel"))
		submitsubmissionbutton.Bind(wx.EVT_BUTTON, self.Submit)
		submitsubmissionbutton.Disable()
		submitsizer.Add(submitsubmissionbutton, 0, wx.EXPAND)
		
		entryspacer3 = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(entryspacer3, 0, wx.EXPAND)
		
		topsizer.Add(submitsizer, 0, wx.EXPAND)
		
		entryspacer4 = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(entryspacer4, 0, wx.EXPAND)
		
		instructionssizer = wx.BoxSizer(wx.VERTICAL)
		
		instructionslabel = wx.StaticText(self, -1, self.t("vetforminstructionslabel"))
		font = instructionslabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 3)
		instructionslabel.SetFont(font)
		
		instructionssizer.Add(instructionslabel, 0, wx.ALIGN_LEFT)
		
		instructionsentry = wx.TextCtrl(self, -1, "")
		instructionsentry.Disable()
		instructionsentry.SetToolTipString(self.t("vetforminstructionstooltip"))
		#instructionsentry.Bind(wx.EVT_CHAR, self.ClearEntryLabel)
		instructionssizer.Add(instructionsentry, 0, wx.EXPAND)
		
		#instructionsspacer = wx.StaticText(self, -1, "", size=(5,-1))
		#instructionssizer.Add(instructionsspacer, 0, wx.EXPAND)
		
		topsizer.Add(instructionssizer, 0, wx.EXPAND)
		
		topsizer.Add(wx.StaticText(self, -1, "", size=(-1,5)), 0, wx.EXPAND)
		
		batchsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		batchnosizer = wx.BoxSizer(wx.VERTICAL)
		
		batchlabel = wx.StaticText(self, -1, self.t("medicationbatchnolabel"))
		font = batchlabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 3)
		batchlabel.SetFont(font)
		batchnosizer.Add(batchlabel, 0, wx.ALIGN_LEFT)
		
		batchentry = wx.TextCtrl(self, -1, "")
		batchentry.Disable()
		batchentry.SetToolTipString(self.t("vetformbatchnotooltip"))
		#batchentry.Bind(wx.EVT_CHAR, self.ClearEntryLabel)
		batchnosizer.Add(batchentry, 1, wx.EXPAND)
		
		batchsizer.Add(batchnosizer, 1, wx.EXPAND)
		
		expirydatesizer = wx.BoxSizer(wx.VERTICAL)
		
		expirylabel = wx.StaticText(self, -1, self.t("medicationexpireslabel"))
		font = expirylabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 3)
		expirylabel.SetFont(font)
		expirydatesizer.Add(expirylabel, 0, wx.ALIGN_LEFT)
		
		expiryentry = customwidgets.DateCtrl(self, self.localsettings)
		expiryentry.Clear()
		expiryentry.Disable()
		#expiryentry.Bind(wx.EVT_CHAR, self.ClearEntryLabel)
		expirydatesizer.Add(expiryentry, 1, wx.EXPAND)
		
		batchsizer.Add(expirydatesizer, 1, wx.EXPAND)
		
		batchsizer.Add(wx.StaticText(self, -1, "", size=(10,-1)), 0, wx.EXPAND)
		
		printerbitmap = wx.Bitmap("icons/printer.png")
		printlabelbutton = wx.BitmapButton(self, -1, printerbitmap)
		printlabelbutton.Disable()
		printlabelbutton.SetToolTipString(self.t("vetformprintlabeltooltip"))
		printlabelbutton.Bind(wx.EVT_BUTTON, ChooseMedicationDocument)
		batchsizer.Add(printlabelbutton, 0, wx.EXPAND)
		
		topsizer.Add(batchsizer, 0, wx.EXPAND)
		
		entryspacer5 = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(entryspacer5, 0, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.parent = parent
		
		self.entry = entry
		self.resetsubmissionbutton = resetsubmissionbutton
		self.submitsubmissionbutton = submitsubmissionbutton
		self.unitlabel = unitlabel
		self.listbox = listbox
		self.submitsizer = submitsizer
		self.quantityentry = quantityentry
		self.resetsubmissionbutton = resetsubmissionbutton
		self.instructionsentry = instructionsentry
		self.printlabelbutton = printlabelbutton
		self.batchentry = batchentry
		self.expiryentry = expiryentry
		
		listbox.RefreshList()
	
	def ClearEntryLabel(self, ID):
		
		parent = ID.GetEventObject()
		
		self.printlabelbutton.Enable()
		
		if parent.GetValue() == self.t("vetforminstructionslabel") or parent.GetValue() == self.t("medicationbatchnolabel"):
			parent.Clear()
		
		ID.Skip()
	
	def ClearEntry(self, ID):
		
		self.entry.Clear()
	
	def MedicationSelected(self, ID):
		
		listboxid = self.listbox.GetSelection()
		medicationdata = self.listbox.htmllist[listboxid]
		
		unit = medicationdata[3]
		currentbatch = medicationdata[4]
		expirydate = medicationdata[8]
		
		self.unitlabel.SetLabel(" x " + unit + " ")
		self.submitsizer.Layout()
		
		self.batchentry.SetValue(currentbatch)
		
		if expirydate == None:
			self.expiryentry.Clear()
		else:
			expirydate = miscmethods.GetWXDateFromSQLDate(expirydate)
			self.expiryentry.SetValue(expirydate)
		
		self.resetsubmissionbutton.Enable()
		self.submitsubmissionbutton.Enable()
		self.printlabelbutton.Enable()
		
		self.quantityentry.Enable()
		self.instructionsentry.Enable()
		self.batchentry.Enable()
		self.expiryentry.Enable()
		
		self.quantityentry.SetFocus()
		
	def UnSelectMedication(self, ID=False):
		
		self.listbox.SetSelection(-1)
		
		self.quantityentry.Clear()
		self.instructionsentry.Clear()
		self.batchentry.Clear()
		self.expiryentry.Clear()
		
		self.unitlabel.SetLabel(" x " + self.t("unitlabel") + " ")
		self.submitsizer.Layout()
		
		self.resetsubmissionbutton.Disable()
		self.submitsubmissionbutton.Disable()
		self.printlabelbutton.Disable()
		self.quantityentry.Disable()
		self.instructionsentry.Disable()
		self.batchentry.Disable()
		self.expiryentry.Disable()
	
	def RefreshList(self, ID):
		
		self.UnSelectMedication()
		self.listbox.RefreshList()
	
	def Submit(self, ID):
		
		listboxid = self.listbox.GetSelection()
		
		medicationdata = self.listbox.htmllist[listboxid]
		
		medicationid =  medicationdata[0]
		
		medicationoutdata = medicationmethods.MedicationOutData(medicationid)
		
		
		medicationoutdata.batchno = self.batchentry.GetValue()
		
		date = datetime.date.today()
		medicationoutdata.date = miscmethods.GetSQLDateFromDate(date)
		
		name = unicode(medicationdata[1], "utf8")
		unit = unicode(medicationdata[3], "utf8")
		unitprice = medicationdata[5]
		
		instructions = self.instructionsentry.GetValue()
		
		medicationoutdata.amount = self.quantityentry.GetValue()
		
		medicationoutdata.appointmentid = self.parent.GetParent().appointmentdata.ID
		
		description = name + ", " + str(medicationoutdata.amount) + " x " + unit
		
		price = unitprice * float(medicationoutdata.amount) * -1
		
		vetform = self.parent.GetParent()
		
		medicationoutdata.whereto = vetform.appointmentdata.animaldata.name + " " + vetform.appointmentdata.clientdata.surname + " (" + vetform.appointmentdata.animaldata.species + ")"
		
		medicationoutdata.Submit(self.localsettings)
		
		dbmethods.WriteToReceiptTable(self.localsettings.dbconnection, False, medicationoutdata.date, description, price, 0, medicationoutdata.ID, vetform.appointmentdata.ID, self.localsettings.userid)
		
		
		self.parent.GetParent().receiptlistbox.RefreshList()
		self.listbox.RefreshList()
		
		self.parent.GetParent().notesentry.AppendText("\n" + medicationoutdata.amount + " x " + unit + " " + name + " (" + medicationoutdata.batchno + ") - " + instructions)
		
		self.UnSelectMedication()
	
	def PrintLabel(self, ID):
		
		listboxid = self.listbox.GetSelection()
		medicationdata = self.listbox.htmllist[listboxid]
		
		medicationid = medicationdata[0]
		medicationbatchno = medicationdata[4]
		
		date = datetime.date.today()
		date = miscmethods.GetSQLDateFromDate(date)
		
		name = medicationdata[1]
		unit = medicationdata[3]
		unitprice = medicationdata[5]
		
		instructions = self.instructionsentry.GetValue()
		
		quantity = self.quantityentry.GetValue()
		
		if quantity == "":
			
			quantity = "0"
		
		appointmentid = self.parent.GetParent().appointmentdata.ID
		
		description = name + ", " + str(quantity) + " x " + unit
		
		price = unitprice * float(quantity) * -1
		
		price = miscmethods.FormatPrice(price)
		
		title = self.parent.GetParent().appointmentdata.clientdata.title
		forenames = self.parent.GetParent().appointmentdata.clientdata.forenames
		surname = self.parent.GetParent().appointmentdata.clientdata.surname
		address = self.parent.GetParent().appointmentdata.clientdata.address
		postcode = self.parent.GetParent().appointmentdata.clientdata.postcode
		
		
		body = """
		<table width=300 align=center>
			<tr>
				<td colspan=2 align=center>
					<font size=2><b>""" + self.localsettings.practicename + """</b></font><br>
					<font size=1>""" + self.localsettings.practiceaddress.replace("\n", ", ") + ", " + self.localsettings.practicepostcode + ", " + self.localsettings.practicetelephone + """.</font>
				</td>
			</tr>
			<tr>
				<td valign=top>
					<fieldset><legend><font size=1>""" + self.t("clientlabel") + """</font></legend>
					<font size=1>""" + title + " " + forenames + " " + surname + """<br>""" + address.replace("\n", "<br>") + "<br>" + postcode + """</font>
					</fieldset>
				</td>
				<td valign=top>
					<fieldset><legend><font size=1>""" + self.t("animallabel") + """</font></legend>
					<font size=1>""" + self.parent.GetParent().appointmentdata.animaldata.name + "<br>" + self.parent.GetParent().appointmentdata.animaldata.species + "<br>" + self.parent.GetParent().appointmentdata.animaldata.colour + """</font>
					</fieldset>
				</td>
			</tr>
			<tr>
				<td colspan=2>
					<fieldset><legend><font size=1>""" + self.t("medicationlabel") + """</font></legend>
					<font size=2><b>""" + name + " x " + quantity + """</b></font>
					</fieldset>
				</td>
			</tr>
			<tr>
				<td colspan=2>
					<fieldset><legend><font size=1>""" + self.t("vetforminstructionslabel") + """</font></legend>
					<font size=2><b>""" + instructions + """</b></font>
					</fieldset>
				</td>
			</tr>
			<tr>
				<td colspan=2 align=center>
					<font size=1>Keep all medicines out of reach of children<br>ANIMAL TREATMENT ONLY</font>
				</td>
			</tr>
		</table>
		"""
		
		formmethods.BuildLabel(self.localsettings, body)
		
		#self.printlabelbutton.Disable()

class VaccinationPanel(MedicationPanel):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, parent, localsettings):
		
		self.localsettings = localsettings
		
		wx.Panel.__init__(self, parent)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		entrysizer = wx.BoxSizer(wx.HORIZONTAL)
		
		resetbitmap = wx.Bitmap("icons/reset.png")
		resetbutton = wx.BitmapButton(self, -1, resetbitmap)
		resetbutton.SetToolTipString(self.t("vetformmedicationclearcontainstooltip"))
		entrysizer.Add(resetbutton, 0, wx.EXPAND)
		
		entrylabel = wx.StaticText(self, -1, " " + self.t("containslabel") + ": ")
		entrysizer.Add(entrylabel, 0, wx.ALIGN_CENTER)
		
		entry = wx.TextCtrl(self, -1, "")
		resetbutton.Bind(wx.EVT_BUTTON, self.ClearEntry)
		entrysizer.Add(entry, 1, wx.EXPAND)
		
		refreshbitmap = wx.Bitmap("icons/refresh.png")
		refreshbutton = wx.BitmapButton(self, -1, refreshbitmap)
		refreshbutton.SetToolTipString(self.t("vetformrefreshvaccinationtooltip"))
		
		entrysizer.Add(refreshbutton, 0, wx.EXPAND)
		
		entryspacer = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(entryspacer, 0, wx.EXPAND)
		
		topsizer.Add(entrysizer, 0, wx.EXPAND)
		
		entryspacer1 = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(entryspacer1, 0, wx.EXPAND)
		
		listbox = VaccinationListbox(self, localsettings)
		listbox.Bind(wx.EVT_LISTBOX, self.VaccinationSelected)
		refreshbutton.Bind(wx.EVT_BUTTON, self.RefreshList)
		topsizer.Add(listbox, 1, wx.EXPAND)
		
		entryspacer2 = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(entryspacer2, 0, wx.EXPAND)
		
		submitsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		resetbitmap = wx.Bitmap("icons/reset.png")
		resetsubmissionbutton = wx.BitmapButton(self, -1, resetbitmap)
		resetsubmissionbutton.SetToolTipString(self.t("resetlabel"))
		resetsubmissionbutton.Bind(wx.EVT_BUTTON, self.UnSelectVaccination)
		resetsubmissionbutton.Disable()
		submitsizer.Add(resetsubmissionbutton, 0, wx.EXPAND)
		
		nextvacclabel = wx.StaticText(self, -1, " " + self.t("nextduelabel") + ": ")
		submitsizer.Add(nextvacclabel, 0, wx.ALIGN_CENTER)
		
		nextvaccentry = customwidgets.DateCtrl(self, self.localsettings)
		nextvaccentry.Disable()
		submitsizer.Add(nextvaccentry, 1, wx.EXPAND)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		submitsubmissionbutton = wx.BitmapButton(self, -1, submitbitmap)
		submitsubmissionbutton.SetToolTipString(self.t("submitlabel"))
		submitsubmissionbutton.Bind(wx.EVT_BUTTON, self.Submit)
		submitsubmissionbutton.Disable()
		submitsizer.Add(submitsubmissionbutton, 0, wx.EXPAND)
		topsizer.Add(submitsizer, 0, wx.EXPAND)
		
		
		batchlabel = wx.StaticText(self, -1, self.t("medicationbatchnolabel"))
		font = batchlabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 3)
		batchlabel.SetFont(font)
		topsizer.Add(batchlabel, 0, wx.ALIGN_LEFT)
		
		
		batchentry = wx.TextCtrl(self, -1, "")
		batchentry.Bind(wx.EVT_CHAR, self.ClearEntryLabel)
		batchentry.SetToolTipString(self.t("vetformbatchnotooltip"))
		batchentry.Disable()
		topsizer.Add(batchentry, 0, wx.EXPAND)
		
		entryspacer3 = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(entryspacer3, 0, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.parent = parent
		
		self.entry = entry
		self.resetsubmissionbutton = resetsubmissionbutton
		self.submitsubmissionbutton = submitsubmissionbutton
		self.listbox = listbox
		self.nextvaccentry = nextvaccentry
		self.resetsubmissionbutton = resetsubmissionbutton
		self.batchentry = batchentry
		
		listbox.RefreshList()
	
	def ClearEntryLabel(self, ID):
		
		parent = ID.GetEventObject()
		
		if parent.GetValue() == self.t("medicationbatchnolabel"):
			parent.Clear()
		
		ID.Skip()
		
	
	def VaccinationSelected(self, ID):
		
		listboxid = self.listbox.GetSelection()
		currentbatch = self.listbox.htmllist[listboxid][3]
		
		self.resetsubmissionbutton.Enable()
		self.submitsubmissionbutton.Enable()
		self.nextvaccentry.Enable()
		self.batchentry.SetValue(currentbatch)
		self.batchentry.Enable()
		
	def UnSelectVaccination(self, ID=False):
		
		self.listbox.SetSelection(-1)
		
		self.resetsubmissionbutton.Disable()
		self.submitsubmissionbutton.Disable()
		today = miscmethods.GetTodaysWXDate()
		self.nextvaccentry.SetValue(today)
		self.batchentry.SetValue(self.t("medicationbatchnolabel"))
		self.batchentry.Disable()
		self.nextvaccentry.Disable()
	
	def RefreshList(self, ID):
		
		self.UnSelectVaccination()
		self.listbox.RefreshList()
	
	def Submit(self, ID):
		
		listboxid = self.listbox.GetSelection()
		vaccinationdata = self.listbox.htmllist[listboxid]
		
		vaccinationid = vaccinationdata[0]
		vaccinationbatchno = self.batchentry.GetValue()
		
		date = datetime.date.today()
		date = miscmethods.GetSQLDateFromDate(date)
		
		name = unicode(vaccinationdata[1], "utf8")
		unitprice = vaccinationdata[4] * -1
		
		appointmentid = self.parent.GetParent().appointmentdata.ID
		
		description = name
		
		price = unitprice
		
		#price = miscmethods.FormatPrice(price)
		
		vetform = self.parent.GetParent()
		
		whereto = vetform.appointmentdata.animaldata.name + " " + vetform.appointmentdata.clientdata.surname + " (" + vetform.appointmentdata.animaldata.species + ")"
		
		nextduedate = self.nextvaccentry.GetValue()
		
		nextduedate = miscmethods.GetSQLDateFromWXDate(nextduedate)
		
		vaccinationoutdata = vaccinationmethods.VaccinationOutData(vaccinationid)
		
		date = datetime.date.today()
		vaccinationoutdata.date = miscmethods.GetSQLDateFromDate(date)
		vaccinationoutdata.amount = 1
		vaccinationoutdata.batchno = vaccinationbatchno
		vaccinationoutdata.whereto = whereto
		vaccinationoutdata.appointmentid = appointmentid
		vaccinationoutdata.nextdue = nextduedate
		
		vaccinationoutdata.Submit(self.localsettings)
		
		dbmethods.WriteToReceiptTable(self.localsettings.dbconnection, False, date, description, price, 2, vaccinationoutdata.ID, appointmentid, self.localsettings.userid)
		
		self.parent.GetParent().receiptlistbox.RefreshList()
		self.listbox.RefreshList()
		
		nextduedate = miscmethods.FormatSQLDate(nextduedate, self.localsettings)
		
		self.parent.GetParent().notesentry.AppendText("\n" + name + " (" + vaccinationbatchno + ")")
		self.parent.GetParent().planentry.AppendText("\n" + name + " " + self.t("nextduelabel") + " " + nextduedate)

class ProcedurePanel(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, parent, localsettings):
		
		self.localsettings = localsettings
		
		wx.Panel.__init__(self, parent)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		entrysizer = wx.BoxSizer(wx.HORIZONTAL)
		
		resetbitmap = wx.Bitmap("icons/reset.png")
		resetbutton = wx.BitmapButton(self, -1, resetbitmap)
		resetbutton.SetToolTipString(self.t("vetformmedicationclearcontainstooltip"))
		entrysizer.Add(resetbutton, 0, wx.EXPAND)
		
		entrylabel = wx.StaticText(self, -1, " " + self.t("containslabel") + ": ")
		entrysizer.Add(entrylabel, 0, wx.ALIGN_CENTER)
		
		entry = wx.TextCtrl(self, -1, "")
		resetbutton.Bind(wx.EVT_BUTTON, self.ClearEntry)
		entrysizer.Add(entry, 1, wx.EXPAND)
		
		refreshbitmap = wx.Bitmap("icons/refresh.png")
		refreshbutton = wx.BitmapButton(self, -1, refreshbitmap)
		refreshbutton.SetToolTipString(self.t("vetformrefreshprocedurestooltip"))
		
		entrysizer.Add(refreshbutton, 0, wx.EXPAND)
		
		entryspacer = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(entryspacer, 0, wx.EXPAND)
		
		topsizer.Add(entrysizer, 0, wx.EXPAND)
		
		entryspacer1 = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(entryspacer1, 0, wx.EXPAND)
		
		listbox = ProceduresListbox(self, localsettings)
		listbox.Bind(wx.EVT_LISTBOX, self.ProcedureSelected)
		listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.Submit)
		refreshbutton.Bind(wx.EVT_BUTTON, self.RefreshList)
		topsizer.Add(listbox, 1, wx.EXPAND)
		
		entryspacer2 = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(entryspacer2, 0, wx.EXPAND)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		submitsubmissionbutton = wx.BitmapButton(self, -1, submitbitmap)
		submitsubmissionbutton.SetToolTipString(self.t("submitlabel"))
		submitsubmissionbutton.Bind(wx.EVT_BUTTON, self.Submit)
		submitsubmissionbutton.Disable()
		topsizer.Add(submitsubmissionbutton, 0, wx.ALIGN_RIGHT)
		
		entryspacer3 = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(entryspacer3, 0, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.entry = entry
		self.submitsubmissionbutton = submitsubmissionbutton
		self.listbox = listbox
		self.parent = parent
		
		listbox.RefreshList()
	
	def ClearEntry(self, ID):
		
		self.entry.Clear()
	
	def ProcedureSelected(self, ID):
		
		listboxid = self.listbox.GetSelection()
		proceduredata = self.listbox.htmllist[listboxid]
		
		self.submitsubmissionbutton.Enable()
	
	def UnSelectProcedure(self, ID):
		
		self.listbox.SetSelection(-1)
		
		self.submitsubmissionbutton.Disable()
	
	def RefreshList(self, ID=False):
		
		self.submitsubmissionbutton.Disable()
		self.listbox.SetSelection(-1)
		self.listbox.RefreshList()
	
	def Submit(self, ID):
		
		listboxid = self.listbox.GetSelection()
		proceduredata = self.listbox.htmllist[listboxid]
		
		procedureid = proceduredata[0]
		
		date = datetime.date.today()
		date = miscmethods.GetSQLDateFromDate(date)
		
		name = proceduredata[1]
		price = proceduredata[3] * -1
		description = proceduredata[2]
		appointmentid = self.parent.GetParent().appointmentdata.ID
		
		dbmethods.WriteToReceiptTable(self.localsettings.dbconnection, False, date, name, price, 1, procedureid, appointmentid, self.localsettings.userid)
		
		self.parent.GetParent().receiptlistbox.RefreshList()
		
		self.parent.GetParent().notesentry.AppendText("\n" + description)

class ManualPanel(wx.Panel):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, parent, localsettings):
		
		self.localsettings = localsettings
		
		wx.Panel.__init__(self, parent)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		spacer = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(spacer, 0, wx.EXPAND)
		
		descriptionlabel = wx.StaticText(self, -1, self.t("descriptionlabel") + ":")
		font = descriptionlabel.GetFont()
		font.SetPointSize(font.GetPointSize() - 2)
		descriptionlabel.SetFont(font)
		topsizer.Add(descriptionlabel, 0, wx.ALIGN_LEFT)
		
		descriptionentry = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
		topsizer.Add(descriptionentry, 1, wx.EXPAND)
		
		spacer2 = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(spacer2, 0, wx.EXPAND)
		
		pricesizer = wx.BoxSizer(wx.HORIZONTAL)
		
		resetbitmap = wx.Bitmap("icons/reset.png")
		resetbutton = wx.BitmapButton(self, -1, resetbitmap)
		resetbutton.SetToolTipString(self.t("resetlabel"))
		resetbutton.Bind(wx.EVT_BUTTON, self.ClearEntry)
		pricesizer.Add(resetbutton, 0, wx.EXPAND)
		
		pricespacer = wx.StaticText(self, -1, "", size=(5,-1))
		
		pricelabel = wx.StaticText(self, -1, self.t("pricelabel") + ":")
		pricelabel.SetFont(font)
		pricesizer.Add(pricelabel, 0, wx.ALIGN_LEFT)
		pricesizer.Add(pricespacer, 0, wx.EXPAND)
		
		priceentry = wx.TextCtrl(self, -1, "")
		pricesizer.Add(priceentry, 1, wx.EXPAND)
		
		pricespacer2 = wx.StaticText(self, -1, "", size=(5,-1))
		pricesizer.Add(pricespacer2, 0, wx.EXPAND)
		
		submitbitmap = wx.Bitmap("icons/submit.png")
		submitsubmissionbutton = wx.BitmapButton(self, -1, submitbitmap)
		submitsubmissionbutton.SetToolTipString(self.t("submitlabel"))
		submitsubmissionbutton.Bind(wx.EVT_BUTTON, self.Submit)
		pricesizer.Add(submitsubmissionbutton, 0, wx.ALIGN_BOTTOM)
		
		topsizer.Add(pricesizer, 0, wx.EXPAND)
		
		spacer3 = wx.StaticText(self, -1, "", size=(-1,5))
		topsizer.Add(spacer3, 0, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.parent = parent
		self.priceentry = priceentry
		self.descriptionentry = descriptionentry
	
	def ClearEntry(self, ID):
		
		self.priceentry.Clear()
		self.descriptionentry.Clear()
	
	def Submit(self, ID):
		
		date = datetime.date.today()
		date = miscmethods.GetSQLDateFromDate(date)
		
		appointmentid = self.parent.GetParent().appointmentdata.ID
		
		price = self.priceentry.GetValue()
		
		price = miscmethods.ConvertPriceToPennies(price) * -1
		
		if price != 1:
			
			description = self.descriptionentry.GetValue()
			
			if description == "":
				miscmethods.ShowMessage(self.t("vetformnodescriptionmessage"))
			else:
				
				dbmethods.WriteToReceiptTable(self.localsettings.dbconnection, False, date, description, price, 3, 0, appointmentid, self.localsettings.userid)
				
				self.parent.GetParent().receiptlistbox.RefreshList()

class MedicationListbox(wx.HtmlListBox):
	
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
			total = self.htmllist[n][-1]
			price = self.htmllist[n][5]
			price = miscmethods.FormatPrice(price)
			
			output = "<table width=100% cellpadding=0 cellspacing=0><tr><td align=left><font color=blue>" + name + "</font>&nbsp;<font size=2>(&pound;" + str(price) + ")</font></td><td align=right>" + str(total) + "&nbsp;</td></tr></table>"
			
			return output
	
	def RefreshList(self, ID=False):
		
		self.Hide()
		entrytext = self.parent.entry.GetValue()
		
		action = "SELECT * FROM medication WHERE Name LIKE \"%" + entrytext + "%\" ORDER BY Name"
		medication = db.SendSQL(action, self.localsettings.dbconnection)
		
		action = "SELECT * FROM medicationin"
		medicationin = db.SendSQL(action, self.localsettings.dbconnection)
		
		action = "SELECT * FROM medicationout"
		medicationout = db.SendSQL(action, self.localsettings.dbconnection)
		
		
		self.htmllist = []
		
		
		for a in medication:
			
			medicationintotal = 0
			
			if len(medicationin) > 0:
				
				for b in medicationin:
					
					if b[1] == a[0]:
						
						medicationintotal = medicationintotal + int(b[3])
			
			medicationouttotal = 0
			
			if len(medicationout) > 0:
				
				for b in medicationout:
					
					if b[1] == a[0]:
						
						medicationouttotal = medicationouttotal + int(b[3])
			
			total = medicationintotal - medicationouttotal
			
			if total > 0:
				
				total = (total,)
				
				self.htmllist.append(a + total)
		
		self.SetItemCount(len(self.htmllist))
		
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
		
		if len(self.htmllist) != 0:
			
			name = self.htmllist[n][1]
			total = self.htmllist[n][-1]
			price = self.htmllist[n][4]
			price = miscmethods.FormatPrice(price)
			
			output = "<table width=100% cellpadding=0 cellspacing=0><tr><td align=left><font color=blue>" + name + "</font>&nbsp;<font size=2>(&pound;" + str(price) + ")</font></td><td align=right>" + str(total) + "&nbsp;</td></tr></table>"
			
			return output
	
	def RefreshList(self, ID=False):
		
		self.Hide()
		entrytext = self.parent.entry.GetValue()
		
		action = "SELECT * FROM vaccinationtype WHERE Name LIKE \"%" + entrytext + "%\" ORDER BY Name"
		vaccination = db.SendSQL(action, self.localsettings.dbconnection)
		
		action = "SELECT * FROM vaccinationin"
		vaccinationin = db.SendSQL(action, self.localsettings.dbconnection)
		
		action = "SELECT * FROM vaccinationout"
		vaccinationout = db.SendSQL(action, self.localsettings.dbconnection)
		
		
		self.htmllist = []
		
		
		for a in vaccination:
			
			vaccinationintotal = 0
			
			if len(vaccinationin) > 0:
				
				for b in vaccinationin:
					
					if b[1] == a[0]:
						
						vaccinationintotal = vaccinationintotal + int(b[3])
			
			vaccinationouttotal = 0
			
			if len(vaccinationout) > 0:
				
				for b in vaccinationout:
					
					if b[1] == a[0]:
						
						vaccinationouttotal = vaccinationouttotal + int(b[3])
			
			total = vaccinationintotal - vaccinationouttotal
			
			if total > 0:
				
				total = (total,)
				
				self.htmllist.append(a + total)
		
		self.SetItemCount(len(self.htmllist))
		
		self.Show()

class ProceduresListbox(wx.HtmlListBox):
	
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
			price = self.htmllist[n][3]
			price = miscmethods.FormatPrice(price)
			
			output = "<table width=100% cellpadding=0 cellspacing=0><tr><td align=left><font color=blue>" + name + "</font></td><td align=right>&pound;" + price + "&nbsp;</td></tr></table>"
			
			return output
	
	def RefreshList(self, ID=False):
		
		self.Hide()
		entrytext = self.parent.entry.GetValue()
		
		action = "SELECT * FROM procedures WHERE Name LIKE \"%" + entrytext + "%\" ORDER BY Name"
		results = db.SendSQL(action, self.localsettings.dbconnection)
		
		self.htmllist = results
		
		self.SetItemCount(len(self.htmllist))
		
		self.Show()

def ChooseMedicationDocument(ID):
	
	parent = ID.GetEventObject().GetParent()
	
	dialog = wx.Dialog(parent, -1, "Choose a template")
	dialog.parent = parent
	
	dialogsizer = wx.BoxSizer(wx.VERTICAL)
	
	panel = wx.Panel(dialog)
	
	panel.parent = parent
	panel.localsettings = parent.localsettings
	
	topsizer = wx.BoxSizer(wx.VERTICAL)
	
	action = "SELECT Title FROM form WHERE FormType = \"medication\""
	results = db.SendSQL(action, panel.localsettings.dbconnection)
	
	
	panel.listbox = wx.ListBox(panel, -1)
	panel.listboxtitles = []
	
	for a in results:
		panel.listbox.Append(a[0])
		panel.listboxtitles.append(a[0])
	
	if len(panel.listboxtitles) > 0:
		
		panel.listbox.SetSelection(0)
	
	topsizer.Add(panel.listbox, 1, wx.EXPAND)
	
	submitbutton = wx.Button(panel, -1, "Submit")
	submitbutton.Bind(wx.EVT_BUTTON, GenerateMedicationDocument)
	topsizer.Add(submitbutton, 0, wx.ALIGN_CENTER)
	
	panel.SetSizer(topsizer)
	
	dialogsizer.Add(panel, 1, wx.EXPAND)
	
	dialog.SetSizer(dialogsizer)
	
	dialog.ShowModal()

def GenerateMedicationDocument(ID):
	
	panel = ID.GetEventObject().GetParent()
	
	listboxid = panel.listbox.GetSelection()
	
	dialog = panel.GetParent()
	
	if listboxid > -1:
		
		choiceid = panel.parent.medicationlistbox.GetSelection()
		
		medicationname = panel.parent.medicationdata[choiceid][1]
		
		appointmentdata = dialog.parent.GetGrandParent().appointmentdata
		
		unit = panel.parent.medicationdata[choiceid][3]
		quantity = panel.parent.quantityentry.GetValue()
		instructions = panel.parent.instructionsentry.GetValue()
		batchno = panel.parent.batchentry.GetValue()
		expires = panel.parent.expiresentry.GetValue()
		
		listboxid = panel.listbox.GetSelection()
		title = panel.listboxtitles[listboxid]
		
		formmethods.GenerateMedicationDocument(title, appointmentdata, medicationname, unit, quantity, instructions, batchno, expires)
	
	dialog.Close()

#panel.medicationdata = medicationdata
#panel.batchentry = batchentry
#panel.expiresentry = expiresentry
#panel.medicationchoice = medicationchoice
#panel.instructionsentry = instructionsentry
#panel.quantityentry = quantityentry
#panel.nextduelabel = nextduelabel
#panel.nextdueentry = nextdueentry
