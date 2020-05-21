[![Build Status](https://travis-ci.com/BuzonIO/zipfly.svg?branch=master)](https://travis-ci.com/BuzonIO/zipfly)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/buzonio/zipfly)
[![Downloads](https://pepy.tech/badge/zipfly)](https://pepy.tech/project/zipfly)

# Buzon - ZipFly

ZipFly is a zip archive generator based on zipfile.py.
It was created by Buzon.io to generate very large ZIP archives for immediate sending out to clients, or for writing large ZIP archives without memory inflation.

# Requirements
Python 3.5+

# Install
    pip3 install zipfly

# Basic usage, compress on-the-fly during writes
Basic use case is compressing on the fly. Some data will be buffered by the zipfile deflater, but memory inflation is going to be very constrained. Data will be written to destination at fairly regular intervals.

`ZipFly` class may have arguments (defaults) for greater flexibility:<br>    
- <b>paths:</b> [ ] <br/>
- <b>mode:</b> w <br/>
- <b>chunksize:</b> (bytes) 16384 <br/>
- <b>compression:</b> Stored <br/>
- <b>allowZip64:</b> True <br/>
- <b>compresslevel:</b> None <br/>
- <b>storesize:</b> (bytes) 0 <br/>


<br/>

`paths` <b>list of dictionaries:</b>

- `fs` (filesystem): `path from your disk`<br>
- `n` (name): `final path in zip file`


```python
    import zipfly
    
    paths = [ 
        {
            'fs': 'home/user/Videos/jupiter.mp4', 
            'n': 'movies/jupiter.mp4', 
        },       
        {
            'fs': 'home/user/Documents/mercury.mp4', 
            'n': 'movies/mercury.mp4', 
        },          
    ]

    zfly = zipfly.ZipFly( paths = paths )

    generator = zfly.generator()
    print ( generator )
    # <generator object generator at 0x7f85aad60b13>

    with open("test.zip", "wb") as f:
        for i in generator:
            f.write(i)


```
# Examples

> <b>Create a ZIP file with size estimation</b>
Use the `BufferPredictionSize` to compute the correct size of the resulting archive before creating it.

> <b>Streaming a large file</b>
Efficient way to read a single very large binary file in python

> <b>Streaming multiple files in a zip</b>
The easiest is to use the Django or Flask built-in streaming feature


# Maintainer
Santiago Debus <a href="http://santiagodebus.com/" target="_blank">(@santiagodebus.com)</a><br>

<i>Santiago's open-source projects are supported by his Patreon. If you found this project helpful, any monetary contributions to the Patreon are appreciated and will be put to good creative use.</i>

# License
This library was created by Buzon.io and is released under the MIT. Copyright 2020 Grow HQ, Inc.
