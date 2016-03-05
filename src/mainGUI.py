# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\lole\PycharmProjects\creo-file-utils\src\mainGUI.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frm_main(object):
    def setupUi(self, frm_main):
        frm_main.setObjectName("frm_main")
        frm_main.resize(375, 281)
        frm_main.setMinimumSize(QtCore.QSize(375, 85))
        frm_main.setMaximumSize(QtCore.QSize(375, 1000))
        self.widget = QtWidgets.QWidget(frm_main)
        self.widget.setGeometry(QtCore.QRect(12, 45, 217, 22))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cb_backup = QtWidgets.QCheckBox(self.widget)
        self.cb_backup.setChecked(True)
        self.cb_backup.setObjectName("cb_backup")
        self.horizontalLayout_2.addWidget(self.cb_backup)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.checkBox = QtWidgets.QCheckBox(self.widget)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_2.addWidget(self.checkBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.widget1 = QtWidgets.QWidget(frm_main)
        self.widget1.setGeometry(QtCore.QRect(240, 240, 123, 25))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.btn_purge = QtWidgets.QPushButton(self.widget1)
        self.btn_purge.setObjectName("btn_purge")
        self.horizontalLayout_3.addWidget(self.btn_purge)
        self.widget2 = QtWidgets.QWidget(frm_main)
        self.widget2.setObjectName("widget2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edt_folder = QtWidgets.QLineEdit(self.widget2)
        self.edt_folder.setDragEnabled(False)
        self.edt_folder.setObjectName("edt_folder")
        self.horizontalLayout.addWidget(self.edt_folder)
        self.btn_folder = QtWidgets.QPushButton(self.widget2)
        self.btn_folder.setObjectName("btn_folder")
        self.horizontalLayout.addWidget(self.btn_folder)

        self.retranslateUi(frm_main)
        QtCore.QMetaObject.connectSlotsByName(frm_main)

    def retranslateUi(self, frm_main):
        _translate = QtCore.QCoreApplication.translate
        frm_main.setWindowTitle(_translate("frm_main", "Purge Creo Files"))
        self.cb_backup.setText(_translate("frm_main", "Backuop"))
        self.checkBox.setText(_translate("frm_main", "Rename to 1"))
        self.btn_purge.setText(_translate("frm_main", "Purge"))
        self.btn_folder.setText(_translate("frm_main", "Folder"))

