# easy way to create the array paths 

import os

parent = "/home/user/Documents/large_files/"
paths = []

for dirpath, dnames, fnames in os.walk(parent):
    for f in fnames:
        paths.append(
            {
                'fs': f'{parent}{f}',
                'n': f'large_files/{f}',
            }
        )