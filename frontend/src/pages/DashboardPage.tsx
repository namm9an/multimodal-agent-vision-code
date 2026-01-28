import { useNavigate } from "react-router-dom";
import { useAuth } from "@clerk/clerk-react";
import { Loader2 } from "lucide-react";

import { FileUploader } from "../components/features/upload/FileUploader";
import { JobList } from "../components/features/upload/JobList";
import { FadeIn } from "@/components/ui/Animations";
import { SpotlightCard } from "@/components/ui/SpotlightCard";

/**
 * Dashboard page with dark theme matching the homepage.
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
                <Loader2 className="h-8 w-8 animate-spin text-white/60" />
            </div>
        );
    }

    return (
        <div className="space-y-8 max-w-4xl mx-auto">
            {/* Header */}
            <FadeIn>
                <div>
                    <h1 className="text-4xl font-bold text-white">Dashboard</h1>
                    <p className="text-white/50 mt-2">
                        Upload images and view your processing jobs.
                    </p>
                </div>
            </FadeIn>

            {/* Upload Section */}
            <FadeIn delay={0.1}>
                <SpotlightCard className="p-0">
                    <div className="p-6 border-b border-white/5">
                        <h2 className="text-xl font-semibold text-white">Upload Image</h2>
                    </div>
                    <div className="p-6">
                        <FileUploader />
                    </div>
                </SpotlightCard>
            </FadeIn>

            {/* Jobs Section */}
            <FadeIn delay={0.2}>
                <SpotlightCard className="p-0">
                    <div className="p-6 border-b border-white/5">
                        <h2 className="text-xl font-semibold text-white">Recent Jobs</h2>
                    </div>
                    <div className="p-6">
                        <JobList />
                    </div>
                </SpotlightCard>
            </FadeIn>
        </div>
    );
}
