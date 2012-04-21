# Volt widgets


def header_taglink(tags):
    """Jinja2 filter for displaying blog tag links."""
    blog_url = '/blog'
    string = '<a href="%s/tag/%s/" class="button red">%s</a>'
    return ', '.join([string % (blog_url, tag, tag) for tag in tags])


def header_timelink(time_obj):
    """Jinja2 filter for displaying blog time links."""
    blog_url = '/blog'
    time_url = '<a href="%s/%s/" class="button green">%s</a>'

    month = time_obj.strftime("%B")
    year = time_obj.strftime("%Y")
    month_url = time_url % (blog_url, time_obj.strftime("%Y/%m"), month)
    year_url = time_url % (blog_url, time_obj.strftime("%Y"), year)

    return '%s%s' % (month_url, year_url)


def css_minifier(site):
    """Site widget for minifying CSS."""
    import os
    import cssmin

    target_name = 'minified.css'
    source_dir = os.path.join(os.path.dirname(__file__), 'site', 'css')
    source_files = [os.path.join(source_dir, f) for f in os.listdir(source_dir) \
            if f != target_name and f.endswith('.css')]

    css = ''
    for f in source_files:
        with open(f, 'r') as source_file:
            css += source_file.read()

    with open(os.path.join(source_dir, target_name), 'w') as target_file:
        target_file.write(cssmin.cssmin(css))
