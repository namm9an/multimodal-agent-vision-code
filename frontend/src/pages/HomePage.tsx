import { Link } from "react-router-dom";
import { SignedIn, SignedOut, SignUpButton } from "@clerk/clerk-react";
import { Upload, Eye, Code, Play, ArrowRight, Sparkles, Shield, Cpu } from "lucide-react";

/**
 * Clean, minimal home page inspired by Limitless design.
 */
export function HomePage() {
    return (
        <div className="space-y-24">
            {/* Hero Section */}
            <section className="text-center pt-16 pb-8 space-y-8 max-w-4xl mx-auto">
                {/* Badge */}
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-full text-sm text-gray-600">
                    <Sparkles className="h-4 w-4" />
                    <span>Powered by vision AI</span>
                </div>

                {/* Heading */}
                <h1 className="text-5xl md:text-6xl lg:text-7xl font-semibold tracking-tight leading-[1.1]">
                    Understand images.
                    <br />
                    <span className="text-gray-400">Generate code.</span>
                </h1>

                {/* Subheading */}
                <p className="text-xl text-gray-500 max-w-2xl mx-auto leading-relaxed">
                    Upload any image and let AI analyze it, extract data,
                    and automatically generate Python code for your workflows.
                </p>

                {/* CTA */}
                <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
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
                        <Link to="/dashboard" className="btn-secondary">
                            Try demo
                        </Link>
                    </SignedOut>
                </div>
            </section>

            {/* Visual Demo Section */}
            <section className="card-clean p-8 md:p-12 max-w-5xl mx-auto">
                <div className="aspect-video rounded-xl bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
                    <div className="text-center space-y-4">
                        <div className="inline-flex p-4 rounded-2xl bg-white shadow-soft">
                            <Upload className="h-8 w-8 text-gray-400" />
                        </div>
                        <p className="text-gray-500">Drop an image to see the magic</p>
                    </div>
                </div>
            </section>

            {/* How It Works */}
            <section className="max-w-5xl mx-auto space-y-16">
                <div className="text-center">
                    <h2 className="text-3xl md:text-4xl font-semibold">
                        How it works
                    </h2>
                </div>

                <div className="grid md:grid-cols-4 gap-6">
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
            <section className="max-w-5xl mx-auto space-y-16">
                <div className="text-center">
                    <h2 className="text-3xl md:text-4xl font-semibold">
                        Built for developers
                    </h2>
                </div>

                <div className="grid md:grid-cols-3 gap-6">
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
            <section className="text-center py-16 space-y-6 max-w-2xl mx-auto">
                <h2 className="text-3xl md:text-4xl font-semibold">
                    Ready to start?
                </h2>
                <p className="text-gray-500 text-lg">
                    Join developers who are automating image analysis with AI.
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
        <div className="card-clean p-6 hover-lift">
            <div className="text-xs font-medium text-gray-400 mb-4">{number}</div>
            <div className="inline-flex p-2.5 rounded-xl bg-gray-100 text-gray-600 mb-4">
                {icon}
            </div>
            <h3 className="font-semibold text-lg mb-1">{title}</h3>
            <p className="text-gray-500 text-sm">{description}</p>
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
        <div className="card-clean p-6 hover-lift">
            <div className="inline-flex p-3 rounded-xl bg-gray-100 text-gray-700 mb-4">
                {icon}
            </div>
            <h3 className="font-semibold text-lg mb-2">{title}</h3>
            <p className="text-gray-500">{description}</p>
        </div>
    );
}
