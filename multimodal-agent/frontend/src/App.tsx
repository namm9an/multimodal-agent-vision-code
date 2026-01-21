import { Routes, Route } from "react-router-dom";
import {
    SignedIn,
    SignedOut,
    SignInButton,
    SignUpButton,
    UserButton,
} from "@clerk/clerk-react";

import { Layout } from "./components/common/Layout";
import { HomePage } from "./pages/HomePage";
import { DashboardPage } from "./pages/DashboardPage";
import { JobDetailPage } from "./pages/JobDetailPage";

/**
 * Main application component with routing.
 */
export default function App() {
    return (
        <Routes>
            <Route path="/" element={<Layout />}>
                {/* Public home page */}
                <Route index element={<HomePage />} />

                {/* Protected routes */}
                <Route path="dashboard" element={<DashboardPage />} />
                <Route path="jobs/:jobId" element={<JobDetailPage />} />
            </Route>
        </Routes>
    );
}
