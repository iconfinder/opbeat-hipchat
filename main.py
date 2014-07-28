import json
import os
import requests
import sys
from bottle import post, run, request
from bottle import jinja2_template as template


DEFAULT_TEMPLATE = '{{app.name}}: {{title}} - {{summary}} ({{url}})'
TEMPLATES = {
    'errorgroup': {
        'fixed': '{{app.name}}: {{title}} - {{summary}} ({{url}})',
    },
}
"""Templates.

Mapping subject type and action to templates.
"""


def get_template(subject_type, action):
    return TEMPLATES.get(subject_type, {}).get(action, DEFAULT_TEMPLATE)


DEFAULT_COLOR = "yellow"
COLORS = {
    "errorgroup": {"created": "red", "fixed": "green"},
    "release": {"created": "purple"},
}


def get_color(subject_type, action):
    return COLORS.get(subject_type, {}).get(action, DEFAULT_COLOR)


HIPCHAT_AUTH_TOKEN = os.environ.get('HIPCHAT_AUTH_TOKEN')
if not HIPCHAT_AUTH_TOKEN:
    print >> sys.stderr, 'Missing environment variable HIPCHAT_AUTH_TOKEN'
    exit(1)

HIPCHAT_ROOM_ID = os.environ.get('HIPCHAT_ROOM_ID')
if not HIPCHAT_ROOM_ID:
    print >> sys.stderr, 'Missing environment variable HIPCHAT_ROOM_ID'
    exit(1)


def send(data):
    rendered_activity = template(get_template(data['subject_type'],
                                              data['action']), **data)
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
        print >> sys.stderr, 'Failed to send activity to Hipchat (status ' \
            'code %d): %s' % (resp.status_code, resp.text)
    else:
        print "Sent activity to Hipchat"


@post('/new-activity')
def new_activity():
    data = request.json
    print 'Activity:', data
    send(data)
    return "OK"


run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
