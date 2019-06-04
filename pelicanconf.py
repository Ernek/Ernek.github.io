#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Ernek'
SITENAME = 'Ernesto\'s Blog'
RELATIVE_URLS = False
SITETITLE = SITENAME
SITEURL = 'http://localhost:8000'
SITESUBTITLE = 'Theoretical and Computational Chemistry'
SITEDESCRIPTION = 'A place to save my learning journey'
SITELOGO = "/images/avatar02.jpg"

#USE_FOLDER_AS_CATEGORY = False
MAIN_MENU = True
#HOME_HIDE_TAGS = False
DISABLE_URL_HASH = True

MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)

DELETE_OUTPUT_DIRECTORY = False

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'
THEME = "Flex"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Python.org', 'http://python.org/'),)

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/ErnestoCheco'),
          ('github', 'https://github.com/Ernek'),)

DEFAULT_PAGINATION = 10
#PAGINATED_DIRECT_TEMPLATES = ('categories', 'archives')

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['images']
