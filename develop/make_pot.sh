#!/bin/bash

# Author: Gianluca Pernigotto <jeanlucperni@gmail.com>
# Copyright: (c) 2020/2021 Gianluca Pernigotto <jeanlucperni@gmail.com>
# license: GPL3
# Rev: Nov.18.2021
#
# Make a new `ffcuesplitter-gui.po` file on '../../ffcuesplitter-gui/locale'.
# The previus ffcuesplitter-gui.po file will be overwrite with new one
# incoming which will update latest strings for traslation .

PLATFORM=$(uname)  # command to show platform
self="$(readlink -f -- $0)"  # this file
here="${self%/*}"  # dirname of this file
rootdir=$(dirname $here)  # base sources directory
target="$rootdir/ffcuesplitter_gui/locale"  # location to store new incoming

cd $target

if [ "$PLATFORM" = "Darwin" ]; then
    # On my Macos xgettext is in '/usr/local/Cellar/gettext/0.20.1/bin/xgettext'
    # which is't in $PATH
    XGETTEXT="/usr/local/Cellar/gettext/0.20.1/bin/xgettext"

elif [ "$PLATFORM" = "Linux" ]; then
    XGETTEXT="xgettext"
fi

$XGETTEXT -d ffcuesplitter-gui "../gui_app.py" \
"../_dialogs/cd_info.py" \
"../_dialogs/check_new_version.py" \
"../_dialogs/infoprg.py" \
"../_dialogs/preferences.py" \
"../_dialogs/showlogs.py" \
"../_dialogs/track_info.py" \
"../_dialogs/wizard_dlg.py" \
"../_main/main_frame.py" \
"../_panels/cuesplitter_panel.py" \
"../_utils/utils.py" \

if [ $? != 0 ]; then
    echo 'Failed!'
else
    mv ffcuesplitter-gui.po ffcuesplitter-gui.pot
    echo "Done!"
    echo "'ffcuesplitter-gui.pot' was created on: '${target}'"
fi
