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
 * Dark glassmorphism layout with floating background.
 */
export function Layout() {
    return (
        <div className="min-h-screen bg-black text-white">
            {/* Navigation Header */}
            <header className="fixed top-0 left-0 right-0 z-50 glass border-b border-white/5">
                <div className="container mx-auto flex h-16 items-center justify-between px-6">
                    {/* Logo */}
                    <Link to="/" className="flex items-center space-x-2.5 group">
                        <div className="p-1.5 rounded-lg bg-white group-hover:scale-110 transition-transform">
                            <Sparkles className="h-4 w-4 text-black" />
                        </div>
                        <span className="font-semibold text-lg">
                            Multimodal Agent
                        </span>
                    </Link>

                    {/* Navigation */}
                    <nav className="flex items-center space-x-4">
                        <SignedIn>
                            <Link
                                to="/dashboard"
                                className="px-4 py-2 text-sm font-medium text-white/60 hover:text-white transition-colors"
                            >
                                Dashboard
                            </Link>
                            <UserButton
                                afterSignOutUrl="/"
                                appearance={{
                                    elements: {
                                        avatarBox: "h-8 w-8 ring-2 ring-white/20",
                                    },
                                }}
                            />
                        </SignedIn>

                        <SignedOut>
                            <SignInButton mode="modal">
                                <button className="px-4 py-2 text-sm font-medium text-white/60 hover:text-white transition-colors">
                                    Sign in
                                </button>
                            </SignInButton>
                            <SignUpButton mode="modal">
                                <button className="btn-primary text-sm">
                                    Get started
                                </button>
                            </SignUpButton>
                        </SignedOut>
                    </nav>
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-6 pt-24 pb-12">
                <Outlet />
            </main>

            {/* Footer */}
            <footer className="glass border-t border-white/5">
                <div className="container mx-auto px-6 py-8">
                    <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                        <div className="flex items-center space-x-2 text-sm text-white/40">
                            <Sparkles className="h-4 w-4" />
                            <span>Powered by Qwen, Llama & DeepSeek</span>
                        </div>
                        <p className="text-sm text-white/30">
                            © 2026 Multimodal Agent
                        </p>
                    </div>
                </div>
            </footer>
        </div>
    );
}
