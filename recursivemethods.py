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

def deletefolder(sourcefolder):
	
	folderstodelete = []
	totalfolders = []
	filestodelete = []
	
	sourcecontents = os.listdir(sourcefolder)
	
	for a in sourcecontents:
		
		if os.path.isdir(sourcefolder + "/" + a) == True:
			
			folderstodelete.append(a)
			totalfolders.append(a)
		
		else:
			
			filestodelete.append(a)
	
	while len(folderstodelete) > 0:
		
		for a in folderstodelete:
			
			foldercontents = os.listdir(sourcefolder + "/" + a)
			
			for b in foldercontents:
				
				if os.path.isdir(sourcefolder + "/" + a + "/" + b):
					
					folderstodelete.append(a + "/" + b)
					totalfolders.append(a + "/" + b)
				
				else:
					
					filestodelete.append(a + "/" + b)
			
			folderstodelete.remove(a)
	
	for a in filestodelete:
		
		os.remove(sourcefolder + "/" + a)
	
	reversedtotalfolders = []
	
	while len(totalfolders) > 0:
		
		reversedtotalfolders.append(totalfolders[-1])
		totalfolders.pop()
	
	totalfolders = reversedtotalfolders
	
	for a in totalfolders:
		
		os.rmdir(sourcefolder + "/" + a)
	
	os.rmdir(sourcefolder)

def CopyFolderContents(sourcefolder, destinationfolder):
	
	#Note: the CONTENTS of sourcefolder are copied INTO destination folder
	
	folderstocopy = []
	totalfolders = []
	filestocopy = []
	
	sourcecontents = os.listdir(sourcefolder)
	
	for a in sourcecontents:
		
		if os.path.isdir(sourcefolder + "/" + a) == True:
			
			folderstocopy.append(a)
			totalfolders.append(a)
		
		else:
			
			filestocopy.append(a)
	
	while len(folderstocopy) > 0:
		
		for a in folderstocopy:
			
			foldercontents = os.listdir(sourcefolder + "/" + a)
			
			for b in foldercontents:
				
				if os.path.isdir(sourcefolder + "/" + a + "/" + b):
					
					folderstocopy.append(a + "/" + b)
					totalfolders.append(a + "/" + b)
				
				else:
					
					filestocopy.append(a + "/" + b)
			
			folderstocopy.remove(a)
	
	#List of files to be copied obtained - writing new files
	
	for a in totalfolders:
		
		if os.path.isdir(destinationfolder + "/" + a) == False:
			
			os.mkdir(destinationfolder + "/" + a)
	
	for a in filestocopy:
		
		inp = open(sourcefolder + "/" + a, "rb")
		filecontents = inp.readlines()
		inp.close()
		
		out = open(destinationfolder + "/" + a, "wb")
		for b in filecontents:
			out.write(b)
		out.close()

def EmptyFolder(destinationfolder):
	
	folders = []
	totalfolders = []
	files = []
	
	rootcontents = os.listdir(destinationfolder)
	
	for a in rootcontents:
		
		if os.path.isdir(destinationfolder + "/" + a) == True:
			
			folders.append(a)
			totalfolders.append(a)
		
		else:
			
			files.append(a)
	
	while len(folders) > 0:
		
		for a in folders:
			
			foldercontents = os.listdir(destinationfolder + "/" + a)
			
			for b in foldercontents:
				
				if os.path.isdir(destinationfolder + "/" + a + "/" + b):
					
					folders.append(a + "/" + b)
					totalfolders.append(a + "/" + b)
				
				else:
					
					files.append(a + "/" + b)
			
			folders.remove(a)
	
	#Deleting files first
	
	for a in files:
		
		os.remove(destinationfolder + "/" + a)
	
	#Now deleting empty folders
	
	newtotalfolders = []
	
	while len(totalfolders) > 0:
		
		newtotalfolders.append(totalfolders.pop())
	
	totalfolders = newtotalfolders
	
	for a in totalfolders:
		
		os.rmdir(destinationfolder + "/" + a)