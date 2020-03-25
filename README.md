# Buzon - ZipFly

ZipFly is a zip archive generator based on zipfile.py.
It was created by Buzon.io to generate a zipfly on-the-fly for download in a python application.


# Install
    pip install zipfly

# Basic usage

```python
    import zipfly
        
    zipfly = zipfly.ZipFly()

    # set comment
    zipfly.set_comment("my comment")

    # get zip generator
    zipfly.generator()

```

## Examples

### django

```python
    
    from django.http import StreamingHttpResponse
    import zipfly

    paths = [
        {
            'filesystem': '/path/to/your/file1.mp4',
            'name': '/name/in/zip/file/file1.mp4', 
        },

        {
            'filesystem': '/path/to/your/file1.mp4',
            'name': '/name/in/zip/file/file1.mp4', 
        },        

    ]

    # paths is a list of maps
        
    zipfly = zipfly.ZipFly(paths=paths)
    z = zipfly.generator()


    response = StreamingHttpResponse(
       z, content_type='application/octet-stream'
    )          

    response['Transfer-Encoding'] = 'chunked'

    return response 
```


# Requirements
Python > 3.5

# License
This library was created by Buzon.io and is released under the MIT. Copyright 2019 Grow HQ, Inc.