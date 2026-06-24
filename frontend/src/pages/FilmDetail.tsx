import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api/axios';
import { useLang } from '../context/LangContext';
import { useAuth } from '../context/AuthContext';
import { GlassInput, GlassButton } from '../components/ui';
import type { Film, Review } from '../types';

export default function FilmDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const { langVersion } = useLang();
  const [film, setFilm] = useState<Film | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [showPlayer, setShowPlayer] = useState(false);
  const [reviewText, setReviewText] = useState('');
  const [reviewStars, setReviewStars] = useState(5);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => { setLoading(true); Promise.all([api.get(`/film/${id}/`), api.get(`/review/?film_id=${id}`)]).then(([f, r]) => { setFilm(f.data); setReviews(r.data.results || r.data); }).finally(() => setLoading(false)); }, [id, langVersion]);

  const submitReview = async () => { if (!reviewText.trim()) return; setSubmitting(true); try { await api.post('/review/', { film_id: Number(id), text: reviewText, stars: reviewStars }); setReviewText(''); setReviewStars(5); const r = await api.get(`/review/?film_id=${id}`); setReviews(r.data.results || r.data); } catch {} setSubmitting(false); };

  if (loading) return <div><div className="heroSkeleton" /></div>;
  if (!film) return <div style={{ padding: '200px 28px', textAlign: 'center', color: 'var(--text-muted)' }}>Не найдено</div>;

  return (<div>
    <div className="detailHero">
      <div className="detailBg" style={{ backgroundImage: `url(${film.poster_image})` }} />
      <div className="detailGrad" />
      <div className="container detailContent">
        <div className="detailInfo">
          <h1 className="detailTitle">{film.title}</h1>
          <div className="detailMeta">
            {film.get_avg_rating !== undefined && film.get_avg_rating > 0 && <span className="gold" style={{ fontWeight: 700 }}>★ {film.get_avg_rating.toFixed(1)}</span>}
            <span>{film.year}</span><span>{film.duration} мин</span><span>{film.language}</span>
            {film.access_type !== 'Free' && <span style={{ padding: '3px 10px', borderRadius: 8, fontSize: 12, fontWeight: 600, background: 'linear-gradient(135deg, var(--gold), var(--purple))', color: '#050509' }}>{film.access_type === 'Subscription' ? 'VIP' : 'Аренда'}</span>}
          </div>
          <p className="detailDesc">{film.description}</p>
          <div className="detailBtns">
            <button className="btnPlay" onClick={() => setShowPlayer(true)}>▶ Смотреть</button>
            {film.trailer && <a href={film.trailer} target="_blank" rel="noopener noreferrer" className="btnGhost">🎬 Трейлер</a>}
          </div>
          <div className="detailTags">{film.genres?.map(g => <span key={g.id} className="tag">{g.name}</span>)}{film.country && <span className="tag">{film.country.country}</span>}</div>
        </div>
      </div>
    </div>

    {showPlayer && <div className="videoModal" onClick={() => setShowPlayer(false)}><div className="videoBox" onClick={e => e.stopPropagation()}><button className="videoClose" onClick={() => setShowPlayer(false)}>✕</button><div className="videoPlaceholder"><p style={{ fontSize: 48 }}>▶</p><p style={{ marginTop: 12 }}>{film.title}</p></div></div></div>}

    <div className="reviews">
      {film.persons && film.persons.length > 0 && <div style={{ marginBottom: 24 }}><h3 style={{ fontSize: 16, fontWeight: 600, color: 'var(--gold)', marginBottom: 12 }}>Актёры</h3><div style={{ display: 'flex', gap: 14, flexWrap: 'wrap' }}>{film.persons.slice(0, 6).map(p => <div key={p.id} style={{ display: 'flex', alignItems: 'center', gap: 10 }}><img src={p.person_image} alt="" style={{ width: 36, height: 36, borderRadius: 10, objectFit: 'cover' }} /><span style={{ fontSize: 13, color: 'var(--text-secondary)' }}>{p.first_name} {p.last_name}</span></div>)}</div></div>}

      <h3 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Отзывы ({reviews.length})</h3>
      {user && <div className="reviewForm"><select className="glass-input" style={{ width: 70, padding: '10px 6px', marginTop: 0 }} value={reviewStars} onChange={e => setReviewStars(Number(e.target.value))}>{[10,9,8,7,6,5,4,3,2,1].map(s => <option key={s} value={s}>{s}</option>)}</select><GlassInput placeholder="Ваш отзыв..." value={reviewText} onChange={e => setReviewText(e.target.value)} style={{ marginTop: 0, flex: 1 }} /><GlassButton onClick={submitReview} disabled={submitting || !reviewText.trim()} style={{ width: 'auto', padding: '12px 20px', marginTop: 0 }}>{submitting ? '...' : '→'}</GlassButton></div>}
      {reviews.map(r => <div key={r.id} className="reviewItem"><div className="reviewHead"><span className="reviewAuthor">{r.user_review.first_name} {r.user_review.last_name}</span><span className="reviewStars">★ {r.stars}/10</span></div><p className="reviewText">{r.text}</p><span className="reviewDate">{new Date(r.created_date).toLocaleDateString('ru-RU')}</span></div>)}
      {reviews.length === 0 && <p style={{ color: 'var(--text-muted)', padding: '16px 0' }}>Нет отзывов</p>}
    </div>
  </div>);
}
