################################################################################
##                     BASIC (REQUIRED) CONFIGURATION                         ##
################################################################################
PATH_DB = '/home/magnus/Dropbox/data/mmfinder-db/'

## setup computers, ## name of db : path on that host'
computer1 = {
    'dropbox': '/home/magnus/Dropbox',
    'debian': '/home/magnus/',
    'StoreJet': '/media/StoreJet',
    '1TB': '/media/1TB',
    'StoreJet': '/media/StoreJet',
    }

computer2 = {
    'dropbox': '/home/magnus/Dropbox',
    'maximus': '/home/magnus/',
    'truecrypt': '/media/truecrypt1/',
    }

## map computer to hostname
HOSTS = {'debian': computer1, 'maximus': computer2}


################################################################################
##                     ADVANCED CONFIGURATION                                 ##
################################################################################

## list of disk
PLACES_LOCAL = ['dropbox']

databases_of_computers = [h.keys() for h in HOSTS.values()]
global_places = []
for db in databases_of_computers:
    for i in db:
        if i not in global_places:
            global_places.append(i)
PLACES_GLOBAL = global_places


DONT_DB = [
    'Dropbox',
    ' Trash',
    'english-lingXwavsOnline',
    'backups-snapshots',
    '.libreoffice',
    '.dropbox.cache',
    'pubmex-all-pdfs-shit-test',
    ]

## firefox bookmarks (optional)
FF_SQLITE_DATABASE = '/home/magnus/.mozilla/firefox/ssfbppfu.default/places.sqlite'

## extensios of documents and media
EXTENSIONS_OF_DOCUMENTS = ['rtf', 'doc', 'odt', 'ppt', 'odp', 'ods', 'xls']
EXTENSIONS_OF_MEDIA = ['avi', 'mp4']

## html mode to present results
HTML_FN = '/tmp/a120c.html'
#HTML_CMD = '/usr/bin/firefox'
HTML_CMD = '/usr/bin/x-www-browser'

## logfile
PATH_LOGFILE = PATH_DB + '/log'

## grep cmd
GREP_CMD = 'grep -C 2 -r '  # -C 1

## run update, --mm but what for???
RUN_UPDATE = True
