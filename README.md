[![Build Status](https://img.shields.io/circleci/build/github/sandes/zipfly/master)](https://app.circleci.com/pipelines/github/sandes/zipfly)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/buzonio/zipfly)
[![Downloads](https://pepy.tech/badge/zipfly)](https://pepy.tech/project/zipfly)

# ZipFly

ZipFly is a zip archive generator based on zipfile.py.
It was created by <a href="https://santiagodebus.com" target="blank">Santiago Debus</a> to generate very large ZIP archives for immediate sending out to clients, or for writing large ZIP archives without memory inflation.

# Requirements
Python 3.6+ Added <a href="https://docs.python.org/3/library/zipfile.html#zipfile-objects" target="blank">support</a> for writing to unseekable streams.

# Install
    pip3 install zipfly

# Basic usage, compress on-the-fly during writes
Using this library will save you from having to write the Zip to disk. Some data will be buffered by the zipfile deflater, but memory inflation is going to be very constrained. Data will be written to destination by default at regular 32KB intervals.


`ZipFly` defaults attributes:<br>    
- <b>paths:</b> [ ] <br/>
- <b>mode:</b> (write) w <br/>
- <b>chunksize:</b> (bytes) 32768 <br/>
- <b>compression:</b> Stored <br/>
- <b>allowZip64:</b> True <br/>
- <b>compresslevel:</b> None <br/>
- <b>storesize:</b> (bytes) 0 <br/>
- <b>encode:</b> utf-8 <br/>

<br/>



`paths` <b>list of dictionaries:</b>

|                   |.                          
|----------------   |-------------------------------      
|**fs**             |Should be the path to a file on the filesystem            
|**n** *(Optional)* |Is the name which it will have within the archive <br> (by default, this will be the same as **fs**)

<br>

```python

    import zipfly

    paths = [
        {
            'fs': '/path/to/large/file'
        },
    ]

    zfly = zipfly.ZipFly(paths = paths)

    generator = zfly.generator()
    print (generator)
    # <generator object ZipFly.generator at 0x7f74d52bcc50>


    with open("large.zip", "wb") as f:
        for i in generator:
            f.write(i)

```


# Examples

> <b>Streaming multiple files in a zip with Django or Flask</b>
Send forth large files to clients with the most popular frameworks

> <b>Create paths</b>
Easy way to create the array `paths` from a parent folder.

> <b>Predict the size of the zip file before creating it</b>
Use the `BufferPredictionSize` to compute the correct size of the resulting archive before creating it.

> <b>Streaming a large file</b>
Efficient way to read a single very large binary file in python

> <b>Set a comment</b>
Your own comment in the zip file


# Maintainer
Santiago Debus <a href="http://santiagodebus.com/" target="_blank">(@santiagodebus.com)</a><br>


# License
This library was created by Buzon.io and is released under the MIT. Copyright 2021 Cardallot, Inc.
