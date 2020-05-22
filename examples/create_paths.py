# create paths

import zipfly
import os

parent = "/home/user/Documents/folder/"
paths = []

# Create paths
for dirpath, dnames, fnames in os.walk(parent):
    for f in fnames:
        paths.append(
            {
                'fs': f'{parent}{f}',
                'n': f'large_folder/{f}',
            }
        )    

# ZipFly
zfly = zipfly.ZipFly( paths = paths )

with open("large.zip", "wb") as f:
    for i in zfly.generator():
        f.write(i)