#!/usr/bin/env python
"""Translate from a blink student list into a list of emails that can
be used to populate Piazza.

The first lines of a Blink student list are:

Sect ID	Course	Title	SecCode	Instructor	
785801	CSE103	Practical Intro/Prob & Stats	A00	Freund, Yoav

Sec ID	PID	Student	Credits	College	Major	Level	Email	
785801	A10318231	Abid, Michael E	4.00	RE	CS26	SR	mabid@ucsd.edu
785801	A10917852	Abney, Beck Graham	4.00	SI	CS26	FR	babney@ucsd.edu

"""
import sys

Filenames={
    'CL':'StandardOutput-CL-1410209210488.xls',
    'WL':'StandardOutput-WL-1410209279097.xls'
    }

outfile=open('StudentTable.csv','w')
outfile.write('PID, Last,First,Major, Level, Email, Status\n')

for Status in ('CL','WL'):
    print 'Status=',Status
    Infile=open(Filenames[Status],'r')
    for i in range(4):      #skip header lines
        Infile.readline()

    for line in Infile.readlines():
        #parts = line.strip().split('\t')
        #print line,parts
        if Status=='CL':
            SecID, PID, Student, Credits, College, Major, Level, Email= line.strip().split('\t')
        else:
            SecID, PID, Student, College, Major, Level, Date, Time, Email= line.strip().split('\t')
        Last, First = Student.split(',')
        Email=Email.strip()
        outfile.write(','.join((PID, Last,First,Major, Level, Email,Status))+'\n')
    Infile.close()
outfile.close()