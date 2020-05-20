# -*- coding: utf-8 -*-

import sys


def from_one_file(file_location, chunksize=int(0x4000)):

    """read a file piece by piece.
    Default chunk size 0x4000 bytes"""

    with open(file_location, 'rb') as entry:

        for chunk in iter(lambda: entry.read(chunksize), b''):

            yield chunk


class Buffer:

    def __init__(self, paths, ss=0):
        self.paths = paths
        self.pfbs = 0
        self.storesize = int( ss )

        
        #paths_size_in_bytes(self)
        # encode to utf-8 and get string's size
        """ python3 zipfile
        """

        bt = 0
        for path in self.paths:

            tmp_bt = 0
            for c in path['n']:

                """
                getting bytes from character in UTF-8 format
                example: 
                    1) 'a' has 1 byte in utf-8 format ( b'a' )
                    2) 'ñ' has 2 bytes in utf-8 format ( b'\xc3\xb1' )
                    3) '传' has 3 bytes in utf-8 format ( b'\xe4\xbc\xa0' )
                """

                tmp_bt += len( c.encode('utf-8') ) * int( 0x2 )

            # bytes size
            bt += tmp_bt

        self.pfbs = bt + self.storesize

    


