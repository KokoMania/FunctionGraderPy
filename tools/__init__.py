import importlib
import os

# Get the current directory
_pkg_dir = os.path.dirname(__file__)

# List all .py files (except __init__.py)
_modules = [
    f[:-3]
    for f in os.listdir(_pkg_dir)
    if f.endswith(".py") and f not in ("__init__.py",)
]

# Import each module automatically
for _mod in _modules:
    importlib.import_module(f"{__name__}.{_mod}")

# Optional: make them available directly via `from tools import <module>`
__all__ = _modules
