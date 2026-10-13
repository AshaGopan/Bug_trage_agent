import React from 'react';
import { ExternalLink, Users, Gauge, CheckSquare, Sparkles, ArrowRight, RotateCcw, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function TriageResults({
  result,
  missingInfo,
  onToggleMissingInfo,
  onReviewResponse,
  onAnalyzeAnother,
}) {
  if (!result) return null;

  const {
    title,
    repository = 'kubernetes/kubernetes',
    url,
    suggestedTeam = 'SIG Node',
    predictedLabel = 'sig/node',
    confidence = 85.0,
    status = 'Triaged',
    whyThisTeam,
    similarIssues = [],
  } = result;

  const isHighConfidence = confidence >= 85;

  return (
    <div className="relative z-10 max-w-5xl mx-auto px-4 pb-16 transition-colors duration-200">
      {/* Header Card */}
      <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-6 shadow-card dark:shadow-dark-card mb-6">
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-[11px] font-bold uppercase tracking-wider text-[#2E31E8] dark:text-indigo-300 bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-100 dark:border-indigo-800/60 px-2.5 py-0.5 rounded-full">
                Triage Results
              </span>
              <span className="text-xs font-mono text-[#64748B] dark:text-slate-400 bg-gray-100 dark:bg-[#1E293B] px-2 py-0.5 rounded-md border border-gray-200 dark:border-[#334155]">
                {repository}
              </span>
            </div>
            <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A] dark:text-[#F8FAFC] tracking-tight leading-snug">
              {title}
            </h1>
          </div>

          {url && (
            <a
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 bg-white dark:bg-[#1E293B] hover:bg-gray-50 dark:hover:bg-[#283548] border border-[#E5E7EB] dark:border-[#334155] text-[#334155] dark:text-slate-200 text-xs font-semibold px-3.5 py-2 rounded-xl shadow-sm transition-all shrink-0"
            >
              <span>GitHub Issue</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          )}
        </div>
      </div>

      {/* 3 Metric Columns Card */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {/* Metric 1: Suggested Team */}
        <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-5 shadow-card dark:shadow-dark-card">
          <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-[#64748B] dark:text-[#94A3B8] mb-2">
            <span>Suggested Team</span>
            <Users className="w-4 h-4 text-[#2E31E8] dark:text-indigo-400" />
          </div>
          <div className="text-2xl font-extrabold text-[#2E31E8] dark:text-indigo-400 tracking-tight">
            {suggestedTeam}
          </div>
          <div className="text-xs font-mono text-[#64748B] dark:text-slate-400 mt-1 bg-[#F8F9FC] dark:bg-[#161F30] inline-block px-2 py-0.5 rounded border border-gray-200 dark:border-[#1F2937]">
            {predictedLabel}
          </div>
        </div>

        {/* Metric 2: Confidence */}
        <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-5 shadow-card dark:shadow-dark-card">
          <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-[#64748B] dark:text-[#94A3B8] mb-2">
            <span>Confidence</span>
            <Gauge className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
          </div>
          <div className="text-2xl font-extrabold text-[#0F172A] dark:text-[#F8FAFC] tracking-tight">
            {confidence}%
          </div>
          <div className="mt-1">
            <span
              className={`text-xs font-semibold px-2 py-0.5 rounded-full inline-flex items-center gap-1 ${
                isHighConfidence
                  ? 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800'
                  : 'bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800'
              }`}
            >
              {isHighConfidence ? '● High Confidence (>=85%)' : '● Low Confidence (<85%)'}
            </span>
          </div>
        </div>

        {/* Metric 3: Status */}
        <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-5 shadow-card dark:shadow-dark-card">
          <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-[#64748B] dark:text-[#94A3B8] mb-2">
            <span>Status</span>
            {status === 'Triaged' ? (
              <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            ) : (
              <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400" />
            )}
          </div>
          <div className="text-2xl font-extrabold text-[#0F172A] dark:text-[#F8FAFC] tracking-tight">
            {status}
          </div>
          <div className="text-xs text-[#64748B] dark:text-[#94A3B8] mt-1">
            {status === 'Triaged' ? 'Automated SIG assignment' : 'Maintainer review recommended'}
          </div>
        </div>
      </div>

      {/* "Why this team?" Explanation Box */}
      <div className="bg-white dark:bg-[#111827] border-l-4 border-l-[#2E31E8] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-6 shadow-card dark:shadow-dark-card mb-6">
        <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[#2E31E8] dark:text-indigo-400 mb-1.5">
          <Sparkles className="w-4 h-4" />
          <span>Why this team?</span>
        </div>
        <p className="text-sm text-[#334155] dark:text-slate-300 leading-relaxed">
          {whyThisTeam ||
            `This report exhibits strong lexical and architectural alignment with ${suggestedTeam} controller loops, container lifecycle handlers, and error traces.`}
        </p>
      </div>

      {/* Bottom Split Cards: Similar Issues (Left) vs Missing Information (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Left: Similar Issues */}
        <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-6 shadow-card dark:shadow-dark-card flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4 pb-2 border-b border-[#F1F5F9] dark:border-[#1F2937]">
              <h2 className="text-base font-bold text-[#0F172A] dark:text-[#F8FAFC]">Similar Issues</h2>
              <span className="text-xs text-[#64748B] dark:text-[#94A3B8]">ChromaDB Vector Retrieval</span>
            </div>

            <div className="space-y-3">
              {similarIssues && similarIssues.length > 0 ? (
                similarIssues.slice(0, 3).map((item, idx) => (
                  <div
                    key={idx}
                    className="p-3 bg-[#F8F9FC] dark:bg-[#161F30] border border-[#E5E7EB] dark:border-[#1F2937] rounded-xl hover:border-gray-300 dark:hover:border-slate-700 transition-colors"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="text-xs font-semibold text-[#0F172A] dark:text-[#F8FAFC] line-clamp-2">
                        #{item.issue_id}: {item.title}
                      </div>
                      <span className="text-[10px] font-mono bg-white dark:bg-[#1E293B] text-[#2E31E8] dark:text-indigo-400 px-1.5 py-0.5 rounded border border-indigo-100 dark:border-indigo-800/60 shrink-0">
                        {item.label}
                      </span>
                    </div>
                    {item.distance !== undefined && item.distance !== null && (
                      <div className="text-[10px] text-[#94A3B8] dark:text-slate-500 mt-1">
                        Cosine Distance: {typeof item.distance === 'number' ? item.distance.toFixed(3) : item.distance}
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <div className="text-xs text-[#94A3B8] dark:text-slate-500 p-4 text-center bg-gray-50 dark:bg-[#161F30] rounded-xl">
                  No historical matches retrieved.
                </div>
              )}
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-[#F1F5F9] dark:border-[#1F2937] text-[11px] text-[#94A3B8] dark:text-slate-500">
            Aggregated over 70/15/15 chronological training graphs
          </div>
        </div>

        {/* Right: Missing Information Checkboxes */}
        <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-6 shadow-card dark:shadow-dark-card flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4 pb-2 border-b border-[#F1F5F9] dark:border-[#1F2937]">
              <h2 className="text-base font-bold text-[#0F172A] dark:text-[#F8FAFC]">Missing Information</h2>
              <span className="text-xs text-[#64748B] dark:text-[#94A3B8]">Diagnostic Audit</span>
            </div>

            <p className="text-xs text-[#64748B] dark:text-[#94A3B8] mb-4">
              Toggle items to automatically incorporate them into the maintainer's response draft:
            </p>

            <div className="space-y-3">
              <label className="flex items-center gap-3 p-3 rounded-xl border border-[#E5E7EB] dark:border-[#1F2937] hover:bg-gray-50 dark:hover:bg-[#1E293B] cursor-pointer transition-colors">
                <input
                  type="checkbox"
                  checked={missingInfo.stepsToReproduce}
                  onChange={() => onToggleMissingInfo('stepsToReproduce')}
                  className="w-4 h-4 rounded text-[#2E31E8] focus:ring-[#2E31E8] border-gray-300 dark:border-slate-700 bg-white dark:bg-[#1E293B]"
                />
                <div className="text-xs font-semibold text-[#1E293B] dark:text-slate-200">
                  Steps to reproduce
                </div>
              </label>

              <label className="flex items-center gap-3 p-3 rounded-xl border border-[#E5E7EB] dark:border-[#1F2937] hover:bg-gray-50 dark:hover:bg-[#1E293B] cursor-pointer transition-colors">
                <input
                  type="checkbox"
                  checked={missingInfo.relevantLogs}
                  onChange={() => onToggleMissingInfo('relevantLogs')}
                  className="w-4 h-4 rounded text-[#2E31E8] focus:ring-[#2E31E8] border-gray-300 dark:border-slate-700 bg-white dark:bg-[#1E293B]"
                />
                <div className="text-xs font-semibold text-[#1E293B] dark:text-slate-200">
                  Relevant logs
                </div>
              </label>

              <label className="flex items-center gap-3 p-3 rounded-xl border border-[#E5E7EB] dark:border-[#1F2937] hover:bg-gray-50 dark:hover:bg-[#1E293B] cursor-pointer transition-colors">
                <input
                  type="checkbox"
                  checked={missingInfo.environmentDetails}
                  onChange={() => onToggleMissingInfo('environmentDetails')}
                  className="w-4 h-4 rounded text-[#2E31E8] focus:ring-[#2E31E8] border-gray-300 dark:border-slate-700 bg-white dark:bg-[#1E293B]"
                />
                <div className="text-xs font-semibold text-[#1E293B] dark:text-slate-200">
                  Environment details
                </div>
              </label>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-[#F1F5F9] dark:border-[#1F2937] text-[11px] text-[#94A3B8] dark:text-slate-500">
            Checked items prompt the contributor for diagnostic completeness
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-wrap items-center justify-between gap-4 pt-2">
        <button
          onClick={onReviewResponse}
          className="bg-[#2E31E8] hover:bg-[#2326C4] text-white font-semibold px-6 py-2.5 rounded-xl text-sm shadow-md shadow-indigo-600/25 transition-all flex items-center gap-2"
        >
          <span>Review Suggested Response</span>
          <ArrowRight className="w-4 h-4" />
        </button>

        <button
          onClick={onAnalyzeAnother}
          className="bg-white dark:bg-[#1E293B] hover:bg-gray-50 dark:hover:bg-[#283548] border border-[#E5E7EB] dark:border-[#334155] text-[#334155] dark:text-slate-200 font-semibold px-4 py-2.5 rounded-xl text-sm shadow-sm transition-all flex items-center gap-2"
        >
          <RotateCcw className="w-4 h-4" />
          <span>Analyze Another Issue</span>
        </button>
      </div>
    </div>
  );
}
