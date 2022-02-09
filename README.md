[![Image](https://img.shields.io/static/v1?label=python&logo=python&message=3.7%20|%203.8|%203.9&color=blue)](https://www.python.org/downloads/)
[![image](https://img.shields.io/badge/wxpython-phoenix-green)](https://www.wxpython.org/)
[![Image](https://img.shields.io/badge/license-GPLv3-orange)](https://github.com/jeanslack/FFcuesplitter-GUI/blob/main/LICENSE)
![image](https://img.shields.io/badge/platform-linux%20|%20freebsd%20|%20macos%20|%20windows-brigthgreen) 

# FFcuesplitter-GUI 

FFcuesplitter-gui splits the audio CD images supplied with the CUE sheet via FFmpeg.

![preview](./docs/gui_preview.gif)

## Description

It is a cross-platform GUI for the [FFcuesplitter](https://github.com/jeanslack/FFcuesplitter) 
library written in wxPython Phoenix. It features editable tags per track, checkboxes 
for selecting the tracks to save, an audio CD properties viewer, support for wav, 
flac, mp3 and ogg output formats with audio compression selectors and the 
ability to copy audio codec without re-encoding.

## Requirements
- [Python >= 3.7.0](https://www.python.org/)
- [wxPython-Phoenix >= 4.0.3](https://wxpython.org/)
- [PyPubSub >= 4.0.3](https://pypi.org/project/PyPubSub/)
- [ffcuesplitter >= 1.0.7](https://pypi.org/project/ffcuesplitter/)
- [ffmpeg >=4.3](https://ffmpeg.org/)
- [ffprobe >=4.3](https://ffmpeg.org/ffprobe.html)

## Running from source code

```
git clone https://github.com/jeanslack/FFcuesplitter-GUI.git
cd FFcuesplitter-GUI
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 launcher
```

## Authors
See [AUTHORS](AUTHORS) file

## License
The [GNU GENERAL PUBLIC LICENSE Version 3](LICENSE)