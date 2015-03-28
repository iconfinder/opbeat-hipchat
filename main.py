from __future__ import print_function

import json
import os
import requests
import sys

from bottle import get, post, run, request
from bottle import jinja2_template as template


DEFAULT_COLOR = 'yellow'
COLORS = {
    'errorgroup': {
        'created': 'red',
        'fixed': 'green',
        'regressed': 'red',
    },
    'release': {
        'created': 'purple',
    },
}


def get_color(subject_type, action):
    return COLORS.get(subject_type, {}).get(action, DEFAULT_COLOR)


def get_template(data):
    if data.get('html_url'):
        return '{{app.name}}: {{title}} - {{summary}} ({{subject.html_url}})'

    return '{{app.name}}: {{title}} - {{summary}}'


HIPCHAT_ROOM_AUTH_TOKEN = os.environ.get('HIPCHAT_ROOM_AUTH_TOKEN')
if not HIPCHAT_ROOM_AUTH_TOKEN:
    print('Missing environment variable HIPCHAT_ROOM_AUTH_TOKEN',
          file=sys.stderr)
    exit(1)


HIPCHAT_ROOM = os.environ.get('HIPCHAT_ROOM')
if not HIPCHAT_ROOM:
    print('Missing environment variable HIPCHAT_ROOM', file=sys.stderr)
    exit(1)


def send(data):
    rendered_activity = template(get_template(data), **data)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(HIPCHAT_ROOM_AUTH_TOKEN),
    }
    message_data = {
        'message': rendered_activity,
        'message_format': 'text',
        'color': get_color(data['subject_type'], data['action']),
    }
    url = 'https://api.hipchat.com/v2/room/{}/notification'

    resp = requests.post(
        url.format(HIPCHAT_ROOM),
        data=json.dumps(message_data),
        headers=headers,
    )
    if not resp.ok:
        msg = 'Failed to send activity to Hipchat (status code {}): {}'
        print(msg.format(resp.status_code, resp.text), file=sys.stderr)
    else:
        print('Sent activity to Hipchat')


@post('/new-activity')
def new_activity():
    data = request.json
    send(data)
    return "OK"


@get('/setup')
def setup():
    url = request.url.replace("/setup", "/new-activity")
    return template("This is your hook url, copy it:<h3>{{url}}</h3>", url=url)

run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
