from minio import Minio


class MinioTool:
    def __init__(self, url, access_key, secret_key, bucket_name: str = "capivara"):
        self.bucket_name = bucket_name
        self.minio_client = Minio(
            f"{url}",
            access_key=access_key,
            secret_key=secret_key,
        )

    def upload_file(self, file_path: str, file_name: str, content_type: str = "application/octet-stream"):
        self.minio_client.fput_object(self.bucket_name, file_name, file_path, content_type=content_type)

    def download_file(self, file_name: str, file_path: str, content_type: str = "application/octet-stream"):
        self.minio_client.fget_object(self.bucket_name, file_name, file_path, content_type=content_type)

    def delete_file(self, file_name: str):
        self.minio_client.remove_object(self.bucket_name, file_name)

    def list_files(self, prefix: str = ""):
        return self.minio_client.list_objects(self.bucket_name, prefix=prefix)

    def get_file_url(self, file_name: str):
        return self.minio_client.presigned_get_object(self.bucket_name, file_name)
