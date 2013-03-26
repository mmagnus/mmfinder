#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""

a tool for finding your files across different machines!

not pretty.. full of quick-and-dirty hacks .. but works :-)

"""
__author__ = "Marcin Magnus"
__copyright__ = "Copyright 2010, Marcin Magnus"
__license__ = "GPL"
__maintainer__ = "Marcin Magnus"
__email__ = "mag_dex@o2.pl"
__status__ = "Development"
__version__ = '0.98 alpha'

from sys import exit, argv
from string import ascii_letters
from os import path, getcwd, system, sep
from subprocess import Popen
from commands import getoutput
from re import compile, search, I
from time import sleep
from optparse import OptionParser
from getpass import getuser

import getpass


from mmfinder_deamon import start as start_deamon

from lib.utils import banner2, hr, get_hostname, hr_text, print_red_and_blue, check_user_configuration
from mmfinder_config import PLACES_LOCAL, PLACES_GLOBAL,\
PATH_DB, FF_SQLITE_DATABASE,\
EXTENSIONS_OF_DOCUMENTS, EXTENSIONS_OF_MEDIA, HTML_FN, HTML_CMD, GREP_CMD

IDS = ascii_letters


class App:
    """
    Class for the main app
    """
    def __init__(self):
        """
        Inits the main app.
        """
        self.items = []

    def search(self, arguments, opt):
        """
        This searches :-)

        This function is way too big and should be split up
        (it has 267 lines and up to 45 local variables!)

        * input:

        - arguments & opt based on cmd input by user
        """
        list_with_action = True

        hr()

        # if x 2 related to firefox's bookmarks
        if opt.bookmarks:
            # sqlite3 is required!
            import sqlite3
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

                    # a stupid way
                    word = arguments[0]
                    try:
                        word2 = arguments[1]
                    except IndexError:
                        word2 = ''

                    if compile(word, I).search(line) \
                        and compile(word2, I).search(line):
                        print_red_and_blue(title, ' ' + r[1])
                exit(1)

        if opt.bookmarks_folder:
            # dirty but works
            # django required!
            try:
                from django.conf import settings
            except ImportError:
                print 'ImportError: Install python-django to run this feature: sudo apt-get install python-django or sudo pip install django'
                exit(1)
                
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME':  FF_SQLITE_DATABASE,
                    'HOST': '',
                    'PORT': '',
                    }
                }
            settings.configure(DATABASES=DATABASES)

            from orm.models import MozBookmarks

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

        # main search body
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
            cmd = GREP_CMD + " '" + words.replace('*', '') + "' *"
            if opt.verbose:
                print 'cmd: ', cmd
            out = getoutput(cmd).strip()
            for l in out.split('\n'):
                if l.find(':') > -1:
                    try:
                        filename, text = l.split(':')
                        filename += ':'
                    except:
                        items = l.split(':')
                        filename = items[0]
                        text = ':'.join(items[1:])
                    print_red_and_blue(filename, text)

                elif l.find('-') > -1:
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

        if opt.find_dir:
            places = ['find directories@' + get_hostname()]
        if opt.find_find:
            places = ['find@' + get_hostname()]
        if opt.find_tu:
            places = ['find here -t tu@' + get_hostname()]

        # reset file
        paths_text_file = open('/home/' + getuser() + '/.mmfinder-paths', 'w')
        paths_text_file_to_open = open('/home/' +
                                        getuser() +
                                        '/.mmfinder-paths-to-open', 'w')

        mmterminalpathtext = ''
        mmterminalpathtext_to_open = ''

        html_hits = ''
        c = 1
        for p in places:
            hr_text(p + '...')
            html_hits += '#' + p + '\n'

            status = ''

            if opt.pdf_find:
                status = 'pdf searching...'
                cmd = "locate -d " + PATH_DB + p + '.db' + " " + \
                    wholename_or_basename + " -i -r '" + words_rex + "pdf"

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

            # execute!
            out = getoutput(cmd).strip()

            if opt.dev:
                hr_text('dev::out')
                print out
                hr()

            if out and list_with_action:
                for item in out.strip().split('\n'):
                    # @@ BUG @@ id = IDS[c]
                    id = 'a'  # TO FIX
                    h = Hit(id, item)
                    self.items.append(h)
                    h.check_filetype()
                    #print i.is_dir
                    #if i.is_dir and find_dir:
                    #    i.show()
                    #print 'x'
                    #if not find_dir:
                    hit = h.show(opt.not_less,
                                 opt.noncolor, c)
                    if opt.www_browser:
                        html_hits += hit + '\n'
                    else:
                        mmterminalpathtext += hit.split('\n')[0].strip() \
                        + ' #' + str(c) + '\n'
                        mmterminalpathtext_to_open += hit.split('\n')[1].strip() \
                        + ' #' + str(c) + '\n'
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

        paths_text_file.write(mmterminalpathtext)
        paths_text_file_to_open.write(mmterminalpathtext_to_open)
        paths_text_file.close()


class Hit:
    """
    Class for a hit of search.
    """
    def __init__(self, id, path):
        self.path = path
        self.id = id
        self.filetype = ''
        self.is_pdf = False
        self.is_empty = False

    def show(self, not_less, noncolor, c):
        """
        Shows (print/save to html) one hit.

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
            print '\t\'' + path.dirname(self.path) + \
                  '/' + path.basename(self.path) + "'"
        else:
            print_red_and_blue(str(c) + '\t\'' +
                               path.dirname(self.path) +
                               '/', '' + path.basename(self.path) + "'")
        # hack #1
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
        return out.replace('file://', '').replace('%20', ' ')

    def check_filetype(self, verbose=False):
        """
        Checks filetype of a hit.
        """
        if not path.isfile(self.path):
            self.is_dir = True
            self.filetype = 'dir'
        else:
            self.is_dir = False

            cmd = "file '" + self.path + "'"
            out = getoutput(cmd)
            if verbose:
                print '# out', out

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
                self.filetype = 'empty'
                self.is_empty = True

        if verbose:
            print '\t#filetype: ', self.filetype


def option_parser():
    """
    This shows and gets options.
    """
    description = ''
    version = __version__
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

    if not arguments:
        if not opt.update_db:
            parser.print_help()
            exit(1)
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
    """
    This runs the main program.
    """
    config = check_user_configuration()
    banner2('mmfinder.py')
    arguments, opt = option_parser()
    if arguments:
        m = App()
        m.search(arguments, opt)

if __name__ == "__main__":
    start()
