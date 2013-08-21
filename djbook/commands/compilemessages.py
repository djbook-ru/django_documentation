from cliff.command import Command as BaseCommand
import logging
import os


class Command(BaseCommand):
    """
    Compile .po files to .mo.
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        for path, dirs, files in os.walk(self.app.locale_path):
            for f in files:
                if f.endswith('.po'):
                    po_path = os.path.join(path, f)
                    mo_path = po_path[:-2] + 'mo'
                    os.system('msgfmt %s -o %s' % (po_path, mo_path))

        self.app.stdout.write('.mo files compiled!\n')
