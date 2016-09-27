from os.path import expanduser, exists
from os import makedirs
from os import errno
from tools.paths import makePath
import subprocess

HOME = expanduser("~")
USER_FOLDER = makePath([HOME, '.guisse'])

USER_STYLES = 'styles'
USER_EXAMPLES = 'examples'
USER_TMP = 'tmp'
USER_STRUCTURE = [USER_STYLES, USER_EXAMPLES, USER_TMP]

REQUIREMENTS = ['gnuplot -V']  # , 'xfig -h', 'pstoedit -help' ]

def checkDirs():
	if not exists(USER_FOLDER):
		makedirs(USER_FOLDER)

	for folder in USER_STRUCTURE:
		target = makePath([USER_FOLDER, folder])
		if not exists(target):
			makedirs(target)

def checkRequirements():
	for program in REQUIREMENTS:
		try:
			subprocess.call([program])
		except OSError as e:
			if e.errno == errno.ENOENT:
				pass
			else:
				# Something else went wrong while trying to run `wget`
				print '"' + program.split(' ')[0] + '" is not installed. Can not proceed'
				exit()
