import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchSeriesDetail } from "../api/endpoints";
import { mediaUrl } from "../api/client";
import { Loader, ErrorState } from "../components/States";
import FavoriteButton from "../components/FavoriteButton";
import ReviewSection from "../components/ReviewSection";

export default function SeriesDetail() {
  const { id } = useParams();
  const [item, setItem] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    setItem(null);
    setError(false);
    fetchSeriesDetail(id)
      .then(setItem)
      .catch(() => setError(true));
  }, [id]);

  if (error) return <div className="container"><ErrorState message="Серия не найдена или доступна только по подписке VIP." /></div>;
  if (!item) return <Loader />;

  return (
    <div className="container">
      <div className="detail-hero">
        <div className="detail-poster">
          <img src={mediaUrl(item.image)} alt={item.title} />
        </div>
        <div>
          <h1 className="detail-title">{item.title}</h1>
          <div className="detail-meta-row">
            <span>{item.year}</span>
            <span>{item.language}</span>
            <span>{item.country?.country}</span>
            <span className="tag accent">{item.access_type}</span>
            {item.season && <span className="tag">Сезон №{item.season}</span>}
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
            <FavoriteButton idKey="series_id" matchKey="series" itemId={item.id} />
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
          <video controls src={mediaUrl(item.video)} poster={mediaUrl(item.image)} />
        </div>
      )}

      {item.persons?.length > 0 && (
        <section style={{ marginBottom: 40 }}>
          <h2 className="section-title" style={{ marginBottom: 14 }}>
            Актёры и режиссёры
          </h2>
          <div className="cast-row">
            {item.persons.map((p) => (
              <div className="cast-item" key={p.id}>
                <img className="cast-photo" src={mediaUrl(p.person_image)} alt={p.last_name} />
                <p className="cast-name">{p.last_name}</p>
              </div>
            ))}
          </div>
        </section>
      )}

      <ReviewSection idKey="series_id" itemId={item.id} />
    </div>
  );
}
