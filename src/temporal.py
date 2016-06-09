# -*- coding: utf-8 -*-


PROJECTFILES = {}
PROJECTFILES["scriptFile"] = False
PROJECTFILES["folder"] = False
PROJECTFILES["mainPath"] = False

FOLDER_PATH = False
FILE_PATH = False
CONFIG_DATA = False
SCRIPT_PATH = False

def reset():
	FOLDER_PATH = False
	FILE_PATH = False
	CONFIG_DATA = False
	SCRIPT_PATH = False
	PROJECTFILES = {}
	PROJECTFILES["scriptFile"] = False
	PROJECTFILES["folder"] = False
	PROJECTFILES["mainPath"] = False
