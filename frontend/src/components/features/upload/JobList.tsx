import { Link } from "react-router-dom";
import { Clock, CheckCircle, XCircle, Loader2, ImageIcon } from "lucide-react";

// Placeholder job data - will be replaced with React Query
const PLACEHOLDER_JOBS = [
    {
        id: "job-001",
        filename: "chart.png",
        status: "completed",
        createdAt: "2026-01-21T10:30:00Z",
    },
    {
        id: "job-002",
        filename: "diagram.jpg",
        status: "processing",
        createdAt: "2026-01-21T11:00:00Z",
    },
    {
        id: "job-003",
        filename: "screenshot.png",
        status: "pending",
        createdAt: "2026-01-21T11:30:00Z",
    },
];

/**
 * Skeleton component for loading states (Phase 4).
 */
function JobSkeleton() {
    return (
        <div className="flex items-center justify-between p-4 rounded-lg border animate-pulse">
            <div className="flex items-center gap-3">
                <div className="h-5 w-5 bg-slate-200 dark:bg-slate-700 rounded-full" />
                <div>
                    <div className="h-4 w-32 bg-slate-200 dark:bg-slate-700 rounded mb-2" />
                    <div className="h-3 w-24 bg-slate-200 dark:bg-slate-700 rounded" />
                </div>
            </div>
            <div className="h-4 w-16 bg-slate-200 dark:bg-slate-700 rounded" />
        </div>
    );
}

/**
 * Empty state component with illustration (Phase 4).
 */
function EmptyState() {
    return (
        <div className="text-center py-12 px-4">
            <div className="mx-auto w-16 h-16 rounded-full bg-gradient-to-br from-blue-100 to-indigo-100 dark:from-blue-900/30 dark:to-indigo-900/30 flex items-center justify-center mb-4">
                <ImageIcon className="h-8 w-8 text-blue-500 dark:text-blue-400" />
            </div>
            <h3 className="text-lg font-semibold text-slate-800 dark:text-slate-200 mb-2">
                No jobs yet
            </h3>
            <p className="text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
                Upload an image to get started. Our AI will analyze it and generate Python code for you.
            </p>
        </div>
    );
}

/**
 * List of recent jobs with status indicators.
 * Phase 4: Enhanced with skeleton loading and empty states.
 */
export function JobList() {
    // TODO: Replace with React Query hook
    const jobs = PLACEHOLDER_JOBS;
    const isLoading = false;

    if (isLoading) {
        return (
            <div className="space-y-3">
                <JobSkeleton />
                <JobSkeleton />
                <JobSkeleton />
            </div>
        );
    }

    if (jobs.length === 0) {
        return <EmptyState />;
    }

    return (
        <div className="space-y-3">
            {jobs.map((job) => (
                <JobCard key={job.id} job={job} />
            ))}
        </div>
    );
}

interface Job {
    id: string;
    filename: string;
    status: string;
    createdAt: string;
}

function JobCard({ job }: { job: Job }) {
    const statusConfig: Record<string, { icon: any; className: string; label: string }> = {
        pending: {
            icon: Clock,
            className: "text-yellow-500",
            label: "Pending",
        },
        processing: {
            icon: Loader2,
            className: "text-blue-500 animate-spin",
            label: "Processing...",
        },
        completed: {
            icon: CheckCircle,
            className: "text-green-500",
            label: "Completed",
        },
        failed: {
            icon: XCircle,
            className: "text-red-500",
            label: "Failed",
        },
    };

    const { icon: StatusIcon, className, label } = statusConfig[job.status] || statusConfig.pending;

    return (
        <Link
            to={`/jobs/${job.id}`}
            className="flex items-center justify-between p-4 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:border-blue-300 dark:hover:border-blue-700 transition-all duration-200 group"
        >
            <div className="flex items-center gap-3">
                <StatusIcon className={`h-5 w-5 ${className}`} />
                <div>
                    <p className="font-medium text-slate-800 dark:text-slate-200 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                        {job.filename}
                    </p>
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                        {new Date(job.createdAt).toLocaleString()}
                    </p>
                </div>
            </div>
            <span className={`text-sm font-medium ${className}`}>{label}</span>
        </Link>
    );
}

