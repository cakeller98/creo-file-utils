#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""filetools.py: Description of what filetools does.

Testing
"""

import logging
import os
import pathlib
import sqlite3
import sys
import time
import shutil

__author__ = "Lars-Olof Levén"
__copyright__ = "Copyright 2016, Lars-Olof Levén"
__license__ = "The MIT License"
__version__ = "1.0.0"
__maintainer__ = "Lars-Olof Levén"
__email__ = "lars-olof.leven@lwdot.se"
__status__ = "Development"


class creo_file_tool:
    def __init__(self, output):
        self.patterns = ['*.prt.*', '*.asm.*', '*.drw.*', '*.lay.*']
        self.temp_env = ['TMPDIR', 'TEMP', 'TMP']

        self.temp_folder = None

        self.insertstmt = 'INSERT INTO files VALUES (?,?,?,?,?)'
        self.selectstmt_01 = 'select folder, name, ext, version from files group by folder, name,ext'
        self.selectstmt_02 = 'select * from files where folder=? and name=? and ext=? and version<=?'
        self.selectstmt_03 = 'select * from files where folder not like "%backup%" order by folder, name, ext, version'

        self.drop_stmt = 'DROP TABLE IF EXISTS files'
        self.create_stmt = 'create table files (filename varchar(1024), folder varchat(1024), name varchar(1024),ext varchar(100),version bigint)'

        self.temp_folder = self.get_temp_folder()

        self.print_out = output

        self.backup = True
        self.keep_version = 1
        self.rename_to_one = False
        self.remove_number = False
        self.folder = ''
        self.sub_folders = False

        self.init_db()

    def get_temp_folder(self):

        temp_str = ''

        for temp_item in self.temp_env:
            if temp_str is None and os.environ.get(temp_item) is not None:
                temp_str = os.environ.get(temp_item)

        return temp_str

    def init_db(self):
        self.temp_folder=self.get_temp_folder()
        self.con = sqlite3.connect(r'c:\temp\slask.db3')
        # self.con = sqlite3.connect(':memory:')

    def rename_files(self):

        rename_str = r'{0}\{1}.{2}.{3}'
        rename_str_no_number = r'{0}\{1}.{2}'

        cur = self.con.cursor()

        cur.execute(self.drop_stmt)
        cur.execute(self.create_stmt)
        self.con.commit()

        for pattern in self.patterns:
            searchfor = r'{0}\{1}'.format(self.folder, pattern)

            if self.sub_folders:
                files = pathlib.Path(self.folder).glob('**/{0}'.format(pattern))
            else:
                files = pathlib.Path(self.folder).glob(pattern)

            for file in files:
                p = pathlib.WindowsPath(file)
                strtmp = file.name.split('.')

                if strtmp[2].isdigit():
                    parameters = (str(file), str(p.parent), strtmp[0], strtmp[1], strtmp[2])
                    cur.execute(self.insertstmt, parameters)

        self.con.commit()

        cur.execute(self.selectstmt_03)
        rows = cur.fetchall()

        temp_file_name = ''
        temp_file_ext = ''
        num_value = 1

        for row in rows:
            full_file_name = row[0]
            file = row[2]
            ext = row[3]
            version = row[4]

            if temp_file_name != file and temp_file_ext != ext:
                temp_file_name = file
                temp_file_ext = ext
                num_value = 1

            if self.rename_to_one:
                try:
                    dir_str = os.path.dirname(full_file_name)

                    self.print_out.add_to_table('Rename', full_file_name,
                                                rename_str.format(dir_str, file, ext, num_value))
                    os.rename(full_file_name,rename_str.format(dir_str,file,ext,num_value))
                    num_value += 1
                except (IOError, OSError) as e:
                    print(str(e))
                    logging.error('Problem to rename file: ' + str(e))
                except Exception as e:
                    print(str(e))
                    logging.error('Problem to rename file: ' + str(e))

            if self.remove_number:
                try:
                    dir_str = os.path.dirname(full_file_name)
                    self.print_out.add_to_table('Remove ext', full_file_name,
                                                rename_str_no_number.format(dir_str, file, ext, num_value))
                    os.rename(full_file_name, rename_str_no_number.format(dir_str, file, ext, num_value))
                except (IOError, OSError) as e:
                    print(str(e))
                    logging.error('Problem to rename file: ' + str(e))
                except Exception as e:
                    print(str(e))
                    logging.error('Problem to rename file: ' + str(e))

    def purge_files(self):

        cur = self.con.cursor()

        cur.execute(self.drop_stmt)
        cur.execute(self.create_stmt)
        self.con.commit()

        for pattern in self.patterns:

            if self.sub_folders:
                files = pathlib.Path(self.folder).glob('**/{0}'.format(pattern))
            else:
                files = pathlib.Path(self.folder).glob(pattern)

            for file in files:
                strtmp = file.name.split('.')
                p = pathlib.WindowsPath(file)

                if strtmp[2].isdigit():
                    parameters = (str(file), str(p.parent), strtmp[0], strtmp[1], strtmp[2])
                    cur.execute(self.insertstmt, parameters)

        self.con.commit()

        cur.execute(self.selectstmt_01)
        rows = cur.fetchall()

        for row in rows:
            folder=row[0]
            file = row[1]
            ext = row[2]
            version = row[3]

            cur1 = self.con.cursor()
            cur1.execute(self.selectstmt_02, (folder, file, ext, version - self.keep_version))
            rows02 = cur1.fetchall()

            for row02 in rows02:
                deletefile = row02[0]

                dir_str = os.path.dirname(deletefile)

                try:
                    if self.backup:
                        os.makedirs(r'{0}\Backup'.format(dir_str), exist_ok=True)

                    try:
                        if self.backup:
                            self.print_out.add_to_table('Move', deletefile, r'{0}\Backup'.format(dir_str))
                            shutil.move(deletefile, r'{0}\Backup'.format(dir_str))

                        else:
                            self.print_out.add_to_table('Delete', deletefile)
                            os.remove(deletefile)
                    except (IOError, OSError) as e:
                        print(str(e))
                        logging.error('Problem to delete file: ' + str(e))
                    except Exception as e:
                        print(str(e))
                        logging.error('Problem to delete file: ' + str(e))
                except (IOError, OSError) as e:
                    print(str(e))
                    logging.error('Problem to create backuo folder: ' + str(e))
                except Exception as e:
                    print(str(e))
                    logging.error('Problem to create backuo folder: ' + str(e))


def main(argv):
    folder = r'c:\work'

    starttime = time.time()

    # purge_files(folder, sub_folders=True)

    endtime = time.time()
    totaltime = (str(endtime - starttime))[:6]

    print(starttime)
    print(endtime)
    print(totaltime)


if __name__ == "__main__":
    main(sys.argv)
