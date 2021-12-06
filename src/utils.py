# ===================================
# - Official Astro Source Code -
# ===================================
"""Main entrypoint of LLVM-Astro. """
# ===================================
# Dunder Credentials
# ===================================
__author__  = 'xyLotus'
# ===================================
# Imports
# ===================================
from typing import Any, AnyStr
import inspect
import sys

try:
    from colorama import Fore, Style
    import colorama
except ImportError as e:
    print(f'[utils] - {e}')
    exit(1)


# Yeah, yeah I know it's code that gets auto-run upon importing,
# but I have better things to do, so I'm just gonna leave this here. Bye.
if sys.platform == 'win32':
        colorama.init()

class ColorFormat:
    '''Acts as a singleton container (at most) for clored Astro-style text.
    Note: All methods are also a staticmethod.'''
    
    @staticmethod
    def src_log(src: str, msg: str) -> AnyStr:
        '''Outputs & returns customizable log message, with manually defined source.'''
        return f'{Fore.CYAN}[{src}-Log]{Fore.WHITE} - {msg}{Style.RESET_ALL}'

    @staticmethod
    def log(msg: str) -> AnyStr:
        '''Outputs & returns customizable log message, without manually defined source.'''
        return f'{Fore.CYAN}[Log]{Fore.WHITE} - {msg}{Style.RESET_ALL}'

    @staticmethod
    def src_warning(src: str, msg: str) -> AnyStr:
        '''Outputs & returns customizable warning message, with manually defined source.'''
        return f'{Fore.YELLOW}[{src}-Warn]{Fore.WHITE} - {msg}{Style.RESET_ALL}'

    @staticmethod
    def warning(msg: str) -> AnyStr:
        '''Outputs & returns customizable warning message, without manually defined source.'''
        return f'{Fore.YELLOW}[Warn]{Fore.WHITE} - {msg}{Style.RESET_ALL}'

    @staticmethod
    def src_error(src: str, msg: str) -> AnyStr:
        '''Outputs & returns customizable error message, without manually defined source.'''
        return f'{Fore.RED}[{src}-Error]{Fore.WHITE} - {msg}{Style.RESET_ALL}'

    @staticmethod
    def error(msg: str) -> AnyStr:
        '''Outputs & returns customizable error message, without manually defined source.'''
        return f'{Fore.RED}[Error]{Fore.WHITE} - {msg}{Style.RESET_ALL}'


# You can output colored text in 2 ways
# Use 1: print(ColorFormat.error('err-src', 'err-msg'))
# Use 2: colored_out(ColorFormat.error, 'err-src', 'err-msg')
def colored_out(text_format, *args):
    '''Acts as a optional wrapper function for @class ColoredText,
    responsible for outputting colored text returned 
    from @class ColoredText.'''
    try:
        print(text_format(*args))
        if text_format == ColorFormat.src_error or \
           text_format == ColorFormat.error:
            exit(1)
    except TypeError as e:
        print(ColorFormat.src_error('utils.py@colored_out', e))
        exit(1)


class ClassUtils:
    '''Automatically inherits a auto-adjusting __str__ and __repr__ method.'''
    def __str__(self):
        '''Uses reflection (__dict__) attribute to return the class name and
        inspect to get the class parameters.'''
        class_name = self.__class__.__name__
        class_args = inspect.signature(self.__init__)
        return f'{class_name}{class_args}'

    def __repr__(self):
        return self.__str__()


class LogOutput:
    '''Manages Log output with a level-based importance system.
    Note: Intended level use => The lower the level (1 being the lowest),
          the higher the priority of it. Can also be a list for multiple levels
          of output.'''
    def __init__(self, levels: list):
        '''Parameters:
        @level: Dev-mutable level of output importance.
                All func calls with given level will output.'''
        self.levels = levels

    def src_log(self, lvl: int, src: str, msg: str):
        '''ColorFormat.src_log wrapper with level importance sys implemented.'''
        if lvl in self.levels:
            print(f'{Fore.CYAN}[{src}-Log]{Fore.WHITE} - {msg}{Style.RESET_ALL}')

    def log(self, lvl: int, msg: str):
        '''ColorFormat.log wrapper with level importance sys implemented.'''
        if lvl in self.levels:
            print(f'{Fore.CYAN}[Log]{Fore.WHITE} - {msg}{Style.RESET_ALL}')