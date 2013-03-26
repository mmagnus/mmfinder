from setuptools import setup, find_packages
from os import system, path
from time import sleep

__version__ = "0.98 alpha"

print '*' * 80
print '*', 'Welcome!'
print '*', 'mmfinder ', __version__
print '*', 'run setup.py as a root!'
print '*' * 80

print 'figlet installing...'
system('sudo apt-get install figlet')
print
setup(
    # basic package data
    name = "mmfinder",
    author = "Marcin Magnus",
    description = 'a tool for finding your files across different machines',
    version = __version__,
    license = 'GPLv3',
    url = 'https://github.com/m4rx9/mmfinder',
    author_email = "mag_dex@o2.pl",
    packages = ['mmfinder','mmfinder.lib'],
    #long_description = read('README.md'),
    install_requires = ['pysqlite'],
    entry_points={
        'console_scripts': [
            'mmfinder = mmfinder.mmfinder:start',
            'mmfinder-deamon = mmfinder.mmfinder_deamon:start',
        ],
        }
)
print
print 'done :-) edit `~/.mmfinder-config.py` & run `mmfinder` to see what happens'
