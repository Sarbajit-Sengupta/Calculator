"""Exercise calculator button callbacks without a graphical Kivy window."""
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch


class Widget:
    def __init__(self, **kwargs):
        self.children = []
        self.callbacks = {}
        self.text = ''
        self.height = 100
        self.__dict__.update(kwargs)

    def add_widget(self, widget):
        self.children.insert(0, widget)

    def bind(self, **callbacks):
        self.callbacks.update(callbacks)


class CalculatorTests(unittest.TestCase):
    def test_zero_division_recovery_clear_and_resize(self):
        modules = {}
        for name, cls in [('kivy.app', 'App'), ('kivy.uix.button', 'Button'),
                          ('kivy.uix.boxlayout', 'BoxLayout'), ('kivy.uix.gridlayout', 'GridLayout'),
                          ('kivy.uix.label', 'Label')]:
            module = types.ModuleType(name)
            setattr(module, cls, Widget)
            modules[name] = module
        state = {'__name__': '__test__'}
        with patch.dict(sys.modules, modules):
            exec(compile(Path(__file__).with_name('main.py').read_text(), 'main.py', 'exec'), state)
        root = state['myApp']().build()
        clear, grid, output = root.children
        buttons = {button.text: button for button in grid.children}

        def press(text):
            for symbol in text:
                button = buttons[symbol]
                button.callbacks['on_press'](button)

        press('1/0=')
        self.assertEqual(output.text, 'Error')
        press('2+3=')
        self.assertEqual(output.text, '5')
        clear.callbacks['on_press'](clear)
        self.assertEqual(output.text, '')
        output.callbacks['height'](output, 100)
        self.assertEqual(output.font_size, 50)


if __name__ == '__main__':
    unittest.main()
