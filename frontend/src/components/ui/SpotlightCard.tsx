"use client";

import { useRef, useState } from "react";
import { motion } from "framer-motion";

interface SpotlightCardProps {
    children: React.ReactNode;
    className?: string;
}

/**
 * Card with spotlight hover effect (Linear-style).
 * A glowing spot follows the mouse within the card.
 */
export function SpotlightCard({ children, className = "" }: SpotlightCardProps) {
    const cardRef = useRef<HTMLDivElement>(null);
    const [position, setPosition] = useState({ x: 0, y: 0 });
    const [isHovered, setIsHovered] = useState(false);

    const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
        if (!cardRef.current) return;

        const rect = cardRef.current.getBoundingClientRect();
        setPosition({
            x: e.clientX - rect.left,
            y: e.clientY - rect.top,
        });
    };

    return (
        <motion.div
            ref={cardRef}
            className={`relative overflow-hidden rounded-2xl bg-white/5 border border-white/10 ${className}`}
            onMouseMove={handleMouseMove}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            whileHover={{ scale: 1.02, borderColor: "rgba(255,255,255,0.2)" }}
            transition={{ duration: 0.3, ease: "easeOut" }}
        >
            {/* Spotlight effect */}
            <motion.div
                className="pointer-events-none absolute -inset-px opacity-0 transition-opacity duration-300"
                style={{
                    background: `radial-gradient(400px circle at ${position.x}px ${position.y}px, rgba(99, 102, 241, 0.15), transparent 40%)`,
                }}
                animate={{ opacity: isHovered ? 1 : 0 }}
            />

            {/* Border glow on hover */}
            <motion.div
                className="pointer-events-none absolute -inset-px rounded-2xl opacity-0"
                style={{
                    background: `radial-gradient(300px circle at ${position.x}px ${position.y}px, rgba(99, 102, 241, 0.3), transparent 40%)`,
                }}
                animate={{ opacity: isHovered ? 1 : 0 }}
            />

            {/* Content */}
            <div className="relative z-10 p-6">
                {children}
            </div>
        </motion.div>
    );
}
