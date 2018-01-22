class IODevice(object):
    @staticmethod
    def init_handler():
        pass
    def exit_handler():
        pass

from .file import *
from .html import *
from .pdf import *
from .terminal import *
from .templates import *
