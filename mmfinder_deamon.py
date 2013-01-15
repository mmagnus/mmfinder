#!/usr/bin/python

import mmfinder_config as config
import myutilspy
import sys
import string
import os
import subprocess
import commands
import re 
import time
import os.path


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
            dont_db = ' '.join(config.DONT_DB)
            cmd = "updatedb -l 0 -U '" + self.path_to_scan + "' -n '" + dont_db + "' -o '" + self.filename_db + "'"
            print cmd
            if config.RUN_UPDATE:
                os.system(cmd)
            myutilspy.print_green('# done')
            return True
        else:
            myutilspy.print_red('# ERROR: No such file or directory')
            return False

    def print_statistics(self):
        cmd = "locate -S -d '" + self.filename_db + "'"
        out = commands.getoutput(cmd)
        myutilspy.hr()
        print out
        self.statistics = out
        myutilspy.hr()
        return 
        
def start():

    hostname = myutilspy.get_hostname()
    locs = config.HOSTS[hostname]

    for l in locs:
        myutilspy.hr_text(l)
        path = locs[l]
      
        myutilspy.print_blue("# PATH: " + path)

        filename_db = config.PATH_DB + l + '.db'
        print "# creating DB ... ", filename_db
        
        dbf = db(path, filename_db)
        if dbf.scan():
            dbf.print_statistics()

    ## log
    f = open(config.PATH_LOGFILE, 'aw')
    f.write(myutilspy.get_datetime() + '\n')
    f.close()

if __name__ == "__main__":
    start()

