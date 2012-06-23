###
###   INIT & CONFIGURATION FILE
###
PATH = '/home/magnus/Dropbox/workspace/mmfinder/'
RUN_UPDATE = True

# MMFINDER DEAMON
## LOCS ##################################
LOCS = {

    #name of db : path on that host'

    'EON'      : '/media/EONVECTOR',
    'dropbox'  : '/home/magnus/Dropbox',
    'maximus'  : '/home/magnus/',
    '1TB'      : '/media/1TB',
    'StoreJet' : '/media/StoreJet',
    'truecrypt': '/media/truecrypt1/',

    }

LOCS_HP = {
    'hp' : '/home/magnus/',
    'dropbox' : '/home/magnus/Dropbox',
}

LOCS_NETBOOK = {
    'netbook' : '/home/magnus/',
    'dropbox' : '/home/magnus/Dropbox',
    #'EON'     : '/media/EONVECTOR',
    #'1TB'     : '/media/1TB',
    'StoreJet'     : '/media/disk',
    }

HOSTS = {'maximus' : LOCS, 'netbook' : LOCS_NETBOOK, 'hp' : LOCS_HP}
## you can check a hostname by '$hostname'
########################################


#MMFINDER
########################################
#list of db
PLACES_GLOBAL = ['dropbox','maximus', 'netbook', 'EON', '1TB', 'StoreJet', 'truecrypt'] 
PLACES_LOCAL = ['dropbox'] # + hostname

PATH_DB = '/home/magnus/Dropbox/workspace/mmfinder/db/'
DONT_DB = [
    'Dropbox',
    ' Trash',
    'english-lingXwavsOnline',
    'backups-snapshots',
    '.libreoffice',
    '.dropbox.cache'
    ]

#
EXTENSIONS_OF_DOCUMENTS = ['rtf','doc','odt', 'ppt', 'odp', 'ods', 'xls']
EXTENSIONS_OF_MEDIA = ['avi', 'mp4']

#FF BOOKMARK SEARCHER
FF_SQLITE_DATABASE = '/home/magnus/.mozilla/firefox/ssfbppfu.default/places.sqlite'
