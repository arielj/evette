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

import os
import sys
import logging
import traceback
import db
import settings
import wx
import datetime
import appointmentmethods
import base64
import random
import re
from decimal import Decimal

logging.basicConfig(filename='exceptions.log')

def GetImagePath():
  
  imageslist = []
  
  for a in os.listdir("icons/images"):
    
    if a.split(".")[-1].lower() == "jpg":
      
      imageslist.append(a)
  
  
  return "icons/images/" + imageslist[int(random.random() * len(imageslist))]

def GetSex(localsettings, sexint):
  
  if sexint == 1:
    
    sex = localsettings.t("malelabel")
    
  elif sexint == 2:
    
    sex = localsettings.t("femalelabel")
    
  else:
    
    sex = localsettings.t("unknownlabel")
  
  return sex

def GetAgeFromDOB(dob, localsettings):
  
  try:
    
    if localsettings.t("dateformat") == "DDMMYYYY":
      
      if len(dob) == 4:
        
        day = "01"
        month = "01"
        year = dob
        
      elif len(dob) == 7:
        
        day = "01"
        month = dob[:2]
        year = dob[-4:]
        
      else:
        
        day = dob[0:2]
        month = dob[3:5]
        year = dob[6:10]
      
    elif localsettings.t("dateformat") == "MMDDYYYY":
      
      if len(dob) == 4:
        
        day = "01"
        month = "01"
        year = dob
        
      elif len(dob) == 7:
        
        day = "01"
        month = dob[:2]
        year = dob[-4:]
        
      else:
        
        day = dob[3:5]
        month = dob[0:2]
        year = dob[6:10]
      
    else:
      
      if len(dob) == 4:
        
        day = "01"
        month = "01"
        year = dob
        
      elif len(dob) == 7:
        
        day = "01"
        month = dob[:2]
        year = dob[-4:]
        
      else:
        
        day = dob[-2:]
        month = dob[5:7]
        year = dob[:4]
    
    #print "Day: " + day
    #print "Month: " + month
    #print "Year: " + year
    
    today = datetime.date.today()
    dob = datetime.date(int(year), int(month), int(day))
    
    timedelta = today - dob
    
    days = timedelta.days
    
    weeks = 0
    months = 0
    years = 0
    
    while days >= 365:
      
      years = years + 1
      days = days - 365
    
    while days >= 30:
      
      months = months + 1
      days = days - 30
    
    while days >= 7:
      
      weeks = weeks + 1
      days = days - 7
    
    age = ""
    
    if years > 0:
      
      age += str(years) + " " + localsettings.t("yearslabel") + " "
      
    elif months > 0:
      
      age += str(months) + " " + localsettings.t("monthslabel") + " "
      
    else:
      
      age += str(weeks) + " " + localsettings.t("weekslabel") + " " + str(days) + " " + localsettings.t("dayslabel") + " "
    
    return age
    
  except:
    
    return localsettings.t("invaliddobtooltip").lower()
  

def NoWrap(string):
  
  ###Altered code from Jurgis Pralgauskis
  
  try:
    string = unicode(string).replace(u" ", u"\xa0")
    
  except UnicodeDecodeError:
    
    print "NoWrap error"
  
  return string
  
  ###Original code
  
  #string = string.replace(" ", u"\xa0")
  
  #return string

# monthint goes from 1 to 12!!!
def GetMonth(monthint, localsettings):
  return localsettings.t('monthnames',monthint-1)

def GetWeekday(weekdayint, localsettings):
  
  return GetDayNameFromID(weekdayind,localsettings)

def GetTimeFromMinutes(time):
  
  hour = str(float(time) / 60).split(".")[0]
  if len(hour) == 1:
    hour = "0" + hour
  
  minutes = str(float(time) / 60).split(".")[1]
  minutes = float("0." + minutes)
  minutes = str(float(minutes * 60))
  if int(minutes.split(".")[1][0]) < 5:
    minutes = minutes.split(".")[0]
  else:
    minutes = str(int(minutes.split(".")[0]) + 1)
  
  if len(minutes) == 1:
    minutes = "0" + minutes
  
  timestring = str(hour) + ":" + str(minutes)
  
  return timestring

def GetMinutesFromTime(time):
  
  minutes = ( int(time.split(":")[0]) * 60 ) + int(time.split(":")[1])
  
  return minutes

