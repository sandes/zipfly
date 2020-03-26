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

    zfly = zipfly.ZipFly(paths=paths)
    

    # IMPORTANT: buffer size is not required
    buffer_size = zfly.buffer_size() # no multicore.


    # new generator to streaming
    z = zfly.generator()

    response = StreamingHttpResponse(
       z, content_type='application/octet-stream'
    )          
    
    response['Content-Length'] = buffer_size
    response['Transfer-Encoding'] = 'chunked'

    return response 
```


# Requirements
Python > 3.5

# License
This library was created by Buzon.io and is released under the MIT. Copyright 2019 Grow HQ, Inc.