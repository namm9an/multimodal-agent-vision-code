"""Celery tasks for background job processing.

This module contains the Celery tasks that run the LangGraph agent pipeline.
"""

import asyncio
from datetime import datetime
from typing import Any

import structlog
from sqlalchemy import select

from app.agents.graph import run_agent
from app.config import get_settings
from app.core.database import async_session_maker
from app.models.file import File
from app.models.job import Job, JobStatus
from app.services.storage import StorageService
from app.workers.celery_app import celery_app

logger = structlog.get_logger()


async def _process_job_async(job_id: str) -> dict[str, Any]:
    """Async implementation of job processing.

    This function handles:
    1. Loading job and file from database
    2. Downloading file from MinIO
    3. Running the LangGraph agent
    4. Updating job status with results

    Args:
        job_id: The ID of the job to process.

    Returns:
        Dict with job result information.
    """
    _ = get_settings()  # Keep for future use

    async with async_session_maker() as session:
        # 1. Load job from database
        result = await session.execute(select(Job).where(Job.id == job_id))
        job = result.scalar_one_or_none()

        if not job:
            logger.error("Job not found", job_id=job_id)
            return {"job_id": job_id, "status": "error", "error": "Job not found"}

        # Update status to processing
        job.status = JobStatus.PROCESSING
        job.updated_at = datetime.utcnow()
        await session.commit()

        logger.info("Job status updated to processing", job_id=job_id)

        # 2. Load file from database
        result = await session.execute(select(File).where(File.id == job.file_id))
        file = result.scalar_one_or_none()

        if not file:
            logger.error("File not found", job_id=job_id, file_id=job.file_id)
            job.status = JobStatus.FAILED
            job.error_message = "File not found"
            job.updated_at = datetime.utcnow()
            await session.commit()
            return {
                "job_id": job_id,
                "status": "error",
                "error": "File not found",
            }

        # 3. Download file from MinIO
        try:
            storage = StorageService()
            image_data = await storage.download(file.storage_path)
            logger.info(
                "File downloaded from storage",
                job_id=job_id,
                file_size=len(image_data),
            )
        except Exception as e:
            logger.error("Failed to download file", job_id=job_id, error=str(e))
            job.status = JobStatus.FAILED
            job.error_message = f"Failed to download file: {str(e)}"
            job.updated_at = datetime.utcnow()
            await session.commit()
            return {
                "job_id": job_id,
                "status": "error",
                "error": str(e),
            }

        # 4. Run the LangGraph agent
        try:
            final_state = await run_agent(
                job_id=job_id,
                user_id=job.user_id,
                image_path=file.storage_path,
                image_data=image_data,
                image_mime_type=file.content_type,
                user_prompt=job.prompt or "Analyze this image and generate useful Python code.",
            )

            # Check for errors
            if final_state.get("error"):
                logger.error(
                    "Agent returned error",
                    job_id=job_id,
                    error=final_state["error"],
                )
                job.status = JobStatus.FAILED
                job.error_message = final_state["error"]
            else:
                # Success - save results
                job.status = JobStatus.COMPLETED

                # Store generated code in the job result
                # In Phase 3, we'll also store the execution result
                generated_code = final_state.get("generated_code", "")

                # Save result to MinIO if we have code
                if generated_code:
                    result_path = f"results/{job_id}/generated_code.py"
                    await storage.upload(
                        result_path,
                        generated_code.encode("utf-8"),
                        "text/x-python",
                    )
                    job.result_url = result_path

                logger.info(
                    "Agent completed successfully",
                    job_id=job_id,
                    has_code=bool(generated_code),
                )

            job.updated_at = datetime.utcnow()
            await session.commit()

            return {
                "job_id": job_id,
                "status": job.status.value,
                "image_analysis": final_state.get("image_analysis"),
                "reasoning": final_state.get("reasoning"),
                "generated_code": final_state.get("generated_code"),
                "error": final_state.get("error"),
            }

        except Exception as e:
            logger.error("Agent execution failed", job_id=job_id, error=str(e))
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.updated_at = datetime.utcnow()
            await session.commit()
            return {
                "job_id": job_id,
                "status": "error",
                "error": str(e),
            }


@celery_app.task(bind=True, name="process_job")
def process_job(self, job_id: str) -> dict:
    """Process a job asynchronously using the LangGraph agent.

    This task orchestrates:
    - Vision analysis with Qwen
    - Reasoning with Mistral
    - Code generation with DeepSeek

    Args:
        job_id: The ID of the job to process.

    Returns:
        Dict with job result information.
    """
    logger.info("Starting job processing", job_id=job_id)

    # Run the async processing function
    result = asyncio.run(_process_job_async(job_id))

    logger.info(
        "Job processing complete",
        job_id=job_id,
        status=result.get("status"),
    )

    return result


@celery_app.task(name="health_check")
def health_check() -> str:
    """Simple health check task to verify Celery is working.

    Returns:
        Success message.
    """
    return "Celery worker is healthy"
