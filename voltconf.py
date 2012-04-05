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
    PLUGINS = (
        ('markdown_parser', ['blog', 'plain']),
        ('atomic', ['blog']),
    ),
    EXTRA_PAGES = (
        'index.html',
    ),
    DISQUS_NAME = "bow",
    GOOGLE_ANALYTICS_ID = "UA-4847388-8",
)

# Plain engine configurations
ENGINE_PLAIN = Config(
    URL = "/",
    PERMALINK = "{slug}",
)

# Blog engine configurations
ENGINE_BLOG = Config(
    URL = "/blog",
    PERMALINK = "{time:%Y/%m}/{slug}",
    PAGINATIONS = ('', 'tag/{tags}', '{time:%Y/%m}', '{time:%Y}',),
    UNITS_PER_PAGINATION = 5, 
    EXCERPT_LENGTH = 400, 
)

# Plugins configurations
PLUGIN_ATOMIC = Config(
    OUTPUT_FILE = os.path.join(os.getcwd(), 'site', 'atom.xml'),
)

# Jinja custom filters
def taglist(tags):
    string = '<a href="/blog/tag/%s/" class="button red">%s</a>'
    return ', '.join([string % (tag, tag) for tag in tags])

JINJA2_FILTERS = Config(
    taglist = taglist,
)
