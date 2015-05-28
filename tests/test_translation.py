import json
import os
from unittest import TestCase
from opbeat_hipchat.translation import ActivityTranslator


class ActivityTranslatorTestCase(TestCase):
    """Test case for :class:`ActivityTranslator`.
    """

    def test_translate(self):
        """ActivityTranslator(..).translate(..)
        """

        translator = ActivityTranslator()
        fixtures_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'fixtures'
        )

        for fixture_name, expected in (
                ('assignmentlog_created_and_assigned.json', {
                    'color': 'red',
                    'message_format': 'html',
                    'message':
                    '<a href="https://opbeat.com/iconfinder/nextfinder/" title'
                    '="Nextfinder">Nextfinder</a>: <a href="https://opbeat.com'
                    '/iconfinder/nextfinder/errors/821/" title="Error group E#'
                    '821">Error group E#821</a> - The error group was first se'
                    'en and auto-assigned to Nick',
                }),
                ('release_created.json', {
                    'color': 'purple',
                    'message_format': 'html',
                    'message':
                    '<a href="https://opbeat.com/iconfinder/nextfinder/" title'
                    '="Nextfinder">Nextfinder</a>: <a href="https://opbeat.com'
                    '/iconfinder/nextfinder/releases/1192/" title="Release R#1'
                    '192">Release R#1192</a> - 2 commits (+27/-10) by Nick wer'
                    'e deployed.',
                }),
        ):
            with open(os.path.join(fixtures_path, fixture_name), 'rb') as f:
                fixture = json.loads(f.read().decode('utf-8'))

            actual = translator.translate(fixture)
            self.assertEquals(expected, actual)
