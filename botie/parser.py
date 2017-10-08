#
#
#

from argparse import Action, ArgumentError, ArgumentParser
from re import compile as re_compile


# https://stackoverflow.com/a/9236426
class NoAction(Action):

    def __init__(self, option_strings, dest, default=True, required=False,
                 help=None):
        opt = option_strings[0]
        option_strings = [opt, '--no-{}'.format(opt[2:])]
        super(NoAction, self).__init__(option_strings, dest, nargs=0,
                                       const=None, default=default,
                                       required=required, help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        if option_string and option_string.startswith('--no-'):
            setattr(namespace, self.dest, False)
        else:
            setattr(namespace, self.dest, True)


class HasSpacesAction(Action):

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, ' '.join(values))


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
