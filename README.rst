Steward Web
===========
This is a Steward extension for adding a web interface. It provides a base
template and other basics to build off of.

Setup
=====
To use ``steward_web``, just add it to your includes either programmatically::

    config.include('steward_web')

or in the config.ini file::

    pyramid.includes = steward_web

Configuration
=============
::

    # Use the built-in username/password login system. You may want to disable
    # this if you want to use custom login with OpenID or something similar
    steward.web.basic_login = true
