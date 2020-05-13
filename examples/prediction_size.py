import zipfly

"""
@attribute "storesize"
    https://github.com/BuzonIO/zipfly#create-a-zip-file-with-size-estimation
"""


ss = 92896201 # (file.mp4 + background.jpg) size in bytes

zfly = zipfly.ZipFly( paths=paths, storesize=ss )

print ( zfly.buffer_prediction_size() )
# 92896795