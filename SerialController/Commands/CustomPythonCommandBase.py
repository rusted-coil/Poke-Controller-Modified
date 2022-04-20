#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import DEBUG, NullHandler, getLogger
from Commands.PythonCommandBase import PythonCommand

class CustomPythonCommand(PythonCommand):
    def __init__(self, preview):
        super(CustomPythonCommand, self).__init__()

        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True

        self.Preview = preview
