"""Job management endpoints."""

import uuid
from datetime import datetime, timezone

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import UserInfo, verify_clerk_token
from app.core.database import get_db
from app.models.job import JobModel, JobStatus

router = APIRouter()
logger = structlog.get_logger()


class JobCreate(BaseModel):
    """Request model for creating a new job."""

    file_id: str
    task: str = "analyze"
    prompt: str | None = None


class JobResponse(BaseModel):
    """Response model for job information."""

    job_id: str
    user_id: str
    file_id: str
    status: str
    task: str
    prompt: str | None
    result_url: str | None
    error_message: str | None
    created_at: str
    updated_at: str


class JobListResponse(BaseModel):
    """Response model for listing jobs."""

    jobs: list[JobResponse]
    total: int


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new job",
    description="Create a new job to process an uploaded file.",
)
async def create_job(
    job_data: JobCreate,
    user: UserInfo = Depends(verify_clerk_token),
    db: AsyncSession = Depends(get_db),
) -> JobResponse:
    """Create a new processing job.

    Args:
        job_data: Job creation data.
        user: Current authenticated user.
        db: Database session.

    Returns:
        JobResponse: Created job information.

    Raises:
        HTTPException: If file not found or job creation fails.
    """
    from app.models.file import FileModel

    # Verify file exists and belongs to user
    result = await db.execute(
        select(FileModel).where(
            FileModel.id == job_data.file_id,
            FileModel.user_id == user.user_id,
        )
    )
    file_record = result.scalar_one_or_none()

    if not file_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found. Please upload a file first.",
        )

    # Create job
    job_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    job = JobModel(
        id=job_id,
        user_id=user.user_id,
        file_id=job_data.file_id,
        status=JobStatus.PENDING,
        task=job_data.task,
        prompt=job_data.prompt,
        created_at=now,
        updated_at=now,
    )

    db.add(job)
    await db.commit()
    await db.refresh(job)

    logger.info(
        "Job created",
        job_id=job_id,
        user_id=user.user_id,
        file_id=job_data.file_id,
        task=job_data.task,
    )

    # TODO: Queue job for processing with Celery
    # from app.workers.tasks import process_job
    # process_job.delay(job_id)

    return JobResponse(
        job_id=job.id,
        user_id=job.user_id,
        file_id=job.file_id,
        status=job.status.value,
        task=job.task,
        prompt=job.prompt,
        result_url=job.result_url,
        error_message=job.error_message,
        created_at=job.created_at.isoformat(),
        updated_at=job.updated_at.isoformat(),
    )


@router.get(
    "",
    response_model=JobListResponse,
    summary="List all jobs",
    description="List all jobs for the current user.",
)
async def list_jobs(
    user: UserInfo = Depends(verify_clerk_token),
    db: AsyncSession = Depends(get_db),
    limit: int = 20,
    offset: int = 0,
) -> JobListResponse:
    """List all jobs for the current user.

    Args:
        user: Current authenticated user.
        db: Database session.
        limit: Maximum number of jobs to return.
        offset: Number of jobs to skip.

    Returns:
        JobListResponse: List of jobs.
    """
    from sqlalchemy import func

    # Get total count
    count_result = await db.execute(
        select(func.count(JobModel.id)).where(JobModel.user_id == user.user_id)
    )
    total = count_result.scalar() or 0

    # Get jobs
    result = await db.execute(
        select(JobModel)
        .where(JobModel.user_id == user.user_id)
        .order_by(JobModel.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    jobs = result.scalars().all()

    return JobListResponse(
        jobs=[
            JobResponse(
                job_id=job.id,
                user_id=job.user_id,
                file_id=job.file_id,
                status=job.status.value,
                task=job.task,
                prompt=job.prompt,
                result_url=job.result_url,
                error_message=job.error_message,
                created_at=job.created_at.isoformat(),
                updated_at=job.updated_at.isoformat(),
            )
            for job in jobs
        ],
        total=total,
    )


@router.get(
    "/{job_id}",
    response_model=JobResponse,
    summary="Get job status",
    description="Get the status and details of a specific job.",
)
async def get_job(
    job_id: str,
    user: UserInfo = Depends(verify_clerk_token),
    db: AsyncSession = Depends(get_db),
) -> JobResponse:
    """Get a specific job's status and details.

    Uses Redis caching for improved performance on frequent polling.
    Cache TTL varies based on job status (shorter for active jobs).

    Args:
        job_id: The ID of the job to retrieve.
        user: Current authenticated user.
        db: Database session.

    Returns:
        JobResponse: Job information.

    Raises:
        HTTPException: If job not found.
    """
    from app.core.cache import cache_manager, CacheManager

    # Try cache first (Phase 4)
    cache_key = CacheManager.generate_key("job", job_id)
    cached = await cache_manager.get(cache_key)

    if cached and cached.get("user_id") == user.user_id:
        logger.debug("Job cache hit", job_id=job_id)
        return JobResponse(**cached)

    # Cache miss - fetch from database
    result = await db.execute(
        select(JobModel).where(
            JobModel.id == job_id,
            JobModel.user_id == user.user_id,
        )
    )
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    response_data = {
        "job_id": job.id,
        "user_id": job.user_id,
        "file_id": job.file_id,
        "status": job.status.value,
        "task": job.task,
        "prompt": job.prompt,
        "result_url": job.result_url,
        "error_message": job.error_message,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat(),
    }

    # Cache with TTL based on status (Phase 4)
    # Active jobs: short TTL (10s) for fresher data
    # Completed/Failed: longer TTL (1 hour)
    if job.status in (JobStatus.COMPLETED, JobStatus.FAILED):
        ttl = 3600  # 1 hour
    else:
        ttl = 10  # 10 seconds for active jobs

    await cache_manager.set(cache_key, response_data, ttl=ttl)
    logger.debug("Job cached", job_id=job_id, ttl=ttl)

    return JobResponse(**response_data)

