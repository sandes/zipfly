# -*- coding: utf-8 -*-

class FileResponse:

    """read a file piece by piece.
    Default chunk size 0x4000 bytes"""

    def __init__(self,
                 file_location = '/',
                 chunksize = int(0x4000)):

        self.file_location = file_location
        self.chunksize = chunksize


    def __iter__(self):

        with open(self.file_location, 'rb') as entry:

            for chunk in iter(lambda: entry.read(self.chunksize), b''):

                yield chunk