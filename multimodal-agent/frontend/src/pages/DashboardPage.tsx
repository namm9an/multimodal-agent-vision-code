import { useNavigate } from "react-router-dom";
import { useAuth } from "@clerk/clerk-react";
import { Loader2 } from "lucide-react";

import { FileUploader } from "../components/features/upload/FileUploader";
import { JobList } from "../components/features/upload/JobList";

/**
 * Main dashboard page for authenticated users.
 */
export function DashboardPage() {
    const { isSignedIn, isLoaded } = useAuth();
    const navigate = useNavigate();

    // Redirect to home if not signed in
    if (isLoaded && !isSignedIn) {
        navigate("/");
        return null;
    }

    if (!isLoaded) {
        return (
            <div className="flex items-center justify-center py-20">
                <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
            </div>
        );
    }

    return (
        <div className="space-y-8">
            {/* Header */}
            <div>
                <h1 className="text-3xl font-bold">Dashboard</h1>
                <p className="text-slate-600 dark:text-slate-300 mt-2">
                    Upload images and view your processing jobs.
                </p>
            </div>

            {/* Upload Section */}
            <section className="rounded-xl border bg-white p-6 shadow-sm dark:bg-slate-800 dark:border-slate-700">
                <h2 className="text-xl font-semibold mb-4">Upload Image</h2>
                <FileUploader />
            </section>

            {/* Jobs Section */}
            <section className="rounded-xl border bg-white p-6 shadow-sm dark:bg-slate-800 dark:border-slate-700">
                <h2 className="text-xl font-semibold mb-4">Recent Jobs</h2>
                <JobList />
            </section>
        </div>
    );
}
