"""Reload regression tests using isolated scripts, without GUI or hardware."""

import importlib
import marshal
import os
from pathlib import Path
import struct
import sys
import tempfile
import textwrap
import unittest
import uuid


SOURCE_DIR = Path(__file__).resolve().parents[1] / 'SerialController'
sys.path.insert(0, str(SOURCE_DIR))
from CommandLoader import CommandLoader
import Utility


class CommandLoaderReloadTests(unittest.TestCase):
    def setUp(self):
        self.original_cwd = os.getcwd()
        self.original_path = list(sys.path)
        self.temp = tempfile.TemporaryDirectory(prefix='poke_loader_test_')
        self.root = Path(self.temp.name)
        self.package = 'reload_fixture_' + uuid.uuid4().hex
        self.module_prefix = self.package + '.commands'
        self.command_path = os.path.join(self.package, 'commands')
        self.write(self.package + '/__init__.py', '')
        self.write(self.package + '/base.py', '''
            class Command:
                pass
        ''')
        (self.root / self.command_path).mkdir()
        os.chdir(str(self.root))
        sys.path.insert(0, str(self.root))
        self.base_module = importlib.import_module(self.package + '.base')
        self.loader = CommandLoader(self.command_path, self.base_module.Command)

    def tearDown(self):
        os.chdir(self.original_cwd)
        sys.path[:] = self.original_path
        for name in list(sys.modules):
            if name == self.package or name.startswith(self.package + '.'):
                del sys.modules[name]
        importlib.invalidate_caches()
        self.temp.cleanup()

    def write(self, relative_path, source):
        destination = self.root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(textwrap.dedent(source).lstrip('\n'), encoding='utf-8')
        return destination

    def script(self, relative_path, source):
        return self.write(self.command_path + '/' + relative_path, source)

    def entry(self, imports, body, filename='entry.py', classname='Example', name='Example'):
        return self.script(filename, '\n'.join([
            'from {}.base import Command'.format(self.package),
            imports,
            'class {}(Command):'.format(classname),
            '    NAME = {!r}'.format(name),
            textwrap.indent(textwrap.dedent(body).strip(), '    '),
            '',
        ]))

    @staticmethod
    def only(classes):
        if len(classes) != 1:
            raise AssertionError('Expected one command, got {}'.format(classes))
        return classes[0]

    def test_single_script_edit_takes_effect_after_one_reload(self):
        self.entry('', 'def value(self):\n    return "old"')
        self.assertEqual(self.only(self.loader.load())().value(), 'old')
        self.entry('', 'def value(self):\n    return "updated"')
        self.assertEqual(self.only(self.loader.reload())().value(), 'updated')

    def test_imported_class_function_and_constant_refresh_together(self):
        def write_helper(value):
            self.script('helper.py', '''
                VALUE = {value!r}
                def read():
                    return {value!r}
                class Shared:
                    def read(self):
                        return {value!r}
            '''.format(value=value))

        write_helper('old')
        self.entry('from .helper import VALUE, read, Shared', '''
            def value(self):
                return VALUE, read(), Shared().read()
        ''')
        self.assertEqual(self.only(self.loader.load())().value(), ('old',) * 3)
        write_helper('updated')
        self.assertEqual(self.only(self.loader.reload())().value(), ('updated',) * 3)

    def test_three_level_from_import_dependency_refreshes_once(self):
        self.script('third.py', 'class Third:\n    def value(self):\n        return "old"\n')
        self.script('second.py', 'from .third import Third\nclass Second(Third):\n    pass\n')
        self.script('first.py', 'from .second import Second\nclass First(Second):\n    pass\n')
        self.entry('from .first import First', 'def value(self):\n    return First().value()')
        self.assertEqual(self.only(self.loader.load())().value(), 'old')
        self.script('third.py', 'class Third:\n    def value(self):\n        return "updated"\n')
        self.assertEqual(self.only(self.loader.reload())().value(), 'updated')

    def test_deleted_class_does_not_survive_in_module_dictionary(self):
        self.entry('', 'pass')
        self.assertEqual(len(self.loader.load()), 1)
        self.script('entry.py', 'VALUE = "no commands"\n')
        self.assertEqual(self.loader.reload(), [])
        self.assertFalse(hasattr(sys.modules[self.module_prefix + '.entry'], 'Example'))

    def test_renamed_class_replaces_old_definition(self):
        self.entry('', 'pass', classname='OldCommand', name='Old')
        self.loader.load()
        self.entry('', 'pass', classname='NewCommand', name='New')
        command = self.only(self.loader.reload())
        self.assertEqual(command.__name__, 'NewCommand')
        self.assertEqual(command.NAME, 'New')
        self.assertFalse(hasattr(sys.modules[self.module_prefix + '.entry'], 'OldCommand'))

    def test_deleted_file_and_renamed_file_remove_old_modules(self):
        old_path = self.entry('', 'pass', filename='old_entry.py')
        self.loader.load()
        # Model the on-disk result of a rename, without requiring rename permission.
        old_path.with_name('new_entry.py').write_bytes(old_path.read_bytes())
        old_path.unlink()
        command = self.only(self.loader.reload())
        self.assertEqual(command.__module__, self.module_prefix + '.new_entry')
        self.assertNotIn(self.module_prefix + '.old_entry', sys.modules)
        self.assertFalse(hasattr(sys.modules[self.module_prefix], 'old_entry'))
        old_path.with_name('new_entry.py').unlink()
        self.assertEqual(self.loader.reload(), [])
        self.assertNotIn(self.module_prefix + '.new_entry', sys.modules)

    def test_new_dependency_is_available_on_first_reload(self):
        self.entry('', 'def value(self):\n    return "old"')
        self.loader.load()
        self.script('new_helper.py', 'VALUE = "new dependency"\n')
        self.entry('from .new_helper import VALUE', 'def value(self):\n    return VALUE')
        self.assertEqual(self.only(self.loader.reload())().value(), 'new dependency')

    def test_package_init_reexports_are_refreshed_and_normalized(self):
        self.script('__init__.py', 'from .helper import VALUE, Shared\n')
        self.script('helper.py', 'VALUE = "old"\nclass Shared:\n    value = "old"\n')
        self.entry('from . import VALUE, Shared', 'def value(self):\n    return VALUE, Shared.value')
        self.assertEqual(self.only(self.loader.load())().value(), ('old', 'old'))
        self.script('helper.py', 'VALUE = "updated"\nclass Shared:\n    value = "updated"\n')
        self.assertEqual(self.only(self.loader.reload())().value(), ('updated', 'updated'))
        module_names = Utility.getModuleNames(self.command_path)
        self.assertIn(self.module_prefix, module_names)
        self.assertNotIn(self.module_prefix + '.__init__', module_names)
        self.assertNotIn(self.module_prefix + '.__init__', sys.modules)

    def test_from_package_import_submodule_has_no_stale_parent_attribute(self):
        self.script('helper.py', 'VALUE = "old"\n')
        self.entry('from . import helper', 'def value(self):\n    return helper.VALUE')
        self.loader.load()
        parent = sys.modules[self.package]
        old_commands_package = parent.commands
        old_helper = old_commands_package.helper
        self.script('helper.py', 'VALUE = "updated"\n')
        self.assertEqual(self.only(self.loader.reload())().value(), 'updated')
        self.assertIs(parent.commands, sys.modules[self.module_prefix])
        self.assertIs(parent.commands.helper, sys.modules[self.module_prefix + '.helper'])
        self.assertIsNot(parent.commands, old_commands_package)
        self.assertIsNot(parent.commands.helper, old_helper)

    def test_same_timestamp_and_size_bytecode_does_not_hide_source_change(self):
        helper = self.script('helper.py', 'VALUE = "old"\n')
        timestamp = 1600000000
        os.utime(str(helper), (timestamp, timestamp))
        # A valid timestamp cache, written directly because py_compile uses an
        # atomic rename that some restricted Windows environments disallow.
        cache = Path(importlib.util.cache_from_source(str(helper)))
        cache.parent.mkdir(parents=True, exist_ok=True)
        header = importlib.util.MAGIC_NUMBER
        if sys.version_info >= (3, 7):
            header += struct.pack('<I', 0)  # Timestamp-based cache flags.
        header += struct.pack('<II', timestamp, helper.stat().st_size)
        cache.write_bytes(header + marshal.dumps(compile(helper.read_bytes(), str(helper), 'exec')))
        self.entry('from .helper import VALUE', 'def value(self):\n    return VALUE')
        self.assertEqual(self.only(self.loader.load())().value(), 'old')
        old_size = helper.stat().st_size
        self.script('helper.py', 'VALUE = "new"\n')
        os.utime(str(helper), (timestamp, timestamp))
        self.assertEqual(helper.stat().st_size, old_size)
        cached_globals = {}
        module_name = self.module_prefix + '.helper'
        cached_code = importlib.machinery.SourceFileLoader(module_name, str(helper)).get_code(module_name)
        exec(cached_code, cached_globals)
        self.assertEqual(cached_globals['VALUE'], 'old')
        self.assertEqual(self.only(self.loader.reload())().value(), 'new')

    def test_external_base_module_and_class_identity_are_preserved(self):
        self.entry('', 'pass')
        self.loader.load()
        old_base = self.base_module.Command
        self.write(self.package + '/base.py', 'class Command:\n    changed = True\n')
        command = self.only(self.loader.reload())
        self.assertIs(sys.modules[self.package + '.base'], self.base_module)
        self.assertIs(self.base_module.Command, old_base)
        self.assertTrue(issubclass(command, old_base))
        self.assertFalse(hasattr(old_base, 'changed'))

    def test_failed_reload_restores_modules_parent_attributes_and_commands(self):
        self.script('__init__.py', 'from . import helper\n')
        self.script('helper.py', 'VALUE = "old"\n')
        self.entry('from .helper import VALUE', 'def value(self):\n    return VALUE')
        old_command = self.only(self.loader.load())
        old_modules = self.loader.modules
        snapshot = {name: module for name, module in sys.modules.items()
                    if name == self.module_prefix or name.startswith(self.module_prefix + '.')}
        parent = sys.modules[self.package]
        old_package = parent.commands
        self.script('helper.py', 'VALUE = "updated"\n')
        self.entry('from .helper import VALUE\nfrom .new_helper import ADDED',
                   'def value(self):\n    return VALUE, ADDED')
        self.script('new_helper.py', 'ADDED = "added"\n')
        self.script('zz_broken.py', 'def broken(:\n')
        with self.assertRaises(SyntaxError):
            self.loader.reload()
        self.assertIs(self.loader.modules, old_modules)
        self.assertIs(self.only(self.loader.getCommandClasses()), old_command)
        self.assertEqual(old_command().value(), 'old')
        self.assertIs(parent.commands, old_package)
        for name, module in snapshot.items():
            self.assertIs(sys.modules[name], module)
        self.assertIs(parent.commands.helper, snapshot[self.module_prefix + '.helper'])
        self.assertNotIn(self.module_prefix + '.new_helper', sys.modules)
        self.assertNotIn(self.module_prefix + '.zz_broken', sys.modules)
        self.assertFalse(hasattr(parent.commands, 'new_helper'))
        self.script('zz_broken.py', '# corrected\n')
        self.assertEqual(self.only(self.loader.reload())().value(), ('updated', 'added'))

    def test_imported_aliases_do_not_duplicate_commands_with_same_display_name(self):
        self.entry('', 'pass', filename='first.py', classname='First', name='Same label')
        self.entry('', 'pass', filename='second.py', classname='Second', name='Same label')
        self.script('consumer.py', 'from .first import First\nAlias = First\n')
        with (self.root / self.command_path / 'first.py').open('a', encoding='utf-8') as stream:
            stream.write('AnotherAlias = First\n')
        for classes in (self.loader.load(), self.loader.reload()):
            self.assertEqual(len(classes), 2)
            self.assertEqual({command.__name__ for command in classes}, {'First', 'Second'})
            self.assertEqual([command.NAME for command in classes], ['Same label'] * 2)


if __name__ == '__main__':
    unittest.main()
