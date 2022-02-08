# -*- coding: UTF-8 -*-
"""
Name: argparser.py
Porpose: FFcuesplitter-GUI Command line arguments
Compatibility: Python3
Author: Gianluca Pernigotto <jeanlucperni@gmail.com>
Copyright: (c) 2021/2022 Gianluca Pernigotto <jeanlucperni@gmail.com>
license: GPL3
Rev: Feb.04.2022
Code checker: flake8, pylint .

This file is part of FFcuesplitter-GUI.

   FFcuesplitter-GUI is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   FFcuesplitter-GUI is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with FFcuesplitter-GUI.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import sys
from shutil import which
import argparse
from ffcuesplitter_gui._sys.info import (__appname__, __descriptionfull__)
from ffcuesplitter_gui._sys.version import __version__
try:
    import wx
    MSGWX = f"{wx.version()})"
except ModuleNotFoundError as errwx:
    MSGWX = f"not installed! ({errwx})"


def args():
    """
    User inputs parser for command line
    """
    parser = argparse.ArgumentParser(description=__descriptionfull__,)
    parser.add_argument('-v', '--version',
                        help="show the current version and exit",
                        action="store_true",
                        )
    parser.add_argument('-c', '--check',
                        help=('List of executables used by FFcuesplitter-GUI '
                              'found on the system'),
                        action="store_true",
                        )

    argmts = parser.parse_args()

    if argmts.check:
        deps = {'Required': {'ffmpeg': None, 'ffprobe': None}}
        for key, val in deps.items():
            if key in ('Required'):
                for exe in val:
                    val[exe] = which(exe, mode=os.F_OK | os.X_OK, path=None)
        print('\nList of executables used by FFcuesplitter-GUI:')
        for key, val in deps.items():
            for exe, path in val.items():
                if path:
                    print(f"\t[{key}] '{exe}' ...Ok")
                    print(f"\tpath: '{path}'\n")
                else:
                    print(f"\t[{key}] '{exe}' ...Not Installed")
                    print(f"\tpath: {path}\n")

    elif argmts.version:
        print(f'{__appname__}: v{__version__}')
        print(f'Python: {sys.version}')
        print(f'wxPython: {MSGWX}')

    else:
        print("Type 'ffcuesplitter-gui -h' for help.")
