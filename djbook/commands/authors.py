from cliff.command import Command as BaseCommand
from git import *
import logging
import git


class Command(BaseCommand):
    """
    Get authors from git history
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        repo = Repo(self.app.doc_path)

        authors = set(c.author for c in repo.iter_commits('master'))
        authors = self.filter_authors(authors)

        for a in authors:
            print a.name, a.email

    def filter_authors(self, authors):
        output = [Actor('Alerion', 'alerion.um(at)gmail.com')]
        names = []

        for author in authors:
            if 'alerion' in author.name.lower() \
                or 'alerion' in author.email.lower() \
                or 'dmitriy' in author.name.lower() \
                or 'dmitriy' in author.email.lower() \
                or 'dkos' in author.email.lower():
                continue

            if author.name in names:
                continue

            author.email = author.email.replace('@', '(at)')
            output.append(author)
            names.append(author.name)

        return output