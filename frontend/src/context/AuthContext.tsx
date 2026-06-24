import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { User } from '../types';
import api from '../api/axios';

interface AuthContextType { user: User | null; isAuthenticated: boolean; login: (username: string, password: string) => Promise<void>; register: (email: string, username: string, password: string, phone_number?: string) => Promise<void>; logout: () => void; loading: boolean; refreshUser: () => Promise<void>; }

const AuthContext = createContext<AuthContextType>({} as AuthContextType);
export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const fetchUser = async () => { try { const r = await api.get('/users/'); setUser(Array.isArray(r.data) ? r.data[0] : r.data); } catch { localStorage.removeItem('access_token'); localStorage.removeItem('refresh_token'); } };
  useEffect(() => { const t = localStorage.getItem('access_token'); if (t) fetchUser().finally(() => setLoading(false)); else setLoading(false); }, []);
  const login = async (username: string, password: string) => { const r = await api.post('/login/', { username, password }); localStorage.setItem('access_token', r.data.access); localStorage.setItem('refresh_token', r.data.refresh); await fetchUser(); };
  const register = async (email: string, username: string, password: string, phone_number?: string) => { await api.post('/register/', { email, username, password, phone_number }); };
  const logout = () => { const rt = localStorage.getItem('refresh_token'); if (rt) api.post('/logout/', { refresh: rt }).catch(() => {}); localStorage.removeItem('access_token'); localStorage.removeItem('refresh_token'); setUser(null); };
  return <AuthContext.Provider value={{ user, isAuthenticated: !!user, login, register, logout, loading, refreshUser: fetchUser }}>{children}</AuthContext.Provider>;
}
