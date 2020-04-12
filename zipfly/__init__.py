# -*- coding: utf-8 -*-
"""
Iterable ZIP archive generator.

Derived directly from zipfile.py
"""
from __future__ import unicode_literals, print_function, with_statement

__version__ = '1.1.8'
__author__ = 'Santiago Debus - Buzon.io'
__license__ = 'MIT'

from .zipfly import ZipFly
from .api import from_one_file
