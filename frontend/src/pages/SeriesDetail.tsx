import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api/axios';
import { useLang } from '../context/LangContext';
import type { Series as S } from '../types';

export default function SeriesDetail() {
  const { id } = useParams();
  const { langVersion } = useLang();
  const [s, setS] = useState<S | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => { api.get(`/series/${id}/`).then(r => setS(r.data)).finally(() => setLoading(false)); }, [id, langVersion]);
  if (loading) return <div><div className="heroSkeleton" /></div>;
  if (!s) return <div style={{ padding: '200px', textAlign: 'center', color: 'var(--text-muted)' }}>Не найдено</div>;
  return (<div><div className="detailHero" style={{ minHeight: 480 }}><div className="detailBg" style={{ backgroundImage: `url(${s.image})` }} /><div className="detailGrad" /><div className="container detailContent"><div className="detailInfo"><h1 className="detailTitle">{s.title}</h1><div className="detailMeta"><span>{s.year}</span><span>{s.language}</span></div><p className="detailDesc">{s.description}</p>{s.trailer_url && <div className="detailBtns"><a href={s.trailer_url} target="_blank" rel="noopener noreferrer" className="btnGhost">🎬 Трейлер</a></div>}<div className="detailTags">{s.genres?.map(g => <span key={g.id} className="tag">{g.name}</span>)}</div></div></div></div></div>);
}
