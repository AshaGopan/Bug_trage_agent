import React from 'react';
import { Bot, Layers, History, User, Settings, LogOut, Sparkles, Sun, Moon } from 'lucide-react';

export default function Navbar({ currentScreen, onNavigate, user, onSignOut, theme, onToggleTheme }) {
  const isWorkspace = ['workspace_landing', 'split_view', 'analyzing', 'results', 'suggested_response'].includes(currentScreen);
  const isHistory = currentScreen === 'history';
  const isSettings = currentScreen === 'settings';
  const isStates = currentScreen === 'component_states';

  return (
    <header className="relative z-10 w-full max-w-5xl mx-auto pt-4 pb-6 px-4">
      <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl px-5 py-3 shadow-sm dark:shadow-dark-card flex items-center justify-between transition-colors duration-200">
        {/* Brand Logo & Name */}
        <button
          onClick={() => onNavigate('workspace_landing')}
          className="flex items-center gap-3 text-left focus:outline-none group"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#2E31E8] to-[#6366F1] flex items-center justify-center text-white shadow-md shadow-indigo-500/20 group-hover:scale-105 transition-transform">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-base text-[#0F172A] dark:text-[#F8FAFC] tracking-tight">Bug Triage AI</span>
              <span className="text-[10px] font-semibold bg-indigo-50 dark:bg-indigo-950/60 text-[#2E31E8] dark:text-indigo-300 border border-indigo-100 dark:border-indigo-800/60 px-1.5 py-0.5 rounded-full">
                K8s Edition
              </span>
            </div>
            <p className="text-xs text-[#64748B] dark:text-[#94A3B8] font-medium -mt-0.5">Multi-Modal Issue Intelligence</p>
          </div>
        </button>

        {/* Center Navigation Tabs */}
        <nav className="flex items-center gap-1.5 bg-[#F8F9FC] dark:bg-[#161F30] p-1 rounded-xl border border-[#E5E7EB] dark:border-[#1F2937] transition-colors duration-200">
          <button
            onClick={() => onNavigate('workspace_landing')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
              isWorkspace
                ? 'bg-[#2E31E8] text-white shadow-sm'
                : 'text-[#475569] dark:text-[#94A3B8] hover:text-[#0F172A] dark:hover:text-[#F8FAFC] hover:bg-white/80 dark:hover:bg-[#1E293B]'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5" />
            Workspace
          </button>

          <button
            onClick={() => onNavigate('history')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
              isHistory
                ? 'bg-[#2E31E8] text-white shadow-sm'
                : 'text-[#475569] dark:text-[#94A3B8] hover:text-[#0F172A] dark:hover:text-[#F8FAFC] hover:bg-white/80 dark:hover:bg-[#1E293B]'
            }`}
          >
            <History className="w-3.5 h-3.5" />
            History
          </button>

          <button
            onClick={() => onNavigate('component_states')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
              isStates
                ? 'bg-[#2E31E8] text-white shadow-sm'
                : 'text-[#475569] dark:text-[#94A3B8] hover:text-[#0F172A] dark:hover:text-[#F8FAFC] hover:bg-white/80 dark:hover:bg-[#1E293B]'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            States (UI)
          </button>
        </nav>

        {/* Right Section: Theme Toggle & Profile */}
        <div className="flex items-center gap-2.5">
          {/* Theme Toggle Button */}
          <button
            onClick={onToggleTheme}
            title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            className="w-9 h-9 rounded-xl border border-[#E5E7EB] dark:border-[#334155] bg-white dark:bg-[#1E293B] text-[#475569] dark:text-amber-400 hover:bg-gray-50 dark:hover:bg-[#283548] flex items-center justify-center transition-all shadow-sm group"
          >
            {theme === 'dark' ? (
              <Sun className="w-4 h-4 transition-transform group-hover:rotate-45" />
            ) : (
              <Moon className="w-4 h-4 text-indigo-600 transition-transform group-hover:-rotate-12" />
            )}
          </button>

          {/* Profile / Account Settings */}
          <button
            onClick={() => onNavigate('settings')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-xl border transition-all text-left ${
              isSettings
                ? 'border-[#2E31E8] bg-indigo-50/50 dark:bg-indigo-950/40 text-[#2E31E8] dark:text-indigo-300'
                : 'border-[#E5E7EB] dark:border-[#334155] bg-white dark:bg-[#1E293B] text-[#334155] dark:text-[#F8FAFC] hover:bg-gray-50 dark:hover:bg-[#283548]'
            }`}
          >
            <div className="w-7 h-7 rounded-full bg-indigo-100 dark:bg-indigo-950 text-[#2E31E8] dark:text-indigo-300 font-bold text-xs flex items-center justify-center border border-indigo-200 dark:border-indigo-800">
              {user?.name?.[0] || 'A'}
            </div>
            <div className="hidden sm:block text-xs">
              <div className="font-semibold text-[#0F172A] dark:text-[#F8FAFC] leading-tight">{user?.name || 'Alex Morgan'}</div>
              <div className="text-[10px] text-emerald-600 dark:text-emerald-400 font-medium">● Maintainer</div>
            </div>
            <Settings className="w-3.5 h-3.5 text-gray-400 dark:text-gray-500 ml-1" />
          </button>
        </div>
      </div>
    </header>
  );
}
