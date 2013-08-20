from cliff.command import Command as BaseCommand
from jinja2 import Environment, FileSystemLoader
from github import Github, GithubException
import logging
import os
import getpass

PASS_CHACHE_FILE = '.github.auth'


class Command(BaseCommand):
    """
    Get authors from git history
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        github_username, github_password = None, None

        try:
            with open(PASS_CHACHE_FILE) as f:
                data = f.read()
                if data:
                    github_username, github_password = data.split('\n')
        except IOError as e:
            pass

        if not github_username or not github_password:
            print 'We need authenticate your in Github for Search API.'
            github_username = raw_input('Github username: ')
            github_password = getpass.getpass('Github password: ')

            with open(PASS_CHACHE_FILE, 'w') as f:
                f.write(github_username)
                f.write('\n')
                f.write(github_password)

        repo_name = 'Alerion/django_documentation'

        github = Github(github_username, github_password)
        repo = github.get_repo(repo_name)

        try:
            self.save_to_file({
                'contributors': repo.get_contributors()
            })
        except GithubException as e:
            print e
            print dir(e)

    def save_to_file(self, context):
        env = Environment(loader=FileSystemLoader(self.app.templates_path))
        template_name = 'authors.html'
        template = env.get_template(template_name)
        with open(os.path.join(self.app.doc_path, '_build', 'html', template_name), 'w') as output:
            output.write(template.render(**context).encode('utf8'))
