from flask_script import Command
import sys
import logging


class OutputWrapper(object):
    """
    Wrapper around stdout/stderr
    """
    @property
    def style_func(self):
        return self._style_func

    @style_func.setter
    def style_func(self, style_func):
        if style_func and self.isatty():
            self._style_func = style_func
        else:
            self._style_func = lambda x: x

    def __init__(self, out, style_func=None, ending='\n'):
        self._out = out
        self.style_func = None
        self.ending = ending

    def __getattr__(self, name):
        return getattr(self._out, name)

    def isatty(self):
        return hasattr(self._out, 'isatty') and self._out.isatty()

    def write(self, msg, style_func=None, ending=None):
        ending = self.ending if ending is None else ending
        if ending and not msg.endswith(ending):
            msg += ending
        style_func = style_func or self.style_func
        self._out.write(str(style_func(msg)))


class BaseCommand(Command):
    def __init__(self, stdout=None, stderr=None, *args, **kwargs):
        self.stdout = OutputWrapper(stdout or sys.stdout)
        self.stderr = OutputWrapper(stderr or sys.stderr)
        self.logger = logging.getLogger('application-cli')
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.DEBUG)
        super(BaseCommand, self).__init__(*args, **kwargs)
