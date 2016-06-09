# -*- coding: utf-8 -*-
from tools.files import Readfile_string
from tools.dictionaries import str2dic, file2dic
from Classes import LineStyle, ArrowStyle

from tools.files import getFolders
import json
from Gplot import gnuplotVersion


def getStyles():
	'''
	This method search in the folder 'styles/' for all the styles available that in their inside have the manifest file.
	This file contains the imformation of the style
	'''
	Styles = []
	folders = getFolders('styles/')
	for folder in folders:
		manifest = readStyleManifest(folder)

		if manifest:
			styleInfo = str2dic(manifest)
			version = styleInfo['version']
			# the version of Gnuplot should be at least the same of the one for what the tempalte was made
			gp_ver = gnuplotVersion()
			if version > gp_ver:
				warning = "Warning: Style [%s] is ment for version [%s] and you have version: [%s]. Cant load Style." % (styleInfo['name'], str(version), str(gp_ver))
				print warning
				continue
			Styles.append([folder, styleInfo])
	return Styles


def manifestInfo(manifest, entry):
	manifest = json.loads(manifest)
	if entry in manifest.keys():
		return manifest[entry]


def readStyleManifest(path):
	manifest = Readfile_string(path + '/manifest.txt')
	if manifest:
		return manifest


def openStyle(path='styles/default/'):
	style = {}
	if path[-1] is not '/':
		path = path + '/'

	style['style_lines'] = file2dic(path + 'lines.sty')
	# this need to fill the vectors type to insert
	style['style_vectors'] = file2dic(path + 'vectors.sty')
	# this need to fill the arrow type to insert
	style['style_arrows'] = file2dic(path + 'arrows.sty')
	# this need to fill the arrow type to insert
	style['lines_raw'] = file2dic(path + 'lines_raw.sty')
	style['commands'] = file2dic(path + 'commands.sty')
	return style


def generateTemplate(style):
	template = ''

	lines = style['style_lines']
	vectors = style['style_vectors']
	arrows = style['style_arrows']
	lines_plot = style['lines_raw']
	# commands = style['commands']

	template += '# Lines Style definition\n'
	for line in lines:
		LS = LineStyle(line)
		template += LS.getStyle() + '\n'

	template += '# Vector definitions\n'
	for vector in vectors:
		VT = ArrowStyle(vector)
		template += VT.getStyle() + '\n'

	template += '# Arrow definitions\n'
	for arrow in arrows:
		AR = ArrowStyle(arrow)
		template += AR.getStyle() + '\n'

	template += '# Plot lines definitions\n'
	for lines_plt in lines_plot:
		LN = ArrowStyle(lines_plt)
		template += LN.getStyle() + '\n'

	return template
