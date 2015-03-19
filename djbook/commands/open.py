import logging
import webbrowser

from cliff.command import Command as BaseCommand


class Command(BaseCommand):
    """
    Open documentation in a browser
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        webbrowser.open('%s/index.html' % self.app.html_path)
