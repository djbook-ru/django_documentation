import logging
import os
from math import ceil
from cliff.command import Command as BaseCommand
from jinja2 import Environment, FileSystemLoader
from polib import pofile

import conf


class Command(BaseCommand):
    """
    Calculate translation % complete and generate statistic.html
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        statistic = []
        total = 0
        translated = 0

        exclude = [
            '/misc/',
            '/releases/',
            '/internals/',
            '/ref/contrib/gis/',
            '/sphinx.po'
        ]

        for path, dirs, files in os.walk(self.app.locale_path):
            for f in files:
                if f.endswith('.po'):
                    po_path = os.path.join(path, f)
                    po = pofile(po_path)

                    name = po_path[len(self.app.locale_path):]

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

                    statistic.append((unicode(name), translated_perc, untranslated_perc, fuzzy_perc, need_fix_count))

        def sort_statistic(item1, item2):
            if item1[4] == 0:
                return 1
            if item2[4] == 0:
                return -1
            return item1[4] - item2[4]

        statistic.sort(cmp=sort_statistic)

        self.save_to_file({
            'statistic': statistic,
            'total_perc': '%.02f' % ((100.00 / float(total)) * translated),
            'total': total,
            'translated': translated,
            'version': conf.version
        })

        self.app.stdout.write('Complete statistic generated!\n')

    def save_to_file(self, context):
        env = Environment(loader=FileSystemLoader(self.app.templates_path))
        template_name = 'statistic.html'
        template = env.get_template(template_name)
        with open(os.path.join(self.app.doc_path, '_build', 'html', template_name), 'w') as output:
            output.write(template.render(**context).encode('utf8'))
