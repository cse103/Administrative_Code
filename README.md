## Generating Assignments

Webwork allows importing assignment descriptions from def files. In many ways
it's easier to track the problems we use outside of webwork itself, so we have a
few scripts and files to generate the def files for us which we then import into
webwork itself.

All the PG files used in Fall 2014 are located in the
[cse103/PG_files](http://github.com/cse103/PG_files) repository. They were
collected there after an initial selection pass made by Yoav. On the webwork
server, they are under /opt/webwork/courses/{COURSE}/templates/Reorganized
to isolate them from the rest of the files which were kept from previous
quarters.

The file [set_assignments.csv](set_assignments.csv) is a table which maps PG
files to sets. The columns include Set Name, PG File Path,Topic, Used, and
Original Path for files that were previously in other locations.

The Python script [CSV_to_defs.py](CSV_to_defs.py) takes the file
set_assignments.csv and uses it to generate def files for each set name given.
It generates due dates automatically based on the lexicographic sort order of
the set names (this could be improved).

The Bash script [scp_defs.sh](scp_defs.sh) runs the above Python script and then
copies the generated def files to the appropriate location on the webwork server.
Once the def files are on the server, you should delete any existing versions of
assignments you want to re-import and then go to the import page in the homework
sets editor and select the def files that you want to import.'
