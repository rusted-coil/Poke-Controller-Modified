"""Reload UI regression tests without opening a window or connecting devices."""

import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock


SOURCE = Path(__file__).resolve().parents[1] / 'SerialController' / 'Window.py'


class ComboBox:
    """The selection operations used by the command UI, including duplicate labels."""

    def __init__(self):
        self.values = []
        self.value = ''
        self.index = -1

    def __getitem__(self, key):
        assert key == 'values'
        return self.values

    def __setitem__(self, key, values):
        assert key == 'values'
        self.values = list(values)

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
        if not (0 <= self.index < len(self.values) and self.values[self.index] == value):
            self.index = self.values.index(value) if value in self.values else -1

    def current(self, index=None):
        if index is not None:
            self.index = index
            self.value = self.values[index]
        return self.index


def load_app_methods(dialogs):
    # Compile the production methods while avoiding Window.py's camera/GUI imports.
    tree = ast.parse(SOURCE.read_text(encoding='utf-8-sig'))
    app = next(node for node in tree.body
               if isinstance(node, ast.ClassDef) and node.name == 'PokeControllerApp')
    methods = {'_getCommandTag', '_getSelectedCommandKey', 'setCommandItems',
               'assignCommand', 'reloadCommands', 'ReloadCommandWithF5'}
    app.body = [node for node in app.body
                if isinstance(node, ast.FunctionDef) and node.name in methods]
    tree.body = [app]
    namespace = {
        'CustomPythonCommand': type('CustomPythonCommand', (), {}),
        'PythonCommandBase': SimpleNamespace(ImageProcPythonCommand=type('ImageCommand', (), {})),
        'tkmsg': dialogs,
    }
    exec(compile(tree, str(SOURCE), 'exec'), namespace)
    return namespace['PokeControllerApp']


class CommandReloadUITests(unittest.TestCase):
    def setUp(self):
        self.dialogs = Mock()
        self.app_type = load_app_methods(self.dialogs)

    @staticmethod
    def command(module, label):
        return type('Example', (), {'__module__': module, 'NAME': label})

    def app(self, classes, index=0):
        app = self.app_type()
        app.tag_cb = ComboBox()
        app.py_cb = ComboBox()
        app.py_classes = classes
        app.startButton = {'text': 'Start'}
        app._logger = Mock()
        app.py_loader = Mock()
        app.setCommandItems()
        app.py_cb.current(index)
        app.assignCommand()
        return app

    def test_f5_does_not_reload_while_command_is_running(self):
        app = self.app([self.command('scripts.one', 'One')])
        original = app.cur_command
        app.startButton['text'] = 'Stop'

        app.ReloadCommandWithF5()

        app.py_loader.reload.assert_not_called()
        self.assertIs(app.cur_command, original)
        self.dialogs.showwarning.assert_called_once()

    def test_reload_waits_for_thread_even_when_start_button_has_reset(self):
        app = self.app([self.command('scripts.one', 'One')])
        original = app.cur_command
        original.thread = SimpleNamespace(is_alive=lambda: True)

        app.reloadCommands()

        app.py_loader.reload.assert_not_called()
        self.assertIs(app.cur_command, original)
        self.dialogs.showwarning.assert_called_once()

    def test_failed_reload_preserves_list_selection_and_instance(self):
        app = self.app([self.command('scripts.one', 'Same'),
                        self.command('scripts.two', 'Same')], index=1)
        original_classes = app.py_classes
        original_filtered = app.filtered_py_classes
        original_command = app.cur_command
        app.py_loader.reload.side_effect = SyntaxError('invalid edited script')

        app.reloadCommands()

        self.assertIs(app.py_classes, original_classes)
        self.assertIs(app.filtered_py_classes, original_filtered)
        self.assertIs(app.cur_command, original_command)
        self.assertEqual(app.py_cb.current(), 1)
        app._logger.exception.assert_called_once()
        self.dialogs.showerror.assert_called_once()
        self.assertIn('invalid edited script', self.dialogs.showerror.call_args[0][1])

    def test_duplicate_names_preserve_selected_class_after_reordering(self):
        app = self.app([self.command('scripts.one', 'Same'),
                        self.command('scripts.two', 'Same')], index=1)
        updated_one = self.command('scripts.one', 'Same')
        updated_two = self.command('scripts.two', 'Same')
        app.py_loader.reload.return_value = [updated_two, updated_one]

        app.reloadCommands()

        self.assertEqual(app.py_cb.current(), 0)
        self.assertIs(type(app.cur_command), updated_two)
        self.dialogs.showerror.assert_not_called()

    def test_name_edit_preserves_selected_class(self):
        app = self.app([self.command('scripts.one', 'One'),
                        self.command('scripts.two', 'Old name')], index=1)
        updated_two = self.command('scripts.two', 'New name')
        app.py_loader.reload.return_value = [self.command('scripts.one', 'One'), updated_two]

        app.reloadCommands()

        self.assertEqual(app.py_cb.get(), 'New name')
        self.assertIs(type(app.cur_command), updated_two)


if __name__ == '__main__':
    unittest.main()
