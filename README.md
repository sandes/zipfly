# Buzon - ZipFly

ZipFly is a zip archive generator based on zipfile.py.
It was created by Buzon.io to generate a zipfly on-the-fly for download in a python application.


# Install
    pip install zipfly==1.1.4

# Basic usage

```python
    import zipfly
        
    paths = [ 
        {
            'filesystem': 'file1.mp4', # in your disk
            'name': 'file1.mp4', # in zip file generated
        },        
    ]

    # write a file in disk
    zf = zipfly.ZipFly(paths=paths)

    with open("test.zip", "wb") as f:
        for i in zf.generator():
            f.write(i)

```

## Examples

### django

```python
    
    from django.http import StreamingHttpResponse
    import zipfly

    paths = [
        {
            'filesystem': 'file1.mp4', # in your disk
            'name': 'file1.mp4', # in zip file generated
        },      
    ]

    zipfly = ZipFly(paths=paths)
    
    
    # IMPORTANT: get the buffer's size is optional
    for i in zipfly.generator():
        pass
    buffer_size = zipfly.buffer_size()


    # new generator to streaming
    z = zipfly.generator()

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