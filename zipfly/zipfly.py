# -*- coding: utf-8 -*-

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

    def __init__(self, mode='w', paths=None, chunksize=16, store_size=0):
        
        """
            @param store size : int : size of all files 
            in paths without compression
          
        """ 

        if mode not in ('w',):
            raise RunTimeError("requires mode w")

        self.comment = b'Written using Buzon-ZipFly'
        self.paths = paths
        self.chunksize = chunksize
        self.store_size = int(store_size)

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
       

    def get_size(self):
        
        return self._buffer_size


    def buffer_size(self):

        # using to get the buffer size
        # this size is different from the size of each file added

        for i in self.generator(): pass
        return self._buffer_size

    def buffer_prediction_size(self):

        """
            @CONSTANTS : bytes
            142, 48 : initial zipfile size             

        """
        LEN_PATHS = len( self.paths )
        LEN_UTF8 = 2 * LEN_PATHS
        LEN_INITIAL_ZIPFILE_ONE = 142 * LEN_PATHS
        LEN_INITIAL_ZIPFILE_MULTIPLE = 48 * ( LEN_PATHS -1 )


        def string_size_in_bytes(filename):
            
            # encode to utf-8 and get string's size
            """ python3 zipfile
            """         

            filename_size = 0
            for character in filename:
                filename_size += len(character.encode('utf-8')) * 2 
            
            # bytes size
            return filename_size 
        
        paths_filename_bytes_size=0
        for path in self.paths:
            paths_filename_bytes_size += string_size_in_bytes(path['name'])

        prediction_size = self.store_size + \
                          ( LEN_INITIAL_ZIPFILE_ONE ) - \
                          ( LEN_INITIAL_ZIPFILE_MULTIPLE ) + \
                          ( paths_filename_bytes_size - LEN_UTF8 )

        return prediction_size
  
    def generator(self):

        """
        @ from_file classemthod of ZipFile->ZipInfo

        filename should be the path to a file or directory on the filesystem.
        arcname is the name which it will have within the archive (by default,
        this will be the same as filename, but without a drive letter and with
        leading path separators removed).
        """           

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


    # close stream