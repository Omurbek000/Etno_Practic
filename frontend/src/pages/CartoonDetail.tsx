import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api/axios';
import { useLang } from '../context/LangContext';
import type { Cartoon } from '../types';

export default function CartoonDetail() {
  const { id } = useParams();
  const { langVersion } = useLang();
  const [c, setC] = useState<Cartoon | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => { api.get(`/cartoon/${id}/`).then(r => setC(r.data)).finally(() => setLoading(false)); }, [id, langVersion]);
  if (loading) return <div><div className="heroSkeleton" /></div>;
  if (!c) return <div style={{ padding: '200px', textAlign: 'center', color: 'var(--text-muted)' }}>Не найдено</div>;
  return (<div><div className="detailHero" style={{ minHeight: 480 }}><div className="detailBg" style={{ backgroundImage: `url(${c.cartoon_image})` }} /><div className="detailGrad" /><div className="container detailContent"><div className="detailInfo"><h1 className="detailTitle">{c.title}</h1><div className="detailMeta"><span>{c.year}</span><span>{c.duration} мин</span><span>{c.age_rating}</span></div><p className="detailDesc">{c.description}</p>{c.trailer_url && <div className="detailBtns"><a href={c.trailer_url} target="_blank" rel="noopener noreferrer" className="btnGhost">🎬 Трейлер</a></div>}<div className="detailTags">{c.genres?.map(g => <span key={g.id} className="tag">{g.name}</span>)}</div></div></div></div></div>);
}
