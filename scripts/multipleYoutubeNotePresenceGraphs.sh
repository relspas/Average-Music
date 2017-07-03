#!/bin/bash
#Usage: ./multipleYoutubeNotePresenceGraphs.sh <youtube_list.txt>
#
#youtube_list.txt format:
#<youtube_URL> <file_name>
#<youtube_URL> <file_name>
#
#Example:
#https://www.youtube.com/watch?v=s0f_go8vQOY river_flows_in_you
#https://www.youtube.com/watch?v=pFZ5_q86u0E sherlock
filename="$1"
tr -d '\r' < $filename > out
while read -u 10 -r f1 f2
do
   sh ./youtubeNotePresenceGraph.sh $f1 $f2
done 10<out
