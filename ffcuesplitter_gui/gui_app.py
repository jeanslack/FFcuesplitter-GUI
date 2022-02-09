# -*- coding: UTF-8 -*-
"""
Name: gui_app.py
Porpose: bootstrap for FFcuesplitter-GUI app.
Compatibility: Python3, wxPython Phoenix
Author: Gianluca Pernigotto <jeanlucperni@gmail.com>
Copyright: (c) 2022/2023 Gianluca Pernigotto <jeanlucperni@gmail.com>
license: GPL3
Rev: Feb.04.2022
Code checker: flake8, pylint

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
import builtins
import wx
try:
    from wx.svg import SVGimage
except ModuleNotFoundError:
    pass
from ffcuesplitter_gui._sys.argparser import args
from ffcuesplitter_gui._sys import settings_manager
from ffcuesplitter_gui._sys import app_const as appC
from ffcuesplitter_gui._utils.utils import del_filecontents

# add translation macro to builtin similar to what gettext does
builtins.__dict__['_'] = wx.GetTranslation


class CuesplitterGUI(wx.App):
    """
    bootstrap the wxPython GUI toolkit before
    starting the main_frame.

    """

    def __init__(self, redirect=True, filename=None):
        """
        - redirect=False will send print statements to a console
          window (in use)
        - redirect=True will be sent to a little textbox window.
        - filename=None Redirect sys.stdout and sys.stderr
          to a popup window.
        - filename='path/to/file.txt' Redirect sys.stdout
          and sys.stderr to file

        See main() function below to settings it.

        """
        self.locale = None
        self.appset = {'DISPLAY_SIZE': None,
                       'GETLANG': None,
                       # short name for the locale
                       'SUPP_LANGs': ['it_IT', 'en_EN', 'ru_RU'],
                       # supported help langs
                       }
        self.data = settings_manager.DataSource()  # instance data
        self.appset.update(self.data.get_fileconf())  # data system
        self.iconset = None

        wx.App.__init__(self, redirect, filename)  # constructor
        wx.SystemOptions.SetOption("osx.openfiledialog.always-show-types", "1")
    # -------------------------------------------------------------------

    def OnInit(self):
        """Bootstrap interface."""

        if self.appset.get('ERROR'):
            wx.MessageBox(f"FATAL: {self.appset['ERROR']}\n\nSorry, cannot "
                          f"continue..", 'FFcuesplitter-GUI - ERROR',
                          wx.ICON_STOP)
            return False

        self.appset['DISPLAY_SIZE'] = wx.GetDisplaySize()  # get monitor res
        self.iconset = self.data.icons_set(self.appset['icontheme'])

        # locale
        #wx.Locale.AddCatalogLookupPathPrefix(self.appset['localepath'])
        #self.update_language()
        #self.appset['GETLANG'] = self.locale.GetName()

        if not os.path.exists(self.appset['logdir']):
            try:  # make log folder
                os.makedirs(self.appset['logdir'], mode=0o777)
            except OSError as err:
                wx.MessageBox(f'{err}', 'FFcuesplitter-GUI', wx.ICON_STOP)
                return False

        if self.check_ffmpeg() is True:
            self.wizard(self.iconset['ffcuesplittergui'])
            return True

        from ffcuesplitter_gui._main.main_frame import MainFrame
        main_frame = MainFrame()
        main_frame.Show()
        self.SetTopWindow(main_frame)
        return True
    # -------------------------------------------------------------------

    def check_ffmpeg(self):
        """
        Get the FFmpeg's executables. On Unix/Unix-like systems
        perform a check for permissions.
        """
        for link in [self.appset['ffmpeg_cmd'],
                     self.appset['ffprobe_cmd'],
                     ]:
            if self.appset['ostype'] == 'Windows':  # check for exe
                # HACK use even for unix, if not permission is equal
                # to not binaries
                if not which(link, mode=os.F_OK | os.X_OK, path=None):
                    return True
            else:
                if not os.path.isfile(f"{link}"):
                    return True

        if not self.appset['ostype'] == 'Windows':
            # check for permissions when linked locally
            for link in [self.appset['ffmpeg_cmd'],
                         self.appset['ffprobe_cmd'],
                         ]:
                if which(link, mode=os.F_OK | os.X_OK, path=None):
                    permissions = True
                else:
                    wx.MessageBox(_('Permission denied: {}\n\n'
                                    'Check execution permissions.').format
                                  (link), 'FFcuesplitter-GUI', wx.ICON_STOP)
                    permissions = False
                    break

            return False if not permissions else None
        return None
    # -------------------------------------------------------------------

    def wizard(self, wizardicon):
        """
        Show an initial dialog to setup the application
        during the first start-up.

        """
        from ffcuesplitter_gui._dialogs.wizard_dlg import Wizard
        main_frame = Wizard(wizardicon)
        main_frame.Show()
        self.SetTopWindow(main_frame)
        return True
    # -------------------------------------------------------------------

    def update_language(self, lang=None):
        """
        Update the language to the requested one.
        Make *sure* any existing locale is deleted before the new
        one is created.  The old C++ object needs to be deleted
        before the new one is created, and if we just assign a new
        instance to the old Python variable, the old C++ locale will
        not be destroyed soon enough, likely causing a crash.

        :param string `lang`: one of the supported language codes

        """
        # if an unsupported language is requested default to English
        if lang in appC.supLang:
            selectlang = appC.supLang[lang]
        else:
            selectlang = wx.LANGUAGE_DEFAULT

        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale

        # create a locale object for this language
        self.locale = wx.Locale(selectlang)
        if self.locale.IsOk():
            self.locale.AddCatalog(appC.langDomain)
        else:
            self.locale = None
    # -------------------------------------------------------------------

    def OnExit(self):
        """
        OnExit provides an interface for exiting the application.
        The ideal place to run the last few things before completely
        exiting the application, eg. delete temporary files etc.
        """
        if self.appset['clearlogfiles'] is True:
            logdir = self.appset['logdir']
            if os.path.exists(logdir):
                flist = os.listdir(logdir)
                if flist:
                    for logname in flist:
                        logfile = os.path.join(logdir, logname)
                        try:
                            del_filecontents(logfile)
                        except Exception as err:
                            wx.MessageBox(_("Unexpected error while "
                                            "deleting file contents:\n\n"
                                            "{0}").format(err),
                                          'FFcuesplitter-GUI', wx.ICON_STOP)
                            return False
        return True
    # -------------------------------------------------------------------


def main():
    """
    Without arguments starts the wx.App mainloop
    instead to print output to console.
    """
    if not sys.argv[1:]:
        app = CuesplitterGUI(redirect=False)
        app.MainLoop()

    else:
        args()
        sys.exit(0)
