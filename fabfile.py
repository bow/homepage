import glob, os
from datetime import datetime

import secret
from fabric.api import *
from volt.config import CONFIG


DRAFT_DIR = os.path.join(CONFIG.VOLT.ROOT_DIR, "drafts")
POST_DATE = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
DRAFT_DATE = "0000/00/00 00:00:00"
DEPLOY_TARGET = secret.DEPLOY_TARGET
PACK_NAME = "homepage.tgz"


def post_count(directory=CONFIG.BLOG.CONTENT_DIR):
    """Returns published post count."""
    try:
        return max([int(f[:3]) for f in os.listdir(directory)])
    except ValueError:
        return 0

def draft_count():
    """Returns draft count."""
    return len(os.listdir(DRAFT_DIR))

def total_count():
    """Returns draft and published posts count."""
    return post_count() + draft_count()

def post_list(directory=CONFIG.BLOG.CONTENT_DIR):
    """Prints post filenames."""
    local("ls -l %s | awk '{print $9}'" % directory)

def draft_list():
    """Prints draft filenames."""
    post_list(DRAFT_DIR)

def draft(title):
    """Start writing a new draft."""
    template = "\n".join([
        "---",
        "categories: ",
        "date: %(date)s",
        "title: %(title)s",
        "---",
        " ",
        ])
    date = DRAFT_DATE
    count = str(total_count() + 1).zfill(3)
    format = os.path.join(DRAFT_DIR, "%s_%s.draft.md")
    title_file = "-".join(title.lower().split(" "))
    filename = format % (count, title_file)
    with open(filename, 'w') as post:
        post.write(template % locals())
    local("vim %s" % filename)

def edit(index=total_count()):
    """Edit draft."""
    index = str(index).zfill(3)
    draft_name = glob.glob(os.path.join(DRAFT_DIR, "%s_*.draft.md" % index)).pop()
    local("vim %s" % draft_name)

def post(index=draft_count()):
    """Post draft."""
    index = str(index).zfill(3)
    draft_name = glob.glob(os.path.join(DRAFT_DIR, "%s_*.draft.md" % index)).pop()
    post_name = draft_name.replace(DRAFT_DIR, CONFIG.BLOG.CONTENT_DIR).replace(".draft", "")
    local("sed -i -e's!%s!%s!' %s" % (DRAFT_DATE, POST_DATE, draft_name))
    local("mv %s %s" % (draft_name, post_name))

def generate():
    """Generates site."""
    local("volt gen")

def serve():
    """Generates site and serve."""
    generate()
    local("volt serve")

def pack():
    """Packages the live site directory."""
    with lcd(CONFIG.VOLT.SITE_DIR):
        local("tar czfv ../%s *" % PACK_NAME)

@hosts(DEPLOY_TARGET)
def deploy(message=None):
    """Deploy site to host."""
    generate()
    if message:
        local('git add .')
        local('git cm -am "%s"' % message)
    pack()
    put("homepage.tgz", secret.REMOTE_DIR)
    with cd(secret.REMOTE_DIR):
        run("rm -rf %s/*" % secret.REMOTE_PUBLIC)
        run("tar xzfv %s -C %s && rm %s" % (PACK_NAME, secret.REMOTE_PUBLIC, PACK_NAME))
    local("rm %s" % PACK_NAME)
