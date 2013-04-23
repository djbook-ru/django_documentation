import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
LOCALE_PATH = os.path.join(BASE_PATH, 'locale/ru/LC_MESSAGES')
TRANSLATION_PATH = os.path.join(BASE_PATH, '_build/translation')

for path, dirs, files in os.walk(TRANSLATION_PATH):
    for f in files:
        if f.endswith('.pot'):
            pot_path = os.path.join(path, f)
            p = pot_path[len(TRANSLATION_PATH) + 1:-1]
            po_path = os.path.join(LOCALE_PATH, p)

            if not os.path.exists(os.path.dirname(po_path)):
                os.makedirs(os.path.dirname(po_path))

            if not os.path.exists(po_path):
                os.system('msginit -i %s -o %s -l ru --no-translator' % (pot_path, po_path))
            else:
                os.system('msgmerge %s %s -U' % (po_path, pot_path))
