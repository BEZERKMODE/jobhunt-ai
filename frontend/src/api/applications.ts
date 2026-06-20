import api from './axios';

export interface Application {
  id: string;
  job_id: string;
  user_id: string;
  status: string;
  applied_at?: string;
}

export async function getApplications(): Promise<Application[]> {
  const resp = await api.get('/applications');
  return resp.data;
}

export async function createApplication(jobId: string): Promise<Application> {
  const resp = await api.post('/applications', { job_id: jobId });
  return resp.data;
}
