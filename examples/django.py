from django.http import StreamingHttpResponse
import zipfly


"""

@attribute "paths"
    https://github.com/BuzonIO/zipfly#basic-usage-compress-on-the-fly-during-writes

@attribute "storesize"
https://github.com/BuzonIO/zipfly#create-a-zip-file-with-size-estimation

"""

zfly = zipfly.ZipFly( mode='w', paths=paths, storesize=ss )

z = zfly.generator()
# z (<generator object generator at 0x7f85aad34a50>)

response = StreamingHttpResponse(
    z,
    content_type='application/octet-stream',
)          

response['Content-Length'] = zfly.buffer_prediction_size() 
response['Content-Disposition'] = 'attachment; filename=file.zip'    

return response 