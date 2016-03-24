#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""filetools.py: Description of what filetools does.

Testing
"""

import logging
import os
import pathlib
import sqlite3
import shutil

__author__ = "Lars-Olof Lev�n"
__copyright__ = "Copyright 2016, Lars-Olof Lev�n"
__license__ = "The MIT License"
__version__ = "1.0.0"
__maintainer__ = "Lars-Olof Lev�n"
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
        self.error = False

        self.header = '---------------------------------'

        self.init_db()

    def get_temp_folder(self):

        temp_str = ''

        for temp_item in self.temp_env:
            if temp_str is None and os.environ.get(temp_item) is not None:
                temp_str = os.environ.get(temp_item)

        return temp_str

    def init_db(self):
        self.temp_folder = self.get_temp_folder()
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
                    os.rename(full_file_name, rename_str.format(dir_str, file, ext, num_value))
                    num_value += 1
                except (IOError, OSError) as e:
                    self.error = True
                    logging.error('{0}\n{1}\n{2}'.format(self.header, 'Problem to rename file:',
                                                         "Error {}".format(e.args[0])))
                except Exception as e:
                    self.error = True
                    logging.error('{0}\n{1}\n{2}'.format(self.header, 'Problem to rename file:',
                                                         "Error {}".format(e.args[0])))

            if self.remove_number:
                try:
                    dir_str = os.path.dirname(full_file_name)
                    self.print_out.add_to_table('Remove ext', full_file_name,
                                                rename_str_no_number.format(dir_str, file, ext, num_value))
                    os.rename(full_file_name, rename_str_no_number.format(dir_str, file, ext, num_value))
                except (IOError, OSError) as e:
                    self.error = True
                    logging.error('{0}\n{1}\n{2}'.format(self.header, 'Problem to remove number:',
                                                         "Error {}".format(e.args[0])))
                except Exception as e:
                    self.error = True
                    logging.error('{0}\n{1}\n{2}'.format(self.header, 'Problem to remove number:',
                                                         "Error {}".format(e.args[0])))

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
            folder = row[0]
            file = row[1]
            ext = row[2]
            version = row[3]

            cur1 = self.con.cursor()
            cur1.execute(self.selectstmt_02, (folder, file, ext, version - self.keep_version))
            rows02 = cur1.fetchall()

            for row02 in rows02:
                delete_file = row02[0]

                dir_str = os.path.dirname(delete_file)
                file_name = os.path.basename(delete_file)

                try:
                    if self.backup:
                        os.makedirs(r'{0}\Backup'.format(dir_str), exist_ok=True)

                    try:
                        if self.backup:
                            backup_dst = r'{0}\Backup'.format(dir_str)
                            self.print_out.add_to_table('Move', delete_file, backup_dst)

                            if os.path.exists(r'{0}\{1}'.format(backup_dst, file_name)):
                                os.remove(r'{0}\{1}'.format(backup_dst, file_name))

                            shutil.move(delete_file, backup_dst)
                        else:
                            self.print_out.add_to_table('Delete', delete_file)
                            os.remove(delete_file)
                    except (IOError, OSError) as e:
                        self.error = True
                        logging.error('{0}\n{1}\n{2}'.format(self.header, 'Problem to delete file:',
                                                             "Error {}".format(e.args[0])))
                    except Exception as e:
                        self.error = True
                        logging.error('{0}\n{1}\n{2}'.format(self.header, 'Problem to delete file:',
                                                             "Error {}".format(e.args[0])))
                except (IOError, OSError) as e:
                    self.error = True
                    logging.error('{0}\n{1}\n{2}'.format(self.header, 'Problem to create backup folder:',
                                                         "Error {}".format(e.args[0])))
                except Exception as e:
                    self.error = True
                    logging.error('{0}\n{1}\n{2}'.format(self.header, 'Problem to create backup folder:',
                                                         "Error {}".format(e.args[0])))
