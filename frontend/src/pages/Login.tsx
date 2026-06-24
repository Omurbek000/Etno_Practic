import { useState } from 'react';
import type { FormEvent } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { GlassCard, GlassTitle, GlassInput, GlassButton } from '../components/ui';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const nav = useNavigate();
  const handleSubmit = async (e: FormEvent) => { e.preventDefault(); setError(''); setLoading(true); try { await login(username, password); nav('/'); } catch (err: any) { setError(err.response?.data ? String(Object.values(err.response.data).flat()[0]) : 'Ошибка входа'); } finally { setLoading(false); } };
  return (<div className="authPage"><GlassCard className="authCard"><GlassTitle>Театр Етно</GlassTitle>{error && <div className="authError">{error}</div>}<form onSubmit={handleSubmit} className="authForm"><GlassInput placeholder="Имя пользователя" value={username} onChange={e => setUsername(e.target.value)} required /><GlassInput placeholder="Пароль" type="password" value={password} onChange={e => setPassword(e.target.value)} required /><GlassButton type="submit" disabled={loading}>{loading ? '...' : 'Войти'}</GlassButton></form><div className="authLink">Нет аккаунта? <Link to="/register">Регистрация</Link></div></GlassCard></div>);
}
