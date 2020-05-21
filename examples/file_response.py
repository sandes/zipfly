import zipfly

file_location = '/home/user/Documents/file-100-GB.csv'

# Efficient way to read a single very large binary file in python
go_to_streaming = zipfly.FileResponse( file_location )

print ( go_to_streaming )
# <generator object from_one_file at 0x7f85aad34a50>
 