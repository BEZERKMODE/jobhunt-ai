import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import {
  Mail, Lock, Eye, EyeOff, Briefcase, ArrowRight,
  AlertCircle, Sparkles, Zap, ShieldCheck, TrendingUp
} from 'lucide-react';

export default function Login() {
  const navigate = useNavigate();
  const { login, isLoading, error, clearError } = useAuthStore();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch {
      // error already set in store
    }
  };

  const features = [
    { icon: Zap, text: 'Auto-apply to 100s of jobs overnight' },
    { icon: ShieldCheck, text: 'ATS-optimised resumes for every listing' },
    { icon: TrendingUp, text: 'Real-time application match scoring' },
  ];

  return (
    <div className="min-h-screen w-full flex items-center justify-center relative overflow-hidden bg-slate-950">
      {/* Layered animated blobs */}
      <div className="absolute top-[-20%] left-[-10%] w-[500px] h-[500px] rounded-full bg-violet-700/15 blur-[130px] animate-pulse-slow pointer-events-none" />
      <div className="absolute bottom-[-15%] right-[-5%] w-[600px] h-[600px] rounded-full bg-purple-800/10 blur-[150px] pointer-events-none" />
      <div className="absolute top-[40%] left-[45%] w-[400px] h-[400px] rounded-full bg-fuchsia-700/8 blur-[120px] pointer-events-none" />

      <div className="w-full max-w-5xl mx-auto px-4 py-12 flex items-stretch gap-0 z-10">
        {/* Left panel — branding */}
        <div className="hidden lg:flex flex-col justify-between flex-1 bg-gradient-to-br from-violet-700/30 via-purple-800/20 to-slate-900/40 rounded-l-3xl border border-r-0 border-white/5 p-10 backdrop-blur-sm relative overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_left,rgba(124,58,237,0.15),transparent_70%)] pointer-events-none" />

          {/* Logo */}
          <div className="flex items-center gap-3 z-10">
            <div className="w-11 h-11 rounded-xl bg-gradient-to-tr from-violet-600 to-purple-500 flex items-center justify-center shadow-lg shadow-purple-900/40">
              <Briefcase className="w-5 h-5 text-white" />
            </div>
            <span className="text-2xl font-bold text-white tracking-tight">
              JobHunt <span className="text-purple-400 font-extrabold">AI</span>
            </span>
          </div>

          {/* Headline */}
          <div className="z-10 space-y-5">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-medium text-purple-300">
              <Sparkles className="w-3.5 h-3.5" />
              AI-Powered Job Hunting
            </div>
            <h2 className="text-3xl font-bold text-white leading-snug">
              Apply smarter,<br />
              <span className="bg-gradient-to-r from-violet-400 to-fuchsia-400 bg-clip-text text-transparent">
                not harder
              </span>
            </h2>
            <p className="text-slate-400 text-sm leading-relaxed max-w-xs">
              Let our AI engine handle the repetitive work of job applications while you focus on what matters.
            </p>

            {/* Feature list */}
            <ul className="space-y-3 pt-2">
              {features.map(({ icon: Icon, text }) => (
                <li key={text} className="flex items-center gap-3 text-sm text-slate-300">
                  <div className="w-7 h-7 rounded-lg bg-violet-500/15 border border-violet-500/25 flex items-center justify-center text-violet-400 flex-shrink-0">
                    <Icon className="w-3.5 h-3.5" />
                  </div>
                  {text}
                </li>
              ))}
            </ul>
          </div>

          {/* Testimonial / social proof */}
          <div className="glass rounded-2xl p-4 z-10 border border-white/5">
            <p className="text-sm text-slate-300 italic leading-relaxed">
              "JobHunt AI sent 240 tailored applications in my first week. I had 18 interviews scheduled by Friday."
            </p>
            <p className="text-xs text-slate-500 mt-2 font-medium">— Priya M., Senior Software Engineer</p>
          </div>
        </div>

        {/* Right panel — form */}
        <div className="w-full lg:w-[420px] flex-shrink-0 glass-card rounded-3xl lg:rounded-l-none lg:rounded-r-3xl border border-white/5 p-8 sm:p-10 flex flex-col justify-center">
          {/* Mobile logo */}
          <div className="lg:hidden flex items-center gap-2 mb-8">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-violet-600 to-purple-500 flex items-center justify-center">
              <Briefcase className="w-4 h-4 text-white" />
            </div>
            <span className="text-xl font-bold text-white">JobHunt <span className="text-purple-400">AI</span></span>
          </div>

          <h1 className="text-2xl font-bold text-white mb-1.5">Welcome back</h1>
          <p className="text-slate-400 text-sm mb-8">Sign in to your account to continue</p>

          {/* Error */}
          {error && (
            <div className="flex items-start gap-2.5 p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/25 text-rose-400 text-sm mb-6">
              <AlertCircle className="w-4 h-4 mt-0.5 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Email */}
            <div className="space-y-1.5">
              <label htmlFor="email" className="block text-xs font-medium text-slate-400 uppercase tracking-wider">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
                <input
                  id="email"
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
              <div className="flex items-center justify-between">
                <label htmlFor="password" className="block text-xs font-medium text-slate-400 uppercase tracking-wider">
                  Password
                </label>
                <Link to="/forgot-password" className="text-xs text-purple-400 hover:text-purple-300 transition-colors">
                  Forgot password?
                </Link>
              </div>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
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
            </div>

            {/* Submit */}
            <button
              id="login-submit"
              type="submit"
              disabled={isLoading}
              className="w-full flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 shadow-lg shadow-purple-900/30 hover:shadow-purple-900/50 transition-all duration-300 disabled:opacity-60 disabled:cursor-not-allowed group"
            >
              {isLoading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Signing in…</span>
                </>
              ) : (
                <>
                  <span>Sign In</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                </>
              )}
            </button>
          </form>

          <p className="text-sm text-slate-500 text-center mt-8">
            Don't have an account?{' '}
            <Link to="/register" className="text-purple-400 hover:text-purple-300 font-medium transition-colors">
              Create one free
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
