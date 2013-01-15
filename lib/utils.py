LENGTH_OF_THE_SCREEN=100
CHAR = "#"

from os import system
from commands import getoutput

def banner2(word):
    """
    Print banner via figlet
    """
    system('figlet ' + word)

def hr(len_of_hr = LENGTH_OF_THE_SCREEN,verbose=True):
    """
    GET:
    - len, by default it equals to LENGTH_OF_THE_SCREEN

    RETURNS:
    - string, like: -------------------------------------------------------
    """
    if verbose:
        st = CHAR * len_of_hr
        print st
        return True
    else:
        return False

def get_hostname(verbose = False):
    """

    In [4]: mmscikit.get_hostname()
    magnusbook
    Out[4]: 'magnusbook'

    """
    cmd = "hostname"
    out = getoutput(cmd)
    if verbose: print out
    return out

def hr_text(text, len_of_hr = LENGTH_OF_THE_SCREEN,verbose=True):
    """
    GET:
    - len, by default it equals to LENGTH_OF_THE_SCREEN

    RETURNS:

    **********************************************************************
    # Job_id                                                        A1VY95
    ************************************************************** A1VY95 *
    """
    if verbose:
        text=str(text)
        st=CHAR * (len_of_hr - 3 - len(text)) + ' ' + text + ' ' + CHAR # 3 = ' 'test' '* = 2x' ' + 1x*
        print st
        return True
    else:
        return False

def print_red_and_blue(text,text2, newline = True):
    """
    http://www.siafoo.net/snippet/88
    """
    if newline:
        print '\033[1;31m' + text + '\033[1;m' + '\033[1;34m' + text2 + '\033[1;m'
    else:
        print '\033[1;31m' + text + '\033[1;m' + '\033[1;34m' + text2 + '\033[1;m'
