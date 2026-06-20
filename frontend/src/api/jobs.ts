export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  description: string;
  salary?: number;
  posted_at?: string;
  match_score?: number;
}

export async function getJobs(): Promise<Job[]> {
  const resp = await fetch('/api/v1/jobs', {
    credentials: 'include',
  });
  if (!resp.ok) throw new Error('Failed to fetch jobs');
  const data = await resp.json();
  // Adjust depending on backend response shape
  return data.results ?? data;
}

export async function saveJob(jobId: string): Promise<void> {
  await fetch(`/api/v1/jobs/${jobId}/save`, {
    method: 'POST',
    credentials: 'include',
  });
}

export async function unsaveJob(jobId: string): Promise<void> {
  await fetch(`/api/v1/jobs/${jobId}/save`, {
    method: 'DELETE',
    credentials: 'include',
  });
}

export async function applyJob(jobId: string): Promise<void> {
  await fetch(`/api/v1/jobs/${jobId}/apply`, {
    method: 'POST',
    credentials: 'include',
  });
}

// New function to fetch dashboard statistics

export async function fetchStats(): Promise<{ total_jobs: number; total_saved_cvs: number; total_applications: number }> {
  const resp = await fetch('/api/v1/stats', { credentials: 'include' });
  if (!resp.ok) throw new Error('Failed to fetch stats');
  const data = await resp.json();
  return {
    total_jobs: data.total_jobs ?? 0,
    total_saved_cvs: data.total_saved_cvs ?? 0,
    total_applications: data.total_applications ?? 0,
  };
}

export async function triggerScrape(query: string = "remote software engineer"): Promise<{ status: string }> {
  const resp = await fetch(`/api/v1/jobs/scrape/indeed?query=${encodeURIComponent(query)}`, {
    method: 'POST',
    credentials: 'include',
  });
  if (!resp.ok) throw new Error('Failed to trigger scrape');
  return resp.json();
}

export async function triggerAutoApply(): Promise<{ status: string }> {
  const resp = await fetch('/api/v1/jobs/auto-apply', {
    method: 'POST',
    credentials: 'include',
  });
  if (!resp.ok) throw new Error('Failed to trigger auto apply');
  return resp.json();
}
