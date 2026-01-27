"""Job database model."""

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class JobStatus(str, Enum):
    """Enum for job status values."""

    PENDING = "pending"
    PROCESSING = "processing"
    VALIDATING = "validating"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"


class JobModel(Base):
    """SQLAlchemy model for processing jobs."""

    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    file_id: Mapped[str] = mapped_column(String(36), index=True)
    status: Mapped[JobStatus] = mapped_column(
        String(20),
        default=JobStatus.PENDING,
    )
    task: Mapped[str] = mapped_column(String(50), default="analyze")
    prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    result_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    trace_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        """String representation of the job."""
        return f"<Job(id={self.id}, status={self.status})>"
