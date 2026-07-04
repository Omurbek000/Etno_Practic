import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchCartoon } from "../api/endpoints";
import { mediaUrl } from "../api/client";
import { Loader, ErrorState } from "../components/States";
import FavoriteButton from "../components/FavoriteButton";
import ReviewSection from "../components/ReviewSection";

export default function CartoonDetail() {
  const { id } = useParams();
  const [item, setItem] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    setItem(null);
    setError(false);
    fetchCartoon(id)
      .then(setItem)
      .catch(() => setError(true));
  }, [id]);

  if (error) return <div className="container"><ErrorState message="Мультфильм не найден или доступен только по подписке VIP." /></div>;
  if (!item) return <Loader />;

  return (
    <div className="container">
      <div className="detail-hero">
        <div className="detail-poster">
          <img src={mediaUrl(item.cartoon_image)} alt={item.title} />
        </div>
        <div>
          <h1 className="detail-title">{item.title}</h1>
          <div className="detail-meta-row">
            <span>{item.year}</span>
            <span>{item.duration} мин</span>
            <span>{item.language}</span>
            <span className="tag accent">{item.access_type}</span>
            <span className="tag">{item.age_rating}</span>
          </div>
          <div className="detail-meta-row" style={{ marginTop: -8 }}>
            {item.genres?.map((g) => (
              <span className="tag" key={g.id}>
                {g.name}
              </span>
            ))}
          </div>
          {item.description && <p className="detail-desc">{item.description}</p>}
          <div className="detail-actions">
            <FavoriteButton idKey="cartoon_id" matchKey="cartoon" itemId={item.id} />
            {item.trailer_url && (
              <a className="btn" href={item.trailer_url} target="_blank" rel="noreferrer">
                Трейлер ↗
              </a>
            )}
          </div>
        </div>
      </div>

      {item.video && (
        <div className="video-wrap">
          <video controls src={mediaUrl(item.video)} poster={mediaUrl(item.cartoon_image)} />
        </div>
      )}

      <ReviewSection idKey="cartoon_id" itemId={item.id} />
    </div>
  );
}
