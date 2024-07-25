import os
import importlib
from pkg.utils.lang import safe_attribute_chain


_modules = [file for file in os.listdir(os.path.dirname(__file__)) if not file.startswith('__') and file.endswith('py')]

_imported_modules = [importlib.import_module(f'.{file.replace('.py', '')}', package=__name__) for file in _modules]
_imported_builders = [safe_attribute_chain(lambda: module.Builder) for module in _imported_modules]

crawler_builders = dict([(Builder.NAME, Builder.make) for Builder in _imported_builders])
