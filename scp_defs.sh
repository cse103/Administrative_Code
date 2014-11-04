#!/usr/bin/env bash

python CSV_to_defs.py
scp setWeek*.def webwork.cse.ucsd.edu:/opt/webwork/courses/CSE103_Fall14/templates/
