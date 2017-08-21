import os
import sys

import winshell
from cx_Freeze import setup, Executable

platform = sys.platform
base = 'Win32GUI' if platform == 'win32' else platform

python_path = sys.exec_prefix

os.environ['TCL_LIBRARY'] = os.path.join(python_path, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(python_path, 'tcl', 'tk8.6')

executable = Executable('main.py',
                        base=base,
                        icon='icon.ico',
                        targetName='Demonica.exe')

options = {'build_exe': {
               'include_files': [
                   os.path.join(python_path, 'DLLs', 'tcl86t.dll'),
                   os.path.join(python_path, 'DLLs', 'tk86t.dll'),
                   'icon.ico'
               ]
          }
}

setup(name='Demonica',
      version="0.1",
      description='A save editor for Shin Megami Tensei 4: Apocalypse.',
      options=options,
      executables=[executable])

path = os.path.join(os.getcwd(), 'build', 'exe.win32-3.6', 'Demonica.exe')

with winshell.shortcut('Demonica.lnk') as link:
    link.path = path
    link.icon = path, 0
    link.description = 'A save editor for Shin Megami Tensei 4: Apocalypse.'
