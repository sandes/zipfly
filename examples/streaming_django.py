# django

from django.http import StreamingHttpResponse
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

storesize = 92896201 # (jupiter.mp4 + mercury.mp4) size in bytes

"""
# You can get the file size in python with:

storesize = 0
for path in paths:

    # (jupiter.mp4 + mercury.mp4) size in bytes

    f = open(path['fs'], 'rb')
    storesize += os.fstat(f.fileno()).st_size

"""


# constructor
zfly = zipfly.ZipFly( mode='w', paths=paths, storesize=storesize )

# z is a new generator 
# (<generator object generator at 0x7f85aad34a50>)
z = zfly.generator()

# django streaming
response = StreamingHttpResponse(
    z,
    content_type='application/octet-stream',
)          

# zip size before creating it
content_length = zfly.buffer_prediction_size()

response['Content-Length'] =  content_length
response['Content-Disposition'] = 'attachment; filename=file.zip'    

return response 