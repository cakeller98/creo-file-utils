from distutils.core import setup
import os
import py2exe

includes = ["sip",
            "PyQt5",
            "PyQt5.QtCore",
            "PyQt5.QtGui",
            "os",
            "sys"]
            
datafiles = [("platforms", ["C:\\ProgLib\\Devel\\Python34\\Lib\\site-packages\\PyQt5\\plugins\\platforms\\qwindows.dll"]),
             ("", [r"c:\windows\syswow64\MSVCP100.dll",
                   r"c:\windows\syswow64\MSVCR100.dll"])]
            
setup(
    # console=[{"script":"tt.py"}], 
    windows=[
        {
            "script":"purgeFiles.py",
            "icon_resources": [(1, "test_01.ico")]
        }
    ],
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