#!/usr/bin/python

import wx

class DrawPanel(wx.Panel):

    """Draw a line to a panel."""

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen("BLACK", 4))
        dc.DrawLine(0, 0, 50, 50)

app = wx.PySimpleApp(False)
frame = wx.Frame(None, title="Draw on Panel")
DrawPanel(frame)
frame.Show(True)
app.MainLoop()