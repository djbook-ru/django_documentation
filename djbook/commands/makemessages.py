from cliff.command import Command as BaseCommand
import logging
import shutil
import os
from djbook.polib import pofile


class Command(BaseCommand):
    """
    Generate .pot files from document sources, then update .po files from .pot files.
    Remove .po file if there are not the relative .pot file.
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        TRANSLATION_PATH = os.path.join(self.app.doc_path, '_build/translation')

        shutil.rmtree(TRANSLATION_PATH)
        os.system('sphinx-build -b gettext %s %s' % (self.app.doc_path, TRANSLATION_PATH))

        for path, dirs, files in os.walk(TRANSLATION_PATH):
            for f in files:
                if not f.endswith('.pot'):
                    continue

                pot_path = os.path.join(path, f)
                p = pot_path[len(TRANSLATION_PATH) + 1:-1]
                po_path = os.path.join(self.app.locale_path, p)

                if not os.path.exists(os.path.dirname(po_path)):
                    os.makedirs(os.path.dirname(po_path))

                if not os.path.exists(po_path):
                    os.system('msginit -i %s -o %s -l ru --no-translator' % (pot_path, po_path))
                else:
                    os.system('msgmerge %s %s -U' % (po_path, pot_path))

        for path, dirs, files in os.walk(self.app.locale_path):
            for po_name in files:
                if not po_name.endswith('.po'):
                    continue

                po_path = os.path.join(path, po_name)
                po_relative_name = po_path[len(self.app.locale_path) + 1:]
                pot_name = po_relative_name + 't'
                pot_path = os.path.join(TRANSLATION_PATH, pot_name)

                if not os.path.exists(pot_path):
                    po = pofile(po_path)
                    if po.percent_translated() != 0:
                        self.app.stdout.write('WARNING! Removed file %s with %s%% complete\n' % (po_relative_name, po.percent_translated()))
                    os.remove(po_path)
