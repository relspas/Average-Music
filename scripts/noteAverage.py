########################################
# Use: 
# python noteAverage.py <songList.txt> [options]
#
# Format of songList.txt. make sure there are no trailing lines at end
# of file:
# file1.csv
# file2.csv
#
# Options:
# -w : THe presence of notes in graph are weighted (Default: not weighted)
# -t graph_song_title : This becomes the song title on the graph (Default: fils name)
# -s : Save the graph in ../graphs/ (Default: not saved)
# --no-display : don't display graph (Default: displayed through X-11 forwarding)
# python notePresence.py songlist.txt -w -t Haru_Haru -s
########################################

import sys
import matplotlib.pyplot as plt
import numpy as np
from textwrap import wrap
import math

csvListFileName = sys.argv[1]
WEIGHTFLAG = False
DISPLAYFLAG = True
SAVEFLAG = False
GRAPHSONGTITLE = csvListFileName
FILESAVENAME = csvListFileName

argNum = 2
while argNum < len(sys.argv):
   if sys.argv[argNum] == "-w":
      WEIGHTFLAG = True
      print "Using weighted velocity"
   elif sys.argv[argNum] == "-t":
      argNum += 1
      GRAPHSONGTITLE = sys.argv[argNum]
      print "Using Graph Title: " + GRAPHSONGTITLE
   elif sys.argv[argNum] == "-s":
      argNum += 1
      SAVEFLAG = True
      FILESAVENAME = sys.argv[argNum]
      print "Using file save name: " + FILESAVENAME
   elif sys.argv[argNum] == "--no-display":
      DISPLAYFLAG = False
      print "Not displaying graph"
   argNum += 1

songCount = sum(1 for line in open(csvListFileName))
averagePerSong = [0]*songCount
std_dev = [0]*songCount
songNumber = 0
labels = [""]*songCount

csvListFilePointer = open(csvListFileName)
for song in csvListFilePointer:
   print "looping"
   song = song.strip()
   csvFilePointer = open("../csv/"+song)
   lastNoteTime = [0]*128 #arr 0-127
   noteWeightsTemp = [0]*128
   noteWeights = [0]*128
   maxMidiClocks = 0
   maxVelocity = 0

   #find max velocity
   for line in csvFilePointer:
      lineArr = [x.strip() for x in line.split(",")]
      if len(lineArr) < 6: continue
      velocity = int(lineArr[5])
      if maxVelocity < velocity:
         maxVelocity = velocity
   csvFilePointer.close()

   #read through file
   csvFilePointer = open("../csv/"+song)
   for line in csvFilePointer:
      lineArr = [x.strip() for x in line.split(",")]
      if len(lineArr) < 6: continue
      timeStamp = int(lineArr[1])
      eventName = lineArr[2]
      note = int(lineArr[4])
      velocity = int(lineArr[5])
      if eventName == "Note_on_c":
         lastNoteTime[note] = timeStamp
         noteWeightsTemp[note] = velocity
      elif eventName == "Note_off_c":
         noteLength = timeStamp - lastNoteTime[note]
         if WEIGHTFLAG:
            noteWeights[note] = noteWeights[note] + float(noteWeightsTemp[note])/maxVelocity * noteLength   
         else:
            noteWeights[note] = noteWeights[note] + noteLength   
      if maxMidiClocks < timeStamp:
         maxMidiClocks = timeStamp

   noteWeightsNormalized = [float(x)/maxMidiClocks*100 for x in noteWeights]
   #mean DOUBLE CHECK THIS CALCULATION
   expectedPreprocess = [0]*128
   for i in range(0,128):
      expectedPreprocess[i] = noteWeightsNormalized[i]*i
   averagePerSong[songNumber] = sum(expectedPreprocess)/sum(noteWeightsNormalized)
   print averagePerSong

   #variance 
   variancePreprocess = [0]*128
   for i in range(0,128):
      variancePreprocess[i] = noteWeightsNormalized[i]*(i**2)#(averagePerSong[songNumber]-i)**2
   std_dev[songNumber] = math.sqrt(\
      sum(variancePreprocess)/sum(noteWeightsNormalized) \
      - (averagePerSong[songNumber]**2))
   print std_dev

   #label
   labels[songNumber] = song[:-4] 
   songNumber += 1

#plot
print "plotting..."
fig, ax = plt.subplots()
# ax.plot(averagePerSong,range(1,songCount+1),'bo')
ax.errorbar(averagePerSong, range(1,songCount+1), xerr=std_dev, fmt='o', capthick=1)

#plot labels
ax.set_ylabel('Song Name')
if WEIGHTFLAG:
   ax.set_xlabel('Average Pitch in song (60-middle C)')
   ax.set_title('Average Pitch of Selected Songs')
else:
   ax.set_xlabel('Weighted Average Pitch in song (60-middle C)')
   ax.set_title('Weighted Average Pitch of Selected Songs')
labels = [ '\n'.join(wrap(l, 20)) for l in labels ]
plt.yticks(range(1,songCount+1), labels)

if SAVEFLAG:
   saveLocation = '../graphs/'+FILESAVENAME
   if WEIGHTFLAG:
      saveLocation += '_weighted'
   saveLocation += '_note_average.png'
   plt.savefig(saveLocation)

if DISPLAYFLAG:
   plt.show()