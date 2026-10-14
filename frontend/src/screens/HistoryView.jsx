import React, { useState, useEffect } from 'react';
import { Search, ExternalLink, ArrowRight, Bug, Calendar, FolderGit2, Users } from 'lucide-react';
import { getHistory } from '../services/historyStorage';

export default function HistoryView({ onViewResult }) {
  const [historyItems, setHistoryItems] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    setHistoryItems(getHistory());
  }, []);

  const filteredItems = historyItems.filter((item) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    const titleMatch = (item.title || '').toLowerCase().includes(q);
    const repoMatch = (item.repository || '').toLowerCase().includes(q);
    const teamMatch = (item.suggestedTeam || '').toLowerCase().includes(q);
    return titleMatch || repoMatch || teamMatch;
  });

  return (
    <div className="relative z-10 max-w-5xl mx-auto px-4 pb-16 transition-colors duration-200">
      {/* Header */}
      <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-6 shadow-card dark:shadow-dark-card mb-6">
        <h1 className="text-2xl font-bold text-[#0F172A] dark:text-[#F8FAFC] tracking-tight">
          Recent Issues
        </h1>
        <p className="text-xs sm:text-sm text-[#64748B] dark:text-[#94A3B8] mt-1">
          Return to issues you analyzed earlier.
        </p>

        {/* Search Bar */}
        <div className="mt-4 relative">
          <Search className="w-4 h-4 text-gray-400 dark:text-gray-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by issue title or repository..."
            className="w-full bg-[#F3F4F6] dark:bg-[#1E293B] border border-[#E5E7EB] dark:border-[#334155] rounded-xl pl-10 pr-4 py-2.5 text-xs sm:text-sm text-[#0F172A] dark:text-[#F8FAFC] placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#2E31E8] dark:focus:ring-[#4F46E5] focus:bg-white dark:focus:bg-[#1E293B] transition-all"
          />
        </div>
      </div>

      {/* History Content */}
      {filteredItems.length === 0 ? (
        /* Empty State Card */
        <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-12 text-center shadow-card dark:shadow-dark-card max-w-md mx-auto my-8">
          <div className="w-14 h-14 rounded-full bg-gray-100 dark:bg-[#161F30] text-gray-400 dark:text-slate-500 flex items-center justify-center mx-auto mb-4 border border-transparent dark:border-[#1F2937]">
            <Bug className="w-7 h-7" />
          </div>
          <h3 className="text-lg font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-1">No issues analyzed yet</h3>
          <p className="text-xs sm:text-sm text-[#64748B] dark:text-[#94A3B8] leading-relaxed">
            Your analyzed issues will appear here.
          </p>
        </div>
      ) : (
        /* Table of Issues */
        <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl shadow-card dark:shadow-dark-card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-[#F1F5F9] dark:border-[#1F2937] bg-[#F8F9FC] dark:bg-[#161F30] text-[11px] font-bold uppercase tracking-wider text-[#64748B] dark:text-[#94A3B8]">
                  <th className="py-3.5 px-5">Issue</th>
                  <th className="py-3.5 px-4">Repository</th>
                  <th className="py-3.5 px-4">Suggested Team</th>
                  <th className="py-3.5 px-4">Date Analyzed</th>
                  <th className="py-3.5 px-5 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#F1F5F9] dark:divide-[#1F2937] text-xs">
                {filteredItems.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50/80 dark:hover:bg-[#161F30]/80 transition-colors">
                    {/* Issue Title & ID */}
                    <td className="py-4 px-5 max-w-xs sm:max-w-md">
                      <div className="font-semibold text-[#0F172A] dark:text-[#F8FAFC] line-clamp-2">
                        {item.title}
                      </div>
                      {item.url && (
                        <a
                          href={item.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-[11px] text-[#2E31E8] dark:text-indigo-400 hover:underline inline-flex items-center gap-1 mt-0.5"
                        >
                          <span>{item.id}</span>
                          <ExternalLink className="w-2.5 h-2.5" />
                        </a>
                      )}
                    </td>

                    {/* Repository */}
                    <td className="py-4 px-4 whitespace-nowrap">
                      <span className="font-mono text-[11px] bg-gray-100 dark:bg-[#1E293B] text-[#475569] dark:text-slate-300 px-2 py-0.5 rounded border border-gray-200 dark:border-[#334155]">
                        {item.repository}
                      </span>
                    </td>

                    {/* Suggested Team */}
                    <td className="py-4 px-4 whitespace-nowrap">
                      <span className="font-semibold text-[#2E31E8] dark:text-indigo-300 bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-100 dark:border-indigo-800/60 px-2.5 py-1 rounded-full text-[11px] inline-flex items-center gap-1">
                        {item.suggestedTeam}
                      </span>
                    </td>

                    {/* Date Analyzed */}
                    <td className="py-4 px-4 whitespace-nowrap text-[#64748B] dark:text-slate-400 text-[11px]">
                      {item.dateAnalyzed || 'Recently'}
                    </td>

                    {/* Action */}
                    <td className="py-4 px-5 text-right whitespace-nowrap">
                      <button
                        onClick={() => onViewResult(item)}
                        className="bg-white dark:bg-[#1E293B] hover:bg-indigo-50 dark:hover:bg-indigo-950/50 border border-[#E5E7EB] dark:border-[#334155] hover:border-indigo-200 dark:hover:border-indigo-800 text-[#2E31E8] dark:text-indigo-300 font-semibold px-3 py-1.5 rounded-xl text-xs shadow-sm transition-all inline-flex items-center gap-1"
                      >
                        <span>View Results</span>
                        <ArrowRight className="w-3 h-3" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
