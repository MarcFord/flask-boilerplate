import os
import sys
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, 'models')
for f in os.listdir(path):
    if f.endswith('.py') and f != '__init__.py':
        package = f[:-3]
        import_path = '.'.join(['models', package])
        mod = __import__(import_path, fromlist=[package])
        classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
        for cls in classes:
            setattr(sys.modules[__name__], cls.__name__, cls)

register_models = None
