#!/usr/bin/env python

from logging import DEBUG as LOGGING_DEBUG, getLogger
from os import environ
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line
from tornado.web import Application

from botie.backends.slack import SlackBackend
from botie.handlers.base import BaseSlashHandler
from botie.handlers.status import StatusHandler

define('debug', default=False, help='Enable debug mode')
define('address', default='0.0.0.0',
       help='Set the interface to listen on')
define('port', default=8888, help='Port to listen on')


class EchoHandler(BaseSlashHandler):
    log = getLogger('EchoHandler')

    def handle(self):
        self.log.debug('handle:')
        self.write_simple_response(self.text)


class ItsfineHandler(BaseSlashHandler):
    log = getLogger('ItsFineHandler')

    def handle(self):
        self.log.debug('handle:')
        url = 'https://i2.wp.com/johngaltfla.com/wordpress/wp-content/' \
            'uploads/2016/06/DOGFIRE.gif'
        self.write_image_response("It's Fine", url, 'f49b42')


if __name__ == '__main__':
    parse_command_line()

    auth_tokens = environ['SLACK_AUTH_TOKENS'].split(',')
    app = Application([
        (r'/slack/echo', EchoHandler, {
            'backend': SlackBackend(auth_tokens=auth_tokens)
        }),
        (r'/slack/itsfine', ItsfineHandler, {
            'backend': SlackBackend(auth_tokens=auth_tokens)
        }),
        (r'/_status', StatusHandler),
    ], debug=options.debug)
    if options.debug:
        getLogger().level = LOGGING_DEBUG
    app.listen(options.port, address=options.address)
    IOLoop.current().start()
