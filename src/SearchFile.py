# -*- coding: utf-8 -*-
import os
from PyQt4 import QtGui, QtCore


class PathMethods():
	def __init__(self, parent=None):
		pass

	def PathConnections(self):
		self.connect(self.btn_searchFile, QtCore.SIGNAL("clicked()"), self.searchFile)
		self.connect(self.field_path, QtCore.SIGNAL("textChanged(QString)"), self.checkPath)
		# self.connect(self.btnExport, QtCore.SIGNAL("clicked()"), self.getExportInfo)
		# self.connect(self.btnCancel, QtCore.SIGNAL("clicked()"), self.closeWin)

	def searchFile(self):
		path = str(QtGui.QFileDialog.getOpenFileName(self, "Select Directory", '', '*.plt'))
		path = os.path.normcase(path)
		self.field_path.setText(path)

	def checkPath(self):
		path = str(self.field_path.text())
		folder = os.path.dirname(path)
		isValid = os.access(os.path.dirname(path), os.W_OK)
		if not isValid:
			path = False
			folder = False

		return path, folder

	def closeEvent(self, event):
		self.closeWin()

	def closeWin(self):
		# self.accept()
		pass
