# -*- coding: utf-8 -*-

import io
import stat
import zipfile
from version import __version__
from stream import ZipflyStream

class ZipFly:

    def __init__(self,
                 mode = 'w',
                 paths = [],
                 chunksize = 0x4000,
                 compression = zipfile.ZIP_STORED,
                 allowZip64 = True,
                 compresslevel = None,
                 storesize = 0,
                 filesystem = 'fs',
                 arcname = 'n',
                 encode = 'utf-8',):

        """
        @param store size : int : size of all files
        in paths without compression
        """

        if mode not in ('w',):
            raise RuntimeError("ZipFly requires 'w' mode")

        if compression not in ( zipfile.ZIP_STORED,):
            raise RuntimeError("Not compression supported")

        if compresslevel not in (None, ):
            raise RuntimeError("Not compression level supported")


        self.comment = f'Written using Zipfly v{__version__}'
        self.mode = mode
        self.paths = paths
        self.filesystem = filesystem
        self.arcname = arcname
        self.chunksize = int(chunksize)
        self.compression = compression
        self.allowZip64 = allowZip64
        self.compresslevel = compresslevel
        self.storesize = storesize
        self.encode = encode
        self.ezs = 0x8e # empty zip size in bytes

    def set_comment(self, comment):

        if not isinstance(comment, bytes):
            comment = str.encode(comment)

        if len(comment) >= zipfile.ZIP_MAX_COMMENT:

            # trunk comment
            comment = comment[:zipfile.ZIP_MAX_COMMENT]

        self.comment = comment


    def reader(self, entry):

        def get_chunk():
            return entry.read( self.chunksize )

        return get_chunk()


    def buffer_size(self):

        '''
        FOR UNIT TESTING (not used)
        using to get the buffer size
        this size is different from the size of each file added
        '''

        for i in self.generator(): pass
        return self._buffer_size


    def buffer_prediction_size(self):

        '''
        BufferPredictionSize.
        :var    hexadecimal     LIZO:     Initial length for one file
        :var    hexadecimal     LIZM:     Initial length for multiples files (null for one file)
        :var    hexadecimal     COMM:     Comment length in bytes set to 26 bytes (magic number)

        Initialize a Buffer
        :arg    integer     pfbs:           Buffer variable to return
        :arg    integer     storesize:      Initial storesize
        :arg    bytes       comment:        Buffer comment zip file

        getting bytes from character in UTF-8 format
        example:
            1) 'a' has 1 byte in utf-8 format ( b'a' )
            2) 'ñ' has 2 bytes in utf-8 format ( b'\xc3\xb1' )
            3) '传' has 3 bytes in utf-8 format ( b'\xe4\xbc\xa0' )
        '''

        # initial values
        _len = len( self.paths )
        _len_utf8 = int( 0x2 ) * _len

        LIZO = int( 0x8e ) * _len
        LIZM = int( 0x30 ) * ( _len - 1 )

        # comment
        tmp_comment = self.comment
        if isinstance(self.comment, bytes):
            tmp_comment = ( self.comment ).decode()

        COMM = int( 0x1a )
        tmp_s = 0
        for c in tmp_comment:
            tmp_s += len( c.encode(self.encode) )
        COMM = tmp_s - COMM

        # files names
        bt = 0
        for path in self.paths:
            tmp_bt = 0

            name = self.arcname
            if not self.arcname in path:
                name = self.filesystem

            tmp_name = path[name]
            if (tmp_name)[0] in ('/', ):
                # is dir then trunk
                tmp_name = (tmp_name)[ 1 : len( tmp_name ) ]

            for c in tmp_name:
                tmp_bt += len( c.encode(self.encode) ) * int( 0x2 )

            bt += tmp_bt

        # current process size
        pfbs = (
            bt + COMM + self.storesize
        )

        # simple arithmetic
        return int(
            LIZO - LIZM + pfbs -  _len_utf8
        )

    def generator(self):

        # stream
        stream = ZipflyStream()

        with zipfile.ZipFile(
            stream,
            mode = self.mode,
            compression = self.compression,
            allowZip64 = self.allowZip64,) as zf:

            for path in self.paths:

                if not self.filesystem in path:

                    raise RuntimeError(
                        f" '{self.filesystem}' key is required "
                    )

                """
                filesystem should be the path to a file or directory on the filesystem.
                arcname is the name which it will have within the archive (by default,
                this will be the same as filename
                """

                if not self.arcname in path:

                    # arcname will be default path
                    path[self.arcname] = path[self.filesystem]

                z_info = zipfile.ZipInfo.from_file(
                    path[self.filesystem],
                    path[self.arcname]
                )

                with open( path[self.filesystem], 'rb' ) as e:
                    # Read from filesystem:

                    with zf.open( z_info, mode = self.mode ) as d:

                        for chunk in iter( lambda: e.read( self.chunksize ), b'' ):

                            # (e.read( ... )) this get a small chunk of the file
                            # and return a callback to the next iterator

                            d.write( chunk )
                            yield stream.get()


            self.set_comment(self.comment)
            zf.comment = self.comment

        # last chunk
        yield stream.get()

        # (TESTING)
        # get the real size of the zipfile
        self._buffer_size = stream.size()

        # Flush and close this stream.
        stream.close()


    def get_size(self):

        return self._buffer_size
