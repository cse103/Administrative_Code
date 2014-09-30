import pandas as pd
import argparse
import datetime

df = pd.read_csv('set_assignments.csv')
df

sets = sorted(set(df['Set Name']))
start_date = datetime.datetime(2014, 10, 1, 12)
week = datetime.timedelta(days=7)
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
        set_problems = df[df['Set Name']==set_id]['PG File Path']
        for problem in set_problems:
            def_file.write("{0}\n".format(problem))

