import { Link } from "react-router-dom";
import { SignedIn, SignedOut, SignUpButton } from "@clerk/clerk-react";
import { Upload, Cpu, Shield, Zap, Sparkles, Code, Eye, Play } from "lucide-react";

/**
 * Premium home page with modern glassmorphism design.
 */
export function HomePage() {
    return (
        <div className="relative min-h-screen overflow-hidden">
            {/* Animated Background Orbs */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                <div className="orb w-96 h-96 bg-purple-500 -top-48 -left-48 animate-pulse" />
                <div className="orb w-80 h-80 bg-pink-500 top-1/3 -right-40" style={{ animationDelay: '1s' }} />
                <div className="orb w-64 h-64 bg-blue-500 bottom-0 left-1/4" style={{ animationDelay: '2s' }} />
            </div>

            <div className="relative z-10 space-y-24 py-12">
                {/* Hero Section */}
                <section className="text-center space-y-8 pt-16">
                    {/* Badge */}
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-purple-500/20">
                        <Sparkles className="h-4 w-4 text-purple-400" />
                        <span className="text-sm text-purple-300">Powered by Advanced AI Models</span>
                    </div>

                    {/* Main Heading */}
                    <h1 className="text-6xl md:text-7xl font-bold tracking-tight leading-tight">
                        Transform Images Into
                        <br />
                        <span className="gradient-text">Insights & Code</span>
                    </h1>

                    {/* Subheading */}
                    <p className="text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
                        Upload any image and watch AI analyze it, understand its content,
                        and generate Python code to extract data, create visualizations,
                        and automate your workflows.
                    </p>

                    {/* CTA Buttons */}
                    <div className="flex flex-col sm:flex-row justify-center gap-4 pt-6">
                        <SignedIn>
                            <Link
                                to="/dashboard"
                                className="group inline-flex items-center justify-center gap-2 px-8 py-4 text-lg font-semibold text-white bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl btn-glow"
                            >
                                Go to Dashboard
                                <Zap className="h-5 w-5 group-hover:animate-pulse" />
                            </Link>
                        </SignedIn>

                        <SignedOut>
                            <SignUpButton mode="modal">
                                <button className="group inline-flex items-center justify-center gap-2 px-8 py-4 text-lg font-semibold text-white bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl btn-glow pulse-glow">
                                    Start Free
                                    <Zap className="h-5 w-5 group-hover:animate-pulse" />
                                </button>
                            </SignUpButton>
                            <Link
                                to="/dashboard"
                                className="inline-flex items-center justify-center gap-2 px-8 py-4 text-lg font-semibold text-slate-300 glass rounded-xl hover:bg-white/10 transition-all"
                            >
                                View Demo
                            </Link>
                        </SignedOut>
                    </div>
                </section>

                {/* Features Section */}
                <section className="grid md:grid-cols-3 gap-6 px-4">
                    <FeatureCard
                        icon={<Upload className="h-8 w-8" />}
                        title="Drag & Drop Upload"
                        description="Simply drag your images — charts, documents, screenshots, or any visual data you want to analyze."
                        gradient="from-blue-500 to-cyan-500"
                    />
                    <FeatureCard
                        icon={<Eye className="h-8 w-8" />}
                        title="Vision AI Analysis"
                        description="Powered by Qwen2.5-VL for deep image understanding and intelligent content extraction."
                        gradient="from-purple-500 to-pink-500"
                    />
                    <FeatureCard
                        icon={<Shield className="h-8 w-8" />}
                        title="Secure Sandbox"
                        description="All generated code runs in an isolated container with strict security controls."
                        gradient="from-green-500 to-emerald-500"
                    />
                </section>

                {/* How It Works */}
                <section className="space-y-12 px-4">
                    <div className="text-center">
                        <h2 className="text-4xl font-bold mb-4">
                            How It <span className="gradient-text-blue">Works</span>
                        </h2>
                        <p className="text-slate-400 max-w-xl mx-auto">
                            From image to insights in four simple steps
                        </p>
                    </div>

                    <div className="grid md:grid-cols-4 gap-4">
                        <StepCard
                            step={1}
                            icon={<Upload className="h-6 w-6" />}
                            title="Upload"
                            description="Drop your image"
                        />
                        <StepCard
                            step={2}
                            icon={<Eye className="h-6 w-6" />}
                            title="Analyze"
                            description="AI understands content"
                        />
                        <StepCard
                            step={3}
                            icon={<Code className="h-6 w-6" />}
                            title="Generate"
                            description="Python code created"
                        />
                        <StepCard
                            step={4}
                            icon={<Play className="h-6 w-6" />}
                            title="Execute"
                            description="Results delivered"
                        />
                    </div>
                </section>

                {/* Stats Section */}
                <section className="glass-strong rounded-2xl p-8 mx-4">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
                        <StatItem value="3" label="AI Models" />
                        <StatItem value="<30s" label="Processing Time" />
                        <StatItem value="100%" label="Secure Sandbox" />
                        <StatItem value="∞" label="Possibilities" />
                    </div>
                </section>

                {/* CTA Section */}
                <section className="text-center space-y-6 pb-16">
                    <h3 className="text-3xl font-bold">
                        Ready to <span className="gradient-text">Get Started?</span>
                    </h3>
                    <SignedOut>
                        <SignUpButton mode="modal">
                            <button className="inline-flex items-center gap-2 px-8 py-4 text-lg font-semibold text-white bg-gradient-to-r from-purple-600 via-pink-600 to-orange-500 rounded-xl btn-glow">
                                Create Free Account
                                <Sparkles className="h-5 w-5" />
                            </button>
                        </SignUpButton>
                    </SignedOut>
                    <SignedIn>
                        <Link
                            to="/dashboard"
                            className="inline-flex items-center gap-2 px-8 py-4 text-lg font-semibold text-white bg-gradient-to-r from-purple-600 via-pink-600 to-orange-500 rounded-xl btn-glow"
                        >
                            Go to Dashboard
                            <Sparkles className="h-5 w-5" />
                        </Link>
                    </SignedIn>
                </section>
            </div>
        </div>
    );
}

interface FeatureCardProps {
    icon: React.ReactNode;
    title: string;
    description: string;
    gradient: string;
}

function FeatureCard({ icon, title, description, gradient }: FeatureCardProps) {
    return (
        <div className="group glass rounded-2xl p-6 card-hover">
            <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${gradient} mb-4`}>
                <div className="text-white">{icon}</div>
            </div>
            <h3 className="text-xl font-semibold mb-2 group-hover:text-purple-400 transition-colors">
                {title}
            </h3>
            <p className="text-slate-400 leading-relaxed">{description}</p>
        </div>
    );
}

interface StepCardProps {
    step: number;
    icon: React.ReactNode;
    title: string;
    description: string;
}

function StepCard({ step, icon, title, description }: StepCardProps) {
    return (
        <div className="relative glass rounded-xl p-6 text-center group hover:bg-white/10 transition-all">
            {/* Step Number */}
            <div className="absolute -top-3 -left-3 w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-sm font-bold">
                {step}
            </div>

            {/* Icon */}
            <div className="inline-flex p-3 rounded-full bg-white/5 text-purple-400 mb-3 group-hover:scale-110 transition-transform">
                {icon}
            </div>

            <h4 className="font-semibold mb-1">{title}</h4>
            <p className="text-sm text-slate-500">{description}</p>
        </div>
    );
}

interface StatItemProps {
    value: string;
    label: string;
}

function StatItem({ value, label }: StatItemProps) {
    return (
        <div>
            <div className="text-3xl font-bold gradient-text mb-1">{value}</div>
            <div className="text-sm text-slate-400">{label}</div>
        </div>
    );
}