def GetTimeFromMinutes(minutes):
  
  hours = 0
  
  while minutes > 59:
    
    hours = hours + 1
    minutes = minutes - 60
  
  if len(str(hours)) == 1:
    
    hours = "0" + str(hours)
  
  if len(str(minutes)) == 1:
    
    minutes = "0" + str(minutes)
  
  return str(hours) + ":" + str(minutes)

def GetHome():
  
  if str(sys.platform)[:3] == "lin":
    home = os.environ["HOME"]
    
  elif str(sys.platform)[:3] == "win":
    home = os.environ["USERPROFILE"]
  else:
    home = False
  
  return home

def CheckConfFileExists():
  
  home = GetHome()
  conffile = home + "/.evette.conf"
  if os.path.isfile(conffile):
    success = True
  else:
    success = False
  
  return success

def CheckEvetteFolderExists():
  
  home = GetHome()
  evettefolder = home + "/.evette"
  if os.path.isdir(evettefolder):
    success = True
  else:
    success = False
  
  return success

def CreateEvetteFolder():
  
  localsettings = settings.settings(False)
  localsettings.GetSettings()
  
  home = GetHome()
  evettefolder = home + "/.evette"
  os.mkdir(evettefolder)
  os.mkdir(evettefolder + "/html")
  os.mkdir(evettefolder + "/temp")
  os.mkdir(evettefolder + "/templates")
  header = """\
<html>
<head>
  <meta http-equiv='content-type' content='text/html; charset=UTF-8' />
  <style type='text/css'>
    #wrapper {
      width: 800px;
      margin: 0 auto;
    }
    .appointment {
      width: 100%%;
      font-size: 1em;
      font-family: Arial, Helvetica, sans-serif;
    }
  </style>
</head>
<body>
  <div id='wrapper'>
    <table id='wrapper' cellpadding=0 cellspacing=10>
      <tr>
        <td class='vetname' valign=top>$$vetname$$</td>
        <td valign=middle align=right>
          <font size=1 color=red>%(h1)s<br></font><font size=1><i>%(h2)s <br>$HOME/.evette/html/header.dat</i></font>
        </td>
      </tr>
    </table>
    <hr>""" % {'h1': localsettings.t("headertext1").encode('utf-8'), 'h2': localsettings.t("headertext2").encode('utf-8')}

  out = open(evettefolder + "/html/header.dat", "w")
  out.write(header)
  out.close()

def CheckDBConnection():
  
  localsettings = settings.settings(False)
  success = False
  try:
    localsettings.GetSettings()
    connection = db.GetConnection(localsettings)
    connection.close()
    success = True
  except:
    LogException()
  
  return success

def GetPageTitle(notebook, pagetitle):
  
  occurrences = 0
  
  for a in notebook.pages:
    
    if a.pagetitle[0:len(pagetitle)] == pagetitle:
      
      occurrences = occurrences + 1
  
  if occurrences == 0:
    output = pagetitle
  else:
    output = pagetitle + " (" + str(occurrences) + ")"
  
  if notebook.localsettings.multiplepanels == 0:
    
    output = pagetitle
  
  return output

def ConfirmMessage(message, parent=None):
  
  dialog = wx.MessageDialog(parent, message, "Evette", wx.YES_NO)
  
  if dialog.ShowModal() == wx.ID_YES:
    
    output = True
    
  else:
    
    output = False
  
  return output

def ClosePanel(ID):
  
  try:
    panel = ID.GetEventObject().GetParent()
  except:
    panel = ID
  
  notebook = panel.GetParent()
  notebook.ClosePage(self.activepage)

def FormatText(text):
  
  #localsettings = settings.settings(False)
  #localsettings.GetSettings()
  
  #if localsettings.language == 0:
    
    #if text != "":
      
      #output = ""
      #maintextlist = text.split("\n")
      #for b in range(0, len(maintextlist)):
        #textlist = maintextlist[b].split(" ")
        #for a in range(0, len(textlist)):
          #newword = textlist[a]
          #if newword == "and":
            #output = output + newword
          #elif newword.upper() == "SH":
            #output = output + "SH"
          #elif newword.upper() == "SLH":
            #output = output + "SLH"
          #elif newword.upper() == "LH":
            #output = output + "LH"
          #else:
            #word = textlist[a][0].upper() + textlist[a][1:].lower()
            #output = output + word
          #if a != int(len(textlist) - 1):
            #output = output + " "
        #if b != int(len(maintextlist) - 1):
          #output = output + "\n"
      #return output
    #else:
      #return ""
  #else:
    #return text
  
  return text

