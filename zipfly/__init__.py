# -*- coding: utf-8 -*-
"""
Iterable ZIP archive generator.

Derived directly from zipfile.py
"""
from __future__ import unicode_literals, print_function, with_statement

__version__ = '1.1.4'

from zipfile import (
    ZIP_STORED,
    ZIP64_LIMIT,
    ZIP_FILECOUNT_LIMIT, 
    ZIP_MAX_COMMENT,
    ZIP_DEFLATED,
    zlib,
    crc32
)

import stat
import io
from io import RawIOBase
from zipfile import ZipFile, ZipInfo


class Stream(RawIOBase):
    def __init__(self):
        self._buffer = b''
        self._size=0

    def writable(self):
        return True

    def write(self, b):
        if self.closed:
            raise ValueError('Stream was closed!')
        self._buffer += b
        return len(b)
    
    def get(self):
        chunk = self._buffer
        self._buffer = b''
        self._size += len(chunk)
        return chunk

    def size(self):
        return self._size


class ZipFly:

    def __init__(self, mode='w', paths=None, chunksize=16):
        
        if mode not in ('w',):
            raise RunTimeError("requires mode w")

        self.comment = b'Written using Buzon-ZipFly'
        self.paths = paths
        self.chunksize = chunksize

    def set_comment(self, comment):

        if not isinstance(comment, bytes):
            str.encode(comment)

        if len(comment) >= ZIP_MAX_COMMENT:

            # trunk comment
            comment = comment[:ZIP_MAX_COMMENT]

        self.comment = comment

    def reader(self, entry):

        def get_chunk():
            return entry.read(1024 * self.chunksize)

        return get_chunk()

    def buffer_size(self):

        # using to get the buffer size
        # this size is different from the size of each file added
        
        return self._buffer_size
  
    def generator(self):

        stream = Stream()
        
        with ZipFile(stream, mode='w', ) as zf:

            for path in self.paths:

                z_info = ZipInfo.from_file(path['filesystem'], path['name'])

                with open(path['filesystem'], 'rb') as entry:
                    
                    with zf.open(z_info, mode='w') as dest:

                        for chunk in iter(lambda: entry.read(1024 * self.chunksize), b''):
                            dest.write(chunk)
                            # Yield chunk of the zip file stream in bytes.
                            yield stream.get()


            zf.comment = self.comment

        yield stream.get()
        self._buffer_size = stream.size()
        stream.close()