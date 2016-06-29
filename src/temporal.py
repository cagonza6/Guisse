# -*- coding: utf-8 -*-


PROJECTFILES = {}
PROJECTFILES["scriptFile"] = False
PROJECTFILES["folder"] = False
PROJECTFILES["mainPath"] = False

FOLDER_PATH = False
FILE_PATH = False
CONFIG_DATA = False
SCRIPT_PATH = False

TEMP_FOLDER = '/tmp/script0.gnu'

def reset():
	FOLDER_PATH = False
	FILE_PATH = False
	CONFIG_DATA = False
	SCRIPT_PATH = False
	PROJECTFILES = {}
	PROJECTFILES["scriptFile"] = False
	PROJECTFILES["folder"] = False
	PROJECTFILES["mainPath"] = False
