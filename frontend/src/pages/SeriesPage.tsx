import { useState, useEffect } from 'react';
import api from '../api/axios';
import { useLang } from '../context/LangContext';
import MovieCard from '../components/MovieCard';
import type { Series as S, Genre } from '../types';

export default function SeriesPage() {
  const { langVersion } = useLang();
  const [items, setItems] = useState<S[]>([]);
  const [genres, setGenres] = useState<Genre[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [genre, setGenre] = useState('');

  useEffect(() => {
    const p: any = { page, page_size: 20 };
    if (genre) p.genres = genre;
    setLoading(true);
    api.get('/series/', { params: p }).then(r => { setItems(r.data.results || r.data); setTotal(r.data.count || 0); }).finally(() => setLoading(false));
  }, [page, genre, langVersion]);
  useEffect(() => { api.get('/genre/').then(r => setGenres(r.data.results || r.data)); }, [langVersion]);

  return (<div>
    <div className="filterBar">
      <button className={`filterChip ${!genre ? 'active' : ''}`} onClick={() => { setGenre(''); setPage(1); }}>Все</button>
      {genres.map(g => <button key={g.id} className={`filterChip ${genre === String(g.id) ? 'active' : ''}`} onClick={() => { setGenre(genre === String(g.id) ? '' : String(g.id)); setPage(1); }}>{g.name}</button>)}
    </div>
    <div className="grid">
      {loading ? Array.from({ length: 10 }).map((_, i) => <div key={i} className="skeleton" />) : items.map(s => <MovieCard key={s.id} id={s.id} title={s.title} posterUrl={s.image || ''} accessType={s.access_type} type="series" />)}
    </div>
    {total > 20 && <div className="pagination"><button className="pageBtn" disabled={page <= 1} onClick={() => setPage(p => p - 1)}>←</button><span className="pageInfo">{page}/{Math.ceil(total / 20)}</span><button className="pageBtn" disabled={page >= Math.ceil(total / 20)} onClick={() => setPage(p => p + 1)}>→</button></div>}
  </div>);
}
