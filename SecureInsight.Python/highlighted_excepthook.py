
import sys
import traceback
from pygments import highlight
from abc import ABC, abstractmethod
from colorama import init, Fore, Style
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

class IExceptionHighlighter(ABC):
    @abstractmethod
    def highlight_traceback(self, type, value, tb):
        pass

class ICustomExceptHook(ABC):
    @abstractmethod
    def excepthook(self, type, value, tb):
        pass
    
class ExceptionHighlighter(IExceptionHighlighter):
    def __init__(self, lexer_name="py3tb"):
        init()
        self.lexer = get_lexer_by_name(lexer_name)
        self.formatter = TerminalFormatter()

    def highlight_traceback(self, type, value, tb):
        tbtext = ''.join(traceback.format_exception(type, value, tb))
        return highlight(tbtext, self.lexer, self.formatter)

class CustomExceptHook(ICustomExceptHook):
    def __init__(self, highlighter):
        self.highlighter = highlighter

    def _get_exception_color(self, type):
        exception_colors = {
            ValueError: Fore.RED,
            TypeError: Fore.YELLOW,
            KeyError: Fore.BLUE,
            IndexError: Fore.CYAN,
            ArithmeticError: Fore.MAGENTA,
            AssertionError: Fore.LIGHTRED_EX,
            AttributeError: Fore.LIGHTGREEN_EX,
            EOFError: Fore.LIGHTBLUE_EX,
            ImportError: Fore.LIGHTMAGENTA_EX,
            LookupError: Fore.LIGHTCYAN_EX,
            MemoryError: Fore.LIGHTWHITE_EX,
            NameError: Fore.LIGHTYELLOW_EX,
            OSError: Fore.LIGHTBLACK_EX,
            ReferenceError: Fore.LIGHTBLUE_EX,
            RuntimeError: Fore.LIGHTMAGENTA_EX,
            StopIteration: Fore.LIGHTGREEN_EX,
            StopAsyncIteration: Fore.LIGHTCYAN_EX,
            SyntaxError: Fore.LIGHTRED_EX,
            SystemError: Fore.LIGHTWHITE_EX,
            Warning: Fore.LIGHTYELLOW_EX,
        }
        return exception_colors.get(type, Fore.RESET)

    def excepthook(self, type, value, tb):
        color = self._get_exception_color(type)
        highlighted_tbtext = self.highlighter.highlight_traceback(type, value, tb)
        sys.stderr.write(color + highlighted_tbtext + Style.RESET_ALL)

class ExceptionSetup:
    """
    Class responsible for setting up the exception highlighter and custom exception hook.
    """
    def __init__(self):
        # Determine the appropriate lexer for syntax highlighting based on the Python version
        lexer_name = "pytb" if sys.version_info.major < 3 else "py3tb"
        # Create an ExceptionHighlighter instance
        self.highlighter = ExceptionHighlighter(lexer_name)
        # Create a CustomExceptHook instance with the highlighter
        self.custom_hook = CustomExceptHook(self.highlighter)

    def setup_exception_hook(self):
        """
        Set the custom exception hook that highlights tracebacks.
        """
        set_highlighted_excepthook(self.highlighter, self.custom_hook)

def set_highlighted_excepthook(highlighter: IExceptionHighlighter, hook: ICustomExceptHook):
    sys.excepthook = hook.excepthook
