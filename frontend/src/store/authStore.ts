import { create } from 'zustand';
import api, { toFormUrlEncoded } from '../api/axios';

export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  plan: string;
  created_at: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,

  clearError: () => set({ error: null }),

  login: async (email, password) => {
    set({ isLoading: true, error: null });
    try {
      // Login API expects OAuth2 Form Data (username/password)
      await api.post(
        '/auth/login',
        toFormUrlEncoded({ username: email, password: password }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );

      // Fetch the actual user details after a successful login
      const response = await api.get<User>('/auth/me');
      set({
        user: response.data,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Login failed. Please check your credentials.';
      set({ error: errorMsg, isLoading: false, isAuthenticated: false, user: null });
      throw err;
    }
  },

  register: async (name, email, password) => {
    set({ isLoading: true, error: null });
    try {
      // Register user with JSON body
      await api.post('/auth/register', { name, email, password });

      // Automatically log the user in after registration
      await get().login(email, password);
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Registration failed. Try a different email.';
      set({ error: errorMsg, isLoading: false });
      throw err;
    }
  },

  logout: async () => {
    set({ isLoading: true, error: null });
    try {
      await api.post('/auth/logout');
    } catch (err) {
      console.error('Logout error on backend:', err);
    } finally {
      // Always clear local state even if backend logout fails or cookie is already cleared
      set({
        user: null,
        isAuthenticated: false,
        isLoading: false,
      });
    }
  },

  checkAuth: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get<User>('/auth/me');
      set({
        user: response.data,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (err) {
      // User is not logged in or token is invalid
      set({
        user: null,
        isAuthenticated: false,
        isLoading: false,
      });
    }
  },
}));
