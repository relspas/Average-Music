#!/bin/bash
# Usage: ./youtubeNotePresenceGraph.sh <youtube URL> <file output name>
youtube-dl --extract-audio --audio-format mp3 $1 -o ../mp3/$2.mp3
ffmpeg -i ../mp3/$2.mp3 -acodec pcm_u8 -ar 22050 ../wav/$2.wav
./../waon-0.10/waon -i ../wav/$2.wav -o ../mid/$2.mid
./../midicsv-1.1/midicsv ../mid/$2.mid ../csv/$2.csv
python notePresence.py ../csv/$2.csv -t $2 -s $2 --no-display
