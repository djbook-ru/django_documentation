#!/usr/bin/python
from jinja2 import Environment, FileSystemLoader
from polib import pofile
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
LOCALE_PATH = os.path.join(BASE_PATH, 'locale/ru/LC_MESSAGES')


def save_to_file(context):
    env = Environment(loader=FileSystemLoader(os.path.join(BASE_PATH, 'djbook', 'templates')))
    template = env.get_template('statistic.html')
    with open(os.path.join(BASE_PATH, '_build', 'html', 'statistic.html'), 'w') as output:
        output.write(template.render(**context).encode('utf8'))


def create_statistic():
    statistic = []
    total = 0
    translated = 0

    main = ['/intro/', '/howto/', '/ref/', '/faq/', '/topics/']
    exclude = ['/releases/']
    main_total = 0
    main_translated = 0

    for path, dirs, files in os.walk(LOCALE_PATH):
        for f in files:
            if f.endswith('.po'):
                po_path = os.path.join(path, f)
                po = pofile(po_path)

                name = po_path[len(LOCALE_PATH):]

                excluded = False
                for item in exclude:
                    if name.startswith(item):
                        excluded = True
                        break

                if excluded:
                    continue

                statistic.append((unicode(name),  po.percent_translated()))

                msg_total = len([e for e in po if not e.obsolete])
                msg_translated = len(po.translated_entries())
                total += msg_total
                translated += msg_translated

                for item in main:
                    if name.startswith(item):
                        main_total += msg_total
                        main_translated += msg_translated
                        break

    save_to_file({
        'statistic': statistic,
        'total': '%.02f' % ((100.00 / float(total)) * translated),
        'main_total': '%.02f' % ((100.00 / float(main_total)) * main_translated)
    })

if __name__ == '__main__':
    create_statistic()
