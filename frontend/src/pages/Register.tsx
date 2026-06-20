import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import {
  Mail, Lock, Eye, EyeOff, User, Briefcase, ArrowRight,
  AlertCircle, Sparkles, CheckCircle2
} from 'lucide-react';

function getPasswordStrength(pw: string): { label: string; color: string; width: string } {
  if (pw.length === 0) return { label: '', color: '', width: 'w-0' };
  if (pw.length < 6) return { label: 'Too short', color: 'bg-rose-500', width: 'w-1/4' };
  if (pw.length < 8) return { label: 'Weak', color: 'bg-orange-400', width: 'w-2/4' };
  const hasUpper = /[A-Z]/.test(pw);
  const hasNum = /[0-9]/.test(pw);
  const hasSpecial = /[^A-Za-z0-9]/.test(pw);
  const score = [hasUpper, hasNum, hasSpecial].filter(Boolean).length;
  if (score >= 2) return { label: 'Strong', color: 'bg-emerald-500', width: 'w-full' };
  return { label: 'Fair', color: 'bg-yellow-400', width: 'w-3/4' };
}

export default function Register() {
  const navigate = useNavigate();
  const { register, isLoading, error, clearError } = useAuthStore();

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const strength = getPasswordStrength(password);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    try {
      await register(name, email, password);
      navigate('/dashboard');
    } catch {
      // error set in store
    }
  };

  const perks = [
    'Apply to 50 jobs/month on Free',
    'AI resume tailoring for every listing',
    'Upgrade to Pro anytime for unlimited',
  ];

  return (
    <div className="min-h-screen w-full flex items-center justify-center relative overflow-hidden bg-slate-950">
      {/* Background blobs */}
      <div className="absolute top-[-15%] right-[-10%] w-[600px] h-[600px] rounded-full bg-violet-700/12 blur-[140px] pointer-events-none animate-pulse-slow" />
      <div className="absolute bottom-[-10%] left-[-8%] w-[500px] h-[500px] rounded-full bg-fuchsia-800/10 blur-[120px] pointer-events-none" />
      <div className="absolute top-[50%] right-[40%] w-[350px] h-[350px] rounded-full bg-purple-600/8 blur-[100px] pointer-events-none" />

      <div className="w-full max-w-5xl mx-auto px-4 py-12 flex items-stretch gap-0 z-10">
        {/* Right panel — form (shown first on desktop to mirror login layout) */}
        <div className="w-full lg:w-[440px] flex-shrink-0 glass-card rounded-3xl lg:rounded-r-none lg:rounded-l-3xl border border-white/5 p-8 sm:p-10 flex flex-col justify-center">
          {/* Mobile logo */}
          <div className="lg:hidden flex items-center gap-2 mb-8">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-violet-600 to-purple-500 flex items-center justify-center">
              <Briefcase className="w-4 h-4 text-white" />
            </div>
            <span className="text-xl font-bold text-white">JobHunt <span className="text-purple-400">AI</span></span>
          </div>

          <h1 className="text-2xl font-bold text-white mb-1.5">Create your account</h1>
          <p className="text-slate-400 text-sm mb-8">Free forever. No credit card required.</p>

          {/* Error */}
          {error && (
            <div className="flex items-start gap-2.5 p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/25 text-rose-400 text-sm mb-6">
              <AlertCircle className="w-4 h-4 mt-0.5 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Full Name */}
            <div className="space-y-1.5">
              <label htmlFor="name" className="block text-xs font-medium text-slate-400 uppercase tracking-wider">
                Full Name
              </label>
              <div className="relative">
                <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
                <input
                  id="name"
                  type="text"
                  autoComplete="name"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Jane Smith"
                  className="glass-input w-full pl-10 pr-4 py-3 rounded-xl text-sm text-white placeholder-slate-600 focus:ring-0"
                />
              </div>
            </div>

            {/* Email */}
            <div className="space-y-1.5">
              <label htmlFor="reg-email" className="block text-xs font-medium text-slate-400 uppercase tracking-wider">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
                <input
                  id="reg-email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  className="glass-input w-full pl-10 pr-4 py-3 rounded-xl text-sm text-white placeholder-slate-600 focus:ring-0"
                />
              </div>
            </div>

            {/* Password */}
            <div className="space-y-1.5">
              <label htmlFor="reg-password" className="block text-xs font-medium text-slate-400 uppercase tracking-wider">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
                <input
                  id="reg-password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="new-password"
                  required
                  minLength={6}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Create a strong password"
                  className="glass-input w-full pl-10 pr-11 py-3 rounded-xl text-sm text-white placeholder-slate-600 focus:ring-0"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>

              {/* Strength bar */}
              {password.length > 0 && (
                <div className="pt-1 space-y-1">
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className={`h-full rounded-full transition-all duration-500 ${strength.color} ${strength.width}`} />
                  </div>
                  <p className="text-xs text-slate-500">
                    Strength: <span className={strength.label === 'Strong' ? 'text-emerald-400' : 'text-slate-400'}>{strength.label}</span>
                  </p>
                </div>
              )}
            </div>

            {/* Submit */}
            <button
              id="register-submit"
              type="submit"
              disabled={isLoading}
              className="w-full flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 shadow-lg shadow-purple-900/30 hover:shadow-purple-900/50 transition-all duration-300 disabled:opacity-60 disabled:cursor-not-allowed group mt-2"
            >
              {isLoading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Creating account…</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Create Free Account</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                </>
              )}
            </button>

            <p className="text-xs text-slate-600 text-center">
              By creating an account you agree to our{' '}
              <a href="#" className="text-slate-500 hover:text-slate-400 transition-colors underline">Terms</a> &amp;{' '}
              <a href="#" className="text-slate-500 hover:text-slate-400 transition-colors underline">Privacy Policy</a>
            </p>
          </form>

          <p className="text-sm text-slate-500 text-center mt-8">
            Already have an account?{' '}
            <Link to="/login" className="text-purple-400 hover:text-purple-300 font-medium transition-colors">
              Sign in
            </Link>
          </p>
        </div>

        {/* Left panel — benefits */}
        <div className="hidden lg:flex flex-col justify-between flex-1 bg-gradient-to-br from-slate-900/60 via-purple-900/15 to-violet-900/25 rounded-r-3xl border border-l-0 border-white/5 p-10 backdrop-blur-sm relative overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_right,rgba(124,58,237,0.12),transparent_70%)] pointer-events-none" />

          {/* Logo */}
          <div className="flex items-center gap-3 z-10">
            <div className="w-11 h-11 rounded-xl bg-gradient-to-tr from-violet-600 to-purple-500 flex items-center justify-center shadow-lg shadow-purple-900/40">
              <Briefcase className="w-5 h-5 text-white" />
            </div>
            <span className="text-2xl font-bold text-white tracking-tight">
              JobHunt <span className="text-purple-400 font-extrabold">AI</span>
            </span>
          </div>

          {/* Main text */}
          <div className="z-10 space-y-5">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-medium text-purple-300">
              <Sparkles className="w-3.5 h-3.5" />
              Free plan — no credit card
            </div>
            <h2 className="text-3xl font-bold text-white leading-snug">
              Start your job search
              <span className="block bg-gradient-to-r from-violet-400 to-fuchsia-400 bg-clip-text text-transparent">
                in under 2 minutes
              </span>
            </h2>
            <p className="text-slate-400 text-sm leading-relaxed max-w-xs">
              Join thousands of professionals who automated their job hunt and landed roles 3× faster.
            </p>

            <ul className="space-y-3 pt-2">
              {perks.map((perk) => (
                <li key={perk} className="flex items-center gap-3 text-sm text-slate-300">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                  {perk}
                </li>
              ))}
            </ul>
          </div>

          {/* Stats bar */}
          <div className="grid grid-cols-3 gap-3 z-10">
            {[
              { value: '12k+', label: 'Users' },
              { value: '95%', label: 'ATS Pass Rate' },
              { value: '3.2×', label: 'Faster Hiring' },
            ].map(({ value, label }) => (
              <div key={label} className="glass rounded-xl p-3 text-center border border-white/5">
                <p className="text-xl font-bold bg-gradient-to-r from-violet-400 to-purple-400 bg-clip-text text-transparent">{value}</p>
                <p className="text-xs text-slate-500 mt-0.5">{label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
