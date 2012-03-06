# Volt configurations file

import os

from volt.config.base import Config


# Volt configurations
VOLT = Config(
    COLORED_TEXT = True,
)

# General project configurations
SITE = Config(
    TITLE = "bow.web.id",
    URL = "http://bow.web.id",
    DESC = "Because static sites have potential",
    ENGINES = ['blog', 'plain'],
    PLUGINS = (('volt-markdown', ['blog', 'plain']),
               ('volt-atomic', ['blog']),
    ),
    DISQUS_NAME = "bow",
)

# Blog engine configurations
BLOG = Config(
    URL = "blog",
    PERMALINK = "{time:%Y/%m}/{slug}",
    GLOBAL_FIELDS = {'author': 'Wibowo Arindrarto', },
    DISPLAY_DATETIME_FORMAT = '%B %Y',
    POSTS_PER_PAGE = 5, 
    EXCERPT_LENGTH = 400, 
    PACKS = ('', 'category/{categories}', '{time:%Y/%m}', '{time:%Y}',),
)

# Page engine configurations
PLAIN = Config(
    URL = "/",
    PERMALINK = "{slug}",
)

# Plugins configurations
PLUGINS = Config(
    ATOM_OUTPUT_FILE = os.path.join(os.getcwd(), 'site', 'atom.xml'),
)

# Jinja custom filters
def appendhash(permalink, string):
    """Append hash + string to the end of the given permalink."""
    return permalink[:-1] + '#' + string

def catlist(catlist):
    """Show categories in comma-separated links."""
    s = []
    for cat in catlist:
        s.append('<a href="/blog/category/' + cat + '/" class="button red">' + cat+ '</a>')
    return ', '.join(s)

def displaytime(time, format):
    """Show time according to format."""
    return time.strftime

JINJA2 = Config(
    FILTERS = {
        'appendhash': appendhash,
        'catlist': catlist,
        'displaytime': displaytime,
    }
)
