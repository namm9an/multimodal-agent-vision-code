import { Link } from "react-router-dom";
import { SignedIn, SignedOut, SignUpButton } from "@clerk/clerk-react";
import { Upload, Eye, Code, Play, ArrowRight, Cpu, Shield, Zap } from "lucide-react";
import { motion } from "framer-motion";
import { MouseGradient } from "@/components/ui/MouseGradient";
import { SpotlightCard } from "@/components/ui/SpotlightCard";
import { FadeIn, StaggerContainer, StaggerItem } from "@/components/ui/Animations";

/**
 * Home page with Resend/Linear style animations.
 */
export function HomePage() {
    return (
        <div className="relative min-h-screen">
            {/* Mouse-following gradient background */}
            <MouseGradient />

            {/* Content */}
            <div className="relative z-10 space-y-32 py-16">
                {/* Hero Section */}
                <section className="text-center space-y-8 pt-20 max-w-5xl mx-auto">
                    <FadeIn>
                        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 text-sm text-white/60">
                            <Zap className="h-4 w-4" />
                            <span>Powered by vision AI</span>
                        </div>
                    </FadeIn>

                    <FadeIn delay={0.1}>
                        <h1 className="text-5xl md:text-7xl lg:text-8xl font-semibold tracking-tight leading-[1.05]">
                            Understand images.
                            <br />
                            <span className="text-white/40">Generate code.</span>
                        </h1>
                    </FadeIn>

                    <FadeIn delay={0.2}>
                        <p className="text-xl text-white/50 max-w-2xl mx-auto leading-relaxed">
                            Upload any image and let AI analyze it, extract insights,
                            and automatically generate Python code for your workflows.
                        </p>
                    </FadeIn>

                    <FadeIn delay={0.3}>
                        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-8">
                            <SignedIn>
                                <Link to="/dashboard">
                                    <motion.button
                                        className="px-6 py-3 bg-white text-black font-medium rounded-full flex items-center gap-2"
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.98 }}
                                    >
                                        Open Dashboard
                                        <ArrowRight className="h-4 w-4" />
                                    </motion.button>
                                </Link>
                            </SignedIn>

                            <SignedOut>
                                <SignUpButton mode="modal">
                                    <motion.button
                                        className="px-6 py-3 bg-white text-black font-medium rounded-full flex items-center gap-2"
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.98 }}
                                    >
                                        Get started
                                        <ArrowRight className="h-4 w-4" />
                                    </motion.button>
                                </SignUpButton>
                                <Link to="/dashboard">
                                    <motion.button
                                        className="px-6 py-3 text-white font-medium rounded-full bg-white/5 border border-white/10"
                                        whileHover={{ scale: 1.02, backgroundColor: "rgba(255,255,255,0.1)" }}
                                        whileTap={{ scale: 0.98 }}
                                    >
                                        View demo
                                    </motion.button>
                                </Link>
                            </SignedOut>
                        </div>
                    </FadeIn>
                </section>

                {/* Demo Preview */}
                <FadeIn delay={0.4}>
                    <section className="max-w-4xl mx-auto px-4">
                        <SpotlightCard className="aspect-video flex items-center justify-center relative overflow-hidden">
                            {/* Grid pattern background */}
                            <div
                                className="absolute inset-0 opacity-20"
                                style={{
                                    backgroundImage: `linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px)`,
                                    backgroundSize: '40px 40px'
                                }}
                            />

                            <div className="text-center space-y-6 z-10">
                                <motion.div
                                    className="flex items-center justify-center gap-8"
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ duration: 1 }}
                                >
                                    {/* Upload icon */}
                                    <div className="flex flex-col items-center gap-2">
                                        <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                                            <Upload className="h-6 w-6 text-white/40" />
                                        </div>
                                        <span className="text-xs text-white/30">Upload</span>
                                    </div>

                                    {/* Arrow */}
                                    <ArrowRight className="h-5 w-5 text-white/20" />

                                    {/* Process icon */}
                                    <div className="flex flex-col items-center gap-2">
                                        <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                                            <Cpu className="h-6 w-6 text-white/40" />
                                        </div>
                                        <span className="text-xs text-white/30">Analyze</span>
                                    </div>

                                    {/* Arrow */}
                                    <ArrowRight className="h-5 w-5 text-white/20" />

                                    {/* Code icon */}
                                    <div className="flex flex-col items-center gap-2">
                                        <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                                            <Code className="h-6 w-6 text-white/40" />
                                        </div>
                                        <span className="text-xs text-white/30">Generate</span>
                                    </div>
                                </motion.div>

                                <p className="text-white/30 text-sm">See it in action on your dashboard</p>
                            </div>
                        </SpotlightCard>
                    </section>
                </FadeIn>


                {/* How It Works */}
                <section className="max-w-5xl mx-auto px-4 space-y-16">
                    <FadeIn>
                        <h2 className="text-4xl md:text-5xl font-semibold text-center">
                            How it works
                        </h2>
                    </FadeIn>

                    <StaggerContainer className="grid md:grid-cols-4 gap-4">
                        <StaggerItem>
                            <SpotlightCard>
                                <div className="text-xs font-medium text-white/30 mb-4">01</div>
                                <div className="inline-flex p-2.5 rounded-xl bg-white/5 text-white/60 mb-4">
                                    <Upload className="h-5 w-5" />
                                </div>
                                <h3 className="font-semibold text-lg mb-1">Upload</h3>
                                <p className="text-white/40 text-sm">Drag and drop any image</p>
                            </SpotlightCard>
                        </StaggerItem>
                        <StaggerItem>
                            <SpotlightCard>
                                <div className="text-xs font-medium text-white/30 mb-4">02</div>
                                <div className="inline-flex p-2.5 rounded-xl bg-white/5 text-white/60 mb-4">
                                    <Eye className="h-5 w-5" />
                                </div>
                                <h3 className="font-semibold text-lg mb-1">Analyze</h3>
                                <p className="text-white/40 text-sm">AI understands content</p>
                            </SpotlightCard>
                        </StaggerItem>
                        <StaggerItem>
                            <SpotlightCard>
                                <div className="text-xs font-medium text-white/30 mb-4">03</div>
                                <div className="inline-flex p-2.5 rounded-xl bg-white/5 text-white/60 mb-4">
                                    <Code className="h-5 w-5" />
                                </div>
                                <h3 className="font-semibold text-lg mb-1">Generate</h3>
                                <p className="text-white/40 text-sm">Python code is created</p>
                            </SpotlightCard>
                        </StaggerItem>
                        <StaggerItem>
                            <SpotlightCard>
                                <div className="text-xs font-medium text-white/30 mb-4">04</div>
                                <div className="inline-flex p-2.5 rounded-xl bg-white/5 text-white/60 mb-4">
                                    <Play className="h-5 w-5" />
                                </div>
                                <h3 className="font-semibold text-lg mb-1">Execute</h3>
                                <p className="text-white/40 text-sm">Results delivered securely</p>
                            </SpotlightCard>
                        </StaggerItem>
                    </StaggerContainer>
                </section>

                {/* Features */}
                <section className="max-w-5xl mx-auto px-4 space-y-16">
                    <FadeIn>
                        <h2 className="text-4xl md:text-5xl font-semibold text-center">
                            Built for developers
                        </h2>
                    </FadeIn>

                    <StaggerContainer className="grid md:grid-cols-3 gap-4">
                        <StaggerItem>
                            <SpotlightCard>
                                <div className="inline-flex p-3 rounded-xl bg-white/5 text-white/70 mb-4">
                                    <Cpu className="h-6 w-6" />
                                </div>
                                <h3 className="font-semibold text-lg mb-2">Multiple AI Models</h3>
                                <p className="text-white/40">Choose from Qwen, Llama, and DeepSeek for optimal results.</p>
                            </SpotlightCard>
                        </StaggerItem>
                        <StaggerItem>
                            <SpotlightCard>
                                <div className="inline-flex p-3 rounded-xl bg-white/5 text-white/70 mb-4">
                                    <Shield className="h-6 w-6" />
                                </div>
                                <h3 className="font-semibold text-lg mb-2">Secure Sandbox</h3>
                                <p className="text-white/40">All code runs in isolated containers with strict security.</p>
                            </SpotlightCard>
                        </StaggerItem>
                        <StaggerItem>
                            <SpotlightCard>
                                <div className="inline-flex p-3 rounded-xl bg-white/5 text-white/70 mb-4">
                                    <Zap className="h-6 w-6" />
                                </div>
                                <h3 className="font-semibold text-lg mb-2">Instant Results</h3>
                                <p className="text-white/40">Get analysis and code in seconds, not minutes.</p>
                            </SpotlightCard>
                        </StaggerItem>
                    </StaggerContainer>
                </section>

                {/* CTA Section */}
                <FadeIn>
                    <section className="text-center py-20 space-y-6 max-w-2xl mx-auto">
                        <h2 className="text-4xl md:text-5xl font-semibold">
                            Ready to start?
                        </h2>
                        <p className="text-white/50 text-lg">
                            Join developers automating image analysis with AI.
                        </p>
                        <SignedOut>
                            <SignUpButton mode="modal">
                                <motion.button
                                    className="px-6 py-3 bg-white text-black font-medium rounded-full flex items-center gap-2 mx-auto"
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.98 }}
                                >
                                    Create free account
                                    <ArrowRight className="h-4 w-4" />
                                </motion.button>
                            </SignUpButton>
                        </SignedOut>
                        <SignedIn>
                            <Link to="/dashboard">
                                <motion.button
                                    className="px-6 py-3 bg-white text-black font-medium rounded-full flex items-center gap-2 mx-auto"
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.98 }}
                                >
                                    Open Dashboard
                                    <ArrowRight className="h-4 w-4" />
                                </motion.button>
                            </Link>
                        </SignedIn>
                    </section>
                </FadeIn>
            </div>
        </div>
    );
}
