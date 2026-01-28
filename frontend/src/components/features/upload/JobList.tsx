import { Link } from "react-router-dom";
import { Clock, CheckCircle, XCircle, Loader2, ImageIcon } from "lucide-react";
import { motion } from "framer-motion";

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
 * Empty state component.
 */
function EmptyState() {
    return (
        <div className="text-center py-12 px-4">
            <div className="mx-auto w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-4">
                <ImageIcon className="h-7 w-7 text-white/40" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">
                No jobs yet
            </h3>
            <p className="text-white/40 max-w-sm mx-auto">
                Upload an image to get started. AI will analyze it and generate Python code.
            </p>
        </div>
    );
}

/**
 * Dark-themed job list with status indicators.
 */
export function JobList() {
    const jobs = PLACEHOLDER_JOBS;
    const isLoading = false;

    if (isLoading) {
        return (
            <div className="space-y-3">
                {[1, 2, 3].map((i) => (
                    <div key={i} className="flex items-center justify-between p-4 rounded-xl bg-white/5 animate-pulse">
                        <div className="flex items-center gap-3">
                            <div className="h-5 w-5 bg-white/10 rounded-full" />
                            <div>
                                <div className="h-4 w-32 bg-white/10 rounded mb-2" />
                                <div className="h-3 w-24 bg-white/10 rounded" />
                            </div>
                        </div>
                        <div className="h-4 w-16 bg-white/10 rounded" />
                    </div>
                ))}
            </div>
        );
    }

    if (jobs.length === 0) {
        return <EmptyState />;
    }

    return (
        <div className="space-y-3">
            {jobs.map((job, index) => (
                <JobCard key={job.id} job={job} index={index} />
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

function JobCard({ job, index }: { job: Job; index: number }) {
    const statusConfig: Record<string, { icon: any; className: string; label: string }> = {
        pending: {
            icon: Clock,
            className: "text-yellow-400",
            label: "Pending",
        },
        processing: {
            icon: Loader2,
            className: "text-indigo-400 animate-spin",
            label: "Processing...",
        },
        completed: {
            icon: CheckCircle,
            className: "text-green-400",
            label: "Completed",
        },
        failed: {
            icon: XCircle,
            className: "text-red-400",
            label: "Failed",
        },
    };

    const { icon: StatusIcon, className, label } = statusConfig[job.status] || statusConfig.pending;

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
        >
            <Link
                to={`/jobs/${job.id}`}
                className="flex items-center justify-between p-4 rounded-xl border border-white/10 hover:border-white/20 hover:bg-white/5 transition-all duration-200 group"
            >
                <div className="flex items-center gap-3">
                    <StatusIcon className={`h-5 w-5 ${className}`} />
                    <div>
                        <p className="font-medium text-white group-hover:text-indigo-300 transition-colors">
                            {job.filename}
                        </p>
                        <p className="text-sm text-white/40">
                            {new Date(job.createdAt).toLocaleString()}
                        </p>
                    </div>
                </div>
                <span className={`text-sm font-medium ${className}`}>{label}</span>
            </Link>
        </motion.div>
    );
}
