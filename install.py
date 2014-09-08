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
import recursivemethods

if str(sys.platform)[:3] == "win":
	
	home = os.environ["USERPROFILE"]
	programfilesfolder = os.environ["PROGRAMFILES"]
	programfolder = programfilesfolder + "\evette"

	batchfile = "CD \"" + programfolder + "\"\n\nlaunch.exe\""
        
        if os.path.isdir("C:/Documents and Settings/All Users/Start Menu/Programs/Evette") == False:
            os.mkdir("C:/Documents and Settings/All Users/Start Menu/Programs/Evette")
        
	
	out = open("C:/Documents and Settings/All Users/Start Menu/Programs/Evette/Evette.bat", "w")
	out.write(batchfile)
	out.close()

	sourcefolder = os.path.curdir + "/winxp"
else:
	
	home = os.environ["HOME"]
	programfolder = "/usr/local/lib/evette"
	
	launchscript = "#!/bin/bash\n\ncd " + programfolder + "\npython launch.py"
	
	out = open("/usr/local/bin/evette", "w")
	out.write(launchscript)
	out.close()
	
	os.chmod("/usr/local/bin/evette", 111)

	sourcefolder = os.path.curdir
	
if os.path.isdir(programfolder):
	recursivemethods.deletefolder(programfolder)
os.mkdir(programfolder)

recursivemethods.CopyFolderContents(sourcefolder, programfolder)

os.link
