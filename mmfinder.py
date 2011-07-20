#!/usr/bin/python

VERSION = '0.09'

import mmscikit
import sys
import string
import os
import subprocess
import commands
import re 
import time
from optparse import OptionParser
import config
import mmfinder_deamon

op = {}
op['txt'] = 'gedit ' 
#op['pdf'] = 'evince '
#op['pdf'] = 'okular '
op['pdf'] = 'mmpdf.sh '
op['odt'] = 'oowriter '
op['doc'] = 'oowriter '

IDS = string.ascii_letters


class main:
    def __init__(self):
        self.items = []

    def load_db(self):
        pass

    def search(self, word,word2, opt, ext = '', method = 'find', verbose = True):

        verbose_cmd = True
        verbose_out = False
        list_with_action = True
        
        mmscikit.hr()
        # @@@        
        if opt.global_search:
            PLACES = config.PLACES
        else:
            PLACES = config.PLACES_LOCAL
            PLACES.append(mmscikit.get_hostname())
        # @@@
        if opt.find_dir:
            PLACES = ['find directories@' + mmscikit.get_hostname()]
        if opt.find_find:
            PLACES = ['find@' + mmscikit.get_hostname()]
        if opt.find_tu:
            PLACES = ['find here -t tu@' + mmscikit.get_hostname()]
        for p in PLACES:
            mmscikit.hr_text( p + '...' )
            #if method == 'locate_local':
            # @@@@
            # -e existing a co ze zdalnymi bazami?!?!
            #
            # TODO word2
            #
            
            if opt.pdf_find:

            if opt.document_find:
                cmd = "locate -d " + config.PATH_DB + p + '.db' + " -b -i --regex '.*" + word + ".*" + word2 + ".*(doc$|odt$)'"
                
            elif opt.find_tu:
                cmd = "find " + os.getcwd() + " -iname '*" + word + "*" + word2 +"'"
            elif opt.find_find:
                cmd = "find ~ -iname '*" + word + "*" + word2 +"'"
            elif opt.find_dir:
                cmd = "find ~ -iname '*" + word + "*" + word2 + "' -type d" ## very slow :-(
                if False:
                    if word.startswith('^'):
                        word_without = word.replace('^','')
                        cmd = "locate -d " + config.PATH_DB + p + '.db' + " -e -i -r  '/" + word_without +"*' | xargs file" #locate -r '/*python2.7*/' | less
                    else:
                        cmd = "locate -d " + config.PATH_DB + p + '.db' + " -e -i -r  '/*" + word +"*/'" #locate -r '/*python2.7*/' | less
            else:
                cmd = "locate -d " + config.PATH_DB + p + '.db' + " -b -i '*" + word + "*"+ word2 +"*'"
            # @@@@
            if verbose_cmd:
                print '# cmd', cmd
            #out = mmscikit.shell(cmd)
            #os.system(cmd)
            out = commands.getoutput(cmd).strip()

            if verbose_out:
                print out

            if out and list_with_action:
                #mmscikit.hr()
                c = 0
                for item in out.strip().split('\n'):
                    ########################################### @@ BUG @@ id = IDS[c]
                    id = 'a' ### TO FIX

                    i = obj(id, item)
                    self.items.append(i)
                    i.check_filetype()
                    #print i.is_dir
                    #if i.is_dir and find_dir:
                    #    i.show()
                    #print 'x'
                    #if not find_dir:
                    i.show(opt.show_hash)
                                            
                    c += 1
                print

    def get_command(self):
        input = raw_input('What to do? [ids action] [abc o]:')
        if not len(input.strip()):
            print 'exit'
            sys.exit(1)

        # zaprogramuj przedzialy a-b, lub *, lub aegh

        ids, action = input.split() ## 'abc o'

        # *
        if ids == '*': 
            ids = IDS
        # change a-c -> abc
        if re.search('-',  ids):
            start, end = ids.split('-')
            print start, end
            print IDS.index(start)
            ids = IDS[ IDS.index(start): IDS.index(end)+1 ]
            print ids
        # ** end ** change a-c -> abc

        print 'ids', ids
        print 'action', action

        for item in self.items: ## for each item
            if re.search(item.id, ids):
                if not item.is_empty:
                    #item = self.items[ids.index(id)]

                    #sys.exit(1)

                    if action == 'g':
                        cmd = 'cd ' + item.path

                    if action == 'q' or id == '':
                        print 'exit'
                        sys.exit(1)

                    if action == 'o':
                        cmd = op[item.filetype] + ' ' + "'" + item.path + "' "
                        print cmd
                        cmd_text = "opening " + item.path + ' by ' + op[item.filetype] + ' ...'

                    import shlex
                    args = shlex.split(cmd)
                    #print args
                    print cmd_text
                    subprocess.Popen(args)
                    #subprocess.call(args)

                #print out
