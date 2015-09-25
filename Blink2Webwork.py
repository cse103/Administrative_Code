#!/usr/bin/env python

"""
Take in two arguments: readfile writefile
readfile is a .tsv file of student rouster
writefile is a .lst file used by webwork (classlist file)

Translate from a blink student list into a webwork student list.

The first lines of a Blink student list are:

Sect ID	Course	Title	SecCode	Instructor	
785801	CSE103	Practical Intro/Prob & Stats	A00	Freund, Yoav

Sec ID	PID	Student	Credits	College	Major	Level	Email	
785801	A10318231	Abid, Michael E	4.00	RE	CS26	SR	mabid@ucsd.edu
785801	A10917852	Abney, Beck Graham	4.00	SI	CS26	FR	babney@ucsd.edu
"""

import sys
readfile = open(sys.argv[1], 'r')
writefile = sys.argv[2]

for i in range(4):      #skip header lines
    readfile.readline()

for line in readfile.readlines():
    # parts = line.strip().split('\t')
    #SecID, PID, Student, College, Major, Level, Date, Time, Email= line.strip().split('\t')
    SecID, PID, Student, Credits, College, Major, Level, Email= line.strip().split('\t')
    Last, First = Student.split(',')
    Email=Email.strip()
    userID,emailDomain = Email.split('@')
    with open(writefile, "a") as myfile:
    	myfile.write(','.join([PID,Last,First,'','',SecID,'',Email,userID])+'\n')
    #print ','.join([PID,Last,First,'','',SecID,'',Email,userID])
    #print '\t,'.join([PID,Last,First,'Enrolled (C)','',SecID,'',Email,userID])
    
