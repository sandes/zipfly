# -*- coding: utf-8 -*-

import sys


def from_one_file(file_location):

    """read a file piece by piece.
    Default chunk size 1024 * 16 bytes"""

    with open(file_location, 'rb') as entry:

        for chunk in iter(lambda: entry.read(1024 * 16), b''):

            yield chunk


