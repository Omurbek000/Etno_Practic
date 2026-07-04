import { createContext, useContext, useEffect, useState, useCallback } from "react";
import { loginUser, logoutUser, registerUser, fetchMe } from "../api/endpoints";
import { setTokens, clearTokens } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadMe = useCallback(async () => {
    const access = localStorage.getItem("access");
    if (!access) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      // /users/ возвращает список из одного элемента — текущего пользователя.
      const list = await fetchMe();
      setUser(Array.isArray(list) ? list[0] || null : list);
    } catch {
      clearTokens();
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadMe();
  }, [loadMe]);

  const login = async (username, password) => {
    const data = await loginUser({ username, password });
    setTokens({ access: data.access, refresh: data.refresh });
    await loadMe();
    return data;
  };

  const register = async (payload) => {
    return registerUser(payload);
  };

  const logout = async () => {
    const refresh = localStorage.getItem("refresh");
    try {
      if (refresh) await logoutUser(refresh);
    } catch {
      // даже если бэкенд отказал — чистим токены локально
    }
    clearTokens();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refreshUser: loadMe }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
