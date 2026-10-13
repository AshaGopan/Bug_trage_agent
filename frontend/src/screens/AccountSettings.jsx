import React, { useState } from 'react';
import { User, Mail, Github, LogOut, Check, Settings, Shield, Sun, Moon, Palette } from 'lucide-react';

export default function AccountSettings({ user, onUpdateUser, onSignOut, theme, onToggleTheme }) {
  const [name, setName] = useState(user?.name || 'Alex Morgan');
  const [email, setEmail] = useState(user?.email || 'maintainer@k8s.io');
  const [isGitHubConnected, setIsGitHubConnected] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  const handleSave = (e) => {
    e.preventDefault();
    onUpdateUser({ name, email });
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2500);
  };

  const toggleGitHub = () => {
    setIsGitHubConnected(!isGitHubConnected);
  };

  return (
    <div className="relative z-10 max-w-5xl mx-auto px-4 pb-16 transition-colors duration-200">
      {/* Header */}
      <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-6 shadow-card dark:shadow-dark-card mb-6">
        <h1 className="text-2xl font-bold text-[#0F172A] dark:text-[#F8FAFC] tracking-tight">
          Account Settings
        </h1>
        <p className="text-xs sm:text-sm text-[#64748B] dark:text-[#94A3B8] mt-1">
          Manage your maintainer profile, theme appearance, and connected integrations.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 items-start">
        {/* Sidebar Nav */}
        <div className="md:col-span-1 bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-4 shadow-card dark:shadow-dark-card space-y-1.5">
          <button className="w-full text-left px-3.5 py-2.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-100 dark:border-indigo-800/60 text-[#2E31E8] dark:text-indigo-300 font-semibold text-xs flex items-center gap-2">
            <Settings className="w-4 h-4" />
            <span>Account Settings</span>
          </button>

          <button
            onClick={onSignOut}
            className="w-full text-left px-3.5 py-2.5 rounded-xl text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/30 hover:border hover:border-rose-100 dark:hover:border-rose-900/40 font-semibold text-xs flex items-center gap-2 transition-colors"
          >
            <LogOut className="w-4 h-4" />
            <span>Sign Out</span>
          </button>
        </div>

        {/* Main Content Area */}
        <div className="md:col-span-3 space-y-6">
          {/* Appearance (Theme) Card */}
          <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-6 shadow-card dark:shadow-dark-card">
            <h2 className="text-base font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-1 flex items-center gap-2">
              <Palette className="w-4 h-4 text-[#2E31E8] dark:text-indigo-400" />
              <span>Appearance</span>
            </h2>
            <p className="text-xs text-[#64748B] dark:text-[#94A3B8] mb-5">
              Customize the visual theme of your triage workspace.
            </p>

            <div className="flex flex-wrap items-center gap-3">
              <button
                type="button"
                onClick={() => theme !== 'light' && onToggleTheme()}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold border transition-all ${
                  theme === 'light'
                    ? 'bg-indigo-50 border-[#2E31E8] text-[#2E31E8] shadow-sm'
                    : 'bg-white dark:bg-[#1E293B] border-gray-200 dark:border-[#334155] text-gray-700 dark:text-slate-300 hover:bg-gray-50 dark:hover:bg-[#283548]'
                }`}
              >
                <Sun className="w-4 h-4 text-amber-500" />
                <span>Light Mode</span>
                {theme === 'light' && <Check className="w-3.5 h-3.5 ml-1" />}
              </button>

              <button
                type="button"
                onClick={() => theme !== 'dark' && onToggleTheme()}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold border transition-all ${
                  theme === 'dark'
                    ? 'bg-indigo-950/60 border-indigo-500 text-indigo-300 shadow-sm'
                    : 'bg-white dark:bg-[#1E293B] border-gray-200 dark:border-[#334155] text-gray-700 dark:text-slate-300 hover:bg-gray-50 dark:hover:bg-[#283548]'
                }`}
              >
                <Moon className="w-4 h-4 text-indigo-400" />
                <span>Dark Mode</span>
                {theme === 'dark' && <Check className="w-3.5 h-3.5 ml-1" />}
              </button>
            </div>
          </div>

          {/* Profile Card */}
          <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-6 shadow-card dark:shadow-dark-card">
            <h2 className="text-base font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-1 flex items-center gap-2">
              <User className="w-4 h-4 text-[#2E31E8] dark:text-indigo-400" />
              <span>Profile</span>
            </h2>
            <p className="text-xs text-[#64748B] dark:text-[#94A3B8] mb-5">
              Update your maintainer details displayed across triage sessions.
            </p>

            <form onSubmit={handleSave} className="space-y-4 max-w-lg">
              <div>
                <label className="block text-xs font-semibold text-[#1E293B] dark:text-slate-200 mb-1">Full name</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-[#F3F4F6] dark:bg-[#1E293B] border border-[#E5E7EB] dark:border-[#334155] rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-[#0F172A] dark:text-[#F8FAFC] focus:outline-none focus:ring-2 focus:ring-[#2E31E8] dark:focus:ring-[#4F46E5] focus:bg-white dark:focus:bg-[#1E293B] transition-all"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-[#1E293B] dark:text-slate-200 mb-1">Email address</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-[#F3F4F6] dark:bg-[#1E293B] border border-[#E5E7EB] dark:border-[#334155] rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-[#0F172A] dark:text-[#F8FAFC] focus:outline-none focus:ring-2 focus:ring-[#2E31E8] dark:focus:ring-[#4F46E5] focus:bg-white dark:focus:bg-[#1E293B] transition-all"
                />
              </div>

              <div className="pt-2 flex items-center gap-3">
                <button
                  type="submit"
                  className="bg-[#2E31E8] hover:bg-[#2326C4] text-white font-semibold px-5 py-2 rounded-xl text-xs sm:text-sm shadow-md shadow-indigo-600/25 transition-all flex items-center gap-1.5"
                >
                  <Check className="w-4 h-4" />
                  <span>Save Changes</span>
                </button>

                {savedSuccess && (
                  <span className="text-xs text-emerald-600 dark:text-emerald-400 font-semibold animate-fade-in">
                    ✓ Changes saved successfully!
                  </span>
                )}
              </div>
            </form>
          </div>

          {/* GitHub Connection Card */}
          <div className="bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-6 shadow-card dark:shadow-dark-card">
            <h2 className="text-base font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-1 flex items-center gap-2">
              <Github className="w-4 h-4 text-[#0F172A] dark:text-white" />
              <span>GitHub Connection</span>
            </h2>
            <p className="text-xs text-[#64748B] dark:text-[#94A3B8] mb-5">
              Connect your GitHub account to access supported repository features.
            </p>

            <div className="flex flex-wrap items-center justify-between gap-4 p-4 bg-[#F8F9FC] dark:bg-[#161F30] border border-[#E5E7EB] dark:border-[#1F2937] rounded-xl max-w-lg">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-full bg-white dark:bg-[#1E293B] border border-gray-200 dark:border-[#334155] flex items-center justify-center text-gray-700 dark:text-gray-300 shadow-sm">
                  <Github className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-xs font-semibold text-[#0F172A] dark:text-[#F8FAFC]">GitHub Integration</div>
                  <div className="mt-0.5">
                    {isGitHubConnected ? (
                      <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-700 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800/60 px-2 py-0.5 rounded-full">
                        Connected as @k8s-maintainer
                      </span>
                    ) : (
                      <span className="text-[10px] font-bold uppercase tracking-wider text-gray-600 dark:text-slate-400 bg-gray-200 dark:bg-[#1E293B] border border-gray-300 dark:border-[#334155] px-2 py-0.5 rounded-full">
                        Not connected
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <button
                type="button"
                onClick={toggleGitHub}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold border transition-all ${
                  isGitHubConnected
                    ? 'bg-white dark:bg-[#1E293B] border-gray-300 dark:border-[#334155] text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-[#283548]'
                    : 'bg-[#0F172A] hover:bg-gray-800 dark:bg-[#2E31E8] dark:hover:bg-[#2326C4] text-white border-transparent shadow-sm'
                }`}
              >
                {isGitHubConnected ? 'Disconnect' : 'Connect GitHub'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
