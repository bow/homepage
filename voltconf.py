# -*- coding: utf-8 -*-
# Volt configurations file

import os

from volt.config import Config


# General project configurations
SITE = Config(
    TITLE = "bow.web.id",
    URL = "http://bow.web.id",
    ENGINES = (
        'plain',
        'blog',
    ),
    EXTRA_PAGES = (
        'index.html',
    ),
    DISQUS_NAME = "bow",
    GOOGLE_ANALYTICS_ID = "UA-4847388-8",
    FILTERS = ('header_taglink', 'header_timelink',),
)

# Plain engine configurations
ENGINE_PLAIN = Config(
    URL = "/",
    PERMALINK = "{slug}",
    PLUGINS = ('markdown_parser',),
)

# Blog engine configurations
ENGINE_BLOG = Config(
    URL = "/blog",
    PERMALINK = "{time:%Y/%m}/{slug}",
    PAGINATIONS = ('', 'tag/{tags}', '{time:%Y/%m}', '{time:%Y}',),
    UNITS_PER_PAGINATION = 5, 
    EXCERPT_LENGTH = 400, 
    PLUGINS = ('markdown_parser', 'syntax', 'atomic',),
)

# Plugins configurations
PLUGIN_ATOMIC = Config(
    OUTPUT_FILE = os.path.join(os.getcwd(), 'site', 'atom.xml'),
)

PLUGIN_SYNTAX = Config(
    CSS_FILE = os.path.join(os.getcwd(), 'site', 'css', 'syntax_highlight.css'),
    PYGMENTS_LEXER = {
        'stripall': True,
    },
)
