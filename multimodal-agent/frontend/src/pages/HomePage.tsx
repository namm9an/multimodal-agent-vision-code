import { Link } from "react-router-dom";
import { SignedIn, SignedOut, SignUpButton } from "@clerk/clerk-react";
import { Upload, Cpu, Shield, Zap } from "lucide-react";

/**
 * Public home page with hero section and features.
 */
export function HomePage() {
    return (
        <div className="space-y-16">
            {/* Hero Section */}
            <section className="text-center space-y-6 py-12">
                <h1 className="text-5xl font-bold tracking-tight">
                    <span className="gradient-text">AI-Powered</span> Image Analysis
                </h1>
                <p className="text-xl text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
                    Upload images, let AI analyze them, and automatically generate Python
                    code to extract insights, create visualizations, and process data.
                </p>

                <div className="flex justify-center gap-4 pt-4">
                    <SignedIn>
                        <Link
                            to="/dashboard"
                            className="inline-flex items-center rounded-lg bg-blue-600 px-6 py-3 text-lg font-medium text-white hover:bg-blue-700 transition-colors"
                        >
                            Go to Dashboard
                            <Zap className="ml-2 h-5 w-5" />
                        </Link>
                    </SignedIn>

                    <SignedOut>
                        <SignUpButton mode="modal">
                            <button className="inline-flex items-center rounded-lg bg-blue-600 px-6 py-3 text-lg font-medium text-white hover:bg-blue-700 transition-colors">
                                Get Started Free
                                <Zap className="ml-2 h-5 w-5" />
                            </button>
                        </SignUpButton>
                    </SignedOut>
                </div>
            </section>

            {/* Features Section */}
            <section className="grid md:grid-cols-3 gap-8">
                <FeatureCard
                    icon={<Upload className="h-8 w-8 text-blue-600" />}
                    title="Upload Images"
                    description="Simply drag and drop PNG or JPG images. We support charts, graphs, documents, and more."
                />
                <FeatureCard
                    icon={<Cpu className="h-8 w-8 text-purple-600" />}
                    title="AI Analysis"
                    description="Powered by Qwen, Mistral, and DeepSeek models for vision understanding and code generation."
                />
                <FeatureCard
                    icon={<Shield className="h-8 w-8 text-green-600" />}
                    title="Secure Execution"
                    description="Generated Python code runs in an isolated sandbox with strict security controls."
                />
            </section>

            {/* How It Works Section */}
            <section className="space-y-8">
                <h2 className="text-3xl font-bold text-center">How It Works</h2>
                <div className="grid md:grid-cols-4 gap-6">
                    <StepCard step={1} title="Upload" description="Upload your image" />
                    <StepCard
                        step={2}
                        title="Analyze"
                        description="AI understands the content"
                    />
                    <StepCard
                        step={3}
                        title="Generate"
                        description="Python code is created"
                    />
                    <StepCard
                        step={4}
                        title="Execute"
                        description="Results are delivered"
                    />
                </div>
            </section>
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
        <div className="rounded-xl border bg-white p-6 shadow-sm card-hover dark:bg-slate-800 dark:border-slate-700">
            <div className="mb-4">{icon}</div>
            <h3 className="text-lg font-semibold mb-2">{title}</h3>
            <p className="text-slate-600 dark:text-slate-300">{description}</p>
        </div>
    );
}

interface StepCardProps {
    step: number;
    title: string;
    description: string;
}

function StepCard({ step, title, description }: StepCardProps) {
    return (
        <div className="text-center space-y-2">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 text-blue-600 font-bold text-lg dark:bg-blue-900 dark:text-blue-300">
                {step}
            </div>
            <h4 className="font-semibold">{title}</h4>
            <p className="text-sm text-slate-600 dark:text-slate-400">{description}</p>
        </div>
    );
}
