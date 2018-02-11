# move_paid_csv.py
# 2/6/18

# Copies Windows generated csv file from Linux-share directory (on Win box)
# to Windows-share directory (within Linux)

import shutil
from pathlib2 import Path

def main():
    old_dir = '/media/smenon/Windows7_OS/Documents and Settings/Sanjay/Desktop/Linux-share/'
    new_dir = '/home/smenon/Desktop/Windows-share/'

    filename = 'LB_paid.csv'

    in_file = Path(old_dir + filename)

    if in_file.is_file():
        print "All good"
        shutil.copy (old_dir + filename, new_dir)
    else:
        print "LB input file is not present"
        exit(1)

main()
