#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
mmfinder: the tool to find different types of files on many machines
"""
from myutilspy import banner2, hr, get_hostname, hr_text, print_red_and_blue
from sys import exit, argv
from string import ascii_letters
from os import path, getcwd, system
from subprocess import Popen
from commands import getoutput
from re import compile, search, I
from time import sleep
#from ipdb import set_trace
from optparse import OptionParser
from mmfinder_deamon import start as start_deamon
from django.conf import settings
from subprocess import Popen


from config import PLACES_LOCAL, PLACES_GLOBAL, PATH_DB, FF_SQLITE_DATABASE, EXTENSIONS_OF_DOCUMENTS, EXTENSIONS_OF_MEDIA, HTML_FN, HTML_CMD, GREP_CMD

VERSION = '0.2'
IDS = ascii_letters

class main:

    def __init__(self):
        self.items = []

    def get_command(self):
        """
        !!! not used in this VERSION !!!
        """
        op = {}
        op['txt'] = 'gedit '
        op['pdf'] = 'mmpdf.sh '
        op['odt'] = 'oowriter '
        op['doc'] = 'oowriter '


        input = raw_input('What to do? [ids action] [abc o]:')
        if not len(input.strip()):
            print 'exit'
            exit(1)

        # program selection a-b, or *, or aegh

        ids, action = input.split()  # 'abc o'

        # *
        if ids == '*':
            ids = IDS
        # change a-c -> abc
        if search('-',  ids):
            start, end = ids.split('-')
            print start, end
            print IDS.index(start)
            ids = IDS[IDS.index(start):IDS.index(end) + 1]
            print ids
        # ** end ** change a-c -> abc

        print 'ids', ids
        print 'action', action

        for item in self.items:  # for each item
            if search(item.id, ids):
                if not item.is_empty:
                    #item = self.items[ids.index(id)]

                    #exit(1)

                    if action == 'g':
                        cmd = 'cd ' + item.path

                    if action == 'q' or id == '':
                        print 'exit'
                        exit(1)

                    if action == 'o':
                        cmd = op[item.filetype] + ' ' + "'" + item.path + "' "
                        print cmd
                        cmd_text = "opening " + item.path + ' by ' + \
                            op[item.filetype] + ' ...'
                    arguments = shlex.split(cmd)
                    #print arguments
                    print cmd_text
                    Popen(arguments)
                    #subprocess.call(arguments)

    def search(self, arguments,
               opt, ext='', method='find', verbose=True):
        list_with_action = True
        hr()

        import sqlite3
        
        if opt.bookmarks:
            conn = sqlite3.connect(FF_SQLITE_DATABASE)
            c = conn.cursor()
            c.execute("select title, url from moz_places;")
            conn.commit()
            results = c.fetchall()
            if 1:
                for r in results:
                    title = r[0]
                    if title:
                        pass
                    else:
                        title = ''
                    line = title + r[1]

                    ## stupid way
                    word = arguments[0]
                    try:
                        word2 = arguments[1]
                    except IndexError:
                        word2 = ''

                    if compile(word, I).search(line) and compile(word2, I).search(line):
                        print_red_and_blue(title, ' ' + r[1])
                exit(1)

        if opt.bookmarks_folder:
            """
            dirty but works
            """
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME':  FF_SQLITE_DATABASE,
                    'HOST': '',
                    'PORT': '',
                    }
                }
            settings.configure(DATABASES=DATABASES)

            from orm.models import MozAnnoAttributes, MozAnnos, MozBookmarks, MozBookmarksRoots, MozFavicons, MozHistoryvisits, MozInputhistory, MozItemsAnnos, MozKeywords, MozPlaces, SqliteStat1

            show_path = False

            phrase = argv[2].strip()
            print 'phrase:', phrase, '\n'

            bookmarks = MozBookmarks.objects.all()

            c = 0
            for b in bookmarks:
                if b.fk is None and b.title != '':  # b.fk = has bookmarks
                    try:
                        path = b.title.strip()
                    except AttributeError:
                        print '-- b.title:', b.title
                    while b.parent != 1:
                        parent = MozBookmarks.objects.get(id=b.parent)
                        path = parent.title.strip() + '/' + path
                        b = parent
                    if show_path:
                        print path
                    if path.lower().find(phrase.lower()) > -1:
                        print path
                c += 1
            exit(1)

        if opt.invert:
            arguments.reverse()

        words = '*' + '*'.join(arguments) + '*'  # '*a*b*c*'
        words_rex = '.*' + '.*'.join(arguments) + '.*'  # '.*a.*b*.c*'


        if opt.global_search:
            places = PLACES_GLOBAL
        else:
            places = PLACES_LOCAL
            places.append(get_hostname())

        if opt.grep_here:
            places = ['current dir']
            status = 'grepping the current directory'
            cmd = GREP_CMD + " '" + words.replace('*','') + "' *"
            if opt.verbose: print 'cmd: ', cmd
            out = getoutput(cmd).strip()
            for l in out.split('\n'):
                if l.find(':')>-1:
                    try:
                        filename, text = l.split(':')
                        filename += ':'
                    except:
                        items = l.split(':')
                        filename = items[0]
                        text = ':'.join(items[1:])
                    print_red_and_blue(filename, text)

                elif l.find('-')>-1:
                    try:
                        filename, text = l.split('-')
                        filename += '-'
                    except:
                        items = l.split('-')
                        filename = items[0]
                        text = '-'.join(items[1:])
                    print_red_and_blue(filename, text)
                else:
                    print l
            exit(1)

        if opt.wholename:  # or basename
            wholename_or_basename = ' -w '
        else:
            wholename_or_basename = ' -b '
        #
        if opt.find_dir:
            places = ['find directories@' + get_hostname()]
        if opt.find_find:
            places = ['find@' + get_hostname()]
        if opt.find_tu:
            places = ['find here -t tu@' + get_hostname()]

        html_hits = ''
        c = 1
        for p in places:
            hr_text(p + '...')
            html_hits += '#' + p + '\n'
            #if method == 'locate_local':
            # @@@@
            # -e existing a co ze zdalnymi bazami?!?!
            #
            # TODO word2
            #
            status = ''

            if opt.pdf_find:
                status = 'pdf searching...'
                cmd = "locate -d " + PATH_DB + p + '.db' + " " + \
                    wholename_or_basename + " -i -r '" + words_rex + "pdf$'"
            elif opt.document_find:
                status = 'document searching...'
                extensions = '$|'.join(EXTENSIONS_OF_DOCUMENTS)
                cmd = "locate -d " + PATH_DB + p + '.db' + " " + \
                    wholename_or_basename + " -i --regex '" + \
                    words_rex + ".*(" + extensions + ")'"
            elif opt.find_media:
                status = 'document searching...'
                extensions = '$|'.join(EXTENSIONS_OF_MEDIA)
                cmd = "locate -d " + PATH_DB + p + '.db' + " " + \
                    wholename_or_basename + " -i --regex '" + \
                    words_rex + ".*(" + extensions + ")'"
            elif opt.rex:
                status = 'rex searching...'
                word = arguments[0]  # <--- !!!
                cmd = "locate -d " + PATH_DB + p + '.db' + " " + \
                    wholename_or_basename + " -i --regex '" + word + "'"

            elif opt.find_tu:
                status = 'finding here (tutaj)...'
                cmd = "find '" + getcwd() + "' -iname '" + words + "'"
            elif opt.find_find:
                status = 'finding /home/...'
                cmd = "find ~ -iname '" + words + "'"
            elif opt.find_dir:
                status = 'finding a dir /...'
                cmd = "find ~ -iname '" + words + "' -type d"  # very slow :-(

                if False:
                    if word.startswith('^'):
                        word_without = word.replace('^', '')
                        cmd = "locate -d " + PATH_DB + p + '.db' + \
                            " -e -i -r  '/" + word_without + \
                            "*' | xarguments file"
                            #locate -r '/*python2.7*/' | less
                    else:
                        cmd = "locate -d " + PATH_DB + p + '.db' + \
                            " -e -i -r  '/*" + word + "*/'" \
                            #locate -r '/*python2.7*/' | less
            else:

                status = 'basic search...'
                cmd = "locate -d " + PATH_DB + p + '.db' + \
                    " " + wholename_or_basename + " -i '" + words + "'"
            if opt.un_grep:
                cmd = cmd + " | grep -v '" + opt.un_grep + "'"

            if opt.verbose:
                print '# status:', status
                print '# cmd', cmd

            ## execute!
            out = getoutput(cmd).strip()
            
            if opt.dev:
                hr_text('dev::out')
                print out
                hr()

            if out and list_with_action:
                for item in out.strip().split('\n'):
                    ############################ @@ BUG @@ id = IDS[c]
                    id = 'a'  # TO FIX
                    i = obj(id, item)
                    self.items.append(i)
                    i.check_filetype()
                    #print i.is_dir
                    #if i.is_dir and find_dir:
                    #    i.show()
                    #print 'x'
                    #if not find_dir:
                    hit = i.show(opt.show_hash, opt.not_less,
                                 opt.noncolor, opt.www_browser, c)
                    if opt.www_browser:
                        html_hits += hit + '\n'
                    c += 1
                print

            # and out becuase don't 'press key' for empty outputs
            if opt.key and out:
                raw_input('[press key]')

        if opt.www_browser:

            html_text = '<pre>'
            html_text += html_hits.replace('\n', '</br>')
            html_text += '<pre>'

            fn = HTML_FN
            f = open(fn, 'w')
            f.write(html_text)
            f.close()

            cmd = HTML_CMD + ' ' + fn
            print cmd
            system(cmd)

        ##
        paths_text_file.write(mmterminalpathtext)
        paths_text_file_to_open.write(mmterminalpathtext_to_open)
        paths_text_file.close()

class obj:
    def __init__(self, id, path):
        self.path = path
        self.id = id
        self.filetype = ''
        self.is_pdf = False
        self.is_empty = False

    def show(self, show_hash, not_less, noncolor, www_browser, c):
        """
        * input:
         - show_hash **is not used**
         - less: True/False show only first line of a hit, dont show path file:///
         - noncolor: True/False use color to show a path and a filename
         - www_browser: save the result as a html file and open it in www_browser

        * output:
        - '\tfile:///home/magnus/Dropbox/pdf\n\tfile:///home/magnus/Dropbox/pdf/XXXXXXX.pdf'
        or
        html code for opening in www_browser
        """
        #if not self.is_empty:
            # out = '\t [' + self.filetype + '] ' + self.id + ") \
                # file://"+self.path.replace(' ','\ ')+""
            #out = '\t [' + self.filetype + '] ' + self.id + ") \
                # file://"+self.path.replace(' ','%20')+""
        if noncolor:
            print '\t\'' + path.dirname(self.path) \
                  + '/' + path.basename(self.path) + "'"
        else:
            print_red_and_blue(str(c) + '\t\'' + \
                               path.dirname(self.path) + \
                               '/', '' + path.basename(self.path) + "'")
        ## hack #1
        out = ''
        dir_file = True
        if dir_file:
            out = "\tfile://" + \
                path.dirname(self.path).strip().replace(' ', '%20') + "\n"
                #out = '\t [' + self.filetype + '] ' + \
                #self.id + ") " + '' + " \t\tfile://"+
                #self.path.replace(' ','%20')+""
        out += "\tfile://" + self.path.replace(' ', '%20') + ""
            # @todo
            #if show_hash:
            #    out += '\n\t' + hash_file(self.path)[0]

            #out = '\t [' + self.filetype + '] ' + self.id + ") \
                # file:'//"+self.path+"'" # NO
            #out = '\t [' + self.filetype + '] ' + self.id + ") \
            # 'file://"+self.path+"'" # NO
        if not_less:
            print out
        return out.replace('file://', '').replace('%20',' ')


    def check_filetype(self):
        """

        problem.. jezeli plik nie wpadnie w zadna z kategorii
        to (czyli self.filetype == '') to wtedy dostaje is_empty

