import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchStats, triggerAutoApply } from '../api/jobs';
import { useAuthStore } from '../store/authStore';
import {
  User, Mail, Shield, Calendar, Briefcase,
  TrendingUp, CheckCircle2, Clock, Sparkles, ChevronRight, Zap
} from 'lucide-react';

export default function Dashboard() {
  const { user } = useAuthStore();
  const navigate = useNavigate();
  const [statsData, setStatsData] = useState({ totalJobs: 0, totalSavedCVs: 0, totalApplications: 0 });
  const [isApplying, setIsApplying] = useState(false);
  const [toast, setToast] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToast(msg);
    setTimeout(() => setToast(null), 4000);
  };

  useEffect(() => {
    fetchStats()
      .then((data) => {
        setStatsData({
          totalJobs: data.total_jobs ?? 0,
          totalSavedCVs: data.total_saved_cvs ?? 0,
          totalApplications: data.total_applications ?? 0,
        });
      })
      .catch((err) => console.error('Failed to fetch stats', err));
  }, []);


  const colorMap: Record<string, string> = {
  violet: 'from-violet-500/20 to-violet-600/5 border-violet-500/20 text-violet-400',
  emerald: 'from-emerald-500/20 to-emerald-600/5 border-emerald-500/20 text-emerald-400',
  purple: 'from-purple-500/20 to-purple-600/5 border-purple-500/20 text-purple-400',
  fuchsia: 'from-fuchsia-500/20 to-fuchsia-600/5 border-fuchsia-500/20 text-fuchsia-400',
};
  const createdAt = user?.created_at
    ? new Date(user.created_at).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
    : '—';

  // Define stats array based on fetched data
  const stats = [
    { label: 'Applications Sent', value: statsData.totalApplications.toString(), icon: Briefcase, color: 'violet' },
    { label: 'Interviews Scheduled', value: '0', icon: CheckCircle2, color: 'emerald' },
    { label: 'Match Score Avg', value: 'N/A', icon: TrendingUp, color: 'purple' },
    { label: 'Jobs Tracked', value: statsData.totalJobs.toString(), icon: Clock, color: 'fuchsia' },
  ];

  return (
    <div className="w-full space-y-8 relative">
      {/* Decorative blurs */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-purple-900/10 rounded-full blur-[80px] pointer-events-none z-0" />

      {/* Toast notification */}
      {toast && (
        <div className="fixed top-6 right-6 z-50 px-5 py-3 rounded-xl bg-emerald-500/20 border border-emerald-500/30 text-emerald-300 text-sm font-medium flex items-center gap-2 shadow-xl animate-pulse">
          <Zap className="w-4 h-4" />
          {toast}
        </div>
      )}

      {/* Welcome banner */}
      <div className="relative z-10 glass-card rounded-2xl p-6 sm:p-8 flex flex-col sm:flex-row sm:items-center justify-between gap-5">
        <div>
          <p className="text-sm font-medium text-purple-400 mb-1 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5" />
            Welcome back
          </p>
          <h1 className="text-2xl sm:text-3xl font-bold text-white">
            {user?.name} 👋
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Here's your JobHunt AI overview. Your automation journey starts here.
          </p>
        </div>
        <div className="flex-shrink-0">
          <span className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm font-semibold border ${user?.plan === 'pro' ? 'bg-gradient-to-r from-amber-500/20 to-yellow-600/10 border-amber-500/30 text-amber-300' : 'bg-gradient-to-r from-slate-700/40 to-slate-800/20 border-slate-700/40 text-slate-300'}`}>
            <Shield className="w-4 h-4" />
            {user?.plan?.toUpperCase()} Plan
          </span>
        </div>
      </div>

      {/* Stats grid */}
      <div className="relative z-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {stats.map(({ label, value, icon: Icon, color }) => (
          <div
            key={label}
            className={`glass-card rounded-2xl p-5 border bg-gradient-to-br ${colorMap[color]} hover:scale-[1.02] transition-all duration-300 cursor-default`}
          >
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">{label}</span>
              <Icon className={`w-5 h-5 ${colorMap[color].split(' ').find(c => c.startsWith('text-'))}`} />
            </div>
            <p className="text-3xl font-bold text-white">{value}</p>
          </div>
        ))}
      </div>

      {/* Main content area */}
      <div className="relative z-10 grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Card */}
        <div className="glass-card rounded-2xl p-6 space-y-4">
          <h2 className="text-base font-semibold text-white border-b border-slate-800 pb-3">Account Details</h2>

          <div className="space-y-3">
            <div className="flex items-center gap-3 text-sm">
              <div className="w-8 h-8 rounded-lg bg-violet-500/10 border border-violet-500/20 flex items-center justify-center text-violet-400 flex-shrink-0">
                <User className="w-4 h-4" />
              </div>
              <div>
                <p className="text-slate-500 text-xs">Full Name</p>
                <p className="text-slate-200 font-medium">{user?.name}</p>
              </div>
            </div>

            <div className="flex items-center gap-3 text-sm">
              <div className="w-8 h-8 rounded-lg bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 flex-shrink-0">
                <Mail className="w-4 h-4" />
              </div>
              <div>
                <p className="text-slate-500 text-xs">Email</p>
                <p className="text-slate-200 font-medium truncate max-w-[160px]">{user?.email}</p>
              </div>
            </div>

            <div className="flex items-center gap-3 text-sm">
              <div className="w-8 h-8 rounded-lg bg-fuchsia-500/10 border border-fuchsia-500/20 flex items-center justify-center text-fuchsia-400 flex-shrink-0">
                <Shield className="w-4 h-4" />
              </div>
              <div>
                <p className="text-slate-500 text-xs">Role</p>
                <p className="text-slate-200 font-medium capitalize">{user?.role?.replace('_', ' ')}</p>
              </div>
            </div>

            <div className="flex items-center gap-3 text-sm">
              <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 flex-shrink-0">
                <Calendar className="w-4 h-4" />
              </div>
              <div>
                <p className="text-slate-500 text-xs">Member Since</p>
                <p className="text-slate-200 font-medium">{createdAt}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="lg:col-span-2 glass-card rounded-2xl p-6">
          <h2 className="text-base font-semibold text-white border-b border-slate-800 pb-3 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {[
              { title: 'Upload Resume / CV', desc: 'Add your resume for AI keyword matching', color: 'violet', action: () => navigate('/profile') },
              { title: 'Set Job Preferences', desc: 'Define roles, location & salary range', color: 'purple', action: () => navigate('/profile') },
              { 
                title: 'Start Auto-Apply', 
                desc: isApplying ? 'Starting...' : 'Let AI apply to matching jobs overnight', 
                color: 'fuchsia', 
                action: async () => {
                  try {
                    setIsApplying(true);
                    await triggerAutoApply();
                    showToast('Auto-Apply started! Check Applications tab later.');
                  } catch (e) {
                    showToast('Failed to start auto apply. Are you logged in?');
                  } finally {
                    setIsApplying(false);
                  }
                }
              },
              { title: 'View Applications', desc: 'Track the status of all submitted jobs', color: 'emerald', action: () => navigate('/applications') },
            ].map(({ title, desc, color, action }) => (
              <button
                key={title}
                onClick={action}
                disabled={isApplying && title === 'Start Auto-Apply'}
                className={`text-left p-4 rounded-xl border border-slate-800 hover:border-${color}-500/30 bg-slate-900/30 hover:bg-${color}-500/5 transition-all duration-200 group`}
              >
                <div className="flex items-center justify-between">
                  <p className="text-sm font-semibold text-white">{title}</p>
                  <ChevronRight className="w-4 h-4 text-slate-600 group-hover:text-slate-400 group-hover:translate-x-0.5 transition-all" />
                </div>
                <p className="text-xs text-slate-500 mt-1">{desc}</p>
              </button>
            ))}
          </div>
          <p className="text-xs text-slate-600 mt-5 text-center">
            🚀 More features coming soon — upgrade to Pro for priority access
          </p>
        </div>
      </div>
    </div>
  );
}