def ShowMessage(message, parent=None):
  
  output = wx.MessageDialog(parent, message, "Evette", wx.OK)
  output.ShowModal()

def GetTodaysWXDate():
  
  date = datetime.date.today()
  day = int(str(date)[8:])
  month = int(str(date)[5:7])
  month = month - 1
  year = int(str(date)[:4])
  
  wxdate = wx.DateTime()
  wxdate.Set(day, month, year)
  return wxdate

def GetDateFromWXDate(wxdate):
  
  day = str(wxdate.GetDay())
  if len(day) == 1:
    day = "0" + day
  month = wxdate.GetMonth()
  if month < 9:
    month = "0" + str(month + 1)
  elif month == 9:
    month = "10"
  else:
    month = str(month + 1)
  year = str(wxdate.GetYear())
  
  output = datetime.date(int(year), int(month), int(day))
  
  return output

def GetSQLDateFromWXDate(wxdate):
  
  #print "WXDate = " + str(wxdate)
  
  if str(wxdate) == "":
    
    sqldate = "0000-00-00"
    
  else:
    
    day = str(wxdate.GetDay())
    
    if len(day) < 2:
      
      day = "0" + day
    
    month = wxdate.GetMonth()
    
    if month < 9:
      
      month = "0" + str(month + 1)
      
    elif month == 9:
      
      month = "10"
      
    else:
      
      month = str(month + 1)
    
    year = str(wxdate.GetYear())
    
    sqldate = str(year + "-" + month + "-" + day)
    
  return sqldate

def GetDateFromSQLDate(sqldate):
  
  day = int(str(sqldate)[8:10])
  month = int(str(sqldate)[5:7])
  year = int(str(sqldate)[:4])
  
  date = datetime.date(year, month, day)
  return date

def GetSQLDateFromDate(date):
  
  sqldate = date.strftime("%Y-%m-%d")
  return sqldate

def GetWXDateFromDate(date):
  
  day = int(str(date)[8:10])
  month = int(str(date)[5:7])
  year = int(str(date)[:4])
  
  month = month - 1
  
  wxdate = wx.DateTime()
  wxdate.Set(day, month, year)
  return wxdate

def GetWXDateFromSQLDate(sqldate):
  
  date = GetDateFromSQLDate(sqldate)
  wxdate = GetWXDateFromDate(date)
  
  return wxdate

def RemoveLineBreaks(input):
  
  output = input.replace("\n", ", ")
  
  return output

def ValidateTime(time):
  
  success = False
  
  try:
    
    hour = int(time.split(":")[0])
    minute = int(time.split(":")[1])
    success = True
    
    if hour < 0 or hour > 23:
      
      success = False
    
    if minute < 0 or minute > 59:
      
      success = False
    
  except:
    
    LogException()
  
  return success

