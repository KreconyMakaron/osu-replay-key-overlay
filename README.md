# Osu Replay Key Overlay
A python script that generates a video (by default .mp4) of a key overlay given an osu!std replay (.osr file) <\br>

# Customisation of your file
You can change the output file by modifing these variables: </br>
- WIDHT and HEIGHT - the dimensions of the video measured in pixels
- FPS - framerate of the video
- KEYWIDTH - width of the blocks (keep in mind that KEYWIDTH*2 should be <= WIDTH)
- SEGMENTS - the amount of segments the height is divided into. The blocks travel a segment each frame so think of this as controlling the speed.
- COLOR - the color of the blocks in hex code

# Dependencies
The required python dependencies are:
- [osrparse](https://pypi.org/project/osrparse/)
- [ffmpeg-python](https://pypi.org/project/ffmpeg-python/) 
- [pillow](https://pypi.org/project/Pillow/)

```
$ python -m pip install osrparse ffmpeg-python pillow
```

Also you need to have ffmpeg installed on your system, download it [here](https://ffmpeg.org/download.html). </br>
If you're on linux you can also use your package manager </br>
For example on arch-based distros:
```
$ yay -S ffmpeg
```

# Usage
```
$ python parse.py <replay_path> <output_path>
```
