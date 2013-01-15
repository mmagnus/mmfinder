## init & configuration file
## list of disk
PLACES_LOCAL = ['dropbox']
PLACES_GLOBAL = ['dropbox','maximus', '1TB', 'StoreJet', 'truecrypt', 'debian'] 

PATH_DB = '/home/magnus/Dropbox/workspace/mmfinder/db/'

## setup computers
## name of db : path on that host'
computer1 = {
    'dropbox' : '/home/magnus/Dropbox',
    'debian'  : '/home/magnus/',
    'StoreJet': '/media/StoreJet',
    '1TB'      : '/media/1TB',
    'StoreJet' : '/media/StoreJet',
    }

computer2 = {
    'dropbox'  : '/home/magnus/Dropbox',
    'maximus'  : '/home/magnus/',
    'truecrypt': '/media/truecrypt1/',
    }

## map computer to hostname
HOSTS = {'debian' : computer1, 'maximus' : computer2}

DONT_DB = [
    'Dropbox',
    ' Trash',
    'english-lingXwavsOnline',
    'backups-snapshots',
    '.libreoffice',
    '.dropbox.cache'
    ]

## firefox bookmarks (optional)
FF_SQLITE_DATABASE = '/home/magnus/.mozilla/firefox/ssfbppfu.default/places.sqlite'

## extensios of documents and media
EXTENSIONS_OF_DOCUMENTS = ['rtf','doc','odt', 'ppt', 'odp', 'ods', 'xls']
EXTENSIONS_OF_MEDIA = ['avi', 'mp4']

## html mode to present results
HTML_FN = '/tmp/a120c.html'
HTML_CMD = '/usr/bin/firefox'

## logfile
PATH_LOGFILE = PATH_DB + '/log'

## grep cmd
GREP_CMD = 'grep -C 2 -r ' # -C 1

## run update, --mm but what for???
RUN_UPDATE = True