class obj:
    def __init__(self, id, path):
        self.path = path
        self.id = id
        self.filetype = ''
        self.is_pdf = False
        self.is_empty = False

    def show(self, show_hash):
        #if not self.is_empty:
            #out = '\t [' + self.filetype + '] ' + self.id + ") file://"+self.path.replace(' ','\ ')+""
            #out = '\t [' + self.filetype + '] ' + self.id + ") file://"+self.path.replace(' ','%20')+""
            print
            mmscikit.print_red('\t' + os.path.dirname(self.path).strip()+'/', newline = False)
            mmscikit.print_blue(''+os.path.basename(self.path))
            out = ''
            
            ### 
            dir_file = True
            
            if dir_file:
                out = "\tfile://"+os.path.dirname(self.path).strip().replace(' ','%20')+"\n"
            #out = '\t [' + self.filetype + '] ' + self.id + ") " + '' + " \t\tfile://"+self.path.replace(' ','%20')+""
            out += "\tfile://"+self.path.replace(' ','%20')+""
            if show_hash:
                out += '\n\t'+ mmscikit.hash_file(self.path)[0]
            #out = '\t [' + self.filetype + '] ' + self.id + ") file:'//"+self.path+"'" # NO
            #out = '\t [' + self.filetype + '] ' + self.id + ") 'file://"+self.path+"'" # NO
            print out

    def check_filetype(self):
        """

        problem.. jezeli plik nie wpadnie w zadna z kategorii to (czyli self.filetype == '') to wtedy dostaje is_empty

magnus@maximus:~/Dropbox/workspace/mmfinder$ file /home/magnus/Dropbox/workspace/myutil/backup_mysql_maximus.sh 
/home/magnus/Dropbox/workspace/myutil/backup_mysql_maximus.sh: Bourne-Again shell script text executable


        """
        if not os.path.isfile(self.path):
            self.is_dir = True
            self.filetype = 'dir'
        else:
            self.is_dir = False

            cmd = "file '" + self.path + "'"
            out = commands.getoutput(cmd)
            #print '# out',out

            if re.search('ASCII text',out):
                self.is_txt = True
                self.filetype = 'txt'

            if re.search('PDF document',out):
                self.is_pdf = True
                self.filetype = 'pdf'

            if re.search('OpenDocument Text',out):
                self.is_odt = True
                self.filetype = 'odt'

            if re.search('CDF V2 Document', out):
                self.is_doc = True
                self.filetype = 'doc'

            if self.filetype == '': ## if still '' ###### 
                #print 'out'
                #print out
                self.filetype = 'empty'
                self.is_empty = True
                   
        #print '\t#filetype: ',self.filetype

def option_parser():
    """
    """
    description=''
    version=VERSION
    usage='%prog <options> word word2'
    parser = OptionParser(description=description,
                              version=version,
                              usage=usage)
    parser.add_option("-u", "--update_db", dest="update_db", default=False,help="force to update databases", action="store_true")
    #parser.add_option("-l", "--local_search", dest="local_search", default=True,help="search only local host i dropbox", action="store_true")
    parser.add_option("-g", "--global_search", dest="global_search", default=False,help="search globally all PLACES", action="store_true")
    parser.add_option("-d", "--find_dir", dest="find_dir", default=False,help="search only for directories", action="store_true")
    parser.add_option("-f", "--find_find", dest="find_find", default=False,help="search only local via find ~", action="store_true")
    parser.add_option("-p", "--pdf_find", dest="pdf_find", default=False,help="search only for PDFs", action="store_true")
    parser.add_option("-s", "--show_hash", dest="show_hash", default=False,help="show_hash", action="store_true")
    parser.add_option("-o", "--document_find", dest="document_find", default=False,help="document_find (documents are odt, doc)", action="store_true")

    parser.add_option("-t", "--find_tu", dest="find_tu", default=False,help="find in a folder", action="store_true")

    (opt, args) = parser.parse_args()

    #@@
    #if not args:
    #    parser.print_help()
    #    sys.exit(1)
    
    if opt.update_db:
        print 'mmfinder_deamon start...'
        mmfinder_deamon.start()
        mmscikit.hr()
        print 'mmfinder_deamon [done]'
        time.sleep(2)


    return args, opt

def start():
    mmscikit.banner2('mmfinder.py')
    args, options = option_parser()
    # @@@
    if args:
        m = main()
        if True:
            args1 = args[0]
            try:
                arg2 = args[1]
            except:
                arg2 = ''
            m.search(args1,arg2,options)#show_hash, global_search,find_dir, find_find,pdf_find ,'')
            #m.get_command()
        else:
            what_to_find = raw_input('>>> ')
            if what_to_find == '':
                pass
            else:
                if len(what_to_find.split()) == 2:
                    what_to_find1, what_to_find2 = what_to_find.split()
                    m.search(what_to_find1, what_to_find2)
                else:
                    m.search(what_to_find)
                #m.get_command()

if __name__ == "__main__":
    start()
