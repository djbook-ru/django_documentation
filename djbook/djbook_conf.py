# to apply these settings add to conf.py
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "djbook")))
# from djbook_conf import *

import sys
from datetime import datetime

# from git import Repo

# from spelling_filters import IgnoreEnglishFilter

# repo = Repo('.')
# commit = repo.commit()

html_context = {
    'git_commit': 'commit here',  #str(commit),
    'git_commit_date': datetime.now(),  #datetime.fromtimestamp(commit.committed_date),
    'git_branch': 'branch here',  #str(repo.active_branch),
    'prev_version': '1.10'
}

html_theme_path = ["_theme", "djbook/_theme"]
html_theme = "djbook"

language = 'ru'
gettext_compact = False

exclude_patterns = ['_build', 'djbook', 'env']

spelling_lang = 'ru_RU'
# spelling_filters = [IgnoreEnglishFilter]
spelling_show_suggestions = False
spelling_word_list_filename = 'djbook/spelling_ignore.txt'
#
if 'spelling' in sys.argv:
    extensions = ["djangodocs", "sphinx.ext.intersphinx", "spelling"]
