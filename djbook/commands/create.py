from cliff.command import Command as BaseCommand
import logging
import os


class Command(BaseCommand):
    """
    Update translation and generate HTML documentation
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.app.run_subcommand(['compilemessages'])
        self.app.run_subcommand(['buildhtml'])
        self.app.run_subcommand(['statistic'])
