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

def organize_assignments(description_file, output_path):
    """

    """
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    out_path = os.path.join(output_path, 'set_assignments.csv')
    with open(description_file, 'r') as f, open(out_path, 'w') as outf:
        data = yaml.load(f)
        for assignment in data:
            print assignment['title']
            for topic, problems in assignment['problems'].iteritems():
                print topic
                topic_dir = os.path.join(output_path, topic)
                for problem_path in problems:
                    filename = os.path.basename(problem_path)
                    new_path = os.path.join(output_path, topic, filename)
                    logger.info("New path: %s", new_path)
                    outf.write('"{0}",\t"{1}"\n'.format(assignment['title'], new_path))
            print

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Organize webwork assignments according to the given file')
    parser.add_argument('--file', default='assignments.yml')
    parser.add_argument('--output-path', default='/opt/webwork/courses/CSE103_Fall14/templates/Organized')
    args = parser.parse_args()
    organize_assignments(args.file, os.path.expanduser(args.output_path))
