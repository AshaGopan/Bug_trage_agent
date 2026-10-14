import React, { useState } from 'react';
import { ArrowLeft, ArrowRight, Bot, User, Github, FileText, Sparkles, RefreshCw } from 'lucide-react';
import { SAMPLE_ISSUES, getNextSample, getSampleByIndex } from '../services/sampleIssues';

export default function SplitViewSession({ onBackToLanding, onStartAnalysis }) {
  const [mode, setMode] = useState('paste'); // 'url' or 'paste'
  const [urlInput, setUrlInput] = useState('https://github.com/kubernetes/kubernetes/issues/123456');
  const [pasteInput, setPasteInput] = useState(
    `Deployment rollout stuck in ProgressDeadlineExceeded on Kubernetes v1.29.2 (Ubuntu 22.04)\n\n` +
    `Steps to reproduce:\n1. Apply Deployment with maxUnavailable: 0 and maxSurge: 1\n2. Trigger image update via kubectl set image\n3. Rollout hangs indefinitely\n\n` +
    `Error logs:\nE1014 replica_set.go:542] Sync "default/web-api" failed with ProgressDeadlineExceeded: ReplicaSet "web-api-7d9f8b" has timed out progressing.`
  );
  const [repository, setRepository] = useState('kubernetes/kubernetes');
  const [currentSampleIndex, setCurrentSampleIndex] = useState(1);

  const currentPayload = mode === 'url' ? urlInput : pasteInput;

  const handleAnalyze = () => {
    if (currentPayload.trim()) {
      onStartAnalysis(currentPayload.trim(), repository.trim() || 'kubernetes/kubernetes');
    }
  };

  const handleCycleSample = () => {
    const { sample, nextIndex } = getNextSample(currentSampleIndex);
    setCurrentSampleIndex(nextIndex);
    if (sample.url) {
      setMode('url');
      setUrlInput(sample.url);
    } else {
      setMode('paste');
      setPasteInput(sample.text);
    }
    setRepository(sample.repository || 'kubernetes/kubernetes');
  };

  const handleSelectSampleChip = (idx) => {
    const { sample } = getSampleByIndex(idx);
    setCurrentSampleIndex(idx);
    if (sample.url) {
      setMode('url');
      setUrlInput(sample.url);
    } else {
      setMode('paste');
      setPasteInput(sample.text);
    }
    setRepository(sample.repository || 'kubernetes/kubernetes');
  };

  const currentSample = currentSampleIndex !== null ? SAMPLE_ISSUES[currentSampleIndex] : null;

  return (
    <div className="relative z-10 max-w-5xl mx-auto px-4 pb-16 transition-colors duration-200">
      {/* Breadcrumb / Back button */}
      <button
        onClick={onBackToLanding}
        className="mb-4 inline-flex items-center gap-1.5 text-xs font-semibold text-[#64748B] dark:text-[#94A3B8] hover:text-[#0F172A] dark:hover:text-[#F8FAFC] transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Workspace</span>
      </button>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
        {/* Left Card: New Triage Session */}
        <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-6 shadow-card dark:shadow-dark-card">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-5">
            <div>
              <h2 className="text-xl font-bold text-[#0F172A] dark:text-[#F8FAFC] tracking-tight">New triage session</h2>
              <p className="text-xs text-[#64748B] dark:text-[#94A3B8] mt-0.5">Hi! Share a GitHub issue and I'll help triage it.</p>
            </div>

            <button
              type="button"
              onClick={handleCycleSample}
              className="bg-gray-50 dark:bg-[#161F30] hover:bg-gray-100 dark:hover:bg-[#1E293B] border border-gray-200 dark:border-[#1F2937] text-gray-700 dark:text-slate-300 px-3 py-1.5 rounded-xl text-xs font-semibold shadow-sm transition-all flex items-center gap-1.5 group"
            >
              <RefreshCw className="w-3.5 h-3.5 text-[#2E31E8] dark:text-indigo-400 group-hover:rotate-180 transition-transform duration-300" />
              <span>Next Sample</span>
            </button>
          </div>

          {/* Sample Active Badge */}
          {currentSample && (
            <div className="mb-4 flex items-center justify-between text-xs bg-indigo-50 dark:bg-indigo-950/60 text-[#2E31E8] dark:text-indigo-300 border border-indigo-100 dark:border-indigo-800/60 px-3 py-1.5 rounded-xl">
              <span className="font-bold">Sample {currentSampleIndex + 1}/8:</span>
              <span className="font-semibold truncate max-w-[260px]">{currentSample.tag}</span>
            </div>
          )}

          {/* Mode Switch Tabs */}
          <div className="flex bg-[#F3F4F6] dark:bg-[#161F30] p-1 rounded-xl mb-4 border border-[#E5E7EB] dark:border-[#1F2937]">
            <button
              onClick={() => setMode('url')}
              className={`flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all flex items-center justify-center gap-1.5 ${
                mode === 'url'
                  ? 'bg-white dark:bg-[#1E293B] text-[#2E31E8] dark:text-indigo-300 shadow-sm'
                  : 'text-[#64748B] dark:text-[#94A3B8] hover:text-[#0F172A] dark:hover:text-[#F8FAFC]'
              }`}
            >
              <Github className="w-3.5 h-3.5" />
              <span>GitHub URL</span>
            </button>
            <button
              onClick={() => setMode('paste')}
              className={`flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all flex items-center justify-center gap-1.5 ${
                mode === 'paste'
                  ? 'bg-white dark:bg-[#1E293B] text-[#2E31E8] dark:text-indigo-300 shadow-sm'
                  : 'text-[#64748B] dark:text-[#94A3B8] hover:text-[#0F172A] dark:hover:text-[#F8FAFC]'
              }`}
            >
              <FileText className="w-3.5 h-3.5" />
              <span>Paste description</span>
            </button>
          </div>

          {/* Repository Input */}
          <div className="mb-4">
            <label className="block text-xs font-semibold text-[#1E293B] dark:text-slate-200 mb-1">Repository</label>
            <input
              type="text"
              value={repository}
              onChange={(e) => setRepository(e.target.value)}
              placeholder="kubernetes/kubernetes"
              className="w-full bg-[#F3F4F6] dark:bg-[#1E293B] border border-[#E5E7EB] dark:border-[#334155] rounded-xl px-3.5 py-2 text-xs text-[#0F172A] dark:text-[#F8FAFC] focus:outline-none focus:ring-2 focus:ring-[#2E31E8] dark:focus:ring-[#4F46E5] focus:bg-white dark:focus:bg-[#1E293B] transition-all font-mono"
            />
          </div>

          {/* Main textarea / URL input */}
          <div className="mb-5">
            <label className="block text-xs font-semibold text-[#1E293B] dark:text-slate-200 mb-1">
              {mode === 'url' ? 'Issue URL' : 'Issue Title & Description'}
            </label>
            {mode === 'url' ? (
              <input
                type="url"
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder="https://github.com/kubernetes/kubernetes/issues/123456"
                className="w-full bg-[#F3F4F6] dark:bg-[#1E293B] border border-[#E5E7EB] dark:border-[#334155] rounded-xl px-3.5 py-2.5 text-xs text-[#0F172A] dark:text-[#F8FAFC] focus:outline-none focus:ring-2 focus:ring-[#2E31E8] dark:focus:ring-[#4F46E5] focus:bg-white dark:focus:bg-[#1E293B] transition-all font-mono"
              />
            ) : (
              <textarea
                rows={6}
                value={pasteInput}
                onChange={(e) => setPasteInput(e.target.value)}
                placeholder="Paste the issue URL, title, description, and error details..."
                className="w-full bg-[#F3F4F6] dark:bg-[#1E293B] border border-[#E5E7EB] dark:border-[#334155] rounded-xl p-3 text-xs text-[#0F172A] dark:text-[#F8FAFC] focus:outline-none focus:ring-2 focus:ring-[#2E31E8] dark:focus:ring-[#4F46E5] focus:bg-white dark:focus:bg-[#1E293B] transition-all resize-none leading-relaxed"
              />
            )}
          </div>

          <button
            onClick={handleAnalyze}
            disabled={!currentPayload.trim()}
            className="w-full bg-[#2E31E8] hover:bg-[#2326C4] disabled:opacity-50 disabled:pointer-events-none text-white font-semibold py-2.5 px-4 rounded-xl text-sm shadow-md shadow-indigo-600/25 transition-all flex items-center justify-center gap-2 mb-4"
          >
            <span>Analyze Issue</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          {/* Quick Scenario Chips */}
          <div className="pt-3 border-t border-[#F1F5F9] dark:border-[#1F2937]">
            <div className="text-[11px] font-semibold text-[#94A3B8] dark:text-slate-500 mb-1.5">Load Specific Scenario:</div>
            <div className="flex flex-wrap gap-1">
              {SAMPLE_ISSUES.map((s, idx) => (
                <button
                  key={s.id}
                  onClick={() => handleSelectSampleChip(idx)}
                  className={`px-2 py-0.5 rounded-lg text-[10px] font-medium border transition-all ${
                    currentSampleIndex === idx
                      ? 'bg-[#2E31E8] text-white border-[#2E31E8]'
                      : 'bg-gray-50 dark:bg-[#161F30] border-gray-200 dark:border-[#1F2937] text-gray-700 dark:text-slate-300 hover:border-indigo-300'
                  }`}
                >
                  {s.shortLabel}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right Card: Conversational Preview */}
        <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-6 shadow-card dark:shadow-dark-card flex flex-col justify-between min-h-[460px]">
          <div>
            <div className="flex items-center justify-between pb-3 mb-4 border-b border-[#F1F5F9] dark:border-[#1F2937]">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                <span className="text-xs font-bold uppercase tracking-wider text-[#64748B] dark:text-[#94A3B8]">Live Conversation Preview</span>
              </div>
              <span className="text-[11px] text-[#94A3B8] dark:text-slate-500">Session #2026-TRG</span>
            </div>

            {/* Bubble 1: You */}
            <div className="flex items-start gap-3 justify-end mb-4">
              <div className="max-w-[85%] bg-[#2E31E8] text-white rounded-2xl rounded-tr-sm p-4 text-xs leading-relaxed shadow-sm">
                <div className="text-[10px] font-bold uppercase tracking-wider text-indigo-200 mb-1 flex items-center gap-1 justify-end">
                  <span>You (Maintainer)</span>
                  <User className="w-3 h-3" />
                </div>
                <div className="font-mono break-all line-clamp-6">
                  {currentPayload.trim() || 'No issue input yet...'}
                </div>
              </div>
            </div>

            {/* Bubble 2: AI */}
            <div className="flex items-start gap-3 justify-start">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-[#2E31E8] to-[#6366F1] flex items-center justify-center text-white shrink-0 shadow-sm mt-1">
                <Bot className="w-4 h-4" />
              </div>
              <div className="max-w-[85%] bg-[#F3F4F6] dark:bg-[#161F30] border border-[#E5E7EB] dark:border-[#1F2937] text-[#1E293B] dark:text-slate-200 rounded-2xl rounded-tl-sm p-4 text-xs leading-relaxed shadow-sm">
                <div className="text-[10px] font-bold uppercase tracking-wider text-[#2E31E8] dark:text-indigo-400 mb-1">
                  Bug Triage AI
                </div>
                <p>
                  Thanks! I'm analyzing this issue now. I'll help you understand the problem, suggest possible causes, and recommend a team or next steps.
                </p>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-[#F1F5F9] dark:border-[#1F2937] mt-6 flex items-center justify-between text-[11px] text-[#94A3B8] dark:text-slate-500">
            <span className="flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-[#2E31E8] dark:text-indigo-400" />
              Multi-modal graph classification engine ready
            </span>
            <span>Target: {repository}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
