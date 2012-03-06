# Volt configurations file

from volt.config.base import Config


# Volt configurations
VOLT = Config(

    # Flag for colored terminal output
    COLORED_TEXT = True,
)


# General project configurations
SITE = Config(

    # Your site name
    TITLE = "bow.web.id",

    # Your site URL
    URL = "http://bow.web.id",

    # Your site description
    DESC = "Because static sites have potential",

    # Engines used in generating the site
    # Available engines are 'page', 'blog', and 'collection'
    # To disable an engine, just remove its name from this list
    ENGINES = ['blog', 'plain'],

    PLUGINS = (('volt-markdown', ('blog', 'plain')),),
)


# Blog engine configurations
BLOG = Config(
  
    # URL for all blog content relative to root URL
    URL = "blog",

    # Blog posts permalink, relative to blog URL
    PERMALINK = "{time:%Y/%m}/{slug}",

    # Global values to be set to all blog posts
    GLOBAL_FIELDS = {'author': 'Wibowo Arindrarto', },

    # Display datetime format
    DISPLAY_DATETIME_FORMAT = '%B %Y',

    # The number of displayed posts per pagination page
    POSTS_PER_PAGE = 5, 

    # Default length (in chars) of blog post excerpts
    EXCERPT_LENGTH = 400, 

    # Packs
    PACKS = ('', 'category/{categories}', '{time:%Y/%m}', '{time:%Y}',),
)


# Page engine configurations
PLAIN = Config(

    # URL for all page content relative to root URL
    URL = "/",

    # Page permalink, relative to page URL
    PERMALINK = "{slug}",
)


# Jinja custom filters
def appendhash(permalink, string):
    """Append hash + string to the end of the given permalink.
            
    This is a Jinja2 filter used to append a given permalink with hash 
    and the given string. All Volt permalinks ends with a slash, so
    we need to use this filter to avoid placing the hash after the slash.
    """
    return permalink[:-1] + '#' + string

def catlist(catlist):
    s = []
    for cat in catlist:
        s.append('<a href="/blog/category/' + cat + '/" class="button red">' + cat+ '</a>')
    return ', '.join(s)

def displaytime(time, format):
    return time.strftime(format)

JINJA2 = Config(
    FILTERS = {
        'appendhash': appendhash,
        'catlist': catlist,
        'displaytime': displaytime,
    }
)
