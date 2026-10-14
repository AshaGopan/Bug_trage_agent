import React, { useState, useEffect } from 'react';
import { Copy, Check, ArrowLeft, Send, Sparkles, MessageSquare } from 'lucide-react';

export default function SuggestedResponse({
  result,
  missingInfo,
  onBackToResults,
}) {
  if (!result) return null;

  const {
    title,
    repository = 'kubernetes/kubernetes',
    suggestedTeam = 'SIG Node',
    predictedLabel = 'sig/node',
    confidence = 85.0,
  } = result;

  const [commentText, setCommentText] = useState('');
  const [copied, setCopied] = useState(false);

  // Generate or update response whenever missingInfo changes
  useEffect(() => {
    const missingFieldNames = [];
    if (missingInfo.stepsToReproduce) missingFieldNames.push('Step-by-step reproduction instructions');
    if (missingInfo.relevantLogs) missingFieldNames.push('Component log excerpts or terminal error output');
    if (missingInfo.environmentDetails) missingFieldNames.push('Kubernetes cluster version and operating environment details');

    let response = '';
    if (confidence >= 85) {
      let missingBlock = '';
      if (missingFieldNames.length > 0) {
        missingBlock = `\n### 📋 Requested Diagnostic Details\nTo help the team review and resolve this faster, could you please provide:\n${missingFieldNames.map((f) => `- ${f}`).join('\n')}\n`;
      }

      response = `Thanks for opening this issue!

### SIG Assignment Recommendation
Based on automated multi-modal triage (**${confidence}% confidence**), this issue has been routed to **\`${predictedLabel}\`** (${suggestedTeam}).
${missingBlock}
### 🔍 Potentially Related Issues
- #115201: kube-proxy connection reset during packet filter reloads
- #108920: Intermittent controller stall under high node churn

*/sig ${predictedLabel.replace('sig/', '')}*`;
    } else {
      let missingList = missingFieldNames.length > 0 
        ? missingFieldNames.map((f) => `- ${f}`).join('\n')
        : '- Additional diagnostic error logs and reproduction steps';

      response = `Thanks for opening this issue!

### 📋 Requested Diagnostic Details
To help us identify the affected Kubernetes subsystem and route this effectively, could you please provide:
${missingList}

Once these details are added, maintainers can assign the appropriate Special Interest Group.`;
    }

    setCommentText(response);
  }, [missingInfo, confidence, predictedLabel, suggestedTeam]);

  const handleCopy = () => {
    navigator.clipboard.writeText(commentText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2200);
  };

  return (
    <div className="relative z-10 max-w-4xl mx-auto px-4 pb-16 transition-colors duration-200">
      {/* Header Card */}
      <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-6 shadow-card dark:shadow-dark-card mb-6">
        <div className="flex items-center gap-2 mb-1.5">
          <span className="text-[11px] font-bold uppercase tracking-wider text-[#2E31E8] dark:text-indigo-300 bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-100 dark:border-indigo-800/60 px-2.5 py-0.5 rounded-full">
            Response Drafter
          </span>
        </div>
        <h1 className="text-2xl font-bold text-[#0F172A] dark:text-[#F8FAFC] tracking-tight">
          Suggested Response
        </h1>
        <p className="text-xs sm:text-sm text-[#64748B] dark:text-[#94A3B8] mt-1">
          Review the draft before using it in GitHub.
        </p>
      </div>

      {/* Metadata Bar */}
      <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-4 shadow-card dark:shadow-dark-card mb-6 flex flex-wrap items-center gap-x-6 gap-y-2 text-xs">
        <div>
          <span className="text-[#64748B] dark:text-[#94A3B8] font-bold uppercase tracking-wider text-[10px]">Issue: </span>
          <span className="font-semibold text-[#0F172A] dark:text-[#F8FAFC] ml-1">{title.slice(0, 50)}...</span>
        </div>

        <div>
          <span className="text-[#64748B] dark:text-[#94A3B8] font-bold uppercase tracking-wider text-[10px]">&lt;/&gt; Repository: </span>
          <span className="font-mono text-[#0F172A] dark:text-[#F8FAFC] ml-1 bg-gray-100 dark:bg-[#1E293B] px-1.5 py-0.5 rounded border border-gray-200 dark:border-[#334155]">{repository}</span>
        </div>

        <div>
          <span className="text-[#64748B] dark:text-[#94A3B8] font-bold uppercase tracking-wider text-[10px]">Suggested Team: </span>
          <span className="font-semibold text-[#2E31E8] dark:text-indigo-300 ml-1 bg-indigo-50 dark:bg-indigo-950/60 px-2 py-0.5 rounded-full border border-indigo-100 dark:border-indigo-800/60">
            {suggestedTeam}
          </span>
        </div>
      </div>

      {/* Editable Comment Box */}
      <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-6 shadow-card dark:shadow-dark-card mb-6">
        <div className="flex items-center justify-between mb-3">
          <label className="text-xs font-bold uppercase tracking-wider text-[#1E293B] dark:text-slate-200 flex items-center gap-1.5">
            <MessageSquare className="w-3.5 h-3.5 text-[#2E31E8] dark:text-indigo-400" />
            <span>GitHub Maintainer Comment Draft</span>
          </label>
          <span className="text-[11px] text-[#94A3B8] dark:text-slate-500">Markdown formatted</span>
        </div>

        <textarea
          rows={11}
          value={commentText}
          onChange={(e) => setCommentText(e.target.value)}
          className="w-full bg-[#F3F4F6] dark:bg-[#1E293B] border border-[#E5E7EB] dark:border-[#334155] rounded-xl p-4 text-xs sm:text-sm font-mono text-[#0F172A] dark:text-[#F8FAFC] focus:outline-none focus:ring-2 focus:ring-[#2E31E8] dark:focus:ring-[#4F46E5] focus:bg-white dark:focus:bg-[#1E293B] transition-all leading-relaxed"
        />

        <div className="mt-5 flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-[#F1F5F9] dark:border-[#1F2937]">
          <div className="flex items-center gap-3">
            <button
              onClick={handleCopy}
              className="bg-[#2E31E8] hover:bg-[#2326C4] text-white font-semibold px-5 py-2.5 rounded-xl text-sm shadow-md shadow-indigo-600/25 transition-all flex items-center gap-2"
            >
              {copied ? (
                <>
                  <Check className="w-4 h-4 text-emerald-300" />
                  <span>Copied to Clipboard!</span>
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  <span>Copy Response</span>
                </>
              )}
            </button>

            <button
              onClick={onBackToResults}
              className="bg-white dark:bg-[#1E293B] hover:bg-gray-50 dark:hover:bg-[#283548] border border-[#E5E7EB] dark:border-[#334155] text-[#334155] dark:text-slate-200 font-semibold px-4 py-2.5 rounded-xl text-sm shadow-sm transition-all flex items-center gap-1.5"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back to Results</span>
            </button>
          </div>

          <span className="text-xs text-[#94A3B8] dark:text-slate-500">Review the response before posting it.</span>
        </div>
      </div>
    </div>
  );
}
