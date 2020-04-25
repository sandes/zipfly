# -*- coding: utf-8 -*-

import sys


def from_one_file(file_location):

    """read a file piece by piece.
    Default chunk size 1024 * 16 bytes"""

    with open(file_location, 'rb') as entry:

        for chunk in iter(lambda: entry.read(1024 * 16), b''):

            yield chunk


class Utils:

    def string_size_in_bytes(filename):
        
        # encode to utf-8 and get string's size
        """ python3 zipfile
        """         

        tmp_b = 0
        for c in filename:
            tmp_b += len( c.encode('utf-8') ) * int(0x2)
        
        # bytes size
        return tmp_b 