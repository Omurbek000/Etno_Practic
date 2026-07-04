import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchFilm } from "../api/endpoints";
import { mediaUrl } from "../api/client";
import { Loader, ErrorState } from "../components/States";
import FavoriteButton from "../components/FavoriteButton";
import ReviewSection from "../components/ReviewSection";

export default function FilmDetail() {
  const { id } = useParams();
  const [film, setFilm] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    setFilm(null);
    setError(false);
    fetchFilm(id)
      .then(setFilm)
      .catch(() => setError(true));
  }, [id]);

  if (error) return <div className="container"><ErrorState message="Фильм не найден или доступен только по подписке VIP." /></div>;
  if (!film) return <Loader />;

  return (
    <div className="container">
      <div className="detail-hero">
        <div className="detail-poster">
          <img src={mediaUrl(film.poster_image)} alt={film.title} />
        </div>
        <div>
          <h1 className="detail-title">{film.title}</h1>
          <div className="detail-meta-row">
            <span>{film.year}</span>
            <span>{film.duration} мин</span>
            <span>{film.language}</span>
            <span>{film.country?.country}</span>
            <span className="tag accent">{film.access_type}</span>
            {film.access_type === "Rent" && film.rent_price && <span className="tag">{film.rent_price} сом</span>}
          </div>
          <div className="detail-meta-row" style={{ marginTop: -8 }}>
            {film.genres?.map((g) => (
              <span className="tag" key={g.id}>
                {g.name}
              </span>
            ))}
          </div>
          <p className="detail-desc">{film.description}</p>
          <div className="detail-actions">
            <FavoriteButton idKey="film_id" matchKey="film" itemId={film.id} />
            {film.trailer && (
              <a className="btn" href={film.trailer} target="_blank" rel="noreferrer">
                Трейлер ↗
              </a>
            )}
          </div>
        </div>
      </div>

      {film.video && (
        <div className="video-wrap">
          <video controls src={mediaUrl(film.video)} poster={mediaUrl(film.poster_image)} />
        </div>
      )}

      {film.persons?.length > 0 && (
        <section style={{ marginBottom: 40 }}>
          <h2 className="section-title" style={{ marginBottom: 14 }}>
            Актёры и режиссёры
          </h2>
          <div className="cast-row">
            {film.persons.map((p) => (
              <div className="cast-item" key={p.id}>
                <img className="cast-photo" src={mediaUrl(p.person_image)} alt={p.last_name} />
                <p className="cast-name">{p.last_name}</p>
              </div>
            ))}
          </div>
        </section>
      )}

      <ReviewSection idKey="film_id" itemId={film.id} />
    </div>
  );
}
