import { useParams, Link } from "react-router-dom";
import { useAuth } from "@clerk/clerk-react";
import { ArrowLeft, Loader2, CheckCircle, XCircle, Clock } from "lucide-react";

/**
 * Job detail page showing job status and results.
 */
export function JobDetailPage() {
    const { jobId } = useParams<{ jobId: string }>();
    const { isSignedIn, isLoaded } = useAuth();

    if (!isLoaded) {
        return (
            <div className="flex items-center justify-center py-20">
                <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
            </div>
        );
    }

    if (!isSignedIn) {
        return (
            <div className="text-center py-20">
                <p>Please sign in to view job details.</p>
            </div>
        );
    }

    // TODO: Fetch job details with React Query
    // For now, show placeholder

    return (
        <div className="space-y-6">
            {/* Back Link */}
            <Link
                to="/dashboard"
                className="inline-flex items-center text-sm text-slate-600 hover:text-slate-900 dark:text-slate-300"
            >
                <ArrowLeft className="h-4 w-4 mr-1" />
                Back to Dashboard
            </Link>

            {/* Job Header */}
            <div className="rounded-xl border bg-white p-6 shadow-sm dark:bg-slate-800 dark:border-slate-700">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-2xl font-bold">Job Details</h1>
                        <p className="text-sm text-slate-500 mt-1 font-mono">{jobId}</p>
                    </div>
                    <StatusBadge status="pending" />
                </div>
            </div>

            {/* Job Info */}
            <div className="grid md:grid-cols-2 gap-6">
                {/* Input Section */}
                <section className="rounded-xl border bg-white p-6 shadow-sm dark:bg-slate-800 dark:border-slate-700">
                    <h2 className="text-lg font-semibold mb-4">Input</h2>
                    <div className="aspect-video bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center">
                        <p className="text-slate-400">Image preview will appear here</p>
                    </div>
                </section>

                {/* Output Section */}
                <section className="rounded-xl border bg-white p-6 shadow-sm dark:bg-slate-800 dark:border-slate-700">
                    <h2 className="text-lg font-semibold mb-4">Output</h2>
                    <div className="aspect-video bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center">
                        <p className="text-slate-400">Results will appear here</p>
                    </div>
                </section>
            </div>

            {/* Generated Code */}
            <section className="rounded-xl border bg-white p-6 shadow-sm dark:bg-slate-800 dark:border-slate-700">
                <h2 className="text-lg font-semibold mb-4">Generated Code</h2>
                <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto text-sm">
                    <code># Generated Python code will appear here</code>
                </pre>
            </section>
        </div>
    );
}

interface StatusBadgeProps {
    status: "pending" | "processing" | "completed" | "failed";
}

function StatusBadge({ status }: StatusBadgeProps) {
    const config = {
        pending: {
            icon: Clock,
            className: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300",
            label: "Pending",
        },
        processing: {
            icon: Loader2,
            className: "bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300",
            label: "Processing",
        },
        completed: {
            icon: CheckCircle,
            className: "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300",
            label: "Completed",
        },
        failed: {
            icon: XCircle,
            className: "bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300",
            label: "Failed",
        },
    };

    const { icon: Icon, className, label } = config[status];

    return (
        <span
            className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-sm font-medium ${className}`}
        >
            <Icon className={`h-4 w-4 ${status === "processing" ? "animate-spin" : ""}`} />
            {label}
        </span>
    );
}
