"""File upload and management endpoints."""

import uuid
from datetime import datetime, timezone

import structlog
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import UserInfo, verify_clerk_token
from app.core.database import get_db
from app.models.file import FileModel
from app.services.storage import StorageService, get_storage_service

router = APIRouter()
logger = structlog.get_logger()

# Allowed image types - NO PDFs
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
ALLOWED_MIMETYPES = {
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/webp",
}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class FileUploadResponse(BaseModel):
    """Response after successful file upload."""

    file_id: str
    filename: str
    content_type: str
    size: int
    created_at: str
    storage_path: str


class FileInfo(BaseModel):
    """File information response."""

    file_id: str
    filename: str
    content_type: str
    size: int
    created_at: str
    user_id: str


def validate_image_file(file: UploadFile) -> None:
    """Validate that the uploaded file is an allowed image type.

    Args:
        file: The uploaded file to validate.

    Raises:
        HTTPException: If file type is not allowed.
    """
    # Check filename extension
    if file.filename:
        extension = file.filename.rsplit(".", 1)[-1].lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Invalid file type '.{extension}'. "
                    f"Allowed types: {', '.join(ALLOWED_EXTENSIONS)}. "
                    "PDF support coming in Phase 2."
                ),
            )

    # Check MIME type
    if file.content_type and file.content_type not in ALLOWED_MIMETYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Invalid content type '{file.content_type}'. "
                "Only images are supported (PNG, JPG, GIF, WebP)."
            ),
        )


@router.post(
    "/upload",
    response_model=FileUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload an image file",
    description="Upload an image file for processing. Only PNG, JPG, GIF, and WebP are supported.",
)
async def upload_file(
    file: UploadFile = File(..., description="Image file to upload"),
    user: UserInfo = Depends(verify_clerk_token),
    db: AsyncSession = Depends(get_db),
    storage: StorageService = Depends(get_storage_service),
) -> FileUploadResponse:
    """Upload an image file for processing.

    Args:
        file: The image file to upload.
        user: Current authenticated user.
        db: Database session.
        storage: Storage service for file operations.

    Returns:
        FileUploadResponse: Information about the uploaded file.

    Raises:
        HTTPException: If file validation fails or upload fails.
    """
    # Validate file type (images only!)
    validate_image_file(file)

    # Read file content
    content = await file.read()

    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024 * 1024)} MB.",
        )

    # Generate unique file ID and storage path
    file_id = str(uuid.uuid4())
    extension = file.filename.rsplit(".", 1)[-1].lower() if file.filename else "png"
    storage_path = f"uploads/{user.user_id}/{file_id}.{extension}"

    try:
        # Upload to MinIO
        await storage.upload_file(
            path=storage_path,
            content=content,
            content_type=file.content_type or "image/png",
        )

        # Create database record
        file_record = FileModel(
            id=file_id,
            user_id=user.user_id,
            filename=file.filename or f"{file_id}.{extension}",
            content_type=file.content_type or "image/png",
            size=len(content),
            storage_path=storage_path,
        )

        db.add(file_record)
        await db.commit()
        await db.refresh(file_record)

        logger.info(
            "File uploaded successfully",
            file_id=file_id,
            user_id=user.user_id,
            size=len(content),
        )

        return FileUploadResponse(
            file_id=file_id,
            filename=file.filename or f"{file_id}.{extension}",
            content_type=file.content_type or "image/png",
            size=len(content),
            created_at=datetime.now(timezone.utc).isoformat(),
            storage_path=storage_path,
        )

    except Exception as e:
        logger.error("File upload failed", error=str(e), file_id=file_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload file. Please try again.",
        )


@router.get(
    "/{file_id}",
    response_model=FileInfo,
    summary="Get file information",
    description="Get information about a previously uploaded file.",
)
async def get_file_info(
    file_id: str,
    user: UserInfo = Depends(verify_clerk_token),
    db: AsyncSession = Depends(get_db),
) -> FileInfo:
    """Get information about an uploaded file.

    Args:
        file_id: The ID of the file to retrieve.
        user: Current authenticated user.
        db: Database session.

    Returns:
        FileInfo: Information about the file.

    Raises:
        HTTPException: If file not found or access denied.
    """
    from sqlalchemy import select

    result = await db.execute(
        select(FileModel).where(
            FileModel.id == file_id,
            FileModel.user_id == user.user_id,
        )
    )
    file_record = result.scalar_one_or_none()

    if not file_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    return FileInfo(
        file_id=file_record.id,
        filename=file_record.filename,
        content_type=file_record.content_type,
        size=file_record.size,
        created_at=file_record.created_at.isoformat(),
        user_id=file_record.user_id,
    )
