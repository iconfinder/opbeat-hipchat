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


HIPCHAT_AUTH_TOKEN = os.environ.get('HIPCHAT_AUTH_TOKEN')
if not HIPCHAT_AUTH_TOKEN:
    print >> sys.stderr, 'Missing environment variable HIPCHAT_AUTH_TOKEN'
    exit(1)


HIPCHAT_ROOM_ID = os.environ.get('HIPCHAT_ROOM_ID')
if not HIPCHAT_ROOM_ID:
    print >> sys.stderr, 'Missing environment variable HIPCHAT_ROOM_ID'
    exit(1)


def send(data):
    rendered_activity = template(get_template(data), **data)
    message_data = {
        'auth_token': HIPCHAT_AUTH_TOKEN,
        'from': 'Opbeat',
        'room_id': HIPCHAT_ROOM_ID,
        'message': rendered_activity,
        'message_format': 'text',
        'color': get_color(data['subject_type'], data['action']),
    }

    resp = requests.post('https://api.hipchat.com/v1/rooms/message',
                         data=message_data)
    if resp.status_code != 200:
        print >> sys.stderr, \
            'Failed to send activity to Hipchat (status code %d): %s' % (
                resp.status_code, resp.text
            )
    else:
        print 'Sent activity to Hipchat'


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
