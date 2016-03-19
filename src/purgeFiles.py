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

        self.workdir = r'C:\Work'

        self.setupUi(self)

    def update_ui(self):
        print('Test')

        self.btn_folder.clicked.connect(self.btn_click_folder)
        self.btn_purge.clicked.connect(self.btn_click_purge)
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

        filetools.purgefiles(self.workdir, self.cb_backup.isChecked())


def main(argv):
    app = QtWidgets.QApplication(sys.argv)

    form = ShowGui()
    form.update_ui()
    form.show()
    result = app.exec_()


if __name__ == "__main__":
    main(sys.argv)
