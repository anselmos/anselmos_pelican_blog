#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Anselmos'
SITENAME = u'Anselmos-Pelican-Blog Example'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Warsaw'
PLUGIN_PATHS = ['plugins']
PLUGINS = ['i18n_subsites']

THEME = "themes/pelican-bootstrap3"
# { PELICAN_BOOTSTRAP3_THEME
JINJA_ENVIRONMENT = {
	"extensions": ['jinja2.ext.i18n'],
}

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
MENUITEMS = [['Menu-Item', "link"]]
PYGMENTS_STYLE = 'vim' # coloring of code blocks - style with pygments
BOOTSTRAP_NAVBAR_INVERSE = True ## for inversing colors at navbar
GITHUB_USER = 'anselmos'  ## just put your github username here.
GITHUB_SKIP_FORK = True
ABOUT_ME = """ Developer. Mainly found at backyard of - pick yourself: (sorted by name) : android | docker | java | linux | python """
DISPLAY_CATEGORIES_ON_SIDEBAR = True

# PELICAN_BOOTSTRAP3_THEME }


STATIC_PATHS = ['images']

DEFAULT_LANG = u'E\x08'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('github', '#'),
          ('twitter', '#'),
          ('linkedin', '#'),)

DEFAULT_PAGINATION = 6

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
