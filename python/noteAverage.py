########################################
# python noteAverage.py song1.csv song2.csv
########################################

import sys
import matplotlib.pyplot as plt
import numpy as np
from textwrap import wrap
import math

songCount = len(sys.argv) - 1

WEIGHTFLAG = True
averagePerSong = [0]*songCount
std_dev = [0]*songCount

for songNumber in range(0,songCount):
   csvFileNameInput = sys.argv[songNumber+1]
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
#plot
print "plotting..."
fig, ax = plt.subplots()
# ax.plot(averagePerSong,range(1,songCount+1),'bo')
ax.errorbar(averagePerSong, range(1,songCount+1), xerr=std_dev, fmt='o', capthick=1)
#plot labels
ax.set_ylabel('Song Name')
ax.set_xlabel('Average Pitch in song (60-middle C)')
labels = sys.argv[1:]
labels = [ '\n'.join(wrap(l, 20)) for l in labels ]
plt.yticks(range(1,songCount+1), labels)
ax.set_title('Average Pitch of Selected Songs')

plt.show()