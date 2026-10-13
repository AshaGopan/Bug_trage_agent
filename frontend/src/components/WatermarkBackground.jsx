import React from 'react';

export default function WatermarkBackground() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden transition-colors duration-200">
      {/* Top right subtle circuit graphic */}
      <svg
        className="corner-watermark-right text-indigo-600 dark:text-indigo-400"
        viewBox="0 0 200 200"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M20 20 H100 V80 H160 V160"
          stroke="currentColor"
          strokeWidth="3"
          strokeLinecap="round"
          strokeDasharray="6 6"
        />
        <circle cx="20" cy="20" r="6" fill="currentColor" />
        <circle cx="100" cy="80" r="5" fill="currentColor" />
        <circle cx="160" cy="160" r="7" fill="currentColor" />
        <path d="M120 20 H180 V60" stroke="currentColor" strokeWidth="2.5" />
        <circle cx="180" cy="60" r="4" fill="currentColor" />
      </svg>

      {/* Bottom left subtle bug watermark */}
      <svg
        className="corner-watermark-left text-indigo-700 dark:text-indigo-400"
        viewBox="0 0 200 200"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Bug outline silhouette */}
        <ellipse cx="100" cy="115" rx="35" ry="45" stroke="currentColor" strokeWidth="3" />
        <circle cx="100" cy="55" r="22" stroke="currentColor" strokeWidth="3" />
        {/* Antennae */}
        <path d="M85 40 Q70 20 55 25" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
        <path d="M115 40 Q130 20 145 25" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
        {/* Legs */}
        <path d="M65 95 Q30 90 20 75" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
        <path d="M135 95 Q170 90 180 75" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
        <path d="M65 115 Q30 115 15 125" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
        <path d="M135 115 Q170 115 185 125" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
        <path d="M65 135 Q35 150 25 170" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
        <path d="M135 135 Q165 150 175 170" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
        {/* Wing split */}
        <line x1="100" y1="70" x2="100" y2="160" stroke="currentColor" strokeWidth="2.5" />
      </svg>
    </div>
  );
}
