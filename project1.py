#Import file created from baselight (Baselight_export.txt)
import argparse
import sys


with open('Baselight_export.txt', 'r') as file:
    for row in file:
        print(row) 


#Import xytech work order (Xytech.txt)

#script will parse data

#computation done to match shareholder's request
    #replace file system from local baselight to facility
    #storage(remember color correcter's prefer local storage for bandwidth issues)

#Export CSV file ('/' indicates columns):
# -Line 1: Producer / Operator / job /notes
# -Line 4: show location / frames to fix
# -Frames in consecutive order shown as ranges

#example code
#Parse arguments for job
parser = argparse.ArgumentParser()
parser.add_argument("--job", dest="jobFolder", help="job to process")
parser.add_argument("--verbose", action="store_true", help="show verbose")
parser.add_argument("--TC", dest="timecode", help="Timecode to process")
args =  parser.parse_args()
if args.jobFolder is None:
    print("No job selected") 
    sys.exit(2)
else:
    job = args.jobFolder
if args.timecode:
    timecodeTC = args.timecode