import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axios';
import MovieCard from '../components/MovieCard';

export default function Favorites() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => { api.get('/favorite/').then(r => setItems(r.data.film_item || [])).catch(() => setItems([])).finally(() => setLoading(false)); }, []);

  const remove = async (id: number) => { try { await api.delete(`/favoriteitem/${id}/`); setItems(prev => prev.filter(i => i.id !== id)); } catch {} };

  if (loading) return <div style={{ paddingTop: 140, textAlign: 'center', color: 'var(--text-muted)' }}>...</div>;

  return (<div style={{ paddingTop: 100 }}>
    <h2 className="sectionTitle" style={{ padding: '0 28px' }}>Избранное</h2>
    {items.length === 0 ? <div style={{ textAlign: 'center', padding: '60px 40px', maxWidth: 500, margin: '40px auto' }} className="glass-card"><p style={{ fontSize: 48, marginBottom: 12 }}>♡</p><p style={{ color: 'var(--text-secondary)' }}>Пусто</p><Link to="/films" className="btnGhost" style={{ display: 'inline-flex', marginTop: 16, textDecoration: 'none' }}>Найти фильмы</Link></div> : <div className="grid">{items.filter((i: any) => i.film).map((i: any) => <div key={i.id} style={{ position: 'relative' }}><MovieCard id={i.film.id} title={i.film.title} posterUrl={i.film.poster_image || ''} rating={i.film.get_avg_rating} accessType={i.film.access_type} type="film" /><button onClick={() => remove(i.id)} style={{ position: 'absolute', top: 8, right: 8, zIndex: 5, width: 26, height: 26, borderRadius: 8, background: 'rgba(0,0,0,0.6)', border: '1px solid rgba(255,255,255,0.15)', color: 'white', fontSize: 12, cursor: 'pointer', opacity: 0, transition: 'opacity 0.2s' }} onMouseEnter={e => (e.currentTarget.style.opacity = '1')} onMouseLeave={e => (e.currentTarget.style.opacity = '0')}>✕</button></div>)}</div>}
  </div>);
}
