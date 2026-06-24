import { Link } from 'react-router-dom';

interface Props {
  id: number; title: string; posterUrl: string;
  rating?: number; accessType?: string;
  type: 'film' | 'series' | 'cartoon';
}

export default function MovieCard({ id, title, posterUrl, rating, accessType, type }: Props) {
  const path = type === 'film' ? `/films/${id}` : type === 'series' ? `/series/${id}` : `/cartoons/${id}`;
  const isPaid = accessType && accessType !== 'Free';

  return (
    <Link to={path} className="movie-card" tabIndex={0}>
      <div className="poster" style={{ backgroundImage: `url(${posterUrl})` }}>
        {isPaid && <span className="badge-paid">{accessType === 'Subscription' ? 'VIP' : 'Аренда'}</span>}
        {rating != null && rating > 0 && <span className="rating">★ {rating.toFixed(1)}</span>}
        <button className="play-button" aria-label={`Смотреть «${title}»`}>▶</button>
        <h3 className="card-title">{title}</h3>
      </div>
    </Link>
  );
}
