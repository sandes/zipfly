# -*- coding: utf-8 -*-

import sys


def from_one_file(file_object, chunk_size=1024*16):
    
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size 1024 * 16 bytes"""

    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data




    with open('really_big_file.dat') as f:
        for piece in from_one_file(f):
            process_data(piece)