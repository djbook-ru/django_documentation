import logging
import os

from cliff.command import Command as BaseCommand


class Command(BaseCommand):
    """
    Generate sitemap.xml
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        prefix_len = len(self.app.html_path) + 1
        priorty = self.app.sitemap_priority
        base_url = self.app.sitemap_base_url
        changefreq = 'weekly'

        output = []
        output.append(u'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

        for path, dirs, files in os.walk(self.app.html_path):
            for f in files:
                if f.endswith('.html'):
                    url = base_url + os.path.join(path, f)[prefix_len:]
                    output.append(
                        '<url><loc>%s</loc><priority>%s</priority><changefreq>%s</changefreq></url>'
                        % (url, priorty, changefreq)
                    )

        output.append(u'</urlset>')

        content = u''.join(output)

        file = open(os.path.join(self.app.html_path, 'sitemap.xml'), 'w')
        file.write(content)
        file.close()
