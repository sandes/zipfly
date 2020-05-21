import zipfly
import os


paths = [ 
    {
        'fs': 'home/user/Videos/jupiter.mp4', 
        'n': 'movies/jupiter.mp4', 
    },             
]


zfly = zipfly.ZipFly( paths=paths )

# set a comment
# IMPORTANT: set a comment before than buffer_prediction_size()
zfly.set_comment("Isaac Newton 1234")







