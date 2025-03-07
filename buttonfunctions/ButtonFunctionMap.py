from . LoadFile import *


BUTTON_FUNCTION_MAP: dict[str, any] = {
    "btn_load": lambda core: loadFile(core)
}