![compressed result](https://files.catbox.moe/zx20qb.gif)

# Video and Audio Fryer

This Python tool allows you to compress video and audio files by using FFmpeg to apply various levels of compression, reducing their size for faster sharing or uploading. You can control the video compression percentage using an easy-to-use slider, and the tool supports a wide range of video formats including `.mp4`, `.mkv`, `.avi`, and `.mov`.

## Features

- Select input video files from your system.
- Choose an output folder for saving the processed video.
- Control the compression percentage (1-500), which affects both video resolution and audio bitrate.
- Automatically adjusts audio bitrate based on selected compression.
- Supports multiple video formats (`.mp4`, `.mkv`, `.avi`, `.mov`).
- Runs FFmpeg in the background for efficient video processing.

## Requirements

- Python 3.x
- `tkinter` for the GUI
- `subprocess` for running FFmpeg commands

You will also need to have FFmpeg installed and available in your system's PATH. If FFmpeg isn't available, the program will prompt you to manually locate the FFmpeg executable.

You can download FFmpeg from [FFmpeg.org](https://ffmpeg.org/download.html).

## Installation

To install the necessary dependencies, run the following:

```bash
pip install tk
```

Make sure FFmpeg is installed on your system and accessible from the command line.

## How to Use

1. Clone or download this repository to your local machine.
2. Run the script `video fryer.py` (or whatever you name it) in your terminal or command prompt.
3. The GUI will open with options to select an input video file and an output directory.
4. Use the slider to select the desired compression percentage (1-500).
5. Click the "Compress Video" button to start processing the video.
6. The compressed video will be saved in the selected output directory.

## Example

```bash
python "video fryer.py"
```

Once you run the program, the GUI will allow you to browse for a video, set the compression level, and then compress the video with the desired settings.
