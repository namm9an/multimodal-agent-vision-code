import { Outlet, Link } from "react-router-dom";
import {
    SignedIn,
    SignedOut,
    SignInButton,
    SignUpButton,
    UserButton,
} from "@clerk/clerk-react";

/**
 * Main layout component with navigation header.
 */
export function Layout() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
            {/* Navigation Header */}
            <header className="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-sm dark:bg-slate-900/80">
                <div className="container mx-auto flex h-16 items-center justify-between px-4">
                    {/* Logo */}
                    <Link to="/" className="flex items-center space-x-2">
                        <span className="text-2xl">🤖</span>
                        <span className="font-bold text-xl gradient-text">
                            Multimodal Agent
                        </span>
                    </Link>

                    {/* Navigation */}
                    <nav className="flex items-center space-x-6">
                        <SignedIn>
                            <Link
                                to="/dashboard"
                                className="text-sm font-medium text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white transition-colors"
                            >
                                Dashboard
                            </Link>
                            <UserButton
                                afterSignOutUrl="/"
                                appearance={{
                                    elements: {
                                        avatarBox: "h-9 w-9",
                                    },
                                }}
                            />
                        </SignedIn>

                        <SignedOut>
                            <SignInButton mode="modal">
                                <button className="text-sm font-medium text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white transition-colors">
                                    Sign In
                                </button>
                            </SignInButton>
                            <SignUpButton mode="modal">
                                <button className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 transition-colors">
                                    Get Started
                                </button>
                            </SignUpButton>
                        </SignedOut>
                    </nav>
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-4 py-8">
                <Outlet />
            </main>

            {/* Footer */}
            <footer className="border-t bg-white dark:bg-slate-900">
                <div className="container mx-auto px-4 py-6 text-center text-sm text-slate-500">
                    <p>© 2026 Multimodal AI Agent. All rights reserved.</p>
                </div>
            </footer>
        </div>
    );
}
