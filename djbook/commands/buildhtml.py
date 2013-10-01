from cliff.command import Command as BaseCommand
import logging
import os


class Command(BaseCommand):
    """
    Generate HTML documentation with Sphinx
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        doctrees_path = os.path.join(self.app.doc_path, '_build/doctrees')
        cmd = 'sphinx-build -E -b djangohtml -d %s %s %s'
        os.system(cmd % (doctrees_path, self.app.doc_path, self.app.html_path))
        self.app.stdout.write('You can find generated documentation here: %s\n' % self.app.html_path)
