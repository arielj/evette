#!/usr/bin/python

import os

listoffiles = os.listdir("./")

for a in listoffiles:
	
	
	
	
	if a[-5:] == ".html":
		print "Altering " + str(a)
		inp = open(a, "r")
		output = ""
		
		filecontents = ""
		
		for b in inp.readlines():
			
			filecontents = filecontents + b
		
		inp.close()
		
		filecontentslist = filecontents.split("<body>")
		filecontents = filecontentslist[1]
		
		filecontentslist = filecontents.split("</html>")
		filecontents = filecontentslist[0]
		
		
		output = filecontents.replace("</body>", "<h3 align=center><a href=makepage.py?menu=homecode.dat&targetpage=help.dat>Back to help index</a></h3>")
		
		output = output.replace("<img src=html/images", "<img src=/imagesfolder/helpimages")
		
		output = output.replace("<img src=../icons", "<img src=/imagesfolder/iconimages")
		
		output = output.replace("<img src=images", "<img src=/imagesfolder/helpimages")
		
		if os.path.isdir("../websitehelp") == False:
			os.mkdir("../websitehelp")
		
		
		newfilename = "../websitehelp/" + a[:-5] + ".dat"
		
		#print "new filename = " + newfilename
		
		out = open(newfilename, "w")
		
		out.write(output)
		out.close()
		
	else:
		print str(a) + " is not an html file - skipping"

print "Done"