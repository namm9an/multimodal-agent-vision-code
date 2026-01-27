import { Link } from "react-router-dom";
import { Clock, CheckCircle, XCircle, Loader2 } from "lucide-react";

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
 * List of recent jobs with status indicators.
 */
export function JobList() {
    // TODO: Replace with React Query hook
    const jobs = PLACEHOLDER_JOBS;
    const isLoading = false;

    if (isLoading) {
        return (
            <div className="flex items-center justify-center py-8">
                <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
            </div>
        );
    }

    if (jobs.length === 0) {
        return (
            <div className="text-center py-8">
                <p className="text-slate-500">No jobs yet. Upload an image to get started!</p>
            </div>
        );
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
    const statusConfig: Record<string, { icon: any; className: string }> = {
        pending: {
            icon: Clock,
            className: "text-yellow-500",
        },
        processing: {
            icon: Loader2,
            className: "text-blue-500 animate-spin",
        },
        completed: {
            icon: CheckCircle,
            className: "text-green-500",
        },
        failed: {
            icon: XCircle,
            className: "text-red-500",
        },
    };

    const { icon: StatusIcon, className } = statusConfig[job.status] || statusConfig.pending;

    return (
        <Link
            to={`/jobs/${job.id}`}
            className="flex items-center justify-between p-4 rounded-lg border hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
        >
            <div className="flex items-center gap-3">
                <StatusIcon className={`h-5 w-5 ${className}`} />
                <div>
                    <p className="font-medium">{job.filename}</p>
                    <p className="text-sm text-slate-500">
                        {new Date(job.createdAt).toLocaleString()}
                    </p>
                </div>
            </div>
            <span className="text-sm text-slate-400 capitalize">{job.status}</span>
        </Link>
    );
}
