import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useLang } from '../context/LangContext';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const { lang, setLang, t } = useLang();
  const loc = useLocation();
  const nav = useNavigate();
  const [langOpen, setLangOpen] = useState(false);

  return (
    <>
      <nav className="navbar">
        <div className="navInner">
          <Link to="/" className="navLogo">ТЕАТР ЕТНО</Link>
          <div className="navLinks">
            <Link to="/" className={`navLink ${loc.pathname === '/' ? 'active' : ''}`}>{t('Главная', 'Башкы', 'Bosh')}</Link>
            <Link to="/films" className={`navLink ${loc.pathname === '/films' ? 'active' : ''}`}>{t('Фильмы', 'Тасмалар', 'Filmlar')}</Link>
            <Link to="/series" className={`navLink ${loc.pathname === '/series' ? 'active' : ''}`}>{t('Сериалы', 'Сериал', 'Serial')}</Link>
            <Link to="/cartoons" className={`navLink ${loc.pathname === '/cartoons' ? 'active' : ''}`}>{t('Мульты', 'Мульт', 'Mult')}</Link>
            {isAuthenticated && <Link to="/favorites" className={`navLink ${loc.pathname === '/favorites' ? 'active' : ''}`}>{t('Избранное', 'Тандалган', 'Tanl')}</Link>}
          </div>
          <div className="navRight">
            <div style={{ position: 'relative' }}>
              <button className="langSwitch" onClick={() => setLangOpen(!langOpen)} aria-label="Сменить язык">{lang.toUpperCase()}</button>
              {langOpen && <div className="langMenu">{(['ru','ky','uz'] as const).map(l => <button key={l} className={`langOption ${lang === l ? 'active' : ''}`} onClick={() => { setLang(l); setLangOpen(false); }}>{l === 'ru' ? 'Русский' : l === 'ky' ? 'Кыргызча' : "O'zbekcha"}</button>)}</div>}
            </div>
            {isAuthenticated ? (<><Link to="/profile" className="navIcon" aria-label="Профиль">{user?.username?.[0]?.toUpperCase()}</Link><button className="navLink" onClick={() => { logout(); nav('/'); }} style={{ fontSize: 12, color: 'var(--text-muted)' }}>Выйти</button></>) : (<Link to="/login" className="navLink" style={{ color: 'var(--gold)' }}>Войти</Link>)}
          </div>
        </div>
      </nav>
      {langOpen && <div style={{ position: 'fixed', inset: 0, zIndex: 150 }} onClick={() => setLangOpen(false)} />}
    </>
  );
}
