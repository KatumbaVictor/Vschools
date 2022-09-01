from storages.backends.s3boto3 import S3BotoStorage

class MediaStorage(S3BotoStorage):
    location = 'media'
    file_overwrite = False