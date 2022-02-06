# -*- coding: UTF-8 -*-
"""
Name: cuesplitter_panel.py
Porpose: main ffcuesplitter panel interface
Compatibility: Python3, wxPython Phoenix
Author: Gianluca Pernigotto <jeanlucperni@gmail.com>
Copyright: (c) 2022/2023 Gianluca Pernigotto <jeanlucperni@gmail.com>
license: GPL3
Rev: Feb.04.2022
Code checker: flake8, pylint
########################################################

This file is part of Cuesplitter-GUI.

   Cuesplitter-GUI is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   Cuesplitter-GUI is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with Cuesplitter-GUI.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import shutil
import tempfile
import datetime
import wx
import wx.lib.scrolledpanel as scrolled
import wx.lib.mixins.listctrl as listmix
from pubsub import pub
from ffcuesplitter.cuesplitter import FFCueSplitter
from ffcuesplitter_gui._utils.utils import get_codec_quality_items
from ffcuesplitter_gui._threads.ffmpeg_processing import Processing
from ffcuesplitter_gui._dialogs.widget_utils import notification_area
from ffcuesplitter_gui._utils.utils import move_files_to_outputdir


if not hasattr(wx, 'EVT_LIST_ITEM_CHECKED'):
    # import wx.lib.mixins.listctrl as listmix

    class TestListCtrl(wx.ListCtrl,
                       listmix.CheckListCtrlMixin,
                       listmix.ListCtrlAutoWidthMixin
                       ):
        """
        This is listctrl with a checkbox for each row in list.
        It work on both wxPython==4.1.? and wxPython<=4.1.? (e.g. 4.0.7).
        Since wxPython <= 4.0.7 has no attributes for fcode.EnableCheckBoxes
        and the 'wx' module does not have attributes 'EVT_LIST_ITEM_CHECKED',
        'EVT_LIST_ITEM_UNCHECKED' for binding, this class maintains backward
        compatibility.
        """
        def __init__(self,
                     parent,
                     _id,
                     pos=wx.DefaultPosition,
                     size=wx.DefaultSize,
                     style=0
                     ):
            self.parent = parent
            wx.ListCtrl.__init__(self, parent, _id, pos, size, style)
            listmix.CheckListCtrlMixin.__init__(self)
            listmix.ListCtrlAutoWidthMixin.__init__(self)
            # self.setResizeColumn(3)


class CueGui(wx.Panel):
    """
    This Represents the main panel for ffcuesplitter-gui
    """
    def __init__(self, parent):
        """
        The first item of the self.info is a complete list of all
        informations getting by extract_info method from youtube_dl
        module.
        """
        self.parent = parent
        get = wx.GetApp()
        self.appdata = get.appset
        self.thread_type = None  # the instantiated thread
        self.abort = False  # if True set to abort current process
        self.error = False  # if True set to error current process
        self.data = None  # it is the ffcuesplitter instance
        self.oldwx = None  # test result of hasattr EVT_LIST_ITEM_CHECKED
        self.tmpdir = None

        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)

        sizer_base = wx.BoxSizer(wx.VERTICAL)
        sizer_div = wx.BoxSizer(wx.HORIZONTAL)
        sizer_base.Add(sizer_div, 1, wx.EXPAND)
        boxoptions = wx.StaticBoxSizer(wx.StaticBox(
            self, wx.ID_ANY, ('')), wx.VERTICAL)
        sizer_div.Add(boxoptions, 0, wx.ALL | wx.EXPAND, 5)
        boxlistctrl = wx.StaticBoxSizer(wx.StaticBox(
            self, wx.ID_ANY, ('')), wx.VERTICAL)
        sizer_div.Add(boxlistctrl, 1, wx.ALL | wx.EXPAND, 5)

        boxoptions.Add((5, 5))
        panelscroll = scrolled.ScrolledPanel(self, -1, size=(220, 600),
                                             style=wx.TAB_TRAVERSAL
                                             | wx.BORDER_THEME,
                                             name="panelscr",
                                             )
        fgs1 = wx.BoxSizer(wx.VERTICAL)
        # fgs1.Add((5, 5))
        self.lbl_formats = wx.StaticText(panelscroll,
                                         wx.ID_ANY,
                                         label=_("Format:")
                                         )
        fgs1.Add(self.lbl_formats, 0, wx.ALL | wx.EXPAND, 5)
        self.cmbx_formats = wx.ComboBox(panelscroll, wx.ID_ANY,
                                        choices=(('wav', 'flac',
                                                  'mp3', 'ogg')),
                                        size=(-1, -1), style=wx.CB_DROPDOWN
                                        | wx.CB_READONLY
                                        )
        fgs1.Add(self.cmbx_formats, 0, wx.ALL | wx.EXPAND, 5)
        self.cmbx_formats.SetSelection(1)
        self.lbl_quality = wx.StaticText(panelscroll,
                                         wx.ID_ANY,
                                         label=_("Compression:")
                                         )
        fgs1.Add(self.lbl_quality, 0, wx.ALL | wx.EXPAND, 5)

        items = get_codec_quality_items(self.cmbx_formats.GetValue())
        self.cmbx_quality = wx.ComboBox(panelscroll, wx.ID_ANY,
                                        choices=(list(items.keys())),
                                        size=(-1, -1), style=wx.CB_DROPDOWN
                                        | wx.CB_READONLY
                                        )
        self.cmbx_quality.SetSelection(6)
        # grid_v.Add((20, 20), 0,)
        fgs1.Add(self.cmbx_quality, 0, wx.ALL | wx.EXPAND, 5)

        self.ckbx_codec_copy = wx.CheckBox(panelscroll, wx.ID_ANY,
                                           (_('Copy codec (very fast)'))
                                           )
        fgs1.Add(self.ckbx_codec_copy, 0, wx.ALL, 5)
        line1 = wx.StaticLine(panelscroll, wx.ID_ANY, pos=wx.DefaultPosition,
                              size=wx.DefaultSize, style=wx.LI_HORIZONTAL,
                              name=wx.StaticLineNameStr
                              )
        fgs1.Add(line1, 0, wx.ALL | wx.EXPAND, 10)
        lbl_outdir = wx.StaticText(panelscroll,
                                   wx.ID_ANY,
                                   label=_("Directory:")
                                   )
        fgs1.Add(lbl_outdir, 0, wx.ALL | wx.EXPAND, 5)
        sizer_outdir = wx.BoxSizer(wx.HORIZONTAL)
        fgs1.Add(sizer_outdir, 0, wx.EXPAND | wx.ALL, 5)
        self.btn_out = wx.Button(panelscroll, wx.ID_ANY, "...", size=(35, -1))
        self.txt_out = wx.TextCtrl(panelscroll,
                                   wx.ID_ANY,
                                   f"{self.appdata['outputfile']}",
                                   style=wx.TE_PROCESS_ENTER
                                   | wx.TE_READONLY
                                   )
        sizer_outdir.Add(self.txt_out, 1, wx.RIGHT | wx.EXPAND, 2)
        sizer_outdir.Add(self.btn_out, 0, wx.LEFT
                         | wx.ALIGN_CENTER_HORIZONTAL
                         | wx.ALIGN_CENTER_VERTICAL, 2
                         )
        boxoptions.Add(panelscroll, 0, wx.ALL | wx.CENTRE, 0)

        panelscroll.SetSizer(fgs1)
        panelscroll.SetAutoLayout(1)
        panelscroll.SetupScrolling()

        # -------------listctrl
        if hasattr(wx, 'EVT_LIST_ITEM_CHECKED'):
            self.oldwx = False
            self.tlist = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT
                                     | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL
                                     )
        else:
            self.oldwx = True
            t_id = wx.NewIdRef()
            self.tlist = TestListCtrl(self, t_id, style=wx.LC_REPORT
                                      | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL
                                      )
        boxlistctrl.Add(self.tlist, 1, wx.ALL | wx.EXPAND, 5)
        self.tlist.InsertColumn(0, (_('Track')), width=60)
        self.tlist.InsertColumn(1, (_('Artist')), width=130)
        self.tlist.InsertColumn(2, (_('Title')), width=130)
        self.tlist.InsertColumn(3, (_('Length')), width=80)
        self.tlist.InsertColumn(4, (_('Album')), width=180)

        sizer_cuefile = wx.BoxSizer(wx.HORIZONTAL)
        sizer_base.Add(sizer_cuefile, 0, wx.EXPAND | wx.ALL, 5)
        self.btn_import = wx.Button(self, wx.ID_OPEN, "...", size=(35, -1))
        self.txt_path_cue = wx.TextCtrl(self, wx.ID_ANY, "*.cue",
                                        style=wx.TE_PROCESS_ENTER |
                                        wx.TE_READONLY
                                        )
        sizer_cuefile.Add(self.txt_path_cue, 1, wx.RIGHT | wx.EXPAND, 2)
        sizer_cuefile.Add(self.btn_import, 0, wx.LEFT
                          | wx.ALIGN_CENTER_HORIZONTAL
                          | wx.ALIGN_CENTER_VERTICAL, 2
                          )

        self.barprog = wx.Gauge(self, wx.ID_ANY, range=0)
        sizer_base.Add(self.barprog, 0, wx.EXPAND | wx.ALL, 5)

        if self.appdata['ostype'] == 'Darwin':
            self.SetMinSize((980, 570))
        elif self.appdata['ostype'] == 'Windows':
            self.SetMinSize((920, 640))
        else:
            self.SetMinSize((800, 550))

        self.SetSizer(sizer_base)
        self.Layout()

        # ----------------------Binder (EVT)----------------------#
        self.Bind(wx.EVT_BUTTON, self.on_import_cuefile, self.btn_import)
        self.Bind(wx.EVT_BUTTON, self.on_output_dir, self.btn_out)

        self.Bind(wx.EVT_COMBOBOX, self.on_formats, self.cmbx_formats)
        self.Bind(wx.EVT_CHECKBOX, self.on_codec_copy, self.ckbx_codec_copy)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select, self.tlist)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_deselect, self.tlist)
    # -----------------------------------------------------------------#
        pub.subscribe(self.update_progress_bar, "UPDATE_EVT")
        pub.subscribe(self.update_count_items, "COUNT_EVT")
        pub.subscribe(self.end_processing, "END_EVT")
        # ---------------------------------------- #

    def on_output_dir(self, event):
        """
        Set output Directory. Note that this function set
        a new path on self.appdata['outputfile'] as well.

        """
        if self.txt_path_cue.GetValue() == '*.cue':
            txt = self.appdata['outputfile']
        else:
            txt = os.path.dirname(self.txt_path_cue.GetValue())

        dlg = wx.DirDialog(self, message=_("Set a destination folder"),
                           defaultPath=txt,
                           style=wx.DD_DEFAULT_STYLE)

        if dlg.ShowModal() == wx.ID_OK:
            self.txt_out.Clear()
            getpath = self.appdata['getpath'](dlg.GetPath())  # relativize
            self.appdata['outputfile'] = getpath
            self.txt_out.AppendText(getpath)
            dlg.Destroy()
    # -----------------------------------------------------------------#

    def on_import_cuefile(self, event):
        """
        file *.cue importing dialog
        """
        wildcard = "Source (*.cue;*.CUE)|*.cue;*.CUE|All files (*.*)|*.*"

        with wx.FileDialog(self, _("Open a CUE sheet"),
                           "", "", wildcard, wx.FD_OPEN |
                           wx.FD_FILE_MUST_EXIST) as filedlg:

            if filedlg.ShowModal() == wx.ID_CANCEL:
                return

            newincoming = filedlg.GetPath()
        self.txt_path_cue.SetValue(newincoming)

        self.data = FFCueSplitter(newincoming,
                                  ffprobe_cmd=self.appdata['ffprobe_cmd'],
                                  ffmpeg_cmd=self.appdata['ffmpeg_cmd'],
                                  ffmpeg_loglevel=self.appdata['ffmpegloglev'],
                                  progress_meter='tqdm'
                                  )  # instance
        try:
            self.data.open_cuefile()
        except Exception as err:
            wx.MessageBox(f'{err}', "Cuesplitter-GUI", wx.ICON_ERROR, self)
            return

        self.set_data_list_ctrl()
    # -----------------------------------------------------------------#

    def set_data_list_ctrl(self):
        """
        Set data on listctrl
        """
        self.tlist.DeleteAllItems()
        if self.oldwx is False:
            self.tlist.EnableCheckBoxes(enable=True)

        for num, item in enumerate(self.data.audiotracks):
            self.tlist.InsertItem(num, item.get('TRACK_NUM', 'N/A'))
            self.tlist.SetItem(num, 1, item.get('PERFORMER', 'N/A'))
            self.tlist.SetItem(num, 2, item.get('TITLE', 'N/A'))
            dur = item.get('DURATION', '')
            sec = str(datetime.timedelta(seconds=dur))[2:7]
            self.tlist.SetItem(num, 3, sec)
            self.tlist.SetItem(num, 4, item.get('ALBUM', 'N/A'))
            self.tlist.CheckItem(num, check=True)

        self.parent.toolbar.EnableTool(12, True)  # start
        self.parent.toolbar.EnableTool(8, True)  # audio CD
        self.parent.toolbar.EnableTool(14, False)  # track tag
        self.parent.statusbar_msg(_("Ready"))
    # -----------------------------------------------------------------#

    def on_formats(self, event):
        """
        Audio format selection
        """
        items = get_codec_quality_items(self.cmbx_formats.GetValue())
        self.cmbx_quality.Clear()
        self.cmbx_quality.Append((list(items.keys())),)
        if self.cmbx_formats.GetValue() == 'wav':
            self.cmbx_quality.SetSelection(0)
        elif self.cmbx_formats.GetValue() == 'flac':
            self.cmbx_quality.SetSelection(6)
        elif self.cmbx_formats.GetValue() == 'mp3':
            self.cmbx_quality.SetSelection(3)
        elif self.cmbx_formats.GetValue() == 'ogg':
            self.cmbx_quality.SetSelection(5)
    # -----------------------------------------------------------------#

    def on_codec_copy(self, event):
        """
        Set copy the source audio codec
        """
        if self.ckbx_codec_copy.IsChecked():
            self.cmbx_formats.Disable()
            self.cmbx_quality.Disable()
            self.lbl_quality.Disable()
            self.lbl_formats.Disable()
        else:
            self.cmbx_formats.Enable()
            self.cmbx_quality.Enable()
            self.lbl_quality.Enable()
            self.lbl_formats.Enable()
    # -----------------------------------------------------------------#

    def on_select(self, event):
        """
        self.fcod selection event that enables btn_play
        """
        self.parent.toolbar.EnableTool(14, True)
    # ----------------------------------------------------------------------

    def on_deselect(self, event):
        """
        self.fcod de-selection event that disables btn_play
        """
        self.parent.toolbar.EnableTool(14, False)
    # ----------------------------------------------------------------------

    def update_attributes_of_ffcuesplitter_api(self, tmpdir):
        """
        Set required arguments on ffcuesplitter API
        """
        self.data.kwargs['ffmpeg_cmd'] = self.appdata['ffmpeg_cmd']
        self.data.kwargs['ffmpeg_loglevel'] = self.appdata['ffmpegloglev']
        self.data.kwargs['outputdir'] = self.appdata['outputfile']
        self.data.kwargs['tempdir'] = tmpdir

        if self.ckbx_codec_copy.IsChecked() is True:
            self.data.kwargs['ffmpeg_add_params'] = ""
            self.data.kwargs['format'] = 'copy'
        else:
            self.data.kwargs['format'] = self.cmbx_formats.GetValue()
            items = get_codec_quality_items(self.cmbx_formats.GetValue())
            compression = items[self.cmbx_quality.GetValue()]
            self.data.kwargs['ffmpeg_add_params'] = compression

        self.data.kwargs['suffix'] = self.cmbx_formats.GetValue()
    # ----------------------------------------------------------------------

    def on_start(self):
        """
        Create thread instance.
        """
        self.tmpdir = tempfile.mkdtemp(suffix=None,
                                       prefix='FFcuesplitterGUI_',
                                       dir=None)
        self.update_attributes_of_ffcuesplitter_api(self.tmpdir)  # set all
        args = self.data.ffmpeg_arguments()  # get command/arguments list

        if self.oldwx is False:
            check = self.tlist.IsItemChecked
        else:
            check = self.tlist.IsChecked

        count = self.tlist.GetItemCount()
        indexes = [x for x in range(count) if not check(x)]
        if indexes:
            for index in sorted(indexes, reverse=True):
                args['arguments'].pop(index)
                args['seconds'].pop(index)

        self.parent.toolbar.EnableTool(13, True)  # stop
        self.parent.toolbar.EnableTool(12, False)  # start
        self.parent.toolbar.EnableTool(5, False)  # setup

        logfile = os.path.join(self.appdata['logdir'], 'ffmpeg.log')
        self.thread_type = Processing(args['arguments'],
                                      args['seconds'],
                                      logfile
                                      )
    # ----------------------------------------------------------------------

    def on_stop(self, event):
        """
        The user changes his mind and wants to abort
        the ongoing process.
        """
        self.abort = True
        self.thread_type.stop()
        self.parent.statusbar_msg(_("wait... I'm aborting"),
                                  'GOLDENROD',
                                  'BLACK')
        self.thread_type.join()
    # ----------------------------------------------------------------------

    def update_progress_bar(self, output, duration, track, status):
        """
        Update progress bar by receving ffmpeg stdout pipe on
        thread loop. If `status` is not 0 means an error is
        occurred. This is usually a syntax error in the command
        arguments passed to the FFmpeg command.
        """
        if not status == 0:
            self.error = True
            return

        secs = round(int(output.split('=')[1]) / 1_000_000)
        percent = secs / round(duration) * 100
        msg = _("Processing Track: {} | Status "
                "Progress: {}%".format(track, round(percent)))
        self.barprog.SetValue(percent)
        self.parent.statusbar_msg(msg, fgrd='ORANGE RED')
    # ----------------------------------------------------------------------

    def update_count_items(self, msg, end):
        """
        Counts occurences for each loop and sets barprog range
        to max percentage starting to 0 (min) value. Note that
        when `msg` argument is equal to str('error') it means
        that an exception is raised by thread with one of the
        exceptions of class OSError or FileNotFoundError.
        """
        if end == 'error':  # This error is given by Exceptions
            self.error = True
            wx.MessageBox(f'{msg}', "Cuesplitter-GUI", wx.ICON_ERROR, self)
        else:
            self.barprog.SetRange(100)  # set overall percentage range
            self.barprog.SetValue(0)  # reset bar progress start to 0
    # ----------------------------------------------------------------------

    def end_processing(self):
        """
        At the end of the process
        """
        if self.abort is True:
            self.parent.statusbar_msg(_("...Interrupted"),
                                      'BLUE VIOLET', 'WHITE')
        elif self.error is True:
            self.parent.statusbar_msg(_("ERROR: See Log for Details"),
                                      'RED', 'WHITE')
            notification_area(_("ERROR!"), _("An error has occurred."),
                              wx.ICON_ERROR)
        else:
            move_files_to_outputdir(self.data.kwargs['outputdir'],
                                    self.data.kwargs['tempdir'])
            self.parent.statusbar_msg(_("...Finished!"),
                                      'DARK GREEN', 'WHITE')
            notification_area(_('Success!'), _("Get your files at the "
                                               "destination specified"),
                              wx.ICON_INFORMATION)
            self.barprog.SetValue(0)

        self.parent.toolbar.EnableTool(13, False)  # stop
        self.parent.toolbar.EnableTool(12, True)  # start
        self.parent.toolbar.EnableTool(5, True)  # setup
        self.thread_type = None
        self.abort = False
        self.error = False

        shutil.rmtree(self.tmpdir, ignore_errors=True)
    # ----------------------------------------------------------------------
