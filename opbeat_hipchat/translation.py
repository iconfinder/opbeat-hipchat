from jinja2 import Environment


class ActivityTranslator(object):
    """Activity translator.

    Translates an Opbeat activity payload into a Hipchat notification.
    """

    _activity_colors = {
        'errorgroup': {
            'created': 'red',
            'fixed': 'green',
            'regressed': 'red',
        },
        'release': {
            'created': 'purple',
        },
        'assignmentlog': {
            'created': 'red',
            'created_and_assigned': 'red',
        }
    }
    _default_color = 'yellow'

    def __init__(self):
        self._env = Environment(autoescape=True)
        self._template = self._env.from_string('''\
<a href="{{ app.url }}" title="{{ app.name }}">{{ app.name }}</a>: \
{% if url %}<a href="{{ url }}" title="{{ title }}">{% endif -%}
    {{ title }}
{%- if url %}</a>{% endif %} - {{ summary }}''')

    def _get_color(self, subject_type, action):
        return self._activity_colors.get(subject_type, {}) \
            .get(action, self._default_color)

    def translate(self, activity):
        """Translate an activity.

        :param activity: Activity payload.
        :type activity: :class:`dict`
        :returns:
            a Hipchat notification activity if the activity translates,
            otherwise ``None``.
        :rtype: :class:`dict`
        """

        # Parse the activity.
        try:
            subject_type = activity['subject_type']
            action = activity['action']
            app = activity['app']
            organization = activity['organization']
            subject = activity['subject']
            summary = activity['summary']
            title = activity['title']

            app_name = app['name']
            app_url = 'https://opbeat.com/{}/{}/'.format(
                app['short_name'],
                organization['short_name']
            )
        except KeyError:
            return None

        if subject_type == 'assignmentlog':
            url = subject.get('errorgroup', {}).get('html_url')
        else:
            url = subject.get('html_url')

        # Render the notification.
        return {
            'message': self._template.render({
                'title': title,
                'summary': summary,
                'app': {
                    'name': app_name,
                    'url': app_url,
                },
                'url': url,
            }),
            'message_format': 'html',
            'color': self._get_color(subject_type, action),
        }
