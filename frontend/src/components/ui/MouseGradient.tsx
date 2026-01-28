"use client";

import { useEffect, useState } from "react";
import { motion, useMotionValue, useSpring } from "framer-motion";

/**
 * Mouse-following radial gradient background (Resend-style).
 * Creates a soft glow that follows the cursor position.
 */
export function MouseGradient() {
    const [mounted, setMounted] = useState(false);

    // Track mouse position
    const mouseX = useMotionValue(0);
    const mouseY = useMotionValue(0);

    // Smooth spring animation for cursor following
    const smoothX = useSpring(mouseX, { damping: 50, stiffness: 300 });
    const smoothY = useSpring(mouseY, { damping: 50, stiffness: 300 });

    useEffect(() => {
        setMounted(true);

        const handleMouseMove = (e: MouseEvent) => {
            mouseX.set(e.clientX);
            mouseY.set(e.clientY);
        };

        window.addEventListener("mousemove", handleMouseMove);
        return () => window.removeEventListener("mousemove", handleMouseMove);
    }, [mouseX, mouseY]);

    if (!mounted) return null;

    return (
        <div className="fixed inset-0 pointer-events-none overflow-hidden">
            {/* Primary gradient - follows cursor */}
            <motion.div
                className="absolute w-[600px] h-[600px] rounded-full"
                style={{
                    x: smoothX,
                    y: smoothY,
                    translateX: "-50%",
                    translateY: "-50%",
                    background: "radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%)",
                    filter: "blur(40px)",
                }}
            />

            {/* Secondary accent gradient */}
            <motion.div
                className="absolute w-[400px] h-[400px] rounded-full"
                style={{
                    x: smoothX,
                    y: smoothY,
                    translateX: "-30%",
                    translateY: "-70%",
                    background: "radial-gradient(circle, rgba(236, 72, 153, 0.1) 0%, transparent 70%)",
                    filter: "blur(60px)",
                }}
            />

            {/* Tertiary blue accent */}
            <motion.div
                className="absolute w-[300px] h-[300px] rounded-full"
                style={{
                    x: smoothX,
                    y: smoothY,
                    translateX: "-70%",
                    translateY: "-30%",
                    background: "radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%)",
                    filter: "blur(50px)",
                }}
            />
        </div>
    );
}
