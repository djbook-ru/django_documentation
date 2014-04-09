# to apply these settings add to conf.py
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "djbook")))
# from djbook_conf import *
import sys
import os
from git import Repo

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "_ext")))

#extensions = ["djbookdocs", "sphinx.ext.intersphinx"]
#html_translator_class = "djbookdocs.DjangoHTMLTranslator"

repo = Repo('.')

html_context = {
    'git_commit': str(repo.commit()),
    'git_branch': str(repo.active_branch)
}

html_theme_path = ["_theme", "djbook/_theme"]
html_theme = "djbook"

language = 'ru'
locale_dirs = ['./locale/']
gettext_compact = False

exclude_patterns = ['_build', 'djbook', 'env']
