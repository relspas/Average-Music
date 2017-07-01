##################################################
# to use file call:
# python notePresence.py <csv file> [options]
# Options:
# -w : THe presence of notes in graph are weighted (Default: not weighted)
# -t graph_song_title : This becomes the song title on the graph (Default: fils name)
# -s graph_song_title : Save the graph in ../graphs/ (Default: not saved)
# --no-display : don't display graph (Default: displayed through X-11 forwarding)
# python notePresence.py filename.csv -w -t Haru_Haru -s -d
##################################################

import sys
import matplotlib.pyplot as plt

csvFileNameInput = sys.argv[1]
WEIGHTFLAG = False
DISPLAYFLAG = True
SAVEFLAG = False
GRAPHSONGTITLE = csvFileNameInput
FILESAVENAME = csvFileNameInput

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

csvFilePointer = open(csvFileNameInput)
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
csvFilePointer = open(csvFileNameInput)
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

#plot
print "plotting..."
fig, ax = plt.subplots()
rects1 = ax.bar(range(0,128), noteWeightsNormalized, 0.5, color='r')

#plot labels
if WEIGHTFLAG:
   ax.set_ylabel('Weighted percentage in song (%)')
   ax.set_title('Weighted Presence of Notes in '+GRAPHSONGTITLE)
else:
   ax.set_ylabel('Percentage in song (%)')
   ax.set_title('Presence of Notes in '+GRAPHSONGTITLE)
ax.set_xlabel('Note in midi notation (60-middle C)')

if SAVEFLAG:
   saveLocation = '../graphs/rnb/'+GRAPHSONGTITLE
   if WEIGHTFLAG:
      saveLocation += '_weighted'
   saveLocation += '_note_presence.png'
   plt.savefig(saveLocation)

if DISPLAYFLAG:
   plt.show()
