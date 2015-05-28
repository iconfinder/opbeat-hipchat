from __future__ import print_function

import json
import os
import requests
import sys

from bottle import get, post, run, request
from bottle import jinja2_template as template

from opbeat_hipchat.translation import ActivityTranslator


activity_translator = ActivityTranslator()
"""Activity translator.
"""


HIPCHAT_AUTH_TOKEN = os.environ.get('HIPCHAT_AUTH_TOKEN')
if not HIPCHAT_AUTH_TOKEN:
    print('Missing environment variable HIPCHAT_AUTH_TOKEN', file=sys.stderr)
    exit(1)


HIPCHAT_ROOM = os.environ.get('HIPCHAT_ROOM')
if not HIPCHAT_ROOM:
    print('Missing environment variable HIPCHAT_ROOM', file=sys.stderr)
    exit(1)


def handle_activity(data):
    # Translate the activity.
    notification = activity_translator.translate(data)
    if not notification:
        return

    # Send the notification.
    resp = requests.post(
        'https://api.hipchat.com/v2/room/{}/notification'.format(HIPCHAT_ROOM),
        data=json.dumps(notification),
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(HIPCHAT_AUTH_TOKEN),
        }
    )

    if not resp.ok:
        msg = 'Failed to send activity to Hipchat (status code {}): {}'
        print(msg.format(resp.status_code, resp.text), file=sys.stderr)
    else:
        print('Sent activity to Hipchat')


@post('/new-activity')
def new_activity():
    handle_activity(request.json)
    return "OK"


@get('/setup')
def setup():
    url = request.url.replace("/setup", "/new-activity")
    return template('''\
<html>
    <head>
        <title>Opbeat Hipchat integration setup</title>
    </head>
    <body>
        <h1>Opbeat Hipchat integration setup</h1>
        <p>
            Use the following as your organization's hook target at
            <code>https://opbeat.com/&lt;organization&gt;/settings/</code>:
        </p>
        <pre>{{ url }}</pre>
    </body>
</html>''', url=url)


if __name__ == '__main__':
    run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