def GenerateDayPlan(localsettings, sqldate, step):
    
    openfromraw = localsettings.openfrom
    openfromtime = ( int(str(openfromraw)[:2]) * 60 ) + int(str(openfromraw)[3:5])
    
    opentoraw = localsettings.opento
    opentotime = ( int(str(opentoraw)[:2]) * 60 ) + int(str(opentoraw)[3:5])
    
    connection = db.GetConnection(localsettings)
    action = "SELECT * FROM staff WHERE Date = \"" + str(sqldate) + "\""
    results = db.SendSQL(action, connection)
    connection.close()
    
    vetnames = []
    vetdata = []
    colours = ("red", "#cbd202", "green", "blue")
    colourcount = 0
    for a in results:
      if vetnames.__contains__(a[1]) == False:
        vetnames.append(a[1])
      
      colour = colours[colourcount]
      vetdata.append((a[1], a[3], a[4], colour, a[5]))
    
    output = "<table><tr><td valign=bottom><u><font size=2>" + localsettings.t("timelabel") + "</font></u></td>"
    for a in vetnames:
      output = output + "<td valign=bottom><u><font size=2>" + a + "</font></u></td>"
    output = output + "<td valign=bottom><u><font size=2>" + localsettings.t("animalappointmentslabel") + "</font></u></td><td valign=bottom><u><font size=2>" + localsettings.t("operationslabel") + "</font></u></td><tr>"
    
    columncount = len(vetnames)
    
    rowcount =  ( opentotime - openfromtime ) / step
    rowcount = rowcount + 1
    
    lasttime = 0
    time = openfromtime
    
    for a in range(0, rowcount):
      
      timestring = GetTimeFromMinutes(time)
      
      output = output + "<tr height=100><td valign=top><font size=1>" + timestring + "<br></font></td>"
      
      noofvets = 0
      
      for b in range(0, columncount):
        
        colourcount = b
        while colourcount > len(colours) - 1:
          colourcount = colourcount - len(colours)
        colour = colours[colourcount]
        
        
        vetname = vetnames[b]
        
        success = False
        
        
        
        for c in range(0, len(vetdata)):
          
          openfromb = vetdata[c][1]
          openfrombint = ( int(openfromb[:2]) * 60 ) + int(openfromb[3:5])
          
          opentob = vetdata[c][2]
          opentobint = ( int(opentob[:2]) * 60 ) + int(opentob[3:5])
          
          vetnameb = vetdata[c][0]
          
          if vetdata[c][4] == 0:
            roleb = localsettings.t("consultinglabel").lower()
          else:
            roleb = localsettings.t("operatinglabel").lower()
          
          if time > openfrombint - 1 and time < opentobint + 1 and vetnameb == vetname:
            output = output + "<td bgcolor=" + colour + "><font size=1 color=white>" + roleb + "</font></td>"
            success = True
            noofvets = noofvets + 1
            break
        
        if success == False:
          output = output + "<td></td>"
      
      
      appointmenttime = GetTimeFromMinutes(time) + ":00"
      nextappointmenttime = GetTimeFromMinutes(time + step - 1) + ":59"
      connection = db.GetConnection(localsettings)
      action = "SELECT ID FROM appointment WHERE Date = \"" + sqldate + "\" AND Time BETWEEN \"" + appointmenttime + "\" AND \"" + nextappointmenttime + "\" AND Operation = 0"
      results = db.SendSQL(action, connection)
      connection.close()
      noofappointments = len(results)
      noofspaces = ( float(step) / 10 ) * float(noofvets)
      
      if float(noofappointments) > noofspaces:
        appointmentcolour = "red"
      else:
        appointmentcolour = "green"
      
      output = output + "<td align=center><font size=2 color=" + appointmentcolour + "><b>" + str(noofappointments) + "</b></font></td>"
      
      if a == 0:
        connection = db.GetConnection(localsettings)
        action = "SELECT ID FROM appointment WHERE Date = \"" + sqldate + "\" AND Operation = 1"
        results = db.SendSQL(action, connection)
        connection.close()
        
        noofappointments = len(results)
        output = output + "<td align=center><font size=2><b>" + str(noofappointments) + "</b></font></td></tr>"
      else:
        output = output + "<td></td></tr>"
      
      lasttime = time
      time = time + step
      
    
    output = output + "</table>"
    
    return output

def GetDayNameFromID(ID, localsettings):
  
  return localsettings.t("daynames",ID)

def FormatPrice(price):
  
  price = str(price)
  
  if price[0] != "-":
    if len(price) == 1:
      price = "0.0" + price
    elif len(price) == 2:
      price = "0." + price
    else:
      price = price[:-2] + "." + price[-2:]
  else:
    price = price[1:]
    
    if len(price) == 1:
      price = "0.0" + price
    elif len(price) == 2:
      price = "0." + price
    else:
      price = price[:-2] + "." + price[-2:]
    
    price = "-" + price
  
  return price



