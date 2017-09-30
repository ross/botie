#
#
#

from tornado.web import RequestHandler


class BaseSlashHandler(RequestHandler):

    def initialize(self, backend):
        self.backend = backend

    def post(self):
        self.log.debug('post:')
        self.backend.check_auth(self)
        self.handle()

    @property
    def command(self):
        return self.backend.command(self)

    @property
    def text(self):
        return self.backend.text(self)

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
