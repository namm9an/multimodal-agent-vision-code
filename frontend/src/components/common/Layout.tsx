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
 * Clean, minimal layout inspired by Limitless design.
 */
export function Layout() {
    return (
        <div className="min-h-screen bg-white">
            {/* Navigation Header */}
            <header className="sticky top-0 z-50 w-full bg-white/80 backdrop-blur-md border-b border-gray-100">
                <div className="container mx-auto flex h-16 items-center justify-between px-6">
                    {/* Logo */}
                    <Link to="/" className="flex items-center space-x-2.5">
                        <div className="p-1.5 rounded-lg bg-gray-900">
                            <Sparkles className="h-4 w-4 text-white" />
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
                                className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
                            >
                                Dashboard
                            </Link>
                            <UserButton
                                afterSignOutUrl="/"
                                appearance={{
                                    elements: {
                                        avatarBox: "h-8 w-8",
                                    },
                                }}
                            />
                        </SignedIn>

                        <SignedOut>
                            <SignInButton mode="modal">
                                <button className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors">
                                    Sign in
                                </button>
                            </SignInButton>
                            <SignUpButton mode="modal">
                                <button className="px-4 py-2 text-sm font-medium text-white bg-gray-900 rounded-full hover:bg-gray-800 transition-colors">
                                    Get started
                                </button>
                            </SignUpButton>
                        </SignedOut>
                    </nav>
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-6 py-12">
                <Outlet />
            </main>

            {/* Footer */}
            <footer className="border-t border-gray-100">
                <div className="container mx-auto px-6 py-8">
                    <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                        <div className="flex items-center space-x-2 text-sm text-gray-500">
                            <Sparkles className="h-4 w-4" />
                            <span>Powered by Qwen, Llama & DeepSeek</span>
                        </div>
                        <p className="text-sm text-gray-400">
                            © 2026 Multimodal Agent
                        </p>
                    </div>
                </div>
            </footer>
        </div>
    );
}
