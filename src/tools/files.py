# -*- coding: UTF-8 -*-
import os
from django.utils.encoding import smart_str  # , smart_unicode

def writestring2File(file_, string):
	if os.path.isfile(file_) and not os.access(file_, os.R_OK):
		print "\t\tError: at saving"
		return False
	try:
		FO = open(file_, "w")
		FO.write(string)
		FO.close()
		print "Donde: Saved File: " + file_
	except IOError:
		print "Error: File not saved: " + file_


def Readfile(file_):
	db = False
	if not os.path.isfile(file_):
		print "Error: File not found: " + file_
		return False
	try:
		DB = open(file_, "r")
		db = DB.readlines()
	except IOError:
		print "Error: File does not appear to exist: " + file_
	return db


def Readfile_string(file_):
	file_str = ''
	lines = Readfile(file_)
	if not lines:
		return False
	for line in lines:
		file_str += smart_str(line.strip()) + '\n'
	return smart_str(file_str)


def getFolders(pathbase):
	fodlers=[]
	for dirpath, dirnames, filenames in os.walk(pathbase):
		dirnames = sorted(dirnames)
		for i in range(0, len(dirnames)):
			folder = dirnames[i]
			folder = os.path.join(dirpath, folder).strip()
			fodlers.append(folder)
	return fodlers
