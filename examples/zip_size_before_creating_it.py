import zipfly
import os


# IMPORTANT:
# BufferPredictionSize using Linux

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

storesize = 0
for path in paths:

    # (jupiter.mp4 + mercury.mp4) size in bytes

    f = open(path['fs'], 'rb')
    storesize += os.fstat(f.fileno()).st_size


zfly = zipfly.ZipFly( paths=paths, storesize=storesize )


# zip size before creating it in bytes
try:
    prediction = zfly.buffer_prediction_size()
except zipfly.LargePredictionSize as e:
    print (e)
