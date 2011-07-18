#!/usr/bin/python

import mmscikit
import sys
import string
import os
import subprocess
import commands
import re 
import time
import os.path


import config

class db:
    """

    d = db('/home/magnus/', '/home/magnus/Dropbox/db/netbook.db')
    d.scan()
    d.statistics()

    """
    def __init__(self, path_to_scan, filename_db):
        self.path_to_scan = path_to_scan
        self.filename_db = filename_db ### ~/Dropbox/db/netbook.db ## ~/Dropbox/db/maximus.db # 1TB.db # hp.db
        self.statistics = ''
        self.scan_done = False
    def scan(self):
        #cmd = "updatedb -l 0 -U '" + /home/magnus -o magnus.db
        #
        if os.path.exists(self.path_to_scan):
            cmd = "updatedb -l 0 -U '" + self.path_to_scan + "' -n 'Dropbox' -o '" + self.filename_db + "'"
            print cmd
            if config.RUN_UPDATE:
                os.system(cmd)
            mmscikit.print_green('# done')
            return True
        else:
            mmscikit.print_red('# ERROR: No such file or directory')
            return False

    def print_statistics(self):
        cmd = "locate -S -d '" + self.filename_db + "'"
        out = commands.getoutput(cmd)
        mmscikit.hr()
        print out
        self.statistics = out
        mmscikit.hr()
        return 
        
def start():
    if mmscikit.get_hostname() == 'maximus':
        locs = config.LOCS
    else:
        locs = config.LOCS_NETBOOK
    ##

    for l in locs:
        mmscikit.hr_text(l)
        path = locs[l]
      
        mmscikit.print_blue("# PATH: " + path)

        filename_db = config.PATH_DB + l + '.db'
        print "# creating DB ... ", filename_db
        
        dbf = db(path, filename_db)
        if dbf.scan():
            dbf.print_statistics()

if __name__ == "__main__":
    start()

