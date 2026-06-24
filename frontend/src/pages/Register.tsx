import { useState } from 'react';
import type { FormEvent } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { GlassCard, GlassTitle, GlassInput, GlassButton } from '../components/ui';

export default function Register() {
  const [f, setF] = useState({ email: '', username: '', password: '', phone: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [ok, setOk] = useState(false);
  const { register } = useAuth();
  const nav = useNavigate();
  const handleSubmit = async (e: FormEvent) => { e.preventDefault(); setError(''); setLoading(true); try { await register(f.email, f.username, f.password, f.phone || undefined); setOk(true); setTimeout(() => nav('/login'), 1200); } catch (err: any) { setError(err.response?.data ? String(Object.values(err.response.data).flat()[0]) : 'Ошибка'); } finally { setLoading(false); } };
  return (<div className="authPage"><GlassCard className="authCard"><GlassTitle>Театр Етно</GlassTitle>{error && <div className="authError">{error}</div>}{ok && <div className="authOk">Готово! Перенаправление...</div>}<form onSubmit={handleSubmit} className="authForm"><GlassInput placeholder="Имя пользователя" value={f.username} onChange={e => setF({...f, username: e.target.value})} required /><GlassInput type="email" placeholder="Email" value={f.email} onChange={e => setF({...f, email: e.target.value})} required /><GlassInput type="password" placeholder="Пароль" value={f.password} onChange={e => setF({...f, password: e.target.value})} required /><GlassInput placeholder="Телефон" value={f.phone} onChange={e => setF({...f, phone: e.target.value})} /><GlassButton type="submit" disabled={loading || ok}>{loading ? '...' : 'Создать аккаунт'}</GlassButton></form><div className="authLink">Есть аккаунт? <Link to="/login">Войти</Link></div></GlassCard></div>);
}
