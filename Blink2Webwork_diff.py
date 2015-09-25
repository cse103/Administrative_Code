###### Written by Ning Ma ######
###### 9.24.2015 ######

import sys
from sets import Set
"""
Take five arguments representing file names: writeFile, oldEnrollFile, oldWaitListFile, newEnrollFile, newWaitListFile. The file inputs MUST following the above order.

All the files are in .tsv format.

Subtract students who are new to the oldEnrollFile (not from oldWaitListFile)  or new to the oldWaitListFile. Write the informatio of these students to the writeFile and export as .lst format.
"""

#Get PID sets from old enrollment and old waiting list files. 
#The first argument must be the enrollment .lst file and the second file
#must be the waiting list .lst file
def getPIDSet(enrollFile, waitListFile):
    enrollPID = Set()
    waitListPID = Set()

    for i in range(4):
        enrollFile.readline()
        waitListFile.readline()
    
    for line in enrollFile.readlines():
        SecID, PID, Student, Credits, College, Major, Level, Email = line.strip().split('\t')
        enrollPID.add(PID);

    for line in waitListFile.readlines():
        SecID, PID, Student, College, Major, Level, Date, Time, Email= line.strip().split('\t')
        waitListPID.add(PID)

    return [enrollPID, waitListPID]


outputFile = open(sys.argv[1], "a");
oldEnroll = open(sys.argv[2],'r');
oldWaitList = open(sys.argv[3],'r');
newEnroll = open(sys.argv[4],'r');
newWaitList = open(sys.argv[5], 'r');

[oldEnrollPID, oldWaitListPID] = getPIDSet(oldEnroll, oldWaitList)

for i in range(4):
    newEnroll.readline()
    newWaitList.readline()

#add new enrolled student (not from old waiting list) to the outputFIle
for line in newEnroll.readlines():
    SecID, PID, Student, Credits, College, Major, Level, Email = line.strip().split('\t')
    Last, First = Student.split(',');
    Email = Email.strip();
    userID, emailDomain = Email.split('@');

    if (PID not in oldEnrollPID) and (PID not in oldWaitListPID):
        outputFile.write(','.join([PID,Last,First,'','',SecID,'',Email,userID]) + '\n')

#add new waiting list student to the outputFile
for line in newWaitList.readlines():
    SecID, PID, Student, College, Major, Level, Date, Time, Email= line.strip().split('\t')
    Last, First = Student.split(',');
    Email = Email.strip();
    userID, emailDomain = Email.split('@');

    if PID not in oldWaitListPID: 
        outputFile.write(','.join([PID,Last,First,'','',SecID,'',Email,userID]) + '\n')


