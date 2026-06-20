import React, { useEffect, useState } from 'react';
import { useAuthStore } from '../store/authStore';
import { useProfileStore } from '../store/profileStore';
import { Briefcase, Mail, Shield, Calendar, User, Upload, FileText, CheckCircle2, AlertCircle } from 'lucide-react';

export default function Profile() {
  const { isAuthenticated, user } = useAuthStore();
  const { profile, cvs, loading, error, loadProfile, saveProfile, uploadCVFile, loadCVs } = useProfileStore();

  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({ name: '', summary: '', skills: '' });
  const [uploadingCV, setUploadingCV] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      loadProfile();
      loadCVs();
    }
  }, [isAuthenticated, loadProfile, loadCVs]);

  useEffect(() => {
    if (profile) {
      setFormData({
        name: profile.name || user?.name || '',
        summary: (profile as any).summary || '',
        skills: (profile as any).skills?.join(', ') || ''
      });
    }
  }, [profile, user]);

  if (!isAuthenticated) {
    return <p className="text-center text-slate-400 mt-10">Please log in to view your profile.</p>;
  }

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    await saveProfile({
      name: formData.name,
      // Pass other fields depending on schema (backend expects updating via profile/me endpoint)
    });
    setIsEditing(false);
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setUploadingCV(true);
      await uploadCVFile(e.target.files[0]);
      setUploadingCV(false);
    }
  };

  return (
    <div className="w-full max-w-5xl mx-auto p-6 space-y-8">
      <h1 className="text-3xl font-bold text-white mb-2"><User className="w-6 h-6 inline-block mr-2" /> Your Profile</h1>
      <p className="text-slate-400">Manage your personal details and resumes</p>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 flex items-center gap-2">
          <AlertCircle className="w-5 h-5" />
          <span>{error}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Details */}
        <div className="lg:col-span-2 space-y-6">
          <div className="glass-card rounded-2xl p-6 sm:p-8">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-white">Personal Information</h2>
              {!isEditing && (
                <button 
                  onClick={() => setIsEditing(true)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-sm transition-colors"
                >
                  Edit Profile
                </button>
              )}
            </div>

            {loading && !profile && <p className="text-slate-400 animate-pulse">Loading profile...</p>}

            {!isEditing ? (
              <div className="space-y-5">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-violet-500/20 flex items-center justify-center text-violet-400">
                    <User className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="text-xs text-slate-500 uppercase font-medium">Full Name</p>
                    <p className="text-slate-200 text-lg">{profile?.name || user?.name || 'Anonymous'}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400">
                    <Mail className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="text-xs text-slate-500 uppercase font-medium">Email Address</p>
                    <p className="text-slate-200 text-lg">{profile?.email || user?.email}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400">
                    <Briefcase className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="text-xs text-slate-500 uppercase font-medium">Professional Summary</p>
                    <p className="text-slate-200">{formData.summary || 'No summary provided.'}</p>
                  </div>
                </div>
              </div>
            ) : (
              <form onSubmit={handleSave} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-400 mb-1">Full Name</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="glass-input w-full px-4 py-2.5 rounded-xl text-white text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-400 mb-1">Professional Summary</label>
                  <textarea
                    value={formData.summary}
                    onChange={(e) => setFormData({ ...formData, summary: e.target.value })}
                    rows={4}
                    className="glass-input w-full px-4 py-2.5 rounded-xl text-white text-sm resize-none"
                    placeholder="Briefly describe your experience and goals..."
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-400 mb-1">Skills (comma separated)</label>
                  <input
                    type="text"
                    value={formData.skills}
                    onChange={(e) => setFormData({ ...formData, skills: e.target.value })}
                    className="glass-input w-full px-4 py-2.5 rounded-xl text-white text-sm"
                    placeholder="React, Python, AWS..."
                  />
                </div>
                <div className="flex gap-3 pt-2">
                  <button
                    type="submit"
                    className="px-5 py-2.5 bg-violet-600 hover:bg-violet-500 text-white font-medium rounded-xl transition-colors"
                  >
                    Save Changes
                  </button>
                  <button
                    type="button"
                    onClick={() => setIsEditing(false)}
                    className="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-white font-medium rounded-xl transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>

        {/* Right Column: CVs and Stats */}
        <div className="space-y-6">
          <div className="glass-card rounded-2xl p-6">
            <h2 className="text-lg font-bold text-white mb-4">Your Resumes</h2>
            
            <div className="space-y-3 mb-6">
              {cvs.length === 0 ? (
                <p className="text-sm text-slate-400 italic">No resumes uploaded yet.</p>
              ) : (
                cvs.map((cv) => (
                  <div key={cv.id} className="p-3 rounded-xl bg-slate-800/50 border border-slate-700 flex items-center justify-between group">
                    <div className="flex items-center gap-3 overflow-hidden">
                      <div className="p-2 rounded-lg bg-blue-500/20 text-blue-400 flex-shrink-0">
                        <FileText className="w-4 h-4" />
                      </div>
                      <div className="truncate">
                        <p className="text-sm text-slate-200 font-medium truncate">{cv.filename}</p>
                        <p className="text-xs text-slate-500">{cv.created_at ? new Date(cv.created_at).toLocaleDateString() : ''}</p>
                      </div>
                    </div>
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                ))
              )}
            </div>

            <label className="relative flex flex-col items-center justify-center w-full h-32 border-2 border-slate-700 border-dashed rounded-xl cursor-pointer hover:bg-slate-800/50 hover:border-violet-500/50 transition-all">
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                {uploadingCV ? (
                  <div className="w-6 h-6 border-2 border-violet-500 border-t-transparent rounded-full animate-spin mb-2" />
                ) : (
                  <Upload className="w-6 h-6 text-slate-400 mb-2" />
                )}
                <p className="text-sm text-slate-400">
                  <span className="font-semibold text-violet-400">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs text-slate-500 mt-1">PDF, DOCX up to 5MB</p>
              </div>
              <input type="file" className="hidden" accept=".pdf,.doc,.docx" onChange={handleFileChange} disabled={uploadingCV} />
            </label>
          </div>

          <div className="glass-card rounded-2xl p-6">
            <h2 className="text-lg font-bold text-white mb-4">Account Status</h2>
            <div className="space-y-4">
              <div className="flex justify-between items-center pb-3 border-b border-slate-800">
                <span className="text-sm text-slate-400 flex items-center gap-2"><Shield className="w-4 h-4" /> Role</span>
                <span className="text-sm text-slate-200 capitalize bg-slate-800 px-2.5 py-1 rounded-md">{user?.role?.replace('_', ' ') || 'User'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-400 flex items-center gap-2"><Calendar className="w-4 h-4" /> Joined</span>
                <span className="text-sm text-slate-200">{user?.created_at ? new Date(user.created_at).toLocaleDateString() : '—'}</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
