# Buzon - ZipFly

ZipFly is a zip archive generator based on zipfile.py.
It was created by Buzon.io to generate a zipfly on-the-fly for download in a python application.


# Install
    pip install zipfly

# Basic usage

```python
    import zipfly
    
    # `filesystem` and `name` keys are required.
    paths = [ 
        {
            'filesystem': 'file.mp4', # From your disk
            'name': 'folder/file.mp4', # This is how it will appear in the zip file
        },        
    ]

    zfly = zipfly.ZipFly(paths=paths)

    # write a file in disk
    with open("test.zip", "wb") as f:
        for i in zfly.generator():
            f.write(i)

```

## Examples

### Get zipfile's size

```python

    import os
    import zipfly


    # `filesystem` and `name` keys are required.
    paths = [
        {
            'filesystem': 'file.mp4', # From your disk
            'name': 'folder/file.mp4', # This is how it will appear in the zip file
        },      
    ]

    files_size = 0
    for path in paths:
        f = open(path['filesystem'],'rb')
        files_size += os.fstat(f.fileno()).st_size 

    zfly = zipfly.ZipFly(paths=paths, store_size=files_size)

    # total file-zip's size
    print ( zfly.buffer_prediction_size() )


```


### django

```python
    
    from django.http import StreamingHttpResponse
    import zipfly

    # `filesystem` and `name` keys are required.
    paths = [
        {
            'filesystem': 'file.mp4', # From your disk
            'name': 'folder/file.mp4', # This is how it will appear in the zip file
        },      
    ]

    zfly = zipfly.ZipFly(mode='w', paths=paths)
    
    response = StreamingHttpResponse(
       zfly.generator(), content_type='application/octet-stream'
    )          

    return response 
```


# Requirements
Python > 3.5

# License
This library was created by Buzon.io and is released under the MIT. Copyright 2019 Grow HQ, Inc.