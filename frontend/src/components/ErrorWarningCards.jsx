import React from 'react';
import { AlertTriangle, AlertCircle, FileQuestion, Inbox, ArrowRight, RotateCcw } from 'lucide-react';

/**
 * 1. "We couldn't identify this issue"
 */
export function UnidentifiedIssueCard({ onTryAgain }) {
  return (
    <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-8 text-center shadow-card dark:shadow-dark-card max-w-md mx-auto transition-colors duration-200">
      <div className="w-12 h-12 rounded-2xl bg-amber-50 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400 border border-amber-200 dark:border-amber-800/80 flex items-center justify-center mx-auto mb-4 shadow-sm">
        <AlertTriangle className="w-6 h-6" />
      </div>
      <h3 className="text-lg font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-1.5">
        We couldn't identify this issue
      </h3>
      <p className="text-xs sm:text-sm text-[#64748B] dark:text-[#94A3B8] mb-5 leading-relaxed">
        Check the GitHub URL or paste the issue description.
      </p>
      <button
        onClick={onTryAgain}
        className="bg-[#2E31E8] hover:bg-[#2326C4] text-white font-semibold px-5 py-2.5 rounded-xl text-xs sm:text-sm shadow-md shadow-indigo-600/25 transition-all inline-flex items-center gap-1.5"
      >
        <span>Try Again</span>
        <RotateCcw className="w-3.5 h-3.5" />
      </button>
    </div>
  );
}

/**
 * 2. "Analysis couldn't be completed"
 */
export function AnalysisFailedCard({ onRetry }) {
  return (
    <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-8 text-center shadow-card dark:shadow-dark-card max-w-md mx-auto transition-colors duration-200">
      <div className="w-12 h-12 rounded-2xl bg-rose-50 dark:bg-rose-950/60 text-rose-600 dark:text-rose-400 border border-rose-200 dark:border-rose-800/80 flex items-center justify-center mx-auto mb-4 shadow-sm">
        <AlertCircle className="w-6 h-6" />
      </div>
      <h3 className="text-lg font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-1.5">
        Analysis couldn't be completed
      </h3>
      <p className="text-xs sm:text-sm text-[#64748B] dark:text-[#94A3B8] mb-5 leading-relaxed">
        Something went wrong while processing the issue. Please try again.
      </p>
      <button
        onClick={onRetry}
        className="bg-[#2E31E8] hover:bg-[#2326C4] text-white font-semibold px-5 py-2.5 rounded-xl text-xs sm:text-sm shadow-md shadow-indigo-600/25 transition-all inline-flex items-center gap-1.5"
      >
        <span>Retry Analysis</span>
        <RotateCcw className="w-3.5 h-3.5" />
      </button>
    </div>
  );
}

/**
 * 3. "More details would help"
 */
export function MoreDetailsCard({ onReviewMissing }) {
  return (
    <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-8 text-center shadow-card dark:shadow-dark-card max-w-md mx-auto transition-colors duration-200">
      <div className="w-12 h-12 rounded-2xl bg-indigo-50 dark:bg-indigo-950/60 text-[#2E31E8] dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800/80 flex items-center justify-center mx-auto mb-4 shadow-sm">
        <FileQuestion className="w-6 h-6" />
      </div>
      <h3 className="text-lg font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-1.5">
        More details would help
      </h3>
      <p className="text-xs sm:text-sm text-[#64748B] dark:text-[#94A3B8] mb-5 leading-relaxed">
        This issue may need additional diagnostic information before it can be triaged confidently.
      </p>
      <button
        onClick={onReviewMissing}
        className="bg-white dark:bg-[#1E293B] hover:bg-gray-50 dark:hover:bg-[#283548] border border-[#E5E7EB] dark:border-[#334155] text-[#2E31E8] dark:text-indigo-400 font-semibold px-5 py-2.5 rounded-xl text-xs sm:text-sm shadow-sm transition-all inline-flex items-center gap-1.5"
      >
        <span>Review Missing Information</span>
        <ArrowRight className="w-3.5 h-3.5" />
      </button>
    </div>
  );
}

/**
 * 4. "Nothing here yet"
 */
export function EmptyStateCard({ onAction }) {
  return (
    <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-8 text-center shadow-card dark:shadow-dark-card max-w-md mx-auto transition-colors duration-200">
      <div className="w-12 h-12 rounded-2xl bg-gray-50 dark:bg-[#161F30] text-gray-400 dark:text-slate-500 border border-gray-200 dark:border-[#1F2937] flex items-center justify-center mx-auto mb-4 shadow-sm">
        <Inbox className="w-6 h-6" />
      </div>
      <h3 className="text-lg font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-1.5">
        Nothing here yet
      </h3>
      <p className="text-xs sm:text-sm text-[#64748B] dark:text-[#94A3B8] mb-5 leading-relaxed">
        Your analyzed issues will appear here when available.
      </p>
      {onAction && (
        <button
          onClick={onAction}
          className="bg-[#2E31E8] hover:bg-[#2326C4] text-white font-semibold px-5 py-2 rounded-xl text-xs shadow-sm transition-all inline-flex items-center gap-1.5"
        >
          <span>Go to Workspace</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      )}
    </div>
  );
}
