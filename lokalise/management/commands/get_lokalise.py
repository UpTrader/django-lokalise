import requests
from django.conf import settings
from django.core.management import BaseCommand

from lokalise import handle_content


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--project_id', type=str, dest='project_id', help='A unique project identifier.')
        parser.add_argument('--token', type=str, dest='token', help='Personal X-Api-Token')

    def handle(self, *args, **options):
        if options.get('project_id'):
            project_id = options['project_id']
        else:
            project_id = settings.LOKALISE_PROJECT_ID

        if options.get('token'):
            token = options['token']
        else:
            token = settings.LOKALISE_X_API_TOKEN

        create_po_resp = requests.post(
            'https://api.lokalise.co/api2/projects/{project_id}/files/download'.format(project_id=project_id),
            headers={'x-api-token': token},
            json={
                'format': 'po',
                'original_filenames': False,
                'replace_breaks': False
            }
        )

        r = requests.get(create_po_resp.json()['bundle_url'])

        handle_content(r.content)

        self.stdout.write('Lokalise successfully update!')
