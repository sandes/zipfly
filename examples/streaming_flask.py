# flask

from flask import Response
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

# flask streaming
response = Response(z, mimetype='application/zip',)
response.headers['Content-Disposition'] = 'attachment; filename=file.zip'

return response