def GetAppointmentHtml(appointmentdata):
  
  localsettings = appointmentdata.animaldata.localsettings
  
  time = str(appointmentdata.time)
  
  if len(str(time)) == 7:
    
    time = "0" + time[:4]
    
  else:
    
    time = time[:5]
  
  animalname = appointmentdata.animaldata.name
  ownersurname = appointmentdata.clientdata.surname
  sex = appointmentdata.animaldata.sex
  neutered = appointmentdata.animaldata.neutered
  
  if neutered == 0:
    
    neutered = localsettings.t("entirelabel").lower()
    
  else:
    
    neutered = localsettings.t("neuteredlabel").lower()
  
  species = appointmentdata.animaldata.species
  breed = appointmentdata.animaldata.breed
  
  animalcomments = appointmentdata.animaldata.comments
  
  if animalcomments != "":
    
    animalcomments = "<font size=1 color=red><br>" + animalcomments.strip().replace("\n", "<br>") + "</font>"
    
  clientcomments = appointmentdata.clientdata.comments
  
  if clientcomments != "":
    
    clientcomments = "<font size=1 color=red><br>" + clientcomments.strip().replace("\n", "<br>").replace("£", "&pound;") + "</font>"
  
  reason = appointmentdata.reason
  dob = appointmentdata.animaldata.dob
  
  age = GetAgeFromDOB(dob, localsettings)
  
  title = appointmentdata.clientdata.title
  
  
  
  
  output = "<font size=1><b>" + time + "</font>&nbsp;<font color=blue size=1>(" + localsettings.t("vetlabel") + ": " + appointmentdata.vet + ")</font> - <font size=1><b>" + animalname + " " + ownersurname + "</b>"
  
  output = output + "<br></font><font color=red size=2><b>" + reason + "</b><br></font>"
  
  output = output + "<font size=1>" + GetSex(localsettings, sex) + " (" + neutered + ") " + breed.lower() + " " + species.lower() + ", " + age + "</font>" + animalcomments + "<font size=1><br>""" + localsettings.t("animalownerlabel") + """: </font><font color=blue size=1>""" + title + " " + ownersurname + "</font>" + clientcomments
  
  return output

def GetAppointmentDetailsHtml(localsettings, appointmentid, short=False):
  
  appointmentdata = appointmentmethods.AppointmentSettings(localsettings, False, appointmentid)
  
  date = appointmentdata.date
  date = FormatSQLDate(date, localsettings)
  
  time = FormatTime(appointmentdata.time)
  
  action = "SELECT * FROM receipt WHERE AppointmentID = " + str(appointmentdata.ID)
  results = db.SendSQL(action, localsettings.dbconnection)
  
  if short == False:
  
    receipthtml = "<td valign=top align=left width=40%><font size=1><u>" + localsettings.t("receiptlabel") + "</u><br></font><table width=100%>"
    
    receipttotal = 0
    
    for a in results:
      
      description = unicode(a[2], "utf8")
      price = a[3]
      
      receipttotal = receipttotal + price
      
      price = FormatPrice(price)
      
      receipthtml = receipthtml + "<tr><td align=left valign=top>" + description + "</td><td align=right valign=top nowrap>" + localsettings.t("currency") + price + "</td></tr>"
    
    receipttotal = FormatPrice(receipttotal)
    
    receipthtml = receipthtml + "<tr><td align=left valign=top><b>" + localsettings.t("totallabel") + ":</b></td><td align=right valign=top nowrap><b>" + localsettings.t("currency") + receipttotal + "</b></td></tr></table></td>"
    
  else:
    
    receipthtml = ""
  
  if GetDateFromSQLDate(appointmentdata.date) <= datetime.date.today():
    
    #Appointment is in the past
    
    if appointmentdata.arrived == 0 and appointmentdata.withvet == 0 and appointmentdata.done == 0:
      
      #DNA
      
      arrivaltimehtml = " (" + localsettings.t("dnalabel") + ")"
      
    elif appointmentdata.arrivaltime == None:
      
      #Unknown arrival time
      
      arrivaltimehtml = ""
      
    elif appointmentdata.time < appointmentdata.arrivaltime:
      
      #Arrived late
      
      arrivaltimehtml = " (" + localsettings.t("latelabel") + ")"
      
    else:
      
      arrivaltimehtml = " (" + localsettings.t("ontimelabel") + ")"
    
  else:
    
    #Appointment has not happened yet
    
    arrivaltimehtml = ""
  
  output =  "<table class='appointment' cellpadding=0 cellspacing=0><tr><td width=15% valign=top align=left><font color=blue><b>" + date + " " + time + "</b>" + arrivaltimehtml + "</font><br>" + localsettings.t("vetlabel") + ": <b>" + appointmentdata.vet + "</b></font><br /><font color=red>" + appointmentdata.reason + "</font></td><td width=50%><u>" + localsettings.t("problemlabel") + "</u><br />" + appointmentdata.problem + "<br /><br /><u>" + localsettings.t("noteslabel") + "</u><br />" + appointmentdata.notes + "<br /><br /><u>" + localsettings.t("planlabel") + "</u><br />" + appointmentdata.plan + "</td>" + receipthtml + "</tr></table>"
  
  return output

