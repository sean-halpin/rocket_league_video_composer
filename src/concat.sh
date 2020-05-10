#!/bin/bash

echo "run this inside the clips dir"

ls -1 -d "$PWD/"* | xargs -iXXX echo "file 'XXX'" > ../cliplist.txt

ffmpeg -f concat -safe 0 -i ../cliplist.txt -c copy ../concatenated.mp4

