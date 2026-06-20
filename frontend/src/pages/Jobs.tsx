import { useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import { useJobStore } from '../store/jobStore';
import { Briefcase, MapPin, Building, Clock } from 'lucide-react';

export default function Jobs() {
  const { isAuthenticated } = useAuthStore();
  const { jobs, loading, error, fetchJobs, applyToJob } = useJobStore();

  useEffect(() => {
    if (isAuthenticated) {
      fetchJobs();
    }
  }, [isAuthenticated, fetchJobs]);

  if (!isAuthenticated) {
    return <p className="text-center text-slate-400 mt-10">Please log in to view jobs.</p>;
  }

  return (
    <div className="w-full max-w-5xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold text-white mb-8"><Briefcase className="w-6 h-6 inline-block mr-2" /> Available Jobs</h1>
      
      {loading && <p className="text-slate-400">Loading jobs...</p>}
      {error && <p className="text-red-400">Error: {error}</p>}
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {!loading && jobs.length === 0 && (
          <p className="text-slate-400">No jobs found.</p>
        )}
        
        {jobs.map((job: any) => (
          <div key={job.id} className="glass-card p-6 flex flex-col justify-between hover:bg-slate-800/50 transition-colors">
            <div>
              <div className="flex items-start justify-between mb-2">
                <h2 className="text-xl font-bold text-white pr-2">{job.title}</h2>
                {job.match_score !== undefined && job.match_score !== null && (
                  <div className={`px-2.5 py-1 rounded-lg text-xs font-bold border flex items-center gap-1 flex-shrink-0 ${
                    job.match_score >= 80 ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' :
                    job.match_score >= 50 ? 'bg-amber-500/20 text-amber-400 border-amber-500/30' :
                    'bg-slate-500/20 text-slate-400 border-slate-500/30'
                  }`}>
                    ✨ {Math.round(job.match_score)}% Match
                  </div>
                )}
              </div>
              <div className="flex flex-wrap gap-4 text-sm text-slate-400 mb-4">
                <span className="flex items-center"><Building className="w-4 h-4 mr-1" /> {job.company}</span>
                {job.location && <span className="flex items-center"><MapPin className="w-4 h-4 mr-1" /> {job.location}</span>}
                {job.type && <span className="flex items-center"><Clock className="w-4 h-4 mr-1" /> {job.type}</span>}
              </div>
              <p className="text-slate-300 text-sm line-clamp-3 mb-4">{job.description}</p>
            </div>
            
            <div className="mt-4 flex justify-end">
              <button 
                onClick={() => applyToJob(job.id)}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-md text-sm font-medium transition-colors"
              >
                Apply Now
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
