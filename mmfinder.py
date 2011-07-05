import mmscikit
import sys
import string
import os
import subprocess
import commands
import re 
import time

op = {}
op['txt'] = 'gedit '
#op['pdf'] = 'evince '
op['pdf'] = 'okular '
op['odt'] = 'oowriter '
op['doc'] = 'oowriter '

ids = string.ascii_letters

class main:
    def __init__(self):
        self.items = []
    def search(self, word,ext = '', verbose = True):
        mmscikit.hr()
        cmd = "find /home/magnus/ -iname '*" + word + "*" + ext + "*'"
        if verbose:
            print '# cmd', cmd
        out = mmscikit.shell2(cmd)
        mmscikit.hr()
        print
        
        c = 0
        for item in out.strip().split('\n'):
            id = ids[c]
            i = obj(id, item)
            self.items.append(i)
            i.check_filetype()
            i.show()
            c += 1
        print
        mmscikit.hr()

    def get_command(self):
        input = raw_input('What to do? [ao]:')
        if not len(input.strip()):
            print 'exit'
            sys.exit(1)
        id = input[0]
        action = input[1]
        print 'id', id
        print 'action', action

        item = self.items[ids.index(id)]


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
    def show(self):
        if not self.is_empty:
            out = '\t [' + self.filetype + '] ' + self.id + ') '+self.path
            print out
    def check_filetype(self):
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

            if self.filetype == '': ## if still ''
                #print 'out'
                #print out
                self.filetype = 'empty'
                self.is_empty = True
                   
        #print '\t#filetype: ',self.filetype
if __name__ == "__main__":
    os.system('clear')
    mmscikit.banner2('mmfinder.py')
    #for i in range(0,3):
    #    print '.'
    #    time.sleep(0.2)
    while 1:
        m = main()
        if False:
            m.search(sys.argv[1],sys.argv[2])
            m.get_command()
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
                m.get_command()
