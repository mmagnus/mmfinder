#!/usr/bin/python

import mmfinder_config as config
import sys
import string
import os
import subprocess
import commands
import re 
import time
import os.path

from lib.utils import banner2, hr, get_hostname, hr_text, print_red_and_blue, print_green, print_red, print_blue, get_datetime

class db:
    """

    d = db('/home/magnus/', '/home/magnus/Dropbox/db/netbook.db')
    d.scan()
    d.statistics()

    """
    def __init__(self, path_to_scan, filename_db):
        self.path_to_scan = path_to_scan
        self.filename_db = filename_db
        self.statistics = ''
        self.scan_done = False
    def scan(self):
        if os.path.exists(self.path_to_scan):
            dont_db = ' '.join(config.DONT_DB)
            cmd = "updatedb -l 0 -U '" + self.path_to_scan + "' -n '" + dont_db + "' -o '" + self.filename_db + "'"
            print cmd
            if config.RUN_UPDATE:
                os.system(cmd)
            print_green('# done')
            return True
        else:
            print_red('# ERROR: No such file or directory')
            return False

    def print_statistics(self):
        cmd = "locate -S -d '" + self.filename_db + "'"
        out = commands.getoutput(cmd)
        hr()
        print out
        self.statistics = out
        hr()
        return 
        
def start():

    hostname = get_hostname()
    locs = config.HOSTS[hostname]

    for l in locs:
        hr_text(l)
        path = locs[l]
      
        print_blue("# PATH: " + path)

        filename_db = config.PATH_DB + l + '.db'
        print "# creating DB ... ", filename_db
        
        dbf = db(path, filename_db)
        if dbf.scan():
            dbf.print_statistics()

    ## log
    f = open(config.PATH_LOGFILE, 'aw')
    f.write(get_datetime() + '\n')
    f.close()

if __name__ == "__main__":
    start()

