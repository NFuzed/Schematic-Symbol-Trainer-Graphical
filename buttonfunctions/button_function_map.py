from traitlets import Callable

from . load_file import *


BUTTON_FUNCTION_MAP: dict[str, any] = {
    "btn_load": lambda core: load_file()
}