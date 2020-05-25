# -*- coding: utf-8 -*-

"""
pythoncompat

Copied from requests
"""

import sys

PY3 = sys.version_info[0] == 3

builtin_str = str
str = str
bytes = bytes
basestring = (str, bytes)
numeric_types = (int, float)

from zipfile import ZIP64_VERSION
from zipfile import BZIP2_VERSION
from zipfile import ZIP_BZIP2
from zipfile import LZMA_VERSION
from zipfile import ZIP_LZMA
from zipfile import ZIP_MAX_COMMENT

# Copy from io
SEEK_SET = 0  # start of the stream (the default); offset should be zero or positive
SEEK_CUR = 1  # current stream position; offset may be negative
SEEK_END = 2  # end of the stream; offset is usually negative
