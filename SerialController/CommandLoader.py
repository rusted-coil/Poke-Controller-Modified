import importlib
import importlib.abc
import importlib.machinery
import os
import sys

import Utility as util


class _SourceOnlyLoader(importlib.machinery.SourceFileLoader):
    def get_code(self, fullname):
        # A same-size edit within one timestamp tick can leave a valid-looking
        # .pyc behind. Reload explicitly reads source, without deleting caches.
        source = self.get_data(self.path)
        return self.source_to_code(source, self.path)


class _CommandModuleFinder(importlib.abc.MetaPathFinder):
    def __init__(self, package):
        self.package = package

    def find_spec(self, fullname, path=None, target=None):
        if fullname != self.package and not fullname.startswith(self.package + '.'):
            return None
        spec = importlib.machinery.PathFinder.find_spec(fullname, path, target)
        if spec is not None and isinstance(spec.loader, importlib.machinery.SourceFileLoader):
            spec.loader = _SourceOnlyLoader(fullname, spec.origin)
        return spec


class CommandLoader:
    def __init__(self, base_path, base_class):
        self.path = base_path
        self.package = os.path.normpath(base_path).replace(os.sep, '.')
        self.base_type = base_class
        self.modules = []

    def load(self):
        if not self.modules:  # load if empty
            return self.reload()

        # return command class types
        return self.getCommandClasses()

    def reload(self):
        """Re-import the command package as a unit, keeping application state.

        Fresh modules let Python resolve dependencies normally, including
        ``from ... import ...``, and discard names deleted from source. Only
        this package is replaced; shared application modules (base classes,
        serial connections, GUI state, etc.) keep their identity.
        """
        module_names = util.getModuleNames(self.path)
        previous = self._loadedModules()
        parent_name, _, attribute = self.package.rpartition('.')
        parent = sys.modules.get(parent_name)
        missing = object()
        previous_attribute = vars(parent).get(attribute, missing) if parent else missing

        # Parent packages also cache child modules as attributes. Leaving this
        # binding behind can make `from parent import commands` return old code.
        for name in previous:
            sys.modules.pop(name, None)
        if parent is not None and attribute in vars(parent):
            delattr(parent, attribute)

        finder = _CommandModuleFinder(self.package)
        sys.meta_path.insert(0, finder)
        try:
            importlib.invalidate_caches()
            modules = util.importAllModules(self.path, module_names)
            classes = self._getCommandClasses(modules)
        except BaseException:
            # Do not leave half of a failed import mixed with the old commands.
            # Import-time side effects outside the command package cannot be
            # undone, but its modules and the previous command list stay usable.
            for name in self._loadedModules():
                sys.modules.pop(name, None)
            sys.modules.update(previous)
            parent = sys.modules.get(parent_name)
            if parent is not None:
                if previous_attribute is missing:
                    if attribute in vars(parent):
                        delattr(parent, attribute)
                else:
                    setattr(parent, attribute, previous_attribute)
            raise
        finally:
            sys.meta_path.remove(finder)

        self.modules = modules
        return classes

    def _loadedModules(self):
        return {name: module for name, module in list(sys.modules.items())
                if name == self.package or name.startswith(self.package + '.')}

    def getCommandClasses(self):
        return self._getCommandClasses(self.modules)

    def _getCommandClasses(self, modules):
        classes = []
        seen = set()
        for mod in modules:
            for command in util.getClassesInModule(mod):
                # A command imported by another script is not a second entry.
                if (command.__module__ == mod.__name__
                        and issubclass(command, self.base_type)
                        and getattr(command, 'NAME', None)
                        and command not in seen):
                    classes.append(command)
                    seen.add(command)

        return classes
