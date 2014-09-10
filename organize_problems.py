#!/usr/bin/env python

import yaml
import argparse
import datetime
import os
import os.path
import logging
import shutil

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger('organize_problems')

def organize_assignments(description_file, base_path, output_path):
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    
    with open(description_file, 'r') as f:
        data = yaml.load(f)
        for assignment in data:
            print assignment['title']
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
            print

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Organize webwork assignments according to the given file')
    parser.add_argument('--file', default='assignments.yml')
    parser.add_argument('--base-path', default='/opt/webwork/courses/CSE103_Fall14/templates')
    parser.add_argument('--output-path', default='/opt/webwork/courses/CSE103_Fall14/templates/Organized')
    args = parser.parse_args()
    organize_assignments(args.file, os.path.expanduser(args.base_path), os.path.expanduser(args.output_path))
