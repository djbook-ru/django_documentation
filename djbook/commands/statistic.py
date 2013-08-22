from cliff.command import Command as BaseCommand
from jinja2 import Environment, FileSystemLoader
from djbook.polib import pofile
import logging
import os


class Command(BaseCommand):
    """
    Calculate translation % complete and generate statistic.html
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        statistic = []
        total = 0
        translated = 0

        main = ['/intro/', '/howto/', '/ref/', '/faq/', '/topics/']
        exclude = ['/releases/', '/internals/']
        main_total = 0
        main_translated = 0

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
                    untranslated_count = msg_total - msg_translated
                    total += msg_total
                    translated += msg_translated

                    statistic.append((unicode(name),  po.percent_translated(), untranslated_count))

                    for item in main:
                        if name.startswith(item):
                            main_total += msg_total
                            main_translated += msg_translated
                            break

        self.save_to_file({
            'statistic': statistic,
            'total': '%.02f' % ((100.00 / float(total)) * translated),
            'main_total': '%.02f' % ((100.00 / float(main_total)) * main_translated)
        })

        self.app.stdout.write('Complete statistic generated!\n')

    def save_to_file(self, context):
        env = Environment(loader=FileSystemLoader(self.app.templates_path))
        template_name = 'statistic.html'
        template = env.get_template(template_name)
        with open(os.path.join(self.app.doc_path, '_build', 'html', template_name), 'w') as output:
            output.write(template.render(**context).encode('utf8'))
