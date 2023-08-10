#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Name: setup.py
Porpose: script to setup FFcuesplitter-gui.
Compatibility: Python3
Platform: all
Writer: Gianluca Pernigotto <jeanlucperni@gmail.com>
Copyright: 2023-2023 Gianluca Pernigotto <jeanlucperni@gmail.com>
license: GPL3
Rev: Aug.1.2023
Code checker: flake8, pylint
########################################################

This file is part of FFcuesplitter-gui.

    FFcuesplitter-gui is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    FFcuesplitter-gui is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with FFcuesplitter-gui.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
import platform
from setuptools import setup, find_packages
from ffcuesplitter_gui._sys.info import (__version__,
                                         __author__,
                                         __contact__,
                                         # __maintainer__,
                                         # __maintainer_contact__,
                                         # __projecturl__,
                                         __githuburl__,
                                         # __appname__,
                                         __packagename__,
                                         __license__,
                                         __description__,
                                         __descriptionfull__,
                                         # __copyleft__,
                                         # __licensefull__
                                         )


def source_build():
    """
    Source/Build distributions

    """
    if 'sdist' in sys.argv or 'bdist_wheel' in sys.argv:

        inst_req = ["wxpython>=4.0.7; platform_system=='Windows' or "
                    "platform_system=='Darwin'",
                    "PyPubSub>=4.0.3",
                    "ffcuesplitter>=1.0.22",
                    ]
        setup_req = ["setuptools>=47.1.1",
                     "wheel>=0.34.2",
                     "twine>=3.1.1"
                     ]
        with open('README.md', 'r', encoding='utf8') as readme:
            long_descript = readme.read()

        long_description_ct = 'text/markdown'

    else:  # e.g. to make a Debian source package, include wxpython.
        inst_req = ["wxpython>=4.0.7",
                    "PyPubSub>=4.0.3",
                    "ffcuesplitter>=1.0.22",
                    ]
        setup_req = []
        long_descript = __descriptionfull__
        long_description_ct = 'text'

    excluded = ['']
    # pathnames must be relative-path
    if platform.system() == 'Windows':
        data_f = [('share/pixmaps',
                   ['ffcuesplitter_gui/art/icons/ffcuesplittergui.png'])]

    elif platform.system() == 'Darwin':
        data_f = [('share/pixmaps',
                   ['ffcuesplitter_gui/art/icons/ffcuesplittergui.png']),
                  ('share/man/man1',
                   ['docs/man/man1/ffcuesplitter-gui.1.gz']),
                  ]
    else:
        pkg = 'ffcuesplitter_gui'
        png = 'ffcuesplittergui.png'
        desktop = 'io.github.jeanslack.ffcuesplitter_gui.desktop'
        metainfo = 'io.github.jeanslack.ffcuesplitter_gui.appdata.xml'
        data_f = [
            ('share/applications', [f'{pkg}/art/{desktop}']),
            ('share/metainfo', [f'{metainfo}']),
            ('share/pixmaps', [f'{pkg}/art/icons/{png}']),
            ('share/icons/hicolor/48x48/apps',
             [f'{pkg}/art/icons/hicolor/48x48/apps/{png}']),
            ('share/icons/hicolor/256x256/apps',
             [f'{pkg}/art/icons/hicolor/256x256/apps/{png}']),
            ('share/icons/hicolor/scalable/apps',
             [f'{pkg}/art/icons/hicolor/scalable/apps/ffcuesplittergui.svg']),
            ('share/man/man1', ['docs/man/man1/ffcuesplitter-gui.1.gz']),
            ]
    setup(name=__packagename__,
          version=__version__,
          description=__description__,
          long_description=long_descript,
          long_description_content_type=long_description_ct,
          author=__author__,
          author_email=__contact__,
          url=__githuburl__,
          license=__license__,
          platforms=["All"],
          packages=find_packages(exclude=excluded),
          data_files=data_f,
          package_data={"ffcuesplitter_gui": ["art/icons/*", "locale/*"]
                        },
          exclude_package_data={
              "ffcuesplitter_gui": ["art/ffcuesplittergui.icns",
                                    "art/ffcuesplittergui.ico",
                                    "locale/README",
                                    "locale/ffcuesplitter-gui.pot"]
              },
          include_package_data=True,
          zip_safe=False,
          python_requires=">=3.7.0, <4.0",
          install_requires=inst_req,
          setup_requires=setup_req,
          entry_points={
              'gui_scripts':
                  ['ffcuesplitter-gui = ffcuesplitter_gui.gui_app:main']},
          classifiers=[
              'Environment :: X11 Applications :: GTK',
              'Development Status :: 4 - Beta',
              'Operating System :: MacOS',
              'Operating System :: Microsoft :: Windows',
              'Operating System :: POSIX :: Linux',
              'Intended Audience :: End Users/Desktop',
              ('License :: OSI Approved :: GNU General Public License v3 '
                  '(GPLv3)'),
              'Natural Language :: English',
              'Natural Language :: Italian',
              'Natural Language :: Russian',
              'Programming Language :: Python :: 3 :: Only',
              'Programming Language :: Python :: 3.7',
              'Programming Language :: Python :: 3.8',
              'Programming Language :: Python :: 3.9',
              'Programming Language :: Python :: 3.10',
              'Programming Language :: Python :: 3.11',
              'Topic :: Multimedia :: Sound/Audio',
              'Topic :: Multimedia :: Sound/Audio :: Conversion',
              'Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Ripping',
              ],
          )


if __name__ == '__main__':
    source_build()
