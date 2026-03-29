# Python imports
import os
import ctypes

# Lib imports

# Application imports
from .libs.tree_sitter import Language, Parser



_LIB_PATH     = os.path.join(
    os.path.dirname(__file__), "languages", "languages.so"
)
_LANGUAGE_LIB = ctypes.CDLL(_LIB_PATH)



def load_language(name: str) -> Language | None:
    symbol   = f"tree_sitter_{name}"

    try:
        func = getattr(_LANGUAGE_LIB, symbol)
    except AttributeError:
        logger.warning(f"Tree-sitter: {name} not found in 'languages.so' shared library...")
        return None

    func.restype = ctypes.c_void_p
    return Language(func())


LANGUAGES = {
    "python": load_language("python"),
    "python3": load_language("python"),
    "javascript": load_language("javascript"),
    "html": load_language("html"),
    "css": load_language("css"),
    "json": load_language("json"),
    "java": load_language("java"),
    "c": load_language("c"),
    "cpp": load_language("cpp"),
    "go": load_language("go")
}


def get_parser(lang_name: str) -> Parser | None:
    if not lang_name in LANGUAGES: return

    language = LANGUAGES[lang_name]

    if not language: return

    parser          = Parser()
    parser.language = language

    return parser

