# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/MainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(640, 480)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuScript = QtGui.QMenu(self.menubar)
        self.menuScript.setObjectName(_fromUtf8("menuScript"))
        MainWindow.setMenuBar(self.menubar)
        self.actionLoadFile = QtGui.QAction(MainWindow)
        self.actionLoadFile.setObjectName(_fromUtf8("actionLoadFile"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionNewProject = QtGui.QAction(MainWindow)
        self.actionNewProject.setObjectName(_fromUtf8("actionNewProject"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionOpen_REcent = QtGui.QAction(MainWindow)
        self.actionOpen_REcent.setObjectName(_fromUtf8("actionOpen_REcent"))
        self.menuFile.addAction(self.actionLoadFile)
        self.menuFile.addAction(self.actionOpen_REcent)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNewProject)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuFile.addSeparator()
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuScript.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "GUISSE: Gnuplot User Interpreter Suggested for Student\'s Experimentation", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuScript.setTitle(_translate("MainWindow", "Script", None))
        self.actionLoadFile.setText(_translate("MainWindow", "Open", None))
        self.actionLoadFile.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.actionNewProject.setText(_translate("MainWindow", "New", None))
        self.actionNewProject.setShortcut(_translate("MainWindow", "Ctrl+N", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))
        self.actionOpen_REcent.setText(_translate("MainWindow", "Recent project", None))

