import sys

PATH = '/home/magnus/Dropbox/workspace/mmfinder/'
sys.path.append(PATH)
sys.path.append('/home/magnus/Dropbox/workspace/mmscikit/')

RUN_UPDATE = True

## LOCS ##################################
LOCS = {

    #name of db : path on that host'

    'EON'      : '/media/EONVECTOR',
    'SD8GB'    : '/media/SD8GB',
    'SD8GB2'   : '/media/8GB2'    ,
    'dropbox'  : '/home/magnus/Dropbox',
    'maximus'  : '/home/magnus/',
    '1TB'      : '/media/1TB',
    'StoreJet' : '/media/StoreJet',
    'truecrypt': '/media/truecrypt1/',
    }

LOCS_NETBOOK = {
    'magnusbook' : '/home/magnus/',
    'dropbox' : '/home/magnus/Dropbox',
	'srv' : '/srv/',
    #'EON'     : '/media/EONVECTOR',
    #'SD8GB'   : '/media/SD8GB',
    #'8GB2'   : '/media/8GB2'    ,

    #'1TB'     : '/media/1TB',
    #'StoreJet'     : '/media/StoreJet',
    }

HOSTS = {'maximus' : LOCS, 'magnusbook' : LOCS_NETBOOK}
## you can check a hostname by '$hostname'
########################################


PLACES = ['dropbox','maximus', 'magnusbook','EON',  '8GB2', '1TB', 'StoreJet', 'truecrypt'] # 'SD8GB',
#PLACES = ['dropbox','maximus']
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
EXTENSIONS_OF_DOCUMENTS = ['rtf','doc','odt', 'ppt', 'odp', 'ods', 'xls']
EXTENSIONS_OF_MEDIA = ['avi', 'mp4']

FF_SQLITE_DATABASE = '/home/magnus/.mozilla/firefox/ssfbppfu.default/places.sqlite'
