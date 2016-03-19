# -*- coding: iso-8859-15 -*-
import shutil
import os
import sqlite3
import sys
import time
import pathlib


class creo_file_tool:
    def __init__(self, output):
        self.patterns = ['*.prt.*', '*.asm.*', '*.drw.*', '*.lay.*']
        self.temp_env = ['TMPDIR', 'TEMP', 'TMP']

        self.temp_folder = None

        self.insertstmt = 'INSERT INTO files VALUES (?,?,?,?)'
        self.selectstmt_01 = 'select name, ext, version from files group by name,ext'
        self.selectstmt_02 = 'select * from files where name=? and ext=? and version<=?'


        self.drop_stmt = "DROP TABLE IF EXISTS files"
        self.create_stmt = 'create table files (filename varchar(100), name varchar(100),ext varchar(100),version bigint)'

        for temp_str in self.temp_env:
            if self.temp_folder is None and os.environ.get(temp_str) is not None:
                self.temp_folder = os.environ.get(temp_str)

        self.print_out=output

    def init_db(self):
        self.con = sqlite3.connect(r'c:\temp\slask.db3')
        # self.con = sqlite3.connect(':memory:')

    def rename_files(self, folder, sub_folders=False):
        print("Rename files")

        cur = self.con.cursor()

        cur.execute(self.drop_stmt)
        cur.execute(self.create_stmt)
        self.con.commit()

        for pattern in self.patterns:
            searchfor = r'{0}\{1}'.format(folder, pattern)

            print("Sök: " + searchfor)

            if sub_folders:
                files = pathlib.Path(folder).glob('**/{0}'.format(pattern))
            else:
                files = pathlib.Path(folder).glob(pattern)

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

    def purge_files(self, folder, backup=True, keepversion=1, sub_folders=False):
        print("Purge files")

        cur = self.con.cursor()

        cur.execute(self.drop_stmt)
        cur.execute(self.create_stmt)
        self.con.commit()

        for pattern in self.patterns:
            searchfor = r'{0}\{1}'.format(folder, pattern)

            print("Sök: " + searchfor)

            if sub_folders:
                files = pathlib.Path(folder).glob('**/{0}'.format(pattern))
            else:
                files = pathlib.Path(folder).glob(pattern)

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
            cur1.execute(self.selectstmt_02, (file, ext, version - keepversion))
            rows02 = cur1.fetchall()

            for row02 in rows02:
                deletefile = row02[0]

                dir_str = os.path.dirname(deletefile)

                if backup:
                    os.makedirs(r'{0}\Backup'.format(dir_str), exist_ok=True)

                try:
                    print('Deleting: ' + deletefile)
                    self.print_out.print_str('Deleting: ' + deletefile)

                    if backup:
                        shutil.move(deletefile, r'{0}\Backup'.format(dir_str))
                    else:
                        print(deletefile)
                        # os.remove(deletefile)
                except Exception as e:
                    print(str(e))


def main(argv):
    folder = r'c:\work'

    starttime = time.time()

    purge_files(folder, sub_folders=True)

    endtime = time.time()
    totaltime = (str(endtime - starttime))[:6]

    print(starttime)
    print(endtime)
    print(totaltime)


if __name__ == "__main__":
    main(sys.argv)
