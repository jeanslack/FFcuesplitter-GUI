# -*- coding: UTF-8 -*-
"""
Name: settings_manager.py
Porpose: Set FFcuesplitter-gui configuration on startup
Compatibility: Python3
Author: Gianluca Pernigotto <jeanlucperni@gmail.com>
Copyright: (c) 2022/2023 Gianluca Pernigotto <jeanlucperni@gmail.com>
license: GPL3
Rev: Jan.30.2022
Code checker: flake8, pylint .

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
import sys
import site
import shutil
import json
import platform


class ConfigManager:
    """
    It represents the setting of the configuration file
    in its read and write aspects.
    """
    VERSION = 4.0
    DEFAULT_OPTIONS = {
        "confversion": VERSION,
        "outputfile": f"{os.path.expanduser('~')}",
        "ffmpeg_cmd": "",
        "ffmpeg_islocal": False,
        "ffmpegloglev": "info",
        "ffprobe_cmd": "",
        "ffprobe_islocal": False,
        "warnexiting": True,
        "clearlogfiles": False,
        "icontheme": "Colored",
        "toolbarsize": 24,
        "toolbarpos": 0,
        "toolbartext": "show"
        }

    def __init__(self, file_path):
        """
        Set file configuration path name
        """
        self.file_path = file_path

    def write_options(self, **options):
        """
        Writes options to configuration file.
        """
        if options:
            set_options = options
        else:
            set_options = ConfigManager.DEFAULT_OPTIONS

        with open(self.file_path, "w", encoding='utf-8') as settings_file:

            json.dump(set_options,
                      settings_file,
                      indent=4,
                      separators=(",", ": ")
                      )

    def read_options(self):
        """
        Reads options from configuration file
        """
        with open(self.file_path, 'r', encoding='utf-8') as settings_file:
            try:
                options = json.load(settings_file)
            except json.JSONDecodeError:
                return None

        return options


def get_options(dirconf, file_path):
    """
    Check application options. Reads the `settings.json` file; if
    it does not exist or is unreadable or its version is different,
    try to restore it. If `dirconf` does not exist try to restore
    both `dirconf` and `settings.json`

    Return dict key == 'R', else return a dict key == ERROR
    """
    conf = ConfigManager(file_path)
    version = ConfigManager.VERSION

    if os.path.exists(dirconf):
        if os.path.isfile(file_path):
            data = {'R': conf.read_options()}
            if not data['R']:
                conf.write_options()
                data = {'R': conf.read_options()}
            if float(data['R']['confversion']) != version:  # conf version
                new = conf.options  # model
                data = {'R': {**data['R'], **new}}
                conf.write_options(**data['R'])
        else:
            conf.write_options()
            data = {'R': conf.read_options()}

    else:  # try to restore entire configuration directory
        try:  # make conf folder
            os.mkdir(dirconf, mode=0o777)
        except (OSError, TypeError) as err:
            data = {'ERROR': err}
        else:
            conf.write_options()
            data = {'R': conf.read_options()}

    return data


def get_pyinstaller():
    """
    Get pyinstaller-based package attributes to determine
    how to use sys.executable
    When a bundled app starts up, the bootloader sets the sys.frozen
    attribute and stores the absolute path to the bundle folder
    in sys._MEIPASS.
    For a one-folder bundle, this is the path to that folder.
    For a one-file bundle, this is the path to the temporary folder
    created by the bootloader.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        frozen, meipass = True, True
        mpath = getattr(sys, '_MEIPASS', os.path.abspath(__file__))
        data_locat = mpath

    else:
        frozen, meipass = False, False
        mpath = os.path.realpath(os.path.abspath(__file__))
        data_locat = os.path.dirname(os.path.dirname(mpath))

    return frozen, meipass, mpath, data_locat


def conventional_paths():
    """
    Establish the conventional paths based on OS

    """
    user = os.path.expanduser('~')

    if platform.system() == 'Windows':
        fpath = "\\AppData\\Roaming\\ffcuesplitter_gui\\settings.json"
        file_conf = os.path.join(user + fpath)
        dir_conf = os.path.join(user + "\\AppData\\Roaming\\ffcuesplitter_gui")
        log_dir = os.path.join(dir_conf, 'log')  # logs

    elif platform.system() == "Darwin":
        fpath = "Library/Application Support/ffcuesplitter_gui/settings.json"
        file_conf = os.path.join(user, fpath)
        dir_conf = os.path.join(user, os.path.dirname(fpath))
        log_dir = os.path.join(user, "Library/Logs/ffcuesplitter_gui")

    else:  # Linux, FreeBsd, etc.
        fpath = ".config/ffcuesplitter_gui/settings.json"
        file_conf = os.path.join(user, fpath)
        dir_conf = os.path.join(user, ".config/ffcuesplitter_gui")
        log_dir = os.path.join(user, ".local/share/ffcuesplitter_gui/log")

    return file_conf, dir_conf, log_dir


