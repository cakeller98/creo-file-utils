#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""purgeFiles.py: Description of what filetools does.

Testing
"""

import datetime
import logging
import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import filetools
import mainGUI
from util import log_util

__author__ = "Lars-Olof Levén"
__copyright__ = "Copyright 2016, Lars-Olof Levén"
__license__ = "The MIT License"
__version__ = "1.0.0"
__maintainer__ = "Lars-Olof Levén"
__email__ = "lars-olof.leven@lwdot.se"
__status__ = "Development"


class ShowGui(QtWidgets.QDialog, mainGUI.Ui_frm_main):
    def __init__(self, parent=None):
        super(ShowGui, self).__init__(parent)

        self.model_dir = os.path.dirname(os.path.abspath(__file__))
        self.module_name = os.path.basename(sys.argv[0])

        self.setupUi(self)

    def update_ui(self):
        self.btn_folder.clicked.connect(self.btn_click_folder)
        self.btn_purge.clicked.connect(self.btn_click_purge)
        self.spin_keep.valueChanged[int].connect(self.spin_keep_version)
        self.spin_keep.valueChanged[str].connect(self.spin_keep_version)
        self.edt_folder.setText(self.model_dir)

        self.table_output.setColumnCount(3)
        self.table_output.setRowCount(0)
        self.table_output.setHorizontalHeaderLabels(['Action', 'From', 'To'])

    def btn_click_folder(self):
        old_model_dir = self.model_dir

        self.model_dir = QFileDialog.getExistingDirectory(self, 'Select a folder', old_model_dir,
                                                          QFileDialog.ShowDirsOnly)

        if self.model_dir == '' or self.model_dir is None:
            self.model_dir = old_model_dir

        self.edt_folder.setText(self.model_dir)

    def btn_click_purge(self):
        creo_file_util = filetools.CreoFileTool(self)
        creo_file_util.rename_to_one = self.cb_rename_from_one.isChecked() and self.cb_rename_from_one.isEnabled()
        creo_file_util.remove_number = self.cb_remove_version.isChecked() and self.cb_remove_version.isEnabled()
        creo_file_util.sub_folders = self.cb_sub_folders.isChecked()
        creo_file_util.backup = self.cb_backup.isChecked()
        creo_file_util.folder = self.model_dir
        creo_file_util.keep_version = self.spin_keep.value()

        information_text = 'Rename finished!!!'

        self.table_output.setRowCount(0)

        try:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            creo_file_util.purge_files()

            if creo_file_util.rename_to_one or creo_file_util.remove_number:
                creo_file_util.rename_files()
        except Exception as e:
            log_util.log_information('ERROR', self.module_name, info_str='Problem to purge the files:',
                                     message_str="Error {}".format(e.args[0]))
        finally:
            QApplication.restoreOverrideCursor()

        if creo_file_util.error:
            information_text = 'Problem to rename'

        QMessageBox.information(self, 'Message', information_text, QMessageBox.Ok)

    def spin_keep_version(self, new_value):
        if int(new_value) > 1:
            self.cb_rename_from_one.setEnabled(True)
            self.cb_remove_version.setEnabled(False)
        else:
            self.cb_rename_from_one.setEnabled(False)
            self.cb_remove_version.setEnabled(True)

    def auto_size_table(self):
        self.table_output.resizeColumnsToContents()
        self.table_output.resizeRowsToContents()
        self.table_output.horizontalHeader().setStretchLastSection(True)

    def add_to_table(self, action_str, from_str, to_str=''):
        current_row_count = self.table_output.rowCount()
        self.table_output.insertRow(current_row_count)
        self.table_output.setItem(current_row_count, 0, QtWidgets.QTableWidgetItem(action_str))
        self.table_output.setItem(current_row_count, 1, QtWidgets.QTableWidgetItem(from_str))
        self.table_output.setItem(current_row_count, 2, QtWidgets.QTableWidgetItem(to_str))
        self.auto_size_table()


def main():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_util.init_logging(script_dir, date_str, logging.DEBUG)

    app = QtWidgets.QApplication(sys.argv)

    form = ShowGui()
    form.update_ui()
    form.show()
    result = app.exec_()

    log_util.clean_log_files(script_dir, keep_log_file=5)


if __name__ == "__main__":
    main()
