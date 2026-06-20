import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { Sparkles, Briefcase, Zap, ShieldCheck, ArrowRight } from 'lucide-react';

export default function Home() {
  const { isAuthenticated } = useAuthStore();

  return (
    <div className="flex flex-col items-center justify-center py-12 md:py-20 text-center relative w-full">
      {/* Decorative Blur Spheres */}
      <div className="absolute top-10 left-10 w-72 h-72 bg-violet-600/10 rounded-full blur-[80px] pointer-events-none animate-pulse-slow z-0" />
      <div className="absolute bottom-10 right-10 w-80 h-80 bg-fuchsia-600/10 rounded-full blur-[100px] pointer-events-none z-0" />

      {/* Hero Badge */}
      <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-900/80 border border-slate-800 text-xs font-medium text-purple-300 mb-6 shadow-sm relative z-10">
        <Sparkles className="w-3.5 h-3.5" />
        <span>Next Generation AI Job Search</span>
      </div>

      {/* Main Title */}
      <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight text-white mb-6 max-w-4xl leading-tight relative z-10">
        Land Your Dream Job with{' '}
        <span className="bg-gradient-to-r from-violet-400 via-purple-400 to-fuchsia-400 bg-clip-text text-transparent">
          AI Auto-Applications
        </span>
      </h1>

      {/* Subtitle */}
      <p className="text-lg text-slate-450 max-w-2xl mb-10 leading-relaxed relative z-10">
        Let JobHunt AI analyze listings, optimize your resume keywords, and submit high-probability applications automatically—all while you sleep.
      </p>

      {/* Actions */}
      <div className="flex flex-col sm:flex-row gap-4 mb-20 relative z-10">
        <Link
          to={isAuthenticated ? '/dashboard' : '/register'}
          className="px-8 py-4 rounded-xl font-medium text-white bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 shadow-xl shadow-purple-900/25 hover:shadow-purple-900/40 transition-all duration-300 flex items-center justify-center gap-2 group"
        >
          <span>Start Applying Now</span>
          <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
        </Link>
        <Link
          to={isAuthenticated ? '/dashboard' : '/login'}
          className="px-8 py-4 rounded-xl font-medium text-slate-350 bg-slate-900/60 hover:bg-slate-900 hover:text-white border border-slate-800 hover:border-slate-700 transition-all duration-300 flex items-center justify-center"
        >
          Explore Dashboard
        </Link>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl w-full text-left relative z-10">
        {/* Card 1 */}
        <div className="glass-card p-6 rounded-2xl relative group hover:border-purple-500/35 transition-all duration-300">
          <div className="w-12 h-12 rounded-xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center text-violet-400 mb-5 group-hover:scale-110 transition-transform duration-300">
            <Zap className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-semibold text-white mb-2">Automated Applying</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Crawls top job boards (Indeed, LinkedIn) and auto-fills registration, questionnaires, and application forms.
          </p>
        </div>

        {/* Card 2 */}
        <div className="glass-card p-6 rounded-2xl relative group hover:border-purple-500/35 transition-all duration-300">
          <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 mb-5 group-hover:scale-110 transition-transform duration-300">
            <Briefcase className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-semibold text-white mb-2">Tailored Resumes</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Customizes key skills, highlight bullets, and work histories in real-time to match listing descriptors for 95%+ ATS scoring.
          </p>
        </div>

        {/* Card 3 */}
        <div className="glass-card p-6 rounded-2xl relative group hover:border-purple-500/35 transition-all duration-300">
          <div className="w-12 h-12 rounded-xl bg-fuchsia-500/10 border border-fuchsia-500/20 flex items-center justify-center text-fuchsia-400 mb-5 group-hover:scale-110 transition-transform duration-300">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-semibold text-white mb-2">Anti-Detect Guard</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Utilizes randomized user agents, realistic scrolling speed, and unique IP proxy routing to remain undetectable to employer ATS scripts.
          </p>
        </div>
      </div>
    </div>
  );
}
