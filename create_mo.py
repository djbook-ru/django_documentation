import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
LOCALE_PATH = os.path.join(BASE_PATH, 'locale/ru/LC_MESSAGES')

for path, dirs, files in os.walk(LOCALE_PATH):
    for f in files:
        if f.endswith('.po'):
            po_path = os.path.join(path, f)
            mo_path = po_path[:-2] + 'mo'
            os.system('msgfmt %s -o %s' % (po_path, mo_path))
