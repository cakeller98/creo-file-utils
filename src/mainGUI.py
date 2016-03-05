# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Development\PycharmProjects\purgeFiles\mainGUI.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frm_main(object):
    def setupUi(self, frm_main):
        frm_main.setObjectName("frm_main")
        frm_main.resize(375, 85)
        frm_main.setMinimumSize(QtCore.QSize(375, 85))
        frm_main.setMaximumSize(QtCore.QSize(375, 85))
        self.layoutWidget = QtWidgets.QWidget(frm_main)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 12, 351, 58))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edt_folder = QtWidgets.QLineEdit(self.layoutWidget)
        self.edt_folder.setDragEnabled(False)
        self.edt_folder.setObjectName("edt_folder")
        self.horizontalLayout.addWidget(self.edt_folder)
        self.btn_folder = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_folder.setObjectName("btn_folder")
        self.horizontalLayout.addWidget(self.btn_folder)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cb_backup = QtWidgets.QCheckBox(self.layoutWidget)
        self.cb_backup.setChecked(True)
        self.cb_backup.setObjectName("cb_backup")
        self.horizontalLayout_2.addWidget(self.cb_backup)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btn_purge = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_purge.setObjectName("btn_purge")
        self.horizontalLayout_2.addWidget(self.btn_purge)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(frm_main)
        QtCore.QMetaObject.connectSlotsByName(frm_main)

    def retranslateUi(self, frm_main):
        _translate = QtCore.QCoreApplication.translate
        frm_main.setWindowTitle(_translate("frm_main", "Purge Creo Files"))
        self.btn_folder.setText(_translate("frm_main", "Folder"))
        self.cb_backup.setText(_translate("frm_main", "Backuop"))
        self.btn_purge.setText(_translate("frm_main", "Purge"))

