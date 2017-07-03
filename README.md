# Average Music
Research trends in music categories

This research effort was originally used to find out what average music looks like from a signal processing standpoint.

## Setup
Clone this repo.

Install youtube-dl: `sudo apt-get install youtube-dl`

Install ffmpeg: `sudo apt-get install ffmpeg`

Jump into git folder: `cd Average-Music`

Get midi-csv converter: `wget http://www.fourmilab.ch/webtools/midicsv/midicsv-1.1.tar.gz`.
If this command produces a failure, go to (http://www.fourmilab.ch/webtools/midicsv/).

extract folder: `tar -xzvf midicsv-1.1.tar.gz`

Jump into midi-1.1: `cd midicsv-1.1`

make: `make`

jump back to main folder: `cd ..`

get wav-midi converter: `git clone https://github.com/kichiki/WaoN.git`

jump into WaoN:`cd WaoN`

make: `make`

## Quick Use
All scripts are in scripts folder:
```
cd scripts
```
More man/options info at the top of each script file.

### Display Summed Fourier Transform Average of mp3
Put mp3 in Average-Music/mp3/
```
python notePresence.py <csv_file> [options]
```

### Display Summed Fourier Transform of mp3 from youtube video
```
chmod +x multipleYoutubeNotePresenceGraph.sh
./youtubeNotePresenceGraph.sh <youtube_URL> <file_output_name>
```

### Display Summed Fourier Transform of mp3 from list of youtube videos
Shell script reads from text file which needs to be formatted like this:
```
<youtube_URL> <file_name>
<youtube_URL> <file_name>
```
Example:
```
https://www.youtube.com/watch?v=s0f_go8vQOY river_flows_in_you
https://www.youtube.com/watch?v=pFZ5_q86u0E sherlock
```
Code:
```
chmod +x youtubeNotePresenceGraph.sh
./youtubeNotePresenceGraph.sh <youtube_list.txt>
```
### Convert all

Will fill in soon

### mp3 to wav

mp3 to wav coversion is done with the ffmpeg package that can be installed on the command line with the following command:
`sudo apt-get install ffmpeg`

### wav to midi

wav to midi is done using the program waon found [here](https://github.com/kichiki/WaoN).

### midi to csv

midi to csv is done by the included midicsv.exe found [here](http://www.fourmilab.ch/webtools/midicsv/).
This file is included in the source here so it does not need to be downloaded again.

## How it works
This program first collects an mp3 from [youtube-dl](https://github.com/rg3/youtube-dl) for ease of collecting mp3s:

+ mp3  --> wav
+ wav  --> midi
+ midi --> csv

There is a batch script that performs all of these tasks and places each file that it creates in it's respective folder.

