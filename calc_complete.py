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

    for path, dirs, files in os.walk(LOCALE_PATH):
        for f in files:
            if f.endswith('.po'):
                po_path = os.path.join(path, f)
                po = pofile(po_path)

                total += len([e for e in po if not e.obsolete])
                translated += len(po.translated_entries())

                name = po_path[len(LOCALE_PATH):]
                statistic.append((unicode(name),  po.percent_translated()))

    save_to_file({
        'statistic': statistic,
        'total': '%.02f' % ((100.00 / float(total)) * translated)
    })

if __name__ == '__main__':
    create_statistic()
