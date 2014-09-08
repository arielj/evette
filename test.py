### SmallApp.py/pyw:
###     Small test wxPython program along with py2Exe scripts to build a windows executable
###     ToDo:
###         - wrap RTB, menu items, etc in classes (see DemoA.py for a good example)

import os
import time
from wxPython.wx import *

#-------------------------------------------------------------------------------
# Define booleans until Python ver 2.3
True=1
False=0

APP_NAME = "SmallApp"

# --- Menu and control ID's
ID_NEW=101
ID_OPEN=102
ID_SAVE=103
ID_SAVEAS=104
ID_EXIT=109
ID_ABOUT=141
ID_RTB=201

SB_INFO = 0
SB_ROWCOL = 1
SB_DATETIME = 2

#-------------------------------------------------------------------------------
# --- our frame class
class smallAppFrame(wxFrame):
    """ Derive a new class of wxFrame. """


    def __init__(self, parent, id, title):
        # --- a basic window frame/form
        wxFrame.__init__(self, parent = None, id = -1,
                         title = APP_NAME + " - Greg's 1st wxPython App",
                         pos = wxPoint(200, 200), size = wxSize(379, 207),
                         name = '', style = wxDEFAULT_FRAME_STYLE)

        # --- real windows programs have icons, so here's ours!
        # XXX see about integrating this into our app or a resource file
        #try:            # - don't sweat it if it doesn't load
            #self.SetIcon(wxIcon("test.ico", wxBITMAP_TYPE_ICO))
        #finally:
            #pass

        # --- add a menu, first build the menus (with accelerators
        fileMenu = wxMenu()

        fileMenu.Append(ID_NEW, "&New\tCtrl+N", "Creates a new file")
        EVT_MENU(self, ID_NEW, self.OnFileNew)
        fileMenu.Append(ID_OPEN, "&Open\tCtrl+O", "Opens an existing file")
        EVT_MENU(self, ID_OPEN, self.OnFileOpen)
        fileMenu.Append(ID_SAVE, "&Save\tCtrl+S", "Save the active file")
        EVT_MENU(self, ID_SAVE, self.OnFileSave)
        fileMenu.Append(ID_SAVEAS, "Save &As...", "Save the active file with a new name")
        EVT_MENU(self, ID_SAVEAS, self.OnFileSaveAs)

        fileMenu.AppendSeparator()
        fileMenu.Append(ID_EXIT, "E&xit\tAlt+Q", "Exit the program")
        EVT_MENU(self, ID_EXIT, self.OnFileExit)

        helpMenu = wxMenu()
        helpMenu.Append(ID_ABOUT, "&About", "Display information about the program")
        EVT_MENU(self, ID_ABOUT, self.OnHelpAbout)

        # --- now add them to a menubar & attach it to the frame
        menuBar = wxMenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)

        #  Not needed!, just put them in text form after tab in menu item!
        # --- add accelerators to the menus
        #self.SetAcceleratorTable(wxAcceleratorTable([(wxACCEL_CTRL, ord('O'), ID_OPEN), 
        #                          (wxACCEL_ALT, ord('Q'), ID_EXIT)]))

        # --- add a statusBar (with date/time panel)
        sb = self.CreateStatusBar(3)
        sb.SetStatusWidths([-1, 65, 150])
        sb.PushStatusText("Ready", SB_INFO)
        # --- set up a timer to update the date/time (every 5 seconds)
        self.timer = wxPyTimer(self.Notify)
        self.timer.Start(5000)
        self.Notify()       # - call it once right away

        # --- add a control (a RichTextBox) & trap KEY_DOWN event
        self.rtb = wxTextCtrl(self, ID_RTB, size=wxSize(400,200),
                              style=wxTE_MULTILINE | wxTE_RICH2)
        ### - NOTE: binds to the control itself!
        EVT_KEY_UP(self.rtb, self.OnRtbKeyUp)

        # --- need to add a sizer for the control - yuck!
        self.sizer = wxBoxSizer(wxVERTICAL)
        # self.sizer.SetMinSize(200,400)
        self.sizer.Add(self.rtb, 1, wxEXPAND)
        # --- now add it to the frame (at least this auto-sizes the control!)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.SetSizeHints(self)

        # --- initialize other settings
        self.dirName = ""
        self.fileName = ""

        # - this is ugly, but there's no static available 
        #   once we build a class for RTB, move this there
        self.oldPos = -1
        self.ShowPos()

        # --- finally - show it!
        self.Show(True)

