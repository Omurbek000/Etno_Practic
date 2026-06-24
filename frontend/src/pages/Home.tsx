import { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axios';
import { useLang } from '../context/LangContext';
import MovieCard from '../components/MovieCard';
import type { Film, Series, Cartoon } from '../types';

export default function Home() {
  const { t, langVersion } = useLang();
  const [films, setFilms] = useState<Film[]>([]);
  const [series, setSeries] = useState<Series[]>([]);
  const [cartoons, setCartoons] = useState<Cartoon[]>([]);
  const [freeFilms, setFreeFilms] = useState<Film[]>([]);
  const [loading, setLoading] = useState(true);
  const [hi, setHi] = useState(0);

  useEffect(() => {
    setLoading(true);
    Promise.all([api.get('/film/?page_size=20'), api.get('/series/?page_size=15'), api.get('/cartoon/?page_size=15'), api.get('/film/?page_size=10&access_type=Free')])
      .then(([f, s, c, ff]) => { setFilms(f.data.results || f.data); setSeries(s.data.results || s.data); setCartoons(c.data.results || c.data); setFreeFilms(ff.data.results || ff.data); })
      .finally(() => setLoading(false));
  }, [langVersion]);

  const hf = films.filter(f => f.description && f.poster_image).slice(0, 4);
  const h = hf[hi];
  const nextH = useCallback(() => setHi(p => (p + 1) % hf.length), [hf.length]);
  useEffect(() => { if (hf.length <= 1) return; const id = setInterval(nextH, 6000); return () => clearInterval(id); }, [hf.length, nextH]);

  if (loading) return <div><div className="heroSkeleton" /><div style={{ padding: '40px 28px' }}><div className="grid">{Array.from({ length: 10 }).map((_, i) => <div key={i} className="skeleton" />)}</div></div></div>;

  return (<div>
    {h && <section className="hero">
      <div className="heroBg" style={{ backgroundImage: `url(${h.poster_image})` }} />
      <div className="heroOverlay" />
      <div className="container heroContent">
        <div className="heroText">
          <span className="heroTag">{t('В тренде', 'Тренд', 'Trend')}</span>
          <h1 className="heroTitle">{h.title}</h1>
          <div className="heroMeta">
            {h.get_avg_rating !== undefined && h.get_avg_rating > 0 && <span className="gold">★ {h.get_avg_rating.toFixed(1)}</span>}
            <span>•</span><span>{h.genres?.map(g => g.name).join(' · ')}</span>
            <span>•</span><span>{h.year}</span>
          </div>
          <p className="heroDesc">{h.description}</p>
          <div className="heroBtns">
            <Link to={`/films/${h.id}`} className="btnPlay">▶ {t('Смотреть', 'Көрүү', 'Ko\'rish')}</Link>
            <Link to={`/films/${h.id}`} className="btnGhost">ℹ {t('Подробнее', 'Батафыл', 'Batafsil')}</Link>
          </div>
        </div>
      </div>
    </section>}

    <div className="contentArea">
      {freeFilms.length > 0 && <div className="section">
        <div className="sectionHead"><h2 className="sectionTitle">{t('Бесплатно', 'Бекер', 'Bepul')}</h2></div>
        <div className="scrollRow">{freeFilms.map(f => <MovieCard key={f.id} id={f.id} title={f.title} posterUrl={f.poster_image || ''} rating={f.get_avg_rating} accessType={f.access_type} type="film" />)}</div>
      </div>}

      {films.length > 0 && <div className="section">
        <div className="sectionHead"><h2 className="sectionTitle">{t('Популярные фильмы', 'Популярдуу тасмалар', 'Mashhur filmlar')}</h2><Link to="/films" className="sectionMore">{t('Все', 'Бардыгы', 'Hammasi')} →</Link></div>
        <div className="grid">{films.slice(0, 10).map(f => <MovieCard key={f.id} id={f.id} title={f.title} posterUrl={f.poster_image || ''} rating={f.get_avg_rating} accessType={f.access_type} type="film" />)}</div>
      </div>}

      {series.length > 0 && <div className="section">
        <div className="sectionHead"><h2 className="sectionTitle">{t('Сериалы', 'Сериалдар', 'Seriallar')}</h2><Link to="/series" className="sectionMore">{t('Все', 'Бардыгы', 'Hammasi')} →</Link></div>
        <div className="scrollRow">{series.map(s => <MovieCard key={s.id} id={s.id} title={s.title} posterUrl={s.image || ''} accessType={s.access_type} type="series" />)}</div>
      </div>}

      {cartoons.length > 0 && <div className="section">
        <div className="sectionHead"><h2 className="sectionTitle">{t('Мультфильмы', 'Мультфильмдер', 'Multfilmlar')}</h2><Link to="/cartoons" className="sectionMore">{t('Все', 'Бардыгы', 'Hammasi')} →</Link></div>
        <div className="scrollRow">{cartoons.map(c => <MovieCard key={c.id} id={c.id} title={c.title} posterUrl={c.cartoon_image || ''} accessType={c.access_type} type="cartoon" />)}</div>
      </div>}
    </div>
    <footer className="footer"><p className="footerCopy">© 2026 ТЕАТР ЕТНО</p></footer>
  </div>);
}
