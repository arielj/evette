#!/usr/bin/python

import MySQLdb
import cgi

def GetConnection():
	
	dbip = "127.0.0.1"
	dbuser = "root"
	dbpass = ""
	dbname = "evette"
	
	if dbpass == "" or dbpass == "None" or dbpass == "False":
		connection = MySQLdb.connect(host=dbip, user=dbuser, db=dbname)
	else:
		connection = MySQLdb.connect(host=dbip, user=dbuser, passwd=dbpass, db=dbname)
	
	return connection

def SendSQL(action, connection):
	
	cursor = connection.cursor()
	cursor.execute(action)
	output = cursor.fetchall()
	cursor.close()
	connection.commit()
	
	return output

def GenerateAppointmentHTML(appointmentdata):
	
	animalid = appointmentdata[1]
	ownerid = appointmentdata[2]
	date = appointmentdata[3]
	time = appointmentdata[4]
	reason = unicode(appointmentdata[5], "utf8")
	problem = unicode(appointmentdata[8], "utf8")
	notes = unicode(appointmentdata[9], "utf8")
	plan = unicode(appointmentdata[10], "utf8")
	operation = appointmentdata[12]
	vet = unicode(appointmentdata[13], "utf8")
	
	return "<fieldset><legend><font color=blue size=1><b>" + str(date) + " " + str(time) + "</b></font></legend><table width=100% cellpadding=0 cellspacing=0><tr><td valign=top align=left><font size=1>Vet: <b>" + vet + "</b><br></font><font color=red size=1>" + reason + "</font><br><br><font size=1><u>Problem</u><br>" + problem + "<br><u>Notes</u><br>" + notes + "<br><u>Plan</u><br>" + plan + "</font></td></tr></table></fieldset>"

print "Content-type: text/html\n\n<html><head><title>Evette Record</title><link href=/style.css rel=stylesheet></head><body>"

forminfo = cgi.FieldStorage()
asmref = forminfo["asmref"].value

connection = GetConnection()

action = "SELECT animal.Name, animal.Sex, animal.Neutered, animal.Species, animal.Breed, animal.Colour, animal.DOB, animal.Comments, animal.ChipNo, animal.IsDeceased, animal.DeceasedDate, animal.CauseOfDeath, CONCAT(client.ClientTitle, \" \", client.ClientForenames, \" \", client.ClientSurname) FROM animal INNER JOIN client ON animal.OwnerID = client.ID WHERE animal.ASMRef = \"" + asmref + "\""

animaldata = SendSQL(action, connection)

owner = animaldata[0][12]
name = animaldata[0][0]

sex = animaldata[0][1]
neutered = animaldata[0][2]

if neutered == 0:
	
	sex = sex + " (entire)"
	
else:
	
	sex = sex + " (neutered)"


species = animaldata[0][3]
breed = animaldata[0][4]
colour = animaldata[0][5]
dob = animaldata[0][6]
comments = animaldata[0][7]
chipno = animaldata[0][8]
deceased = animaldata[0][9]
deceaseddate = animaldata[0][10]
causeofdeath = animaldata[0][11]

output = """
<h1 align=center><b>""" + asmref + " " + name + """</b></h1>

<table width=100%>
	<tr>
		<td width=300>
		<fieldset>
			<table cellspacing=10 cellpadding=0>
				<tr>
					<td>
						Owner:
					</td>
					<td>
						""" + owner + """
					</td>
				</tr>
				<tr>
					<td>
						Species:
					</td>
					<td>
						""" + species + """
					</td>
				</tr>
				<tr>
					<td>
						Sex:
					</td>
					<td>
						""" + sex + """
					</td>
				</tr>
				<tr>
					<td>
						breed:
					</td>
					<td>
						""" + breed + """
					</td>
				</tr>
				<tr>
					<td>
						DOB:
					</td>
					<td>
						""" + dob + """
					</td>
				</tr>
				<tr>
					<td>
						Chip No:
					</td>
					<td>
						""" + chipno + """
					</td>
				</tr>
				<tr>
					<td>
						Comments:
					</td>
					<td>
						""" + comments.replace("\n", "<br>") + """
					</td>
				</tr>
			</table>
			</fieldset>
		</td>
		<td width=50>
		</td>
		<td>
			<h2 align=center><b>Appointment History</b></h2>
"""

action = "SELECT appointment.* FROM appointment INNER JOIN animal ON animal.ID = appointment.AnimalID WHERE animal.ASMRef = \"" + asmref + "\" ORDER BY appointment.Date"
results = SendSQL(action, connection)

for a in results:
	
	output = output + GenerateAppointmentHTML(a) + "<br>"

connection.close()

print output + "</td></tr></table>"


print "</body></html>"