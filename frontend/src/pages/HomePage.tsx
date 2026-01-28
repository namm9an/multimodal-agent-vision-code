import { Link } from "react-router-dom";
import { SignedIn, SignedOut, SignUpButton } from "@clerk/clerk-react";
import { Upload, Eye, Code, Play, ArrowRight, Sparkles, Shield, Cpu } from "lucide-react";

/**
 * Dark theme home page with floating orbs and glass effects.
 */
export function HomePage() {
    return (
        <div className="relative min-h-screen overflow-hidden">
            {/* Floating Orbs Background */}
            <div className="fixed inset-0 pointer-events-none overflow-hidden">
                <div className="floating-orb orb-1" />
                <div className="floating-orb orb-2" />
                <div className="floating-orb orb-3" />
            </div>

            {/* Content */}
            <div className="relative z-10 space-y-32 py-16">
                {/* Hero Section */}
                <section className="text-center space-y-8 pt-16 max-w-5xl mx-auto fade-up">
                    {/* Badge */}
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass text-sm text-white/70">
                        <Sparkles className="h-4 w-4" />
                        <span>Powered by vision AI</span>
                    </div>

                    {/* Heading */}
                    <h1 className="text-hero fade-up delay-1">
                        Understand images.
                        <br />
                        <span className="text-white/40">Generate code.</span>
                    </h1>

                    {/* Subheading */}
                    <p className="text-xl text-white/50 max-w-2xl mx-auto leading-relaxed fade-up delay-2">
                        Upload any image and let AI analyze it, extract insights,
                        and automatically generate Python code for your workflows.
                    </p>

                    {/* CTA */}
                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-8 fade-up delay-3">
                        <SignedIn>
                            <Link to="/dashboard" className="btn-primary flex items-center gap-2">
                                Open Dashboard
                                <ArrowRight className="h-4 w-4" />
                            </Link>
                        </SignedIn>

                        <SignedOut>
                            <SignUpButton mode="modal">
                                <button className="btn-primary flex items-center gap-2">
                                    Get started
                                    <ArrowRight className="h-4 w-4" />
                                </button>
                            </SignUpButton>
                            <Link to="/dashboard" className="btn-ghost">
                                View demo
                            </Link>
                        </SignedOut>
                    </div>
                </section>

                {/* Demo Card */}
                <section className="max-w-4xl mx-auto px-4 fade-up delay-4">
                    <div className="card-glass aspect-video flex items-center justify-center">
                        <div className="text-center space-y-4">
                            <div className="inline-flex p-4 rounded-2xl glass-strong">
                                <Upload className="h-8 w-8 text-white/60" />
                            </div>
                            <p className="text-white/40">Drop an image to start</p>
                        </div>
                    </div>
                </section>

                {/* How It Works */}
                <section className="max-w-5xl mx-auto px-4 space-y-16">
                    <h2 className="text-4xl md:text-5xl font-semibold text-center fade-up">
                        How it works
                    </h2>

                    <div className="grid md:grid-cols-4 gap-4">
                        <StepCard
                            number="01"
                            icon={<Upload className="h-5 w-5" />}
                            title="Upload"
                            description="Drag and drop any image"
                        />
                        <StepCard
                            number="02"
                            icon={<Eye className="h-5 w-5" />}
                            title="Analyze"
                            description="AI understands content"
                        />
                        <StepCard
                            number="03"
                            icon={<Code className="h-5 w-5" />}
                            title="Generate"
                            description="Python code is created"
                        />
                        <StepCard
                            number="04"
                            icon={<Play className="h-5 w-5" />}
                            title="Execute"
                            description="Results delivered securely"
                        />
                    </div>
                </section>

                {/* Features */}
                <section className="max-w-5xl mx-auto px-4 space-y-16">
                    <h2 className="text-4xl md:text-5xl font-semibold text-center">
                        Built for developers
                    </h2>

                    <div className="grid md:grid-cols-3 gap-4">
                        <FeatureCard
                            icon={<Cpu className="h-6 w-6" />}
                            title="Multiple AI Models"
                            description="Choose from Qwen, Llama, and DeepSeek for optimal results."
                        />
                        <FeatureCard
                            icon={<Shield className="h-6 w-6" />}
                            title="Secure Sandbox"
                            description="All code runs in isolated containers with strict security."
                        />
                        <FeatureCard
                            icon={<Sparkles className="h-6 w-6" />}
                            title="Instant Results"
                            description="Get analysis and code in seconds, not minutes."
                        />
                    </div>
                </section>

                {/* CTA Section */}
                <section className="text-center py-20 space-y-6 max-w-2xl mx-auto">
                    <h2 className="text-4xl md:text-5xl font-semibold">
                        Ready to start?
                    </h2>
                    <p className="text-white/50 text-lg">
                        Join developers automating image analysis with AI.
                    </p>
                    <SignedOut>
                        <SignUpButton mode="modal">
                            <button className="btn-primary flex items-center gap-2 mx-auto">
                                Create free account
                                <ArrowRight className="h-4 w-4" />
                            </button>
                        </SignUpButton>
                    </SignedOut>
                    <SignedIn>
                        <Link to="/dashboard" className="btn-primary flex items-center gap-2 mx-auto w-fit">
                            Open Dashboard
                            <ArrowRight className="h-4 w-4" />
                        </Link>
                    </SignedIn>
                </section>
            </div>
        </div>
    );
}

interface StepCardProps {
    number: string;
    icon: React.ReactNode;
    title: string;
    description: string;
}

function StepCard({ number, icon, title, description }: StepCardProps) {
    return (
        <div className="card-glass">
            <div className="text-xs font-medium text-white/30 mb-4">{number}</div>
            <div className="inline-flex p-2.5 rounded-xl glass text-white/60 mb-4">
                {icon}
            </div>
            <h3 className="font-semibold text-lg mb-1">{title}</h3>
            <p className="text-white/40 text-sm">{description}</p>
        </div>
    );
}

interface FeatureCardProps {
    icon: React.ReactNode;
    title: string;
    description: string;
}

function FeatureCard({ icon, title, description }: FeatureCardProps) {
    return (
        <div className="card-glass">
            <div className="inline-flex p-3 rounded-xl glass text-white/70 mb-4">
                {icon}
            </div>
            <h3 className="font-semibold text-lg mb-2">{title}</h3>
            <p className="text-white/40">{description}</p>
        </div>
    );
}
