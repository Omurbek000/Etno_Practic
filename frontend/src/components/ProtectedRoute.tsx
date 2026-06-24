import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';

export default function ProtectedRoute({ children }: { children: ReactNode }) {
  if (!localStorage.getItem('access_token')) {
    return (<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', flexDirection: 'column', gap: 16 }}>
      <p style={{ fontSize: 48 }}>🔒</p>
      <p style={{ color: 'var(--text-secondary)', fontSize: 16 }}>Авторизуйтесь</p>
      <Link to="/login" className="btnGhost" style={{ textDecoration: 'none', marginTop: 8, display: 'inline-flex' }}>Войти</Link>
    </div>);
  }
  return <>{children}</>;
}
