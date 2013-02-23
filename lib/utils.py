#!/usr/bin/env python
#-*- coding: utf-8 -*-

import commands
import os

LENGTH_OF_THE_SCREEN=80
CHAR = "#"

def print_blue(text, newline = True):
    """
    http://www.siafoo.net/snippet/88
    """
    if newline:
        print '\033[1;34m' + text + '\033[1;m'
    else:
        print '\033[1;34m' + text + '\033[1;m',

def print_green(text, newline = True):
    """
    http://www.siafoo.net/snippet/88
    """
    if newline:
        print '\033[1;32m' + text + '\033[1;m'
    else:
        print '\033[1;32m' + text + '\033[1;m',

def print_red(text, newline = True):
    """
    http://www.siafoo.net/snippet/88
    """
    if newline:
        print '\033[1;31m' + text + '\033[1;m'
    else:
        print '\033[1;31m' + text + '\033[1;m',

def hr(len_of_hr = LENGTH_OF_THE_SCREEN,verbose=True):
    """
    GET:
    - len, by default it equals to LENGTH_OF_THE_SCREEN

    RETURNS:
    - string, like: -------------------------------------------------------
    """
    if verbose:
        st=CHAR * len_of_hr
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
    out = commands.getoutput(cmd)
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

def get_datetime():
    """
    GET:
    - nothing
    RETURN:
    - string 2011-7-31 16:3
    """
    import time
    localtime = time.localtime(time.time())
    return '%d-%d-%d %d:%d'% localtime[:5]
def banner2(word):
    """
    Print banner via figlet
    """
    os.system('figlet ' + word)
def print_red_and_blue(text,text2, newline = True):
    """
    http://www.siafoo.net/snippet/88
    """
    if newline:
        print '\033[1;31m' + text + '\033[1;m' + '\033[1;34m' + text2 + '\033[1;m'
    else:
        print '\033[1;31m' + text + '\033[1;m' + '\033[1;34m' + text2 + '\033[1;m'