magnus@maximus:~/Dropbox/workspace/mmfinder$ file
/home/magnus/Dropbox/workspace/myutil/backup_mysql_maximus.sh
/home/magnus/Dropbox/workspace/myutil/backup_mysql_maximus.sh:
Bourne-Again shell script text executable


        """
        if not path.isfile(self.path):
            self.is_dir = True
            self.filetype = 'dir'
        else:
            self.is_dir = False

            cmd = "file '" + self.path + "'"
            out = getoutput(cmd)
            #print '# out',out

            if search('ASCII text', out):
                self.is_txt = True
                self.filetype = 'txt'

            if search('PDF document', out):
                self.is_pdf = True
                self.filetype = 'pdf'

            if search('OpenDocument Text', out):
                self.is_odt = True
                self.filetype = 'odt'

            if search('CDF V2 Document', out):
                self.is_doc = True
                self.filetype = 'doc'

            if self.filetype == '':  # if still ''
                #print 'out'
                #print out
                self.filetype = 'empty'
                self.is_empty = True
        #print '\t#filetype: ',self.filetype


def option_parser():
    """
    """
    description = ''
    version = VERSION
    usage = '%prog <options> word word word word'
    parser = OptionParser(description=description,
                              version=version,
                              usage=usage)
    parser.add_option("-u", "--update_db", dest="update_db",
                      default=False, help="force to update databases",
                      action="store_true")
    parser.add_option("-l", "--not_less", dest="not_less",
                      default=False, help="not_less, print extra lines",
                      action="store_true")
    parser.add_option("-g", "--global_search", dest="global_search",
                      default=False, help="search globally all PLACES",
                      action="store_true")
    parser.add_option("-d", "--find_dir", dest="find_dir",
                      default=False, help="search only for directories",
                      action="store_true")
    parser.add_option("-f", "--find_find", dest="find_find",
                      default=False, help="search only local via find ~",
                      action="store_true")
    parser.add_option("-p", "--pdf_find", dest="pdf_find",
                      default=False, help="search only for PDFs",
                      action="store_true")
    parser.add_option("-s", "--show_hash", dest="show_hash",
                      default=False, help="show_hash",
                      action="store_true")
    parser.add_option("-o", "--document_find", dest="document_find",
                      default=False,
                      help="document_find (documents are odt, doc)",
                      action="store_true")
    parser.add_option("-t", "--find_tu", dest="find_tu",
                      default=False, help="find in a folder",
                      action="store_true")
    parser.add_option("-e", "--dev", dest="dev",
                      default=False,
                      help="development version.. lots of prints",
                      action="store_true")
    parser.add_option("-k", "--key", dest="key",
                      default=False,
                      help="press key every place",
                      action="store_true")
    parser.add_option("-m", "--find_media", dest="find_media",
                      default=False,
                      help="find media (mp3, avi, mp4 and so on)",
                      action="store_true")
    parser.add_option("-r", "--rex", dest="rex",
                      default=False,
                      help="--regex '.*ods$'", action="store_true")
    parser.add_option("-x", "--un_grep", dest="un_grep",
                      default=False, help="--regex '.*ods$'",
                      action="store", type="string")
    parser.add_option("-w", "--wholename", dest="wholename",
                      default=False,
                      help="-w -match only the whole path " +
                      "name against the specified patterns",
                      action="store_true")
    parser.add_option("-b", "--bookmarks", dest="bookmarks",
                      default=False, help="-b search firefox bookmarks'",
                      action="store_true")
    parser.add_option("-y", "--bookmarks_folder", dest="bookmarks_folder",
                      default=False,
                      help="-y search firefox bookmark folders'",
                      action="store_true")
    parser.add_option("-v", "--verbose", dest="verbose",
                      default=False, help="-v verbose'",
                      action="store_true")
    parser.add_option("-i", "--invert", dest="invert",
                      default=False,
                      help="-i invert word1 word2 word3 --> word3 word2 word1",
                      action="store_true")
    parser.add_option("-c", "--grep_here", dest="grep_here",
                      default=False,
                      help="run grep search in the current folder",
                      action="store_true")
    parser.add_option("-n", "--noncolor", dest="noncolor",
                      default=False,
                      help="dont show colors, useful if you pipe an output",
                      action="store_true")
    parser.add_option("-a", "--www_browser", dest="www_browser",
                      default=False,
                      help="open an output in www browser",
                      action="store_true")

    (opt, arguments) = parser.parse_args()

    #@@
    #if not arguments:
    #    parser.print_help()
    #    exit(1)
    if opt.update_db:
        print 'mmfinder_deamon start...'
        start_deamon()
        hr()
        print 'mmfinder_deamon [done]'
        sleep(2)

    if opt.dev:
        print '# opt', opt
    return arguments, opt


def start():
    banner2('mmfinder.py')
    arguments, opt = option_parser()

    if arguments:
        m = main()
        if True:
            #show_hash, global_search,find_dir, find_find,pdf_find ,'')
            m.search(arguments, opt)
            #m.get_command()
        ###########################################################
        ## else:
        ##     what_to_find = raw_input('>>> ')
        ##     if what_to_find == '':
        ##         pass
        ##     else:
        ##         if len(what_to_find.split()) == 2:
        ##             what_to_find1, what_to_find2 = what_to_find.split()
        ##             m.search(what_to_find1, what_to_find2)
        ##         else:
        ##             m.search(what_to_find)
        ##         #m.get_command()

if __name__ == "__main__":
    start()
