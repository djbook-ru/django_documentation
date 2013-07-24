from cliff.command import Command as BaseCommand
from git import *
from jinja2 import Environment, FileSystemLoader
import logging
import os
import urllib2
import urllib
import base64
import getpass
import json


class Command(BaseCommand):
    """
    Get authors from git history
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        repo = Repo(self.app.doc_path)

        authors = set(c.author for c in repo.iter_commits('master'))
        authors = self.filter_authors(authors)

        self.save_to_file({
            'authors': authors
        })

    def search_in_github(self, username, github_username, github_password):
        github_url = 'https://api.github.com/search/users?%s'

        params = urllib.urlencode({
            'q': '%s in:username' % username
        })

        request = urllib2.Request(github_url % params)
        base64string = base64.encodestring('%s:%s' % (github_username, github_password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header('Accept', 'application/vnd.github.preview')

        try:
            data = json.loads(urllib2.urlopen(request).read())
            if data['total_count']:
                return data['items'][0]
        except urllib2.HTTPError:
            pass

    def filter_authors(self, authors):
        print 'We need authenticate your in Github for Search API.'
        github_username = raw_input('Github username: ')
        github_password = getpass.getpass('Github password: ')

        output = []
        names = []

        for author in authors:
            if 'dmitriy' in author.name.lower() \
                or 'dmitriy' in author.email.lower() \
                or 'dkos' in author.email.lower() \
                or 'dmytro' in author.name.lower() \
                or ('alerion' in author.name.lower() and not 'gmail' in author.email):
                continue

            if author.name.lower() in names:
                continue

            github_data = self.search_in_github(author.name, github_username, github_password)

            output.append({
                'name': author.name,
                'github_data': github_data
            })
            names.append(author.name.lower())

        return output

    def save_to_file(self, context):
        env = Environment(loader=FileSystemLoader(self.app.templates_path))
        template_name = 'authors.html'
        template = env.get_template(template_name)
        with open(os.path.join(self.app.doc_path, '_build', 'html', template_name), 'w') as output:
            output.write(template.render(**context).encode('utf8'))
