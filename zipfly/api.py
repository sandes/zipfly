# -*- coding: utf-8 -*-
import sys

class Buffer:

    def __init__(self,
                 paths = [],
                 storesize = 0,
                 comment = b''):

        self.paths = paths
        self.pfbs = 0
        self.storesize = int(storesize)
        self.comment = comment
