# -*- coding: utf-8 -*-
import subprocess
import re


def gnuplotVersion():
	ver = gplot = 0
	try:
		gplot = subprocess.check_output(['gnuplot', '-V']).split(' ')
		if len(gplot):
			gplot = gplot[1].strip()
	except:
		print "You might not have gnuplot installed..."
	rgex = "^(\d.\d)"
	if gplot:
		ver = re.findall(rgex, gplot)[0]
	return float(ver)
