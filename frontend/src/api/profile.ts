import api from './axios';

export async function getProfile() {
  const res = await api.get('/profile/me');
  return res.data;
}

export async function updateProfile(data: Partial<{ name: string; email: string; }>) {
  const res = await api.put('/profile/me', data);
  return res.data;
}

export async function uploadCV(file: File) {
  const form = new FormData();
  form.append('file', file);
  const res = await api.post('/profile/cv', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
}

export async function listCVs() {
  const res = await api.get('/profile/cv');
  return res.data;
}
