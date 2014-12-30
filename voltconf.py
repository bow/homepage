# -*- coding: utf-8 -*-
# Volt configurations file

import os

from volt.config import Config


# Template filters and tests

def header_taglink(tags, index_html_only=True, max_item=None, sort=False):
    """Jinja2 filter for displaying blog tag links."""
    blog_url = '/blog'
    if index_html_only:
        string = '<a href="%s/tag/%s/" class="button green">%s</a>'
    else:
        string = '<a href="%s/tag/%s.html" class="button green">%s</a>'
    if sort:
        tags.sort()
    if max_item is not None:
        if len(tags) <= max_item:
            return ', '.join([string % (blog_url, tag, tag) for tag in tags[:max_item]])
        else:
            return ', '.join([string % (blog_url, tag, tag) for tag in tags[:max_item]]) + ', ...'
    return ', '.join([string % (blog_url, tag, tag) for tag in tags])


def header_timelink(time_obj, index_html_only=True):
    """Jinja2 filter for displaying blog time links."""
    blog_url = '/blog'
    if index_html_only:
        time_url = '<a href="%s/%s/" class="button blue">%s</a>'
    else:
        time_url = '<a href="%s/%s.html" class="button blue">%s</a>'

    month = time_obj.strftime("%B")
    year = time_obj.strftime("%Y")
    month_url = time_url % (blog_url, time_obj.strftime("%Y/%m"), month)
    year_url = time_url % (blog_url, time_obj.strftime("%Y"), year)

    return '%s%s' % (month_url, year_url)

def in_same_year(units):
    """Jinja2 test for checking if all units have the same year."""
    for idx, unit in enumerate(units):
        if idx >= 1 and unit.time.year != units[idx-1].time.year:
                return False
    return True

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
    FILTERS = [
        header_taglink,
        header_timelink,
    ],
    TESTS = [in_same_year],
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
    UNITS_PER_PAGINATION = 500,
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
