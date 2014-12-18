import logging
import os
import shutil
from cliff.command import Command as BaseCommand


class Command(BaseCommand):
    """
    Generate HTML documentation with Sphinx
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        doctrees_path = os.path.join(self.app.doc_path, '_build/doctrees')

        #for root, dirs, files in os.walk(self.app.html_path):
        #    for f in files:
        #        os.unlink(os.path.join(root, f))
        #    for d in dirs:
        #        shutil.rmtree(os.path.join(root, d))

        cmd = 'sphinx-build -E -b djangohtml -d %s %s %s'
        os.system(cmd % (doctrees_path, self.app.doc_path, self.app.html_path))
        self.app.stdout.write('You can find generated documentation here: %s\n' % self.app.html_path)
