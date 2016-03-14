# -*- coding: iso-8859-15 -*-
import shutil
import os
import sqlite3
import sys
import time
import pathlib


patterns = ['*.prt.*', '*.asm.*', '*.drw.*', '*.lay.*']

def purgefiles(folder, backup=True, keepversion=1,sub_folders=False):
    print("Purge files")

    con = sqlite3.connect(r'c:\temp\slask.db3')
    # con = sqlite3.connect(':memory:')

    insertstmt = 'INSERT INTO files VALUES (?,?,?,?)'
    selectstmt_01 = 'select name, ext, version from files group by name,ext'
    selectstmt_02 = 'select * from files where name=? and ext=? and version<=?'

    with con:
        cur = con.cursor()

        cur.execute("DROP TABLE IF EXISTS files")
        cur.execute('create table files (filename varchar(100), name varchar(100),ext varchar(100),version bigint)')
        con.commit()


        for pattern in patterns:
            searchfor = r'{0}\{1}'.format(folder, pattern)

            print("Sök: "+searchfor)

            if sub_folders:
                files = pathlib.Path(folder).glob('**/{0}'.format(pattern))
            else:
                files=pathlib.Path(folder).glob(pattern)

            for file in files:
                p=pathlib.WindowsPath(file)
                print(file)
                print(p.parent)
                print(file.name)
                strtmp = file.name.split('.')
                print(strtmp)

                if strtmp[2].isdigit():
                    parameters = (str(file), strtmp[0]+strtmp[1], strtmp[1], strtmp[2])
                    cur.execute(insertstmt, parameters)

        con.commit()

        cur.execute(selectstmt_01)
        rows = cur.fetchall()

        for row in rows:
            file = row[0]
            ext = row[1]
            version = row[2]

            print('{0} {1} {2}'.format(file, ext, version))

            cur1 = con.cursor()
            cur1.execute(selectstmt_02, (file, ext, version - keepversion))
            rows02 = cur1.fetchall()

            for row02 in rows02:
                deletefile = row02[0]

                dir_str=os.path.dirname(deletefile)

                if backup:
                    os.makedirs(r'{0}\Backup'.format(dir_str),exist_ok=True)

                try:
                    print('Deleting: '+deletefile)

                    if backup:
                        shutil.move(deletefile,r'{0}\Backup'.format(dir_str))
                    else:
                        print(deletefile)
                        # os.remove(deletefile)
                except Exception as e:
                    print(str(e))


def main(argv):
    folder = r'c:\work'

    starttime = time.time()

    purgefiles(folder,sub_folders=True)

    endtime = time.time()
    totaltime = (str(endtime - starttime))[:6]

    print(starttime)
    print(endtime)
    print(totaltime)


if __name__ == "__main__":
    main(sys.argv)
