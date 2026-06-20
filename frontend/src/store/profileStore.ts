import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { getProfile, updateProfile, uploadCV, listCVs } from '../api/profile';

type CV = {
  id: string;
  filename: string;
  file_url: string;
  created_at: string;
};

type Profile = {
  name: string;
  email: string;
  role?: string;
  plan?: string;
  // add any additional fields you need
};

type ProfileState = {
  profile: Profile | null;
  cvs: CV[];
  loading: boolean;
  error: string | null;
  loadProfile: () => Promise<void>;
  saveProfile: (data: Partial<Profile>) => Promise<void>;
  uploadCVFile: (file: File) => Promise<void>;
  loadCVs: () => Promise<void>;
};

export const useProfileStore = create<ProfileState>()(
  devtools((set) => ({
    profile: null,
    cvs: [],
    loading: false,
    error: null,
    async loadProfile() {
      set({ loading: true, error: null });
      try {
        const data = await getProfile();
        set({ profile: data });
      } catch (e) {
        set({ error: (e as Error).message });
      } finally {
        set({ loading: false });
      }
    },
    async saveProfile(data) {
      set({ loading: true, error: null });
      try {
        const updated = await updateProfile(data);
        set({ profile: updated });
      } catch (e) {
        set({ error: (e as Error).message });
      } finally {
        set({ loading: false });
      }
    },
    async uploadCVFile(file) {
      set({ loading: true, error: null });
      try {
        await uploadCV(file);
        // reload CV list after successful upload
        await this.loadCVs();
      } catch (e) {
        set({ error: (e as Error).message });
      } finally {
        set({ loading: false });
      }
    },
    async loadCVs() {
      set({ loading: true, error: null });
      try {
        const list = await listCVs();
        set({ cvs: list });
      } catch (e) {
        set({ error: (e as Error).message });
      } finally {
        set({ loading: false });
      }
    },
  }))
);
