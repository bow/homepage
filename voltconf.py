# -*- coding: utf-8 -*-
# Volt configurations file

import os
from sys import maxint

from volt.config import Config


# General project configurations
SITE = Config(
    TITLE = "bow.web.id",
    URL = "http://bow.web.id",
    ENGINES = (
        'plain',
        'blog',
    ),
    PAGES = {
        '/index.html': 'index.html',
    },
    PLUGINS = (
        'css_minifier',
    ),
    DISQUS_NAME = "bow",
    GOOGLE_ANALYTICS_ID = "UA-4847388-8",
    FILTERS = (
        'header_taglink',
        'header_timelink',
        'in_same_year',
    ),
    INDEX_HTML_ONLY = True,
)

# Plain engine configurations
ENGINE_PLAIN = Config(
    URL = "/",
    PERMALINK = "{slug}",
    PLUGINS = (
        'markdown_parser',
    ),
)

# Blog engine configurations
ENGINE_BLOG = Config(
    URL = "/blog",
    PERMALINK = "{time:%Y/%m}/{slug}",
    PAGINATIONS = {
        '': '',
        'tag/{tags}': "Posts tagged '%s'",
        '{time:%Y/%m}': "Posts in %B %Y",
        '{time:%Y}': "Posts in %Y",
    },
    UNITS_PER_PAGINATION = maxint,
    EXCERPT_LENGTH = 2000,
    PLUGINS = (
        'markdown_parser',
        'syntax',
        'atomic',
    ),
)

# Plugins configurations
PLUGIN_ATOMIC = Config(
    FEEDS = {
        '': 'atom.xml',
        'tags': 'atom-%s.xml',
    },
    OUTPUT_DIR = os.path.join(os.getcwd(), 'site', 'feed'),
)

PLUGIN_SYNTAX = Config(
    OUTPUT_DIR = os.path.join(os.getcwd(), 'site', 'css'),
    PYGMENTS_LEXER = {
        'stripall': True,
    },
)

PLUGIN_CSS_MINIFIER = Config(
    SOURCE_DIR = os.path.join(os.getcwd(), 'site', 'css'),
    OUTPUT_DIR = os.path.join(os.getcwd(), 'site', 'css'),
)
