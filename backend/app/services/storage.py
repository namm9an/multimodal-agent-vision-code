"""MinIO storage service for file operations."""

from io import BytesIO

import structlog
from minio import Minio
from minio.error import S3Error

from app.config import get_settings

logger = structlog.get_logger()


class StorageService:
    """Service for interacting with MinIO object storage."""

    def __init__(self) -> None:
        """Initialize the storage service with MinIO client."""
        settings = get_settings()

        self.client = Minio(
            endpoint=settings.minio_endpoint,
            access_key=settings.minio_root_user,
            secret_key=settings.minio_root_password,
            secure=settings.minio_use_ssl,
        )
        self.bucket = settings.minio_bucket

        # Ensure bucket exists
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self) -> None:
        """Create the bucket if it doesn't exist."""
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
                logger.info("Created bucket", bucket=self.bucket)
        except S3Error as e:
            logger.error("Failed to create bucket", error=str(e))

    async def upload_file(
        self,
        path: str,
        content: bytes,
        content_type: str = "application/octet-stream",
    ) -> str:
        """Upload a file to MinIO.

        Args:
            path: The path/key for the file in the bucket.
            content: The file content as bytes.
            content_type: The MIME type of the file.

        Returns:
            The storage path of the uploaded file.

        Raises:
            S3Error: If upload fails.
        """
        try:
            self.client.put_object(
                bucket_name=self.bucket,
                object_name=path,
                data=BytesIO(content),
                length=len(content),
                content_type=content_type,
            )
            logger.info("File uploaded", path=path, size=len(content))
            return path
        except S3Error as e:
            logger.error("Upload failed", path=path, error=str(e))
            raise

    async def download_file(self, path: str) -> bytes:
        """Download a file from MinIO.

        Args:
            path: The path/key of the file in the bucket.

        Returns:
            The file content as bytes.

        Raises:
            S3Error: If download fails.
        """
        try:
            response = self.client.get_object(self.bucket, path)
            content = response.read()
            response.close()
            response.release_conn()
            return content
        except S3Error as e:
            logger.error("Download failed", path=path, error=str(e))
            raise

    async def delete_file(self, path: str) -> None:
        """Delete a file from MinIO.

        Args:
            path: The path/key of the file to delete.

        Raises:
            S3Error: If deletion fails.
        """
        try:
            self.client.remove_object(self.bucket, path)
            logger.info("File deleted", path=path)
        except S3Error as e:
            logger.error("Deletion failed", path=path, error=str(e))
            raise

    def get_presigned_url(self, path: str, expires_in: int = 3600) -> str:
        """Generate a presigned URL for file access.

        Args:
            path: The path/key of the file.
            expires_in: URL expiration time in seconds.

        Returns:
            Presigned URL for the file.
        """
        from datetime import timedelta

        return self.client.presigned_get_object(
            bucket_name=self.bucket,
            object_name=path,
            expires=timedelta(seconds=expires_in),
        )


# Singleton instance
_storage_service: StorageService | None = None


def get_storage_service() -> StorageService:
    """Get the storage service singleton.

    Returns:
        StorageService instance.
    """
    global _storage_service
    if _storage_service is None:
        _storage_service = StorageService()
    return _storage_service
