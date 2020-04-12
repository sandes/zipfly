# -*- coding: utf-8 -*-

import sys


def from_one_file(file_object):
    
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size 1024 * 16 bytes"""

    while True:
        data = file_object.read(1024*16)
        if not data:
            break
        yield data



