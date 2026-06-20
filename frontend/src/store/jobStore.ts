// src/store/jobStore.ts
import { create } from 'zustand';
import type { Job } from '../api/jobs';
import { getJobs, saveJob, unsaveJob, applyJob } from '../api/jobs';

interface JobState {
  jobs: Job[];
  loading: boolean;
  error: string | null;
  fetchJobs: () => Promise<void>;
  toggleSave: (jobId: string, saved: boolean) => Promise<void>;
  applyToJob: (jobId: string) => Promise<void>;
}

export const useJobStore = create<JobState>((set, get) => ({
  jobs: [],
  loading: false,
  error: null,

  fetchJobs: async () => {
    set({ loading: true, error: null });
    try {
      const data = await getJobs();
      set({ jobs: data, loading: false });
    } catch (err: any) {
      set({ error: err.message || 'Failed to load jobs', loading: false });
    }
  },

  toggleSave: async (jobId: string, saved: boolean) => {
    try {
      if (saved) await unsaveJob(jobId);
      else await saveJob(jobId);
      // Refresh list after change
      await get().fetchJobs();
    } catch (err) {
      console.error('Save/unsave error', err);
    }
  },

  applyToJob: async (jobId: string) => {
    try {
      await applyJob(jobId);
      // Optionally update UI – e.g., mark as applied in the jobs array
      const updated = get().jobs.map((j: Job) =>
        j.id === jobId ? { ...j, applied: true } : j
      );
      set({ jobs: updated });
    } catch (err) {
      console.error('Apply error', err);
    }
  },
}));
