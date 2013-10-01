from cliff.command import Command as BaseCommand
import logging
import os


class Command(BaseCommand):
    """
    Open documentation in a browser
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        os.system('xdg-open %s/index.html' % self.app.html_path)
