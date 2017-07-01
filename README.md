# Average Music
Research trends in music categories

This research effort was originally used to find out what average music looks like from a signal processing standpoint.

### Dependencies
Will fill this in soon

This program first collects an mp3 from [youtube-dl](https://github.com/rg3/youtube-dl) for ease of collecting mp3s:

+ mp3  --> wav
+ wav  --> midi
+ midi --> csv

There is a batch script that performs all of these tasks and places each file that it creates in it's respective folder.

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

