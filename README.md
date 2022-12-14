[![Image](https://img.shields.io/static/v1?label=python&logo=python&message=3.7%20|%203.8|%203.9&color=blue)](https://www.python.org/downloads/)
[![Image](https://img.shields.io/badge/license-GPLv3-orange)](https://github.com/jeanslack/FFcuesplitter-GUI/blob/main/LICENSE)

# FFcuesplitter-GUI 

Graphical interface for [FFcuesplitter](https://github.com/jeanslack/FFcuesplitter), 
written in wxPython phoenix.

![preview](./docs/gui_preview.gif)

## Description

It is a cross-platform GUI for the [FFcuesplitter](https://github.com/jeanslack/FFcuesplitter) 
library written in wxPython Phoenix. It features editable tags per track, checkboxes 
to select track extractions, an audio CD properties viewer, support for WAV, 
FLAC, MP3 and OGG output formats, audio compression selectors and the ability 
to copy audio codec without re-encoding.

## Requirements
- [Python >= 3.7.0](https://www.python.org/)
- [wxPython-Phoenix >= 4.0.7](https://wxpython.org/)
- [PyPubSub >= 4.0.3](https://pypi.org/project/PyPubSub/)
- [ffcuesplitter >= 1.0.7](https://pypi.org/project/ffcuesplitter/)
- [ffmpeg >=4.3](https://ffmpeg.org/)
- [ffprobe >=4.3](https://ffmpeg.org/ffprobe.html)

## Running from source code

```
git clone https://github.com/jeanslack/FFcuesplitter-GUI.git
cd FFcuesplitter-GUI
python3 -m venv My_env
source My_env/bin/activate
python3 -m pip install -r requirements.txt
python3 launcher
```

## Authors
See [AUTHORS](AUTHORS) file

## License
The [GNU GENERAL PUBLIC LICENSE Version 3](LICENSE)
