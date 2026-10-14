import React, { useEffect, useState } from 'react';
import { CheckCircle2, Loader2, Clock, Sparkles } from 'lucide-react';
import { triageIssue } from '../services/triageApi';
import { addHistoryRecord } from '../services/historyStorage';

export default function AnalyzingProgress({ input, repository = 'kubernetes/kubernetes', onComplete, onError }) {
  const [currentStep, setCurrentStep] = useState(1);
  const [progressPct, setProgressPct] = useState(20);
  const [displayTitle, setDisplayTitle] = useState('Kubernetes Bug Report');

  const steps = [
    { id: 1, label: 'Reading issue details' },
    { id: 2, label: 'Finding similar issues' },
    { id: 3, label: 'Predicting the responsible team' },
    { id: 4, label: 'Preparing a suggested response' },
  ];

  useEffect(() => {
    let isMounted = true;

    // Determine initial title display
    const lines = input.trim().split('\n');
    const firstLine = lines[0].trim();
    if (firstLine.startsWith('http')) {
      const match = firstLine.match(/issues\/(\d+)/);
      setDisplayTitle(match ? `GitHub Issue #${match[1]} (${repository})` : firstLine);
    } else {
      setDisplayTitle(firstLine || 'Kubernetes Bug Report');
    }

    const runTriage = async () => {
      // Step 1
      if (!isMounted) return;
      setCurrentStep(1);
      setProgressPct(25);
      await new Promise((r) => setTimeout(r, 650));

      // Step 2
      if (!isMounted) return;
      setCurrentStep(2);
      setProgressPct(50);
      await new Promise((r) => setTimeout(r, 650));

      // Step 3
      if (!isMounted) return;
      setCurrentStep(3);
      setProgressPct(75);

      try {
        const triageData = await triageIssue(input, repository);

        if (!isMounted) return;
        if (triageData.title) {
          setDisplayTitle(triageData.title);
        }

        // Step 4
        setCurrentStep(4);
        setProgressPct(100);
        await new Promise((r) => setTimeout(r, 550));

        if (!isMounted) return;

        // Persist to history
        const now = new Date();
        const dateStr = now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        const record = {
          id: `issue-${Date.now()}`,
          title: triageData.title,
          repository: triageData.repository || repository,
          url: triageData.url,
          suggestedTeam: triageData.suggestedTeam,
          predictedLabel: triageData.predictedLabel,
          confidence: triageData.confidence,
          status: triageData.status,
          dateAnalyzed: dateStr,
          whyThisTeam: triageData.whyThisTeam,
          similarIssues: triageData.similarIssues,
          missingInfo: triageData.missingInfo,
          suggestedResponse: triageData.suggestedResponse,
        };
        addHistoryRecord(record);

        onComplete(triageData);
      } catch (err) {
        console.error('Triage failed:', err);
        if (isMounted) {
          onError(err.message || 'Analysis could not be completed.');
        }
      }
    };

    runTriage();

    return () => {
      isMounted = false;
    };
  }, [input, repository]);

  return (
    <div className="relative z-10 max-w-3xl mx-auto px-4 pb-16 pt-4 transition-colors duration-200">
      {/* Top summary card */}
      <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-5 shadow-card dark:shadow-dark-card mb-6 flex flex-wrap items-center justify-between gap-3">
        <div className="flex-1 min-w-[240px]">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[11px] font-bold uppercase tracking-wider text-[#2E31E8] dark:text-indigo-300 bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-100 dark:border-indigo-800/60 px-2 py-0.5 rounded-full">
              Issue Summary
            </span>
            <span className="text-xs text-gray-400 dark:text-slate-500 font-mono">{repository}</span>
          </div>
          <h2 className="text-base font-bold text-[#0F172A] dark:text-[#F8FAFC] truncate">
            {displayTitle}
          </h2>
        </div>
        <div className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-gray-50 dark:bg-[#161F30] border border-gray-200 dark:border-[#1F2937] text-gray-600 dark:text-slate-300 flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5 text-[#2E31E8] dark:text-indigo-400" />
          <span>Processing</span>
        </div>
      </div>

      {/* Main Progress Card */}
      <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-7 sm:p-9 shadow-elevated dark:shadow-dark-card text-left">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-[#0F172A] dark:text-[#F8FAFC] tracking-tight">
            Analyzing your issue...
          </h2>
          <p className="text-sm text-[#64748B] dark:text-[#94A3B8] mt-1">
            We're reviewing the issue and preparing triage recommendations.
          </p>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-gray-100 dark:bg-gray-800 h-2 rounded-full mb-8 overflow-hidden">
          <div
            className="bg-[#2E31E8] h-full rounded-full transition-all duration-500 ease-out"
            style={{ width: `${progressPct}%` }}
          />
        </div>

        {/* 4 Steps Checklist */}
        <div className="space-y-3 mb-8">
          {steps.map((step) => {
            const isCompleted = currentStep > step.id;
            const isActive = currentStep === step.id;
            const isPending = currentStep < step.id;

            return (
              <div
                key={step.id}
                className={`flex items-center gap-3.5 p-3.5 rounded-xl border transition-all ${
                  isActive
                    ? 'bg-indigo-50/70 dark:bg-indigo-950/50 border-indigo-200 dark:border-indigo-800/80 text-[#2E31E8] dark:text-indigo-300 font-semibold'
                    : isCompleted
                    ? 'bg-emerald-50/50 dark:bg-emerald-950/30 border-emerald-100 dark:border-emerald-900/40 text-emerald-800 dark:text-emerald-300'
                    : 'bg-white dark:bg-[#161F30] border-[#E5E7EB] dark:border-[#1F2937] text-gray-400 dark:text-slate-500'
                }`}
              >
                <div className="shrink-0">
                  {isCompleted && <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />}
                  {isActive && <Loader2 className="w-5 h-5 text-[#2E31E8] dark:text-indigo-400 animate-spin" />}
                  {isPending && <Clock className="w-5 h-5 text-gray-300 dark:text-slate-600" />}
                </div>

                <div className="text-sm font-medium">
                  {step.label}
                  {isActive && <span className="ml-2 text-xs font-normal opacity-75">...</span>}
                </div>
              </div>
            );
          })}
        </div>

        <div className="pt-4 border-t border-[#F1F5F9] dark:border-[#1F2937] text-xs text-[#94A3B8] dark:text-slate-500 flex items-center justify-between">
          <span>This may take a few moments.</span>
          <span>Connecting to LangGraph agent nodes</span>
        </div>
      </div>
    </div>
  );
}
