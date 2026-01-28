import { Outlet, Link } from "react-router-dom";
import {
    SignedIn,
    SignedOut,
    SignInButton,
    SignUpButton,
    UserButton,
} from "@clerk/clerk-react";
import { Sparkles } from "lucide-react";

/**
 * Premium layout with glassmorphism navigation.
 */
export function Layout() {
    return (
        <div className="min-h-screen animated-gradient dark">
            {/* Navigation Header */}
            <header className="sticky top-0 z-50 w-full glass border-b border-white/10">
                <div className="container mx-auto flex h-16 items-center justify-between px-4">
                    {/* Logo */}
                    <Link to="/" className="flex items-center space-x-3 group">
                        <div className="p-2 rounded-lg bg-gradient-to-br from-purple-600 to-pink-600 group-hover:glow-purple transition-all">
                            <Sparkles className="h-5 w-5 text-white" />
                        </div>
                        <span className="font-bold text-xl gradient-text">
                            Multimodal Agent
                        </span>
                    </Link>

                    {/* Navigation */}
                    <nav className="flex items-center space-x-4">
                        <SignedIn>
                            <Link
                                to="/dashboard"
                                className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white transition-colors"
                            >
                                Dashboard
                            </Link>
                            <UserButton
                                afterSignOutUrl="/"
                                appearance={{
                                    elements: {
                                        avatarBox: "h-9 w-9 ring-2 ring-purple-500/50",
                                    },
                                }}
                            />
                        </SignedIn>

                        <SignedOut>
                            <SignInButton mode="modal">
                                <button className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white transition-colors">
                                    Sign In
                                </button>
                            </SignInButton>
                            <SignUpButton mode="modal">
                                <button className="px-5 py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg hover:opacity-90 transition-all btn-glow">
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
            <footer className="glass border-t border-white/10 mt-16">
                <div className="container mx-auto px-4 py-8">
                    <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                        <div className="flex items-center space-x-2">
                            <Sparkles className="h-4 w-4 text-purple-400" />
                            <span className="text-sm text-slate-400">
                                Powered by Qwen, Llama & DeepSeek
                            </span>
                        </div>
                        <p className="text-sm text-slate-500">
                            © 2026 Multimodal AI Agent. All rights reserved.
                        </p>
                    </div>
                </div>
            </footer>
        </div>
    );
}
