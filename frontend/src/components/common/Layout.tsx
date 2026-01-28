import { Outlet, Link } from "react-router-dom";
import {
    SignedIn,
    SignedOut,
    SignInButton,
    SignUpButton,
    UserButton,
} from "@clerk/clerk-react";
import { motion } from "framer-motion";

/**
 * Clean dark layout - no icons, minimal design.
 */
export function Layout() {
    return (
        <div className="min-h-screen bg-black text-white">
            {/* Navigation Header */}
            <header className="fixed top-0 left-0 right-0 z-50 bg-black/50 backdrop-blur-xl border-b border-white/5">
                <div className="container mx-auto flex h-16 items-center justify-between px-6">
                    {/* Logo - text only */}
                    <Link to="/" className="flex items-center">
                        <motion.span
                            className="font-semibold text-lg"
                            whileHover={{ opacity: 0.8 }}
                        >
                            Multimodal Agent
                        </motion.span>
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
                                        avatarBox: "h-8 w-8",
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
                                <motion.button
                                    className="px-4 py-2 text-sm font-medium text-white bg-white/10 rounded-full border border-white/10"
                                    whileHover={{ backgroundColor: "rgba(255,255,255,0.15)" }}
                                >
                                    Get started
                                </motion.button>
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
            <footer className="border-t border-white/5">
                <div className="container mx-auto px-6 py-8">
                    <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                        <span className="text-sm text-white/40">
                            Powered by Qwen, Llama & DeepSeek
                        </span>
                        <span className="text-sm text-white/30">
                            © 2026 Multimodal Agent
                        </span>
                    </div>
                </div>
            </footer>
        </div>
    );
}
