#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""purgeFiles.py: Description of what filetools does.

Testing
"""

from PyQt5 import QtWidgets
# from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import mainGUI
import filetools
import logging
import datetime
import os

__author__ = "Lars-Olof Levén"
__copyright__ = "Copyright 2016, Lars-Olof Levén"
__license__ = "The MIT License"
__version__ = "1.0.0"
__maintainer__ = "Lars-Olof Levén"
__email__ = "lars-olof.leven@lwdot.se"
__status__ = "Development"

def initLogging(dateStr,logLevel):
   scriptDir=os.path.dirname(os.path.abspath(__file__))
   fmt='%(asctime)s - %(name)s - %(levelname)s - %(module)s : %(lineno)d - %(message)s'
   filename =scriptDir+r'\log '+dateStr+'.log'
   logging.basicConfig(level=logLevel,format=fmt,filename=filename,filemode='w')

class ShowGui(QtWidgets.QDialog, mainGUI.Ui_frm_main):
    def __init__(self, parent=None):
        super(ShowGui, self).__init__(parent)

        self.workdir = r'C:\Work'

        self.setupUi(self)

    def update_ui(self):
        print('Test')

        self.btn_folder.clicked.connect(self.btn_click_folder)
        self.btn_purge.clicked.connect(self.btn_click_purge)
        self.spin_keep.valueChanged[int].connect(self.spin_keep_version)
        # self.spin_keep.valueChanged[str].connect(self.spin_keep_version)
        self.edt_folder.setText(self.workdir)

    def btn_click_folder(self):
        oldworkingdir = self.workdir

        self.workdir = QFileDialog.getExistingDirectory(self, 'Select a folder', oldworkingdir,
                                                        QFileDialog.ShowDirsOnly)

        if self.workdir == '' or self.workdir is None:
            self.workdir = oldworkingdir

        self.edt_folder.setText(self.workdir)

    def btn_click_purge(self):
        print('tttt')

        creo_file_util=filetools.creo_file_tool(self)
        creo_file_util.rename_to_one = self.cb_rename_from_one.isChecked() and self.cb_rename_from_one.isEnabled()
        creo_file_util.remove_number = self.cb_remove_version.isChecked() and self.cb_remove_version.isEnabled()
        creo_file_util.sub_folders = self.cb_sub_folders.isChecked()
        creo_file_util.backup = self.cb_backup.isChecked()
        creo_file_util.folder = self.workdir

        creo_file_util.purge_files()

        if creo_file_util.rename_to_one or creo_file_util.remove_number:
            creo_file_util.rename_files()
        # filetools.purgefiles(self.workdir, self.cb_backup.isChecked())

    def spin_keep_version(self, new_value):
        # slasl=self.spin_keep.value()
        if new_value>1:
            self.cb_rename_from_one.setEnabled(True)
            self.cb_remove_version.setEnabled(False)
        else:
            self.cb_rename_from_one.setEnabled(False)
            self.cb_remove_version.setEnabled(True)


def main(argv):
    dateStr = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    initLogging(dateStr, logging.DEBUG)

    app = QtWidgets.QApplication(sys.argv)

    form = ShowGui()
    form.update_ui()
    form.show()
    result = app.exec_()


if __name__ == "__main__":
    main(sys.argv)
