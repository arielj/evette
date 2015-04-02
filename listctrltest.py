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
import wx.lib.mixins.listctrl as listmix


class ListCtrl(wx.Panel, listmix.ColumnSorterMixin):
	
	def t(self, field, idx = 0):
		
		return self.localsettings.t(field,idx)
	
	def __init__(self, parent, localsettings, columns):
		
		wx.Panel.__init__(self, parent)
		
		topsizer = wx.BoxSizer(wx.VERTICAL)
		
		buttonssizer = wx.BoxSizer(wx.HORIZONTAL)
		
		clearbutton = wx.Button(self, -1, "Clear")
		clearbutton.Bind(wx.EVT_BUTTON, self.DeselectAll)
		buttonssizer.Add(clearbutton, 0, wx.EXPAND)
		
		getselectionbutton = wx.Button(self, -1, "Get Selection")
		getselectionbutton.Bind(wx.EVT_BUTTON, self.GetSelection)
		buttonssizer.Add(getselectionbutton, 0, wx.EXPAND)
		
		setselectionbutton = wx.Button(self, -1, "Set Selection 1")
		setselectionbutton.Bind(wx.EVT_BUTTON, self.SetSelection)
		buttonssizer.Add(setselectionbutton, 0, wx.EXPAND)
		
		topsizer.Add(buttonssizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
		
		self.listctrl = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
		listmix.ColumnSorterMixin.__init__(self, 2)
		
		self.listctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.ItemSelected)
		self.listctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.DoubleClick)
		self.listctrl.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.RightClick)
		
		topsizer.Add(self.listctrl, 1, wx.EXPAND)
		
		self.SetSizer(topsizer)
		
		self.localsettings = localsettings
		self.columns = columns
		self.htmllist = htmllist
		
		self.RefreshList()
	
	def GetSelection(self, ID):
		
		selection = -1
		
		for a in range(0, len(self.htmllist)):
			
			if self.listctrl.IsSelected(a) == True:
				
				selection = a
	
	def SetSelection(self, ID):
		
		self.listctrl.Select(1)
	
	def DeselectAll(self, ID):
		
		for a in range(0, len(self.htmllist)):
			
			self.listctrl.Select(a, 0)
	
	def ItemSelected(self, ID):
		
		focuseditem = self.listctrl.GetFocusedItem()
		
		print "Item Selected - " + str(focuseditem)
		
	def RightClick(self, ID):
		
		print "Right click"
		
	def DoubleClick(self, ID):
		
		print "Double Click"
	
	def GetListCtrl(self):# Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
		
        	return self.listctrl
	
	def RefreshList(self):
		
		self.itemDataMap = {}
		
		self.listctrl.ClearAll()
		
		count = 0
		
		for a in self.columns:
			
			self.listctrl.InsertColumn(count, a)
			
			count = count + 1
		
		count = 0
		
		for a in self.htmllist:
			
			self.itemDataMap[a[1]] = ( a[0], a[1] )
			
			self.listctrl.InsertStringItem(count, a[0])
			self.listctrl.SetStringItem(count, 1, str(a[1]) )
			
			self.listctrl.SetItemData(count, a[1])
			
			count = count + 1
			
		self.listctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
		self.listctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE)
		
		self.htmllist = results

app = wx.App()
frame = wx.Frame(None, -1, "ListCtrl Test")
panel = ListCtrlPanel(frame)
frame.Show()
app.MainLoop()
