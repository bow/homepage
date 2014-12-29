# Volt widgets


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

