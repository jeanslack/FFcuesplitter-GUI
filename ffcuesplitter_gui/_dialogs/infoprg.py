# -*- coding: UTF-8 -*-
"""
Name: infoprog.py
Porpose: about ffcuesplitter-gui
Compatibility: Python3, wxPython Phoenix
Author: Gianluca Pernigotto <jeanlucperni@gmail.com>
Copyright: (c) 2022 Gianluca Pernigotto <jeanlucperni@gmail.com>
license: GPL3
Rev: Jan.31.2022
########################################################

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
import wx
import wx.adv
from ffcuesplitter_gui._sys import info, version


def info_gui(parent, prg_icon):
    """
    It's a predefined template to create a dialog on
    the program information

    """
    infoprg = wx.adv.AboutDialogInfo()
    infoprg.SetIcon(wx.Icon(prg_icon, type=wx.BITMAP_TYPE_PNG))
    infoprg.SetName(info.__appname__)
    infoprg.SetVersion(f'v{version.__version__}')
    infoprg.SetDescription(_(info.__description__))
    infoprg.SetCopyright(f'Copyleft {info.__copyleft__} {info.__author__}')
    infoprg.SetWebSite(info.__projecturl__)
    infoprg.SetLicence(info.__licensefull__)
    infoprg.AddDeveloper(info.__author__)
    infoprg.AddDocWriter(f"{info.__author__}")
    infoprg.AddTranslator(f"{info.__author__} (it_IT)")
    # info.AddTranslator("Nestor Blanco <random@mail.es> (es_ES)")
    infoprg.SetArtists(
        [f"{info.__author__}"])
    wx.adv.AboutBox(infoprg)
    # event.Skip()
