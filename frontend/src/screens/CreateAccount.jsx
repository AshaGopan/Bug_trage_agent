import React, { useState } from 'react';
import { Bot, ArrowRight, User, Mail, Lock, Sun, Moon } from 'lucide-react';

export default function CreateAccount({ onSignUp, onSwitchToSignIn, theme, onToggleTheme }) {
  const [fullName, setFullName] = useState('Alex Morgan');
  const [email, setEmail] = useState('maintainer@k8s.io');
  const [password, setPassword] = useState('password123');
  const [confirmPassword, setConfirmPassword] = useState('password123');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!fullName.trim() || !email.trim()) {
      setError('Please fill in your name and email address.');
      return;
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    setError('');
    onSignUp({ name: fullName.trim(), email: email.trim() });
  };

  return (
    <div className="relative z-10 min-h-[85vh] flex items-center justify-center p-4">
      {/* Floating Theme Toggle in top-right corner */}
      <div className="fixed top-5 right-5 z-20">
        <button
          onClick={onToggleTheme}
          title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
          className="w-10 h-10 rounded-xl border border-[#E5E7EB] dark:border-[#334155] bg-white dark:bg-[#111827] text-[#475569] dark:text-amber-400 hover:bg-gray-50 dark:hover:bg-[#1E293B] flex items-center justify-center shadow-sm transition-all"
        >
          {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5 text-indigo-600" />}
        </button>
      </div>

      <div className="w-full max-w-md bg-white dark:bg-[#111827] border border-[#E5E7EB] dark:border-[#1F2937] rounded-2xl p-8 shadow-elevated dark:shadow-dark-card transition-colors duration-200">
        {/* Brand Logo & Header */}
        <div className="text-center mb-6">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-[#2E31E8] to-[#6366F1] flex items-center justify-center text-white mx-auto mb-3 shadow-md shadow-indigo-500/25">
            <Bot className="w-6 h-6" />
          </div>
          <div className="text-xs font-bold uppercase tracking-wider text-[#2E31E8] dark:text-indigo-400 mb-1">Bug Triage AI</div>
          <h2 className="text-2xl font-bold text-[#0F172A] dark:text-[#F8FAFC] tracking-tight">Create your account</h2>
          <p className="text-sm text-[#64748B] dark:text-[#94A3B8] mt-1">Get started with smarter GitHub issue triage.</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 dark:bg-red-950/50 border border-red-100 dark:border-red-900/50 rounded-xl text-xs text-red-600 dark:text-red-400 font-medium">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-3.5">
          <div>
            <label className="block text-xs font-semibold text-[#1E293B] dark:text-slate-200 mb-1">Full name</label>
            <div className="relative">
              <User className="w-4 h-4 text-gray-400 dark:text-gray-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Alex Morgan"
                className="w-full bg-[#F3F4F6] dark:bg-[#1E293B] border border-[#E5E7EB] dark:border-[#334155] rounded-xl pl-10 pr-3.5 py-2 text-sm text-[#0F172A] dark:text-[#F8FAFC] placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#2E31E8] dark:focus:ring-[#4F46E5] focus:bg-white dark:focus:bg-[#1E293B] transition-all"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-[#1E293B] dark:text-slate-200 mb-1">Email address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-gray-400 dark:text-gray-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="alex@k8s.io"
                className="w-full bg-[#F3F4F6] dark:bg-[#1E293B] border border-[#E5E7EB] dark:border-[#334155] rounded-xl pl-10 pr-3.5 py-2 text-sm text-[#0F172A] dark:text-[#F8FAFC] placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#2E31E8] dark:focus:ring-[#4F46E5] focus:bg-white dark:focus:bg-[#1E293B] transition-all"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-[#1E293B] dark:text-slate-200 mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-gray-400 dark:text-gray-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-[#F3F4F6] dark:bg-[#1E293B] border border-[#E5E7EB] dark:border-[#334155] rounded-xl pl-10 pr-3.5 py-2 text-sm text-[#0F172A] dark:text-[#F8FAFC] placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#2E31E8] dark:focus:ring-[#4F46E5] focus:bg-white dark:focus:bg-[#1E293B] transition-all"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-[#1E293B] dark:text-slate-200 mb-1">Confirm password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-gray-400 dark:text-gray-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-[#F3F4F6] dark:bg-[#1E293B] border border-[#E5E7EB] dark:border-[#334155] rounded-xl pl-10 pr-3.5 py-2 text-sm text-[#0F172A] dark:text-[#F8FAFC] placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#2E31E8] dark:focus:ring-[#4F46E5] focus:bg-white dark:focus:bg-[#1E293B] transition-all"
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full mt-2 bg-[#2E31E8] hover:bg-[#2326C4] active:scale-[0.99] text-white font-semibold py-2.5 px-4 rounded-xl text-sm shadow-md shadow-indigo-600/20 transition-all flex items-center justify-center gap-2"
          >
            <span>Create Account</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        {/* Footer switch to sign in */}
        <div className="mt-6 pt-5 border-t border-[#F1F5F9] dark:border-[#1F2937] text-center">
          <p className="text-xs text-[#64748B] dark:text-[#94A3B8]">
            Already have an account?{' '}
            <button
              onClick={onSwitchToSignIn}
              className="text-[#2E31E8] dark:text-indigo-400 font-semibold hover:underline ml-1"
            >
              Sign In
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
