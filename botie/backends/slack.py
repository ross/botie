#
#
#

from logging import getLogger
from requests import Session
from tornado.web import HTTPError

# Passed as body_arguments:
#
# {'channel_id': [b'C6XJSQPU5'],
#  'channel_name': [b'general'],
#  'command': [b'/graph'],
#  'response_url': [b'https://hooks.slack.com/commands/XYZ/1234/'
#                   b'abc123'],
#  'team_domain': [b'ross-dev'],
#  'team_id': [b'T6XJSQN3F'],
#  'text': [b'me -1h foo.bar'],
#  'token': [b'dOUuXGFm8cWLVG7zBrcQ1p9U'],
#  'user_id': [b'U6WUKH2M7'],
#  'user_name': [b'rwmcfa1']}


class SlackBackend(object):
    leader = '/'

    log = getLogger('SlackBackend')

    session = Session()

    def __init__(self, auth_tokens,
                 response_url_prefix='https://hooks.slack.com'):
        self.auth_tokens = auth_tokens
        self.response_url_prefix = response_url_prefix

    def check_auth(self, handler):
        if handler.get_argument('token', 'no-exist') not in self.auth_tokens:
            self.log.warning('check_auth: invalid auth token')
            raise HTTPError(401, 'Authentication required')
        response_url = handler.get_argument('response_url')
        if not response_url.startswith(self.response_url_prefix):
            raise HTTPError(400, 'Invalid response_url')

    def command(self, handler):
        return handler.get_argument('command')

    def text(self, handler):
        return handler.get_argument('text')

    def user_name(self, handler):
        return handler.get_argument('user_name')

    def user_mention(self, handler):
        return '<@{}>'.format(handler.get_argument('user_id'))

    @property
    def pre_start(self):
        return '```'

    @property
    def pre_end(self):
        return '```'

    def _write(self, handler, data):
        handler.write(data)

    def _send(self, handler, data):
        response_url = handler.get_argument('response_url')
        resp = self.session.post(response_url, json=data, timeout=5)
        content = resp.content
        if content != b'ok':
            self.log.error('reply_delayed: resp.content=%s', content)
        resp.raise_for_status()

    def write_echo(self, handler):
        self._write(handler, {
            'response_type': 'in_channel'
        })

    def _simple_data(self, text):
        return {
            'response_type': 'in_channel',
            'text': text,
        }

    def write_simple_response(self, handler, text):
        return self._write(handler, self._simple_data(text))

    def send_simple_response(self, handler, text):
        return self._send(handler, self._simple_data(text))

    def _image_data(self, title, image_url, text, color, title_link):
        return {
            'response_type': 'in_channel',
            'attachments': [{
                'color': color,
                'fallback': '{} - {}'.format(title, image_url),
                'image_url': image_url,
                'text': text,
                'title': title,
                'title_link': title_link,
            }]
        }

    def write_image_response(self, handler, title, image_url, text=None,
                             color=None, title_link=None):
        return self._write(handler, self._image_data(title, image_url, text,
                                                     color, title_link))

    def send_image_response(self, handler, title, image_url, text=None,
                            color=None, title_link=None):
        return self._send(handler, self._image_data(title, image_url, text,
                                                    color, title_link))

    def _error_data(self, text):
        return {
            'response_type': 'in_channel',
            'attachments': [{
                'color': 'ff0000',
                'text': text,
            }]
        }

    def write_error_response(self, handler, text):
        return self._write(handler, self._error_data(text))

    def send_error_response(self, handler, text):
        return self._send(handler, self._error_data(text))
