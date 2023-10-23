# Osu Replay Key Overlay
A python script that generates a video (by default .mp4) of a key overlay given an osu!std replay (.osr file)

## Customisation of your file
You can change the output file by modifing these variables: </br>
- WIDHT and HEIGHT - the dimensions of the video measured in pixels
- FPS - framerate of the video
- KEYWIDTH - width of the blocks (keep in mind that KEYWIDTH*2 should be <= WIDTH)
- SEGMENTS - the amount of segments the height is divided into. The blocks travel a segment each frame so think of this as controlling the speed.
- COLOR - the color of the blocks in hex code

## Dependencies
The required python dependencies are:
- [osrparse](https://pypi.org/project/osrparse/)
- [ffmpeg-python](https://pypi.org/project/ffmpeg-python/) 
- [pillow](https://pypi.org/project/Pillow/)

```
$ python -m pip install osrparse ffmpeg-python pillow
```

Also you need to have ffmpeg installed on your system, download it [here](https://ffmpeg.org/download.html). </br>
If you're on Linux you can also use your package manager. For example on arch-based distros:
```
$ yay -S ffmpeg
```

## Usage
```
$ python parse.py <replay_path> <output_path>
```
## Example Output
https://github.com/KreconyMakaron/osu-replay-key-overlay/assets/55319736/16b1685a-88e3-4a1b-99eb-6bf8620ee0b8

And then if you edit it and add to a video you can create cpol-like replays like [this](https://www.youtube.com/watch?v=-mODyQMSnas)
