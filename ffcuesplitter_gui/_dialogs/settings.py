# -*- coding: UTF-8 -*-
"""
Name: settings.py
Porpose: FFcuesplitter-GUI setup dialog
Compatibility: Python3, wxPython Phoenix
Author: Gianluca Pernigotto <jeanlucperni@gmail.com>
Copyright: (c) 2022 Gianluca Pernigotto <jeanlucperni@gmail.com>
license: GPL3
Rev: Jan.30.2022
Code checker: pycodestyle
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
import os
import sys
import webbrowser
import wx
from ffcuesplitter_gui._utils.utils import detect_binaries
from ffcuesplitter_gui._sys.settings_manager import ConfigManager


class Setup(wx.Dialog):
    """
    Represents settings and configuration
    storing of the program.

    """
    FFMPEG_LOGLEV = [("error (Show all errors)"),
                     ("warning (Show all warnings and errors)"),
                     ("info (Show informative messages during processing)"),
                     ("verbose (Same as `info`, except more verbose.)"),
                     ("debug (Show everything, including debugging info.)")
                     ]
    # -----------------------------------------------------------------

    def __init__(self, parent):
        """
        self.appdata: (dict) settings already loaded on the App
        self.confmanager: instance to ConfigManager class
        self.settings: (dict) current user settings from file conf.
        """
        get = wx.GetApp()
        self.appdata = get.appset
        self.confmanager = ConfigManager(self.appdata['fileconfpath'])
        self.settings = self.confmanager.read_options()

        if self.appdata['ostype'] == 'Windows':
            self.ffmpeg = 'ffmpeg.exe'
            self.ffprobe = 'ffprobe.exe'
        else:
            self.ffmpeg = 'ffmpeg'
            self.ffprobe = 'ffprobe'

        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)

        # ----------------------------set notebook
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        notebook = wx.Notebook(self, wx.ID_ANY, style=0)
        sizer_base.Add(notebook, 1, wx.ALL | wx.EXPAND, 5)

        # -----tab 1
        tabOne = wx.Panel(notebook, wx.ID_ANY)
        sizerGen = wx.BoxSizer(wx.VERTICAL)
        sizerGen.Add((0, 15))
        self.checkbox_logclr = wx.CheckBox(tabOne, wx.ID_ANY, (
                        _("Delete the contents of the log files\n"
                          "when exiting the application")))
        sizerGen.Add(self.checkbox_logclr, 0, wx.ALL, 5)
        sizerGen.Add((0, 15))
        self.checkbox_exit = wx.CheckBox(tabOne, wx.ID_ANY, (
                                         _("Warn on exit")))
        sizerGen.Add(self.checkbox_exit, 0, wx.ALL, 5)

        tabOne.SetSizer(sizerGen)
        notebook.AddPage(tabOne, _("Miscellanea"))

        # -----tab 2
        tabTwo = wx.Panel(notebook, wx.ID_ANY)
        sizerFiles = wx.BoxSizer(wx.VERTICAL)
        sizerFiles.Add((0, 15))
        msg = _("Where do you prefer to save your files?")
        labfile = wx.StaticText(tabTwo, wx.ID_ANY, msg)
        sizerFiles.Add(labfile, 0, wx.ALL | wx.EXPAND, 5)
        sizeFFdirdest = wx.BoxSizer(wx.HORIZONTAL)
        sizerFiles.Add(sizeFFdirdest, 0, wx.EXPAND)
        self.txt_outdir = wx.TextCtrl(tabTwo, wx.ID_ANY, "",
                                          style=wx.TE_READONLY
                                          )
        sizeFFdirdest.Add(self.txt_outdir, 1, wx.ALL, 5)
        self.txt_outdir.AppendText(self.appdata['outputfile'])

        self.btn_outdir = wx.Button(tabTwo, wx.ID_ANY, _("Browse.."))
        sizeFFdirdest.Add(self.btn_outdir, 0, wx.RIGHT |
                          wx.ALIGN_CENTER_VERTICAL |
                          wx.ALIGN_CENTER_HORIZONTAL, 5
                          )
        # sizerFiles.Add((0, 15))
        tabTwo.SetSizer(sizerFiles)
        notebook.AddPage(tabTwo, _("File"))

        # -----tab 3
        tabThree = wx.Panel(notebook, wx.ID_ANY)
        sizerFFmpeg = wx.BoxSizer(wx.VERTICAL)
        sizerFFmpeg.Add((0, 15))
        labFFexec = wx.StaticText(tabThree, wx.ID_ANY,
                                  _('Path to the executables'))
        sizerFFmpeg.Add(labFFexec, 0, wx.ALL | wx.EXPAND, 5)
        # ----
        self.checkbox_exeFFmpeg = wx.CheckBox(tabThree, wx.ID_ANY, (
                                _("Enable another location to run FFmpeg")))
        self.btn_pathFFmpeg = wx.Button(tabThree, wx.ID_ANY, _("Browse.."))
        self.txtctrl_ffmpeg = wx.TextCtrl(tabThree, wx.ID_ANY, "",
                                          style=wx.TE_READONLY
                                          )
        sizerFFmpeg.Add(self.checkbox_exeFFmpeg, 0, wx.ALL, 5)
        gridFFmpeg = wx.BoxSizer(wx.HORIZONTAL)
        sizerFFmpeg.Add(gridFFmpeg, 0, wx.EXPAND)
        gridFFmpeg.Add(self.txtctrl_ffmpeg, 1, wx.ALL, 5)
        gridFFmpeg.Add(self.btn_pathFFmpeg, 0, wx.RIGHT | wx.CENTER, 5)
        # ----
        self.checkbox_exeFFprobe = wx.CheckBox(tabThree, wx.ID_ANY, (
                                _("Enable another location to run FFprobe")))
        self.btn_pathFFprobe = wx.Button(tabThree, wx.ID_ANY, _("Browse.."))
        self.txtctrl_ffprobe = wx.TextCtrl(tabThree, wx.ID_ANY, "",
                                           style=wx.TE_READONLY
                                           )
        sizerFFmpeg.Add(self.checkbox_exeFFprobe, 0, wx.ALL, 5)
        gridFFprobe = wx.BoxSizer(wx.HORIZONTAL)
        sizerFFmpeg.Add(gridFFprobe, 0, wx.EXPAND)
        gridFFprobe.Add(self.txtctrl_ffprobe, 1, wx.ALL, 5)
        gridFFprobe.Add(self.btn_pathFFprobe, 0, wx.RIGHT | wx.CENTER, 5)
        # ----
        tabThree.SetSizer(sizerFFmpeg)
        notebook.AddPage(tabThree, _("FFmpeg"))

        # -----tab 5
        tabFive = wx.Panel(notebook, wx.ID_ANY)
        sizerAppearance = wx.BoxSizer(wx.VERTICAL)
        sizerAppearance.Add((0, 15))
        labTheme = wx.StaticText(tabFive, wx.ID_ANY, _('Icon themes'))
        sizerAppearance.Add(labTheme, 0, wx.ALL | wx.EXPAND, 5)
        self.cmbx_icons = wx.ComboBox(tabFive, wx.ID_ANY,
                                      choices=[
                                          ("Light"),
                                          ("Dark"),
                                          ("Colored"),
                                          ],
                                      size=(200, -1),
                                      style=wx.CB_DROPDOWN | wx.CB_READONLY
                                      )
        sizerAppearance.Add(self.cmbx_icons, 0,
                            wx.ALL |
                            wx.ALIGN_CENTER_HORIZONTAL, 5
                            )
        sizerAppearance.Add((0, 15))
        labTB = wx.StaticText(tabFive, wx.ID_ANY, _("Toolbar customization"))
        sizerAppearance.Add(labTB, 0, wx.ALL | wx.EXPAND, 5)
        tbchoice = [_('At the top of window (default)'),
                    _('At the bottom of window'),
                    _('At the right of window'),
                    _('At the left of window')]
        self.rdbTBpref = wx.RadioBox(tabFive, wx.ID_ANY,
                                     (_("Place the toolbar")),
                                     choices=tbchoice,
                                     majorDimension=1,
                                     style=wx.RA_SPECIFY_COLS
                                     )
        sizerAppearance.Add(self.rdbTBpref, 0, wx.ALL | wx.EXPAND, 5)

        gridTBsize = wx.FlexGridSizer(0, 2, 0, 5)
        sizerAppearance.Add(gridTBsize, 0, wx.ALL, 5)
        lab1_appearance = wx.StaticText(tabFive, wx.ID_ANY,
                                        _('Icon size:'))
        gridTBsize.Add(lab1_appearance, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.cmbx_iconsSize = wx.ComboBox(tabFive, wx.ID_ANY,
                                          choices=[("16"), ("24"), ("32"),
                                                   ("64")], size=(120, -1),
                                          style=wx.CB_DROPDOWN | wx.CB_READONLY
                                          )
        gridTBsize.Add(self.cmbx_iconsSize, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        if 'wx.svg' not in sys.modules:  # only in wx version 4.1 to up
            self.cmbx_iconsSize.Disable()
            lab1_appearance.Disable()

        self.checkbox_tbtext = wx.CheckBox(tabFive, wx.ID_ANY, (
                                _("Shows the text in the toolbar buttons")))
        sizerAppearance.Add(self.checkbox_tbtext, 0, wx.ALL, 5)

        tabFive.SetSizer(sizerAppearance)  # aggiungo il sizer su tab 4
        notebook.AddPage(tabFive, _("Appearance"))

        # -----tab 6
        tabSix = wx.Panel(notebook, wx.ID_ANY)
        sizerLog = wx.BoxSizer(wx.VERTICAL)
        sizerLog.Add((0, 15))

        msglog = _("The following settings affect output messages and\n"
                   "the log messages during transcoding processes.\n"
                   "Change only if you know what you are doing.\n")
        labLog = wx.StaticText(tabSix, wx.ID_ANY, (msglog))
        sizerLog.Add(labLog, 0, wx.ALL | wx.CENTRE, 5)
        self.rdbFFmpeg = wx.RadioBox(
                                tabSix, wx.ID_ANY,
                                ("Set logging level flags used by FFmpeg"),
                                choices=Setup.FFMPEG_LOGLEV, majorDimension=1,
                                style=wx.RA_SPECIFY_COLS
                                     )
        sizerLog.Add(self.rdbFFmpeg, 0, wx.ALL | wx.EXPAND, 5)
        tabSix.SetSizer(sizerLog)
        notebook.AddPage(tabSix, _("Logging levels"))
        # ------ btns bottom
        grdBtn = wx.GridSizer(1, 2, 0, 0)
        grdhelp = wx.GridSizer(1, 1, 0, 0)
        btn_help = wx.Button(self, wx.ID_HELP, "")
        grdhelp.Add(btn_help, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        grdBtn.Add(grdhelp)
        grdexit = wx.BoxSizer(wx.HORIZONTAL)
        btn_close = wx.Button(self, wx.ID_CANCEL, "")
        grdexit.Add(btn_close, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        btn_ok = wx.Button(self, wx.ID_OK, "")
        grdexit.Add(btn_ok, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        grdBtn.Add(grdexit, flag=wx.ALL | wx.ALIGN_RIGHT | wx.RIGHT, border=0)
        sizer_base.Add(grdBtn, 0, wx.EXPAND)
        # ------ set sizer
        #self.SetMinSize((550, -1))
        # print(self.GetSize())
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()

        # ----------------------Properties----------------------#
        self.SetTitle(_("FFcuesplitter-GUI Setup"))
        # set font
        if self.appdata['ostype'] == 'Darwin':
            labfile.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
            labcache.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
            labFFexec.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
            labTheme.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
            labTB.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
            labLog.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL))
        else:
            labfile.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
            labFFexec.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
            labTheme.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
            labTB.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
            labLog.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL))

        # ----------------------Binding (EVT)----------------------#
        self.Bind(wx.EVT_CHECKBOX, self.exit_warn, self.checkbox_exit)
        self.Bind(wx.EVT_CHECKBOX, self.clear_logs, self.checkbox_logclr)

        self.Bind(wx.EVT_BUTTON, self.on_output_path, self.btn_outdir)

        self.Bind(wx.EVT_CHECKBOX, self.exeFFmpeg, self.checkbox_exeFFmpeg)
        self.Bind(wx.EVT_BUTTON, self.open_path_ffmpeg, self.btn_pathFFmpeg)
        self.Bind(wx.EVT_CHECKBOX, self.exeFFprobe, self.checkbox_exeFFprobe)
        self.Bind(wx.EVT_BUTTON, self.open_path_ffprobe, self.btn_pathFFprobe)

        self.Bind(wx.EVT_COMBOBOX, self.on_Iconthemes, self.cmbx_icons)
        self.Bind(wx.EVT_RADIOBOX, self.on_toolbarPos, self.rdbTBpref)
        self.Bind(wx.EVT_COMBOBOX, self.on_toolbarSize, self.cmbx_iconsSize)
        self.Bind(wx.EVT_CHECKBOX, self.on_toolbarText, self.checkbox_tbtext)

        self.Bind(wx.EVT_RADIOBOX, self.logging_ffmpeg, self.rdbFFmpeg)

        self.Bind(wx.EVT_BUTTON, self.on_help, btn_help)
        self.Bind(wx.EVT_BUTTON, self.on_close, btn_close)
        self.Bind(wx.EVT_BUTTON, self.on_ok, btn_ok)
        # --------------------------------------------#
        self.current_settings()  # call function for initialize setting layout

    def current_settings(self):
        """
        Setting enable/disable in according to the configuration file

        """
        self.cmbx_icons.SetValue(str(self.appdata['icontheme']))
        self.cmbx_iconsSize.SetValue(str(self.appdata['toolbarsize']))
        self.rdbTBpref.SetSelection(int(self.appdata['toolbarpos']))

        for strs in range(self.rdbFFmpeg.GetCount()):
            if (self.appdata['ffmpegloglev'] in
               self.rdbFFmpeg.GetString(strs).split()[0]):
                self.rdbFFmpeg.SetSelection(strs)

        if self.appdata['ffmpeg_islocal'] is False:
            self.btn_pathFFmpeg.Disable()
            self.txtctrl_ffmpeg.Disable()
            self.txtctrl_ffmpeg.AppendText(self.appdata['ffmpeg_cmd'])
            self.checkbox_exeFFmpeg.SetValue(False)
        else:
            self.txtctrl_ffmpeg.AppendText(self.appdata['ffmpeg_cmd'])
            self.checkbox_exeFFmpeg.SetValue(True)

        if self.appdata['ffprobe_islocal'] is False:
            self.btn_pathFFprobe.Disable()
            self.txtctrl_ffprobe.Disable()
            self.txtctrl_ffprobe.AppendText(self.appdata['ffprobe_cmd'])
            self.checkbox_exeFFprobe.SetValue(False)
        else:
            self.txtctrl_ffprobe.AppendText(self.appdata['ffprobe_cmd'])
            self.checkbox_exeFFprobe.SetValue(True)

        if self.appdata['toolbartext'] == 'show':
            self.checkbox_tbtext.SetValue(True)
        else:
            self.checkbox_tbtext.SetValue(False)

        if self.appdata['clearlogfiles'] is True:
            self.checkbox_logclr.SetValue(True)
        else:
            self.checkbox_logclr.SetValue(False)

        if self.appdata['warnexiting'] is True:
            self.checkbox_exit.SetValue(True)
        else:
            self.checkbox_exit.SetValue(False)
    # --------------------------------------------------------------------#

    def on_output_path(self, event):
        """set up a custom user path for file export"""

        dlg = wx.DirDialog(self, _("Set a persistent location to save "
                                   "exported files"), "", wx.DD_DEFAULT_STYLE)

        if dlg.ShowModal() == wx.ID_OK:
            self.txt_outdir.Clear()
            getpath = self.appdata['getpath'](dlg.GetPath())
            self.txt_outdir.AppendText(getpath)
            self.settings['outputfile'] = getpath
            dlg.Destroy()
    # --------------------------------------------------------------------#

    def logging_ffmpeg(self, event):
        """specifies loglevel type for ffmpeg"""
        logg = self.rdbFFmpeg.GetStringSelection().split()[0]
        self.settings['ffmpegloglev'] = logg
    # --------------------------------------------------------------------#

    def exeFFmpeg(self, event):
        """Enable or disable ffmpeg local binary"""
        if self.checkbox_exeFFmpeg.IsChecked():
            self.btn_pathFFmpeg.Enable()
            self.txtctrl_ffmpeg.Enable()
            self.settings['ffmpeg_islocal'] = True
        else:
            self.btn_pathFFmpeg.Disable()
            self.txtctrl_ffmpeg.Disable()
            self.settings['ffmpeg_islocal'] = False

            status = detect_binaries(self.appdata['ostype'],
                                     self.ffmpeg,
                                     self.appdata['FFMPEG_pkg']
                                     )
            if status[0] == 'not installed':
                self.txtctrl_ffmpeg.Clear()
                self.txtctrl_ffmpeg.write(status[0])
                self.settings['ffmpeg_cmd'] = ''
            else:
                self.txtctrl_ffmpeg.Clear()
                getpath = self.appdata['getpath'](status[1])
                self.txtctrl_ffmpeg.write(getpath)
                self.settings['ffmpeg_cmd'] = getpath
    # --------------------------------------------------------------------#

    def open_path_ffmpeg(self, event):
        """Indicates a new ffmpeg path-name"""

        with wx.FileDialog(self, _("Choose the {} "
                                   "executable").format(self.ffmpeg), "", "",
                           f"ffmpeg binarys (*{self.ffmpeg})|*{self.ffmpeg}| "
                           f"All files (*.*)|*.*",
                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fdlg:

            if fdlg.ShowModal() == wx.ID_OK:
                if os.path.basename(fdlg.GetPath()) == self.ffmpeg:
                    self.txtctrl_ffmpeg.Clear()
                    getpath = self.appdata['getpath'](fdlg.GetPath())
                    self.txtctrl_ffmpeg.write(getpath)
                    self.settings['ffmpeg_cmd'] = getpath
    # --------------------------------------------------------------------#

    def exeFFprobe(self, event):
        """Enable or disable ffprobe local binary"""
        if self.checkbox_exeFFprobe.IsChecked():
            self.btn_pathFFprobe.Enable()
            self.txtctrl_ffprobe.Enable()
            self.settings['ffprobe_islocal'] = True

        else:
            self.btn_pathFFprobe.Disable()
            self.txtctrl_ffprobe.Disable()
            self.settings['ffprobe_islocal'] = False

            status = detect_binaries(self.appdata['ostype'],
                                     self.ffprobe,
                                     self.appdata['FFMPEG_pkg']
                                     )
            if status[0] == 'not installed':
                self.txtctrl_ffprobe.Clear()
                self.txtctrl_ffprobe.write(status[0])
                self.settings['ffprobe_cmd'] = ''
            else:
                self.txtctrl_ffprobe.Clear()
                getpath = self.appdata['getpath'](status[1])
                self.txtctrl_ffprobe.write(getpath)
                self.settings['ffprobe_cmd'] = getpath
    # --------------------------------------------------------------------#

    def open_path_ffprobe(self, event):
        """Indicates a new ffprobe path-name"""

        with wx.FileDialog(self, _("Choose the {} "
                                   "executable").format(self.ffprobe), "", "",
                           f"ffmpeg binarys "
                           f"(*{self.ffprobe})|*{self.ffprobe}| "
                           f"All files (*.*)|*.*",
                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fdlg:

            if fdlg.ShowModal() == wx.ID_OK:
                if os.path.basename(fdlg.GetPath()) == self.ffprobe:
                    self.txtctrl_ffprobe.Clear()
                    getpath = self.appdata['getpath'](fdlg.GetPath())
                    self.txtctrl_ffprobe.write(getpath)
                    self.settings['ffprobe_cmd'] = getpath
    # --------------------------------------------------------------------#

    def on_Iconthemes(self, event):
        """
        Set themes of icons
        """
        self.settings['icontheme'] = self.cmbx_icons.GetStringSelection()
    # --------------------------------------------------------------------#

    def on_toolbarSize(self, event):
        """
        Set the size of the toolbar buttons and the size of its icons
        """
        size = self.cmbx_iconsSize.GetStringSelection()
        self.settings['toolbarsize'] = size
    # --------------------------------------------------------------------#

    def on_toolbarPos(self, event):
        """
        Set toolbar position on main frame
        """
        self.settings['toolbarpos'] = self.rdbTBpref.GetSelection()
    # --------------------------------------------------------------------#

    def on_toolbarText(self, event):
        """
        Show or hide text along toolbar buttons
        """
        if self.checkbox_tbtext.IsChecked():
            self.settings['toolbartext'] = 'show'
        else:
            self.settings['toolbartext'] = 'hide'
    # --------------------------------------------------------------------#

    def exit_warn(self, event):
        """
        Enable or disable the warning message before
        exiting the program
        """
        if self.checkbox_exit.IsChecked():
            self.settings['warnexiting'] = True
        else:
            self.settings['warnexiting'] = False
    # --------------------------------------------------------------------#

    def clear_logs(self, event):
        """
        if checked, set to clear all log files on exit
        """
        if self.checkbox_logclr.IsChecked():
            self.settings['clearlogfiles'] = True
        else:
            self.settings['clearlogfiles'] = False
    # --------------------------------------------------------------------#

    def on_help(self, event):
        """
        Open default web browser via Python Web-browser controller.
        see <https://docs.python.org/3.8/library/webbrowser.html>
        """
        pass
        #if self.appdata['GETLANG'] in self.appdata['SUPP_LANGs']:
            #lang = self.appdata['GETLANG'].split('_')[0]
            #page = ('https://jeanslack.github.io/Videomass/Pages/User-guide-'
                    #'languages/%s/2-Startup_and_Setup_%s.pdf' % (lang, lang))
        #else:
            #page = ('https://jeanslack.github.io/Videomass/Pages/User-guide-'
                    #'languages/en/2-Startup_and_Setup_en.pdf')

        #webbrowser.open(page)
    # --------------------------------------------------------------------#

    def getvalue(self):
        """
        Get user preferences on exiting the app
        """

        if wx.MessageBox(_("Changes will take effect once the program "
                           "has been restarted.\n\n"
                           "Do you want to exit the application now?"),
                         _('Exit'),
                         wx.ICON_QUESTION
                         | wx.YES_NO, self) == wx.YES:
            return True

        return None
    # --------------------------------------------------------------------#

    def on_close(self, event):
        """
        Close event
        """
        event.Skip()
    # --------------------------------------------------------------------#

    def on_ok(self, event):
        """
        Applies all changes writing the new entries
        """
        self.confmanager.write_options(**self.settings)
        # self.Destroy() # WARNING on mac not close corretly, on linux ok
        event.Skip()
