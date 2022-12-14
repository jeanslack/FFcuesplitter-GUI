# -*- coding: UTF-8 -*-
"""
Name: ffmpeg_processing.py
Porpose: FFmpeg long processing task
Compatibility: Python3, wxPython4 Phoenix
Author: Gianluca Pernigotto <jeanlucperni@gmail.com>
Copyright: (c) 2022/2023 Gianluca Pernigotto <jeanlucperni@gmail.com>
license: GPL3
Rev: Feb.03.2022
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
from threading import Thread
import time
import itertools
import subprocess
import platform
from ffcuesplitter.utils import Popen
import wx
from pubsub import pub
if not platform.system() == 'Windows':
    import shlex


class Processing(Thread):
    """
    This class represents a separate thread for running
    ffmpeg processes, which need to read the stdout/stderr
    in real time.

    NOTE MS Windows:

    subprocess.STARTUPINFO()

    https://stackoverflow.com/questions/1813872/running-
    a-process-in-pythonw-with-popen-without-a-console?lq=1>

    NOTE capturing output in real-time (Windows, Unix):

    https://stackoverflow.com/questions/1388753/how-to-get-output-
    from-subprocess-popen-proc-stdout-readline-blocks-no-dat?rq=1

    """
    get = wx.GetApp()  # get wx.App attribute
    appdata = get.appset
    NOT_EXIST_MSG = _("Is 'ffmpeg' installed on your system?")
    # ---------------------------------------------------------------

    def __init__(self, args, duration, logname):
        """
        args: a list of [command/args]
        duration: a list of (durations)
        logname: absolute path name of the file log.

        Note that `args` and` duration` lists must be the
        same length.
        """
        self.stop_work_thread = False  # if True the process terminates
        self.args = args  # list of commands/aguments
        self.duration = duration  # duration list
        self.logname = logname  # path name of file log
        self.count = 0  # count for loop
        self.countmax = len(args)  # length commands/aguments list

        Thread.__init__(self)

        self.start()  # start the thread
    # --------------------------------------------------------------------#

    def run(self):
        """
        Subprocess initialize thread.
        """
        for (cmd,
             duration) in itertools.zip_longest(self.args,
                                                self.duration,
                                                fillvalue='',
                                                ):
            self.count += 1
            track = f'{self.count}/{self.countmax}'

            wx.CallAfter(pub.sendMessage,
                         "COUNT_EVT",
                         msg='',
                         end='',
                         )
            if not platform.system() == 'Windows':
                cmd = shlex.split(cmd)

            with open(self.logname, "w", encoding='utf-8') as log:
                log.write(f'\nCOMMAND: {cmd}')

                try:
                    with Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=log,
                               bufsize=1,
                               encoding='utf8',
                               universal_newlines=True) as proc:
                        for line in proc.stdout:
                            if "out_time_ms" in line.strip():
                                wx.CallAfter(pub.sendMessage,
                                             "UPDATE_EVT",
                                             output=line,
                                             duration=duration,
                                             track=track,
                                             status=0,
                                             )
                            if self.stop_work_thread:
                                proc.terminate()
                                break  # break second 'for' loop

                        if proc.wait():  # error
                            wx.CallAfter(pub.sendMessage,
                                         "UPDATE_EVT",
                                         output='',
                                         duration=duration,
                                         track='',
                                         status=proc.wait(),
                                         )
                except (OSError, FileNotFoundError) as err:
                    excepterr = f"{err}\n  {Processing.NOT_EXIST_MSG}"
                    log.write(f'\nERROR: {excepterr}')
                    wx.CallAfter(pub.sendMessage,
                                 "COUNT_EVT",
                                 msg=excepterr,
                                 end='error',
                                 )
                    break

                if self.stop_work_thread:
                    proc.terminate()
                    break  # break second 'for' loop

        time.sleep(.5)
        wx.CallAfter(pub.sendMessage, "END_EVT")
    # --------------------------------------------------------------------#

    def stop(self):
        """
        Sets the stop work thread to terminate the process
        """
        self.stop_work_thread = True
