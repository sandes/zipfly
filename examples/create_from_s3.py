import zipfly


AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_S3_ENDPOINT_WITH_PROTOCOL=None
BUCKET=""


paths = [
    {
        'fs': "s3://bucket_name/path/file.txt"
    },
]

zfly = zipfly.ZipFly(
    paths= paths,
    s3_endpoint_url=AWS_S3_ENDPOINT_WITH_PROTOCOL,
    s3_access_key_id=AWS_ACCESS_KEY_ID,
    s3_secret_access_key=AWS_SECRET_ACCESS_KEY,
    s3_bucket=BUCKET,
)

generator = zfly.generator()

with open("large.zip", "wb") as f:
    for i in generator:
        f.write(i)