def GetAnimalDetailsHTML(animaldata):
  
  localsettings = animaldata.localsettings
  
  animalname = animaldata.name
  sex = animaldata.sex
  neutered = animaldata.neutered
  
  if neutered == 0:
    
    neutered = localsettings.t("entirelabel").lower()
    
  else:
    
    neutered = localsettings.t("neuteredlabel").lower()
  
  species = animaldata.species
  breed = animaldata.breed
  
  age = GetAgeFromDOB(animaldata.dob, animaldata.localsettings)
  
  animalcomments = animaldata.comments
  
  action = "SELECT ClientTitle, ClientForenames, ClientSurname, ClientAddress, ClientPostcode FROM client WHERE ID = " + str(animaldata.ownerid)
  results = db.SendSQL(action, animaldata.localsettings.dbconnection)
  
  ownername = ""
  
  if results[0][0] != "":
    
    ownername = ownername + unicode(results[0][0], "utf8") + " "
    
  if results[0][1] != "":
    
    ownername = ownername + unicode(results[0][1], "utf8") + " "
    
  if results[0][2] != "":
    
    ownername = ownername + unicode(results[0][2], "utf8")
  
  owneraddress = unicode(results[0][3], "utf8").replace("\n", "<br>")
  
  ownerpostcode = unicode(results[0][4], "utf8").upper()
  
  output = "<table align=center><tr><td valign=top><fieldset><legend>" + localsettings.t("animallabel") + "</legend><p>" + localsettings.t("namelabel") + ": <b>" + animalname + "</b><br>" + localsettings.t("animalsexlabel") + ": <b>" + GetSex(animaldata.localsettings, sex) + " (" + neutered + ")</b><br>" + localsettings.t("animalspecieslabel") + ": <b>" + species + "</b><br>" + localsettings.t("animalbreedlabel") + ": <b>" + breed + "</b><br>" + localsettings.t("animalcommentslabel") + ":<br><b>" + animalcomments + "</b></p></fieldset></td><td valign=top><fieldset><legend>" + localsettings.t("clientlabel") + "</legend><p><b>" + ownername + "<br>" + owneraddress + "<br>" + ownerpostcode + "</b></p></fieldset></td></tr></table>"
  
  return output

def FormatTime(time):
  
  timelist = str(time).split(":")[:2]
  
  if len(timelist[0]) == 1:
    hour = "0" + timelist[0]
  else:
    hour = timelist[0]
  
  time = hour + ":" + timelist[1]
  
  return time

def FormatSQLDate(sqldate, localsettings):
  
  day = str(sqldate)[8:10]
  month = str(sqldate)[5:7]
  year = str(sqldate)[:4]
  
  if localsettings.t("dateformat") == "DDMMYYYY":
    return day + "/" + month + "/" + year
  elif localsettings.t("dateformat") == "MMDDYYYY":
    return month + "/" + day + "/" + year
  else:
    return year + "/" + month + "/" + day

def FormatDate(date, localsettings):
  
  if localsettings.t("dateformat") == "DDMMYYYY":
    return date.strftime("%d/%m/%Y")
  elif localsettings.t("dateformat") == "MMDDYYYY":
    return date.strftime("%m/%d/%Y")
  else:
    return date.strftime("%Y/%m/%d")

def GetBalance(clientdata, localsettings):
  
  connection = db.GetConnection(localsettings)
  
  action = "SELECT receipt.Price FROM receipt WHERE receipt.Type = 4 AND receipt.TypeID = " + str(clientdata.ID)
  
  balanceresults1 = db.SendSQL(action, connection)
  
  action = "SELECT receipt.Price FROM appointment INNER JOIN receipt ON appointment.ID = receipt.AppointmentID WHERE appointment.OwnerID = " + str(clientdata.ID)
  
  balanceresults2 = db.SendSQL(action, connection)
  
  connection.close()
  
  balanceresults = balanceresults1 + balanceresults2
  
  balance = 0
  
  for a in balanceresults:
    
    balance = balance + a[0]
  
  return balance

def ConvertPriceToPennies(price, silent=False):

  price = str(price)
  if re.match("^-?\d*\d(\.\d\d)?$",price):
    dec = Decimal(price).quantize(Decimal('0.00')) #make it to two decimals
    return int(str(dec).replace('.','')) #convert it to pennies

  else:

    return False

def ValidateEntryString(string):
  
  #print "Input string = " + string
  
  string = string.replace("\'", "\\\'")
  
  #print "Output string = " + string
  
  return string

