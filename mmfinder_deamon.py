#!/usr/bin/python
#-*-coding: utf-8 -*-
"""

a deamon for collecting data for mmfinder

not pretty.. full of quick-and-dirty hacks .. but works :-)

"""
__author__ = "Marcin Magnus"
__copyright__ = "Copyright 2010, Marcin Magnus"
__license__ = "GPL"
__maintainer__ = "Marcin Magnus"
__email__ = "mag_dex@o2.pl"
__status__ = "Development"
__version__ = '0.98 alpha'

import os
import commands
import os.path

import mmfinder_config as config

from lib.utils import banner2, hr, get_hostname, hr_text, print_red_and_blue, print_green, print_red, print_blue, get_datetime


class Database:
    """
    Class for database that collets data and print statistics.

    Basic usage:

    d = Database('/home/magnus/', '/home/magnus/Dropbox/db/netbook.db')
    d.scan()
    d.statistics()
    """
    def __init__(self, path_to_scan, filename_db):
        self.path_to_scan = path_to_scan
        self.filename_db = filename_db
        self.statistics = ''
        self.scan_done = False

    def scan(self):
        """
        Scans to for files. Prints output for operation:

        # PATH: /home/magnus/Dropbox
        # creating DB ...  /home/magnus/Dropbox/workspace/mmfinder/db/dropbox.db
        updatedb -l 0 -U '/home/magnus/Dropbox' -n 'Dropbox  Trash english-lingXwavsOnline backups-snapshots .libreoffice .dropbox.cache pubmex-all-pdfs-shit-test' -o '/home/magnus/Dropbox/workspace/mmfinder/db/dropbox.db'
        # done
        """
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
        """
        Shows basic statistics, e.g.

        Database /home/magnus/Dropbox/workspace/mmfinder/db/dropbox.db:
        6,683 directories
        39,743 files
        3,434,386 bytes in file names
        1,456,819 bytes used to store database
        """
        cmd = "locate -S -d '" + self.filename_db + "'"
        out = commands.getoutput(cmd)
        hr()
        print out
        self.statistics = out
        hr()


def start():
    """
    Starts the main program.
    """
    hostname = get_hostname()
    locs = config.HOSTS[hostname]

    for l in locs:
        hr_text(l)
        path = locs[l]

        print_blue("# PATH: " + path)

        filename_db = config.PATH_DB + l + '.db'
        print "# creating DB ... ", filename_db

        dbf = Database(path, filename_db)
        if dbf.scan():
            dbf.print_statistics()

    # simply logging
    f = open(config.PATH_LOGFILE, 'aw')
    f.write(get_datetime() + '\n')
    f.close()

if __name__ == "__main__":
    start()
