# -*- coding: utf-8 -*-
import tempfile
import checks
from tools.paths import makePath

PROJECTFILES = {}
PROJECTFILES["scriptFile"] = False
PROJECTFILES["folder"] = False
PROJECTFILES["mainPath"] = False

FOLDER_PATH = False
FILE_PATH = False
CONFIG_DATA = False
SCRIPT_PATH = False

TEMP_FOLDER = tempfile.gettempdir()
TEMP_SCRIPT = makePath([TEMP_FOLDER, 'script0.gnu'])
TEMP_EPS = makePath([TEMP_FOLDER, 'temp.eps'])
USER_LAST_FILES = makePath([checks.USER_FOLDER, checks.USER_TMP, 'lastpaths.txt'])

