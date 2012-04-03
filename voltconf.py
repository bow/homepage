# Volt configurations file

import os

from volt.config import Config


# General project configurations
SITE = Config(
    TITLE = "bow.web.id",
    URL = "http://bow.web.id",
    DESC = "Because static sites have potential",
    ENGINES = (
        'blog',
        'plain',
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

# Blog engine configurations
ENGINE_BLOG = Config(
    URL = "blog",
    PERMALINK = "{time:%Y/%m}/{slug}",
    GLOBAL_FIELDS = {'author': 'Wibowo Arindrarto', },
    DISPLAY_DATETIME_FORMAT = '%B %Y',
    UNITS_PER_PAGINATION = 5, 
    EXCERPT_LENGTH = 400, 
    PAGINATIONS = ('', 'tag/{tags}', '{time:%Y/%m}', '{time:%Y}',),
)

# Page engine configurations
ENGINE_PLAIN = Config(
    URL = "/",
    PERMALINK = "{slug}",
)

# Plugins configurations
PLUGIN_ATOMIC = Config(
    OUTPUT_FILE = os.path.join(os.getcwd(), 'site', 'atom.xml'),
)

# Jinja custom filters
def taglist(tags):
    """Show categories in comma-separated links."""
    s = []
    for tag in tags:
        s.append('<a href="/blog/tag/' + tag + '/" class="button red">' + tag + '</a>')
    return ', '.join(s)

JINJA2_FILTERS = Config(
    taglist = taglist,
)
