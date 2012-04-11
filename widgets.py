# Volt widgets


def taglist(tags):
    """Jinja2 filter for displaying blog tags."""
    string = '<a href="/blog/tag/%s/" class="button red">%s</a>'
    return ', '.join([string % (tag, tag) for tag in tags])
