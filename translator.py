import os
import time
from argparse import ArgumentParser
from functools import cmp_to_key
from jinja2 import Environment, FileSystemLoader
from math import ceil
from polib import pofile

from loguru import logger

import conf  # use shpinx API to load config

TITLE = 'Translator Tools'
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MSG_PATH = os.path.join(BASE_PATH, 'locale', 'ru', 'LC_MESSAGES')
TPL_PATH = os.path.join(BASE_PATH, 'djbook', 'templates')
TREE_PATH = os.path.join(BASE_PATH, '_build', 'doctrees')
HTML_PATH = os.path.join(BASE_PATH, '_build', 'html')
REPO_NAME = 'djbook-ru/django_documentation'
SITEMAP_URL = f'https://djbook.ru/rel{conf.version}/'
SITEMAP_PRIORITY = '0.8'


def mode_sitemap():
    prefix_len = len(HTML_PATH) + 1
    changefreq = 'weekly'
    output = ['<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">']

    for path, dirs, files in os.walk(HTML_PATH):
        for f in files:
            if f.endswith('.html'):
                url = SITEMAP_URL + os.path.join(path, f)[prefix_len:]
                output.append(
                    f'<url><loc>{url}</loc>'
                    f'<priority>{SITEMAP_PRIORITY}</priority>'
                    f'<changefreq>{changefreq}</changefreq></url>')

    output.append(u'</urlset>')

    with open(os.path.join(HTML_PATH, 'sitemap.xml'), 'w') as f:
        content = ''.join(output)
        f.write(content)


def mode_statistic():
    statistic = []
    prefix_len = len(MSG_PATH) + 1
    total = 0
    translated = 0

    exclude = [
        '/misc/',
        '/releases/',
        '/internals/',
        '/ref/contrib/gis/',
        '/sphinx.po',
        ]

    for path, dirs, files in os.walk(MSG_PATH):
        for f in files:
            if f.endswith('.po'):
                po_path = os.path.join(path, f)
                name = po_path[prefix_len:]
                po = pofile(po_path)
                excluded = False
                for item in exclude:
                    if name.startswith(item):
                        excluded = True
                        break
                if excluded:
                    continue

                msg_total = len([e for e in po if not e.obsolete])
                msg_translated = len(po.translated_entries())
                msg_untranslated = len(po.untranslated_entries())
                msg_fuzzy = msg_total - msg_translated - msg_untranslated
                need_fix_count = msg_total - msg_translated
                untranslated_perc = int(ceil(msg_untranslated / float(msg_total) * 100))
                fuzzy_perc = int(ceil(msg_fuzzy / float(msg_total) * 100))
                translated_perc = 100 - untranslated_perc - fuzzy_perc
                total += msg_total
                translated += msg_translated
                statistic.append(
                    (name, translated_perc, untranslated_perc, fuzzy_perc,
                     need_fix_count))

    def sort_statistic(item1, item2):
        if item1[4] == 0:
            return 1
        if item2[4] == 0:
            return -1
        return item1[4] - item2[4]

    statistic.sort(key=cmp_to_key(sort_statistic))

    context = {
        'statistic': statistic,
        'total_perc': '%.02f' % ((100.00 / float(total)) * translated),
        'total': total,
        'translated': translated,
        'version': conf.version,
        }
    env = Environment(loader=FileSystemLoader(TPL_PATH))
    template_name = 'statistic.html'
    template = env.get_template(template_name)
    with open(os.path.join(BASE_PATH, '_build', 'html', template_name), 'w') as f:
        f.write(template.render(**context))
    logger.info('Complete statistic generated!')


def save_to_file(self, context):
    env = Environment(loader=FileSystemLoader(self.app.templates_path))
    template_name = 'statistic.html'
    template = env.get_template(template_name)
    with open(os.path.join(self.app.doc_path, '_build', 'html', template_name), 'w') as output:
        output.write(template.render(**context))


def mode_buildhtml():
    cmd = f'sphinx-build -E -b djangohtml -d {TREE_PATH} {BASE_PATH} {HTML_PATH}'
    os.system(cmd)
    logger.info(f'You can find generated documentation here: {HTML_PATH}')


def mode_compilemessages():
    for path, dirs, files in os.walk(MSG_PATH):
        for f in files:
            if f.endswith('.po'):
                po_path = os.path.join(path, f)
                mo_path = po_path[:-2] + 'mo'
                os.system(f'msgfmt {po_path} -o {mo_path}')

    logger.info('.mo files compiled!')


def read_args():
    parser = ArgumentParser(description=TITLE)
    parser.add_argument(
        '-m', '--mode', required=False, type=str, dest='mode')
    return parser.parse_args()


def main():
    if params.mode == 'compilemessages':
        mode_compilemessages()
    elif params.mode == 'buildhtml':
        mode_buildhtml()
    elif params.mode == 'statistic':
        mode_statistic()
    elif params.mode == 'sitemap':
        mode_sitemap()
    elif params.mode == 'build':
        mode_compilemessages()
        mode_buildhtml()
        mode_statistic()
        mode_sitemap()

if __name__ == '__main__':
    params = read_args()

    try:
        main()
    except KeyboardInterrupt:
        time.sleep(1)
