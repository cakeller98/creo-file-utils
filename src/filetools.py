#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""filetools.py: Description of what filetools does.

Testing
"""

import shutil
import os
import sqlite3
import sys
import time
import pathlib
import logging

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

        self.insertstmt = 'INSERT INTO files VALUES (?,?,?,?)'
        self.selectstmt_01 = 'select name, ext, version from files group by name,ext'
        self.selectstmt_02 = 'select * from files where name=? and ext=? and version<=?'
        self.selectstmt_03 = 'select * from files grop by name, ext order by version'

        self.drop_stmt = 'DROP TABLE IF EXISTS files'
        self.create_stmt = 'create table files (filename varchar(100), name varchar(100),ext varchar(100),version bigint)'

        self.temp_folder = self.get_temp_folder()

        self.print_out = output

        self.backup = True
        self.keep_version = 1
        self.rename_to_one = False
        self.remove_number = False
        self.folder = ''
        self.sub_folders = False

    def get_temp_folder(self):

        temp_str = ''

        for temp_item in self.temp_env:
            if temp_str is None and os.environ.get(temp_item) is not None:
                temp_str = os.environ.get(temp_item)

        return temp_str

    def init_db(self):
        self.con = sqlite3.connect(r'c:\temp\slask.db3')
        # self.con = sqlite3.connect(':memory:')

    def rename_files(self):
        print("Rename files")

        rename_str = r'{0}\{1}.{2}.{3}'
        rename_str_no_number = r'{0}\{1}.{2}'

        cur = self.con.cursor()

        cur.execute(self.drop_stmt)
        cur.execute(self.create_stmt)
        self.con.commit()

        for pattern in self.patterns:
            searchfor = r'{0}\{1}'.format(self.folder, pattern)

            print("Sök: " + searchfor)

            if self.sub_folders:
                files = pathlib.Path(self.folder).glob('**/{0}'.format(pattern))
            else:
                files = pathlib.Path(self.folder).glob(pattern)

            for file in files:
                p = pathlib.WindowsPath(file)
                print(file)
                print(p.parent)
                print(file.name)
                strtmp = file.name.split('.')
                print(strtmp)

                if strtmp[2].isdigit():
                    parameters = (str(file), strtmp[0] + strtmp[1], strtmp[1], strtmp[2])
                    cur.execute(self.insertstmt, parameters)

        self.con.commit()

        cur.execute(self.selectstmt_03)
        rows = cur.fetchall()

        temp_file_name = ''
        temp_file_ext = ''
        num_value = 1

        for row in rows:
            full_file_name = row[0]
            file = row[1]
            ext = row[2]
            version = row[3]

            if temp_file_name != file and temp_file_ext != ext:
                temp_file_name = file
                temp_file_ext = ext
                num_value = 1

            if self.rename_to_one:
                try:
                    dir_str = os.path.dirname(full_file_name)
                    print('---- Start rename ----')
                    print(full_file_name)
                    print(rename_str.format(dir_str, file, ext, num_value))
                    print('---- End rename ----')

                    # os.rename(full_file_name,rename_str.format(dir_str,file,ext,num_value))
                    num_value += 1
                except (IOError, OSError) as e:
                    print(str(e))
                    logging.error('Problem to rename file: ' + str(e))
                except Exception as e:
                    print(str(e))

            if self.remove_number:
                try:
                    dir_str = os.path.dirname(full_file_name)
                    print('---- Start remove num ----')
                    print(full_file_name)
                    print(rename_str_no_number.format(dir_str, file, ext, num_value))
                    print('---- End remove num ----')

                    # os.rename(full_file_name,                rename_str_no_number.format(dir_str,file,ext,num_value))
                except (IOError, OSError) as e:
                    print(str(e))
                except Exception as e:
                    print(str(e))

    def purge_files(self):
        print("Purge files")

        cur = self.con.cursor()

        cur.execute(self.drop_stmt)
        cur.execute(self.create_stmt)
        self.con.commit()

        for pattern in self.patterns:
            searchfor = r'{0}\{1}'.format(self.folder, pattern)

            print("Sök: " + searchfor)

            if self.sub_folders:
                files = pathlib.Path(self.folder).glob('**/{0}'.format(pattern))
            else:
                files = pathlib.Path(self.folder).glob(pattern)

            for file in files:
                p = pathlib.WindowsPath(file)
                print(file)
                print(p.parent)
                print(file.name)
                strtmp = file.name.split('.')
                print(strtmp)

                if strtmp[2].isdigit():
                    parameters = (str(file), strtmp[0] + strtmp[1], strtmp[1], strtmp[2])
                    cur.execute(self.insertstmt, parameters)

        self.con.commit()

        cur.execute(self.selectstmt_01)
        rows = cur.fetchall()

        for row in rows:
            file = row[0]
            ext = row[1]
            version = row[2]

            print('{0} {1} {2}'.format(file, ext, version))

            cur1 = self.con.cursor()
            cur1.execute(self.selectstmt_02, (file, ext, version - self.keepversion))
            rows02 = cur1.fetchall()

            for row02 in rows02:
                deletefile = row02[0]

                dir_str = os.path.dirname(deletefile)

                try:
                    if self.backup:
                        os.makedirs(r'{0}\Backup'.format(dir_str), exist_ok=True)

                    try:
                        print('Deleting: ' + deletefile)
                        self.print_out.print_str('Deleting: ' + deletefile)

                        if self.backup:
                            # shutil.move(deletefile, r'{0}\Backup'.format(dir_str))
                            print('Backup file: ' + deletefile)
                        else:
                            print(deletefile)
                            # os.remove(deletefile)
                    except (IOError, OSError) as e:
                        print(str(e))
                    except Exception as e:
                        print(str(e))

                except (IOError, OSError) as e:
                    print(str(e))
                except Exception as e:
                    print(str(e))

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
