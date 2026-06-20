import { useEffect, useState } from 'react';
import { useAuthStore } from '../store/authStore';
import { useJobStore } from '../store/jobStore';
import { getApplications } from '../api/applications';
import type { Application } from '../api/applications';
import { CheckCircle2, Clock, XCircle, Briefcase, Calendar, MapPin, Building } from 'lucide-react';

export default function Applications() {
  const { isAuthenticated } = useAuthStore();
  const { jobs, fetchJobs } = useJobStore();
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isAuthenticated) {
      // Fetch both jobs and applications to merge data
      Promise.all([
        fetchJobs(),
        getApplications().then(setApplications).catch(err => setError(err.message))
      ]).finally(() => setLoading(false));
    }
  }, [isAuthenticated, fetchJobs]);

  if (!isAuthenticated) {
    return <p className="text-center text-slate-400 mt-10">Please log in to view applications.</p>;
  }

  // Helper to merge job details into application
  const getJobDetails = (jobId: string) => {
    return jobs.find((j: any) => j.id === jobId);
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'PENDING': return <Clock className="w-4 h-4 text-amber-400" />;
      case 'APPLIED': return <CheckCircle2 className="w-4 h-4 text-emerald-400" />;
      case 'INTERVIEW': return <Calendar className="w-4 h-4 text-violet-400" />;
      case 'REJECTED': return <XCircle className="w-4 h-4 text-rose-400" />;
      case 'OFFERED': return <Briefcase className="w-4 h-4 text-purple-400" />;
      default: return <Clock className="w-4 h-4 text-slate-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'PENDING': return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
      case 'APPLIED': return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
      case 'INTERVIEW': return 'bg-violet-500/10 text-violet-400 border-violet-500/20';
      case 'REJECTED': return 'bg-rose-500/10 text-rose-400 border-rose-500/20';
      case 'OFFERED': return 'bg-purple-500/10 text-purple-400 border-purple-500/20';
      default: return 'bg-slate-500/10 text-slate-400 border-slate-500/20';
    }
  };

  return (
    <div className="w-full max-w-5xl mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white"><Briefcase className="w-6 h-6 inline-block mr-2" /> Your Applications</h1>
          <p className="text-slate-400 mt-1">Track the status of roles you have applied for.</p>
        </div>
        <div className="glass px-4 py-2 rounded-xl border border-white/5 flex items-center gap-2">
          <span className="text-xl font-bold text-white">{applications.length}</span>
          <span className="text-sm text-slate-400">Total</span>
        </div>
      </div>

      {loading && <p className="text-slate-400 animate-pulse">Loading applications...</p>}
      {error && <p className="text-rose-400">Error: {error}</p>}

      {!loading && !error && applications.length === 0 && (
        <div className="glass-card rounded-2xl p-10 text-center flex flex-col items-center">
          <div className="w-16 h-16 rounded-full bg-slate-800/50 flex items-center justify-center mb-4">
            <Briefcase className="w-8 h-8 text-slate-500" />
          </div>
          <h3 className="text-lg font-medium text-white mb-2">No applications yet</h3>
          <p className="text-slate-400 max-w-sm mb-6">You haven't applied to any jobs yet. Browse available jobs and let AI do the work for you.</p>
          <a href="/jobs" className="px-5 py-2.5 bg-violet-600 hover:bg-violet-500 text-white rounded-xl text-sm font-medium transition-colors">
            Browse Jobs
          </a>
        </div>
      )}

      {!loading && applications.length > 0 && (
        <div className="glass-card rounded-2xl overflow-hidden border border-slate-800">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-900/50 border-b border-slate-800 text-xs uppercase tracking-wider font-medium text-slate-400">
                  <th className="px-6 py-4">Job Details</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4">Applied Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50">
                {applications.map((app) => {
                  const job = getJobDetails(app.job_id);
                  return (
                    <tr key={app.id} className="hover:bg-slate-800/20 transition-colors group">
                      <td className="px-6 py-4">
                        <p className="text-sm font-medium text-slate-200 mb-1">
                          {job?.title || 'Unknown Job'}
                        </p>
                        <div className="flex items-center gap-3 text-xs text-slate-500">
                          <span className="flex items-center"><Building className="w-3.5 h-3.5 mr-1" /> {job?.company || 'Unknown Company'}</span>
                          {job?.location && <span className="flex items-center"><MapPin className="w-3.5 h-3.5 mr-1" /> {job.location}</span>}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(app.status)}`}>
                          {getStatusIcon(app.status)}
                          {app.status}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <span className="text-sm text-slate-400">
                          {app.applied_at ? new Date(app.applied_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'Recently'}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