def portable_paths(portdir):
    """
    Make portable-data paths based on OS

    """
    if platform.system() == 'Windows':
        file_conf = portdir + "\\portable_data\\settings.json"
        dir_conf = portdir + "\\portable_data"
        log_dir = os.path.join(dir_conf, 'log')  # logs
    else:
        file_conf = portdir + "/portable_data/settings.json"
        dir_conf = portdir + "/portable_data"
        log_dir = os.path.join(dir_conf, 'log')  # logs

    return file_conf, dir_conf, log_dir


def get_outdir(outdir, relpath, apptype):
    """
    Set default or user-custom output folders
    """
    if not outdir:
        outputdir = outdir
    elif relpath is True:
        appdir = (os.path.dirname(sys.prefix) if
                  apptype == 'embed' else os.getcwd())
        outputdir = os.path.relpath(os.path.join(appdir, 'My_Files'))

        if not os.path.exists(outputdir):
            try:  # make a files folder
                os.mkdir(outputdir, mode=0o777)
            except OSError as err:
                return None, err
            except TypeError as err:
                return None, err
    else:
        outputdir = os.path.expanduser('~')

    return outputdir, None


def msg(arg):
    """
    print logging messages during startup
    """
    print('Info:', arg)


class DataSource():
    """
    This class represents the start-up configuration for
    the following packaging methods:
        - As script launched by launcher.py file
        - Python package by PyPi (cross-platform, multiuser/user)
        - Linux's distributions packaging (multiuser)
        - Bundled app by pyinstaller (windowed for MacOs and Windows)
        - AppImage for Linux (user)

        * multiuser: root installation
        * user: local installation

    """
    FROZEN, MEIPASS, MPATH, DATA_LOCAT = get_pyinstaller()
    portdirname = os.path.dirname(sys.executable)
    portdir = os.path.join(portdirname, 'portable_data')

    if FROZEN and MEIPASS and os.path.isdir(portdir):
        # if portdir is true, make application really portable
        FILE_CONF, DIR_CONF, LOG_DIR = portable_paths(portdirname)
        RELPATH = platform.system() == 'Windows'

    elif os.path.isdir(os.path.join(DATA_LOCAT, 'portable_data')):
        # Remember to add portable_data/ folder within ffcuesplitter-gui/
        FILE_CONF, DIR_CONF, LOG_DIR = portable_paths(DATA_LOCAT)
        RELPATH = '-embed-' in os.path.basename(sys.prefix)

    else:
        FILE_CONF, DIR_CONF, LOG_DIR = conventional_paths()
        RELPATH = False
    # -------------------------------------------------------------------

    def __init__(self):
        """
        Given the pathnames defined by `DATA_LOCAT` it performs
        the initialization described in DataSource.

            `self.srcpath` > configuration folder for recovery
            `self.icodir` > set of icons
            `self.localepath` > locale folder

        """
        self.apptype = None  # appimage, pyinstaller on None
        self.workdir = os.path.dirname(os.path.dirname
                                       (os.path.dirname(DataSource.MPATH))
                                       )
        self.localepath = os.path.join(DataSource.DATA_LOCAT, 'locale')
        self.srcpath = os.path.join(DataSource.DATA_LOCAT, 'share')
        self.icodir = os.path.join(DataSource.DATA_LOCAT, 'art', 'icons')
        self.ffmpeg_pkg = os.path.join(DataSource.DATA_LOCAT, 'FFMPEG')
        launcher = os.path.isfile(f'{self.workdir}/launcher')

        if DataSource.FROZEN and DataSource.MEIPASS or launcher:
            msg(f'frozen={DataSource.FROZEN} '
                f'meipass={DataSource.MEIPASS} '
                f'launcher={launcher}')

            self.apptype = 'pyinstaller' if not launcher else None
            self.prg_icon = f"{self.icodir}/ffcuesplittergui.png"

        elif ('/tmp/.mount_' in sys.executable or os.path.exists(
              os.path.dirname(os.path.dirname(os.path.dirname(
                  sys.argv[0]))) + '/AppRun')):
            # embedded on python appimage
            msg('Embedded on python appimage')
            self.apptype = 'appimage'
            userbase = os.path.dirname(os.path.dirname(sys.argv[0]))
            pixmaps = '/share/pixmaps/ffcuesplittergui.png'
            self.prg_icon = os.path.join(userbase + pixmaps)

        else:
            binarypath = shutil.which('ffcuesplitter-gui')
            if platform.system() == 'Windows':  # any other packages
                exe = binarypath if binarypath else sys.executable
                msg(f'Win32 executable={exe}')
                self.prg_icon = self.icodir + "\\ffcuesplittergui.png"
                if '-embed-' in os.path.basename(sys.prefix):
                    self.apptype = 'embed'

            elif binarypath == '/usr/local/bin/ffcuesplittergui':
                msg(f'executable={binarypath}')
                # pip as super user, usually Linux, MacOs, Unix
                share = '/usr/local/share/pixmaps'
                self.prg_icon = share + '/ffcuesplittergui.png'

            elif binarypath == '/usr/bin/ffcuesplittergui':
                msg(f'executable={binarypath}')
                # installed via apt, rpm, etc, usually Linux
                share = '/usr/share/pixmaps'
                self.prg_icon = share + "/ffcuesplittergui.png"

            else:
                msg(f'executable={binarypath}')
                # pip as normal user, usually Linux, MacOs, Unix
                if binarypath is None:
                    # need if user $PATH is not set yet
                    userbase = site.getuserbase()
                else:
                    userbase = os.path.dirname(os.path.dirname(binarypath))
                pixmaps = '/share/pixmaps/ffcuesplittergui.png'
                self.prg_icon = os.path.join(userbase + pixmaps)
    # ---------------------------------------------------------------------

    def get_fileconf(self):
        """
        Get ffcuesplitter-gui configuration data and returns a dict object
        with current data-set for bootstrap.

        Note: If returns a dict key == ERROR it will raise a windowed
        fatal error in the gui_app bootstrap.
        """
        userconf = get_options(DataSource.DIR_CONF, DataSource.FILE_CONF)

        if userconf.get('ERROR'):
            return userconf
        userconf = userconf['R']

        # set output directories
        outfile = get_outdir(userconf['outputfile'],
                             DataSource.RELPATH,
                             self.apptype
                             )

        if outfile[1]:
            return {'ERROR': f'{outfile[1]}'}

        def _relativize(path, relative=DataSource.RELPATH):
            """
            Returns a relative pathname if *relative* param is True.
            If not, it returns the given pathname. Also return the given
            pathname if `ValueError` is raised. This function is called
            several times during program execution.
            """
            try:
                return os.path.relpath(path) if relative else path
            except ValueError:
                # return {'ERROR': f'{error}'}  # use `as error` here
                return path

        return ({'ostype': platform.system(),
                 'srcpath': _relativize(self.srcpath),
                 'localepath': _relativize(self.localepath),
                 'fileconfpath': _relativize(DataSource.FILE_CONF),
                 'workdir': _relativize(self.workdir),
                 'confdir': _relativize(DataSource.DIR_CONF),
                 'logdir': _relativize(DataSource.LOG_DIR),
                 'FFMPEG_pkg': _relativize(self.ffmpeg_pkg),
                 'app': self.apptype,
                 'relpath': DataSource.RELPATH,
                 'getpath': _relativize,
                 'outputfile': outfile[0],
                 'ffmpeg_cmd': _relativize(userconf['ffmpeg_cmd']),
                 'ffprobe_cmd': _relativize(userconf['ffprobe_cmd']),
                 **userconf
                 })
    # --------------------------------------------------------------------

    def icons_set(self, icontheme):
        """
        Determines icons set assignment defined on the configuration
        file (see `icontheme` in the settings.json file).
        Returns a icontheme dict object.

        """
        keys = ('ffcuesplittergui', 'startsplit', 'setup',
                'stop', 'trackinfo', 'CDinfo', 'log',
                'empty_2',)

        ext = 'svg' if 'wx.svg' in sys.modules else 'png'

        iconames = {'Light':  # icons for light themes
                    {'x22': f'{self.icodir}/Light/24x24'},
                    'Dark':  # icons for dark themes
                    {'x22': f'{self.icodir}/Dark/24x24'},
                    'Colored':  # icons for all themes
                    {'x22': f'{self.icodir}/Colored/24x24'},
                    }

        choose = iconames.get(icontheme)  # set appropriate icontheme

        iconset = (self.prg_icon,
                   f"{choose.get('x22')}/startsplit.{ext}",
                   f"{choose.get('x22')}/setup.{ext}",
                   f"{choose.get('x22')}/stop.{ext}",
                   f"{choose.get('x22')}/trackinfo.{ext}",
                   f"{choose.get('x22')}/CDinfo.{ext}",
                   f"{choose.get('x22')}/log.{ext}",
                   f"{choose.get('x22')}/empty_2.{ext}",
                   )
        values = [os.path.join(norm) for norm in iconset]  # normalize pathns

        return dict(zip(keys, values))
