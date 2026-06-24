import { useState, useEffect } from 'react';
import api from '../api/axios';
import { useLang } from '../context/LangContext';
import MovieCard from '../components/MovieCard';
import type { Film, Genre } from '../types';

export default function Films() {
  const { langVersion } = useLang();
  const [films, setFilms] = useState<Film[]>([]);
  const [genres, setGenres] = useState<Genre[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [genre, setGenre] = useState('');
  const [access, setAccess] = useState('');

  useEffect(() => {
    const p: any = { page, page_size: 20 };
    if (genre) p.genres = genre;
    if (access) p.access_type = access;
    setLoading(true);
    api.get('/film/', { params: p }).then(r => { setFilms(r.data.results || r.data); setTotal(r.data.count || 0); }).finally(() => setLoading(false));
  }, [page, genre, access, langVersion]);

  useEffect(() => { api.get('/genre/').then(r => setGenres(r.data.results || r.data)); }, [langVersion]);

  return (<div>
    <div className="filterBar">
      <button className={`filterChip ${!genre && !access ? 'active' : ''}`} onClick={() => { setGenre(''); setAccess(''); setPage(1); }}>Все</button>
      {genres.map(g => <button key={g.id} className={`filterChip ${genre === String(g.id) ? 'active' : ''}`} onClick={() => { setGenre(genre === String(g.id) ? '' : String(g.id)); setAccess(''); setPage(1); }}>{g.name}</button>)}
      <button className={`filterChip ${access === 'Free' ? 'active' : ''}`} onClick={() => { setAccess(access === 'Free' ? '' : 'Free'); setGenre(''); setPage(1); }}>Free</button>
      <button className={`filterChip ${access === 'Subscription' ? 'active' : ''}`} onClick={() => { setAccess(access === 'Subscription' ? '' : 'Subscription'); setGenre(''); setPage(1); }}>VIP</button>
    </div>
    <div className="grid">
      {loading ? Array.from({ length: 10 }).map((_, i) => <div key={i} className="skeleton" />) : films.map(f => <MovieCard key={f.id} id={f.id} title={f.title} posterUrl={f.poster_image || ''} rating={f.get_avg_rating} accessType={f.access_type} type="film" />)}
    </div>
    {total > 20 && <div className="pagination"><button className="pageBtn" disabled={page <= 1} onClick={() => setPage(p => p - 1)}>←</button><span className="pageInfo">{page}/{Math.ceil(total / 20)}</span><button className="pageBtn" disabled={page >= Math.ceil(total / 20)} onClick={() => setPage(p => p + 1)}>→</button></div>}
  </div>);
}
