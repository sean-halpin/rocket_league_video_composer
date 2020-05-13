# Rocketleague video composer

### Description 

Python repo to;
 - Take Rocket League Video Clips
 - Detect goals in video clips using Tesseract 
 - Trim the video clips to shorter size
 - Put all the clips together into goal compilation

### Output

This compilation consists of about 1590 goals that I dumped from my ps4 recorded between 2015 & 2017 mostly.
Showing a progression from bronze in 2015 to diamond in 2017. 

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/OAh2Le0AEC8/0.jpg)](https://www.youtube.com/watch?v=OAh2Le0AEC8)

Taking 40GB of Rocket League clips I had saved on my ps4 between 2015 to 2017
This code searched through every one of them programmatically looking for the text "REPLAY" in the bottom left corner. 
When the replay text was found, we rewind 3 seconds then take the previous 8 seconds for a clip of the goal. 
When all the clips are trimmed, we concatenate them into a single video sorted by time they were recorded. 

### How to use this very rough code

I whipped this together in an hour or so, results may vary

- Edit line 84 of `detect.py`, to point to your mp4 rocket league clips are stored.
- `python detect.py`
- `python clip.py`
- `cd ./clips && ./concat.sh`
