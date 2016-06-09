# -*- coding: utf-8 -*-
import sip
sip.setapi('QVariant', 2)
from PyQt4 import QtGui
from ui.MainWindow import Ui_MainWindow
from CentralPanel import CentralPanel
import temporal
import parser
from SearchFile import PathMethods
from tools.dictionaries import dic2str
from tools.files import writestring2File, Readfile_string
import tools.paths as Path


class MainWindow(QtGui.QMainWindow, Ui_MainWindow, PathMethods):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__()
		self.setupUi(self)
		self.CentralWidget = CentralPanel(self)
		self.setCentralWidget(self.CentralWidget)
		# actions
		self.actionNewProject.triggered.connect(self.newProject)
		self.actionLoadFile.triggered.connect(self.openFile)
		self.actionSave.triggered.connect(self.saveProject)

	def setLastPath(self, path):
		writestring2File('temp/lastpath.txt', path.strip())

	def getLastPath(self):
		lastPath = Readfile_string('temp/lastpath.txt')
		if not lastPath:
			return ''
		return lastPath.strip()

	def saveProject(self):
		self.CentralWidget.saveProject()

	def checkFile(self, new=False):
		if new:
			path = str(QtGui.QFileDialog.getOpenFileName(self, "Select Directory", self.getLastPath(), '(*.plt)'))
		else:
			path = str(QtGui.QFileDialog.getSaveFileName(self, "Select Directory", self.getLastPath(), '(*.plt)'))
			if path and '.plt' not in path:
				path = path.strip()+'.plt'
		pathData = Path.getPathData(path)

		return pathData

	def newProject(self):
		print "Starting New File"
		self.openFile(new_=True)


	def openFile(self, new_=False):
		temporal.PROJECTFILES = {}
		if not new_:
			print "Opening existing File"
		pathData = self.checkFile(new=not new_)

		if new_:
			writestring2File(pathData['mainPath'],'')

		temporal.PROJECTFILES = pathData
		if not pathData:
			print "path not found"
			return
		configData = parser.plotConfig(pathData['mainPath'], pathData['baseName'], new=new_)
		self.setLastPath(pathData['folder'])
		self.CentralWidget.openFile(configData)
		if new_:
			self.CentralWidget.saveProject()


if __name__ == '__main__':

	import sys
	app = QtGui.QApplication(sys.argv)
	app.setApplicationName('GNUPletes')
	app.setApplicationVersion('Alpha - 0.1')
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())
