#!/usr/bin/env python

import yaml
import argparse
import datetime
import os
import os.path
import logging
import shutil
import pytz

import dateutil.parser

pt = pytz.timezone('US/Pacific')
def timestamp_constructor(loader, node):
    return dateutil.parser.parse(node.value).astimezone(pt)
yaml.add_constructor(u'tag:yaml.org,2002:timestamp', timestamp_constructor)

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger('organize_problems')

def organize_assignments(description_file, base_path, output_path):
    """
    openDate          = 10/01/2012 at 11:02am PDT
    dueDate           = 12/14/2013 at 03:00pm PST
    answerDate        = 12/14/2013 at 03:00pm PST
    paperHeaderFile   = defaultHeader
    screenHeaderFile  = defaultHeader
    problemList       = 
    setTestPreparation/cond15_hint.pg, 1, 1 
    setTestPreparation/cond14_hint.pg, 1, 1 
    setTestPreparation/Bayes2_hint.pg, 1, 1 
    setTestPreparation/Bayes7_hint.pg, 1, 1 
    setTestPreparation/stat212-HW05-02_hint.pg, 1, 1 
    setTestPreparation/ur_pb_7_2_hint.pg, 1, 1 
    setTestPreparationST/prob5.pg, 1, 1 
    setAssignment18/RandAlgs_2_2.pg, 1, -1 

    """
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    
    with open(description_file, 'r') as f:
        data = yaml.load(f)
        for assignment in data:
            print assignment['title']
            def_path = os.path.join(output_path, "set{0}.def".format(assignment['title']))
            with open(def_path, 'w') as def_file:
                def_file.write("openDate          = {0}\n".format(
                    assignment['open_date'].strftime('%m/%d/%Y at %I:%M%p %Z')))
                def_file.write("dueDate           = {0}\n".format(
                               assignment['close_date'].strftime('%m/%d/%Y at %I:%M%p %Z')))
                def_file.write("answerDate        = {0}\n".format(
                               assignment['close_date'].strftime('%m/%d/%Y at %I:%M%p %Z')))
                def_file.write("paperHeaderFile   = defaultHeader\n")
                def_file.write("screenHeaderFile  = defaultHeader\n")
                def_file.write("problemList       =\n")
                for topic, problems in assignment['problems'].iteritems():
                    print topic
                    topic_dir = os.path.join(output_path, topic)
                    if not os.path.isdir(topic_dir):
                        os.makedirs(topic_dir)
                    for problem_path in problems:
                        abs_path = os.path.join(base_path, problem_path)
                        if not os.path.isfile(abs_path):
                            logger.warn("File may be missing: %s", os.path.join(base_path, problem_path))
                        else:
                            filename = os.path.basename(problem_path)
                            new_path = os.path.join(output_path, topic, filename)
                            if os.path.isfile(new_path):
                                logger.warn("File %s exists, adding suffix", filename)
                                i = 0
                                base, ext = os.path.splitext(filename)
                                while os.path.isfile(new_path):
                                    i += 1
                                    new_path = os.path.join(output_path, topic, "{0}_{1}.{2}".format(base, i, ext))
                            logger.info("New path: %s", new_path)
                            shutil.copyfile(abs_path, new_path)
                            relative_path = new_path.split('templates/')[1]
                            def_file.write(relative_path)
                            def_file.write('\n')
            print

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Organize webwork assignments according to the given file')
    parser.add_argument('--file', default='assignments.yml')
    parser.add_argument('--base-path', default='/opt/webwork/courses/CSE103_Fall14/templates')
    parser.add_argument('--output-path', default='/opt/webwork/courses/CSE103_Fall14/templates/Organized')
    args = parser.parse_args()
    organize_assignments(args.file, os.path.expanduser(args.base_path), os.path.expanduser(args.output_path))
