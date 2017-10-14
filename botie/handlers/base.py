#
#
#

from argparse import ArgumentError
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
        try:
            params = self.parse(text)
            self.handle(*params)
        except ArgumentError as e:
            self.backend.write_error_response(self, e.message)

    def help(self):
        buf = StringIO()
        self.get_parser().print_help(file=buf)
        return buf.getvalue()

    def get_parser(self):
        return BotParser(prog='{}{}'.format(self.backend.leader,
                                            self.command))

    def _split(self, text):
        arg = []
        args = []
        for p in BotParser.splitter.split(text):
            if p.startswith('--'):
                if arg:
                    args.append(arg)
                args.append([p])
                arg = []
            else:
                arg.append(p)
        if arg:
            args.append(arg)

        return [' '.join(p) for p in args]

    def parse(self, text):
        parser = self.get_parser()
        args = self._split(text)
        return parser.parse_known_args(args)

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
