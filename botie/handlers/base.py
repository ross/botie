#
#
#

from io import StringIO
from tornado.web import RequestHandler

from ..parser import BotParser


class BaseSlashHandler(RequestHandler):

    def initialize(self, backend):
        self.backend = backend

    def post(self):
        self.log.debug('post:')
        self.backend.check_auth(self)
        text = self.text
        if text == 'help':
            self.write_simple_response(self.help())
            return
        options, args = self.parse(text)
        self.handle(options, args)

    def help(self):
        buf = StringIO()
        self.get_parser().print_help(file=buf)
        return buf.getvalue()

    def get_parser(self):
        return BotParser(prog='{}{}'.format(self.backend.leader,
                                            self.command))

    def parse(self, text):
        parser = self.get_parser()
        return parser.parse_known_args(text)

    @property
    def command(self):
        return self.backend.command(self)

    @property
    def text(self):
        return self.backend.text(self)

    def write_echo(self):
        return self.backend.write_echo(self)

    def write_simple_response(self, text):
        return self.backend.write_simple_response(self, text)

    def send_simple_response(self, text):
        return self.backend.send_simple_response(self, text)

    def write_image_response(self, title, image_url, text=None, color=None,
                             title_link=None):
        return self.backend.write_image_response(self, title, image_url, text,
                                                 color, title_link)

    def send_image_response(self, title, image_url, text=None, color=None,
                            title_link=None):
        return self.backend.send_image_response(self, title, image_url, text,
                                                color, title_link)
