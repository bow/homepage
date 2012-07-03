import glob, os
from datetime import datetime

import secret
from fabric.api import *

from volt.config import CONFIG
from volt.engine.builtins.blog import Blog


DATETIME_FORMAT = Blog.DEFAULTS.DATETIME_FORMAT
POST_DATE = datetime.now().strftime(DATETIME_FORMAT)
DRAFT_TIME = datetime(2000, 1, 1, 0, 0, 0).strftime(DATETIME_FORMAT)
DEPLOY_TARGET = secret.DEPLOY_TARGET
PACK_NAME = "homepage.tgz"

POST_DIR = os.path.join(CONFIG.VOLT.CONTENT_DIR, 'blog')
DRAFT_DIR = os.path.join(POST_DIR, 'drafts')


def post_count(directory=POST_DIR):
    """Returns published post count."""
    files = [f for f in os.listdir(directory) if '.' in f]
    return max([int(f.split('_', 1)[0]) for f in files])

def draft_count():
    """Returns draft count."""
    if os.path.exists(DRAFT_DIR):
        return len(os.listdir(DRAFT_DIR))
    else:
        return 0

def total_count():
    """Returns draft and published posts count."""
    return post_count() + draft_count()

def post_list(directory=POST_DIR):
    """Prints post filenames."""
    local("ls -l %s | awk '{print $9}'" % directory)

def draft_list():
    """Prints draft filenames."""
    post_list(DRAFT_DIR)

def draft(title):
    """Start writing a new draft."""
    if not os.path.exists(DRAFT_DIR):
        os.makedirs(DRAFT_DIR)
    template = "\n".join([
        "---",
        "title: %(title)s",
        "time: %(time)s",
        "tags: ",
        "---",
        " ",
        ])
    time = DRAFT_TIME
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

def post(index=total_count()):
    """Post draft."""
    index = str(index).zfill(3)
    print index
    draft_name = glob.glob(os.path.join(DRAFT_DIR, "%s_*.draft.md" % index)).pop()
    post_name = draft_name.replace(DRAFT_DIR, POST_DIR).replace(".draft", "")
    local("sed -i -e's!%s!%s!' %s" % (DRAFT_TIME, POST_DATE, draft_name))
    local("mv %s %s" % (draft_name, post_name))

def pack():
    """Packages the live site directory."""
    with lcd(CONFIG.VOLT.SITE_DIR):
        local("tar czfv ../%s *" % PACK_NAME)

@hosts(DEPLOY_TARGET)
def deploy(message=None):
    """Deploy site to host."""
    local('volt gen')
    if message:
        local('git add .')
        local('git cm -am "%s"' % message)
    pack()
    with lcd(CONFIG.VOLT.ROOT_DIR):
        put("homepage.tgz", secret.REMOTE_DIR)
    with cd(secret.REMOTE_DIR):
        run("rm -rf %s*" % secret.REMOTE_PUBLIC)
        run("tar xzfv %s -C %s && rm %s" % (PACK_NAME, secret.REMOTE_PUBLIC, PACK_NAME))
    with lcd(CONFIG.VOLT.ROOT_DIR):
        local("rm %s" % PACK_NAME)
