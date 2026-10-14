import React from 'react';
import {
  UnidentifiedIssueCard,
  AnalysisFailedCard,
  MoreDetailsCard,
  EmptyStateCard,
} from '../components/ErrorWarningCards';
import { Layers } from 'lucide-react';

export default function ComponentStatesView({ onNavigateToWorkspace, onNavigateToResults }) {
  return (
    <div className="relative z-10 max-w-5xl mx-auto px-4 pb-16 transition-colors duration-200">
      {/* Header */}
      <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-6 shadow-card dark:shadow-dark-card mb-8">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-100 dark:border-indigo-800/60 text-[#2E31E8] dark:text-indigo-300 text-xs font-semibold mb-2">
          <Layers className="w-3.5 h-3.5" />
          <span>Screen 10 Design Specification</span>
        </div>
        <h1 className="text-2xl font-bold text-[#0F172A] dark:text-[#F8FAFC] tracking-tight">
          Error & Warning Component States
        </h1>
        <p className="text-xs sm:text-sm text-[#64748B] dark:text-[#94A3B8] mt-1">
          UI Component Sheet demonstrating all 4 standard system and exception states.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* State 1: We couldn't identify this issue */}
        <div className="flex flex-col">
          <div className="text-xs font-bold uppercase tracking-wider text-[#64748B] dark:text-[#94A3B8] mb-2 px-1">
            State 1 — Unidentified Issue
          </div>
          <UnidentifiedIssueCard onTryAgain={onNavigateToWorkspace} />
        </div>

        {/* State 2: Analysis couldn't be completed */}
        <div className="flex flex-col">
          <div className="text-xs font-bold uppercase tracking-wider text-[#64748B] dark:text-[#94A3B8] mb-2 px-1">
            State 2 — Analysis Failed
          </div>
          <AnalysisFailedCard onRetry={onNavigateToWorkspace} />
        </div>

        {/* State 3: More details would help */}
        <div className="flex flex-col">
          <div className="text-xs font-bold uppercase tracking-wider text-[#64748B] dark:text-[#94A3B8] mb-2 px-1">
            State 3 — Low Confidence / Diagnostic Warning
          </div>
          <MoreDetailsCard onReviewMissing={onNavigateToResults} />
        </div>

        {/* State 4: Nothing here yet */}
        <div className="flex flex-col">
          <div className="text-xs font-bold uppercase tracking-wider text-[#64748B] dark:text-[#94A3B8] mb-2 px-1">
            State 4 — Empty State
          </div>
          <EmptyStateCard onAction={onNavigateToWorkspace} />
        </div>
      </div>
    </div>
  );
}
