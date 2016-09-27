# -*- coding: utf-8 -*-
import subprocess
import shlex
import re

from PyQt4 import QtGui, QtCore
from django.utils.encoding import smart_str  # , smart_unicode
from tools.files import Readfile_string, writestring2File, Readfile
from tools.dictionaries import dic2file
from tools.Fig import fig2latexFriendly
from ui.centralPanel import Ui_CentralPanel
from treeFunctions import TreeWiews
from Styles import openStyle, getStyles, generateTemplate
import temporal
from Small_Editor import GNUplotHighlighter
from Classes import ArrowStyle
from Gplot import gnuplotVersion
import tools.paths as Path

GPVERSION = gnuplotVersion()
CURRENT_LINE_HL = QtGui.QColor(200, 205, 0, 70)


class CentralPanel(QtGui.QWidget, Ui_CentralPanel, TreeWiews):
	def __init__(self, parent=None):
		super(CentralPanel, self).__init__()
		self.setupUi(self)
		# Actions
		self.connect(self.btn_reloadScript, QtCore.SIGNAL("clicked()"), self.reLoadScript)
		self.connect(self.btn_reloadStyle, QtCore.SIGNAL("clicked()"), self.styleChanged)
		self.connect(self.btn_show, QtCore.SIGNAL("clicked()"), self.plotScript)

		# Butons
		self.connect(self.btn_Eps, QtCore.SIGNAL("clicked()"), self.send2eps)
		self.connect(self.btn_fig, QtCore.SIGNAL("clicked()"), self.send2fig)
		self.connect(self.comboStyles, QtCore.SIGNAL("currentIndexChanged(int)"), self.styleChanged)
		self.connect(self.btnNewRep, QtCore.SIGNAL("clicked()"), self.newReplacement)

		# insert buttons
		self.connect(self.cmb_Element, QtCore.SIGNAL("currentIndexChanged(int)"), self.GetElement)
		self.connect(self.cmb_type, QtCore.SIGNAL("currentIndexChanged(int)"), self.GetType)
		self.connect(self.btn_insert, QtCore.SIGNAL("clicked()"), self.insert_code)
		self.connect(self.btnClean, QtCore.SIGNAL("clicked()"), self.cleanReplacements)

		self.customSizes = [
			['5x5', [5, 5]],
			['12x8', [12, 8]]
		]
		# default size filling
		for size in self.customSizes:
			self.combosize.addItem(*size)

		self.ProjectData = False
		self.fileFolder = False

		self.template = ''
		self.loadStyles()
		self.getstyle()

		self.extra_selections = []
		# Line Numbers ...
		self.numbers.construct(self.field_script)
		# Syntax Highlighter ...
		self.highlighter = GNUplotHighlighter(self.field_script.document())
		# Event Filter ...
		self.installEventFilter(self)
		self.left_selected_bracket = QtGui.QTextEdit.ExtraSelection()
		self.right_selected_bracket = QtGui.QTextEdit.ExtraSelection()

		# replacements tree
		self.repSource = []
		self.repLabel = []
		self.replacements = []

		self.proxyModelReplacements = QtGui.QSortFilterProxyModel(self)
		self.resetAll()

	def resetAll(self):
		self.setReplacements()
		self.cleanReplacements()

	# Replacements
	'''
	These set of methods control the behaviour of the replacements for
	the LaTeX friendly outputs.
	A replacements has two parts:
		* original string and
		* and its replacement.
	The idea is to be used this option as latex friendly commands
	that will be replaced in the final xfig.
	'''
	def newReplacement(self):
		'''
		Adds an empty line to write the replacements pair.
		'''
		self.addElement(self.model, [' ', ' '])

	def cleanReplacements(self):
		'''
		Removes the empty lines from the existing replacements
		'''
		self.setReplacements(self.getReplacements())

	def getReplacements(self):
		'''
		Return an array with the replacements as its elements in the
		form [[original1, replacement1], [original1, replacement2],...]
		'''
		pairs = []
		for i in range(0, self.model.rowCount()):
			pair = [
				self.model.data(self.model.index(i, 0)),
				self.model.data(self.model.index(i, 1))
			]
			if pair[0] and pair[1] and str(pair[0]).strip() and str(pair[1]).strip():
				pairs.append([str(pair[0]), str(pair[1])])
		return pairs

	def setReplacements(self, replacements=['']):
		'''
		Sets the given array with all the elements to the replacement
		tree.
		@input: array of replacements [[original1, replacement1], [original1, replacement2],...]
		'''
		self.setTreeDecorations(self.treeReplacements, True)
		self.modelReplacements = self.createElementModel(replacements, [0, 1])
		self.setHeaders(self.modelReplacements, ['Original', 'Replacement'])
		self.setColumnWidth(self.treeReplacements, [100, 100])
		self.proxyModelReplacements.setSourceModel(self.modelReplacements)
		self.treeReplacements.setModel(self.proxyModelReplacements)

	# Elements: this are the definitions from the template
	def GetElement(self):
		'''
		Check what kind of element is selected and fills te item combo with the
		posibilities
		'''
		self.cmb_type.clear()
		types = self.cmb_Element.itemData(self.cmb_Element.currentIndex())
		if not types:
			return
		for i in range(0, len(types)):
			type_ = types[i]
			self.cmb_type.addItem(*type_)

	def GetType(self):
		'''
		Gets the type of element and fills the code in the code box
		'''
		code = str(self.cmb_type.itemData(self.cmb_type.currentIndex()))
		self.codeGen.setPlainText(code)

	def paintEvent(self, event):
		'''
		highlights the key words
		'''
		highlighted_line = QtGui.QTextEdit.ExtraSelection()
		highlighted_line.format.setBackground(CURRENT_LINE_HL)
		highlighted_line.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
		highlighted_line.cursor = self.field_script.textCursor()
		highlighted_line.cursor.clearSelection()
		self.field_script.setExtraSelections([highlighted_line, self.left_selected_bracket, self.right_selected_bracket])

	# File events
	def loadScript(self, path):
		'''
		Open the script located in the given path and
		fills the script field
		'''
		script = Readfile_string(path)
		if script:
			self.field_script.setPlainText(smart_str(script))
		# here the labels are searched in order to make the replacements
		self.stringReplace(script)

	def saveProject(self):
		'''
		saves the script and the config file
		'''
		projectData = self.getProjectParams()

		if False in [projectData, temporal.PROJECTFILES['folder'], temporal.PROJECTFILES['mainPath']]:
			print "Error saving file"
			return

		dic2file(self.getProjectParams(), temporal.PROJECTFILES['mainPath'])
		self.saveScript()

	def saveScript(self):
		# this method saves the script, but not the entire project
		script = self.getScript().strip()
		if not temporal.PROJECTFILES['scriptFile'] or not temporal.PROJECTFILES['scriptPath']:
			print "Error saving s cript: saveScript"
			return
		writestring2File(temporal.PROJECTFILES['scriptPath'], script)

	def openFile(self, configData):
		self.resetAll()
		if not configData:
			print "TODO: clean window!!"
			return False

		self.fillFields(configData)
		temporal.PROJECTFILES['scriptFile'] = configData['scriptFile']
		temporal.PROJECTFILES['scriptPath'] = Path.folderPlusFile(temporal.PROJECTFILES['folder'], temporal.PROJECTFILES['scriptFile'])
		self.loadScript(temporal.PROJECTFILES['scriptPath'])

	def reLoadScript(self):
		if 'scriptPath' in temporal.PROJECTFILES.keys() and temporal.PROJECTFILES['scriptPath']:
			self.loadScript(temporal.PROJECTFILES['scriptPath'])

	# Project Parameters
	def getFigSize(self):
		'''
		gets the plot sise for the figure out of the ui
		'''
		size = [12, 12]
		if self.radioSizeCombo.isChecked():
			size = self.combosize.itemData(self.combosize.currentIndex())
		else:
			w = float(self.figWidth.value())
			h = float(self.figHeight.value())
			size = [w, h]
		return size

	def getXfigCompatible(self):
		# Reads if the xfig latex compatible option is selected
		return self.latexLabel.isChecked()

	def getXfigAutoShow(self):
		# Reads if the xfig latex compatible option is selected
		return self.checkAutoshow.isChecked()

	def getProjectParams(self):
		'''
		This method return the data from the project, that
		is shown in the ui and does not include the script.
		the filename is saven in the temporals in ram
		'''
		projectData = {}
		projectData['template'] = str(self.comboStyles.itemData(self.comboStyles.currentIndex()))
		projectData['FIGoutput'] = str(self.fieldOutputName.text())
		projectData['size'] = self.getFigSize()
		projectData['replacements'] = self.getReplacements()
		self.cleanReplacements()
		projectData['xfig'] = self.getXfigCompatible()
		projectData['autoplot'] = self.getXfigAutoShow()

		return projectData

	def getScript(self):
		return smart_str(self.field_script.toPlainText())

	# Interface: fill functions
	def fillFields(self, configData):
		'''
		Fills all the required parameters from the project
		it includes the template
		'''
		self.fieldOutputName.setText(configData['FIGoutput'])
		self.field_path.setText(configData['scriptFile'])
		self.latexLabel.setChecked(configData['xfig'])

		self.setSize(configData['size'])

		# replacements
		replacements = configData['replacements']
		self.setReplacements(replacements)

		if replacements:
			for replace in replacements:
				if len(replace) < 2:
					continue
				self.repSource.append(replace[0])
				self.repLabel.append(replace[1])
		# style
		indexStyle = self.comboStyles.findData(configData['template'])
		self.comboStyles.setCurrentIndex(indexStyle)

	def setSize(self, size):
		indexSize = False
		for size_ in self.customSizes:
			if size == size_[1]:
				indexSize = self.combosize.findData(size)
				self.combosize.setCurrentIndex(indexSize)
				break
		if indexSize:
			self.radioSizeCombo.setChecked(True)
		else:
			self.radiocustom.setChecked(True)
			self.figWidth.setValue(size[0])
			self.figHeight.setValue(size[1])
		return

	def styleChanged(self):
		folder = str(self.comboStyles.itemData(self.comboStyles.currentIndex()))
		print "changed Style ", folder
		style = openStyle(folder)
		if not style:
			print "Style not found"
		self.template = generateTemplate(style)
		self.loadTemplate(style)

	def setType_(self, items):
		dataPair = []
		if not items:
			return
		for i in range(0, len(items)):
			item = items[i]
			name = '-'
			name = item['comment'].strip('#').strip()
			Code = ArrowStyle(item)
			code = Code.getInsert()
			pair = [name, code]
			dataPair.append(pair)
		return dataPair

	def setcommands(self, commands):
		dataPair = []
		for i in range(0, len(commands)):
			command = commands[i]
			name = command['name'].strip()
			codes = command['code']
			code_str = '# ' + command['description'] + '\n'
			for code in codes:
				code_str += code.strip() + '\n'
			code = code_str.strip()
			pair = [name, code]
			dataPair.append(pair)
		return dataPair

	# Plot related methods
	def insert_code(self):
		new = self.field_script.toPlainText() + '\n' + str(self.cmb_type.itemData(self.cmb_type.currentIndex()))
		self.field_script.setPlainText(new)

	def stringReplace(self, script=False):
		'''
		It is suposed to search for all the strings that can be replaced, it is not jet correctly implemented
		'''
		if not script:
			script = self.getScript().strip().split('\n')
		else:
			script = script.split('\n')
		r1 = r"\'(.+?)\'"
		r2 = r'\"(.+?)\"'

		for line in script:
			matched = re.findall(r1, line) + re.findall(r2, line)
			if matched:
				for match in matched:
					if match not in (self.repSource):
						self.repSource.append(str(match))

	def cleanScript(self):
		txt_ = self.getScript()
		script = txt_.split('\n')
		cleaned = []
		for i in range(0, len(script)):
			line = script[i].strip()
			if not len(line):
				continue
			if line[0] == '#':
				continue
			if 'set ' in line and 'terminal ' in line:
				continue
			if 'set ' in line and 'output ' in line:
				continue
			cleaned.append(line)
		str_ = '\n'.join(cleaned)
		return smart_str('\n' + str_ + '\n')

	def plotScript(self):
		script = 'reset \n'
		if temporal.PROJECTFILES:
			if isinstance(temporal.PROJECTFILES['folder'], str):
				script += "cd \"" + temporal.PROJECTFILES['folder'] + "\"\n"
		if GPVERSION < 5.0:
			script += 'set termoption dash \n'
		script += self.gettemplate() + '\n'
		script += self.cleanScript() + '\n'

		writestring2File(temporal.TEMP_SCRIPT, script)
		self.GP_(temporal.TEMP_SCRIPT, persist=True)

	def send2eps(self):
		self.stringReplace()
		self.send2fig(eps=True)

	def send2fig(self, eps=False):
		script = 'reset \n'
		size = self.getFigSize()
		width = str(size[0])
		height = str(size[1])
		if temporal.PROJECTFILES:
			if isinstance(temporal.PROJECTFILES['folder'], str):
				script += "cd \"" + temporal.PROJECTFILES['folder'] + "\"\n"
		script += 'set terminal postscript portrait enhanced color size ' + width + 'cm,' + height + 'cm "Times-Roman" 11 \n'

		if not temporal.PROJECTFILES:
			print "no target file"
			return

		if eps:
			epsOutput = '\"' + Path.folderPlusFile(temporal.PROJECTFILES['folder'], self.getProjectParams()['FIGoutput'] + '.eps') + '\"'
		else:
			epsOutput = '\"' + Path.str2path(temporal.TEMP_EPS) + '\"'

		script += 'set output ' + epsOutput + ' \n'
		script += self.gettemplate() + '\n'
		# script += 'set dashtype 1 "_"' + '\n'
		script += 'set dashtype 2 "_"' + '\n'
		script += 'set dashtype 3 (0.0,0.1,0.1,0.1)' + '\n'
		script += 'set dashtype 4 ".-' + '\n'
		script += 'set dashtype 5 "..-"' + '\n'

		script += self.getScript()
		writestring2File(temporal.TEMP_SCRIPT, script)
		self.GP_(temporal.TEMP_SCRIPT)

		if eps:
			return

		figOutput = Path.folderPlusFile(temporal.PROJECTFILES['folder'], self.getProjectParams()['FIGoutput'])
		if not eps:
			figOutput += '.fig'
		command = 'pstoedit ' + epsOutput + ' -dis -f fig ' + figOutput
		command = shlex.split(command)
		subprocess.check_output(command)

		if self.getXfigCompatible():
			self.fig2Friendly(figOutput)
		if self.getXfigAutoShow():
			subprocess.check_call(['xfig ' + figOutput], shell=True)

	def fig2Friendly(self, path):
		fig = Readfile(path)
		changes = self.getReplacements()
		newScript = fig2latexFriendly(fig, changes)
		writestring2File(path, newScript)

	def GP_(self, script_path, persist=False):
		commands = 'gnuplot '
		if persist:
			commands += '-p '
		commands += '"' + script_path.strip() + '"'
		commands = shlex.split(commands)
		console = '-'

		try:
			console = subprocess.check_output(commands, stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError, console:
			console = console.output
			print "Error! at reading script"
		print console


	# Style related methods
	def loadTemplate(self, style):
		self.cmb_Element.clear()
		self.cmb_type.clear()
		self.cmb_Element.addItem('Vectors', self.setType_(style['style_vectors']))
		self.cmb_Element.addItem('Arrows', self.setType_(style['style_arrows']))
		self.cmb_Element.addItem('Lines', self.setType_(style['lines_raw']))
		self.cmb_Element.addItem('Others', self.setcommands(style['commands']))

	def gettemplate(self):
		return self.template

	def getstyle(self):
		self.Style = openStyle()

	def loadStyles(self):
		Styles = getStyles()
		for style in Styles:
			path = style[0]
			name = style[1]['name']
			self.comboStyles.addItem(name, path)  # text to show in the combobox

	def getFolderStyle(self):
		return str(self.comboStyles.itemData(self.comboStyles.currentIndex()))
