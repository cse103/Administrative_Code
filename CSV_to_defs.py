#!/usr/bin/env python

import pandas as pd
import argparse
import datetime
from datetime import timedelta

df = pd.read_csv('set_assignments.csv')
df

sets = sorted(set(df['Set Name']))
print set(df['Set Name'])
start_date = datetime.datetime(2014, 10, 1, 17)
week = datetime.timedelta(days=7)

unused_problems = open('setUnusedProblems.def', 'w')
unused_problems.write("openDate          = {0} PST\n".format(
    (datetime.datetime.now() + week).strftime('%m/%d/%Y at %I:%M%p')))
unused_problems.write("dueDate           = {0} PST\n".format(
    (datetime.datetime.now() + 2*week).strftime('%m/%d/%Y at %I:%M%p')))
unused_problems.write("answerDate        = {0} PST\n".format(
    (datetime.datetime.now() + 2*week).strftime('%m/%d/%Y at %I:%M%p')))

unused_problems.write("paperHeaderFile   = defaultHeader\n")
unused_problems.write("screenHeaderFile  = defaultHeader\n")
unused_problems.write("problemList       =\n")

for set_id in sets:
    with open("set{0}.def".format(set_id), 'w') as def_file:
        end_date = start_date + week
        tz_open = 'PST' if start_date.month >=11 and start_date.day>=3 else 'PDT'
        tz_close = 'PST' if end_date.month >=11 and end_date.day>=3 else 'PDT'
        def_file.write("openDate          = {0} {1}\n".format(
                    start_date.strftime('%m/%d/%Y at %I:%M%p'), tz_open))
        def_file.write("dueDate           = {0} {1}\n".format(
                    end_date.strftime('%m/%d/%Y at %I:%M%p'), tz_close))
        def_file.write("answerDate        = {0} {1}\n".format(
            end_date.strftime('%m/%d/%Y at %I:%M%p'), tz_close))

        def_file.write("paperHeaderFile   = defaultHeader\n")
        def_file.write("screenHeaderFile  = defaultHeader\n")
        def_file.write("problemList       =\n")

        start_date = end_date
        set_problems = df[df['Set Name'] == set_id]
        for index, problem in set_problems.iterrows():
            if problem['Used'] == 1:
                def_file.write("{0}\n".format(problem['PG File Path']))
            else:
                unused_problems.write("{0}\n".format(problem['PG File Path']))