#---------------------------------------
    def __del__(self):
        """ Class delete event: don't leave timer hanging around! """
        self.timer.stop()
        del self.timer

#---------------------------------------
    def Notify(self):
        """ Timer event """
        t = time.localtime(time.time())
        st = time.strftime(" %b-%d-%Y  %I:%M %p", t)
        # --- could also use self.sb.SetStatusText
        self.SetStatusText(st, SB_DATETIME)

#---------------------------------------
    def OnFileExit(self, e):
        """ File|Exit event """
        self.Close(True)

#---------------------------------------
    def OnFileNew(self, e):
        """ File|New event - Clear rtb. """
        self.fileName = ""
        self.dirName = ""
        self.rtb.SetValue("")
        self.PushStatusText("Starting new file", SB_INFO)
        self.ShowPos()

#---------------------------------------
    def OnFileOpen(self, e):
        """ File|Open event - Open dialog box. """
        dlg = wxFileDialog(self, "Open", self.dirName, self.fileName,
                           "Text Files (*.txt)|*.txt|All Files|*.*", wxOPEN)
        if (dlg.ShowModal() == wxID_OK):
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()

            ### - this will read in Unicode files (since I'm using Unicode wxPython
            #if self.rtb.LoadFile(os.path.join(self.dirName, self.fileName)):
            #    self.SetStatusText("Opened file: " + str(self.rtb.GetLastPosition()) + 
            #                       " characters.", SB_INFO)
            #    self.ShowPos()
            #else:
            #    self.SetStatusText("Error in opening file.", SB_INFO)

            ### - but we want just plain ASCII files, so:
            try:
                f = file(os.path.join(self.dirName, self.fileName), 'r')
                self.rtb.SetValue(f.read())
                self.SetTitle(APP_NAME + " - [" + self.fileName + "]")
                self.SetStatusText("Opened file: " + str(self.rtb.GetLastPosition()) +
                                   " characters.", SB_INFO)
                self.ShowPos()
                f.close()
            except:
                self.PushStatusText("Error in opening file.", SB_INFO)
        dlg.Destroy()

#---------------------------------------
    def OnFileSave(self, e):
	
	print str(e.GetEventObject())
	
        """ File|Save event - Just Save it if it's got a name. """
        if (self.fileName != "") and (self.dirName != ""):
            try:
                f = file(os.path.join(self.dirName, self.fileName), 'w')
                f.write(self.rtb.GetValue())
                self.PushStatusText("Saved file: " + str(self.rtb.GetLastPosition()) +
                                    " characters.", SB_INFO)
                f.close()
                return True
            except:
                self.PushStatusText("Error in saving file.", SB_INFO)
                return False
        else:
            ### - If no name yet, then use the OnFileSaveAs to get name/directory
            return self.OnFileSaveAs(e)

#---------------------------------------
    def OnFileSaveAs(self, e):
        """ File|SaveAs event - Prompt for File Name. """
        ret = False
        dlg = wxFileDialog(self, "Save As", self.dirName, self.fileName,
                           "Text Files (*.txt)|*.txt|All Files|*.*", wxSAVE)
        if (dlg.ShowModal() == wxID_OK):
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()
            ### - Use the OnFileSave to save the file
            if self.OnFileSave(e):
                self.SetTitle(APP_NAME + " - [" + self.fileName + "]")
                ret = True
        dlg.Destroy()
        return ret

#---------------------------------------
    def OnHelpAbout(self, e):
        """ Help|About event """
        title = self.GetTitle()
        d = wxMessageDialog(self, "About " + title, title, wxICON_INFORMATION | wxOK)
        d.ShowModal()
        d.Destroy()

#---------------------------------------
    def OnRtbKeyUp(self, e):
        """ Update Row/Col indicator based on position """
        self.ShowPos()
        e.Skip()

#---------------------------------------
    def ShowPos(self):
        """ Update Row/Col indicator """
        (bPos,ePos) = self.rtb.GetSelection()
        if (self.oldPos != ePos):
            (c,r) = self.rtb.PositionToXY(ePos)
            self.SetStatusText(" " + str((r+1,c+1)), SB_ROWCOL)
        self.oldPos = ePos

# --- end [testFrame] class


#-------------------------------------------------------------------------------
# --- Program Entry Point
app = wxPySimpleApp()
# --- note: Title never gets used!
frame = smallAppFrame(NULL, -1, "Small wxPython Application")
# frame.Show(True)  # - now shown in class __init__
app.MainLoop()