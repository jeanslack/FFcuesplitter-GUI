# -*- coding: UTF-8 -*-
"""
Name: utils.py
Porpose: It groups useful functions that are called several times
Compatibility: Python3, wxPython Phoenix
Author: Gianluca Pernigotto <jeanlucperni@gmail.com>
Copyright: (c) 2022 Gianluca Pernigotto <jeanlucperni@gmail.com>
license: GPL3
Rev: Feb.03.2022
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
import shutil
import os
import wx



def move_files_to_outputdir(outputdir, tmpdir):
    """
    All files are processed in a /temp folder. After the split
    operation is complete, all tracks are moved from /temp folder
    to output folder. Here evaluates what to do if files already
    exists on output folder.
    """
    ask = True
    overwrite = True

    for track in os.listdir(tmpdir):
        fdir = os.path.join(outputdir, track)
        ftmp = os.path.join(tmpdir, track)
        if os.path.exists(fdir) and ask is True:
            dlg = wx.MessageDialog(None, _('File already exists:\n"{}"\n\n'
                                           'Do you want to overwrite all '
                                           'files?').format(fdir),
                                   _("Warning"),
                                   wx.ICON_WARNING
                                   | wx.YES_NO
                                   | wx.CANCEL).ShowModal()
            if dlg == wx.ID_YES:
                ask = False
                overwrite = True
            elif dlg == wx.ID_NO:
                overwrite = False
                continue
            else:
                return

        if overwrite is True:
            try:
                shutil.move(ftmp, fdir)
            except Exception as error:
                wx.MessageBox(f'{error}', "Cuesplitter-GUI",
                              wx.ICON_ERROR, None)
# ----------------------------------------------------------------#


def get_codec_quality_items(_format_):
    """
    Given an audio format, it returns the corresponding
    audio compression references,if available.
    """
    qualities = {'wav':
                     {"Auto": ""},
                 'flac':
                     {"Auto": "",
                      "very high quality": "-compression_level 0",
                      "quality 1": "-compression_level 1" ,
                      "quality 2": "-compression_level 2",
                      "quality 3": "-compression_level 3",
                      "quality 4": "-compression_level 4",
                      "Standard quality": "-compression_level 5",
                      "quality 6": "-compression_level 6",
                      "quality 7": "-compression_level 7",
                      "low quality": "-compression_level 8"
                          },
                 'ogg':
                     {"Auto": "",
                     "very poor quality": "-aq 1",
                     "VBR 92 kbit/s": "-aq 2",
                     "VBR 128 kbit/s": "-aq 3",
                     "VBR 160 kbit/s": "-aq 4",
                     "VBR 175 kbit/s": "-aq 5",
                     "VBR 192 kbit/s": "-aq 6",
                     "VBR 220 kbit/s": "-aq 7",
                     "VBR 260 kbit/s": "-aq 8",
                     "VBR 320 kbit/s": "-aq 9",
                     "very good quality": "-aq 10"
                         },
                 'mp3':
                     {"Auto": "",
                     "VBR 128 kbit/s (low quality)": "-b:a 128k",
                     "VBR 160 kbit/s": "-b:a 160k",
                     "VBR 192 kbit/s": "-b:a 192k",
                     "VBR 260 kbit/s": "-b:a 260k",
                     "CBR 320 kbit/s (very good quality)": "-b:a 320k"
                         }}
    return qualities[_format_]
# ------------------------------------------------------------------------


def del_filecontents(filename):
    """
    Delete the contents of the file if it is not empty.
    Please be careful as it assumes the file exists.

    USAGE:

        if fileExists is True:
            try:
                del_filecontents(logfile)
            except Exception as err:
                print("Unexpected error while deleting "
                      "file contents:\n\n{0}").format(err)

    MODE EXAMPLE SCHEME:

    |          Mode          |  r   |  r+  |  w   |  w+  |  a   |  a+  |
    | :--------------------: | :--: | :--: | :--: | :--: | :--: | :--: |
    |          Read          |  +   |  +   |      |  +   |      |  +   |
    |         Write          |      |  +   |  +   |  +   |  +   |  +   |
    |         Create         |      |      |  +   |  +   |  +   |  +   |
    |         Cover          |      |      |  +   |  +   |      |      |
    | Point in the beginning |  +   |  +   |  +   |  +   |      |      |
    |    Point in the end    |      |      |      |      |  +   |  +   |

    """
    with open(filename, "r+", encoding='utf8') as fname:
        content = fname.read()
        if content:
            fname.flush()  # clear previous content readed
            fname.seek(0)  # it places the file pointer to position 0
            fname.write("")
            fname.truncate()  # truncates the file to the current file point.
# ------------------------------------------------------------------#


def detect_binaries(platform, executable, additionaldir=None):
    """
    <https://stackoverflow.com/questions/11210104/check-if
    -a-program-exists-from-a-python-script>

    Given an executable name (binary), find it on the O.S.
    via which function, if not found try to find it on the
    optional `additionaldir` .

        If both failed, return ('not installed', None)
        If found on the O.S., return (None, executable)
        If found on the additionaldir, return ('provided', executable).

    platform = platform name get by `platform.system()`
    executable = name of executable without extension
    additionaldir = additional dirname to perform search

    """
    local = False

    if shutil.which(executable):
        installed = True

    else:
        if platform == 'Windows':
            installed = False

        elif platform == 'Darwin':

            if os.path.isfile(f"/usr/local/bin/{executable}"):
                local = True
                installed = True
            else:
                local = False
                installed = False

        else:  # Linux, FreeBSD, etc.
            installed = False

    if not installed:

        if additionaldir:  # check onto additionaldir

            if not os.path.isfile(os.path.join(f"{additionaldir}", "bin",
                                               f"{executable}")):
                provided = False

            else:
                provided = True

            if not provided:
                return 'not installed', None
            # only if ffmpeg is not installed, offer it if found
            return 'provided', os.path.join(f"{additionaldir}",
                                            "bin", f"{executable}")
        return 'not installed', None

    if local:  # only for MacOs
        return None, f"/usr/local/bin/{executable}"
    return None, shutil.which(executable)
