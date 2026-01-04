"""
    Commands Package
"""

import pkgutil
import importlib

__all__ = []

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    module = importlib.import_module(f"{__name__}.{module_name}")
    globals()[module_name] = module  # Add module to package namespace
    __all__.append(module_name)

del pkgutil
del importlib
