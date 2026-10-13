import React, { useState } from 'react';
import { ArrowRight, Sparkles, Search, Users, MessageSquareText, Columns2, RefreshCw } from 'lucide-react';
import { SAMPLE_ISSUES, getNextSample, getSavedSampleIndex, getSampleByIndex } from '../services/sampleIssues';

export default function WorkspaceLanding({ onStartAnalysis, onOpenSplitView }) {
  const [inputText, setInputText] = useState('');
  const [currentSampleIndex, setCurrentSampleIndex] = useState(null);

  const handleAnalyze = () => {
    if (inputText.trim()) {
      onStartAnalysis(inputText.trim());
    }
  };

  const handleTrySample = () => {
    const { sample, nextIndex } = getNextSample(currentSampleIndex);
    setCurrentSampleIndex(nextIndex);
    setInputText(sample.text);
  };

  const handleSelectSampleChip = (idx) => {
    const { sample } = getSampleByIndex(idx);
    setCurrentSampleIndex(idx);
    setInputText(sample.text);
  };

  const currentSample = currentSampleIndex !== null ? SAMPLE_ISSUES[currentSampleIndex] : null;

  return (
    <div className="relative z-10 max-w-4xl mx-auto px-4 pb-16 transition-colors duration-200">
      {/* Hero Header */}
      <div className="text-center pt-6 pb-8">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-100 dark:border-indigo-800/60 text-[#2E31E8] dark:text-indigo-300 text-xs font-semibold mb-4">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Inductive GraphSAGE + Multi-Modal Routing</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-[#0F172A] dark:text-[#F8FAFC] tracking-tight mb-3">
          What issue are we solving today?
        </h1>
        <p className="text-sm sm:text-base text-[#64748B] dark:text-[#94A3B8] max-w-2xl mx-auto leading-relaxed">
          Paste a GitHub issue and let AI help you understand, classify, and triage it.
        </p>
      </div>

      {/* Main Input Card */}
      <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-6 sm:p-7 shadow-card dark:shadow-dark-card mb-8 transition-all hover:shadow-elevated">
        <div className="flex items-center justify-between mb-2">
          <label className="block text-xs font-bold uppercase tracking-wider text-[#1E293B] dark:text-slate-200">
            GitHub issue URL or issue description
          </label>
          <button
            onClick={onOpenSplitView}
            className="text-xs font-semibold text-[#2E31E8] dark:text-indigo-400 hover:underline flex items-center gap-1"
          >
            <Columns2 className="w-3.5 h-3.5" />
            <span>Open Split-View Session</span>
          </button>
        </div>

        <textarea
          rows={5}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Paste a GitHub issue link or describe the problem..."
          className="w-full bg-[#F3F4F6] dark:bg-[#1E293B] border border-[#E5E7EB] dark:border-[#334155] rounded-xl p-4 text-sm text-[#0F172A] dark:text-[#F8FAFC] placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#2E31E8] dark:focus:ring-[#4F46E5] focus:bg-white dark:focus:bg-[#1E293B] transition-all resize-none leading-relaxed"
        />

        {/* Action Controls & Sample Badges */}
        <div className="mt-4 flex flex-wrap items-center justify-between gap-3 pt-1">
          <div className="flex flex-wrap items-center gap-2.5">
            <button
              onClick={handleAnalyze}
              disabled={!inputText.trim()}
              className="bg-[#2E31E8] hover:bg-[#2326C4] disabled:opacity-50 disabled:pointer-events-none text-white font-semibold px-5 py-2.5 rounded-xl text-sm shadow-md shadow-indigo-600/25 transition-all flex items-center gap-2"
            >
              <span>Analyze Issue</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            {/* Try a sample issue button (cycles through 8 pool) */}
            <button
              type="button"
              onClick={handleTrySample}
              className="bg-white dark:bg-[#1E293B] hover:bg-gray-50 dark:hover:bg-[#283548] border border-[#E5E7EB] dark:border-[#334155] text-[#334155] dark:text-slate-200 font-semibold px-4 py-2.5 rounded-xl text-sm shadow-sm transition-all flex items-center gap-1.5 group"
            >
              <RefreshCw className="w-3.5 h-3.5 text-[#2E31E8] dark:text-indigo-400 group-hover:rotate-180 transition-transform duration-300" />
              <span>Try a sample issue</span>
            </button>
          </div>

          {/* Indicator pill showing currently loaded sample */}
          {currentSample && (
            <div className="flex items-center gap-1.5 text-xs bg-indigo-50 dark:bg-indigo-950/60 text-[#2E31E8] dark:text-indigo-300 border border-indigo-100 dark:border-indigo-800/60 px-3 py-1.5 rounded-xl animate-fade-in">
              <span className="font-bold">Sample {currentSampleIndex + 1}/8:</span>
              <span className="font-semibold">{currentSample.tag}</span>
            </div>
          )}
        </div>

        {/* Quick Sample Selector Chips */}
        <div className="mt-4 pt-4 border-t border-[#F1F5F9] dark:border-[#1F2937] flex flex-wrap items-center gap-1.5 text-xs text-[#64748B] dark:text-slate-400">
          <span className="text-[11px] font-semibold text-[#94A3B8] dark:text-slate-500 mr-1">Quick Scenarios:</span>
          {SAMPLE_ISSUES.map((s, idx) => (
            <button
              key={s.id}
              onClick={() => handleSelectSampleChip(idx)}
              className={`px-2.5 py-1 rounded-lg text-[11px] font-medium border transition-all ${
                currentSampleIndex === idx
                  ? 'bg-[#2E31E8] text-white border-[#2E31E8] shadow-sm'
                  : 'bg-gray-50 dark:bg-[#161F30] border-gray-200 dark:border-[#1F2937] text-gray-700 dark:text-slate-300 hover:bg-white dark:hover:bg-[#1E293B] hover:border-indigo-200'
              }`}
            >
              {s.shortLabel}
            </button>
          ))}
        </div>
      </div>

      {/* 3 Bottom Feature Cards with Soft Purple Circular Icons */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Feature 1 */}
        <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-5 shadow-card dark:shadow-dark-card hover:border-gray-300 dark:hover:border-slate-700 transition-all flex flex-col items-start">
          <div className="w-11 h-11 rounded-full bg-[#EEF2FF] dark:bg-indigo-950/70 text-[#2E31E8] dark:text-indigo-300 flex items-center justify-center mb-3.5 shadow-sm border border-transparent dark:border-indigo-800/40">
            <Search className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-1.5">Issue Analysis</h3>
          <p className="text-xs text-[#64748B] dark:text-[#94A3B8] leading-relaxed">
            Automatic diagnostic completeness checks for reproduction steps, error logs, and environment configurations.
          </p>
        </div>

        {/* Feature 2 */}
        <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-5 shadow-card dark:shadow-dark-card hover:border-gray-300 dark:hover:border-slate-700 transition-all flex flex-col items-start">
          <div className="w-11 h-11 rounded-full bg-[#EEF2FF] dark:bg-indigo-950/70 text-[#2E31E8] dark:text-indigo-300 flex items-center justify-center mb-3.5 shadow-sm border border-transparent dark:border-indigo-800/40">
            <Users className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-1.5">Team Recommendation</h3>
          <p className="text-xs text-[#64748B] dark:text-[#94A3B8] leading-relaxed">
            Multi-modal routing via MiniLM embeddings and cold-start GraphSAGE neighbor aggregation across 7 SIG teams.
          </p>
        </div>

        {/* Feature 3 */}
        <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-5 shadow-card dark:shadow-dark-card hover:border-gray-300 dark:hover:border-slate-700 transition-all flex flex-col items-start">
          <div className="w-11 h-11 rounded-full bg-[#EEF2FF] dark:bg-indigo-950/70 text-[#2E31E8] dark:text-indigo-300 flex items-center justify-center mb-3.5 shadow-sm border border-transparent dark:border-indigo-800/40">
            <MessageSquareText className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-1.5">Suggested Response</h3>
          <p className="text-xs text-[#64748B] dark:text-[#94A3B8] leading-relaxed">
            Generates polished maintainer draft replies with missing diagnostic checklists and official GitHub labels.
          </p>
        </div>
      </div>
    </div>
  );
}
