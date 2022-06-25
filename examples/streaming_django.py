# django

from django.http import StreamingHttpResponse
import zipfly


paths = [
    {
        'fs': 'home/user/Videos/jupiter.mp4',
        'n': 'movies/jupiter.mp4',
    },
]

# constructor
zfly = zipfly.ZipFly( paths=paths )

# z is a new generator
z = zfly.generator()

# django streaming
response = StreamingHttpResponse(z, content_type='application/octet-stream')
response['Content-Disposition'] = 'attachment; filename=file.zip'

return response