def NumbersOnly(ID):
  
  keycode = ID.GetKeyCode()
  
  if keycode == 9 or keycode == 8 or keycode == 127 or keycode == 316 or keycode == 317 or keycode == 318 or keycode == 319 or (keycode > 47 and keycode < 58):
    ID.Skip()

def FormatChangeLog(changelog, name, connection):
  
  localsettings = settings.settings(False)
  localsettings.GetSettings()
  
  output = name + "\n\n"
  
  count = 0
  
  for a in changelog.split("$$$"):
    
    date = a.split("%%%")[0]
    userid = a.split("%%%")[1]
    
    try:
      action = "SELECT Name FROM user WHERE ID = " + str(userid)
      results = db.SendSQL(action, connection)
      username = results[0][0]
    except:
      username = localsettings.t("userdeleted")
    
    output = output + date + " - " + username + "\n"
    
    count = count + 1
    
    if count == 10:
      break
  
  return output.strip()

def ShowChangeLog(name, changelog, connection):
  
  localsettings = settings.settings(False)
  localsettings.GetSettings()
  
  changelog = FormatChangeLog(changelog, name, connection)
  output = wx.MessageDialog(None, changelog, localsettings.t("changelog"), wx.OK)
  output.ShowModal()

def WriteToTempFolder(filename, output):
    
    if filename.__contains__("."):
      
      fileextension = filename.split(".")[-1]
      
    else:
      
      fileextension = ""
    
    pathtotempfolder = GetHome() + "/.evette/temp"
    
    count = 0
    
    while os.path.isfile(pathtotempfolder + "/" + filename[:(len(fileextension) * -1)] + str(count) + fileextension) == True:
      
      count = count + 1
    
    filename = filename[:(len(fileextension) * -1)] + str(count) + fileextension
    
    out = open(pathtotempfolder + "/" + filename, "wb")
    out.write(output)
    out.close()
    
    return pathtotempfolder + "/" + filename

def OpenMedia(mediaid, formname=False):
  
  if mediaid != False:
    
    localsettings = settings.settings(False)
    localsettings.GetSettings()
    
    connection = db.GetConnection(localsettings)
    action = "SELECT FileName, Content FROM media WHERE ID = " + str(mediaid)
    results = db.SendSQL(action, connection)
    connection.close()
    
    filename = results[0][0]
    content = results[0][1]
    
    output = base64.decodestring(content)
    
    if filename.__contains__("."):
      
      fileextension = filename.split(".")[-1]
      
    else:
      
      fileextension = ""
    
    targetfile = WriteToTempFolder(filename, output)
    
    out = open(targetfile, "wb")
    out.write(output)
    out.close()
    
  else:
    
    if formname.__contains__("."):
      
      fileextension = formname.split(".")[-1]
      
    else:
      
      fileextension = ""
    
    targetfile = pathtotempfolder = GetHome() + "/.evette/temp/" + formname
  
  pathtofiletypesfile = GetHome() + "/.evette/filetypes.conf"
  
  if os.path.isfile(pathtofiletypesfile) == True:
    
    inp = open(pathtofiletypesfile, "r")
    fileassociations = []
    for a in inp.readlines():
      fileassociations.append(a.strip().split("$$$"))
    inp.close()
    
    program = ""
    
    for a in fileassociations:
      
      if a[0] == fileextension:
        
        program = a[1]
    
    if program == "":
      
      localsettings = settings.settings(False)
      localsettings.GetSettings()
      
      wx.CallAfter(ShowMessage, fileextension + " - " + localsettings.t("noprogramassociatedmessage") + " " + localsettings.t("readfileassociationhelpmessage"))
      
    else:
      
      if str(sys.platform)[:3] == "win":
        
        command = "\"" + program + "\" \"" + targetfile + "\""
        command = command.replace("/", "\\")
        os.system("\"" + command + "\"")
        
      else:
        
        command = "\"" + program + "\" \"" + targetfile + "\""
        os.system(command)
  
  else:
    
    localsettings = settings.settings(False)
    localsettings.GetSettings()
    
    wx.CallAfter(ShowMessage, localsettings.t("noprogramassociatedmessage"))

def CorrectNullString(string):
  
  if str(string) == "None":
    
    string = ""
  
  return string


def LogException():
  etype, value, tb = sys.exc_info()
  logging.error(''.join(traceback.format_exception(etype, value, tb)))
