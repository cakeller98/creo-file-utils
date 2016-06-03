from distutils.core import setup
import os
import py2exe

includes = ["sip",
            "PyQt5",
            "PyQt5.QtCore",
            "PyQt5.QtGui",
            "os",
            "sys"]
            
datafiles = [("platforms", ["D:\\ProgLib\\Devel\\Python34\\Lib\\site-packages\\PyQt5\\plugins\\platforms\\qwindows.dll"]),
             ("", [r"c:\windows\syswow64\MSVCP100.dll",
                   r"c:\windows\syswow64\MSVCR100.dll"])]
            
setup(
    # console=[{"script":"tt.py"}], 
    windows=[{"script":"purgeFiles.py"}],
    scripts=['purgeFiles.py'],
    data_files=datafiles,
    zipfile=None,    
    options={
        "py2exe":{
            "includes":includes,
            "bundle_files": 1,
            "compressed": True
        }
    }
    
)