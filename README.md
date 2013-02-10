# mmfinder

     updated Jan 2012
     version 0.9
     author  Marcin Magnus (mag_dex@o2.pl) 
	 license GNU

--------------------------------------------------------------------------------

<video style="width:500px" src="http://dl.dropbox.com/u/472680/mmfinder_demo_v2.ogg" controls>
</video>

See also: http://www.youtube.com/watch?v=-oQ998IWwTc

TABLE OF CONTENTS
-----------------

1. DESCRIPTION
2. INSTALLATION
3. CONFIGURATION
4. HOW TO USE IT
5. BUGS
6. TODO
7. COPYRIGHT AND LICENSE
8. AUTHOR INFORMATION

1. DESCRIPTION
=======================================

``mmfinder.py`` is a wrapper to *nix commands like ``locate``, ``updatedb``, ``grep``, ``find`` to help you with searching files across several machines (computers). 

Firstly, ``updatedb`` is used by ``mmfinder_deamon.py`` to create databases. You can define as many "databases" as you want in ``mmfinder_config.py`` file.

The syntax is as follows:

	name_of_computer (you can name it as you want!) = {
		'name_of_database' : 'path_to_folder_for_database'
	}

.. real-world working example ..	

    computer1 = {
        'dropbox' : '/home/magnus/Dropbox',
        'debian'  : '/home/magnus/',
        'StoreJet': '/media/StoreJet',
         }

.. for example, if I have the ``StoreJet`` connected to my computer and I run ``mmfinder_deamon.py``, a database ``StoreJet`` will be created that includes data from ``/media/StoreJet`` directory.

Next, imagine that at work, you will never mount ``StoreJet``, but you want to create a database for your ``/home`` directory at work. You define another computer (for example, ``computer02 ``) as follows..

    computer2 = {
        'dropbox'  : '/home/magnus/Dropbox',
        'maximus'  : '/home/magnus/',
        'truecrypt': '/media/truecrypt1/',
        }

My recommendation is to use Dropbox (https://www.dropbox.com/home) to put ``mmfinder`` directory (``~/Dropbox/opt/mmfinder/``) and set the path to your databases (``~/Dropbox/opt/mmfinder/db``).

You can also use anything else (http://alternativeto.net/software/dropbox/) but then you need slightly change configuration file.

## Bash plugin

What is cool about ``mmfinder`` is that you can have pretty nice functionality if you add to your environment ``bash-plugin.sh``. You can g(o) to hit of result, r(un) it, e(emacs it = open in emacs), o(pen it).. see ``bash-plugin.sh``

2. INSTALLATION
=======================================
If you want to use "banners" ..

    sudo apt-get install figlet
	
.. nothing extra is needed.. do you have python? if not, then install it!

	sudo apt-get install python

.. although if you want to search for firefox bookmarks install ..

	sudo apt-get install python-django
	(or pip install django) # you need python-pip for that!

	sudo apt-get install python-sqlite
	
3. CONFIGURATION
=======================================
Go to ``mmfinder_config.py`` ..

to use ``bash-plugin`` add .. 

    source /home/magnus/Dropbox/workspace/mmfinder/bash-plugin.sh

.. to your ``.bashrc``

For ``mmfinder_deamon.py`` you might want to use ``cron`` as follows ..

    00 * * * * /home/magnus/Dropbox/workspace/mmfinder/mmfinder.py_deamon.py

4. HOW TO USE IT
=======================================
Start with configuration, then ``mmfinder.py -u`` or ``mmfinder_deamon.py`` and search ..

      mmfinder.py -g .bashrc # search for .bashrc across all defined machines

etc..

5. BUGS
=======================================

Report bugs to the author.
	
6. TODO
=======================================

- [ ] make a deb pkg
- [ ] get old TODO from git repo with some TODOs :-)
- [ ] check if all options works
- [ ] write test script

- [ ] how to promote the tool
- [ ] add `tracker-search`
- [ ] find similar tools and compare

7. COPYRIGHT AND LICENCE
=======================================

    mmfinder is Copyright (C) 2013 Marcin Magnus.  All rights reserved.
    
    This program is free software; you can redistribute it and/or modify it
    under the same terms as GLP

8. AUTHOR INFORMATION
=======================================

Marcin Magnus, m.magnus@o2.pl
