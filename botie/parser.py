#
#
#

from argparse import ArgumentError, ArgumentParser
from re import compile as re_compile


class BotParser(ArgumentParser):
    splitter = re_compile(r'\s+')

    def __init__(self, *args, **_kwargs):
        kwargs = {
            'add_help': False,
            'allow_abbrev': False,
        }
        kwargs.update(_kwargs)
        super(BotParser, self).__init__(*args, **kwargs)

    def error(self, message):
        raise ArgumentError(None, message)

    def _split(self, text):
        arg = []
        args = []
        for p in self.splitter.split(text):
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

    def parse_known_args(self, text):
        return super(BotParser, self).parse_known_args(self._split(text))
