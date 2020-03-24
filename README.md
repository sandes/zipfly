# Buzon - ZipFly

ZipFly is a zip archive generator based on zipfile.py.
It was created by Buzon.io to generate a zipfly on-the-fly for download in a python application.


# Install
    pip install zipfly

# Usage

```python
    from zipfile import ZIP_DEFLATED
    import zipfly

    filelist = [
        "/to/path/large-file1.mp4",
        "/to/path/large-file2.mp4",
    ]

    z = zipfly.ZipFile( mode='w',
                        compression=ZIP_DEFLATED, 
                        allowZip64=True)
    for f in filelist:
        # get filename and write
        filename = os.path.basename(os.path.normpath(f))
        z.write(f, filename)
```

# Requirements
Python > 2.7

# License
This library was created by Buzon.io and is released under the MIT. Copyright 2019 Grow HQ, Inc.