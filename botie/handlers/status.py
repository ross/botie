#
#
#

from logging import getLogger
from tornado.web import RequestHandler


class StatusHandler(RequestHandler):
    log = getLogger('StatusHandler')

    def get(self):
        self.log.debug('get:')
        self.write('OK')
