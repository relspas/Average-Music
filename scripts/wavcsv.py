#############################################
# python mp3csv.py <input>
# python mp3csv.py input.mp3
#############################################

import sys
from subprocess import call

inputFileName = sys.argv[1]

#wav to midi
call(["./../waon-0.10/waon", "-i", inputFileName[:-3] \
   +"wav", "-o", inputFileName[:-3] +"mid"] )

#midi to csv
call(["./../midicsv-1.1/midicsv", inputFileName[:-3] +"mid", \
   inputFileName[:-3] +"csv"])