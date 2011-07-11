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
    def __init__(self, path_to_scan, filename_db, filename_db_temp):
        self.path_to_scan = path_to_scan
        self.filename_db_temp = filename_db_temp
        self.filename_db = filename_db ### ~/Dropbox/db/netbook.db ## ~/Dropbox/db/maximus.db # 1TB.db # hp.db
        self.statistics = ''
        self.scan_done = False
    def scan(self):
        #cmd = "updatedb -l 0 -U '" + /home/magnus -o magnus.db
        #
        if os.path.exists(self.path_to_scan):
            cmd = "updatedb -l 0 -U '" + self.path_to_scan + "' -o '" + self.filename_db_temp + "'"
            print cmd
            if config.RUN_UPDATE:
                os.system(cmd)
            print '# done'
            return True
        else:
            print '# ERROR: No such file or directory'
            return False

    def print_statistics(self):
        cmd = "locate -S -d '" + self.filename_db + "'"
        out = commands.getoutput(cmd)
        mmscikit.hr()
        print out
        self.statistics = out
        mmscikit.hr()
        return 

    def temp2db(self):
        cmd = 'mv -v ' + self.filename_db_temp + ' ' + self.filename_db
        #print cmd
        print commands.getoutput(cmd)
        
if __name__ == "__main__":

    if mmscikit.get_hostname() == 'maximus':
        locs = config.LOCS
    else:
        locs = config.LOCS_NETBOOK
    ##
    
    for l in locs:
        mmscikit.hr_text(l)
        path = locs[l]
        print "# PATH", path

        filename_db = config.PATH_DB + l + '.db'
        filename_db_temp = config.PATH_DB + l + '.db.temp'

        print "# creating DB ... ", filename_db
        
        dbf = db(path, filename_db, filename_db_temp)
        if dbf.scan():
            dbf.temp2db()
            dbf.print_statistics()
        
